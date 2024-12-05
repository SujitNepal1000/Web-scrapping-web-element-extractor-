from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import pandas as pd
from bs4 import BeautifulSoup
import time

class TestRunner:
    def __init__(self):
        self.driver = None

    def start_browser(self, url, headless=False):
        """Initializes the browser and navigates to the specified URL."""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        try:
            # Initialize Chrome browser
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.driver.maximize_window()
            self.driver.get(url)
            time.sleep(2)  # Wait for page load
            print(f"Successfully opened {url}")
        except Exception as e:
            print(f"Error starting browser: {e}")

    def enter_value(self, locator, value):
        """Enters a value into an input field based on the provided locator."""
        if self.driver:
            try:
                element = self.driver.find_element(By.XPATH, locator)
                element.clear()
                element.send_keys(value)
                time.sleep(1)
                print(f"Entered value: '{value}' into {locator}")
            except Exception as e:
                print(f"Error entering value into {locator}: {e}")
        else:
            print("Browser is not initialized. Call start_browser() first.")

    def click_element(self, locator):
        """Clicks on an element identified by the given locator."""
        if self.driver:
            try:
                element = self.driver.find_element(By.XPATH, locator)
                ActionChains(self.driver).move_to_element(element).click().perform()
                time.sleep(3)
                print(f"Clicked element: {locator}")
            except Exception as e:
                print(f"Error clicking element {locator}: {e}")
        else:
            print("Browser is not initialized. Call start_browser() first.")

    def scroll_to_element(self, locator):
        """Scrolls to an element identified by the locator."""
        if self.driver:
            try:
                element = self.driver.find_element(By.XPATH, locator)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)
                print(f"Scrolled to element: {locator}")
            except Exception as e:
                print(f"Error scrolling to element {locator}: {e}")
        else:
            print("Browser is not initialized. Call start_browser() first.")

    def verify_element(self, locator):
        """Verifies if an element is displayed on the page."""
        if self.driver:
            try:
                element = self.driver.find_element(By.XPATH, locator)
                assert element.is_displayed(), f"Element with locator {locator} is not displayed."
                print(f"Element {locator} is displayed.")
            except Exception as e:
                print(f"Error verifying element {locator}: {e}")
        else:
            print("Browser is not initialized. Call start_browser() first.")

    def get_page_source(self):
        """Returns the page source of the current page."""
        if self.driver:
            return self.driver.page_source
        else:
            print("Browser is not initialized. Call start_browser() first.")
            return None

    def extract_locators(self, html_content):
        """Extracts web locators (XPath, ID, Class, etc.) from the HTML content."""
        if not html_content:
            print("No HTML content provided for locator extraction.")
            return pd.DataFrame()

        soup = BeautifulSoup(html_content, "html.parser")
        elements = []

        def add_element(name, tag, attrs, text=None, placeholder=None):
            """Adds element data to the list of extracted elements."""
            element_data = {
                "Name": text if text else (placeholder if placeholder else name),
                "XPath": '',
                "ID": '',
                "Class": '',
                "CSS Selector": '',
                "Full Link": '',
                "Partial Link": ''
            }

            # Handle Input Fields and Placeholders
            if tag == 'input':
                if 'id' in attrs:
                    element_data["XPath"] = f"//input[@id='{attrs['id']}']"
                elif 'placeholder' in attrs:
                    element_data["XPath"] = f"//input[@placeholder='{attrs['placeholder']}']"
                elif 'name' in attrs:
                    element_data["XPath"] = f"//input[@name='{attrs['name']}']"
                elif 'class' in attrs:
                    class_name = ' '.join(attrs['class'])
                    element_data["XPath"] = f"//input[@class='{class_name}']"
                else:
                    element_data["XPath"] = "//input"
            
            # Handle Button Elements
            elif tag == 'button':
                if text and len(text.strip()) > 0:
                    element_data["XPath"] = f"//button[text()='{text.strip()}']"
                elif 'id' in attrs:
                    element_data["XPath"] = f"//button[@id='{attrs['id']}']"
                elif 'class' in attrs:
                    class_name = ' '.join(attrs['class'])
                    element_data["XPath"] = f"//button[@class='{class_name}']"
                else:
                    element_data["XPath"] = "//button"
            
            # Handle Links
            elif tag == 'a':
                if 'href' in attrs:
                    element_data["XPath"] = f"//a[@href='{attrs['href']}']"
                elif text and len(text.strip()) > 0:
                    element_data["XPath"] = f"//a[normalize-space(text())='{text.strip()}']"
                else:
                    element_data["XPath"] = "//a"

            # Handle other elements like divs, spans, etc.
            elif tag == 'div':
                if 'class' in attrs:
                    class_name = ' '.join(attrs['class'])
                    element_data["XPath"] = f"//div[@class='{class_name}']"
                elif 'id' in attrs:
                    element_data["XPath"] = f"//div[@id='{attrs['id']}']"
                else:
                    element_data["XPath"] = "//div"

            if 'id' in attrs:
                element_data["ID"] = attrs["id"]
            if 'class' in attrs:
                element_data["Class"] = ' '.join(attrs['class'])
            if tag:
                element_data["CSS Selector"] = tag

            if 'href' in attrs:
                element_data["Full Link"] = attrs['href']
                element_data["Partial Link"] = attrs['href'].split('/')[-1]

            elements.append(element_data)

        keywords = {
            "button": "Button",
            "a": "Link",
            "input": "Input/Field",
            "span": "Span",
            "div": "Div",
            "h1": "Heading 1",
            "h2": "Heading 2",
            "h3": "Heading 3",
            "h4": "Heading 4",
            "h5": "Heading 5",
            "h6": "Heading 6"
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
                elif tag == "span" and element.get_text(strip=True):
                    add_element(name, tag, attrs, text=element.get_text(strip=True))
                else:
                    add_element(name, tag, attrs)

        # Return the data in a DataFrame format
        return pd.DataFrame(elements)

    def close_browser(self):
        """Closes the browser."""
        if self.driver:
            self.driver.quit()
            print("Browser closed.")
        else:
            print("Browser is not initialized. Cannot close.")
