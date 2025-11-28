class Gate:
    def __init__(self, nombre):
        self.nombre = nombre
        self.ocupado = False
        self.id_aeronave = None

    def asignar(self, id_aeronave):
        self.ocupado = True
        self.id_aeronave = id_aeronave

    def liberar(self):
        self.ocupado = False
        self.id_aeronave = None

class BoardingArea:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo  # "Schengen" o "non-Schengen"
        self.gates = []

    def agregar_gate(self, gate):
        self.gates.append(gate)

class Terminal:
    def __init__(self, nombre):
        self.nombre = nombre
        self.boarding_areas = []
        self.airlines = []

    def agregar_boarding_area(self, area):
        self.boarding_areas.append(area)

def LoadAirlines(terminal, tname):
    filename = f"{tname}Airlines.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # Asume que el código ICAO es la última columna separada por tabulador
            terminal.airlines = [line.split("\t")[-1].strip() for line in lines if line.strip()]
        return 0
    except FileNotFoundError:
        terminal.airlines = []
        return -1

class BarcelonaAP:
    def __init__(self, codigo_ICAO):
        self.codigo_ICAO = codigo_ICAO
        self.terminales = []

    def agregar_terminal(self, terminal):
        self.terminales.append(terminal)

def SetGates(area, initgate, endgate, prefix):
    """Crea los gates en la boarding area con nombre correspondiente."""
    if endgate < initgate:
        return -1
    area.gates = []
    for n in range(initgate, endgate + 1):
        nombre_gate = f"{prefix}{n}"
        area.gates.append(Gate(nombre_gate))
    return 0

def LoadAirportStructure(filename):
    """
    Lee la estructura del aeropuerto desde el archivo y crea el objeto BarcelonaAP.
    Formato esperado (ejemplo):
        T1
        BoardingArea1 Schengen A 1 10
        BoardingArea2 non-Schengen B 1 8
        ...
        T2
        BoardingArea3 Schengen C 1 5
        BoardingArea4 non-Schengen D 1 6
        ...
    """
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        return None

    bcn = BarcelonaAP("LEBL.txt")
    terminal = None

    for line in lines:
        parts = line.split()
        if len(parts) == 1 and parts[0].startswith("T"):  # Nuevo terminal
            if terminal:  # Si no es la primera, guarda la anterior
                bcn.agregar_terminal(terminal)
            terminal = Terminal(parts[0])
            LoadAirlines(terminal, parts[0])
        elif len(parts) == 5:
            nombre_area, tipo, prefijo, initgate, endgate = parts
            area = BoardingArea(nombre_area, tipo)
            SetGates(area, int(initgate), int(endgate), prefijo)
            terminal.agregar_boarding_area(area)
    if terminal:
        bcn.agregar_terminal(terminal)
    return bcn

def GateOccupancy(bcn):
    datos = []
    for terminal in bcn.terminales:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                datos.append({
                    "terminal": terminal.nombre,
                    "area": area.nombre,
                    "tipo": area.tipo,
                    "gate": gate.nombre,
                    "ocupado": gate.ocupado,
                    "id_aeronave": gate.id_aeronave
                })
    return datos

def IsAirlineInTerminal(terminal, name):
    return name in terminal.airlines if terminal.airlines else False

def SearchTerminal(bcn, name):
    for terminal in bcn.terminales:
        if IsAirlineInTerminal(terminal, name):
            return terminal
    return None

def AssignGate(bcn, aircraft):
    """
    aircraft debe tener los atributos .airline, .id y .schengen
    """
    terminal = SearchTerminal(bcn, aircraft.airline)
    if not terminal:
        return -1  # No hay terminal para esa aerolínea
    tipo = "Schengen" if aircraft.schengen else "non-Schengen"
    for area in terminal.boarding_areas:
        if area.tipo == tipo:
            for gate in area.gates:
                if not gate.ocupado:
                    gate.ocupado = True
                    gate.id_aeronave = aircraft.id
                    return 0  # Asignación exitosa
    return -2  # No hay gates libres de ese tipo

# Sección de prueba ("test section")
if __name__ == "__main__":
    # Suponiendo que existe LEBL.txt.txt y los archivos T1Airlines.txt, T2Airlines.txt, etc.
    bcn = LoadAirportStructure("LEBL.txt.txt")
    print("Puertas disponibles al inicio:\n")
    for d in GateOccupancy(bcn):
        print(d)

    # Ejemplo de clase avión para la prueba (ajusta atributos según tu Aircraft real)
    class Aircraft:
        def __init__(self, id, airline, schengen):
            self.id = id
            self.airline = airline
            self.schengen = schengen

    # Prueba asignando un avión a un gate
    avion1 = Aircraft("EC1234", "VLG", True)
    res = AssignGate(bcn, avion1)
    print("\nResultado de asignación de gate:", res)
    print("\nOcupación de gates tras la llegada de un avión:\n")
    for d in GateOccupancy(bcn):
        print(d)