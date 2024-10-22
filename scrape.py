from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class TestRunner:
    def __init__(self):
        self.driver = None

    def start_browser(self, url):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.driver.get(url)
        time.sleep(2)  # Wait for the page to load

    def enter_value(self, locator, value):
        try:
            element = self.driver.find_element(By.XPATH, locator)
            element.clear()
            element.send_keys(value)
            time.sleep(1)  # Adding delay for better visibility in actions
        except Exception as e:
            raise Exception(f"Error entering value: {e}")

    def click_element(self, locator):
        try:
            element = self.driver.find_element(By.XPATH, locator)
            ActionChains(self.driver).move_to_element(element).click().perform()
            time.sleep(3)  # Wait for action to complete
        except Exception as e:
            raise Exception(f"Error clicking element: {e}")

    def scroll_to_element(self, locator):
        try:
            element = self.driver.find_element(By.XPATH, locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)  # Adding delay for better visibility in actions
        except Exception as e:
            raise Exception(f"Error scrolling to element: {e}")

    def verify_element(self, locator):
        try:
            element = self.driver.find_element(By.XPATH, locator)
            assert element.is_displayed(), f"Element with locator {locator} is not displayed."
        except Exception as e:
            raise Exception(f"Error verifying element: {e}")

    def get_page_source(self):
        return self.driver.page_source

    def extract_locators(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        elements = []

        def add_element(name, tag, attrs, text=None, placeholder=None):
            # Prepare a dictionary for the current element
            element_data = {
                "Name": text if text else (placeholder if placeholder else name),
                "XPath": '',
                "ID": '',
                "Class": '',
                "CSS Selector": '',
                "Full Link": '',
                "Partial Link": ''
            }

            # Determine the XPath locator
            if text and len(text.strip()) > 0:
                element_data["XPath"] = f"//{tag}[text()='{text.strip()}']"
            elif 'id' in attrs:
                element_data["XPath"] = f"//{tag}[@id='{attrs['id']}']"
            elif 'class' in attrs:
                class_name = ' '.join(attrs['class'])
                element_data["XPath"] = f"//{tag}[contains(@class,'{class_name}')]"
            elif placeholder:
                element_data["XPath"] = f"//{tag}[@placeholder='{placeholder}']"
            else:
                element_data["XPath"] = f"//{tag}"

            # Extract other attributes
            if 'id' in attrs:
                element_data["ID"] = attrs["id"]  # Directly use the ID
            if 'class' in attrs:
                element_data["Class"] = ' '.join(attrs['class'])  # Join classes
            if tag:
                element_data["CSS Selector"] = tag  # Use the tag name as CSS Selector

            # Links
            if 'href' in attrs:
                element_data["Full Link"] = attrs['href']
                element_data["Partial Link"] = attrs['href'].split('/')[-1]

            elements.append(element_data)

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

        # Create a DataFrame from the list of elements
        df = pd.DataFrame(elements)

        # Reorder the columns to match the desired output
        df = df[["Name", "XPath", "ID", "Class", "CSS Selector", "Full Link", "Partial Link"]]
        df.index.name = "S.N"  # Set index name as S.N
        df.reset_index(inplace=True)  # Convert index to a column

        return df

    def close_browser(self):
        if self.driver:
            self.driver.quit()
