from tkinter import *
from tkinter import messagebox, simpledialog

from aircraft import *
from airport import *
from LEBL import *

# Variables Globales
airports = []
aircrafts = []      
departures = []     
merged_flights = [] 
bcn = None 

# ==========================================
# GESTIÓN DE AEROPUERTOS
# ==========================================
def load_airports():
    global airports
    airports = LoadAirports("airports.txt")
    if len(airports) > 0:
        messagebox.showinfo("Info", "Cargados " + str(len(airports)) + " aeropuertos.")
    else:
        messagebox.showwarning("Aviso", "No se cargaron aeropuertos.")

def save_airports():
    if len(airports) == 0:
        messagebox.showwarning("Error", "No hay datos para guardar.")
        return
    SaveSchengenAirports(airports, "schengen_airports.txt")
    messagebox.showinfo("Info", "Guardado en 'schengen_airports.txt'")

def add_airport():
    code = simpledialog.askstring("Añadir", "Código ICAO (ej: KJFK):")
    if code == None:
        return
    
    lat = simpledialog.askfloat("Añadir", "Latitud (Decimal):")
    if lat == None:
        return
    
    lon = simpledialog.askfloat("Añadir", "Longitud (Decimal):")
    if lon == None:
        return

    nuevo = Airport()
    nuevo.code = code.upper()
    nuevo.latitude = lat
    nuevo.longitude = lon
    SetSchengen(nuevo)
    
    res = AddAirport(airports, nuevo)
    if res == 0:
        messagebox.showinfo("Exito", "Aeropuerto añadido.")
    else:
        messagebox.showerror("Error", "El aeropuerto ya existe.")

def remove_airport():
    code = simpledialog.askstring("Eliminar", "Código ICAO a borrar:")
    if code == None:
        return
    
    res = RemoveAirport(airports, code.upper())
    if res == 0:
        messagebox.showinfo("Exito", "Aeropuerto eliminado.")
    else:
        messagebox.showerror("Error", "No encontrado.")

def show_airports():
    if len(airports) == 0:
        messagebox.showwarning("Error", "Carga aeropuertos primero.")
        return
    win = Toplevel()
    win.title("Lista de Aeropuertos")
    text = Text(win, width=60, height=15)
    text.pack()
    
    for i in range(len(airports)):
        a = airports[i]
        linea = "✈ " + a.code + " | Lat: " + str(a.latitude) + " | Lon: " + str(a.longitude) + "\n"
        text.insert(END, linea)
        
    text.config(state=DISABLED)

def map_airports():
    if len(airports) == 0:
        return
    MapAirports(airports)
    messagebox.showinfo("Info", "Mapa 'airports_map.kml' creado.")

def plot_airports():
    if len(airports) == 0: 
        messagebox.showwarning("Error", "Carga aeropuertos primero.")
        return
    PlotAirports(airports)


# ==========================================
# GESTIÓN ESTRUCTURA LEBL
# ==========================================
def load_lebl_structure():
    global bcn
    bcn = LoadAirportStructure("LEBL.txt")
    if bcn != None:
        messagebox.showinfo("Info", "Estructura LEBL cargada.")
    else:
        messagebox.showerror("Error", "No se encontró 'LEBL.txt'.")

def show_gate_occupancy():
    if bcn is None:
        messagebox.showwarning("Error", "Carga la estructura del aeropuerto primero.")
        return
    alguna_ocupada = False
    for t in bcn.terminales:
        for ba in t.boarding_areas:
            for g in ba.gates:
                if g.ocupado:
                    alguna_ocupada = True

    if not alguna_ocupada:
        messagebox.showinfo(
            "Aviso",
            "Todas las puertas están libres.\n\n"
            "¿Has asignado gates a los vuelos?\n"
            "Pulsa primero: 'Asignar puertas'."
        )

    win = Toplevel()
    win.title("Ocupación de Gates - LEBL")
    win.geometry("700x500")

    text = Text(win, width=85, height=25)
    text.pack(padx=10, pady=10)

    text.insert(END, "TERMINAL | AREA | GATE | ESTADO | AVIÓN\n")
    text.insert(END, "===============================================\n")

    for t in bcn.terminales:
        text.insert(END, f"\n--- TERMINAL {t.nombre} ---\n")

        for ba in t.boarding_areas:
            tipo = "Schengen" if ba.tipo else "Non-Schengen"
            text.insert(END, f" Área {ba.nombre} ({tipo})\n")

            for g in ba.gates:
                estado = "OCUPADA" if g.ocupado else "LIBRE"
                avion = g.id_aeronave if g.id_aeronave else "-"

                linea = f"    {g.nombre:12} | {estado:7} | {avion}\n"
                text.insert(END, linea)

    text.config(state=DISABLED)

def assign_gates_static():
    if bcn == None or len(aircrafts) == 0:
        messagebox.showwarning("Error", "Faltan datos.")
        return
        
    # Limpieza previa
    for i in range(len(bcn.terminales)):
        t = bcn.terminales[i]
        for j in range(len(t.boarding_areas)):
            ba = t.boarding_areas[j]
            for k in range(len(ba.gates)):
                ba.gates[k].liberar()
            
    asignados = 0
    for i in range(len(aircrafts)):
        avion = aircrafts[i]
        res = AssignGate(bcn, avion)
        if res == 0:
            asignados = asignados + 1
            
    messagebox.showinfo("Resultado", "Asignados: " + str(asignados))


# ==========================================
# GESTIÓN VUELOS Y SIMULACIÓN
# ==========================================
def load_arrivals():
    global aircrafts
    aircrafts = LoadArrivals("arrivals.txt")
    messagebox.showinfo("Info", "Cargadas " + str(len(aircrafts)) + " llegadas.")

def load_departures():
    global departures
    departures = LoadDepartures("departures.txt")
    messagebox.showinfo("Info", "Cargadas " + str(len(departures)) + " salidas.")

def merge_movements():
    global merged_flights
    if len(aircrafts) == 0 and len(departures) == 0:
        messagebox.showwarning("Error", "Carga Llegadas y Salidas primero.")
        return
    merged_flights = MergeMovements(aircrafts, departures)
    messagebox.showinfo("Info", "Fusion OK. Total: " + str(len(merged_flights)))

def run_simulation():
    if bcn == None or len(merged_flights) == 0:
        messagebox.showerror("Error", "Faltan Datos (LEBL o Vuelos fusionados)")
        return
    PlotDayOccupancy(bcn, merged_flights)

def save_flights():
    lista = []
    if len(merged_flights) > 0:
        lista = merged_flights
    else:
        lista = aircrafts
        
    if len(lista) == 0:
        return
        
    SaveFlights(lista, "vuelos_guardados.txt")
    messagebox.showinfo("Info", "Guardado 'vuelos_guardados.txt'")

def map_flights_all():
    lista = []
    if len(merged_flights) > 0:
        lista = merged_flights
    else:
        lista = aircrafts
        
    if len(lista) == 0: return
    
    MapFlights(lista, only_long_distance=False)
    messagebox.showinfo("Info", "KML creado.")

def map_flights_long():
    lista = []
    if len(merged_flights) > 0:
        lista = merged_flights
    else:
        lista = aircrafts

    if len(lista) == 0: return
    
    MapFlights(lista, only_long_distance=True)
    messagebox.showinfo("Info", "KML creado.")

def plot_hours(): 
    if len(aircrafts) > 0:
        PlotArrivals(aircrafts)

def plot_airlines(): 
    if len(aircrafts) > 0:
        PlotAirlines(aircrafts)

def plot_schengen(): 
    if len(aircrafts) > 0:
        PlotFlightsType(aircrafts)

def assign_gates_dynamic_day():
    if bcn is None or len(merged_flights) == 0:
        messagebox.showerror(
            "Error",
            "Carga la estructura LEBL y fusiona llegadas + salidas primero."
        )
        return

    # Resetear gates
    for t in bcn.terminales:
        for ba in t.boarding_areas:
            for g in ba.gates:
                g.liberar()

    no_asignados_total = 0

    for h in range(24):
        time_str = f"{h:02d}:00"
        no_asignados = AssignGatesAtTime(bcn, merged_flights, time_str)
        no_asignados_total += no_asignados[1]

    messagebox.showinfo(
        "Simulación completada",
        f"Asignación dinámica finalizada.\n"
        f"Vuelos no asignados: {no_asignados_total}"
    )


# ==========================================
# INTERFAZ GRÁFICA
# ==========================================
root = Tk()
root.title("Gestión Aeroportuaria")
root.geometry("450x850")

titulo = Label(root, text="GESTIÓN AEROPUERTO", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# --- Bloque 1 ---
frame1 = LabelFrame(root, text="1. Aeropuertos", padx=10, pady=5)
frame1.pack(fill="x", padx=15, pady=5)

Button(frame1, text="Cargar Aeropuertos", command=load_airports).pack(fill="x")
Button(frame1, text="Guardar Aeropuertos", command=save_airports).pack(fill="x")
Button(frame1, text="Añadir", command=add_airport).pack(fill="x")
Button(frame1, text="Eliminar", command=remove_airport).pack(fill="x")
Button(frame1, text="Gráfico Aeropuertos", command=plot_airports).pack(fill="x")
Button(frame1, text="Ver Mapa", command=map_airports).pack(fill="x")

# --- Bloque 2 ---
frame2 = LabelFrame(root, text="2. Infraestructura LEBL", padx=10, pady=5)
frame2.pack(fill="x", padx=15, pady=5)

Button(frame2, text="Cargar LEBL.txt", command=load_lebl_structure).pack(fill="x")
Button(frame2, text="Ver Estado Puertas", command=show_gate_occupancy).pack(fill="x")
Button(frame2, text="Asignar puertas", command=assign_gates_static).pack(fill="x")

# --- Bloque 3 ---
frame3 = LabelFrame(root, text="3. Operaciones", padx=10, pady=5)
frame3.pack(fill="x", padx=15, pady=5)

Button(frame3, text="Cargar Llegadas", command=load_arrivals).pack(fill="x")
Button(frame3, text="Cargar Salidas", command=load_departures).pack(fill="x")
Button(frame3, text="Fusionar Movimientos", command=merge_movements, bg="lightblue").pack(fill="x")
Button(frame3, text="Asignar puertas por hora", command=assign_gates_dynamic_day).pack(fill="x")

Label(frame3, text="--- Estadísticas ---").pack(pady=2)
Button(frame3, text="Gráfico Vuelos x Hora", command=plot_hours).pack(fill="x")
Button(frame3, text="Gráfico x Aerolínea", command=plot_airlines).pack(fill="x")
Button(frame3, text="Gráfico Vuelos Schengen", command=plot_schengen).pack(fill="x")

Label(frame3, text="--- Mapas ---").pack(pady=2)
Button(frame3, text="Mapa Trayectorias (Todas)", command=map_flights_all).pack(fill="x")
Button(frame3, text="Mapa Trayectorias (>2000km)", command=map_flights_long).pack(fill="x")

# Botón Principal
Button(root, text="Grafico de ocupacion por hora", font=("Arial", 11, "bold"), bg="lightgreen", height=2, command=run_simulation).pack(fill="x", padx=15, pady=10)

Button(root, text="SALIR", command=root.quit, bg="red", fg="white").pack(pady=5)

root.mainloop()