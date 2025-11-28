from tkinter import *
from tkinter import messagebox

from aircraft import *
from airport import *
from LEBL import BarcelonaAP, LoadAirportStructure, AssignGate, GateOccupancy

airports = []
aircrafts = []
bcn = None  # aeropuerto LEBL.txt versión 3

# ==== GESTIÓN DE AEROPUERTOS NORMAL ====
def load_airports():
    global airports
    airports = LoadAirports("airports.txt")
    messagebox.showinfo("Info", f"Cargados {len(airports)} aeropuertos")

def show_airports():
    if not airports:
        messagebox.showwarning("Error", "Primero carga aeropuertos")
        return
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


# ==== GESTIÓN DE LEBL.txt V3 ====
def load_lebl_structure():
    global bcn
    bcn = LoadAirportStructure("LEBL.txt")
    if bcn:
        messagebox.showinfo("Info", "Estructura LEBL.txt cargada correctamente")
    else:
        messagebox.showerror("Error", "No se pudo cargar la estructura de LEBL.txt")

def show_gate_occupancy():
    if bcn is None:
        messagebox.showwarning("Error", "Primero carga la estructura del aeropuerto")
        return
    win = Toplevel()
    win.title("Ocupación Gates LEBL.txt")
    text = Text(win, width=80, height=20)
    text.pack()
    text.insert(END, "Terminal\tArea\tTipo\tGate\tOcupado\tID Aeronave\n")
    text.insert(END, "---------------------------------------------------------\n")
    for dato in GateOccupancy(bcn):
        ocupado = "Sí" if dato["ocupado"] else "No"
        id_aeronave = dato["id_aeronave"] if dato["id_aeronave"] else ""
        fila = f'{dato["terminal"]}\t{dato["area"]}\t{dato["tipo"]}\t{dato["gate"]}\t{ocupado}\t{id_aeronave}\n'
        text.insert(END, fila)
    text.config(state=DISABLED)

def assign_gates_to_arrivals():
    if bcn is None:
        messagebox.showwarning("Error", "Carga primero la estructura LEBL.txt")
        return
    if not aircrafts:
        messagebox.showwarning("Error", "Carga primero los vuelos")
        return
    asignados = 0
    errores = 0
    for avion in aircrafts:
        res = AssignGate(bcn, avion)
        if res == 0:
            asignados += 1
        else:
            errores += 1
    messagebox.showinfo("Info", f"Asig. automáticas: {asignados}. Errores: {errores}")

# ==== GESTIÓN DE VUELOS NORMAL ====
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
    text.insert(END, "ID | Origen | Hora | Aerolínea | Schengen\n")
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
        text.insert(END, f"• {a.id}: {a.origin} -> LEBL.txt a las {a.landing_time}\n")
    text.config(state=DISABLED)

def save_flights():
    if not aircrafts:
        messagebox.showwarning("Error", "Primero carga vuelos")
        return
    SaveFlights(aircrafts, "vuelos_guardados.txt")
    messagebox.showinfo("Info", "Vuelos guardados en vuelos_guardados.txt")

# ==== INTERFAZ GRÁFICA ====
root = Tk()
root.title("Sistema Aeropuertos v3")
root.geometry("400x650")

titulo = Label(root, text="SISTEMA AEROPUERTOS", font=("Arial", 14, "bold"))
titulo.pack(pady=10)

# Sección Aeropuertos Genéricos
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

separador = Label(root, text="───────────────")
separador.pack(pady=10)

# Sección Vuelos LEBL.txt
label_lebl = Label(root, text="Gestión de Aeropuerto LEBL.txt v3", font=("Arial", 11))
label_lebl.pack(pady=5)
btn_load_lebl = Button(root, text="Cargar Estructura LEBL.txt", width=20, command=load_lebl_structure)
btn_load_lebl.pack(pady=2)
btn_show_gates = Button(root, text="Mostrar Ocupación Gates", width=20, command=show_gate_occupancy)
btn_show_gates.pack(pady=2)
btn_assign_gates = Button(root, text="Asignar Gates a Vuelos", width=20, command=assign_gates_to_arrivals)
btn_assign_gates.pack(pady=2)

separador2 = Label(root, text="───────────────")
separador2.pack(pady=10)

# Sección Vuelos Genéricos
label_flights = Label(root, text="Gestión de Vuelos LEBL.txt", font=("Arial", 11))
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

btn_exit = Button(root, text="SALIR", width=15, command=root.quit, bg="lightcoral")
btn_exit.pack(pady=15)

root.mainloop()