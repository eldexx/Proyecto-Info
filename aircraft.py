import matplotlib.pyplot as plt
from airport import IsSchengenAirport

def time_to_minutes(time_str):
    # Comprobación básica
    if time_str == "":
        return 0
    # Comprobar si tiene :
    tiene_dos_puntos = False
    for char in time_str:
        if char == ':':
            tiene_dos_puntos = True
            
    if not tiene_dos_puntos:
        return 0
        
    try:
        parts = time_str.split(":")
        h = int(parts[0])
        m = int(parts[1])
        resultado = (h * 60) + m
        return resultado
    except:
        return 0

class Aircraft:
    def __init__(self):
        self.id = ""
        self.airline = ""
        self.origin = "" 
        self.destination = "" 
        self.landing_time = "" 
        self.departure_time = "" 
        self.schengen = False

    def __repr__(self):
        return "[" + self.id + "] Arr:" + self.landing_time + " Dep:" + self.departure_time

def LoadArrivals(filename):
    aircrafts = []
    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
    except:
        print("Archivo no encontrado")
        return aircrafts

    # Bucle normal con i
    for i in range(1, len(lines)):
        line = lines[i]
        line = line.strip()
        if line == "":
            continue
            
        parts = line.split()
        if len(parts) < 4:
            continue

        try:
            a = Aircraft()
            a.id = parts[0]
            a.origin = parts[1]
            a.landing_time = parts[2]
            a.airline = parts[3]
            a.schengen = IsSchengenAirport(a.origin)
            aircrafts.append(a)
        except:
            continue
            
    return aircrafts

def LoadDepartures(filename):
    aircrafts = []
    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
    except:
        print("Archivo no encontrado")
        return aircrafts

    for i in range(1, len(lines)):
        line = lines[i]
        line = line.strip()
        if line == "":
            continue
            
        parts = line.split()
        if len(parts) < 4:
            continue

        try:
            a = Aircraft()
            a.id = parts[0]
            a.destination = parts[1]
            a.departure_time = parts[2]
            a.airline = parts[3]
            # Usamos destination para saber si es schengen
            a.schengen = IsSchengenAirport(a.destination) 
            aircrafts.append(a)
        except:
            continue
            
    return aircrafts

def MergeMovements(arrivals, departures):
    merged_dict = {}

    # 1. Meter todas las llegadas en el diccionario
    for i in range(len(arrivals)):
        a = arrivals[i]
        merged_dict[a.id] = a

    # 2. Procesar salidas
    for j in range(len(departures)):
        d = departures[j]
        
        # Comprobar si ya existe en el diccionario
        if d.id in merged_dict:
            # Ya existe, es un avion que llegó hoy
            avion_existente = merged_dict[d.id]
            
            llegada_min = time_to_minutes(avion_existente.landing_time)
            salida_min = time_to_minutes(d.departure_time)
            
            if llegada_min < salida_min:
                avion_existente.destination = d.destination
                avion_existente.departure_time = d.departure_time
            else:
                # Error de datos, lo ignoramos
                pass
        else:
            # No estaba, es un avion que durmió aquí
            merged_dict[d.id] = d
    
    # Convertir los valores del diccionario a lista
    lista_final = []
    for key in merged_dict:
        lista_final.append(merged_dict[key])
        
    return lista_final

def NightAircraft(aircrafts):
    night_list = []
    for i in range(len(aircrafts)):
        a = aircrafts[i]
        if a.landing_time == "":
            night_list.append(a)
    return night_list

def PlotArrivals(aircrafts):
    if len(aircrafts) == 0:
        return
        
    hours = []
    for k in range(24):
        hours.append(0)
        
    for i in range(len(aircrafts)):
        a = aircrafts[i]
        if a.landing_time != "":
            try:
                parts = a.landing_time.split(':')
                h = int(parts[0])
                hours[h] = hours[h] + 1
            except:
                pass
    
    plt.figure(figsize=(10, 5))
    plt.bar(range(24), hours, color='skyblue', edgecolor='black')
    plt.title('Llegadas por Hora')
    plt.show()

def PlotAirlines(aircrafts):
    if len(aircrafts) == 0:
        return
        
    counts = {}
    for i in range(len(aircrafts)):
        a = aircrafts[i]
        if a.airline in counts:
            counts[a.airline] = counts[a.airline] + 1
        else:
            counts[a.airline] = 1
    
    names = []
    values = []
    for key in counts:
        names.append(key)
        values.append(counts[key])
    
    plt.figure(figsize=(10, 5))
    plt.bar(names, values, color='orange')
    plt.title('Vuelos por Aerolinea')
    plt.show()

def PlotFlightsType(aircrafts):
    if len(aircrafts) == 0:
        return
        
    sch = 0
    non_sch = 0
    for i in range(len(aircrafts)):
        if aircrafts[i].schengen == True:
            sch = sch + 1
        else:
            non_sch = non_sch + 1
            
    plt.bar(["Schengen", "Non-Schengen"], [sch, non_sch], color=['green', 'red'])
    plt.title('Vuelos Schengen')
    plt.show()

def SaveFlights(aircrafts, filename):
    try:
        f = open(filename, "w")
        f.write("AIRCRAFT ORIGIN ARRIVAL DEST DEPARTURE AIRLINE\n")
        
        for i in range(len(aircrafts)):
            a = aircrafts[i]
            orig = a.origin
            if orig == "": orig = "----"
            
            arr = a.landing_time
            if arr == "": arr = "--:--"
            
            dest = a.destination
            if dest == "": dest = "----"
            
            dep = a.departure_time
            if dep == "": dep = "--:--"
            
            linea = a.id + " " + orig + " " + arr + " " + dest + " " + dep + " " + a.airline + "\n"
            f.write(linea)
            
        f.close()
        return 0
    except:
        return -1

def MapFlights(aircrafts, only_long_distance=False):
    if len(aircrafts) == 0:
        print("No hay vuelos.")
        return

    lista_a_pintar = []
    
    # Filtrado manual
    if only_long_distance == True:
        non_european = ['C', 'K', 'P', 'R', 'U', 'Z']
        for i in range(len(aircrafts)):
            a = aircrafts[i]
            if a.origin != "":
                primera_letra = a.origin[0]
                if primera_letra in non_european:
                    lista_a_pintar.append(a)
    else:
        lista_a_pintar = aircrafts

    filename = "flights_map.kml"
    lebl_lon = 2.0833
    lebl_lat = 41.2974

    f = open(filename, "w", encoding="utf-8")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    f.write('<name>Vuelos</name>\n')

    # Estilo amarillo
    f.write('<Style id="yellowLine"><LineStyle><color>7f00ffff</color><width>4</width></LineStyle></Style>\n')

    for j in range(len(lista_a_pintar)):
        a = lista_a_pintar[j]
        
        # Calculo simple para coordenadas falsas
        offset = 0
        if a.origin != "":
            offset = ord(a.origin[0])
            
        origin_lon = lebl_lon + (offset % 20 - 10) * 5 
        origin_lat = lebl_lat + (offset % 10 - 5) * 5

        f.write('<Placemark>\n')
        f.write('<name>' + a.airline + ' ' + a.id + '</name>\n')
        f.write('<styleUrl>#yellowLine</styleUrl>\n')
        f.write('<LineString>\n')
        f.write('<extrude>1</extrude><tessellate>1</tessellate>\n')
        f.write('<coordinates>\n')
        f.write(str(origin_lon) + ',' + str(origin_lat) + ',0\n')
        f.write(str(lebl_lon) + ',' + str(lebl_lat) + ',0\n')
        f.write('</coordinates>\n')
        f.write('</LineString>\n')
        f.write('</Placemark>\n')

    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()
    
    print("Mapa generado.")
    