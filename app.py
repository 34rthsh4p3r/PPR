# app.py
import streamlit as st
from gui.homepage import render_homepage
from gui.profile_generation_page import render_profile_generation_page
import os

# Set Streamlit page configuration
st.set_page_config(page_title="PPR - Paleo Profile Randomizer", page_icon="PPR.ico", layout="wide")


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Homepage", "Profile Generation"))

    if page == "Homepage":
        render_homepage()
    elif page == "Profile Generation":
        render_profile_generation_page()
    elif page == "License":
        render_license_page()

if __name__ == "__main__":
    main()