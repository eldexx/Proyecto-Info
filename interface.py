import tkinter as tk
from tkinter import filedialog, messagebox
from airport import *

airports = []

def load_file():
    global airports
    filename = filedialog.askopenfilename()
    airports = LoadAirports(filename)
    for a in airports: SetSchengen(a)
    messagebox.showinfo("Loaded", f"{len(airports)} airports loaded.")

def show_plot():
    if not airports:
        messagebox.showerror("Error", "No airports loaded.")
    else:
        PlotAirports(airports)

def save_schengen():
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    SaveSchengenAirports(airports, filename)
    messagebox.showinfo("Saved", "Schengen airports saved!")

root = tk.Tk()
root.title("Airport Manager v1")

tk.Button(root, text="Load Airports", command=load_file).pack(pady=5)
tk.Button(root, text="Plot Airports", command=show_plot).pack(pady=5)
tk.Button(root, text="Save Schengen", command=save_schengen).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

root.mainloop()
