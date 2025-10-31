from tkinter import *
from tkinter import messagebox, simpledialog
from airport import *

airports = []  


def load_airports():
    global airports
    filename = "airports.txt"
    airports = LoadAirports(filename)
    messagebox.showinfo("Load Airports", f"Se cargaron {len(airports)} aeropuertos desde {filename}.")


def show_airports():
    if len(airports) == 0:
        messagebox.showwarning("Show Airports", "No hay aeropuertos cargados.")
        return

    ventana = Toplevel(root)
    ventana.title("Lista de Aeropuertos")

    texto = Text(ventana, width=60, height=20)
    texto.pack()

    for a in airports:
        texto.insert(END, f"{a.code}: {a.latitude:.4f}, {a.longitude:.4f}, Schengen={a.schengen}\n")

    texto.config(state=DISABLED)


def add_airport():
    global airports
    code = simpledialog.askstring("Add Airport", "Código del aeropuerto (ej: LEBL):")
    if not code:
        return
    lat = simpledialog.askfloat("Add Airport", "Latitud (ej: 41.297):")
    lon = simpledialog.askfloat("Add Airport", "Longitud (ej: 2.083):")

    a = Airport()
    a.code = code.upper()
    a.latitude = lat
    a.longitude = lon
    SetSchengen(a)
    AddAirport(airports, a)


def delete_airport():
    global airports
    code = simpledialog.askstring("Delete Airport", "Código del aeropuerto a eliminar:")
    if not code:
        return
    RemoveAirport(airports, code.upper())


def set_schengen_all():
    if len(airports) == 0:
        messagebox.showwarning("Set Schengen", "No hay aeropuertos cargados.")
        return

    for a in airports:
        SetSchengen(a)
    messagebox.showinfo("Set Schengen", "Se actualizó el atributo Schengen de todos los aeropuertos.")


def save_schengen():
    if len(airports) == 0:
        messagebox.showwarning("Save Schengen", "No hay aeropuertos cargados.")
        return
    SaveSchengenAirports(airports, "schengen_airports.txt")
    messagebox.showinfo("Save Schengen", "Archivo 'schengen_airports.txt' guardado correctamente.")


def plot_airports():
    if len(airports) == 0:
        messagebox.showwarning("Plot Airports", "No hay aeropuertos cargados.")
        return
    PlotAirports(airports)


def map_airports():
    if len(airports) == 0:
        messagebox.showwarning("Map Airports", "No hay aeropuertos cargados.")
        return
    MapAirports(airports)
    messagebox.showinfo("Map Airports", "Archivo 'airports_map.kml' creado.\nÁbrelo con Google Earth.")


def exit_program():
    if messagebox.askyesno("Exit", "¿Deseas salir del programa?"):
        root.destroy()


root = Tk()
root.title("✈️ Airport Management System")
root.geometry("400x400")
root.resizable(False, False)

Label(root, text="Airport Management", font=("Arial", 16, "bold")).pack(pady=10)


Button(root, text="Load Airports", width=25, command=load_airports).pack(pady=3)
Button(root, text="Show Airports", width=25, command=show_airports).pack(pady=3)
Button(root, text="Add Airport", width=25, command=add_airport).pack(pady=3)
Button(root, text="Delete Airport", width=25, command=delete_airport).pack(pady=3)
Button(root, text="Set Schengen Attribute", width=25, command=set_schengen_all).pack(pady=3)
Button(root, text="Save Schengen Airports", width=25, command=save_schengen).pack(pady=3)
Button(root, text="Plot Airports", width=25, command=plot_airports).pack(pady=3)
Button(root, text="Show Map in Google Earth", width=25, command=map_airports).pack(pady=3)
Button(root, text="Exit", width=25, command=exit_program).pack(pady=10)

root.mainloop()
