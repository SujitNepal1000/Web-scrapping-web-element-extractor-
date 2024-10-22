import streamlit as st
from scrape import TestRunner

def main():
    st.title("Web-Locator Scraper")

    # Step 1: Input URL
    website_url = st.text_input("Enter the website URL:")

    # Step 2: Action Components
    st.header("Action Components")
    action_components = st.session_state.get("action_components", [])

    if st.button("Add Action Component"):
        action_components.append({"type": "enter", "locator": "", "value": ""})
        st.session_state.action_components = action_components

    # Action component input fields
    for index, action in enumerate(action_components):
        col1, col2 = st.columns(2)

        with col1:
            action_type = st.selectbox(f"Action Type {index + 1}", ["enter", "click", "verify", "scroll"], key=f"action_type_{index}")
            action_locator = st.text_input(f"Locator {index + 1}", value=action['locator'], key=f"action_locator_{index}")

            # Display value input only for "enter" action
            if action_type == "enter":
                action_value = st.text_input(f"Value {index + 1}", value=action['value'], key=f"action_value_{index}")
            else:
                action_value = ""  # Clear value if not "enter"

            action_components[index] = {"type": action_type, "locator": action_locator, "value": action_value}

        with col2:
            if st.button(f"Remove Action {index + 1}", key=f"remove_action_{index}"):
                action_components.pop(index)
                st.session_state.action_components = action_components
                st.write("Are you sure you want to remove the action.")
                break  # Exit the loop to refresh the display of components

    st.session_state.action_components = action_components

    # Step 3: Scrape Site Button
    if st.button("Scrape Site"):
        testrunner = TestRunner()  # Initialize browser only once when "Scrape Site" is clicked

        try:
            # Start the browser and navigate to the URL
            testrunner.start_browser(website_url)

            # Perform actions if any
            if action_components:
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

            # Now scrape the website regardless of actions
            html_content = testrunner.get_page_source()  # Use get_page_source to get the HTML content
            locators_df = testrunner.extract_locators(html_content)
            st.session_state.locators_df = locators_df  # Store the dataframe in session state

        except Exception as e:
            st.error(f"An error occurred while performing actions: {e}")
        finally:
            testrunner.close_browser()  # Close the browser once done

    else:
        st.warning("Please enter a URL and add action components if you want to perform certain action.")
    
    # Step 4: Display Extracted Web Elements (if available)
    if 'locators_df' in st.session_state and not st.session_state.locators_df.empty:
        st.subheader("Extracted Web Elements:")
        st.dataframe(st.session_state.locators_df)
    else:
        st.write(" ")

if __name__ == "__main__":
    main()
