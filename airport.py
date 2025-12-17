import matplotlib.pyplot as plt

class Airport:
    def __init__(self):
        self.code = ""
        self.latitude = 0.0
        self.longitude = 0.0
        self.schengen = True

def IsSchengenAirport(code):
    # Un estudiante usaría una lista normal, no un set {}
    if code == "":
        return False
    if len(code) < 2:
        return False
        
    codigos_schengen = [
        'LO', 'EB', 'LK', 'LC', 'EK', 'FO', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
        'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'GC', 'LE',
        'ES', 'LS'
    ]
    
    # Cogemos los dos primeros caracteres
    prefijo = code[0:2]
    prefijo = prefijo.upper()
    
    if prefijo in codigos_schengen:
        return True
    else:
        return False

def SetSchengen(airport):
    airport.schengen = IsSchengenAirport(airport.code)

def PrintAirport(airport):
    print("Code: " + airport.code + " Lat: " + str(airport.latitude) + " Lon: " + str(airport.longitude))

def convertir_coordenada(cadena):
    hemisferio = cadena[0]
    
    # Distinguir formato N/S o E/W por la longitud del texto o posición
    if hemisferio == 'N' or hemisferio == 'S':
        grados = int(cadena[1:3])
        minutos = int(cadena[3:5])
        segundos = int(cadena[5:7])
    else:
        grados = int(cadena[1:4])
        minutos = int(cadena[4:6])
        segundos = int(cadena[6:8])
        
    decimal = grados + (minutos / 60) + (segundos / 3600)
    
    if hemisferio == 'S' or hemisferio == 'W':
        decimal = -decimal
        
    return decimal

def LoadAirports(filename):
    airports = []
    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
    except:
        print("No se encontró el archivo: " + filename)
        return airports

    # Empezamos desde el 1 para saltar la cabecera
    for i in range(1, len(lines)):
        line = lines[i]
        if line.strip() == "":
            continue
            
        parts = line.split()
        if len(parts) != 3:
            continue
            
        try:
            code = parts[0]
            lat_str = parts[1]
            lon_str = parts[2]
            
            lat = convertir_coordenada(lat_str)
            lon = convertir_coordenada(lon_str)
            
            airport = Airport()
            airport.code = code.upper()
            airport.latitude = lat
            airport.longitude = lon
            SetSchengen(airport)
            
            airports.append(airport)
        except:
            # Si falla una línea, la saltamos y seguimos
            print("Error en linea: " + line)
            continue
            
    print("Se cargaron " + str(len(airports)) + " aeropuertos.")
    return airports

def SaveSchengenAirports(airports, filename):
    schengen_airports = []
    for i in range(len(airports)):
        a = airports[i]
        if a.schengen == True:
            schengen_airports.append(a)
            
    if len(schengen_airports) == 0:
        print("No hay aeropuertos Schengen.")
        return -1
        
    try:
        f = open(filename, "w")
        f.write("CODE LAT LON\n")
        for j in range(len(schengen_airports)):
            a = schengen_airports[j]
            linea = a.code + " " + "{:.6f}".format(a.latitude) + " " + "{:.6f}".format(a.longitude) + "\n"
            f.write(linea)
        f.close()
        print("Guardado correctamente.")
        return 0
    except:
        print("Error al guardar.")
        return -1

def AddAirport(airports, airport):
    for i in range(len(airports)):
        a = airports[i]
        if a.code == airport.code:
            print("El aeropuerto ya existe.")
            return -1
            
    airports.append(airport)
    print("Aeropuerto añadido.")
    return 0

def RemoveAirport(airports, code):
    encontrado = -1
    for i in range(len(airports)):
        if airports[i].code == code:
            encontrado = i
            break
            
    if encontrado != -1:
        airports.pop(encontrado)
        print("Aeropuerto eliminado.")
        return 0
    else:
        print("No se encontró el aeropuerto.")
        return -1

def PlotAirports(airports):
    if len(airports) == 0:
        print("No hay datos.")
        return
        
    # Contar manualmente en vez de usar sum()
    count_schengen = 0
    count_no_schengen = 0
    
    for i in range(len(airports)):
        if airports[i].schengen == True:
            count_schengen = count_schengen + 1
        else:
            count_no_schengen = count_no_schengen + 1
            
    plt.bar(["Schengen", "Non-Schengen"], [count_schengen, count_no_schengen], color=['green', 'red'])
    plt.title("Airports by Schengen Status")
    plt.ylabel("Number of Airports")
    plt.show()

def MapAirports(airports):
    if len(airports) == 0:
        return
        
    filename = "airports_map.kml"
    try:
        f = open(filename, "w", encoding="utf-8")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('<Document>\n')
        f.write('<name>Aeropuertos</name>\n')
        
        # Estilos
        f.write('<Style id="greenIcon"><IconStyle><color>ff00ff00</color><scale>1.2</scale><Icon><href>http://maps.google.com/mapfiles/kml/paddle/grn-circle.png</href></Icon></IconStyle></Style>\n')
        f.write('<Style id="redIcon"><IconStyle><color>ff0000ff</color><scale>1.2</scale><Icon><href>http://maps.google.com/mapfiles/kml/paddle/red-circle.png</href></Icon></IconStyle></Style>\n')
        
        for i in range(len(airports)):
            a = airports[i]
            f.write('<Placemark>\n')
            f.write('<name>' + a.code + '</name>\n')
            
            desc = "Aeropuerto " + a.code + "\nLat: " + str(a.latitude) + "\nLon: " + str(a.longitude)
            f.write('<description>' + desc + '</description>\n')
            
            if a.schengen:
                f.write('<styleUrl>#greenIcon</styleUrl>\n')
            else:
                f.write('<styleUrl>#redIcon</styleUrl>\n')
                
            f.write('<Point><coordinates>' + str(a.longitude) + ',' + str(a.latitude) + ',0</coordinates></Point>\n')
            f.write('</Placemark>\n')
            
        f.write('</Document>\n')
        f.write('</kml>\n')
        f.close()
        print("Mapa creado.")
    except:
        print("Error creando mapa.")