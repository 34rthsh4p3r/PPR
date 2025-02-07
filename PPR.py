import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
import os
from PIL import Image, ImageTk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import matplotlib.pyplot as plt


class PaleoProfileRandomizer:

    def __init__(self, master):
        self.master = master
        master.title("PPR - Paleo Profile Randomizer")
        master.state('zoomed')  # Start in full-screen mode

        # --- Load and Display Icon ---
        try:
            icon_path = 'C:/Users/varit/.ico'  # Replace PATH with your icon file's path if different
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
        self.button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        self.generate_button = ttk.Button(self.button_frame, text="Generate Profile", command=self.generate_profile)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        self.save_button = ttk.Button(self.button_frame, text="Save to .csv", command=self.save_data_to_csv)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.save_button.pack_forget()
        self.exit_button = ttk.Button(self.button_frame, text="Exit", command=master.destroy)
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
        version_label = tk.Label(self.bottom_frame, text="Updated on 7 February 2025  |  Made by 34rthsh4p3r",  fg="black")
        version_label.pack(side=tk.TOP, expand=True)

        # --- Educative Purpose Frame ---
        self.ai_credit_frame = tk.Frame(master)
        self.ai_credit_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=0, pady=0) #row 5
        ai_credit_label = tk.Label(self.ai_credit_frame, text="This is for geology students to create fake environmental datasets for educative purposes", fg="black")
        ai_credit_label.pack(side=tk.TOP, expand=True)

        # --- AI Credit Frame ---
        self.ai_credit_frame = tk.Frame(master)
        self.ai_credit_frame.grid(row=6, column=0, columnspan=2, sticky="ew", padx=0, pady=0) #row 6
        ai_credit_label = tk.Label(self.ai_credit_frame, text="Parts of this code were developed with assistance from Google AI Studio Gemini 2.0 Pro Experimental 02-05", fg="black")
        ai_credit_label.pack(side=tk.TOP, expand=True)

        # --- Configure Row Weights ---
        master.rowconfigure(3, weight=1)  # Output frame should expand vertically
        master.columnconfigure(0, weight=1) # Make frames fill entire width
        self.output_frame.columnconfigure(0, weight=1) #canvas should fill output_frame

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
        depth_options = [("200-300", 1), ("300-400", 2), ("400-500", 3), ("500-600", 4), ("600-700", 5)]
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
        depth_ranges = {1: (200, 300), 2: (300, 400), 3: (400, 500), 4: (500, 600), 5: (600, 700)}
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

        # --- Show Save Button ---
        self.save_button.pack(side=tk.LEFT, padx=5) # pack_forget() has been removed

    def generate_unique_zone_percentages(self):
        """Generates 5 unique random numbers that sum to 100."""
        while True:
            nums = [random.randint(10, 60) for _ in range(4)]
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
            zones[i + 1] = (current_depth, int(round(zone_end / 2) * 2))
            current_depth = int(round(zone_end / 2) * 2)
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
                "OM": 0, "CC": 0, "IM": 0, "MS": 0,
                "Clay": 0, "Silt": 0, "Sand": 0,
            }

            for param, (min_val, max_val, trend) in ranges.items():
                if param not in ("OM", "CC", "IM", "Clay", "Silt", "Sand"):
                    # Pass 'data' (the local variable) to generate_value
                    row[param] = self.generate_value(d, depth, min_val, max_val, trend, param, zone_num, zones, data)

            row["OM"], row["CC"], row["IM"] = self.generate_sum_to_100(
                ranges["OM"][0], ranges["OM"][1], ranges["OM"][2],
                ranges["CC"][0], ranges["CC"][1], ranges["CC"][2],
                ranges["IM"][0], ranges["IM"][1], ranges["IM"][2],
                d, depth
            )
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
            return random.randint(min_val, max_val)
        elif trend == "increasing":
            return int(min_val + (max_val - min_val) * normalized_depth)
        elif trend == "decreasing":
            return int(max_val - (max_val - min_val) * normalized_depth)
        elif trend == "sporadic":
            if random.random() < 0.2:
                return random.randint(min_val, max_val)
            else:
                return 0
        elif trend == "increasing_then_stagnant":
            if normalized_depth <= 0.5:
                return int(min_val + (max_val - min_val) * (normalized_depth * 2))
            else:
                return random.randint(int(max_val * 0.95), int(max_val * 1.05))

        elif trend == "decreasing_then_stagnant":
            if normalized_depth <= 0.5:
                return int(max_val - (max_val - min_val) * (normalized_depth * 2))
            else:
                return random.randint(int(min_val * 0.95), int(min_val * 1.05))
        elif trend == "sporadic_up_down":
            base_value = random.randint(min_val, max_val)
            if random.random() < 0.3:
                deviation = random.randint(int(0.3 * (max_val - min_val)), int(0.7 * (max_val - min_val)))
                if random.choice([True, False]):
                    base_value += deviation
                else:
                    base_value -= deviation
                base_value = max(min_val, min(base_value, max_val))
            return base_value
        elif trend == "follow_Pisidium":
            # Use the 'data' passed as an argument (the local data list)
            pisidium_values = [row['Pisidium'] for row in data if row['Depth'] == d]
            if pisidium_values:
                pisidium_value = pisidium_values[0]
                range_width = max_val - min_val
                min_follow = max(min_val, pisidium_value - range_width // 4)
                max_follow = min(max_val, pisidium_value + range_width // 4)
                return random.randint(min_follow, max_follow)
            else:
                return random.randint(min_val, max_val)

        elif trend == "increasing_with_breaks":
            base_value = int(min_val + (max_val - min_val) * normalized_depth)
            if random.random() < 0.2:
                drop_amount = random.randint(int(0.2 * (max_val - min_val)), int(0.5 * (max_val - min_val)))
                return max(min_val, base_value - drop_amount)
            else:
                return base_value

        elif trend == "increasing_then_decreasing":
            midpoint = (zones[zone_num][0] + zones[zone_num][1]) / 2
            if d <= midpoint:
                normalized_zone_depth = (d - zones[zone_num][0]) / (midpoint - zones[zone_num][0]) if (midpoint -
                                                                                                       zones[zone_num][
                                                                                                           0]) > 0 else 0
                return int(min_val + (max_val - min_val) * normalized_zone_depth)
            else:
                normalized_zone_depth = (d - midpoint) / (zones[zone_num][1] - midpoint) if (zones[zone_num][
                                                                                                 1] - midpoint) > 0 else 0
                return int(max_val - (max_val - min_val) * normalized_zone_depth)
        else:
            return random.randint(min_val, max_val)

    def generate_sum_to_100(self, min1, max1, trend1, min2, max2, trend2, min3, max3, trend3, d, depth):
        """Generates three values that sum to 100, with trends."""
        v1 = self.generate_value(d, depth, min1, max1, trend1, "", 0, {}, [])  # Pass empty data list
        v2 = self.generate_value(d, depth, min2, max2, trend2, "", 0, {}, [])
        v3 = self.generate_value(d, depth, min3, max3, trend3, "", 0, {}, [])

        total = v1 + v2 + v3
        if total == 0:
            return 0, 0, 0
        v1 = int(v1 / total * 100)
        v2 = int(v2 / total * 100)
        v3 = 100 - v1 - v2

        return v1, v2, v3

    def get_parameter_ranges(self, base_type, env_type, zone_num):
        """Defines parameter ranges based on base type, environment, and zone."""
        ranges = {}

        if base_type == "Rock":
            ranges = {
                "OM": (0, 5, "increasing"),
                "IM": (70, 95, "decreasing"),
                "CC": (5, 30, "decreasing_then_stagnant"),
                "MS": (150, 250, "stagnant"),
                "Clay": (0, 5, "stagnant"),
                "Silt": (5, 15, "stagnant"),
                "Sand": (70, 90, "stagnant"),
                "Pinus": (100, 150, "stagnant"),
                "Quercus": (0, 0, "stagnant"),
                "Betula": (0, 0, "stagnant"),
                "Cerealia": (0, 0, "stagnant"),
                "Pediastrum": (0, 0, "stagnant"),
                "Charcoal": (0, 10, "sporadic"),
                "Pisidium": (70, 200, "stagnant"),
                "Valvata cristata": (0, 30, "sporadic"),
                "Vallonia costata": (0, 0, "stagnant"),
                "Succinea putris": (0, 0, "stagnant"),
                "Planorbis planorbis": (50, 230, "follow_Pisidium"),
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
                "MS": (150, 200, "stagnant"),
                "Clay": (0, 3, "stagnant"),
                "Silt": (0, 7, "stagnant"),
                "Sand": (85, 97, "stagnant"),
                "Pinus": (100, 150, "stagnant"),
                "Quercus": (0, 0, "stagnant"),
                "Betula": (0, 0, "stagnant"),
                "Cerealia": (0, 0, "stagnant"),
                "Pediastrum": (0, 0, "stagnant"),
                "Charcoal": (0, 10, "sporadic"),
                "Pisidium": (70, 200, "stagnant"),
                "Valvata cristata": (0, 30, "sporadic"),
                "Vallonia costata": (0, 0, "stagnant"),
                "Succinea putris": (0, 0, "stagnant"),
                "Planorbis planorbis": (50, 230, "follow_Pisidium"),
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
                "MS": (100, 150, "stagnant"),
                "Clay": (5, 20, "stagnant"),
                "Silt": (5, 15, "stagnant"),
                "Sand": (70, 90, "stagnant"),
                "Pinus": (100, 150, "stagnant"),
                "Quercus": (0, 0, "stagnant"),
                "Betula": (0, 0, "stagnant"),
                "Cerealia": (0, 0, "stagnant"),
                "Pediastrum": (0, 0, "stagnant"),
                "Charcoal": (0, 10, "sporadic"),
                "Pisidium": (70, 200, "stagnant"),
                "Valvata cristata": (0, 30, "sporadic"),
                "Vallonia costata": (0, 0, "stagnant"),
                "Succinea putris": (0, 0, "stagnant"),
                "Planorbis planorbis": (70, 230, "follow_Pisidium"),
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
                "MS": (100, 150, "stagnant"),
                "Clay": (10, 20, "stagnant"),
                "Silt": (10, 60, "stagnant"),
                "Sand": (20, 40, "stagnant"),
                "Pinus": (100, 150, "stagnant"),
                "Quercus": (0, 0, "stagnant"),
                "Betula": (0, 0, "stagnant"),
                "Cerealia": (0, 0, "stagnant"),
                "Pediastrum": (0, 0, "stagnant"),
                "Charcoal": (0, 10, "sporadic"),
                "Pisidium": (70, 200, "stagnant"),
                "Valvata cristata": (0, 30, "sporadic"),
                "Vallonia costata": (0, 0, "stagnant"),
                "Succinea putris": (0, 0, "stagnant"),
                "Planorbis planorbis": (70, 230, "follow_Pisidium"),
                "Ca": (130, 200, "stagnant"),
                "Mg": (90, 130, "stagnant"),
                "Na": (200, 300, "stagnant"),
                "K": (200, 300, "stagnant")
            }

        if env_type == "Lake":
            if zone_num == 4:
                ranges.update({
                    "OM": (5, 15, "stagnant"),
                    "IM": (40, 80, "stagnant"),
                    "CC": (5, 30, "stagnant"),
                    "MS": (100, 150, "stagnant"),
                    "Clay": (10, 20, "stagnant"),
                    "Silt": (10, 60, "stagnant"),
                    "Sand": (20, 40, "stagnant"),
                    "Pinus": (100, 150, "stagnant"),
                    "Quercus": (0, 0, "stagnant"),
                    "Betula": (0, 0, "stagnant"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Pediastrum": (0, 0, "stagnant"),
                    "Charcoal": (0, 10, "sporadic"),
                    "Pisidium": (70, 200, "stagnant"),
                    "Valvata cristata": (0, 30, "sporadic"),
                    "Vallonia costata": (0, 0, "stagnant"),
                    "Succinea putris": (0, 0, "stagnant"),
                    "Planorbis planorbis": (70, 230, "follow_Pisidium"),
                    "Ca": (130, 200, "stagnant"),
                    "Mg": (90, 130, "stagnant"),
                    "Na": (200, 300, "stagnant"),
                    "K": (200, 300, "stagnant")
                })
            elif zone_num == 3:
                ranges.update({
                    "OM": (5, 15, "sporadic_up_down"),
                    "IM": (40, 80, "sporadic_up_down"),
                    "CC": (5, 30, "sporadic_up_down"),
                    "MS": (100, 150, "stagnant"),
                    "Clay": (5, 40, "stagnant"),
                    "Silt": (5, 60, "stagnant"),
                    "Sand": (5, 60, "stagnant"),
                    "Pinus": (70, 120, "stagnant"),
                    "Quercus": (0, 0, "stagnant"),
                    "Betula": (0, 0, "stagnant"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Pediastrum": (0, 0, "stagnant"),
                    "Charcoal": (0, 3, "stagnant"),
                    "Pisidium": (70, 100, "stagnant"),
                    "Valvata cristata": (5, 30, "stagnant"),
                    "Vallonia costata": (0, 0, "stagnant"),
                    "Succinea putris": (0, 0, "stagnant"),
                    "Planorbis planorbis": (70, 230, "follow_Pisidium"),
                    "Ca": (130, 200, "stagnant"),
                    "Mg": (90, 130, "stagnant"),
                    "Na": (200, 300, "stagnant"),
                    "K": (200, 300, "stagnant")
                })
            elif zone_num == 2:
                ranges.update({
                    "OM": (10, 20, "sporadic_up_down"),
                    "IM": (40, 80, "sporadic_up_down"),
                    "CC": (5, 30, "sporadic_up_down"),
                    "MS": (50, 80, "stagnant"),
                    "Clay": (5, 40, "stagnant"),
                    "Silt": (5, 60, "stagnant"),
                    "Sand": (5, 60, "stagnant"),
                    "Pinus": (70, 120, "stagnant"),
                    "Quercus": (140, 140, "stagnant"),
                    "Betula": (60, 60, "stagnant"),
                    "Cerealia": (0, 10, "increasing"),
                    "Pediastrum": (20, 50, "increasing"),
                    "Charcoal": (0, 0, "stagnant"),
                    "Pisidium": (70, 100, "stagnant"),
                    "Valvata cristata": (5, 30, "stagnant"),
                    "Vallonia costata": (0, 0, "stagnant"),
                    "Succinea putris": (0, 0, "stagnant"),
                    "Planorbis planorbis": (70, 230, "follow_Pisidium"),
                    "Ca": (630, 1200, "stagnant"),
                    "Mg": (190, 230, "stagnant"),
                    "Na": (200, 300, "stagnant"),
                    "K": (200, 300, "stagnant")
                })
            elif zone_num == 1:
                ranges.update({
                    "OM": (5, 15, "sporadic_up_down"),
                    "IM": (40, 80, "sporadic_up_down"),
                    "CC": (5, 30, "sporadic_up_down"),
                    "MS": (150, 300, "increasing"),
                    "Clay": (5, 40, "stagnant"),
                    "Silt": (10, 60, "stagnant"),
                    "Sand": (20, 60, "stagnant"),
                    "Pinus": (30, 190, "stagnant"),
                    "Quercus": (200, 350, "stagnant"),
                    "Betula": (180, 240, "stagnant"),
                    "Cerealia": (20, 90, "increasing"),
                    "Pediastrum": (30, 70, "increasing"),
                    "Charcoal": (30, 40, "sporadic"),
                    "Pisidium": (70, 100, "stagnant"),
                    "Valvata cristata": (5, 30, "stagnant"),
                    "Vallonia costata": (70, 200, "increasing_with_breaks"),
                    "Succinea putris": (70, 100, "increasing_then_decreasing"),
                    "Planorbis planorbis": (70, 230, "follow_Pisidium"),
                    "Ca": (190, 240, "stagnant"),
                    "Mg": (90, 130, "stagnant"),
                    "Na": (400, 600, "stagnant"),
                    "K": (400, 500, "stagnant")
                })
        elif env_type == "Peatland":
            if zone_num == 4:
                ranges.update({
                    "OM": (5, 15, "stagnant"),
                    "IM": (40, 80, "stagnant"),
                    "CC": (5, 30, "stagnant"),
                    "MS": (100, 150, "stagnant"),
                    "Clay": (10, 20, "stagnant"),
                    "Silt": (10, 60, "stagnant"),
                    "Sand": (20, 40, "stagnant"),
                    "Pinus": (100, 150, "stagnant"),
                    "Quercus": (0, 0, "stagnant"),
                    "Betula": (0, 0, "stagnant"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Pediastrum": (0, 0, "stagnant"),
                    "Charcoal": (0, 10, "sporadic"),
                    "Pisidium": (70, 200, "stagnant"),
                    "Valvata cristata": (0, 30, "sporadic"),
                    "Vallonia costata": (0, 0, "stagnant"),
                    "Succinea putris": (0, 0, "stagnant"),
                    "Planorbis planorbis": (70, 230, "follow_Pisidium"),
                    "Ca": (130, 200, "stagnant"),
                    "Mg": (90, 130, "stagnant"),
                    "Na": (200, 300, "stagnant"),
                    "K": (200, 300, "stagnant")
                })
        elif zone_num == 3:
            ranges.update({
                "OM": (10, 30, "sporadic_up_down"),
                "IM": (40, 80, "sporadic_up_down"),
                "CC": (5, 30, "sporadic_up_down"),
                "MS": (100, 150, "stagnant"),
                "Clay": (5, 40, "stagnant"),
                "Silt": (5, 60, "stagnant"),
                "Sand": (5, 60, "stagnant"),
                "Pinus": (70, 120, "stagnant"),
                "Quercus": (0, 0, "stagnant"),
                "Betula": (0, 0, "stagnant"),
                "Cerealia": (0, 0, "stagnant"),
                "Pediastrum": (0, 0, "stagnant"),
                "Charcoal": (0, 3, "sporadic"),
                "Pisidium": (70, 100, "stagnant"),
                "Valvata cristata": (5, 30, "stagnant"),
                "Vallonia costata": (0, 0, "stagnant"),
                "Succinea putris": (0, 0, "stagnant"),
                "Planorbis planorbis": (70, 230, "follow_Pisidium"),
                "Ca": (130, 200, "stagnant"),
                "Mg": (90, 130, "stagnant"),
                "Na": (200, 300, "stagnant"),
                "K": (200, 300, "stagnant")
            })
        elif zone_num == 2:
            ranges.update({
                "OM": (80, 99, "stagnant"),
                "IM": (1, 10, "sporadic_up_down"),
                "CC": (1, 5, "sporadic_up_down"),
                "MS": (20, 40, "stagnant"),
                "Clay": (20, 60, "stagnant"),
                "Silt": (20, 60, "stagnant"),
                "Sand": (1, 5, "stagnant"),
                "Pinus": (30, 90, "stagnant"),
                "Quercus": (70, 140, "increasing"),
                "Betula": (200, 360, "increasing"),
                "Cerealia": (0, 0, "stagnant"),
                "Pediastrum": (20, 50, "increasing"),
                "Charcoal": (0, 10, "sporadic"),
                "Pisidium": (80, 130, "decreasing"),
                "Valvata cristata": (15, 50, "increasing"),
                "Vallonia costata": (30, 80, "stagnant"),
                "Succinea putris": (30, 80, "stagnant"),
                "Planorbis planorbis": (70, 230, "follow_Pisidium"),
                "Ca": (630, 1200, "stagnant"),
                "Mg": (190, 230, "stagnant"),
                "Na": (500, 600, "stagnant"),
                "K": (500, 600, "stagnant")
            })
        elif zone_num == 1:
            ranges.update({
                "OM": (5, 15, "sporadic_up_down"),
                "IM": (40, 80, "sporadic_up_down"),
                "CC": (5, 30, "sporadic_up_down"),
                "MS": (150, 300, "increasing"),
                "Clay": (5, 40, "stagnant"),
                "Silt": (10, 60, "stagnant"),
                "Sand": (20, 60, "stagnant"),
                "Pinus": (30, 190, "stagnant"),
                "Quercus": (200, 350, "stagnant"),
                "Betula": (180, 240, "stagnant"),
                "Cerealia": (20, 90, "increasing"),
                "Pediastrum": (30, 70, "increasing"),
                "Charcoal": (30, 40, "sporadic"),
                "Pisidium": (90, 150, "stagnant"),
                "Valvata cristata": (35, 80, "stagnant"),
                "Vallonia costata": (170, 230, "increasing_with_breaks"),
                "Succinea putris": (70, 100, "increasing_then_decreasing"),
                "Planorbis planorbis": (70, 230, "follow_Pisidium"),
                "Ca": (190, 240, "stagnant"),
                "Mg": (90, 130, "stagnant"),
                "Na": (600, 900, "stagnant"),
                "K": (600, 900, "stagnant")
            })
        elif env_type == "Wetland":
            if zone_num == 4:
                ranges.update({
                    "OM": (5, 15, "stagnant"),
                    "IM": (40, 80, "stagnant"),
                    "CC": (5, 30, "stagnant"),
                    "MS": (100, 150, "stagnant"),
                    "Clay": (10, 20, "stagnant"),
                    "Silt": (10, 60, "stagnant"),
                    "Sand": (20, 40, "stagnant"),
                    "Pinus": (100, 150, "stagnant"),
                    "Quercus": (0, 0, "stagnant"),
                    "Betula": (0, 0, "stagnant"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Pediastrum": (0, 0, "stagnant"),
                    "Charcoal": (0, 10, "sporadic"),
                    "Pisidium": (70, 200, "stagnant"),
                    "Valvata cristata": (0, 30, "sporadic"),
                    "Vallonia costata": (0, 0, "stagnant"),
                    "Succinea putris": (0, 0, "stagnant"),
                    "Planorbis planorbis": (70, 230, "follow_Pisidium"),
                    "Ca": (130, 200, "stagnant"),
                    "Mg": (90, 130, "stagnant"),
                    "Na": (200, 300, "stagnant"),
                    "K": (200, 300, "stagnant")
                })
            elif zone_num == 3:
                ranges.update({
                    "OM": (10, 30, "stagnant"),
                    "IM": (30, 70, "sporadic_up_down"),
                    "CC": (20, 40, "sporadic_up_down"),
                    "MS": (40, 70, "stagnant"),
                    "Clay": (10, 40, "stagnant"),
                    "Silt": (20, 60, "stagnant"),
                    "Sand": (10, 50, "stagnant"),
                    "Pinus": (30, 90, "stagnant"),
                    "Quercus": (70, 140, "increasing"),
                    "Betula": (200, 360, "increasing"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Pediastrum": (20, 50, "increasing"),
                    "Charcoal": (0, 0, "sporadic"),
                    "Pisidium": (80, 130, "decreasing"),
                    "Valvata cristata": (15, 50, "increasing"),
                    "Vallonia costata": (30, 80, "stagnant"),
                    "Succinea putris": (30, 80, "stagnant"),
                    "Planorbis planorbis": (70, 230, "follow_Pisidium"),
                    "Ca": (830, 1400, "stagnant"),
                    "Mg": (390, 530, "stagnant"),
                    "Na": (200, 300, "stagnant"),
                    "K": (200, 300, "stagnant")
                })
            elif zone_num == 2:
                ranges.update({
                    "OM": (50, 90, "stagnant"),
                    "IM": (5, 30, "sporadic_up_down"),
                    "CC": (5, 15, "sporadic_up_down"),
                    "MS": (120, 140, "increasing"),
                    "Clay": (20, 60, "stagnant"),
                    "Silt": (20, 60, "stagnant"),
                    "Sand": (1, 5, "stagnant"),
                    "Pinus": (30, 90, "stagnant"),
                    "Quercus": (70, 140, "increasing"),
                    "Betula": (200, 360, "increasing"),
                    "Cerealia": (0, 0, "stagnant"),
                    "Pediastrum": (20, 50, "increasing"),
                    "Charcoal": (0, 10, "sporadic"),
                    "Pisidium": (80, 130, "decreasing"),
                    "Valvata cristata": (15, 50, "increasing"),
                    "Vallonia costata": (30, 80, "stagnant"),
                    "Succinea putris": (30, 80, "stagnant"),
                    "Planorbis planorbis": (70, 230, "follow_Pisidium"),
                    "Ca": (130, 200, "stagnant"),
                    "Mg": (90, 130, "stagnant"),
                    "Na": (500, 600, "stagnant"),
                    "K": (500, 600, "stagnant")
                })
            elif zone_num == 1:
                ranges.update({
                    "OM": (10, 70, "sporadic_up_down"),
                    "IM": (10, 80, "sporadic_up_down"),
                    "CC": (5, 30, "sporadic_up_down"),
                    "MS": (400, 700, "stagnant"),
                    "Clay": (5, 20, "stagnant"),
                    "Silt": (30, 60, "stagnant"),
                    "Sand": (40, 70, "stagnant"),
                    "Pinus": (50, 100, "stagnant"),
                    "Quercus": (100, 200, "stagnant"),
                    "Betula": (100, 200, "stagnant"),
                    "Cerealia": (300, 400, "stagnant"),
                    "Pediastrum": (50, 140, "stagnant"),
                    "Charcoal": (0, 30, "sporadic"),
                    "Pisidium": (170, 200, "stagnant"),
                    "Valvata cristata": (15, 70, "stagnant"),
                    "Vallonia costata": (100, 300, "stagnant"),
                    "Succinea putris": (100, 200, "stagnant"),
                    "Planorbis planorbis": (170, 330, "follow_Pisidium"),
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
                             fg="black", padx=5, pady=5, font=("Arial", 10, "bold"))  # Removed bg color
                label.grid(row=0, column=j, sticky="ew")

        # --- Populate Table with Data ---
        for i, row_data in enumerate(data):
            for j, header in enumerate(headers):
                 value = row_data[header]
                 label = tk.Label(self.table_frame, text=str(value), relief="solid", borderwidth=1,
                                  fg="black", padx=5, pady=5, font=("Arial", 10))  # Removed bg color
                 label.grid(row=i + 1, column=j, sticky="ew")

         # --- Configure Column Weights (for resizing) ---
        for j in range(len(headers)):
            self.table_frame.columnconfigure(j, weight=1)
        self.table_canvas.config(scrollregion=self.table_canvas.bbox(tk.ALL))

    def on_frame_configure(self, event=None):
        """Updates the scroll region of the canvas."""
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

    def save_data_to_csv(self): #Removed the (self,data) argument
      """Saves the generated data to a CSV file (using self.data)."""

      if not self.data:  # Use self.data
          messagebox.showinfo("No Data", "No data to save.")
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
            self.save_button.pack_forget() # Hide save button after saving

      except Exception as e:
        messagebox.showerror("Error Saving File", f"An error occurred: {e}")
# --- Main Program Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PaleoProfileRandomizer(root)
    root.mainloop()