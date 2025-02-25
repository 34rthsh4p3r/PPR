# app.py
import streamlit as st
from gui.homepage import homepage
from gui.profile_generation_page import profile_generation_page
from gui.license_page import license_page
import os

# Set Streamlit page configuration
st.set_page_config(
    page_title="PPR - Paleo Profile Randomizer",
    page_icon="PPR.ico",
    layout="wide"
    initial_sidebar_state="expanded"
    )


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Homepage", "Profile Generation"))
   
    # Initialize session state for tracking current page
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Home"

    # Sidebar navigation buttons
    if st.sidebar.button("Home"):
        st.session_state["current_page"] = "Home"
    if st.sidebar.button("Profile Generation"):
        st.session_state["current_page"] = "Profile Generation"
    if st.sidebar.button("License"):
        st.session_state["current_page"] = "License"

    # Route to the selected page
    current_page = st.session_state["current_page"]

    if current_page == "Homepage":
        homepage()
    elif current_page == "Profile Generation":
        profile_generation_page()
    elif current_page == "License":
        license_page()

if __name__ == "__main__":
    main()