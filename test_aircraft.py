from aircraft import *



# 1 Cargar Llegadas 
print("\n--- Paso 1: Cargar Llegadas ---")
llegadas = LoadArrivals("Arrivals.txt")
print("Llegadas cargadas: " + str(len(llegadas)))
if len(llegadas) > 0:
    print("Ejemplo llegada: " + str(llegadas[0]))
else:
    print("Error: No se cargaron llegadas. Revisa Arrivals.txt")

# 2 Cargar Salidas 
print("\n--- Paso 2: Cargar Salidas ---")
salidas = LoadDepartures("Departures.txt")
print("Salidas cargadas: " + str(len(salidas)))
if len(salidas) > 0:
    print("Ejemplo salida: " + str(salidas[0]))
else:
    print("Error: No se cargaron salidas. Revisa Departures.txt")

# 3 Fusionar
print("\n--- Paso 3: Fusionar Movimientos ---")
if len(llegadas) > 0 and len(salidas) > 0:
    vuelos_completos = MergeMovements(llegadas, salidas)
    print("Total de movimientos unificados: " + str(len(vuelos_completos)))
    
    encontrado_completo = False
    for i in range(len(vuelos_completos)):
        a = vuelos_completos[i]
        if a.landing_time != "" and a.departure_time != "":
            print("Vuelo completo encontrado (Llega y Sale):")
            print(a)
            encontrado_completo = True
            break
            
    if encontrado_completo == False:
        print("Aviso: No se encontró ningún vuelo que coincida llegada y salida en la muestra.")
else:
    print("No se puede probar Merge sin archivos válidos.")
    vuelos_completos = []

# 4 Detectar aviones nocturnos
print("\n--- Paso 4: Aviones Nocturnos (Solo salida) ---")
nocturnos = NightAircraft(vuelos_completos)
print("Aviones que durmieron en aeropuerto: " + str(len(nocturnos)))
if len(nocturnos) > 0:
    print("Ejemplo nocturno: " + str(nocturnos[0]))

