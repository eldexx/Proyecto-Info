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
                        'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'GC', 'LE',
                        'ES', 'LS'}
    return code[:2].upper() in codigos_schengen


def SetSchengen(airport):
    airport.schengen = IsSchengenAirport(airport.code)


def PrintAirport(airport):
    print(
        f"Code: {airport.code}, Lat: {airport.latitude:.6f}, Lon: {airport.longitude:.6f}, Schengen: {airport.schengen}")


def convertir_coordenada(cadena):
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
    airports = []
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("No se encontró el archivo:", filename)
        return airports

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
        airport.code = code.upper()
        airport.latitude = lat
        airport.longitude = lon
        SetSchengen(airport)

        airports.append(airport)

    print(f"Se cargaron {len(airports)} aeropuertos del archivo {filename}")
    return airports


def SaveSchengenAirports(airports, filename):
    schengen_airports = []
    for a in airports:
        if a.schengen:
            schengen_airports.append(a)

    if len(schengen_airports) == 0:
        print("No hay aeropuertos Schengen para guardar.")
        return -1

    with open(filename, "w") as f:
        f.write("CODE LAT LON\n")
        for a in schengen_airports:
            f.write(f"{a.code} {a.latitude:.6f} {a.longitude:.6f}\n")

    print(f"Se guardaron {len(schengen_airports)} aeropuertos Schengen en {filename}")
    return 0


def AddAirport(airports, airport):
    for a in airports:
        if a.code == airport.code:
            print(f"El aeropuerto {airport.code} ya existe.")
            return -1

    airports.append(airport)
    print(f"Aeropuerto {airport.code} agregado correctamente.")
    return 0


def RemoveAirport(airports, code):
    for i, a in enumerate(airports):
        if a.code == code:
            airports.pop(i)
            print(f"Aeropuerto {code} eliminado.")
            return 0

    print(f"No se encontró el aeropuerto {code}.")
    return -1


import matplotlib.pyplot as plt


def PlotAirports(airports):
    if not airports:
        print("No hay aeropuertos para graficar")
        return

    schengen = sum(1 for a in airports if a.schengen)
    non_schengen = len(airports) - schengen

    plt.bar(["Schengen", "Non-Schengen"], [schengen, non_schengen], color=['green', 'red'])
    plt.title("Airports by Schengen Status")
    plt.ylabel("Number of Airports")
    plt.show()


def MapAirports(airports):
    if not airports:
        print("No hay aeropuertos para mostrar en el mapa.")
        return

    filename = "airports_map.kml"

    with open(filename, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('<Document>\n')
        f.write('<name>Aeropuertos</name>\n')

        # Definir estilos
        f.write('<Style id="greenIcon">\n')
        f.write('  <IconStyle>\n')
        f.write('    <color>ff00ff00</color>\n')
        f.write('    <scale>1.2</scale>\n')
        f.write('    <Icon>\n')
        f.write('      <href>http://maps.google.com/mapfiles/kml/paddle/grn-circle.png</href>\n')
        f.write('    </Icon>\n')
        f.write('  </IconStyle>\n')
        f.write('</Style>\n')

        f.write('<Style id="redIcon">\n')
        f.write('  <IconStyle>\n')
        f.write('    <color>ff0000ff</color>\n')
        f.write('    <scale>1.2</scale>\n')
        f.write('    <Icon>\n')
        f.write('      <href>http://maps.google.com/mapfiles/kml/paddle/red-circle.png</href>\n')
        f.write('    </Icon>\n')
        f.write('  </IconStyle>\n')
        f.write('</Style>\n')

        for a in airports:
            f.write('<Placemark>\n')
            f.write(f'  <name>{a.code}</name>\n')
            f.write(
                f'  <description>Aeropuerto {a.code}\nLatitud: {a.latitude:.6f}\nLongitud: {a.longitude:.6f}\nSchengen: {"SÍ" if a.schengen else "NO"}</description>\n')
            if a.schengen:
                f.write('  <styleUrl>#greenIcon</styleUrl>\n')
            else:
                f.write('  <styleUrl>#redIcon</styleUrl>\n')
            f.write('  <Point>\n')
            f.write(f'    <coordinates>{a.longitude},{a.latitude},0</coordinates>\n')
            f.write('  </Point>\n')
            f.write('</Placemark>\n')

        f.write('</Document>\n')
        f.write('</kml>\n')

    print(f"Archivo '{filename}' creado correctamente. Ábrelo con Google Earth.")