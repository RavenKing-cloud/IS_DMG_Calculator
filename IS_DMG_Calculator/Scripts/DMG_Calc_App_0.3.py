import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import xml.etree.ElementTree as ET


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("DMG Calculator")
        self.geometry("800x600")
        self.resizable(True, True)

        self.create_widgets()

    def create_widgets(self):
        self.left_frame = tk.Frame(self)
        self.right_frame = tk.Frame(self)

        self.left_frame.pack(side="left", fill="both", expand=True)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.create_unit_selection_and_stats(self.left_frame, "Attacker")
        self.create_unit_selection_and_stats(self.right_frame, "Defender")

        self.create_conditions(self.left_frame, "Attacker")
        self.create_conditions(self.right_frame, "Defender")

        self.protocol("WM_DELETE_WINDOW", self.exit_program)

    def create_unit_selection_and_stats(self, parent_frame, entity_type):
        unit_label = tk.Label(parent_frame, text=f"Select {entity_type}:")
        unit_label.pack()

        unit_selection = ttk.Combobox(parent_frame, values=self.get_units_from_file())
        unit_selection.pack()

        stats_labels = ["Tier", "Rank", "HP", "MP", "EP", "RoA", "BAP", "PA", "SA", "PD", "SD", "DEX"]
        stat_vars = {label: tk.StringVar() for label in stats_labels}

        for stat in stats_labels:
            frame = tk.Frame(parent_frame)
            frame.pack(fill="x")

            label = tk.Label(frame, text=stat, width=5)
            label.pack(side="left")

            entry = tk.Entry(frame, textvariable=stat_vars[stat], state="readonly")
            entry.pack(side="left", fill="x", expand=True)

        equipment_labels = ["Equipment 1", "Equipment 2"]
        equipment_vars = {label: tk.StringVar() for label in equipment_labels}

        for equipment in equipment_labels:
            frame = tk.Frame(parent_frame)
            frame.pack(fill="x")

            label = tk.Label(frame, text=equipment, width=10)
            label.pack(side="left")

            entry = ttk.Combobox(frame, textvariable=equipment_vars[equipment], values=self.get_equipment_from_file("Equipment.xml"))
            entry.pack(side="left", fill="x", expand=True)

        unit_selection.bind("<<ComboboxSelected>>", self.display_unit_stats(entity_type, unit_selection, stat_vars, equipment_vars))

    def create_conditions(self, parent_frame, entity_type):
        conditions_frame = tk.LabelFrame(parent_frame, text=f"{entity_type} Conditions")
        conditions_frame.pack(fill="both", expand=True)

        terrain_label = tk.Label(conditions_frame, text="Terrain:")
        terrain_label.pack()

        terrain_selection = ttk.Combobox(conditions_frame, values=self.get_conditions_from_file("Conditions.xml", "terrain"))
        terrain_selection.pack()

        weather_label = tk.Label(conditions_frame, text="Weather:")
        weather_label.pack()

        weather_selection = ttk.Combobox(conditions_frame, values=self.get_conditions_from_file("Conditions.xml", "weather"))
        weather_selection.pack()

        terrain_selection.bind("<<ComboboxSelected>>", self.display_condition(entity_type, "Terrain", terrain_selection))
        weather_selection.bind("<<ComboboxSelected>>", self.display_condition(entity_type, "Weather", weather_selection))

    def get_units_from_file(self):
        try:
            tree = ET.parse("Stats.xml")
            root = tree.getroot()

            units = [unit.get("name") for unit in root.findall("unit")]

            return units
        except ET.ParseError:
            messagebox.showerror("Error", "Invalid XML file.")
            return []
        except FileNotFoundError:
            messagebox.showerror("Error", "Stats.xml file not found.")
            return []

    def get_equipment_from_file(self, file_name):
        try:
            tree = ET.parse(file_name)
            root = tree.getroot()

            equipment = [equip.text for equip in root.findall("equipment")]

            return equipment
        except ET.ParseError:
            messagebox.showerror("Error", "Invalid XML file.")
            return []
        except FileNotFoundError:
            messagebox.showerror("Error", f"{file_name} file not found.")
            return []

    def get_conditions_from_file(self, file_name, element_name):
        try:
            tree = ET.parse(file_name)
            root = tree.getroot()

            conditions = [condition.text for condition in root.findall(element_name)]

            return conditions
        except ET.ParseError:
            messagebox.showerror("Error", "Invalid XML file.")
            return []
        except FileNotFoundError:
            messagebox.showerror("Error", f"{file_name} file not found.")
            return []

    def display_unit_stats(self, entity_type, unit_selection, stat_vars, equipment_vars):
        def callback(event):
            selected_unit = unit_selection.get()

            tree = ET.parse("Stats.xml")
            root = tree.getroot()

            unit_data = root.find(f"unit[@name='{selected_unit}']")
            if unit_data is not None:
                for stat in stat_vars:
                    if stat == "AP":
                        # Change AP to EP
                        stat_vars[stat].set(unit_data.find("EP").text)
                    else:
                        stat_vars[stat].set(unit_data.find(stat).text)

                equipment_data = unit_data.findall("equipment")
                if equipment_data is not None:
                    equipment_list = [equipment.text for equipment in equipment_data]
                    for equipment_var, equipment in zip(equipment_vars.values(), equipment_list):
                        equipment_var.set(equipment)
            else:
                for stat_var in stat_vars.values():
                    stat_var.set("")

                # Clear equipment selection when unit changes
                for equipment_var in equipment_vars.values():
                    equipment_var.set("")

        return callback

    def display_condition(self, entity_type, condition_type, condition_selection):
        def callback(event):
            selected_condition = condition_selection.get()
            messagebox.showinfo(f"{entity_type} {condition_type}", f"Selected {condition_type}: {selected_condition}")

        return callback

    def exit_program(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()


if __name__ == "__main__":
    app = Application()
    app.mainloop()