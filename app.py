# app.py
import streamlit as st
import profile_generation_page
import os

# Set Streamlit page configuration
st.set_page_config(
    page_title="PPR - Paleo Profile Randomizer",
    page_icon="PPR.ico",
    initial_sidebar_state="expanded"
    )

def home_page():
    """
    Displays the Home page for the PPR application, including project
    description, usage instructions, and other relevant information.
    """

    # Display banner image (replace 'banner.png' or 'screenshot.png' with your image)
    # st.image("screenshot.png", use_container_width=True) # Uncomment if you have an image

    st.title("PPR - Paleo Profile Randomizer")
    st.markdown(
        """
        **Welcome to the Paleo Profile Randomizer (PPR) application!**

        This tool generates synthetic paleoecological profile data, simulating information from sediment cores. It's designed for educational purposes, data analysis testing, and exploring paleoenvironmental concepts.
        """
    )

    st.markdown("---")
    st.subheader("Project Description")
    st.markdown("""
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

PPR (Paleo Profile Randomizer) is a Python application designed to generate synthetic paleoecological profile data, simulating the information obtained from sediment cores. This tool allows users to explore how different environmental and geological factors influence the composition of sediment records. PPR is valuable for educational purposes, data analysis testing, hypothesis generation, and model development in paleoecology.

The application generates data based on user-selected parameters:

*   **Depth:** User-defined depth range (e.g., 50-700 cm) with 2 cm intervals.
*   **Zones:** Five distinct zones with randomly assigned percentages (each zone representing 10-60% of the total depth).
*   **Base Type:** Geological base type (Rock, Sand, Paleosol, or Lake Sediment).
*   **Environment Type:** Paleoenvironment (Lake, Peatland, or Wetland).
*   **Parameters:** A comprehensive set of parameters, including:
    *   Loss on Ignition: Organic Matter (OM), Carbonate Content (CC), Inorganic Matter (IM)
    *   Magnetic Susceptibility (MS)
    *   Grain size: Clay, Silt, Sand percentages
    *   Water-soluble geochemical concentrations: Ca, Mg, Na, K
    *   Charcoal abundances
    *   Arboreal pollen (AP) abundances
    *   Non arboreal pollen (NAP) abundances
    *   Mollusc abundances: Warm-loving, Cold-resistant

Data generation is not purely random. Values follow trends (increasing, decreasing, stagnant, sporadic, etc.) that are typical of real-world paleoecological datasets, providing a more realistic simulation. The generated data is displayed in a scrollable table within the application and can be exported as a CSV file.
""")


    st.markdown("---")
    st.subheader("Why PPR is Useful")  # Added this section back
    st.markdown("""
*   **Educational Tool:** Ideal for teaching students about paleoecology.
*   **Data Simulation:** Generate datasets for testing analysis methods.
*   **Hypothesis Generation:** Explore parameter combinations.
*   **Data Interpretation Practice:** Develop interpretation skills.
*   **Model Development:** Adapt algorithms for complex models.
*   **Demonstration and Presentation:** Create visualizations of data.
""")
    st.markdown("---")
    st.subheader("Contributing")
    st.markdown("""
Contributions are welcome! Fork the repository, create a branch, make changes, and submit a pull request.
""")

    st.markdown("---")
    st.subheader("Maintainer")
    st.markdown("""
*   [34rthsh4p3r](https://github.com/34rthsh4p3r)
""")

    st.markdown("---")
    st.subheader("Acknowledgments")
    st.markdown("Developed with assistance from Google AI Studio.")

    st.markdown("---")
    st.subheader("License")
    st.markdown("Licensed under the GNU General Public License v3.0.")


    # Footer (remains the same)
    st.markdown("---")

def main():
    """Main function to handle page navigation."""

    # Initialize session state for tracking current page
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Home"

    # Sidebar navigation buttons
    if st.sidebar.button("Home"):
        st.session_state["current_page"] = "Home"
    if st.sidebar.button("Profile Generation"):
        st.session_state["current_page"] = "Profile Generation"

    # Route to the selected page
    current_page = st.session_state["current_page"]

    if current_page == "Home":
        home_page()  # Correctly call the home_page function
    elif current_page == "Profile Generation":
        profile_generation_page()  # Call the main() function *within* the module

if __name__ == "__main__":
    main()