from airport import *

airport = Airport ()
airport.code = "LEBL"
airport.latitude = 41.297445
airport.longitude = 2.0832941
SetSchengen(airport)
PrintAirport(airport)

print("\n=== Cargando aeropuertos desde archivo ===")
airports = LoadAirports("airports.txt")

print("\n--- Aeropuertos cargados ---")
for a in airports:
    PrintAirport(a)

print("\n--- Guardando aeropuertos Schengen ---")
SaveSchengenAirports(airports, "schengen_airports.txt")

print("\n--- Añadiendo aeropuerto nuevo ---")
nuevo = Airport()
nuevo.code = "DAAG"
nuevo.latitude = 36.4138
nuevo.longitude = 3.1252
SetSchengen(nuevo)
AddAirport(airports, nuevo)

print("\n--- Eliminando aeropuerto CYUL ---")
RemoveAirport(airports, "CYUL")

print("\n--- Lista final de aeropuertos ---")
for a in airports:
    PrintAirport(a)

print("\n✅ Step 4 completado correctamente.")
