# PRIMM 3.4 – Fehler finden: anzahl_blaetter zählt falsch.
# Der Baum ist derselbe wie in primm_3-4_raetsel.py, er hat 3 Blätter (D, E, F).


class Knoten:
    def __init__(self, wert):
        self.wert = wert
        self.kinder = []

    def __repr__(self):                  # damit der Debugger den Knoten lesbar anzeigt
        return "Knoten(" + repr(self.wert) + ")"

    def kind_hinzufuegen(self, knoten):
        self.kinder.append(knoten)


def anzahl_blaetter(knoten):
    anzahl = 0
    for kind in knoten.kinder:
        anzahl = anzahl_blaetter(kind)
    if knoten.kinder == []:
        return 1
    return anzahl


a = Knoten("A")
b = Knoten("B")
c = Knoten("C")
a.kind_hinzufuegen(b)
a.kind_hinzufuegen(c)
b.kind_hinzufuegen(Knoten("D"))
b.kind_hinzufuegen(Knoten("E"))
c.kind_hinzufuegen(Knoten("F"))

print(anzahl_blaetter(a))      # erwartet: 3