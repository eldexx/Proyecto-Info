from airport import *



# 1 Prueba de carga 
print("\n--- Paso 1: Cargar aeropuertos ---")
lista_aeropuertos = LoadAirports("Airports.txt")
cantidad = len(lista_aeropuertos)
print("Se han leído " + str(cantidad) + " aeropuertos.")

if cantidad > 0:
    print("Primer aeropuerto: ")
    PrintAirport(lista_aeropuertos[0])
else:
    print("ERROR: No se han cargado aeropuertos. Revisa el nombre Airports.txt")

# 2 Prueba de añadir uno nuevo
print("\n--- Paso 2: Añadir aeropuerto manual ---")
nuevo = Airport()
nuevo.code = "TEST"
nuevo.latitude = 40.0
nuevo.longitude = 2.0
SetSchengen(nuevo) 

res = AddAirport(lista_aeropuertos, nuevo)
if res == 0:
    print("Aeropuerto TEST añadido correctamente.")
else:
    print("Error al añadir TEST (quizás ya existía).")

# 3 Prueba de buscar y verificar
print("\n--- Paso 3: Verificar que está en la lista ---")
esta_dentro = False
for i in range(len(lista_aeropuertos)):
    if lista_aeropuertos[i].code == "TEST":
        esta_dentro = True
        print("Encontrado: ", end="")
        PrintAirport(lista_aeropuertos[i])

if esta_dentro == False:
    print("ERROR: El aeropuerto TEST no aparece en la lista.")

# 4 Prueba de guardar Schengen
print("\n--- Paso 4: Guardar solo Schengen ---")
res_save = SaveSchengenAirports(lista_aeropuertos, "test_schengen_output.txt")
if res_save == 0:
    print("Archivo 'test_schengen_output.txt' creado con éxito.")
else:
    print("Error al guardar.")

# 5 Prueba de eliminar
print("\n--- Paso 5: Eliminar aeropuerto TEST ---")
res_del = RemoveAirport(lista_aeropuertos, "TEST")
if res_del == 0:
    print("Aeropuerto eliminado correctamente.")
else:
    print("Error al eliminar.")

