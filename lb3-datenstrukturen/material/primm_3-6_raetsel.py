# PRIMM 3.6 – Was macht raetsel?
# Erst auf Papier vorhersagen, dann ausführen (F5), dann mit dem Debugger untersuchen (Strg+F5).


class Knoten:
    def __init__(self, wert, links=None, rechts=None):
        self.wert = wert
        self.links = links
        self.rechts = rechts

    def __repr__(self):                  # damit der Debugger den Knoten lesbar anzeigt
        return "Knoten(" + repr(self.wert) + ")"


baum = Knoten(10, Knoten(5, Knoten(3), Knoten(7)), Knoten(15, None, Knoten(20)))

def raetsel(k, tiefe):
    if k is None:
        return
    raetsel(k.links, tiefe + 1)
    print(k.wert, "auf Tiefe", tiefe)
    raetsel(k.rechts, tiefe + 1)


raetsel(baum, 0)
