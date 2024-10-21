import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class TestRunner:
    def __init__(self):
        self.driver = None
        self.initialize_driver()

    def initialize_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920x1080")  # Set window size

        # Initialize the WebDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def scrape_website(self, url):
        self.driver.get(url)
        time.sleep(3)  # Wait for the page to load
        return self.driver.page_source  # Return the page source for further processing

    def close_driver(self):
        if self.driver:
            self.driver.quit()  # Close the browser

    def extract_locators(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        elements = []

        def add_element(name, tag, attrs, text=None, placeholder=None):
            locators = []
            if text and len(text.strip()) > 0:
                locators.append(f"XPath: //{tag}[text()='{text.strip()}']")
            elif 'id' in attrs:
                locators.append(f"XPath: //{tag}[@id='{attrs['id']}']")
            elif 'class' in attrs:
                class_name = ' '.join(attrs['class'])
                locators.append(f"XPath: //{tag}[contains(@class,'{class_name}')]")
            elif placeholder:
                locators.append(f"XPath: //{tag}[@placeholder='{placeholder}']")
            else:
                locators.append(f"XPath: //{tag}")

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
                "Name": text if text else (placeholder if placeholder else name),
                "XPath": locators[0] if locators else '',
                "ID": locators[1] if len(locators) > 1 else '',
                "Class": locators[2] if len(locators) > 2 else '',
                "CSS Selector": locators[3] if len(locators) > 3 else '',
                "Full Link": locators[4] if len(locators) > 4 else '',
                "Partial Link": locators[5] if len(locators) > 5 else '',
            })

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
            "label": "Label",
            "card": "Card",
            "filter": "Filter"
        }

        for tag, name in keywords.items():
            for element in soup.find_all(tag):
                attrs = element.attrs
                if tag == "a" and element.get_text(strip=True):
                    add_element(name, tag, attrs, text=element.get_text(strip=True))
                elif tag == "button" and element.get_text(strip=True):
                    add_element(name, tag, attrs, text=element.get_text(strip=True))
                elif tag.startswith("h") and element.get_text(strip=True):
                    add_element(name, tag, attrs, text=element.get_text(strip=True))
                elif tag == "input" and 'placeholder' in attrs:
                    add_element(name, tag, attrs, placeholder=attrs['placeholder'])
                elif tag == "label":
                    add_element(name, tag, attrs, text=element.get_text(strip=True))
                else:
                    add_element(name, tag, attrs)

        df = pd.DataFrame(elements)
        return df

    def enter_value(self, locator, value):
        """Enter a value into an input field identified by the locator."""
        try:
            element = self.driver.find_element(By.XPATH, locator)
            element.clear()  # Clear existing text
            element.send_keys(value)  # Send the new value
        except Exception as e:
            print(f"Error while entering value: {e}")

    def click_element(self, locator):
        """Click on an element identified by the locator."""
        try:
            element = self.driver.find_element(By.XPATH, locator)
            element.click()
        except Exception as e:
            print(f"Error while clicking element: {e}")

    def verify_element(self, locator):
        """Verify if an element identified by the locator is present."""
        try:
            element = self.driver.find_element(By.XPATH, locator)
            return element.is_displayed()  # Check if the element is displayed
        except Exception as e:
            print(f"Error while verifying element: {e}")
            return False

    def scroll_to_element(self, locator):
        """Scroll to an element identified by the locator."""
        try:
            element = self.driver.find_element(By.XPATH, locator)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)  # Scroll to the element
        except Exception as e:
            print(f"Error while scrolling to element: {e}")
