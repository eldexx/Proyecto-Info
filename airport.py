
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
