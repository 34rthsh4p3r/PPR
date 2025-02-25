# gui/license_page.py
import streamlit as st
import os

def license_page():
    st.title("License")

    # Define the path to the LICENSE file
    license_path = os.path.join(os.path.dirname(__file__), '..', 'LICENSE')

    # Check if the file exists
    if not os.path.exists(license_path):
        st.error(f"License file not found at: {license_path}")
        return #Exit if not found

    # Read and display the LICENSE content
    try:
        with open(license_path, "r", encoding="utf-8") as f:
            license_content = f.read()
        st.text(license_content)  # Use st.text for plain text display
    except Exception as e:
        st.error(f"Error reading LICENSE file: {e}")