import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Troop Info")
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
        unit_selection.bind("<<ComboboxSelected>>", self.display_unit_stats(parent_frame, unit_selection))

        stats_labels = ["Tier", "Rank", "HP", "MP", "AP", "RoA", "BAP", "PA", "SA", "PD", "SD", "DEX"]
        stat_vars = {label: tk.StringVar() for label in stats_labels}

        for stat in stats_labels:
            frame = tk.Frame(parent_frame)
            frame.pack(fill="x")

            label = tk.Label(frame, text=stat, width=5)
            label.pack(side="left")

            entry = tk.Entry(frame, textvariable=stat_vars[stat])
            entry.pack(side="left", fill="x", expand=True)

        return unit_selection, stat_vars

    def get_units_from_file(self):
        try:
            with open("Units.txt", "r") as f:
                units = f.read().splitlines()
            return units
        except FileNotFoundError:
            messagebox.showerror("Error", "Units.txt file not found.")
            return []

    def display_unit_stats(self, parent_frame, unit_selection):
        def callback(event):
            selected_unit = unit_selection.get()

            conn = sqlite3.connect("Stats.db")
            c = conn.cursor()

            c.execute("SELECT * FROM units WHERE name = ?", (selected_unit,))

            stats = c.fetchone()
            if stats is not None:
                for i, stat in enumerate(stats):
                    parent_frame.stat_vars[parent_frame.stats_labels[i]].set(stat)
            else:
                for stat_var in parent_frame.stat_vars.values():
                    stat_var.set("")

            conn.close()
        return callback

    def exit_program(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

if __name__ == "__main__":
    app = Application()
    app.mainloop()