from tkinter import *
from tkinter import messagebox
from airport import *
from aircraft import *

airports = []
aircrafts = []


def load_airports():
    global airports
    airports = LoadAirports("airports.txt")
    messagebox.showinfo("Info", f"Cargados {len(airports)} aeropuertos")


def show_airports():
    if not airports:
        messagebox.showwarning("Error", "Primero carga aeropuertos")
        return

    # Ventana simple para mostrar
    win = Toplevel()
    win.title("Aeropuertos")
    text = Text(win, width=60, height=15)
    text.pack()

    for a in airports:
        text.insert(END, f"{a.code} - Lat: {a.latitude:.4f}, Lon: {a.longitude:.4f}, Schengen: {a.schengen}\n")

    text.config(state=DISABLED)


def plot_airports():
    if not airports:
        messagebox.showwarning("Error", "Primero carga aeropuertos")
        return
    PlotAirports(airports)


def map_airports():
    if not airports:
        messagebox.showwarning("Error", "Primero carga aeropuertos")
        return
    MapAirports(airports)
    messagebox.showinfo("Info", "Mapa airports_map.kml creado")


# ==================== VUELOS ====================

def load_arrivals():
    global aircrafts
    aircrafts = LoadArrivals("arrivals.txt")
    messagebox.showinfo("Info", f"Cargados {len(aircrafts)} vuelos")


def show_flights():
    if not aircrafts:
        messagebox.showwarning("Error", "Primero carga vuelos")
        return

    win = Toplevel()
    win.title("Vuelos")
    text = Text(win, width=70, height=15)
    text.pack()

    text.insert(END, "ID      | Origen | Hora  | Aerolínea | Schengen\n")
    text.insert(END, "--------|--------|-------|-----------|---------\n")

    for a in aircrafts:
        schengen = "SÍ" if a.schengen else "NO"
        text.insert(END, f"{a.id:7} | {a.origin:6} | {a.landing_time:5} | {a.airline:9} | {schengen:8}\n")

    text.config(state=DISABLED)


def plot_arrivals():
    if not aircrafts:
        messagebox.showwarning("Error", "Primero carga vuelos")
        return
    PlotArrivals(aircrafts)


def plot_airlines():
    if not aircrafts:
        messagebox.showwarning("Error", "Primero carga vuelos")
        return
    PlotAirlines(aircrafts)


def plot_flights_type():
    if not aircrafts:
        messagebox.showwarning("Error", "Primero carga vuelos")
        return
    PlotFlightsType(aircrafts)


def map_flights():
    if not aircrafts:
        messagebox.showwarning("Error", "Primero carga vuelos")
        return
    MapFlights(aircrafts)
    messagebox.showinfo("Info", "Mapa flights_map.kml creado")


def show_long_distance():
    if not aircrafts:
        messagebox.showwarning("Error", "Primero carga vuelos")
        return

    long_flights = LongDistanceArrivals(aircrafts)

    win = Toplevel()
    win.title("Vuelos Larga Distancia")
    text = Text(win, width=60, height=10)
    text.pack()

    text.insert(END, f"Vuelos de larga distancia: {len(long_flights)}\n\n")

    for a in long_flights:
        text.insert(END, f"• {a.id}: {a.origin} -> LEBL a las {a.landing_time}\n")

    text.config(state=DISABLED)


def save_flights():
    if not aircrafts:
        messagebox.showwarning("Error", "Primero carga vuelos")
        return

    # Guardar con nombre fijo
    SaveFlights(aircrafts, "vuelos_guardados.txt")
    messagebox.showinfo("Info", "Vuelos guardados en vuelos_guardados.txt")


# ==================== INTERFAZ ====================

root = Tk()
root.title("Sistema Aeropuertos v2")
root.geometry("350x550")

# Título
titulo = Label(root, text="SISTEMA AEROPUERTOS", font=("Arial", 14, "bold"))
titulo.pack(pady=10)

# Sección Aeropuertos
label_airports = Label(root, text="Gestión de Aeropuertos", font=("Arial", 11))
label_airports.pack(pady=5)

btn_load_airports = Button(root, text="Cargar Aeropuertos", width=20, command=load_airports)
btn_load_airports.pack(pady=2)

btn_show_airports = Button(root, text="Mostrar Aeropuertos", width=20, command=show_airports)
btn_show_airports.pack(pady=2)

btn_plot_airports = Button(root, text="Gráfico Aeropuertos", width=20, command=plot_airports)
btn_plot_airports.pack(pady=2)

btn_map_airports = Button(root, text="Mapa Aeropuertos", width=20, command=map_airports)
btn_map_airports.pack(pady=2)

# Separador
separador = Label(root, text="───────────────")
separador.pack(pady=10)

# Sección Vuelos
label_flights = Label(root, text="Gestión de Vuelos LEBL", font=("Arial", 11))
label_flights.pack(pady=5)

btn_load_flights = Button(root, text="Cargar Vuelos", width=20, command=load_arrivals)
btn_load_flights.pack(pady=2)

btn_show_flights = Button(root, text="Mostrar Vuelos", width=20, command=show_flights)
btn_show_flights.pack(pady=2)

btn_save_flights = Button(root, text="Guardar Vuelos", width=20, command=save_flights)
btn_save_flights.pack(pady=2)

btn_plot_hours = Button(root, text="Gráfico por Horas", width=20, command=plot_arrivals)
btn_plot_hours.pack(pady=2)

btn_plot_airlines = Button(root, text="Gráfico Aerolíneas", width=20, command=plot_airlines)
btn_plot_airlines.pack(pady=2)

btn_plot_schengen = Button(root, text="Gráfico Schengen", width=20, command=plot_flights_type)
btn_plot_schengen.pack(pady=2)

btn_map_flights = Button(root, text="Mapa Vuelos", width=20, command=map_flights)
btn_map_flights.pack(pady=2)

btn_long_distance = Button(root, text="Vuelos Larga Distancia", width=20, command=show_long_distance)
btn_long_distance.pack(pady=2)

# Botón Salir
btn_exit = Button(root, text="SALIR", width=15, command=root.quit, bg="lightcoral")
btn_exit.pack(pady=15)

root.mainloop()