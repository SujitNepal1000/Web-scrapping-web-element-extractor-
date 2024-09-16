from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import pandas as pd

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

    def add_element(name, tag, attrs, text=None):
        locators = []
        
        # Generate XPath based on attributes or text
        if text:
            locators.append(f"XPath: //{tag}[text()='{text}']")
        elif 'id' in attrs:
            locators.append(f"XPath: //{tag}[@id='{attrs['id']}']")
        elif 'class' in attrs:
            locators.append(f"XPath: //{tag}[contains(@class,'{' '.join(attrs['class'])}')]")
        else:
            locators.append(f"XPath: //{tag}")

        # Add class, id, and CSS selectors
        if 'id' in attrs:
            locators.append(f"ID: {attrs['id']}")
        if 'class' in attrs:
            locators.append(f"Class: {' '.join(attrs['class'])}")
        if tag:
            locators.append(f"CSS Selector: {tag}")

        if 'href' in attrs:
            locators.append(f"Full Link: {attrs['href']}")
            locators.append(f"Partial Link: {attrs['href'].split('/')[-1]}")

        elements.append({
            "Name": name,
            "XPath": locators[0] if locators else '',
            "ID": locators[1] if len(locators) > 1 else '',
            "Class": locators[2] if len(locators) > 2 else '',
            "CSS Selector": locators[3] if len(locators) > 3 else '',
            "Full Link": locators[4] if len(locators) > 4 else '',
            "Partial Link": locators[5] if len(locators) > 5 else '',
        })

    # Define keywords to identify specific elements
    keywords = {
        "button": "Button",
        "title": "Title",
        "a": "Link",
        "input": "Search Bar",
        "card": "Card",
        "filter": "Filter"
    }

    for tag, name in keywords.items():
        for element in soup.find_all(tag):
            attrs = element.attrs
            text = element.get_text(strip=True)

            if tag == "a" and text:
                # Handle <a> tags with specific text
                add_element(f"Link - {text}", tag, attrs, text=text)
            elif tag == "button" and text:
                # Handle <button> tags with specific text
                add_element(f"Button - {text}", tag, attrs, text=text)
            else:
                add_element(name, tag, attrs)

    # Create DataFrame
    df = pd.DataFrame(elements)
    return df
