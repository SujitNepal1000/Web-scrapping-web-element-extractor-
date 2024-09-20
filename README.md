Web Scraper with Streamlit and Selenium
This project is a web scraping tool built using Python, Selenium, BeautifulSoup, and Streamlit. It allows users to input a website URL, scrape the webpage, and display the DOM elements (like buttons, links, and headings) along with their XPath, ID, Class, and other locators in a user-friendly table.

Features
Input URL: Enter any website URL to scrape.
Web Element Extraction: The script identifies key HTML elements such as buttons, links, inputs, headings, and more.
Locator Display: For each element found, it provides locators like XPath, ID, Class, and CSS Selector.
Streamlit Interface: A clean, simple UI for interaction.
Installation
Clone this repository:

bash
Copy code
git clone https://github.com/your-username/web-scraper.git
cd web-scraper
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Install ChromeDriver:

Download ChromeDriver matching your Chrome version.
Add the downloaded chromedriver to your system path or place it in the project directory.
Running the Web Scraper
Start the Streamlit app:

bash
Copy code
streamlit run main.py
Open your browser and go to the URL provided by Streamlit (usually http://localhost:8501).

Input the website URL you want to scrape and click the "Scrape Website" button.

The scraped data will be displayed in a table format showing the locators of the HTML elements found on the page.

Files
main.py: The main script for running the Streamlit web application.
scrape.py: Contains the Testrunner class for handling the Selenium Chrome driver and a function to extract HTML elements using BeautifulSoup.
Example
Once you enter a URL, the scraper will display elements like:

Name	 XPath	                     ID	           Class	      CSS Selector	  Full Link
Button	//button[text()='Submit']	               btn-primary    button	
Link	//a[text()='About Us']	               	   nav-link	      a	              /about
