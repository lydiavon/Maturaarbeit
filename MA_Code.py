import tkinter as tk

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
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]
buttons = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]
spielerX = "X"
spielerO = "O"
aktiver_spieler = spielerX
blau = "#00487d"
rot = "#b30000"
grau = "#252526"
gruen = "#008f00"
weiss = "#C6C6C6"
game_over = False
modus = "gegen Computer"
gewinn_counter = {spielerX: 0, spielerO: 0}

"""GUI Setup"""
window = tk.Tk()
window.title("Tic Tac Toe")
window.resizable(False, False)
window.config(background=grau)

frame = tk.Frame(window, background=grau)
frame.grid(row=0, column=0, padx=10, pady=10)

"""Dropdown-Menü erstellen"""
modus_var = tk.StringVar(value="gegen Computer")
modus_menu = tk.OptionMenu(frame, modus_var, "gegen Computer", "gegen Spieler")
modus_menu.config(background=grau, foreground=weiss)
modus_menu.grid(row=0, column=0, pady=5, sticky="w")

label = tk.Label(frame, text=aktiver_spieler + " ist am Zug", font=("Consolas", 15), background=grau, foreground=weiss)
label.grid(row=0, column=1, sticky="we")

gewinn_label = tk.Label(frame, text="0:0", font=("Consolas", 15), background=grau, foreground=weiss)
gewinn_label.grid(row=0, column=2, padx=5, sticky="e")

def update_gewinn_label():
    """Aktualisiert den Counter nach Änderung des Modus oder Spielende."""
    gewinn_label.config(text=f"{gewinn_counter[spielerX]}:{gewinn_counter[spielerO]}")

def neues_spiel():
    """Wird beim Drücken des Neues Spiel Knopfes oder der Modus geändert wird ausgeführt.
    Setzt alle nötigen Variablen auf den Anfang eines neuen Spiels"""
    global aktiver_spieler, game_over, spielfeld, modus, gewinn_counter
    aktiver_spieler = spielerX
    game_over = False
    label.config(text=aktiver_spieler + " ist am Zug", foreground=weiss)
    spielfeld = [["", "", ""], ["", "", ""], ["", "", ""]]
    for row in range(3):
        for column in range(3):
            button = buttons[row][column]
            button.config(text="", foreground=blau)
    if modus != modus_var.get():
        gewinn_counter = {spielerX: 0, spielerO: 0}
    modus = modus_var.get()
    update_gewinn_label()

"""Erstellung des Spielfelds(buttons)"""
for row in range(3):
    for column in range(3):
        button = tk.Button(frame, text="", font=("Consolas", 50, "bold"), background=grau, foreground=blau, width=4, height=1, command=lambda row=row, column=column: set_tile(row, column))
        button.grid(row=row + 1, column=column)
        buttons[row][column] = button

button = tk.Button(frame, text="neues Spiel", font=("Consolas", 15), background=grau, foreground=weiss, command=neues_spiel)
button.grid(row=4, column=0, columnspan=3, sticky="we")

def spielart(*args):
    """Startet neues Spiel wenn Modus geändert wird"""
    neues_spiel()
modus_var.trace("w", spielart)

def update_spielfeld(gespielter_zug):
    """Setzt Zug des Spielers"""
    global aktiver_spieler
    x_kord, y_kord = gespielter_zug
    spielfeld[y_kord][x_kord] = aktiver_spieler
    
def evaluation(spielfeld):
    """Schaut ob das Spiel beendet ist und ob Gewonnen oder Unendschieden"""
    for voraussetzungen in gewinn_voraussetzung:
        a = spielfeld[voraussetzungen[0][0]][voraussetzungen[0][1]]
        b = spielfeld[voraussetzungen[1][0]][voraussetzungen[1][1]]
        c = spielfeld[voraussetzungen[2][0]][voraussetzungen[2][1]]
        if a == b and b == c and a != "":
            return a, voraussetzungen  # Rückgabe des Gewinners und der gewinnenden Steine
    if all(spielfeld[row][column] != "" for row in range(3) for column in range(3)):
        return 0, []  # Unentschieden
    return None, []  # Spiel noch nicht zu Ende

def minimax(spielfeld, tiefe, max_spieler):
    """Rekursiver Aufruf des Minimax Algorithmus um Spielbaum zu erstellen und zu bewerten."""
    ergebnis, _ = evaluation(spielfeld)
    if ergebnis is not None:
        if ergebnis == spielerX:
            return 10 - tiefe # Positive Bewertung je früher der Gewinn
        elif ergebnis == spielerO:
            return tiefe - 10 # Negative Bewertung je früher der Verlust
        else:
            return 0 # Unendschieden
    if max_spieler: # für Spieler O (Computer)
        beste_bewertung = -1000
        for i in range(3):
            for j in range(3):
                if spielfeld[i][j] == "":
                    spielfeld[i][j] = spielerX
                    bewertung = minimax(spielfeld, tiefe + 1, False)
                    spielfeld[i][j] = ""
                    beste_bewertung = max(beste_bewertung, bewertung)
        return beste_bewertung
    else: # für Spieler X (Mensch)
        beste_bewertung = 1000
        for i in range(3):
            for j in range(3):
                if spielfeld[i][j] == "":
                    spielfeld[i][j] = spielerO
                    bewertung = minimax(spielfeld, tiefe + 1, True)
                    spielfeld[i][j] = ""
                    beste_bewertung = min(beste_bewertung, bewertung)
        return beste_bewertung

def minimax_zug():
    """Startet die Erstellung des Spielbaumes und ruft Minimax Funktion auf.
    Wählt den besten Zug aus und sezt diesen auf das Spielfeld."""
    global spielfeld
    beste_bewertung = 1000
    bester_zug = None
    for i in range(3):
        for j in range(3):
            if spielfeld[i][j] == "":
                spielfeld[i][j] = spielerO
                bewertung = minimax(spielfeld, 0, True)
                spielfeld[i][j] = ""
                if bewertung < beste_bewertung:
                    beste_bewertung = bewertung
                    bester_zug = (j, i)
    if bester_zug:
        x_kord, y_kord = bester_zug
        spielfeld[y_kord][x_kord] = spielerO
        button = buttons[y_kord][x_kord]
        button.config(text="O", foreground= rot)


def spiel_status():
    """Ändert Label und ändert die Farbe der gewinnenden Steine"""
    global game_over
    ergebnis, gewinnende_steine = evaluation(spielfeld)
    if ergebnis is not None:
        game_over = True
        if ergebnis == "X":
            label.config(text="X gewinnt", foreground=gruen)
            gewinn_counter[spielerX] += 1
        elif ergebnis == "O":
            label.config(text="O gewinnt", foreground=gruen)
            gewinn_counter[spielerO] += 1
        else:
            label.config(text="Unentschieden", foreground=weiss)
        update_gewinn_label()
        if gewinnende_steine:
            for stein in gewinnende_steine:
                x, y = stein
                buttons[x][y].config(foreground=gruen)
        return True # Spiel zu Ende
    return False # Spiel noch nicht zu Ende

def set_tile(row, column):
    """Überprüft ob das Spiel zu Ende ist, dass kein schon besetzter Button überschrieben wird,
    setzt den Spielzug, startet Minimax wenn Modus darauf ist, ändert den aktiven Spieler"""
    global aktiver_spieler
    if game_over:
        return
    button = buttons[row][column]
    if button["text"] != "":
        return
    button["text"] = aktiver_spieler
    button.config(foreground=blau if aktiver_spieler == spielerX else rot)
    update_spielfeld((column, row))
    if spiel_status():
        return
    if modus_var.get() == "gegen Computer" and aktiver_spieler == spielerX:
        aktiver_spieler = spielerO
        minimax_zug()
        if spiel_status():
            return
        aktiver_spieler = spielerX
    else:
        aktiver_spieler = spielerO if aktiver_spieler == spielerX else spielerX
    label["text"] = aktiver_spieler + " ist am Zug"

window.mainloop() # Startet GUI