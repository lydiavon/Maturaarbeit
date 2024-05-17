from random import randrange
# -1:X, 0: leer, 1:O
spielfeld = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

gewinn_voraussetzung = [
    [(0,0), (0,1), (0,2)],
    [(1,0), (1,1), (1,2)],
    [(2,0), (2,1), (2,2)],
    [(0,0), (1,0), (2,0)],
    [(0,1), (1,1), (2,1)],
    [(0,2), (1,2), (2,2)],
    [(0,0), (1,1), (2,2)],
    [(0,2), (1,1), (2,0)]
]


def spielfeld_anzeigen():
    for row in spielfeld:
        print(row)

def eingabe_pruefen(eingegebener_zug):
    global spielfeld
    try:
        y_kord, x_kord = int(eingegebener_zug[0])-1, int(eingegebener_zug[1])-1
        if 0 <= x_kord < 3 and 0 <= y_kord < 3:
            if spielfeld[y_kord][x_kord] == 0:
                return True, (x_kord, y_kord)
            else:
                print("Ungültiger Spielzug: Feld bereits belegt") #nume bi -1 mache u nid bi pc
                return False, None
        else:
            print("Ungültiger Spielzug: Koordinaten außerhalb des Spielfelds")
            return False, None
    except ValueError:
        print("Ungültige Eingabe")
        return False, None

def eingabe():
    '''
      1 2 3
    1
    2
    3
    '''
    while True:
        eingegebener_zug = input("Geben Sie einen Zug ein: ")
        zug_erlaubt, zug_koordinaten = eingabe_pruefen(eingegebener_zug)
        if zug_erlaubt:
            return zug_koordinaten

def update_spielfeld(gespielter_zug, aktiver_spieler):
    global spielfeld
    x_kord, y_kord = gespielter_zug
    spielfeld[y_kord][x_kord] = aktiver_spieler
    return -aktiver_spieler    

def compter_zug():
    while True:
        eingegebener_zug = randrange(1, 3), randrange(1, 3)
        zug_erlaubt, zug_koordinaten = eingabe_pruefen(eingegebener_zug)
        if zug_erlaubt:
            return zug_koordinaten

def spiel_status():
    runde_gewonnen = False
    
    for i in range(8):
        voraussetzungen = gewinn_voraussetzung[i]
        a = spielfeld[voraussetzungen[0][0]][voraussetzungen[0][1]]
        b = spielfeld[voraussetzungen[1][0]][voraussetzungen[1][1]]
        c = spielfeld[voraussetzungen[2][0]][voraussetzungen[2][1]]
        if a == 0 or b == 0 or c == 0:
            continue
        if a == b and b == c:
            runde_gewonnen = True
            break
    if runde_gewonnen == False:
        return False    
    if runde_gewonnen == True:
        print("Gewonnen")
        return True   #game_loop stoppen
    
    if all(item != 0 for row in spielfeld for item in row):
        print("Unentschieden")
        return True   #game_loop stoppen

def game_loop():
    #Zug ausführen
    #Spielfeld updaten
    #nächster Zug
    runde_ende = False
    aktiver_spieler = -1
    while runde_ende == False:
        spielfeld_anzeigen()
        if aktiver_spieler == -1:
            gespielter_zug = eingabe()
        else:
            gespielter_zug = compter_zug()
        aktiver_spieler = update_spielfeld(gespielter_zug, aktiver_spieler)
        runde_ende = spiel_status()
    #ausgang_anzeigen()

game_loop()