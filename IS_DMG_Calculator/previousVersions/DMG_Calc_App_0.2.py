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

        for frame in [self.left_frame, self.right_frame]:
            self.create_unit_selection_and_stats(frame)

        self.protocol("WM_DELETE_WINDOW", self.exit_program)

    def create_unit_selection_and_stats(self, parent_frame):
        unit_label = tk.Label(parent_frame, text="Select unit:")
        unit_label.pack()

        unit_selection = ttk.Combobox(parent_frame, values=sorted(self.get_units_from_file()))
        unit_selection.pack()

        stats_labels = ["Tier", "Rank", "HP", "MP", "AP", "RoA", "BAP", "PA", "SA", "PD", "SD", "DEX"]
        stat_vars = {label: tk.StringVar() for label in stats_labels}

        for stat in stats_labels:
            frame = tk.Frame(parent_frame)
            frame.pack(fill="x")

            label = tk.Label(frame, text=stat, width=5)
            label.pack(side="left")

            entry = tk.Entry(frame, textvariable=stat_vars[stat], state="readonly")
            entry.pack(side="left", fill="x", expand=True)

        unit_selection.bind("<<ComboboxSelected>>", self.display_unit_stats(parent_frame, unit_selection, stat_vars, stats_labels))

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

    def display_unit_stats(self, parent_frame, unit_selection, stat_vars, stats_labels):
        def callback(event):
            selected_unit = unit_selection.get()

            tree = ET.parse("Stats.xml")
            root = tree.getroot()

            unit_data = root.find(f"unit[@name='{selected_unit}']")
            if unit_data is not None:
                for stat in stats_labels:
                    stat_vars[stat].set(unit_data.find(stat).text)
            else:
                for stat_var in stat_vars.values():
                    stat_var.set("")

        return callback

    def exit_program(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()