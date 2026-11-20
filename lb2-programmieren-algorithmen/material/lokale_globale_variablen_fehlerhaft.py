# Tauschen von zwei Zahlen - fehlerhafte Version
# Aufgabe: Finde heraus, warum das Programm abbricht, und korrigiere es.

# Unterprogramme
def zahlen_eingeben():
    zahl1 = int(input("Zahl 1: "))
    zahl2 = int(input("Zahl 2: "))

def zahlen_tauschen():
    hilf = zahl1
    zahl1 = zahl2
    zahl2 = hilf

def zahlen_ausgeben():
    print("Zahl 1: ", zahl1)
    print("Zahl 2: ", zahl2)

# Hauptprogramm: Funktionsaufrufe
zahlen_eingeben()
zahlen_tauschen()
zahlen_ausgeben()
