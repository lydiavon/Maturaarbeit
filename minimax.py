import copy

gewinn_voraussetzung = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)]
]

spielfeld = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

def evaluation(spielfeld):
    for voraussetzungen in gewinn_voraussetzung:
        a = spielfeld[voraussetzungen[0][0]][voraussetzungen[0][1]]
        b = spielfeld[voraussetzungen[1][0]][voraussetzungen[1][1]]
        c = spielfeld[voraussetzungen[2][0]][voraussetzungen[2][1]]
        if a == b and b == c:
            if a == 1:
                return 1  # KI gewinnt
            elif a == -1:
                return -1  # Mensch gewinnt
    
    if all(item != 0 for row in spielfeld for item in row):
        return 0  # Unentschieden
    
    return None  # Spiel noch nicht zu Ende

def spiel_beendet(spielfeld):
    ergebnis = evaluation(spielfeld)
    if ergebnis is not False:
        return True
    if all(item != 0 for row in spielfeld for item in row):
        return True
    return False

def minimax(spielfeld, tiefe, max_spieler):
    ergebnis = evaluation(spielfeld)
    if ergebnis is not None:
        if ergebnis == 1:
            return 10 - tiefe  # Positive Bewertung je früher der Gewinn
        elif ergebnis == -1:
            return tiefe - 10  # Negative Bewertung je früher der Verlust
        else:
            return 0  # Unentschieden
    
    if max_spieler:  # KI
        beste_bewertung = -1000
        for child in kinder_von_spielfeld(spielfeld, max_spieler):
            beste_bewertung = max(beste_bewertung, minimax(child, tiefe + 1, False))
        return beste_bewertung
    else:  # Mensch
        beste_bewertung = 1000
        for child in kinder_von_spielfeld(spielfeld, max_spieler):
            beste_bewertung = min(beste_bewertung, minimax(child, tiefe + 1, True))
        return beste_bewertung


def kinder_von_spielfeld(spielfeld, max_spieler):
    spielfelder_liste = []
    
    for i in range(3):
        for j in range(3):
            if spielfeld[i][j] == 0:
                neues_spielfeld = [row[:] for row in spielfeld]
                neues_spielfeld[i][j] = 1 if max_spieler else -1
                spielfelder_liste.append(neues_spielfeld) 
    
    return spielfelder_liste
