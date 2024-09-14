from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup


class Testrunner:
    driver = None

    def initialize_driver(self):
        # Use Selenium 4's automatic ChromeDriver management
        options = webdriver.ChromeOptions()
        # Automatically fetches the driver if not present locally
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        return driver

    def scrape_website(self, website):
        print("Launching chrome browser")
        
        try:
            # Initialize the driver
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

# Function to be used by the Streamlit app
def scrape_website(website_url):
    testrunner = Testrunner()
    return testrunner.scrape_website(website_url)

# Modify this function to accept 'html_content' as an argument
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
        
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    
    return cleaned_content

def split_dom_content(dom_content, max_len=6000):
    return [dom_content[i:i + max_len] for i in range(0, len(dom_content), max_len)]
