from random import randrange
from minimax import minimax, evaluation

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
    """Druckt Spielfeld in das Terminal"""
    for row in spielfeld:
        print(row)

def eingabe_pruefen(eingegebener_zug):
    """Prüft ob die Eingabe des Spielers korrekt ist"""
    global spielfeld
    try:
        y_kord, x_kord = int(eingegebener_zug[0])-1, int(eingegebener_zug[1])-1
        if 0 <= x_kord < 3 and 0 <= y_kord < 3:
            if spielfeld[y_kord][x_kord] == 0:
                return True, (x_kord, y_kord)
            else:
                print("Ungültiger Spielzug: Feld bereits belegt")
                return False, None
        else:
            print("Ungültiger Spielzug: Koordinaten außerhalb des Spielfelds")
            return False, None
    except ValueError:
        print("Ungültige Eingabe")
        return False, None

def eingabe():
    '''
    Koordinaten des Spielfelds:
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
    """Setzt die Spielzüge in das Spielfeld"""
    global spielfeld
    x_kord, y_kord = gespielter_zug
    spielfeld[y_kord][x_kord] = aktiver_spieler
    return -aktiver_spieler          

def minimax_zug():
    """Erstellt die erste Ebene des Spielbaums und ruft Minimax Funktion auf.
    Wählt den besten Zug aus und sezt diesen auf das Spielfeld."""
    global spielfeld
    beste_bewertung = -1000
    bester_zug = None
    for i in range(3):
        for j in range(3):
            if spielfeld[i][j] == 0:
                spielfeld[i][j] = 1
                bewertung = minimax(spielfeld, 0, False)
                spielfeld[i][j] = 0
                if bewertung > beste_bewertung:
                    beste_bewertung = bewertung
                    bester_zug = (j, i)
    if bester_zug:
        x_kord, y_kord = bester_zug
        spielfeld[y_kord][x_kord] = 1
        
def spiel_status():
    """Druckt den Gewinner und das beendete Spiel in das Terminal"""
    ergebnis = evaluation(spielfeld)
    if ergebnis is not None:
        if ergebnis == 1:
            print("Du hast verloren")
        elif ergebnis == -1:
            print("Du hast gewonnen")
        else:
            print("Unentschieden")
        spielfeld_anzeigen()
        return True
    return False

def game_loop():
    """
    Solange das Spiel nicht beendet ist, 
    fürt es den Zug aus, 
    aktualisiert das Spielfeld 
    und ändert den aktiven Spieler.
    """
    runde_ende = False
    aktiver_spieler = -1 # Spieler X beginnt
    while runde_ende == False:
        spielfeld_anzeigen()
        if aktiver_spieler == -1: # -1 = Spieler X 
            gespielter_zug = eingabe()
            aktiver_spieler = update_spielfeld(gespielter_zug, aktiver_spieler)
        else:
            gespielter_zug = minimax_zug()
            aktiver_spieler = aktiver_spieler *-1       
    
        runde_ende = spiel_status()

game_loop() # Startet das Spiel