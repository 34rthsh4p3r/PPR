# gui/profile_generation_page.py
import streamlit as st
from profile_generator import ProfileGenerator
import pandas as pd
import matplotlib.pyplot as plt
import io  # Import io

def profile_generation_page():
    st.title("Profile Generation")

    profile_generator = ProfileGenerator()

    # --- Sidebar for Input ---
    st.sidebar.header("Input Parameters")

    # Depth Selection
    depth_choice = st.sidebar.selectbox("Choose a depth:",
                                        options=[("50-100", 1), ("100-200", 2), ("200-300", 3),
                                                 ("300-400", 4), ("500-600", 5), ("600-700", 6)],
                                        format_func=lambda x: x[0])  # Display text, return value


    # Base Type Selection
    base_type = st.sidebar.selectbox("Choose a base type:",
                                        options=["Rock", "Sand", "Paleosol", "Lake sediment"])

    # Environment Type Selection
    env_type = st.sidebar.selectbox("Choose an environment type:",
                                        options=["Lake", "Peatland", "Wetland"])
    
    # --- Generate Profile Button ---
    if st.sidebar.button("Generate Profile"):
        with st.spinner("Generating profile..."):
            data = profile_generator.generate_profile(depth_choice[1], base_type, env_type) # Use the numeric value.  VERY IMPORTANT!
            if data:
                st.session_state.data = data  # Store data in session state
                df = pd.DataFrame(data)
                st.dataframe(df.style.format("{:.2f}"))  # Format to 2 decimal places


                # --- Display Diagram ---
                fig = profile_generator.generate_diagram(data)
                st.pyplot(fig)
            else:
                st.warning("No data generated. Please check your input parameters.")


    # --- Save Data ---
    if 'data' in st.session_state and st.session_state.data:
        st.sidebar.header("Save Data")
        df_download = pd.DataFrame(st.session_state.data)

        # CSV download
        csv = df_download.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='paleo_profile.csv',
            mime='text/csv',
        )

        # Excel (xlsx) download.  Requires openpyxl.
        excel_buffer = io.BytesIO()  # Use BytesIO
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df_download.to_excel(writer, index=False, sheet_name='Profile Data')
        excel_buffer.seek(0)  # Rewind the buffer to the beginning
        st.sidebar.download_button(
            label="Download data as Excel",
            data=excel_buffer,
            file_name='paleo_profile.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        # Save Diagram
        if 'data' in st.session_state and st.session_state.data:
                st.sidebar.header("Save Diagram")
                # Generate the diagram
                fig = profile_generator.generate_diagram(st.session_state.data)

                # Save diagram as PNG
                buf_png = io.BytesIO()
                fig.savefig(buf_png, format="png")
                buf_png.seek(0)
                st.sidebar.download_button(
                    label="Download Diagram as PNG",
                    data=buf_png,
                    file_name="paleo_profile_diagram.png",
                    mime="image/png",
                )

                # Save diagram as SVG
                buf_svg = io.BytesIO()
                fig.savefig(buf_svg, format="svg")
                buf_svg.seek(0)
                st.sidebar.download_button(
                    label="Download Diagram as SVG",
                    data=buf_svg,
                    file_name="paleo_profile_diagram.svg",
                    mime="image/svg+xml",
                )
            
    # --- Advanced Parameter Adjustment (Sliders) ---
    st.sidebar.header("Advanced Parameter Adjustment")
    if st.sidebar.checkbox("Enable Advanced Adjustment"):
        selected_zone = st.sidebar.selectbox("Select Zone:", options=profile_generator.zones) #Using all zones for simplicity
        selected_base_type = st.sidebar.selectbox("Select Base Type (for Zone 5):", options=["Rock", "Sand", "Paleosol", "Lake sediment"], key="base_type_select") #Added key
        selected_env_type = st.sidebar.selectbox("Select Env. Type (for Zones 1-4):", options=["Lake", "Peatland", "Wetland"], key = "env_type_select") #Added key
        ranges = profile_generator.get_parameter_ranges(selected_base_type, selected_env_type, selected_zone)

        updated_ranges = {}
        for param, (min_val, max_val, trend) in ranges.items():
            if param in ["OM", "IM", "CC", "Clay", "Silt", "Sand"]:
                new_min, new_max = st.sidebar.slider(
                    f"{param} Range (Zone {selected_zone}, Trend: {trend})",
                    0, 100, (int(min_val), int(max_val)), step=1
                )
            else:
                new_min, new_max = st.sidebar.slider(
                    f"{param} Range (Zone {selected_zone}, Trend: {trend})",
                    0, 9999, (int(min_val), int(max_val)), step=1
                )
            updated_ranges[param] = (new_min, new_max, trend) #Keep trend

        if st.sidebar.button("Apply Custom Ranges"):
            profile_generator.custom_ranges[(selected_zone, selected_base_type, selected_env_type)] = updated_ranges # Pass base/env
            st.sidebar.success("Custom ranges applied!")