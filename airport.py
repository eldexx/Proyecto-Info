
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
    # ================================================
# STEP 3 - Manejo de listas de aeropuertos
# ================================================

# Función para convertir coordenadas del formato N635906 a decimal
def convertir_coordenada(cadena):
    hemisferio = cadena[0]
    grados = int(cadena[1:3])
    minutos = int(cadena[3:5])
    segundos = int(cadena[5:7])

    decimal = grados + minutos / 60 + segundos / 3600

    if hemisferio == "S" or hemisferio == "W":
        decimal = -decimal

    return decimal


def LoadAirports(filename):
    """Lee un archivo de texto con la lista de aeropuertos y devuelve una lista de objetos Airport"""
    airports = []

    try:
        f = open(filename, "r")
    except FileNotFoundError:
        print("No se encontró el archivo:", filename)
        return airports  # lista vacía

    lines = f.readlines()
    f.close()

    # Saltamos la primera línea (encabezado)
    for line in lines[1:]:
        if line.strip() == "":
            continue  # ignorar líneas vacías

        parts = line.strip().split()
        if len(parts) != 3:
            continue  # si no hay tres datos, se salta

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
    """Agrega un aeropuerto a la lista si no existe ya"""
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
    """Elimina un aeropuerto de la lista por su código"""
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
    with open("airports.kml", "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n')
        for a in airports:
            color = "green" if a.schengen else "red"
            f.write(f"""
<Placemark>
<name>{a.code}</name>
<Style><IconStyle><color>{color}</color></IconStyle></Style>
<Point><coordinates>{a.lon},{a.lat},0</coordinates></Point>
</Placemark>
""")
        f.write('</Document>\n</kml>')


