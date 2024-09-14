import streamlit as st
from scrape import scrape_website,split_dom_content, clean_body_content, extract_body_content


st.title("Web Scraping App")

# Get the website URL from the user
url = st.text_input("Enter the URL of the website you want to scrape:")

# When the button is clicked
if st.button("Scrape Website"):
    if url:  # If the user has entered a URL
        st.write("Scraping the website...")
        try:
            result = scrape_website(url)  # Pass the URL to the scraping function
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)
            
            st.session_state.dom_content = cleaned_content
            
            with st.expander("view DOM content"):
                st.text_area("DOM Content", cleaned_content, height=300)
            st.write("Website scraped successfully!")
            st.code(result)  # Display the scraped HTML content
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid URL.")
