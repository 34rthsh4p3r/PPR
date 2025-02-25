# gui/homepage.py
import streamlit as st
import os

def render_homepage():
    # Define the path to the logo and README using relative paths, as in original code
    logo_path = os.path.join(os.path.dirname(__file__), '..', 'PPR.ico')
    readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')

    #Check if the files actually exist
    if not os.path.exists(logo_path):
        st.error(f"Logo file not found at: {logo_path}")
        return  # Exit the function if the logo isn't found
    if not os.path.exists(readme_path):
        st.error(f"README file not found at: {readme_path}")
        return

    st.title("PPR - Paleo Profile Randomizer")

    # Display the logo
    st.image(logo_path, width=100)

    # Read and display the README.md content
    try:
        with open(readme_path, "r", encoding="utf-8") as f:  # Specify UTF-8 encoding
            readme_content = f.read()
        st.markdown(readme_content, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error reading README.md: {e}")