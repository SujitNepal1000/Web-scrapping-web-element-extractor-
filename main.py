import streamlit as st
from scrape import (
    Testrunner,  # Import the Testrunner class
    extract_locators
)
import pandas as pd

# Streamlit UI
st.title("Web Scraper")

# Step 1: Enter Website URL
url = st.text_input("Enter Website URL")

# Step 2: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")

        try:
            # Create an instance of Testrunner
            testrunner = Testrunner()
            
            # Scrape the website content
            html_content = testrunner.scrape_website(url)

            # Extract locators from the HTML content
            locators_df = extract_locators(html_content)

            # Display the locators in a table format
            st.subheader("Web Element Locators")
            st.dataframe(locators_df)

            st.success("Website scraped successfully!")

        except Exception as e:
            st.error(f"An error occurred: {e}")
