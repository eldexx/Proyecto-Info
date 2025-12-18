from LEBL import *

# Clase auxiliar simple para probar sin depender de aircraft.py completo
class AircraftTest:
    def __init__(self, id, airline, schengen, arr, dep):
        self.id = id
        self.airline = airline
        self.schengen = schengen
        self.landing_time = arr
        self.departure_time = dep



# 1 Cargar estructura 
print("\n--- Paso 1: Cargar Estructura LEBL ---")
bcn = LoadAirportStructure("Terminals.txt")

if bcn == None:
    print("ERROR FATAL: No se cargó Terminals.txt. Asegúrate de que el archivo existe.")
else:
    print("Aeropuerto creado: LEBL")
    print("Número de terminales: " + str(len(bcn.terminales)))
    
    t1 = bcn.terminales[0]
    print("Terminal " + t1.nombre + " tiene " + str(len(t1.airlines)) + " aerolineas cargadas.")

    # 2 Probar ocupación inicial
    print("\n--- Paso 2: Ocupación Inicial ---")
    datos = GateOccupancy(bcn)
    ocupadas = 0
    for i in range(len(datos)):
        if datos[i]["ocupado"] == True:
            ocupadas = ocupadas + 1
    print("Puertas totales: " + str(len(datos)))
    print("Puertas ocupadas al inicio: " + str(ocupadas))

    # 3 Asignación simple
    print("\n--- Paso 3: Asignar un vuelo de prueba ---")
    
    vuelo_test = AircraftTest("TEST001", "VLG", True, "10:00", "11:00")
    
    res = AssignGate(bcn, vuelo_test)
    if res == 0:
        print("Asignación EXITOSA para TEST001 (Vueling).")
    elif res == -1:
        print("FALLO: Terminal no encontrada para VLG.")
    elif res == -2:
        print("FALLO: No hay puertas libres.")

    # Verificamos que ahora hay 1 ocupada
    datos_post = GateOccupancy(bcn)
    for i in range(len(datos_post)):
        if datos_post[i]["id"] == "TEST001":
            print("Verificación: El avión está en la puerta " + datos_post[i]["gate"])
            break

    # 4 Liberar puerta
    print("\n--- Paso 4: Liberar puerta ---")
    res_free = FreeGate(bcn, "TEST001")
    if res_free == 0:
        print("Puerta liberada correctamente.")
    else:
        print("Error al liberar puerta.")

    # 5 Asignación por hora 
    print("\n--- Paso 5: Simulación por hora ---")
    lista_vuelos = []
    # Dos vuelos que llegan en la franja de las 8 de la mañana
    v1 = AircraftTest("VUELO_A", "VLG", True, "08:05", "09:00") 
    v2 = AircraftTest("VUELO_B", "VLG", True, "08:50", "10:00")
    lista_vuelos.append(v1)
    lista_vuelos.append(v2)
    
    print("Ejecutando asignación para las 08:00...")
    resultado = AssignGatesAtTime(bcn, lista_vuelos, "08:00")
    print("Aviones asignados en esta hora: " + str(resultado[0]))
    print("Aviones sin puerta: " + str(resultado[1]))
    
    if resultado[0] == 2:
        print("PRUEBA EXITOSA: Ambos vuelos entraron en la franja de las 08:00.")
    else:
        print("AVISO: Revisa la lógica de horarios.")

