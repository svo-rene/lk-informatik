# Aufgabe 3.6.10: Der Morsebaum
#
# Im Morsecode besteht jedes Zeichen aus Punkten und Strichen. Im Morsebaum führt ein Punkt
# nach links und ein Strich nach rechts. Der Code eines Zeichens ist also der Weg von der
# Wurzel bis zu seinem Knoten. Der Baum wird unten schon aufgebaut.
#
# Teil 1: zeichen_zu(code)        Test: morse.zeichen_zu("...")  -> S
# Teil 2: entschluesseln(nachricht)   Was steht in GEHEIM?
# Teil 3: ebenen() mit einer Schlange. Warum stehen E und T ganz oben?
# Teil 4: Wie viele Zeichen gibt es mit höchstens vier Signalen? Prüfe mit anzahl().
#
# Für ebenen() reicht eine Liste als Schlange: append stellt hinten an, pop(0) nimmt vorn heraus.


class MorseKnoten:
    def __init__(self, zeichen):
        self.zeichen = zeichen
        self.links = None      # Punkt  .
        self.rechts = None     # Strich -


class Morsebaum:
    def __init__(self):
        self.wurzel = MorseKnoten("Start")

    def einfuegen(self, zeichen, code):
        """Vorgegeben: läuft den Code ab (. = links, - = rechts) und legt das Zeichen ab."""
        knoten = self.wurzel
        for signal in code:
            if signal == ".":
                if knoten.links is None:
                    knoten.links = MorseKnoten("?")
                knoten = knoten.links
            else:
                if knoten.rechts is None:
                    knoten.rechts = MorseKnoten("?")
                knoten = knoten.rechts
        knoten.zeichen = zeichen

    # ---------------------------------------------------------------
    # a) Ein Zeichen entschlüsseln
    # ---------------------------------------------------------------
    def zeichen_zu(self, code):
        """Liefert das Zeichen zum Code, z. B. zeichen_zu("...") -> "S".
        Gibt es den Weg nicht, wird "?" geliefert."""
        pass  # TODO

    # ---------------------------------------------------------------
    # b) Eine ganze Nachricht entschlüsseln
    # ---------------------------------------------------------------
    def entschluesseln(self, nachricht):
        """Zeichen sind durch ein Leerzeichen getrennt, Wörter durch " / ".
        Tipp: nachricht.split(" ") liefert die einzelnen Codes."""
        pass  # TODO

    # ---------------------------------------------------------------
    # c) Ebene für Ebene ausgeben (Breitensuche)
    # ---------------------------------------------------------------
    def ebenen(self):
        """Gibt alle Zeichen Ebene für Ebene aus, ohne den Startknoten."""
        pass  # TODO



CODES = [["E", "."], ["T", "-"],
         ["I", ".."], ["A", ".-"], ["N", "-."], ["M", "--"],
         ["S", "..."], ["U", "..-"], ["R", ".-."], ["W", ".--"],
         ["D", "-.."], ["K", "-.-"], ["G", "--."], ["O", "---"],
         ["H", "...."], ["V", "...-"], ["F", "..-."], ["Ü", "..--"],
         ["L", ".-.."], ["Ä", ".-.-"], ["P", ".--."], ["J", ".---"],
         ["B", "-..."], ["X", "-..-"], ["C", "-.-."], ["Y", "-.--"],
         ["Z", "--.."], ["Q", "--.-"], ["Ö", "---."], ["CH", "----"]]

morse = Morsebaum()
for eintrag in CODES:
    morse.einfuegen(eintrag[0], eintrag[1])

GEHEIM = "-.. . .-. / .-.. -.- / .. ... - / -.-. --- --- .-.."

print(morse.zeichen_zu("..."))       # S
print(morse.zeichen_zu("-.-"))       # K
print(morse.entschluesseln(GEHEIM))
morse.ebenen()
