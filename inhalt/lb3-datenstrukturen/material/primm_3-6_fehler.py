# PRIMM 3.6 – Fehler finden: level_order bricht ab.

from queue_knoten import Queue   # Schlange mit Knoten aus Seite 3.2 (Datei in denselben Ordner legen)

class Knoten:
    def __init__(self, wert, links=None, rechts=None):
        self.wert = wert
        self.links = links
        self.rechts = rechts

    def __repr__(self):                  # damit der Debugger den Knoten lesbar anzeigt
        return "Knoten(" + repr(self.wert) + ")"


baum = Knoten(10, Knoten(5, Knoten(3), Knoten(7)), Knoten(15, None, Knoten(20)))

def level_order(wurzel):
    ergebnis = []
    schlange = Queue()
    schlange.enqueue(wurzel)
    while not schlange.is_empty():
        k = schlange.dequeue()
        ergebnis.append(k.wert)
        schlange.enqueue(k.links)
        schlange.enqueue(k.rechts)
    return ergebnis


print(level_order(baum))    # erwartet: [10, 5, 15, 3, 7, 20]