
class Airport:
    def __init__(self):
        self.code = ""
        self.latitude = 0.0
        self.longitude = 0.0
        self.schengen = True

def IsSchengenAirport(code):
   if not code or len(code) < 2:
       return False
   codigos_schengen = {'LO', 'EB', 'LK', 'LC', 'EK', 'FO', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
'BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'GC', 'LE',
'ES', 'LS'}
   return code[:2].upper() in codigos_schengen

def SetSchengen (airport):
    airport.schengen = IsSchengenAirport(airport.code)

def PrintAirport (airport):
    print(airport.__dict__)

def LoadAirports(filename):
    try:
        f = open(filename, "r")
        lines = f.readlines()
    except FileNotFoundError:
        return []

    airports = []
    while lines != "":
        parts = lines.split(" ")
        code = parts[0]
        lat_str = parts[1]
        lon_str = parts[2]

        hem = lat_str[0]
        deg = int(lat_str[1:3])
        min = int(lat_str[3:5])
        sec = int(lat_str[5:7])
        lat = deg + min / 60 + sec / 3600
        if hem == "S":
            lat = -lat

        hem = int(lon_str[0])
        deg = int(lon_str[1:4])
        min = int(lon_str[4:6])
        sec = int(lon_str[6:8])
        lon = deg + min / 60 + sec / 3600
        if hem == "W":
            lon = -lon

        airports.append((code, lat, lon))

        lines = f.readline()
    return airports
  
def convertir_coordenada(cadena):
    """Convierte una coordenada tipo N412944 o W0734429 a grados decimales correctos."""
    hemisferio = cadena[0]

   
    if hemisferio in ['N', 'S']:
        grados = int(cadena[1:3])
        minutos = int(cadena[3:5])
        segundos = int(cadena[5:7])
  
    else:
        grados = int(cadena[1:4])
        minutos = int(cadena[4:6])
        segundos = int(cadena[6:8])

    decimal = grados + (minutos / 60) + (segundos / 3600)

   
    if hemisferio in ['S', 'W']:
        decimal = -decimal

    return decimal


def LoadAirports(filename):
    """Lee un archivo de texto con la lista de aeropuertos y devuelve una lista de objetos Airport."""
    airports = []

    try:
        f = open(filename, "r")
    except FileNotFoundError:
        print("No se encontró el archivo:", filename)
        return airports  

    lines = f.readlines()
    f.close()

   
    for line in lines[1:]:
        if line.strip() == "":
            continue 

        parts = line.strip().split()
        if len(parts) != 3:
            continue  

        code = parts[0]
        lat_str = parts[1]
        lon_str = parts[2]

       
        lat = convertir_coordenada(lat_str)
        lon = convertir_coordenada(lon_str)

        airport = Airport()
        airport.code = code
        airport.latitude = lat
        airport.longitude = lon
        SetSchengen(airport)

        airports.append(airport)

    print(f"Se cargaron {len(airports)} aeropuertos del archivo {filename}")
    return airports


def SaveSchengenAirports(airports, filename):
    """Guarda solo los aeropuertos Schengen en un archivo nuevo"""
    schengen_airports = []
    for a in airports:
        if a.schengen:
            schengen_airports.append(a)

    if len(schengen_airports) == 0:
        print("No hay aeropuertos Schengen para guardar.")
        return -1

    f = open(filename, "w")
    f.write("CODE LAT LON\n")
    for a in schengen_airports:
        f.write(f"{a.code} {a.latitude:.6f} {a.longitude:.6f}\n")
    f.close()

    print(f"Se guardaron {len(schengen_airports)} aeropuertos Schengen en {filename}")
    return 0


def AddAirport(airports, airport):
   
    existe = False
    for a in airports:
        if a.code == airport.code:
            existe = True
            break

    if existe:
        print(f"El aeropuerto {airport.code} ya existe.")
        return -1

    airports.append(airport)
    print(f"Aeropuerto {airport.code} agregado correctamente.")
    return 0


def RemoveAirport(airports, code):
   
    encontrado = False
    for a in airports:
        if a.code == code:
            airports.remove(a)
            encontrado = True
            print(f"Aeropuerto {code} eliminado.")
            break

    if not encontrado:
        print(f"No se encontró el aeropuerto {code}.")
        return -1

    return 0

import matplotlib.pyplot as plt

def PlotAirports(airports):
    schengen = sum(a.schengen for a in airports)
    non_schengen = len(airports) - schengen
    plt.bar(["Schengen", "Non-Schengen"], [schengen, non_schengen])
    plt.title("Airports by Schengen Status")
    plt.show()


def MapAirports(airports):
   
    if len(airports) == 0:
        print("No hay aeropuertos para mostrar en el mapa.")
        return

    filename = "airports_map.kml"

    with open(filename, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write("  <Document>\n")
        f.write("    <name>Airport Map</name>\n")

        for a in airports:
            
            color = "ff00ff00" if a.schengen else "ff0000ff"

            f.write("    <Placemark>\n")
            f.write(f"      <name>{a.code}</name>\n")
            f.write("      <Style>\n")
            f.write("        <IconStyle>\n")
            f.write(f"          <color>{color}</color>\n")
            f.write("          <scale>1.2</scale>\n")
            f.write("          <Icon>\n")
            f.write("            <href>http://maps.google.com/mapfiles/kml/paddle/A.png</href>\n")
            f.write("          </Icon>\n")
            f.write("        </IconStyle>\n")
            f.write("      </Style>\n")
            f.write("      <Point>\n")
           
            f.write(f"        <coordinates>{a.longitude},{a.latitude},0</coordinates>\n")
            f.write("      </Point>\n")
            f.write("    </Placemark>\n")

        f.write("  </Document>\n")
        f.write("</kml>\n")

    print(f"Archivo '{filename}' creado correctamente.")




