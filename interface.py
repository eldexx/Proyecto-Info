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


# FUNCIONES


def load_airports():
    global airports
    airports = LoadAirports("Airports.txt")
    if len(airports) > 0:
        messagebox.showinfo("Info", "Cargados " + str(len(airports)) + " aeropuertos.")
    else:
        messagebox.showwarning("Aviso", "No se cargaron aeropuertos. Revisa Airports.txt")

def save_airports():
    if len(airports) == 0:
        messagebox.showwarning("Error", "No hay datos para guardar.")
        return
    SaveSchengenAirports(airports, "schengen_airports.txt")
    messagebox.showinfo("Info", "Guardado en 'schengen_airports.txt'")

def add_airport():
    code = simpledialog.askstring("Añadir", "Código ICAO (ej: KJFK):")
    if code == None: return
    lat = simpledialog.askfloat("Añadir", "Latitud (Decimal):")
    if lat == None: return
    lon = simpledialog.askfloat("Añadir", "Longitud (Decimal):")
    if lon == None: return

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
    if code == None: return
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
    if len(airports) == 0: return
    MapAirports(airports)
    messagebox.showinfo("Info", "Mapa 'airports_map.kml' creado.")

def plot_airports():
    if len(airports) == 0: 
        messagebox.showwarning("Error", "Carga aeropuertos primero.")
        return
    PlotAirports(airports)

# LEBL 
def load_lebl_structure():
    global bcn
    bcn = LoadAirportStructure("Terminals.txt")
    if bcn != None:
        messagebox.showinfo("Info", "Estructura cargada correctamente.")
    else:
        messagebox.showerror("Error", "No se encontró 'Terminals.txt'.")

def show_gate_occupancy():
    if bcn == None:
        messagebox.showwarning("Error", "Carga la estructura del aeropuerto primero.")
        return
    
    alguna_ocupada = False
    for i in range(len(bcn.terminales)):
        t = bcn.terminales[i]
        for j in range(len(t.boarding_areas)):
            ba = t.boarding_areas[j]
            for k in range(len(ba.gates)):
                if ba.gates[k].ocupado == True:
                    alguna_ocupada = True

    if not alguna_ocupada:
        messagebox.showinfo("Aviso", "Todas las puertas están libres.\nAsigna vuelos primero.")

    win = Toplevel()
    win.title("Ocupación de Gates - LEBL")
    win.geometry("700x500")
    text = Text(win, width=85, height=25)
    text.pack(padx=10, pady=10)
    text.insert(END, "TERMINAL | AREA | GATE | ESTADO | AVIÓN\n")
    text.insert(END, "===============================================\n")

    for i in range(len(bcn.terminales)):
        t = bcn.terminales[i]
        text.insert(END, "\n--- TERMINAL " + t.nombre + " ---\n")
        for j in range(len(t.boarding_areas)):
            ba = t.boarding_areas[j]
            tipo = "Non-Schengen"
            if ba.tipo == "Schengen": tipo = "Schengen"
            text.insert(END, " Área " + ba.nombre + " (" + tipo + ")\n")
            for k in range(len(ba.gates)):
                g = ba.gates[k]
                estado = "LIBRE"
                avion = "-"
                if g.ocupado == True:
                    estado = "OCUPADA"
                    if g.id_aeronave != None: avion = g.id_aeronave
                linea = "    " + g.nombre + " | " + estado + " | " + avion + "\n"
                text.insert(END, linea)
    text.config(state=DISABLED)

def assign_gates_static():
    if bcn == None or len(aircrafts) == 0:
        messagebox.showwarning("Error", "Faltan datos.")
        return
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
        if res == 0: asignados = asignados + 1
    messagebox.showinfo("Resultado", "Asignados: " + str(asignados))

#  Vuelos 
def load_arrivals():
    global aircrafts
    aircrafts = LoadArrivals("Arrivals.txt")
    if len(aircrafts) > 0:
        messagebox.showinfo("Info", "Cargadas " + str(len(aircrafts)) + " llegadas.")
    else:
        messagebox.showwarning("Aviso", "No se cargaron llegadas.")

def load_departures():
    global departures
    departures = LoadDepartures("Departures.txt")
    if len(departures) > 0:
        messagebox.showinfo("Info", "Cargadas " + str(len(departures)) + " salidas.")
    else:
        messagebox.showwarning("Aviso", "No se cargaron salidas.")

def merge_movements():
    global merged_flights
    if len(aircrafts) == 0 and len(departures) == 0:
        messagebox.showwarning("Error", "Carga Llegadas y Salidas primero.")
        return
    merged_flights = MergeMovements(aircrafts, departures)
    messagebox.showinfo("Info", "Fusion OK. Total: " + str(len(merged_flights)))

def run_simulation():
    if bcn == None or len(merged_flights) == 0:
        messagebox.showerror("Error", "Faltan Datos (Estructura o Vuelos fusionados)")
        return
    PlotDayOccupancy(bcn, merged_flights)

def map_flights_all():
    lista = []
    if len(merged_flights) > 0: lista = merged_flights
    else: lista = aircrafts
    if len(lista) == 0: return
    MapFlights(lista, only_long_distance=False)
    messagebox.showinfo("Info", "KML creado.")

def map_flights_long():
    lista = []
    if len(merged_flights) > 0: lista = merged_flights
    else: lista = aircrafts
    if len(lista) == 0: return
    MapFlights(lista, only_long_distance=True)
    messagebox.showinfo("Info", "KML creado.")

def plot_hours(): 
    if len(aircrafts) > 0: PlotArrivals(aircrafts)
def plot_airlines(): 
    if len(aircrafts) > 0: PlotAirlines(aircrafts)
def plot_schengen(): 
    if len(aircrafts) > 0: PlotFlightsType(aircrafts)

# Extras
def plot_ranking_gates():
    if bcn == None:
        messagebox.showwarning("Error", "Carga estructura y simula primero.")
        return
    PlotGateRanking(bcn)

def plot_market_share():
    if len(aircrafts) > 0: PlotMarketShare(aircrafts)
    elif len(merged_flights) > 0: PlotMarketShare(merged_flights)
    else: messagebox.showwarning("Error", "Carga vuelos primero.")

def open_flight_finder():
    finder = Toplevel(root)
    finder.title("Buscador")
    finder.geometry("400x400")
    Label(finder, text="Aerolínea (ej: VLG):").pack(pady=5)
    entry_airline = Entry(finder)
    entry_airline.pack(pady=5)
    text_results = Text(finder, height=15, width=45)
    text_results.pack(pady=10)
    
    def perform_search():
        target = entry_airline.get().upper()
        text_results.delete(1.0, END)
        lista = []
        if len(merged_flights) > 0: lista = merged_flights
        else: lista = aircrafts
        count = 0
        for i in range(len(lista)):
            a = lista[i]
            if a.airline == target:
                info = a.id + " | Org:" + a.origin + " | Dest:" + a.destination + "\n"
                text_results.insert(END, info)
                count = count + 1
        if count == 0: messagebox.showinfo("Buscador", "No se encontraron vuelos.")
            
    Button(finder, text="Buscar", command=perform_search, bg="#ffcc80").pack(pady=5)



# INTERFAZ GRÁFICA 


root = Tk()
root.title("Gestión Aeroportuaria")
root.geometry("600x750") # Altura reducida para que quepa en cualquier pantalla
root.configure(bg="#e6f7ff") 

titulo = Label(root, text="GESTIÓN AEROPUERTO LEBL", font=("Arial", 16, "bold"), bg="#e6f7ff", fg="#003366")
titulo.pack(pady=10)

#  Bloque 1: Aeropuertos 
frame1 = LabelFrame(root, text=" 1. Base de Datos Aeropuertos ", font=("Arial", 9, "bold"), padx=5, pady=5, bg="white", fg="blue")
frame1.pack(fill="x", padx=10, pady=2)

# Fila 1: Cargar y Guardar juntos
f1_row1 = Frame(frame1, bg="white")
f1_row1.pack(fill="x", pady=1)
Button(f1_row1, text="📂 Cargar Aeropuertos", width=25, command=load_airports, bg="#f0f0f0").pack(side=LEFT, padx=5)
Button(f1_row1, text="💾 Guardar Aeropuertos", width=25, command=save_airports, bg="#f0f0f0").pack(side=RIGHT, padx=5)

# Fila 2: Añadir y Eliminar juntos
f1_row2 = Frame(frame1, bg="white")
f1_row2.pack(fill="x", pady=1)
Button(f1_row2, text="➕ Añadir", width=25, command=add_airport, bg="#e1f5fe").pack(side=LEFT, padx=5)
Button(f1_row2, text="➖ Eliminar", width=25, command=remove_airport, bg="#ffebee").pack(side=RIGHT, padx=5)

# Fila 3: Grafico y Mapa juntos
f1_row3 = Frame(frame1, bg="white")
f1_row3.pack(fill="x", pady=1)
Button(f1_row3, text="📊 Gráfico Aeropuertos", width=25, command=plot_airports, bg="#fff3e0").pack(side=LEFT, padx=5)
Button(f1_row3, text="🌍 Ver Mapa (Google Earth)", width=25, command=map_airports, bg="#e8f5e9").pack(side=RIGHT, padx=5)


# Bloque 2: Infraestructura 
frame2 = LabelFrame(root, text=" 2. Infraestructura LEBL ", font=("Arial", 9, "bold"), padx=5, pady=5, bg="white", fg="blue")
frame2.pack(fill="x", padx=10, pady=2)

f2_row1 = Frame(frame2, bg="white")
f2_row1.pack(fill="x", pady=1)
Button(f2_row1, text="📂 Cargar Estructura", width=25, command=load_lebl_structure, bg="#f0f0f0").pack(side=LEFT, padx=5)
Button(f2_row1, text="👁️ Ver Estado Puertas", width=25, command=show_gate_occupancy, bg="#fff3e0").pack(side=RIGHT, padx=5)

Button(frame2, text="⚡ Asignar puertas (Solo llegadas)", command=assign_gates_static, bg="#e3f2fd").pack(fill="x", padx=5, pady=2)


# Bloque 3: Operaciones 
frame3 = LabelFrame(root, text=" 3. Operaciones y Simulación ", font=("Arial", 9, "bold"), padx=5, pady=5, bg="white", fg="blue")
frame3.pack(fill="x", padx=10, pady=2)

f3_row1 = Frame(frame3, bg="white")
f3_row1.pack(fill="x", pady=1)
Button(f3_row1, text="📥 Cargar Llegadas", width=25, command=load_arrivals, bg="#f0f0f0").pack(side=LEFT, padx=5)
Button(f3_row1, text="📤 Cargar Salidas", width=25, command=load_departures, bg="#f0f0f0").pack(side=RIGHT, padx=5)

Button(frame3, text="🔄 Fusionar Movimientos", command=merge_movements, bg="#bbdefb").pack(fill="x", padx=5, pady=2)

Label(frame3, text="--- Estadísticas y Extras ---", bg="white", fg="grey", font=("Arial", 8)).pack(pady=1)

f3_row2 = Frame(frame3, bg="white")
f3_row2.pack(fill="x", pady=1)
Button(f3_row2, text="📊 Vuelos x Hora", width=25, command=plot_hours, bg="#fff3e0").pack(side=LEFT, padx=5)
Button(f3_row2, text="📊 Vuelos Schengen", width=25, command=plot_schengen, bg="#fff3e0").pack(side=RIGHT, padx=5)

f3_row3 = Frame(frame3, bg="white")
f3_row3.pack(fill="x", pady=1)
Button(f3_row3, text="★ Market Share", width=25, command=plot_market_share, bg="#fff9c4").pack(side=LEFT, padx=5)
Button(f3_row3, text="★ Ranking Puertas", width=25, command=plot_ranking_gates, bg="#fff9c4").pack(side=RIGHT, padx=5)

Button(frame3, text="★ Buscador de Vuelos", command=open_flight_finder, bg="#fff9c4").pack(fill="x", padx=5, pady=2)

Label(frame3, text="--- Mapas ---", bg="white", fg="grey", font=("Arial", 8)).pack(pady=1)
f3_row4 = Frame(frame3, bg="white")
f3_row4.pack(fill="x", pady=1)
Button(f3_row4, text="🌍 Mapa (Todas)", width=25, command=map_flights_all, bg="#e8f5e9").pack(side=LEFT, padx=5)
Button(f3_row4, text="🌍 Mapa (>2000km)", width=25, command=map_flights_long, bg="#e8f5e9").pack(side=RIGHT, padx=5)


# BOTONES PRINCIPALES
f_main = Frame(root, bg="#e6f7ff")
f_main.pack(fill="x", padx=10, pady=10)

Button(f_main, text="GRÁFICO SIMULACIÓN (T1 vs T2)", font=("Arial", 11, "bold"), bg="#66bb6a", fg="white", height=2, command=run_simulation).pack(fill="x", pady=5)

Button(f_main, text="CERRAR PROGRAMA", font=("Arial", 11, "bold"), bg="#d32f2f", fg="white", height=2, bd=4, relief=RAISED, command=root.quit).pack(fill="x", pady=5)

root.mainloop()