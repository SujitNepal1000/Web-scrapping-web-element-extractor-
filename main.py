import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_openai

# Streamlit UI
st.title("AI Web Scraper")

# Step 1: Enter Website URL
url = st.text_input("Enter Website URL")

# Step 2: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")

        try:
            # Scrape the website content
            dom_content = scrape_website(url)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

            # Store the DOM content in Streamlit session state
            st.session_state.dom_content = cleaned_content

            # Display the DOM content in an expandable text box
            with st.expander("View Scraped DOM Content"):
                st.text_area("DOM Content", cleaned_content, height=300)

            st.success("Website scraped successfully!")

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Step 3: Describe what you want to parse
if "dom_content" in st.session_state:
    st.subheader("Parsing Section")
    
    # Input for the description of what to parse
    parse_description = st.text_area("Describe what you want to parse")

    # Step 4: Parse the content with OpenAI API
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            try:
                # Split DOM content into chunks for parsing
                dom_chunks = split_dom_content(st.session_state.dom_content)

                # Parse the content using OpenAI API
                parsed_result = parse_with_openai(dom_chunks, parse_description)

                # Display the result in the "Prompt Answer" section
                st.subheader("Prompt Answer")
                st.write(parsed_result)

            except Exception as e:
                st.error(f"An error occurred while parsing: {e}")
        else:
            st.warning("Please describe what you want to parse.")
