from airport import *

print("=== TEST 1: Crear aeropuerto individual ===")
airport = Airport()
airport.code = "LEBL"
airport.latitude = 41.297445
airport.longitude = 2.0832941
SetSchengen(airport)
PrintAirport(airport)

print("\n=== TEST 2: Cargar aeropuertos desde archivo ===")
airports = LoadAirports("airports.txt")

print("\n--- Aeropuertos cargados ---")
for a in airports:
    PrintAirport(a)

print("\n=== TEST 3: Guardar aeropuertos Schengen ===")
SaveSchengenAirports(airports, "schengen_airports.txt")

print("\n=== TEST 4: Añadir aeropuerto nuevo ===")
nuevo = Airport()
nuevo.code = "TEST"
nuevo.latitude = 40.4168
nuevo.longitude = -3.7038
SetSchengen(nuevo)
AddAirport(airports, nuevo)

print("\n=== TEST 5: Eliminar aeropuerto ===")
RemoveAirport(airports, "CYUL")

print("\n=== TEST 6: Lista final de aeropuertos ===")
for a in airports:
    PrintAirport(a)

print("\n✅ Todos los tests completados correctamente.")