# PRIMM 3.4 – Was macht raetsel?
# Erst auf Papier vorhersagen, dann ausführen (F5), dann mit dem Debugger untersuchen (Strg+F5).


class Knoten:
    def __init__(self, wert):
        self.wert = wert
        self.kinder = []

    def __repr__(self):                  # damit der Debugger den Knoten lesbar anzeigt
        return "Knoten(" + repr(self.wert) + ")"

    def kind_hinzufuegen(self, knoten):
        self.kinder.append(knoten)


def raetsel(knoten):
    if knoten.kinder == []:
        return knoten.wert
    ergebnis = ""
    for kind in knoten.kinder:
        ergebnis = ergebnis + raetsel(kind)
    return ergebnis


a = Knoten("A")
b = Knoten("B")
c = Knoten("C")
a.kind_hinzufuegen(b)
a.kind_hinzufuegen(c)
b.kind_hinzufuegen(Knoten("D"))
b.kind_hinzufuegen(Knoten("E"))
c.kind_hinzufuegen(Knoten("F"))

print(raetsel(a))