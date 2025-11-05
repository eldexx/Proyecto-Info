import matplotlib.pyplot as plt
from airport import IsSchengenAirport
import math


class Aircraft:
    def __init__(self):
        self.id = ""
        self.airline = ""
        self.origin = ""
        self.landing_time = ""
        self.schengen = False


def LoadArrivals(filename):
    aircrafts = []
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Archivo {filename} no encontrado")
        return aircrafts

    for line in lines[1:]:
        if line.strip() == "":
            continue

        parts = line.strip().split()
        if len(parts) < 4:
            continue

        try:
            aircraft = Aircraft()
            aircraft.id = parts[0]
            aircraft.origin = parts[1]
            aircraft.landing_time = parts[2]
            aircraft.airline = parts[3]
            aircraft.schengen = IsSchengenAirport(aircraft.origin)
            aircrafts.append(aircraft)
        except:
            continue

    print(f"Se cargaron {len(aircrafts)} vuelos desde {filename}")
    return aircrafts


def PlotArrivals(aircrafts):
    if not aircrafts:
        print("Error: Lista de vuelos vacía")
        return

    hours = [0] * 24
    for aircraft in aircrafts:
        try:
            hour = int(aircraft.landing_time.split(':')[0])
            hours[hour] += 1
        except:
            continue

    plt.figure(figsize=(12, 6))
    plt.bar(range(24), hours, color='skyblue', edgecolor='navy')
    plt.xlabel('Hora del día')
    plt.ylabel('Número de llegadas')
    plt.title('Frecuencia de llegadas por hora - Aeropuerto LEBL')
    plt.xticks(range(0, 24))
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def SaveFlights(aircrafts, filename):
    if not aircrafts:
        print("Error: No hay vuelos para guardar")
        return -1

    try:
        with open(filename, "w") as f:
            f.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")
            for aircraft in aircrafts:
                f.write(f"{aircraft.id} {aircraft.origin} {aircraft.landing_time} {aircraft.airline}\n")
        print(f"Vuelos guardados en {filename}")
        return 0
    except:
        return -1


def PlotAirlines(aircrafts):
    if not aircrafts:
        print("Error: Lista de vuelos vacía")
        return

    airlines = {}
    for aircraft in aircrafts:
        airline = aircraft.airline
        airlines[airline] = airlines.get(airline, 0) + 1

    plt.figure(figsize=(10, 6))
    colors = plt.cm.Set3(range(len(airlines)))
    bars = plt.bar(airlines.keys(), airlines.values(), color=colors)
    plt.xlabel('Aerolínea')
    plt.ylabel('Número de vuelos')
    plt.title('Vuelos por aerolínea - Aeropuerto LEBL')
    plt.xticks(rotation=45)

    # Añadir valores en las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{int(height)}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


def PlotFlightsType(aircrafts):
    if not aircrafts:
        print("Error: Lista de vuelos vacía")
        return

    schengen_count = sum(1 for a in aircrafts if a.schengen)
    non_schengen_count = len(aircrafts) - schengen_count

    plt.figure(figsize=(8, 6))
    bars = plt.bar(["Schengen", "No Schengen"], [schengen_count, non_schengen_count],
                   color=['#2ecc71', '#e74c3c'])
    plt.ylabel('Número de vuelos')
    plt.title('Vuelos Schengen vs No Schengen - Aeropuerto LEBL')

    # Añadir valores en las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{int(height)}', ha='center', va='bottom')

    plt.show()


def haversine(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en km
    R = 6371.0

    # Convertir a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferencia de coordenadas
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula de Haversine
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def LongDistanceArrivals(aircrafts):
    # Coordenadas de LEBL (Barcelona)
    LEBL_LAT = 41.297445
    LEBL_LON = 2.0832941

    long_distance = []

    # Por simplicidad, consideramos vuelos de larga distancia aquellos que vienen de fuera de Europa
    non_european_codes = ['C', 'K', 'P', 'R', 'U', 'Z']  # Prefijos de fuera de Europa

    for aircraft in aircrafts:
        if aircraft.origin[:1] in non_european_codes:
            long_distance.append(aircraft)

    print(f"Se identificaron {len(long_distance)} vuelos de larga distancia")
    return long_distance


def MapFlights(aircrafts):
    if not aircrafts:
        print("No hay vuelos para mostrar en el mapa")
        return

    filename = "flights_map.kml"

    with open(filename, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('<Document>\n')
        f.write('<name>Vuelos LEBL</name>\n')

        # Estilo para vuelos Schengen (verde)
        f.write('<Style id="schengenFlight">\n')
        f.write('  <IconStyle>\n')
        f.write('    <color>ff00ff00</color>\n')
        f.write('    <scale>1.2</scale>\n')
        f.write('    <Icon>\n')
        f.write('      <href>http://maps.google.com/mapfiles/kml/pal4/icon57.png</href>\n')
        f.write('    </Icon>\n')
        f.write('  </IconStyle>\n')
        f.write('</Style>\n')

        # Estilo para vuelos No Schengen (rojo)
        f.write('<Style id="nonSchengenFlight">\n')
        f.write('  <IconStyle>\n')
        f.write('    <color>ff0000ff</color>\n')
        f.write('    <scale>1.2</scale>\n')
        f.write('    <Icon>\n')
        f.write('      <href>http://maps.google.com/mapfiles/kml/pal4/icon57.png</href>\n')
        f.write('    </Icon>\n')
        f.write('  </IconStyle>\n')
        f.write('</Style>\n')

        # Coordenadas de LEBL
        LEBL_LON = 2.0832941
        LEBL_LAT = 41.297445

        for aircraft in aircrafts:
            f.write('<Placemark>\n')
            f.write(f'  <name>{aircraft.id} - {aircraft.origin}</name>\n')
            f.write(
                f'  <description>Vuelo: {aircraft.id}\nOrigen: {aircraft.origin}\nHora: {aircraft.landing_time}\nAerolínea: {aircraft.airline}\nSchengen: {"SÍ" if aircraft.schengen else "NO"}</description>\n')

            if aircraft.schengen:
                f.write('  <styleUrl>#schengenFlight</styleUrl>\n')
            else:
                f.write('  <styleUrl>#nonSchengenFlight</styleUrl>\n')

            f.write('  <Point>\n')
            f.write(f'    <coordinates>{LEBL_LON},{LEBL_LAT},0</coordinates>\n')
            f.write('  </Point>\n')
            f.write('</Placemark>\n')

        f.write('</Document>\n')
        f.write('</kml>\n')

    print(f"Archivo '{filename}' creado. Ábrelo con Google Earth.")


# Sección de pruebas
if __name__ == "__main__":
    print("=== Probando aircraft.py ===")
    aircrafts = LoadArrivals("arrivals.txt")
    print(f"Vuelos cargados: {len(aircrafts)}")

    if aircrafts:
        for aircraft in aircrafts[:3]:  # Mostrar primeros 3
            print(
                f"ID: {aircraft.id}, Origen: {aircraft.origin}, Hora: {aircraft.landing_time}, Aerolínea: {aircraft.airline}, Schengen: {aircraft.schengen}")

        # PlotArrivals(aircrafts)
        # PlotAirlines(aircrafts)
        # PlotFlightsType(aircrafts)
        # SaveFlights(aircrafts, "saved_flights.txt")
        # MapFlights(aircrafts)
        long_distance = LongDistanceArrivals(aircrafts)
        print(f"Vuelos larga distancia: {len(long_distance)}")