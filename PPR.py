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
            icon_path = 'C:/Users/varit/Documents/PPR/PPR.ico'  # Replace PATH with your icon file's path if different
            icon_image = Image.open(icon_path)
            self.icon_photo = ImageTk.PhotoImage(icon_image)
            master.iconphoto(True, self.icon_photo)  
        except Exception as e:
            print(f"Error loading icon: {e}")  # Optional: Handle icon loading failure

        # --- Header Frame ---
        self.header_frame = tk.Frame(master)
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        title_label = tk.Label(self.header_frame, text="Paleo Profile Randomizer",  fg="black", font=("Arial", 16, "bold"))
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
        self.save_csv_button = ttk.Button(self.button_frame, text="Save Data (.csv)", command=self.save_data_to_csv, style="OpenSans.TButton")
        self.save_csv_button.pack(side=tk.LEFT, padx=5)

        self.save_xlsx_button = ttk.Button(self.button_frame, text="Save Data (.xlsx)", command=self.save_data_to_xlsx, style="OpenSans.TButton")
        self.save_xlsx_button.pack(side=tk.LEFT, padx=5)

         # --- Save Diagram Buttons ---
        self.save_png_button = ttk.Button(self.button_frame, text="Save Diagram (.png)", command=lambda: self.save_diagram("png"), style="OpenSans.TButton")
        self.save_png_button.pack(side=tk.LEFT, padx=5)

        self.save_svg_button = ttk.Button(self.button_frame, text="Save Diagram (.svg)", command=lambda: self.save_diagram("svg"), style="OpenSans.TButton")
        self.save_svg_button.pack(side=tk.LEFT, padx=5)
    
        # --- Exit Button ---
        self.exit_button = ttk.Button(self.button_frame, text="Exit", command=master.destroy, style="OpenSans.TButton")
        self.exit_button.pack(side=tk.LEFT, padx=5)

        # --- Output Frame ---
        self.output_frame = tk.Frame(master)
        self.output_frame.grid(row=3, column=0, columnspan=3, sticky="nsew")
        
        # Create left and right frames with 60-40 split
        self.left_frame = tk.Frame(self.output_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add a separator
        ttk.Separator(self.output_frame, orient='vertical').pack(side=tk.LEFT, fill='y', padx=2)
        
        # Right frame with explicit proportion
        self.right_frame = tk.Frame(self.output_frame)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        # Force the right frame to maintain a specific width
        self.right_frame.pack_propagate(False)  # Prevent frame from shrinking
        self.right_frame.configure(width=300)  # Set fixed width for diagram area
        
        # --- Table Frame (Left Side) ---
        self.h_scrollbar = ttk.Scrollbar(self.left_frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scrollbar = ttk.Scrollbar(self.left_frame, orient=tk.VERTICAL)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_canvas = tk.Canvas(self.left_frame, highlightthickness=0,
                                     xscrollcommand=self.h_scrollbar.set,
                                     yscrollcommand=self.v_scrollbar.set)
        self.table_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.table_frame = tk.Frame(self.table_canvas)
        self.table_canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        self.h_scrollbar.config(command=self.table_canvas.xview)
        self.v_scrollbar.config(command=self.table_canvas.yview)
        self.table_frame.bind("<Configure>", self.on_frame_configure)

        # --- Diagram Frame (Right Side) ---
        self.diagram_frame = tk.Frame(self.right_frame)
        self.diagram_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Bottom Frame (for version info) ---
        self.bottom_frame = tk.Frame(master)
        self.bottom_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=0, pady=0) #row 4
        version_label = tk.Label(self.bottom_frame, text="Updated on 10 February 2025",  fg="black", font=("Arial", 10))
        version_label.pack(side=tk.TOP, pady=(0,0))  # Reduce padding

        # Create a clickable link label for "34rthsh4p3r"
        link_label = tk.Label(self.bottom_frame, text="34rthsh4p3r", fg="teal", cursor="hand2", font=("Arial", 10, "bold"))
        link_label.pack(side=tk.TOP, pady=(0,0)) # Reduce padding
        link_label.bind("<Button-1>", lambda e: self.open_url("https://github.com/34rthsh4p3r/PPR"))

        # --- Configure Row Weights ---
        master.rowconfigure(3, weight=3)  # Output frame should expand vertically
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
        depth_label = tk.Label(self.input_container, text="Choose a depth:", fg="black", font=("Arial", 10, "bold"))
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
            rb = ttk.Radiobutton(inner_depth_frame, text=text, variable=self.depth_var, value=value, style="OpenSans.TRadiobutton")
            rb.pack(side=tk.LEFT, padx=5)  # Pack within inner frame


        # --- Base Type Selection ---
        base_label = tk.Label(self.input_container, text="Choose a base type:", fg="black", font=("Arial", 10, "bold"))
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
        env_label = tk.Label(self.input_container, text="Choose an environment type:",  fg="black", font=("Arial", 10, "bold"))
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
            z1 = random.uniform(10, 20)
            z2 = random.uniform(25, 60)
            z3 = random.uniform(30, 60)
            z4 = random.uniform(20, 40)
            z5 = random.uniform(5, 10)
            total = round(z1 + z2 + z3 + z4 + z5, 2)
            if  100-0.02 <= total <= 100+0.02:  #check the rounding
                nums = [z1, z2, z3, z4, z5]
                if len(set(nums)) == 5: #Check for uniqueness
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
            
            all_params = ["MS", "CH", "AP", "NAP", "WL", "CR",
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

        if trend == "SP":  # Sporadic: 70% chance to be 0
            if random.random() < 0.7:
                return round(0, 2)
            else:
                return round(random.uniform(min_val, max_val), 2)

        elif trend == "UP":  # Up: Increasing values
            if not hasattr(self, f'{param}_last_val_up'):
                setattr(self, f'{param}_last_val_up', min_val * 1.3)  # Initialize
            last_val_up = getattr(self, f'{param}_last_val_up')
            new_val = random.uniform(last_val_up, max_val * 0.7)
            setattr(self, f'{param}_last_val_up', new_val)
            return round(new_val, 2)

        elif trend == "DN":  # Down: Decreasing values
            if not hasattr(self, f'{param}_last_val_dn'):
                setattr(self, f'{param}_last_val_dn', max_val * 0.7) # Initialize
            last_val_dn = getattr(self, f'{param}_last_val_dn')
            new_val = random.uniform(min_val * 1.3, last_val_dn)
            setattr(self, f'{param}_last_val_dn', new_val)
            return round(new_val, 2)

        elif trend == "LF":  # LowFluctuation
            if not hasattr(self, f'{param}_lf_center'):
                setattr(self, f'{param}_lf_center', (min_val + max_val) / 2)   # or some other initial value
            lf_center = getattr(self, f'{param}_lf_center')
            fluctuation = (max_val - min_val) * 0.4  # 40% fluctuation
            new_val = random.uniform(lf_center - fluctuation, lf_center + fluctuation)
            setattr(self, f'{param}_lf_center', new_val)  # Update center for next call, creating slow drift
            return round(new_val, 2)

        elif trend == "HF":  # HighFluctuation
            fluctuation = (max_val - min_val) * 0.8  # 80% fluctuation
            center = (min_val + max_val) / 2
            return round(random.uniform(center - fluctuation, center + fluctuation), 2)
            
        elif trend == "SL": #StagnantLow: first stagnant, then decreasing
            midpoint_ratio = random.uniform(0.4, 0.6)
            midpoint = depth * midpoint_ratio
            if d <= midpoint:
                if not hasattr(self, f'{param}_stagnant_center_sl'):
                    setattr(self, f'{param}_stagnant_center_sl', random.uniform(min_val * 1.2, max_val * 0.8))
                stagnant_center_sl = getattr(self, f'{param}_stagnant_center_sl')
                fluctuation = (max_val - min_val) * 0.05  # 5% fluctuation
                return round(random.uniform(max(min_val, stagnant_center_sl - fluctuation), min(max_val, stagnant_center_sl + fluctuation)), 2)

            else:
                if not hasattr(self, f'{param}_last_val_sl'):
                    setattr(self, f'{param}_last_val_sl', getattr(self, f'{param}_stagnant_center_sl'))#initialize with the stagnant value
                last_val_sl = getattr(self, f'{param}_last_val_sl')
                normalized_depth = (d - midpoint) / (depth - midpoint) if (depth - midpoint) > 0 else 0
                new_val = round(float(last_val_sl - (last_val_sl-min_val) * normalized_depth * 0.5 ),2) #slower decreasing
                setattr(self, f'{param}_last_val_sl', new_val)
                return max(min_val, min(new_val, max_val)) #Limit the value

        elif trend == "SH": #StagnantHigh: first stagnant, then increasing
            midpoint_ratio = random.uniform(0.4, 0.6)
            midpoint = depth * midpoint_ratio
            if d <= midpoint:
                if not hasattr(self, f'{param}_stagnant_center_sh'):
                    setattr(self, f'{param}_stagnant_center_sh', random.uniform(min_val * 1.2, max_val * 0.8))
                stagnant_center_sh = getattr(self, f'{param}_stagnant_center_sh')
                fluctuation = (max_val - min_val) * 0.05
                return round(random.uniform(max(min_val, stagnant_center_sh - fluctuation), min(max_val, stagnant_center_sh + fluctuation)), 2)
            else:
                if not hasattr(self, f'{param}_last_val_sh'):
                    setattr(self, f'{param}_last_val_sh', getattr(self, f'{param}_stagnant_center_sh')) #initialize with the stagnant value
                last_val_sh = getattr(self, f'{param}_last_val_sh')
                normalized_depth = (d - midpoint) / (depth - midpoint) if (depth - midpoint) > 0 else 0

                new_val = round(float(last_val_sh + (max_val - last_val_sh) * normalized_depth * 0.5),2) #Slower increasing
                setattr(self, f'{param}_last_val_sh', new_val)
                return max(min_val, min(new_val, max_val))  #Limit the value

        elif trend == "UD":  # UpDown
            midpoint_ratio = random.uniform(0.4, 0.6)
            midpoint = zones[zone_num][0] + (zones[zone_num][1] - zones[zone_num][0]) * midpoint_ratio

            if d <= midpoint:
                # Increasing part
                normalized_zone_depth = (d - zones[zone_num][0]) / (midpoint - zones[zone_num][0]) if (midpoint - zones[zone_num][0]) > 0 else 0
                return round(float(min_val + (max_val - min_val) * normalized_zone_depth), 2)
            else:
                # Decreasing part
                normalized_zone_depth = (d - midpoint) / (zones[zone_num][1] - midpoint) if (zones[zone_num][1] - midpoint) > 0 else 0
                return round(float(max_val - (max_val - min_val) * normalized_zone_depth), 2)

        elif trend == "DU":  # DownUp
            midpoint_ratio = random.uniform(0.4, 0.6)
            midpoint = zones[zone_num][0] + (zones[zone_num][1] - zones[zone_num][0]) * midpoint_ratio

            if d <= midpoint:
                # Decreasing part
                normalized_zone_depth = (d - zones[zone_num][0]) / (midpoint - zones[zone_num][0]) if (midpoint - zones[zone_num][0]) > 0 else 0
                return round(float(max_val - (max_val - min_val) * normalized_zone_depth), 2)
            else:
                # Increasing part
                normalized_zone_depth = (d - midpoint) / (zones[zone_num][1] - midpoint) if (zones[zone_num][1] - midpoint) > 0 else 0
                return round(float(min_val + (max_val - min_val) * normalized_zone_depth), 2)
        
        elif trend == "RM": # Random
            return round(random.uniform(min_val, max_val), 2)

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
                    "OM": (0, 0, "LF"),
                    "IM": (70, 95, "LF"),
                    "CC": (12, 30, "LF"),
                    "Clay": (0, 5, "LF"),
                    "Silt": (5, 15, "HF"),
                    "Sand": (70, 90, "HF"),
                    "MS": (130, 220, "HF"),
                    "CH": (0, 0, "SP"),
                    "AP": (0, 0, "LF"),
                    "NAP": (0, 0, "LF"),
                    "WL": (0, 0, "LF"),
                    "CR": (0, 0, "LF"),
                    "Ca": (270, 400, "HF"),
                    "Mg": (250, 330, "HF"),
                    "Na": (300, 400, "HF"),
                    "K": (300, 400, "HF")
                }
            elif base_type == "Sand":
                ranges = {
                    "OM": (0, 0, "LF"),
                    "IM": (70, 95, "LF"),
                    "CC": (5, 20, "LF"),
                    "Clay": (0, 5, "LF"),
                    "Silt": (0, 10, "LF"),
                    "Sand": (85, 95, "LF"),
                    "MS": (150, 200, "LF"),
                    "CH": (0, 0, "SP"),
                    "AP": (20, 60, "LF"),
                    "NAP": (0, 20, "LF"),
                    "WL": (0, 0, "LF"),
                    "CR": (30, 90, "LF"),
                    "Ca": (70, 100, "LF"),
                    "Mg": (50, 90, "LF"),
                    "Na": (100, 150, "LF"),
                    "K": (100, 140, "LF")
                }
            elif base_type == "Paleosol":
                ranges = {
                    "OM": (15, 35, "LF"),
                    "IM": (40, 70, "LF"),
                    "CC": (10, 30, "DN"),
                    "Clay": (5, 20, "LF"),
                    "Silt": (5, 15, "LF"),
                    "Sand": (70, 90, "LF"),
                    "MS": (100, 150, "LF"),
                    "CH": (0, 10, "SP"),
                    "AP": (130, 280, "LF"),
                    "NAP": (10, 90, "LF"),
                    "WL": (40, 100, "UP"),
                    "CR": (60, 90, "DN"),
                    "Ca": (100, 200, "HF"),
                    "Mg": (100, 130, "HF"),
                    "Na": (100, 200, "LF"),
                    "K": (100, 200, "LF")
                }
            elif base_type == "Lake sediment":
                ranges = {
                    "OM": (5, 15, "LF"),
                    "IM": (40, 80, "LF"),
                    "CC": (5, 30, "LF"),
                    "Clay": (10, 20, "LF"),
                    "Silt": (10, 60, "LF"),
                    "Sand": (20, 40, "LF"),
                    "MS": (100, 150, "LF"),
                    "CH": (0, 10, "SP"),
                    "AP": (120, 260, "LF"),
                    "NAP": (20, 90, "LF"),
                    "WL": (10, 30, "UP"),
                    "CR": (130, 290, "LF"),
                    "Ca": (130, 200, "HF"),
                    "Mg": (90, 130, "HF"),
                    "Na": (200, 300, "LF"),
                    "K": (200, 300, "LF")
                }
        # Zones 1-4, influenced by env_type
        elif zone_num == 4:
            if env_type == "Lake":
                ranges.update({
                    "OM": (5, 20, "LF"),
                    "IM": (40, 80, "HF"),
                    "CC": (5, 35, "LF"),
                    "Clay": (10, 20, "LF"),
                    "Silt": (10, 60, "LF"),
                    "Sand": (20, 40, "DN"),
                    "MS": (100, 150, "LF"),
                    "CH": (0, 0, "SP"),
                    "AP": (100, 160, "DN"),
                    "NAP": (20, 40, "HF"),
                    "WL": (20, 50, "HF"),
                    "CR": (115, 250, "LF"),
                    "Ca": (150, 190, "HF"),
                    "Mg": (110, 140, "HF"),
                    "Na": (220, 310, "HF"),
                    "K": (210, 330, "LF")
                })
            elif env_type == "Peatland":
                ranges.update({
                    "OM": (2, 25, "HF"),
                    "IM": (40, 80, "LF"),
                    "CC": (5, 30, "DN"),
                    "Clay": (10, 20, "HF"),
                    "Silt": (10, 60, "LF"),
                    "Sand": (20, 40, "DN"),
                    "MS": (100, 150, "LF"),
                    "CH": (0, 12, "SP"),
                    "AP": (45, 199, "LF"),
                    "NAP": (40, 80, "HF"),
                    "WL": (40, 140, "HF"),
                    "CR": (30, 90, "LF"),
                    "Ca": (130, 200, "LF"),
                    "Mg": (90, 130, "LF"),
                    "Na": (200, 300, "LF"),
                    "K": (200, 300, "LF")
                })
            elif env_type == "Wetland":
                ranges.update({
                    "OM": (5, 20, "HF"),
                    "IM": (40, 80, "LF"),
                    "CC": (5, 30, "DN"),
                    "Clay": (10, 20, "HF"),
                    "Silt": (10, 60, "LF"),
                    "Sand": (20, 40, "LF"),
                    "MS": (100, 150, "LF"),
                    "CH": (0, 0, "SP"),
                    "AP": (45, 199, "LF"),
                    "NAP": (40, 80, "HF"),
                    "WL": (140, 240, "HF"),
                    "CR": (50, 120, "LF"),
                    "Ca": (130, 200, "HF"),
                    "Mg": (90, 130, "HF"),
                    "Na": (200, 300, "HF"),
                    "K": (200, 300, "HF")
                })

        elif zone_num == 3:
            if env_type == "Lake":
                ranges.update({
                    "OM": (9, 18, "HF"),
                    "IM": (40, 80, "HF"),
                    "CC": (5, 30, "HF"),
                    "Clay": (5, 40, "LF"),
                    "Silt": (5, 60, "LF"),
                    "Sand": (5, 60, "LF"),
                    "MS": (100, 150, "HF"),
                    "CH": (0, 5, "SP"),
                    "AP": (45, 199, "LF"),
                    "NAP": (40, 80, "HF"),
                    "WL": (40, 140, "HF"),
                    "CR": (30, 90, "LF"),
                    "Ca": (130, 200, "HF"),
                    "Mg": (90, 130, "LF"),
                    "Na": (200, 300, "HF"),
                    "K": (200, 300, "HF")
                })
            elif env_type == "Peatland":
              ranges.update({
                "OM": (30, 60, "HF"),
                "IM": (20, 60, "LF"),
                "CC": (5, 30, "LF"),
                "Clay": (5, 40, "HF"),
                "Silt": (5, 60, "LF"),
                "Sand": (5, 40, "LF"),
                "MS": (50, 100, "LF"),
                "CH": (0, 5, "SP"),
                "AP": (45, 199, "LF"),
                "NAP": (40, 80, "HF"),
                "WL": (220, 340, "HF"),
                "CR": (0, 30, "SP"),
                "Ca": (130, 200, "LF"),
                "Mg": (90, 130, "LF"),
                "Na": (200, 300, "LF"),
                "K": (200, 300, "LF")
            })
            elif env_type == "Wetland":
                ranges.update({
                    "OM": (10, 30, "LF"),
                    "IM": (30, 70, "HF"),
                    "CC": (20, 40, "HF"),
                    "Clay": (10, 40, "LF"),
                    "Silt": (20, 60, "LF"),
                    "Sand": (10, 50, "LF"),
                    "MS": (40, 70, "LF"),
                    "CH": (0, 5, "SP"),
                    "AP": (45, 199, "LF"),
                    "NAP": (40, 80, "HF"),
                    "WL": (220, 340, "HF"),
                    "CR": (0, 30, "SP"),
                    "Ca": (830, 1400, "LF"),
                    "Mg": (390, 530, "LF"),
                    "Na": (200, 300, "LF"),
                    "K": (200, 300, "LF")
                })

        elif zone_num == 2:
            if env_type == "Lake":
                ranges.update({
                    "OM": (10, 30, "LF"),
                    "IM": (40, 80, "HF"),
                    "CC": (5, 40, "HF"),
                    "Clay": (5, 40, "HF"),
                    "Silt": (5, 60, "HF"),
                    "Sand": (5, 60, "LF"),
                    "MS": (50, 80, "LF"),
                    "CH": (0, 0, "SP"),
                    "AP": (45, 199, "LF"),
                    "NAP": (40, 80, "HF"),
                    "WL": (220, 340, "HF"),
                    "CR": (0, 10, "SP"),
                    "Ca": (630, 1200, "LF"),
                    "Mg": (190, 230, "LF"),
                    "Na": (200, 300, "LF"),
                    "K": (200, 300, "LF")
                })
            elif env_type == "Peatland":
              ranges.update({
                "OM": (80, 99, "RM"),
                "IM": (1, 10, "HF"),
                "CC": (1, 5, "HF"),
                "Clay": (20, 60, "HF"),
                "Silt": (20, 60, "LF"),
                "Sand": (1, 5, "LF"),
                "MS": (20, 40, "LF"),
                "CH": (0, 0, "SP"),
                "AP": (45, 80, "LF"),
                "NAP": (140, 180, "HF"),
                "WL": (220, 340, "HF"),
                "CR": (0, 10, "SP"),
                "Ca": (630, 1200, "LF"),
                "Mg": (190, 230, "LF"),
                "Na": (500, 600, "LF"),
                "K": (500, 600, "LF")
            })
            elif env_type == "Wetland":
                ranges.update({
                    "OM": (50, 90, "LF"),
                    "IM": (5, 30, "HF"),
                    "CC": (5, 15, "HF"),
                    "Clay": (20, 60, "LF"),
                    "Silt": (20, 60, "LF"),
                    "Sand": (1, 5, "LF"),
                    "MS": (120, 140, "HF"),
                    "CH": (0, 10, "SP"),
                    "AP": (45, 80, "LF"),
                    "NAP": (140, 180, "HF"),
                    "WL": (220, 340, "HF"),
                    "CR": (0, 10, "SP"),
                    "Ca": (130, 200, "LF"),
                    "Mg": (90, 130, "LF"),
                    "Na": (500, 600, "LF"),
                    "K": (500, 600, "LF")
                })

        elif zone_num == 1:
            if env_type == "Lake":
                ranges.update({
                    "OM": (5, 15, "RM"),
                    "IM": (40, 80, "RM"),
                    "CC": (5, 30, "RM"),
                    "Clay": (5, 40, "LF"),
                    "Silt": (10, 60, "LF"),
                    "Sand": (20, 60, "LF"),
                    "MS": (150, 300, "HF"),
                    "CH": (0, 15, "SP"),
                    "AP": (145, 180, "LF"),
                    "NAP": (340, 480, "HF"),
                    "WL": (220, 340, "HF"),
                    "CR": (0, 30, "SP"),
                    "Ca": (190, 240, "LF"),
                    "Mg": (90, 130, "LF"),
                    "Na": (400, 600, "LF"),
                    "K": (400, 500, "LF")
                })
            elif env_type == "Peatland":
              ranges.update({
                "OM": (25, 70, "HF"),
                "IM": (40, 80, "RM"),
                "CC": (5, 20, "RM"),
                "Clay": (5, 40, "LF"),
                "Silt": (10, 60, "LF"),
                "Sand": (20, 60, "LF"),
                "MS": (150, 300, "HF"),
                "CH": (0, 15, "SP"),
                "AP": (145, 180, "LF"),
                "NAP": (340, 480, "HF"),
                "WL": (220, 340, "HF"),
                "CR": (0, 30, "SP"),
                "Ca": (190, 240, "LF"),
                "Mg": (90, 130, "LF"),
                "Na": (600, 900, "LF"),
                "K": (600, 900, "LF")
            })
            elif env_type == "Wetland":
                ranges.update({
                    "OM": (30, 70, "HF"),
                    "IM": (10, 80, "HF"),
                    "CC": (5, 30, "HF"),
                    "Clay": (5, 20, "LF"),
                    "Silt": (30, 60, "LF"),
                    "Sand": (40, 70, "LF"),
                    "MS": (400, 700, "LF"),
                    "CH": (0, 15, "SP"),
                    "AP": (145, 280, "LF"),
                    "NAP": (340, 480, "LF"),
                    "WL": (220, 340, "LF"),
                    "CR": (0, 30, "SP"),
                    "Ca": (130, 250, "LF"),
                    "Mg": (90, 230, "LF"),
                    "Na": (800, 900, "LF"),
                    "K": (800, 900, "LF")
                })

        return ranges
    def display_table(self, data):
        """Displays the generated data in a table within the Tkinter window."""

        # Clear any existing table and diagram
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        # --- Diagram Display ---
        if hasattr(self, 'figure_canvas'):  # Check for existence
            self.figure_canvas.get_tk_widget().destroy()  

        if not data:
            no_data_label = tk.Label(self.table_frame, text="No data to display.", fg="black")  # Removed bg color
            no_data_label.pack()
            return

         # --- Create Table Headers ---

        headers = list(data[0].keys())
        for j, header in enumerate(headers):
                label = tk.Label(self.table_frame, text=header, relief="solid", borderwidth=1,
                             fg="black", padx=2, pady=2, font=("Helvetica", 9, "bold"))  # Removed bg color
                label.grid(row=0, column=j, sticky="nsew") # Changed sticky to nsew

        # --- Populate Table with Data ---

        for i, row_data in enumerate(data):
            for j, header in enumerate(headers):
                 value = row_data[header]
                 label = tk.Label(self.table_frame, text=str(value), relief="solid", borderwidth=1,
                                  fg="black", padx=2, pady=2, font=("Helvetica", 9))  # Removed bg color
                 label.grid(row=i + 1, column=j, sticky="nsew") # Changed sticky to nsew

         # --- Configure Column Weights (for resizing) ---

        for j in range(len(headers)):
            self.table_frame.columnconfigure(j, weight=1)
        #self.table_canvas.config(scrollregion=self.table_canvas.bbox(tk.ALL)) #Removed this line
        self.table_frame.update_idletasks() #Added this line
        self.table_canvas.config(scrollregion=self.table_canvas.bbox("all")) #Added this line


        self.display_diagram(data)  # Call diagram display after table

    def display_diagram(self, data):
        """Displays the generated data as a diagram."""
        if not data:
            return  # No data, no diagram

        df = pd.DataFrame(data)
        df = df.set_index('Depth')
        df = df.drop('Zone', axis=1)  # Remove the 'Zone' column

        # --- Create the Matplotlib Figure ---
        fig, axes = plt.subplots(nrows=1, ncols=len(df.columns), figsize=(10, 10), sharey=True)
        
        if len(df.columns) == 1:
            axes = [axes]

        for ax, col in zip(axes, df.columns):
            ax.plot(df[col], df.index)
            ax.set_title(col, fontsize=9, rotation=0, ha='center')
            ax.invert_yaxis()  # Invert y-axis to show depth increasing downwards
            ax.tick_params(axis='both', which='major', labelsize=6) #Tick size
            ax.tick_params(axis='both', which='minor', labelsize=4) #Tick size
            ax.set_ylim(df.index.max(), 0) #added this line

        fig.subplots_adjust(wspace=0.1)   # Adjust spacing as needed


        # --- Embed Figure in Tkinter ---
        self.figure_canvas = FigureCanvasTkAgg(fig, master=self.output_frame)  # Use output_frame
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True) #Changed side to RIGHT

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
    
    def save_diagram(self, filetype):
        """Saves the current diagram to a file of the specified type (png or svg)."""
        if not hasattr(self, 'figure_canvas'):
            messagebox.showinfo("No Diagram", "No diagram to save. Generate a profile first.")
            return

        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=f".{filetype}",
                filetypes=[(f"{filetype.upper()} files", f"*.{filetype}"), ("All files", "*.*")],
                title=f"Save Diagram as {filetype.upper()}"
            )
            if file_path:
                self.figure_canvas.figure.savefig(file_path)  # Save the *figure*
                messagebox.showinfo("File Saved", f"Diagram saved to {file_path}")

        except Exception as e:
            messagebox.showerror("Error Saving File", f"An error occurred: {e}")
# --- Main Program Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PaleoProfileRandomizer(root)
    root.mainloop()
