# PRIMM 3.5 – Was macht raetsel?
# Erst auf Papier vorhersagen, dann ausführen (F5), dann mit dem Debugger untersuchen (Strg+F5).


class Knoten:
    def __init__(self, wert):
        self.wert = wert
        self.links = None
        self.rechts = None

    def __repr__(self):                  # damit der Debugger den Knoten lesbar anzeigt
        return "Knoten(" + repr(self.wert) + ")"


class Suchbaum:
    def __init__(self):
        self.__wurzel = None

    def einfuegen(self, wert, knoten=None):
        if self.__wurzel is None:          # leerer Baum
            self.__wurzel = Knoten(wert)
            return
        if knoten is None:                 # Aufruf von außen:
            knoten = self.__wurzel         # an der Wurzel starten
        if wert < knoten.wert:
            if knoten.links is None:
                knoten.links = Knoten(wert)
            else:
                self.einfuegen(wert, knoten.links)
        elif wert > knoten.wert:           # gleich: nichts tun
            if knoten.rechts is None:
                knoten.rechts = Knoten(wert)
            else:
                self.einfuegen(wert, knoten.rechts)

    def raetsel(self, grenze, knoten=None):
        if self.__wurzel is None:
            return 0
        if knoten is None:
            knoten = self.__wurzel
        anzahl = 0
        if knoten.links is not None:
            anzahl = anzahl + self.raetsel(grenze, knoten.links)
        if knoten.wert < grenze:
            anzahl = anzahl + 1
            if knoten.rechts is not None:
                anzahl = anzahl + self.raetsel(grenze, knoten.rechts)
        return anzahl


b = Suchbaum()
for w in [8, 3, 10, 1, 6, 14]:
    b.einfuegen(w)

print(b.raetsel(7))
