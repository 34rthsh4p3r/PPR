import tkinter as tk
import tkinter.font as tkFont #For font customization
from tkinter import ttk, filedialog, messagebox
import random
import os
from PIL import Image, ImageTk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import matplotlib.pyplot as plt
from openpyxl import Workbook #For Excel saving


class PaleoProfileRandomizer:

    def __init__(self, master):
        self.master = master
        master.title("PPR - Paleo Profile Randomizer")
        width = 800       # Can be exchanged to: master.winfo_screenwidth()
        height = 600       # Can be exchanged to: master.winfo_screenheight()
        master.geometry("%dx%d" % (width, height))

        # This will open the window in full-size:
        # master.state('zoomed')
        # but you have to remove width, height and master.geometry() lines

        # --- Load and Display Icon ---
        try:
            icon_path = 'PPR.ico'  # Replace PATH with your icon file's path if different
            icon_image = Image.open(icon_path)
            self.icon_photo = ImageTk.PhotoImage(icon_image)
            master.iconphoto(True, self.icon_photo)  
        except Exception as e:
            print(f"Error loading icon: {e}")  # Optional: Handle icon loading failure

        # --- Header Frame ---
        self.header_frame = tk.Frame(master)
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        title_label = tk.Label(self.header_frame, text="Paleo Profile Randomizer",  fg="black", font=("Open Sans", 16, "bold"))
        title_label.pack(side=tk.TOP, expand=True)

        # --- Input Frame ---
        self.input_frame = tk.Frame(master)
        self.input_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        self.create_input_widgets()

        # --- Button Frame ---
        self.button_frame = tk.Frame(master)
        self.button_frame.grid(row=2, column=0, columnspan=3, pady=0)
    
        # --- Generate Profile Button ---
        self.generate_button = ttk.Button(self.button_frame, text="Generate Profile",  command=self.generate_profile, style="OpenSans.TButton")
        self.generate_button.pack(side=tk.LEFT, padx=5)
    
        # --- Save Buttons ---
        self.save_csv_button = ttk.Button(self.button_frame, text="Save to .csv", command=self.save_data_to_csv, style="OpenSans.TButton")
        self.save_csv_button.pack(side=tk.LEFT, padx=5)

        self.save_xlsx_button = ttk.Button(self.button_frame, text="Save to .xlsx", command=self.save_data_to_xlsx, style="OpenSans.TButton")
        self.save_xlsx_button.pack(side=tk.LEFT, padx=5)
    
        # --- Exit Button ---
        self.exit_button = ttk.Button(self.button_frame, text="Exit", command=master.destroy, style="OpenSans.TButton")
        self.exit_button.pack(side=tk.LEFT, padx=5)

        # --- Output Frame ---
        self.output_frame = tk.Frame(master)
        self.output_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # --- Scrollbars ---
        self.h_scrollbar = ttk.Scrollbar(self.output_frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scrollbar = ttk.Scrollbar(self.output_frame, orient=tk.VERTICAL)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Table Canvas ---
        self.table_canvas = tk.Canvas(self.output_frame, highlightthickness=0,
                                     xscrollcommand=self.h_scrollbar.set,
                                     yscrollcommand=self.v_scrollbar.set)
        self.table_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.table_frame = tk.Frame(self.table_canvas)
        self.table_canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        self.h_scrollbar.config(command=self.table_canvas.xview)
        self.v_scrollbar.config(command=self.table_canvas.yview)
        self.table_frame.bind("<Configure>", self.on_frame_configure)

        # --- Bottom Frame (for version info) ---
        self.bottom_frame = tk.Frame(master)
        self.bottom_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=0, pady=0) #row 4
        version_label = tk.Label(self.bottom_frame, text="Updated on 10 February 2025",  fg="black", font=("Open Sans", 10, "italic"))
        version_label.pack(side=tk.TOP, pady=(0,0))  # Reduce padding

        # Create a clickable link label for "34rthsh4p3r"
        link_label = tk.Label(self.bottom_frame, text="34rthsh4p3r", fg="teal", cursor="hand2", font=("Open Sans", 10, "bold"))
        link_label.pack(side=tk.TOP, pady=(0,0)) # Reduce padding
        link_label.bind("<Button-1>", lambda e: self.open_url("https://github.com/34rthsh4p3r/PPR"))

        # --- Configure Row Weights ---
        master.rowconfigure(3, weight=1)  # Output frame should expand vertically
        master.columnconfigure(0, weight=1) # Make frames fill entire width
        self.output_frame.columnconfigure(0, weight=1) #canvas should fill output_frame
    
    def open_url(self, url):
        import webbrowser
        webbrowser.open_new(url)

    def create_input_widgets(self):
        """Creates and centers the radio buttons and labels."""

        # --- Input Frame Centering ---
        # Use a container frame for ALL input elements, and center it.
        self.input_container = tk.Frame(self.input_frame)
        self.input_container.pack(expand=True) # Key: Center the container

        # --- Depth Selection ---
        depth_label = tk.Label(self.input_container, text="Choose a depth:", fg="black")
        depth_label.grid(row=0, column=0, sticky="ew")  # Stretch label
        self.input_container.columnconfigure(0, weight=1) # Allow label column to expand

        self.depth_var = tk.IntVar()
        depth_options = [("50-100", 1), ("100-200", 2), ("200-300", 3), ("300-400", 4), ("500-600", 5), ('600-700', 6)]  # Add more options if needed
        # Frame for radio buttons
        depth_rb_frame = tk.Frame(self.input_container)
        depth_rb_frame.grid(row=1, column=0, sticky="nsew") # Use nsew
        depth_rb_frame.columnconfigure(0, weight=1) #make the frame fill the whole row

        # Inner frame for centering radio buttons
        inner_depth_frame = tk.Frame(depth_rb_frame)
        inner_depth_frame.grid(row=0, column=0)

        for i, (text, value) in enumerate(depth_options):
            rb = ttk.Radiobutton(inner_depth_frame, text=text, variable=self.depth_var, value=value)
            rb.pack(side=tk.LEFT, padx=5)  # Pack within inner frame


        # --- Base Type Selection ---
        base_label = tk.Label(self.input_container, text="Choose a base type:", fg="black")
        base_label.grid(row=2, column=0, sticky="ew")
        self.input_container.columnconfigure(0, weight=1)

        self.base_type_var = tk.StringVar()
        base_type_options = [("Rock", "Rock"), ("Sand", "Sand"), ("Paleosol", "Paleosol"), ("Lake sediment", "Lake sediment")]

        base_rb_frame = tk.Frame(self.input_container)
        base_rb_frame.grid(row=3, column=0, sticky="nsew")  # Stretch frame
        base_rb_frame.columnconfigure(0, weight=1)

        inner_base_frame = tk.Frame(base_rb_frame)
        inner_base_frame.grid(row=0, column=0)


        for i, (text, value) in enumerate(base_type_options):
            rb = ttk.Radiobutton(inner_base_frame, text=text, variable=self.base_type_var, value=value)
            rb.pack(side=tk.LEFT, padx=5)  # Pack within inner frame



        # --- Environment Type Selection ---
        env_label = tk.Label(self.input_container, text="Choose an environment type:",  fg="black")
        env_label.grid(row=4, column=0, sticky="ew")
        self.input_container.columnconfigure(0, weight=1)

        self.env_type_var = tk.StringVar()
        env_type_options = [("Lake", "Lake"), ("Peatland", "Peatland"), ("Wetland", "Wetland")]

        env_rb_frame = tk.Frame(self.input_container)
        env_rb_frame.grid(row=5, column=0, sticky="nsew")  # Stretch frame
        env_rb_frame.columnconfigure(0, weight=1)

        inner_env_frame = tk.Frame(env_rb_frame)
        inner_env_frame.grid(row=0, column=0)

        for i, (text, value) in enumerate(env_type_options):
            rb = ttk.Radiobutton(inner_env_frame, text=text, variable=self.env_type_var, value=value)
            rb.pack(side=tk.LEFT, padx=5)

    

    def generate_unique_zone_percentages(self):
        """Generates 5 unique random numbers that sum to 100."""
        while True:
            nums = [random.uniform(10, 60) for _ in range(4)]
            if len(set(nums)) == 4:
                remaining = 100 - sum(nums)
                if 10 <= remaining <= 60:
                    nums.append(remaining)
                    random.shuffle(nums)
                    return nums

    def assign_depths_to_zones(self, depth, zone_percentages):
        """Assigns depths to zones based on percentages."""
        zones = {}
        current_depth = 0
        for i, percentage in enumerate(zone_percentages):
            zone_end = current_depth + (depth * percentage / 100)
            zones[i + 1] = (current_depth, float(round(zone_end / 2) * 2))
            current_depth = float(round(zone_end / 2) * 2)
        return zones

    def generate_data(self, depth, zones, base_type, env_type):
        """Generates the data for the table."""
        data = []  # Local data
        depth_values = list(range(0, depth + 1, 2))

        for d in depth_values:
            # Determine the zone
            zone_num = None
            for z, (start, end) in zones.items():
                if start <= d <= end:
                    zone_num = z
                    break


            ranges = self.get_parameter_ranges(base_type, env_type, zone_num)

            row = {
                "Depth": d,
                "Zone": zone_num,
                "OM": 0, "CC": 0, "IM": 0,
                "Clay": 0, "Silt": 0, "Sand": 0,
            }
            
            all_params = ["MS", "Pinus", "Quercus", "Betula", "Cerealia", "Poaceae",
                          "Pediastrum", "Charcoal", "Pisidium", "Valvata cristata",
                          "Vallonia costata", "Succinea putris", "Planorbis planorbis",
                          "Ca", "Mg", "Na", "K"]

            for param in all_params:
                if param in ranges:
                    min_val, max_val, trend = ranges[param]
                    row[param] = self.generate_value(d, depth, min_val, max_val, trend, param, zone_num, zones, data)
                else:
                    row[param] = 0

            if "OM" not in ranges:
                row["OM"], row["CC"], row["IM"] = 0,0,0
            else:
                row["OM"], row["CC"], row["IM"] = self.generate_sum_to_100(
                    ranges["OM"][0], ranges["OM"][1], ranges["OM"][2],
                    ranges["CC"][0], ranges["CC"][1], ranges["CC"][2],
                    ranges["IM"][0], ranges["IM"][1], ranges["IM"][2],
                    d, depth
            )
            if "Clay" not in ranges:
                row["Clay"], row["Silt"], row["Sand"] = 0,0,0
            else:
                row["Clay"], row["Silt"], row["Sand"] = self.generate_sum_to_100(
                ranges["Clay"][0], ranges["Clay"][1], ranges["Clay"][2],
                ranges["Silt"][0], ranges["Silt"][1], ranges["Silt"][2],
                ranges["Sand"][0], ranges["Sand"][1], ranges["Sand"][2],
                d, depth
            )

            data.append(row)  # Append to the local 'data'

        return data  # Return the local 'data'

    def generate_value(self, d, depth, min_val, max_val, trend, param, zone_num, zones, data):
        """Generates a value based on the trend."""

        normalized_depth = d / depth if depth > 0 else 0

        if trend == "stagnant":
            midpoint = (min_val + max_val) / 2
            fluctuation = (max_val - min_val) / 10  # Adjust as needed
            result = round(random.uniform(max(min_val, midpoint - fluctuation), min(max_val, midpoint + fluctuation)), 2)
            return result

        elif trend == "increasing":
            return round(random.uniform(min_val + (max_val - min_val) * 0.75, max_val), 2)

        elif trend == "decreasing":
            return round(random.uniform(min_val, min_val + (max_val - min_val) * 0.25), 2)

        elif trend == "increasing with breaks":
            # 80% chance of increase, 20% chance of a dip
            if random.random() < 0.8:
                return round(random.uniform(min_val + (max_val - min_val) * 0.6, max_val), 2) #smaller range than a regular increase
            else:
                return round(random.uniform(min_val, min_val + (max_val-min_val) * 0.4), 2) # Simulates the "break" or dip.

        elif trend == "decreasing then stagnant":
            if random.random() < 0.6:  # 60% chance of decreasing
                return round(random.uniform(min_val, min_val + (max_val - min_val) * 0.4), 2)
            else:  # 40% chance of becoming stagnant
                midpoint = (min_val + max_val) / 2
                fluctuation = (max_val - min_val) / 20  # Smaller fluctuation for stagnant
                return round(random.uniform(max(min_val, midpoint - fluctuation), min(max_val, midpoint + fluctuation)), 2)

        elif trend == "increasing then stagnant":
            if random.random() < 0.6:  # 60% chance of increasing
                return round(random.uniform(min_val + (max_val - min_val) * 0.6, max_val), 2)
            else:  # 40% chance of becoming stagnant
                midpoint = (min_val + max_val) / 2
                fluctuation = (max_val - min_val) / 20  # Smaller fluctuation for stagnant
                return round(random.uniform(max(min_val, midpoint - fluctuation), min(max_val, midpoint + fluctuation)), 2)

        elif trend == "sporadic up and down":
            midpoint = (min_val + max_val) / 2
            fluctuation = (max_val - min_val) / 4  # Larger fluctuation
            return round(random.uniform(max(min_val, midpoint - fluctuation), min(max_val, midpoint + fluctuation)), 2)

        elif trend == "increasing then decreasing":
            if random.random() < 0.5: # 50% chance to be in the increasing part
                return round(random.uniform(min_val, (min_val + max_val) / 2 ), 2)
            else: # 50% chance to be in the decreasing part.
                return round(random.uniform((min_val + max_val) / 2, max_val), 2)
        
        elif trend == "sporadic":
            if random.random() < 0.2:
                return round(random.uniform(min_val, max_val), 2)
            else:
                return round((0),2)
       
        elif trend == "increasing_then_stagnant":
            if normalized_depth <= 0.5:
                return round(float(min_val + (max_val - min_val) * (normalized_depth * 2)),2)
            else:
                return round(random.uniform(float(max_val * 0.95), float(max_val * 1.05)),2)

        elif trend == "decreasing_then_stagnant":
            if normalized_depth <= 0.5:
                return round(float(max_val - (max_val - min_val) * (normalized_depth * 2)),2)
            else:
                return round(random.uniform(float(min_val * 0.95), float(min_val * 1.05)),2)
        elif trend == "sporadic_up_down":
            base_value = random.uniform(min_val, max_val)
            if random.random() < 0.3:
                deviation = random.uniform(float(0.3 * (max_val - min_val)), float(0.7 * (max_val - min_val)))
                if random.choice([True, False]):
                    base_value += deviation
                else:
                    base_value -= deviation
                base_value = max(min_val, min(base_value, max_val))
            return round((base_value),2)
        
        elif trend == "increasing_then_decreasing":
            midpoint = (zones[zone_num][0] + zones[zone_num][1]) / 2
            if d <= midpoint:
                normalized_zone_depth = (d - zones[zone_num][0]) / (midpoint - zones[zone_num][0]) if (midpoint -
                                                                                                       zones[zone_num][
                                                                                                           0]) > 0 else 0
                return round(float(min_val + (max_val - min_val) * normalized_zone_depth),2)
            else:
                normalized_zone_depth = (d - midpoint) / (zones[zone_num][1] - midpoint) if (zones[zone_num][
                                                                                                 1] - midpoint) > 0 else 0
                return round(float(max_val - (max_val - min_val) * normalized_zone_depth),2)
        else:
            return round(random.uniform(min_val, max_val),2)

    def generate_profile(self):
        """Generates the paleo profile based on user selections."""

        # --- Input Validation ---
        try:
            depth_choice = self.depth_var.get()
            base_type = self.base_type_var.get()
            env_type = self.env_type_var.get()

            if not all([depth_choice, base_type, env_type]):
                raise ValueError("Please select an option for all choices.")

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        # --- Depth Calculation ---
        depth_ranges = {1: (50, 100), 2: (100, 200), 3: (200, 300), 4: (300, 400), 5: (400, 500), 6: (500, 600)}
        min_depth, max_depth = depth_ranges[depth_choice]
        depth = random.randrange(min_depth, max_depth + 1, 2)

        # --- Zone Generation ---
        zone_percentages = self.generate_unique_zone_percentages()
        zones = self.assign_depths_to_zones(depth, zone_percentages)

        # --- Data Generation ---
        self.data = []
        self.data = self.generate_data(depth, zones, base_type, env_type)

        # --- Display Data ---
        self.display_table(self.data)

    def generate_sum_to_100(self, min1, max1, trend1, min2, max2, trend2, min3, max3, trend3, d, depth):
        """
        Generates three values that sum to 100 while respecting minimum and maximum bounds
        and following specified trends. Returns values with 2 decimal places.
        
        Args:
            min1, max1, trend1: Parameters for first value
            min2, max2, trend2: Parameters for second value
            min3, max3, trend3: Parameters for third value
            d: Current depth
            depth: Total depth
            
        Returns:
            Tuple of three floats with 2 decimal places that sum to 100
        """
        max_attempts = 100
        for _ in range(max_attempts):
            # Generate initial values based on trends
            v1 = self.generate_value(d, depth, min1, max1, trend1, "", 0, {}, [])
            v2 = self.generate_value(d, depth, min2, max2, trend2, "", 0, {}, [])
            v3 = self.generate_value(d, depth, min3, max3, trend3, "", 0, {}, [])
            
            # Handle case where all values are 0
            if v1 + v2 + v3 == 0:
                return 0.00, 0.00, 0.00
                
            # Calculate proportions that respect the relative magnitudes
            total = v1 + v2 + v3
            p1 = round((v1 / total) * 100, 2)
            p2 = round((v2 / total) * 100, 2)
            p3 = round(100 - p1 - p2, 2)
            
            # Verify all values are within their bounds
            if (min1 <= p1 <= max1 and 
                min2 <= p2 <= max2 and 
                min3 <= p3 <= max3):
                return p1, p2, p3
        
        # If we couldn't find valid values after max attempts,
        # use a fallback approach to ensure values sum to 100
        v1 = round(max(min1, min(max1, 33.33)), 2)
        v2 = round(max(min2, min(max2, 33.33)), 2)
        v3 = round(100 - v1 - v2, 2)
        
        # Adjust if v3 is out of bounds
        if v3 < min3:
            deficit = min3 - v3
            if v1 > min1 + deficit/2 and v2 > min2 + deficit/2:
                v1 = round(v1 - deficit/2, 2)
                v2 = round(v2 - deficit/2, 2)
                v3 = round(min3, 2)
        elif v3 > max3:
            excess = v3 - max3
            v1 = round(v1 + excess/2, 2)
            v2 = round(v2 + excess/2, 2)
            v3 = round(max3, 2)
            
        # Final rounding to ensure exact sum of 100
        v1 = round(v1, 2)
        v2 = round(v2, 2)
        v3 = round(100 - v1 - v2, 2)
        
        return v1, v2, v3

    def get_parameter_ranges(self, base_type, env_type, zone_num):
        """Defines parameter ranges based on base type, environment, and zone."""
        ranges = {}

        if zone_num == 5:  # Base type only applies to zone 5
            if base_type == "Rock":
                ranges = {
                    "OM": (0, 5, "increasing"),
                    "IM": (70, 95, "decreasing"),
                    "CC": (5, 30, "decreasing_then_stagnant"),
                    "Clay": (0, 5, "stagnant"),
                    "Silt": (5, 15, "stagnant"),
                    "Sand": (70, 90, "stagnant"),
                    "MS": (150, 250, "stagnant"),
                    "Pinus": (100, 150, "stagnant"),
                    "Quercus": (0, 0, "stagnant"),
                    "Betula": (0, 0, "stagnant"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Poaceae": (0, 5, "stagnant"),
                    "Pediastrum": (0, 0, "stagnant"),
                    "Charcoal": (0, 10, "sporadic"),
                    "Pisidium": (70, 200, "stagnant"),
                    "Valvata cristata": (0, 30, "sporadic"),
                    "Vallonia costata": (0, 0, "stagnant"),
                    "Succinea putris": (0, 0, "stagnant"),
                    "Planorbis planorbis": (80, 100, "stagnant"),
                    "Ca": (270, 400, "stagnant"),
                    "Mg": (250, 330, "stagnant"),
                    "Na": (300, 400, "stagnant"),
                    "K": (300, 400, "stagnant")
                }
            elif base_type == "Sand":
                ranges = {
                    "OM": (0, 0, "stagnant"),
                    "IM": (70, 95, "stagnant"),
                    "CC": (5, 30, "stagnant"),
                    "Clay": (0, 5, "stagnant"),
                    "Silt": (0, 10, "stagnant"),
                    "Sand": (85, 95, "stagnant"),
                    "MS": (150, 200, "stagnant"),
                    "Pinus": (100, 150, "stagnant"),
                    "Quercus": (0, 0, "stagnant"),
                    "Betula": (0, 0, "stagnant"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Poaceae": (0, 10, "stagnant"),
                    "Pediastrum": (0, 0, "stagnant"),
                    "Charcoal": (0, 10, "sporadic"),
                    "Pisidium": (70, 200, "stagnant"),
                    "Valvata cristata": (0, 30, "sporadic"),
                    "Vallonia costata": (0, 0, "stagnant"),
                    "Succinea putris": (0, 0, "stagnant"),
                    "Planorbis planorbis": (60, 200, "stagnant"),
                    "Ca": (70, 100, "stagnant"),
                    "Mg": (50, 90, "stagnant"),
                    "Na": (100, 150, "stagnant"),
                    "K": (100, 140, "stagnant")
                }
            elif base_type == "Paleosol":
                ranges = {
                    "OM": (15, 35, "stagnant"),
                    "IM": (40, 70, "decreasing"),
                    "CC": (5, 30, "decreasing_then_stagnant"),
                    "Clay": (5, 20, "stagnant"),
                    "Silt": (5, 15, "stagnant"),
                    "Sand": (70, 90, "stagnant"),
                    "MS": (100, 150, "stagnant"),
                    "Pinus": (100, 150, "stagnant"),
                    "Quercus": (0, 0, "stagnant"),
                    "Betula": (0, 0, "stagnant"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Poaceae": (30, 60, "stagnant"),
                    "Pediastrum": (0, 0, "stagnant"),
                    "Charcoal": (0, 10, "sporadic"),
                    "Pisidium": (70, 200, "stagnant"),
                    "Valvata cristata": (0, 30, "sporadic"),
                    "Vallonia costata": (0, 0, "stagnant"),
                    "Succinea putris": (0, 0, "stagnant"),
                    "Planorbis planorbis": (170, 230, "stagnant"),
                    "Ca": (100, 200, "stagnant"),
                    "Mg": (100, 130, "stagnant"),
                    "Na": (100, 200, "stagnant"),
                    "K": (100, 200, "stagnant")
                }
            elif base_type == "Lake sediment":
                ranges = {
                    "OM": (5, 15, "stagnant"),
                    "IM": (40, 80, "stagnant"),
                    "CC": (5, 30, "stagnant"),
                    "Clay": (10, 20, "stagnant"),
                    "Silt": (10, 60, "stagnant"),
                    "Sand": (20, 40, "stagnant"),
                    "MS": (100, 150, "stagnant"),
                    "Pinus": (100, 150, "stagnant"),
                    "Quercus": (0, 0, "stagnant"),
                    "Betula": (0, 0, "stagnant"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Poaceae": (20, 50, "decreasing"),
                    "Poaceae": (120, 150, "stagnant"),
                    "Charcoal": (0, 10, "sporadic"),
                    "Pisidium": (70, 200, "stagnant"),
                    "Valvata cristata": (0, 30, "sporadic"),
                    "Vallonia costata": (0, 0, "stagnant"),
                    "Succinea putris": (0, 0, "stagnant"),
                    "Planorbis planorbis": (70, 200, "stagnant"),
                    "Ca": (130, 200, "stagnant"),
                    "Mg": (90, 130, "stagnant"),
                    "Na": (200, 300, "stagnant"),
                    "K": (200, 300, "stagnant")
                }
        # Zones 1-4, influenced by env_type
        elif zone_num == 4:
            if env_type == "Lake":
                ranges.update({
                    "OM": (5, 15, "stagnant"),
                    "IM": (40, 80, "stagnant"),
                    "CC": (5, 30, "stagnant"),
                    "Clay": (10, 20, "stagnant"),
                    "Silt": (10, 60, "stagnant"),
                    "Sand": (20, 40, "stagnant"),
                    "MS": (100, 150, "stagnant"),
                    "Pinus": (100, 150, "stagnant"),
                    "Quercus": (0, 0, "stagnant"),
                    "Betula": (0, 0, "stagnant"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Poaceae": (100, 120, "stagnant"),
                    "Pediastrum": (0, 0, "stagnant"),
                    "Charcoal": (0, 10, "sporadic"),
                    "Pisidium": (70, 200, "stagnant"),
                    "Valvata cristata": (0, 10, "sporadic"),
                    "Vallonia costata": (0, 0, "stagnant"),
                    "Succinea putris": (0, 0, "stagnant"),
                    "Planorbis planorbis": (70, 230, "stagnant"),
                    "Ca": (130, 200, "stagnant"),
                    "Mg": (90, 130, "stagnant"),
                    "Na": (200, 300, "stagnant"),
                    "K": (200, 300, "stagnant")
                })
            elif env_type == "Peatland":
                ranges.update({
                    "OM": (2, 15, "increasing"),
                    "IM": (40, 80, "stagnant"),
                    "CC": (5, 30, "stagnant"),
                    "Clay": (10, 20, "stagnant"),
                    "Silt": (10, 60, "stagnant"),
                    "Sand": (20, 40, "stagnant"),
                    "MS": (100, 150, "stagnant"),
                    "Pinus": (100, 150, "stagnant"),
                    "Quercus": (0, 0, "stagnant"),
                    "Betula": (0, 0, "stagnant"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Poaceae": (80, 120, "stagnant"),
                    "Pediastrum": (0, 0, "stagnant"),
                    "Charcoal": (0, 10, "sporadic"),
                    "Pisidium": (70, 200, "stagnant"),
                    "Valvata cristata": (0, 30, "sporadic"),
                    "Vallonia costata": (0, 0, "stagnant"),
                    "Succinea putris": (0, 0, "stagnant"),
                    "Planorbis planorbis": (70, 230, "stagnant"),
                    "Ca": (130, 200, "stagnant"),
                    "Mg": (90, 130, "stagnant"),
                    "Na": (200, 300, "stagnant"),
                    "K": (200, 300, "stagnant")
                })
            elif env_type == "Wetland":
                ranges.update({
                    "OM": (5, 20, "stagnant"),
                    "IM": (40, 80, "stagnant"),
                    "CC": (5, 30, "stagnant"),
                    "Clay": (10, 20, "stagnant"),
                    "Silt": (10, 60, "stagnant"),
                    "Sand": (20, 40, "stagnant"),
                    "MS": (100, 150, "stagnant"),
                    "Pinus": (100, 150, "stagnant"),
                    "Quercus": (0, 0, "stagnant"),
                    "Betula": (0, 0, "stagnant"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Poaceae": (80, 130, "stagnant"),
                    "Pediastrum": (0, 0, "stagnant"),
                    "Charcoal": (0, 10, "sporadic"),
                    "Pisidium": (70, 200, "stagnant"),
                    "Valvata cristata": (0, 30, "sporadic"),
                    "Vallonia costata": (0, 0, "stagnant"),
                    "Succinea putris": (0, 0, "stagnant"),
                    "Planorbis planorbis": (70, 230, "stagnant"),
                    "Ca": (130, 200, "stagnant"),
                    "Mg": (90, 130, "stagnant"),
                    "Na": (200, 300, "stagnant"),
                    "K": (200, 300, "stagnant")
                })

        elif zone_num == 3:
            if env_type == "Lake":
                ranges.update({
                    "OM": (5, 15, "sporadic_up_down"),
                    "IM": (40, 80, "sporadic_up_down"),
                    "CC": (5, 30, "sporadic_up_down"),
                    "Clay": (5, 40, "stagnant"),
                    "Silt": (5, 60, "stagnant"),
                    "Sand": (5, 60, "stagnant"),
                    "MS": (100, 150, "stagnant"),
                    "Pinus": (70, 120, "stagnant"),
                    "Quercus": (0, 0, "stagnant"),
                    "Betula": (0, 0, "stagnant"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Poaceae": (40, 90, "decreasing"),
                    "Pediastrum": (0, 0, "stagnant"),
                    "Charcoal": (0, 3, "stagnant"),
                    "Pisidium": (70, 100, "stagnant"),
                    "Valvata cristata": (10, 30, "stagnant"),
                    "Vallonia costata": (0, 0, "stagnant"),
                    "Succinea putris": (0, 0, "stagnant"),
                    "Planorbis planorbis": (70, 230, "stagnant"),
                    "Ca": (130, 200, "stagnant"),
                    "Mg": (90, 130, "stagnant"),
                    "Na": (200, 300, "stagnant"),
                    "K": (200, 300, "stagnant")
                })
            elif env_type == "Peatland":
              ranges.update({
                "OM": (10, 30, "sporadic_up_down"),
                "IM": (40, 80, "sporadic_up_down"),
                "CC": (5, 30, "sporadic_up_down"),
                "Clay": (5, 40, "stagnant"),
                "Silt": (5, 60, "stagnant"),
                "Sand": (5, 60, "stagnant"),
                "MS": (100, 150, "stagnant"),
                "Pinus": (70, 120, "stagnant"),
                "Quercus": (0, 0, "stagnant"),
                "Betula": (0, 0, "stagnant"),
                "Cerealia": (0, 0, "stagnant"),
                "Poaceae": (60, 90, "stagnant"),
                "Pediastrum": (0, 0, "stagnant"),
                "Charcoal": (0, 3, "sporadic"),
                "Pisidium": (70, 100, "stagnant"),
                "Valvata cristata": (5, 30, "stagnant"),
                "Vallonia costata": (0, 0, "stagnant"),
                "Succinea putris": (0, 0, "stagnant"),
                "Planorbis planorbis": (70, 230, "stagnant"),
                "Ca": (130, 200, "stagnant"),
                "Mg": (90, 130, "stagnant"),
                "Na": (200, 300, "stagnant"),
                "K": (200, 300, "stagnant")
            })
            elif env_type == "Wetland":
                ranges.update({
                    "OM": (10, 30, "stagnant"),
                    "IM": (30, 70, "sporadic_up_down"),
                    "CC": (20, 40, "sporadic_up_down"),
                    "Clay": (10, 40, "stagnant"),
                    "Silt": (20, 60, "stagnant"),
                    "Sand": (10, 50, "stagnant"),
                    "MS": (40, 70, "stagnant"),
                    "Pinus": (30, 90, "stagnant"),
                    "Quercus": (70, 140, "increasing"),
                    "Betula": (200, 360, "increasing"),
                    "Poaceae": (80, 110, "stagnant"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Pediastrum": (20, 50, "increasing"),
                    "Charcoal": (0, 0, "sporadic"),
                    "Pisidium": (80, 130, "decreasing"),
                    "Valvata cristata": (15, 50, "increasing"),
                    "Vallonia costata": (30, 80, "stagnant"),
                    "Succinea putris": (30, 80, "stagnant"),
                    "Planorbis planorbis": (70, 230, "stagnant"),
                    "Ca": (830, 1400, "stagnant"),
                    "Mg": (390, 530, "stagnant"),
                    "Na": (200, 300, "stagnant"),
                    "K": (200, 300, "stagnant")
                })

        elif zone_num == 2:
            if env_type == "Lake":
                ranges.update({
                    "OM": (10, 20, "sporadic_up_down"),
                    "IM": (40, 80, "sporadic_up_down"),
                    "CC": (5, 30, "sporadic_up_down"),
                    "Clay": (5, 40, "stagnant"),
                    "Silt": (5, 60, "stagnant"),
                    "Sand": (5, 60, "stagnant"),
                    "MS": (50, 80, "stagnant"),
                    "Pinus": (70, 120, "stagnant"),
                    "Quercus": (140, 140, "stagnant"),
                    "Betula": (60, 60, "stagnant"),
                    "Cerealia": (0, 10, "increasing"),
                    "Poaceae": (30, 60, "decreasing"),
                    "Pediastrum": (20, 50, "increasing"),
                    "Charcoal": (0, 0, "stagnant"),
                    "Pisidium": (70, 100, "stagnant"),
                    "Valvata cristata": (10, 30, "stagnant"),
                    "Vallonia costata": (0, 0, "stagnant"),
                    "Succinea putris": (0, 0, "stagnant"),
                    "Planorbis planorbis": (70, 230, "stagnant"),
                    "Ca": (630, 1200, "stagnant"),
                    "Mg": (190, 230, "stagnant"),
                    "Na": (200, 300, "stagnant"),
                    "K": (200, 300, "stagnant")
                })
            elif env_type == "Peatland":
              ranges.update({
                "OM": (80, 99, "stagnant"),
                "IM": (1, 10, "sporadic_up_down"),
                "CC": (1, 5, "sporadic_up_down"),
                "Clay": (20, 60, "stagnant"),
                "Silt": (20, 60, "stagnant"),
                "Sand": (1, 5, "stagnant"),
                "MS": (20, 40, "stagnant"),
                "Pinus": (30, 90, "stagnant"),
                "Quercus": (70, 140, "increasing"),
                "Betula": (200, 360, "increasing"),
                "Cerealia": (0, 0, "stagnant"),
                "Poaceae": (20, 50, "stagnant"),
                "Pediastrum": (20, 50, "increasing"),
                "Charcoal": (0, 10, "sporadic"),
                "Pisidium": (80, 130, "decreasing"),
                "Valvata cristata": (15, 50, "increasing"),
                "Vallonia costata": (30, 80, "sporadic_up_down"),
                "Succinea putris": (30, 80, "stagnant"),
                "Planorbis planorbis": (70, 230, "stagnant"),
                "Ca": (630, 1200, "stagnant"),
                "Mg": (190, 230, "stagnant"),
                "Na": (500, 600, "stagnant"),
                "K": (500, 600, "stagnant")
            })
            elif env_type == "Wetland":
                ranges.update({
                    "OM": (50, 90, "stagnant"),
                    "IM": (5, 30, "sporadic_up_down"),
                    "CC": (5, 15, "sporadic_up_down"),
                    "Clay": (20, 60, "stagnant"),
                    "Silt": (20, 60, "stagnant"),
                    "Sand": (1, 5, "stagnant"),
                    "MS": (120, 140, "increasing"),
                    "Pinus": (30, 90, "stagnant"),
                    "Quercus": (70, 140, "increasing"),
                    "Betula": (200, 360, "increasing"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Poaceae": (30, 60, "decreasing"),
                    "Pediastrum": (20, 50, "increasing"),
                    "Charcoal": (0, 10, "sporadic"),
                    "Pisidium": (80, 130, "decreasing"),
                    "Valvata cristata": (15, 50, "increasing"),
                    "Vallonia costata": (30, 80, "stagnant"),
                    "Succinea putris": (30, 80, "stagnant"),
                    "Planorbis planorbis": (70, 230, "stagnant"),
                    "Ca": (130, 200, "stagnant"),
                    "Mg": (90, 130, "stagnant"),
                    "Na": (500, 600, "stagnant"),
                    "K": (500, 600, "stagnant")
                })

        elif zone_num == 1:
            if env_type == "Lake":
                ranges.update({
                    "OM": (5, 15, "sporadic_up_down"),
                    "IM": (40, 80, "sporadic_up_down"),
                    "CC": (5, 30, "sporadic_up_down"),
                    "Clay": (5, 40, "stagnant"),
                    "Silt": (10, 60, "stagnant"),
                    "Sand": (20, 60, "stagnant"),
                    "MS": (150, 300, "increasing"),
                    "Pinus": (30, 190, "stagnant"),
                    "Quercus": (200, 350, "stagnant"),
                    "Betula": (180, 240, "stagnant"),
                    "Cerealia": (20, 90, "increasing"),
                    "Poaceae": (20, 50, "decreasing"),
                    "Pediastrum": (30, 70, "increasing"),
                    "Charcoal": (30, 40, "sporadic"),
                    "Pisidium": (70, 100, "stagnant"),
                    "Valvata cristata": (10, 30, "stagnant"),
                    "Vallonia costata": (70, 200, "decreasing"),
                    "Succinea putris": (70, 100, "increasing_then_decreasing"),
                    "Planorbis planorbis": (70, 230, "stagnant"),
                    "Ca": (190, 240, "stagnant"),
                    "Mg": (90, 130, "stagnant"),
                    "Na": (400, 600, "stagnant"),
                    "K": (400, 500, "stagnant")
                })
            elif env_type == "Peatland":
              ranges.update({
                "OM": (5, 20, "sporadic_up_down"),
                "IM": (40, 80, "sporadic_up_down"),
                "CC": (5, 30, "sporadic_up_down"),
                "Clay": (5, 40, "stagnant"),
                "Silt": (10, 60, "stagnant"),
                "Sand": (20, 60, "stagnant"),
                "MS": (150, 300, "increasing"),
                "Pinus": (30, 190, "stagnant"),
                "Quercus": (200, 350, "stagnant"),
                "Betula": (180, 240, "stagnant"),
                "Cerealia": (20, 90, "increasing"),
                "Poaceae": (40, 90, "increasing"),
                "Pediastrum": (30, 70, "increasing"),
                "Charcoal": (30, 40, "sporadic"),
                "Pisidium": (90, 150, "stagnant"),
                "Valvata cristata": (35, 80, "stagnant"),
                "Vallonia costata": (170, 230, "decreasing"),
                "Succinea putris": (70, 100, "increasing_then_decreasing"),
                "Planorbis planorbis": (70, 230, "stagnant"),
                "Ca": (190, 240, "stagnant"),
                "Mg": (90, 130, "stagnant"),
                "Na": (600, 900, "stagnant"),
                "K": (600, 900, "stagnant")
            })
            elif env_type == "Wetland":
                ranges.update({
                    "OM": (10, 70, "sporadic_up_down"),
                    "IM": (10, 80, "sporadic_up_down"),
                    "CC": (5, 30, "sporadic_up_down"),
                    "Clay": (5, 20, "stagnant"),
                    "Silt": (30, 60, "stagnant"),
                    "Sand": (40, 70, "stagnant"),
                    "MS": (400, 700, "stagnant"),
                    "Pinus": (50, 100, "stagnant"),
                    "Quercus": (100, 200, "stagnant"),
                    "Betula": (100, 200, "stagnant"),
                    "Cerealia": (300, 400, "stagnant"),
                    "Poaceae": (20, 50, "decreasing"),
                    "Pediastrum": (50, 140, "stagnant"),
                    "Charcoal": (0, 30, "sporadic"),
                    "Pisidium": (170, 200, "stagnant"),
                    "Valvata cristata": (15, 70, "stagnant"),
                    "Vallonia costata": (100, 300, "stagnant"),
                    "Succinea putris": (100, 200, "stagnant"),
                    "Planorbis planorbis": (170, 330, "stagnant"),
                    "Ca": (130, 250, "stagnant"),
                    "Mg": (90, 230, "stagnant"),
                    "Na": (800, 900, "stagnant"),
                    "K": (800, 900, "stagnant")
                })

        return ranges
    def display_table(self, data):
        """Displays the generated data in a table within the Tkinter window."""

        # Clear any existing table
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        if not data:
            no_data_label = tk.Label(self.table_frame, text="No data to display.", fg="black")  # Removed bg color
            no_data_label.pack()
            return

         # --- Create Table Headers ---
        headers = list(data[0].keys())
        for j, header in enumerate(headers):
                label = tk.Label(self.table_frame, text=header, relief="solid", borderwidth=1,
                             fg="black", padx=5, pady=5, font=("Open Sans", 10, "bold"))  # Removed bg color
                label.grid(row=0, column=j, sticky="ew")

        # --- Populate Table with Data ---
        for i, row_data in enumerate(data):
            for j, header in enumerate(headers):
                 value = row_data[header]
                 label = tk.Label(self.table_frame, text=str(value), relief="solid", borderwidth=1,
                                  fg="black", padx=5, pady=5, font=("Open Sans", 10))  # Removed bg color
                 label.grid(row=i + 1, column=j, sticky="ew")

         # --- Configure Column Weights (for resizing) ---
        for j in range(len(headers)):
            self.table_frame.columnconfigure(j, weight=1)
        self.table_canvas.config(scrollregion=self.table_canvas.bbox(tk.ALL))

    def on_frame_configure(self, event=None):
        """Updates the scroll region of the canvas."""
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

    def save_data_to_csv(self):  # Removed the (self,data) argument
        """Saves the generated data to a CSV file (using self.data)."""

        if not hasattr(self, 'data') or not self.data:  # Use self.data
            messagebox.showinfo("No Data", "No data to save. Generate a profile first.")
            return
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Profile Data"
            )
            if file_path:
                df = pd.DataFrame(self.data)  # Use self.data
                df.to_csv(file_path, index=False)
                messagebox.showinfo("File Saved", f"Data saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error Saving File", f"An error occurred: {e}")

    def save_data_to_xlsx(self):
        """Saves the generated data to an Excel (.xlsx) file."""
        if not hasattr(self, 'data') or not self.data:
            messagebox.showinfo("No Data", "No data to save. Generate a profile first.")
            return

        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Save Profile Data"
            )
            if file_path:
                df = pd.DataFrame(self.data)
                df.to_excel(file_path, index=False, engine='openpyxl')  # Specify openpyxl
                messagebox.showinfo("File Saved", f"Data saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error Saving File", f"An error occurred: {e}")
# --- Main Program Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PaleoProfileRandomizer(root)
    root.mainloop()
