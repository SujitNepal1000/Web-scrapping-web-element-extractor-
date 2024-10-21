import streamlit as st
from scrape import TestRunner

def main():
    st.title("Web Scraper")

    # Step 1: Input URL
    website_url = st.text_input("Enter the website URL:")

    # Step 2: Action Components
    st.header("Action Components")
    action_components = st.session_state.get("action_components", [])

    if st.button("Add Action Component"):
        action_components.append({"type": "enter", "locator": "", "value": ""})
        st.session_state.action_components = action_components

    for index, action in enumerate(action_components):
        col1, col2 = st.columns(2)
        
        with col1:
            action_type = st.selectbox(f"Action Type {index + 1}", ["enter", "click", "verify", "scroll"], key=f"action_type_{index}")
            action_locator = st.text_input(f"Locator {index + 1}", value=action['locator'], key=f"action_locator_{index}")
            action_value = st.text_input(f"Value {index + 1}", value=action['value'], key=f"action_value_{index}")
            action_components[index] = {"type": action_type, "locator": action_locator, "value": action_value}
        
        with col2:
            if st.button(f"Remove Action {index + 1}"):
                action_components.pop(index)
                st.session_state.action_components = action_components
                st.experimental_rerun()

    st.session_state.action_components = action_components

    # Step 3: Scrape Site Button
    if st.button("Scrape Site"):
        if website_url and action_components:
            testrunner = TestRunner()  # Initialize browser only once when "Scrape Site" is clicked

            try:
                # Perform actions before scraping
                for action in action_components:
                    if action['type'] == "click":
                        testrunner.click_element(action['locator'])
                    elif action['type'] == "enter":
                        testrunner.enter_value(action['locator'], action['value'])
                    elif action['type'] == "verify":
                        if not testrunner.verify_element(action['locator']):
                            st.warning(f"Element verification failed for {action['locator']}")
                            return
                    elif action['type'] == "scroll":
                        testrunner.scroll_to_element(action['locator'])

                # Now scrape the website
                html_content = testrunner.scrape_website(website_url)
                locators_df = testrunner.extract_locators(html_content)
                st.session_state.locators_df = locators_df  # Store the dataframe in session state

            except Exception as e:
                st.error(f"An error occurred while performing actions: {e}")
            finally:
                testrunner.close_driver()  # Close the browser once done

        else:
            st.warning("Please enter a URL and add action components.")
    
    # Step 4: Display Extracted Web Elements (if available)
    if 'locators_df' in st.session_state:
        st.subheader("Extracted Web Elements:")
        st.dataframe(st.session_state.locators_df)

if __name__ == "__main__":
    main()
