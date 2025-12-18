import matplotlib.pyplot as plt
from aircraft import time_to_minutes

class Gate:
    def __init__(self, nombre):
        self.nombre = nombre
        self.ocupado = False
        self.id_aeronave = None
        self.free_at_time = 0 
        self.usage_count = 0 

    def asignar(self, id_aeronave, departure_time_str):
        self.ocupado = True
        self.id_aeronave = id_aeronave
        # Contamos el uso cada vez que se asigna
        self.usage_count = self.usage_count + 1
        
        if departure_time_str != "":
            self.free_at_time = time_to_minutes(departure_time_str)
        else:
            # Si no sale, bloqueamos todo el dia
            self.free_at_time = 3000

    def liberar(self):
        self.ocupado = False
        self.id_aeronave = None
        self.free_at_time = 0

class BoardingArea:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo 
        self.gates = []

class Terminal:
    def __init__(self, nombre):
        self.nombre = nombre
        self.boarding_areas = []
        self.airlines = []

    def agregar_boarding_area(self, area):
        self.boarding_areas.append(area)

class BarcelonaAP:
    def __init__(self, codigo_ICAO):
        self.codigo_ICAO = codigo_ICAO
        self.terminales = []

    def agregar_terminal(self, terminal):
        self.terminales.append(terminal)

def LoadAirlines(terminal, tname):
    filename = tname + "_Airlines.txt"
    try:
        f = open(filename, "r", encoding="utf-8")
        lines = f.readlines()
        f.close()
        
        terminal.airlines = []
        for i in range(len(lines)):
            line = lines[i]
            if line.strip() != "":
                parts = line.split("\t")
                icao = parts[len(parts)-1]
                icao = icao.strip()
                terminal.airlines.append(icao)
        return 0
    except:
        print("Warning: No se encontró " + filename)
        terminal.airlines = []
        return -1

def SetGates(area, initgate, endgate, prefix):
    if endgate <= initgate:
        return -1
    
    area.gates = []
    for n in range(initgate, endgate + 1):
        nombre = prefix + str(n)
        g = Gate(nombre)
        area.gates.append(g)
    return 0

def LoadAirportStructure(filename):
    try:
        f = open(filename, "r", encoding="utf-8")
        lines = f.readlines()
        f.close()
    except:
        print("Error: No se encontró " + filename)
        return None

    bcn = BarcelonaAP("LEBL")
    terminal = None
    
    for i in range(len(lines)):
        line = lines[i].strip()
        if line == "":
            continue
            
        parts = line.split()
        
        if parts[0] == "Terminal":
            if terminal != None:
                bcn.agregar_terminal(terminal)
            
            t_name = parts[1]
            terminal = Terminal(t_name)
            LoadAirlines(terminal, t_name)
            
        elif parts[0] == "Area":
            if len(parts) >= 6:
                nombre_area = parts[1]
                tipo = parts[2]
                prefijo = nombre_area 
                
                try:
                    init = int(parts[4])
                    end = int(parts[6])
                    
                    area = BoardingArea(nombre_area, tipo)
                    SetGates(area, init, end, prefijo)
                    terminal.agregar_boarding_area(area)
                except:
                    print("Error leyendo area")
            
    if terminal != None:
        bcn.agregar_terminal(terminal)
        
    return bcn

def IsAirlineInTerminal(terminal, name):
    if name in terminal.airlines:
        return True
    else:
        return False

def SearchTerminal(bcn, airline_name):
    for i in range(len(bcn.terminales)):
        t = bcn.terminales[i]
        if IsAirlineInTerminal(t, airline_name):
            return t
    return None

def GateOccupancy(bcn):
    data = []
    for i in range(len(bcn.terminales)):
        t = bcn.terminales[i]
        for j in range(len(t.boarding_areas)):
            ba = t.boarding_areas[j]
            for k in range(len(ba.gates)):
                g = ba.gates[k]
                
                info = {}
                info["gate"] = g.nombre
                info["ocupado"] = g.ocupado
                info["id"] = g.id_aeronave
                info["free_at"] = g.free_at_time
                data.append(info)
    return data

def FreeGate(bcn, aircraft_id):
    for i in range(len(bcn.terminales)):
        t = bcn.terminales[i]
        for j in range(len(t.boarding_areas)):
            ba = t.boarding_areas[j]
            for k in range(len(ba.gates)):
                g = ba.gates[k]
                if g.id_aeronave == aircraft_id:
                    g.liberar()
                    return 0
    return -1

def AssignGate(bcn, aircraft):
    target_terminal = SearchTerminal(bcn, aircraft.airline)
    if target_terminal == None:
        return -1 

    flight_type = "non-Schengen"
    if aircraft.schengen == True:
        flight_type = "Schengen"
    
    for i in range(len(target_terminal.boarding_areas)):
        ba = target_terminal.boarding_areas[i]
        
        tipo_ba = ba.tipo.lower()
        tipo_vuelo = flight_type.lower()
        
        if tipo_vuelo in tipo_ba:
            for j in range(len(ba.gates)):
                g = ba.gates[j]
                if g.ocupado == False:
                    g.asignar(aircraft.id, aircraft.departure_time)
                    return 0 
    return -2 

def AssignNightGates(bcn, aircrafts):
    count = 0
    for i in range(len(aircrafts)):
        a = aircrafts[i]
        if a.landing_time == "": 
            res = AssignGate(bcn, a)
            if res == 0:
                count = count + 1
    return count

def AssignGatesAtTime(bcn, aircrafts, time_str):
    current_mins = time_to_minutes(time_str)
    
    for i in range(len(bcn.terminales)):
        t = bcn.terminales[i]
        for j in range(len(t.boarding_areas)):
            ba = t.boarding_areas[j]
            for k in range(len(ba.gates)):
                g = ba.gates[k]
                if g.ocupado == True:
                    if g.free_at_time <= current_mins:
                        g.liberar()

    assigned = 0
    errors = 0
    start_interval = current_mins
    end_interval = current_mins + 59
    
    for i in range(len(aircrafts)):
        a = aircrafts[i]
        if a.landing_time != "":
            arr_min = time_to_minutes(a.landing_time)
            
            if arr_min >= start_interval:
                if arr_min <= end_interval:
                    res = AssignGate(bcn, a)
                    if res == 0:
                        assigned = assigned + 1
                    else:
                        errors = errors + 1
                    
    return assigned, errors

def PlotDayOccupancy(bcn, aircrafts):
    for i in range(len(bcn.terminales)):
        t = bcn.terminales[i]
        for j in range(len(t.boarding_areas)):
            ba = t.boarding_areas[j]
            for k in range(len(ba.gates)):
                g = ba.gates[k]
                g.liberar()

    AssignNightGates(bcn, aircrafts)
    
    hours = []
    for h in range(24):
        hours.append(h)
        
    occupancy_t1 = []
    occupancy_t2 = []
    missed_flights = []
    
    for h in range(24):
        time_str = "{:02d}:00".format(h)
        
        res = AssignGatesAtTime(bcn, aircrafts, time_str)
        missed_count = res[1]
        missed_flights.append(missed_count)
        
        occ1 = 0
        occ2 = 0
        
        for i in range(len(bcn.terminales)):
            t = bcn.terminales[i]
            
            count = 0
            for j in range(len(t.boarding_areas)):
                ba = t.boarding_areas[j]
                for k in range(len(ba.gates)):
                    if ba.gates[k].ocupado == True:
                        count = count + 1
            
            if "T1" in t.nombre:
                occ1 = count
            elif "T2" in t.nombre:
                occ2 = count
            
        occupancy_t1.append(occ1)
        occupancy_t2.append(occ2)

    plt.figure(figsize=(12, 6))
    plt.plot(hours, occupancy_t1, label="Ocupación T1", color="blue")
    plt.plot(hours, occupancy_t2, label="Ocupación T2", color="green")
    plt.bar(hours, missed_flights, label="Vuelos sin puerta", color="red", alpha=0.5)
    
    plt.xlabel("Hora del día")
    plt.ylabel("Numero de Gates / Vuelos")
    plt.title("Simulación de Ocupación Diaria LEBL")
    plt.legend()
    plt.grid(True)
    plt.xticks(hours)
    plt.show()

def PlotGateRanking(bcn):
    # Recolectar datos
    datos_puertas = []
    
    for i in range(len(bcn.terminales)):
        t = bcn.terminales[i]
        for j in range(len(t.boarding_areas)):
            ba = t.boarding_areas[j]
            for k in range(len(ba.gates)):
                g = ba.gates[k]
                if g.usage_count > 0:
                    # Guardamos 
                    datos_puertas.append( (g.nombre, g.usage_count) )
    
    if len(datos_puertas) == 0:
        print("No hay datos de uso.")
        return

    # 1. Ordenar de mayor a menor uso
    
    datos_puertas.sort(key=lambda x: x[1], reverse=True)

    # 2. Quedarnos solo con los 15 primeros (TOP 15)
    # Asi evitamos que el grafico se llene de barras
    top_puertas = datos_puertas[:15]
    
    # 3. Invertir para que el mas usado salga arriba en la grafica
    top_puertas.reverse()

    nombres = []
    usos = []
    for item in top_puertas:
        nombres.append(item[0])
        usos.append(item[1])

    # 4. Crear grafico limpio
    plt.figure(figsize=(10, 8))
    plt.barh(nombres, usos, color='purple')
    plt.xlabel('Número de aviones asignados')
    plt.title('Ranking de Uso: TOP 15 Puertas más activas')
    plt.grid(axis='x', linestyle='--', alpha=0.7) # Añadir rejilla para leer mejor
    plt.tight_layout()
    plt.show()