from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import pandas as pd
import re

class Testrunner:
    driver = None

    def initialize_driver(self):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver

    def scrape_website(self, website):
        print("Launching chrome browser")
        
        try:
            self.driver = self.initialize_driver()
            self.driver.get(website)
            print("Navigated to the website")
            html = self.driver.page_source
            time.sleep(5)
            
            return html
        finally:
            print("Closing the browser")
            if self.driver:
                self.driver.quit()

def extract_locators(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    elements = []

    def add_element(name, tag, attrs, text=None, placeholder=None):
        locators = []

        # Prioritize generating locators based on text content if it exists
        if text and len(text.strip()) > 0:
            locators.append(f"XPath: //{tag}[text()='{text.strip()}']")  # Use text for locating
        elif 'id' in attrs:
            locators.append(f"XPath: //{tag}[@id='{attrs['id']}']")  # Use ID if available
        elif 'class' in attrs:
            class_name = ' '.join(attrs['class'])
            locators.append(f"XPath: //{tag}[contains(@class,'{class_name}')]")  # Use class if no text or ID
        elif placeholder:
            locators.append(f"XPath: //{tag}[@placeholder='{placeholder}']")  # Use placeholder if available
        else:
            locators.append(f"XPath: //{tag}")  # Default to basic XPath if no other locators are suitable

        # Add additional locators (ID, class, and CSS selectors)
        if 'id' in attrs:
            locators.append(f"ID: {attrs['id']}")
        if 'class' in attrs:
            locators.append(f"Class: {' '.join(attrs['class'])}")
        if tag:
            locators.append(f"CSS Selector: {tag}")

        # Handle <a> tags with href attributes for full and partial links
        if 'href' in attrs:
            locators.append(f"Full Link: {attrs['href']}")
            locators.append(f"Partial Link: {attrs['href'].split('/')[-1]}")

        elements.append({
            "Name": text if text else (placeholder if placeholder else name),  # Use text, placeholder, or generic name
            "XPath": locators[0] if locators else '',
            "ID": locators[1] if len(locators) > 1 else '',
            "Class": locators[2] if len(locators) > 2 else '',
            "CSS Selector": locators[3] if len(locators) > 3 else '',
            "Full Link": locators[4] if len(locators) > 4 else '',
            "Partial Link": locators[5] if len(locators) > 5 else '',
        })

    # Define keywords for specific elements
    keywords = {
        "button": "Button",
        "a": "Link",
        "input": "Input/Field",
        "textarea": "Text Area",
        "select": "Dropdown",
        "h1": "Heading 1",
        "h2": "Heading 2",
        "h3": "Heading 3",
        "h4": "Heading 4",
        "h5": "Heading 5",
        "h6": "Heading 6",
        "card": "Card",
        "filter": "Filter"
    }

    # Iterate through all relevant tags and extract locators
    for tag, name in keywords.items():
        for element in soup.find_all(tag):
            attrs = element.attrs
            if tag == "a" and element.get_text(strip=True):
                # Handle <a> tags with text
                add_element(name, tag, attrs, text=element.get_text(strip=True))
            elif tag == "button" and element.get_text(strip=True):
                # Handle <button> tags with text
                add_element(name, tag, attrs, text=element.get_text(strip=True))
            elif tag.startswith("h") and element.get_text(strip=True):
                # Handle headings (h1, h2, etc.) with text
                add_element(name, tag, attrs, text=element.get_text(strip=True))
            elif tag == "input" and 'placeholder' in attrs:
                # Handle <input> fields with placeholder
                add_element(name, tag, attrs, placeholder=attrs['placeholder'])
            else:
                # Default handling for other tags
                add_element(name, tag, attrs)

    # Create DataFrame from the extracted elements
    df = pd.DataFrame(elements)
    return df
