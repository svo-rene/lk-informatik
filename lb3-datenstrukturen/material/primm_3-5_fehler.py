# PRIMM 3.5 – Fehler finden: suchen_rek findet manche Werte nicht.


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

    def suchen_rek(self, wert, knoten=None):
        if self.__wurzel is None:
            return False
        if knoten is None:
            knoten = self.__wurzel
        if wert == knoten.wert:
            return True
        if wert < knoten.wert:
            if knoten.links is None:
                return False
            self.suchen_rek(wert, knoten.links)
        else:
            if knoten.rechts is None:
                return False
            return self.suchen_rek(wert, knoten.rechts)


b = Suchbaum()
for w in [8, 3, 10, 1, 6, 14]:
    b.einfuegen(w)

print(b.suchen_rek(14))    # erwartet: True
print(b.suchen_rek(6))     # erwartet: True
print(b.suchen_rek(7))     # erwartet: False
