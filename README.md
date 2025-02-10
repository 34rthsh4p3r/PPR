# PPR - Paleo Profile Randomizer

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Project Description

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

Data generation is not purely random.  Values follow trends (increasing, decreasing, stagnant, sporadic, etc.) that are typical of real-world paleoecological datasets, providing a more realistic simulation.  The generated data is displayed in a scrollable table within the application and can be exported as a CSV file.

## Why PPR is Useful

*   **Educational Tool:** Ideal for teaching students about paleoecology, sediment cores, and data interpretation.
*   **Data Simulation:** Generate synthetic datasets for testing data analysis methods, statistical techniques, or visualization tools.
*   **Hypothesis Generation:** Explore different parameter combinations to formulate hypotheses about environmental change.
*   **Data Interpretation Practice:** Develop and refine skills in interpreting paleoecological data.
*   **Model Development:** The underlying data generation algorithms can be adapted for use in more complex models.
*   **Demonstration and Presentation:** Quickly create visually appealing representations of paleoecological data.

## Getting Started

### Prerequisites

1.  **Python:** You need Python 3.7 or later installed.  You can download it from [python.org](https://www.python.org/).
2.  **Libraries:** Install the required libraries using pip:

    ```bash
    pip install tk pillow pandas matplotlib
    ```
    note: if you are on linux you might need to install python3-tk (ubuntu)

### Installation and Usage

1.  **Clone the Repository (or Download):**
    ```bash
    git clone https://github.com/YOUR_USERNAME/PPR.git  # Replace YOUR_USERNAME
    cd PPR
    ```
    (Or download the ZIP file from GitHub and extract it.)

2.  **Run the Application:**

    ```bash
    python PPR.py
    ```

3.  **Using the GUI:**
    *   Select options for Depth, Base Type, and Environment Type using the radio buttons.
    *   Click "Generate Profile".
    *   View the generated data in the table.
    *   Click "Save to .csv" to export the data.  You will be prompted for a filename and location.
    *   Click "Exit" to close the application.

### Creating a Standalone Executable (Optional)

You can create a standalone executable (.exe) using PyInstaller, allowing you to run PPR without a separate Python installation.

1.  **Install PyInstaller:**

    ```bash
    pip install pyinstaller
    ```

2.  **Build the Executable:**

    ```bash
    pyinstaller --onefile --noconsole --add-data="PPR.ico;." --icon=PPR.ico PPR.py
    ```
    *   `--onefile`: Creates a single executable file.
    *   `--noconsole`: Prevents a console window from appearing.
    *   `--add-data="PPR.ico;."`: Includes the icon file in the executable. The `.` specifies the root directory within the executable.
    *   `--icon=PPR.ico`: set the icon to the application

3.  **Find the Executable:** The .exe file will be created in the `dist` folder within the project directory.

## Troubleshooting

*   **`FileNotFoundError: [Errno 2] No such file or directory: 'PPR.ico'`:** Ensure `PPR.ico` is in the same directory as `PPR.py` (or the executable).  If using PyInstaller, verify the `--add-data` option.
*   **`ModuleNotFoundError: No module named 'pandas'` (or similar):**  Install the missing library using `pip install <module_name>`.
*   If you encounter any other issues, please [open an issue](https://github.com/34rthsh4p3r/PPR/issues) on the GitHub repository.  Provide a detailed description of the problem, including the steps to reproduce it, your operating system, and the Python version you are using.

## Contributing

Contributions are welcome!  If you'd like to contribute:

1.  **Fork the repository.**
2.  **Create a new branch:** `git checkout -b feature/your-feature-name`
3.  **Make your changes and commit them:** `git commit -m "Add some feature"`
4.  **Push to the branch:** `git push origin feature/your-feature-name`
5.  **Create a pull request.**

Please follow good coding practices, include clear commit messages, and test your changes thoroughly.

## Maintainer

*   [34rthsh4p3r](https://github.com/34rthsh4p3r)

## Acknowledgments

This project was developed with significant assistance from Google AI Studio (Gemini 2.0 Pro Experimental 02-05) on PyCharm and Visual Studio Code.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
