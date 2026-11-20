from p5 import *

class Spieler:
    #Attribute der Klasse festlegen
    def __init__(self):
        self.breite = 40
        self.hoehe = 20
        self.x = width / 2
        self.y = height - 50
        self.geschwindigkeit = 5

    #Rechteck für den Spieler erzeugen
    def anzeigen(self):
        rect_mode(CENTER)
        fill(255) #Farbe festlegen
        rect(self.x, self.y, 40, 20) #Spielerfigur als Rechteck festlegen

    def bewegen(self):
        if key_is_pressed and key == 'a':
            self.x = self.x - self.geschwindigkeit #mit Geschwindigkeit nach links bewegen
        if key_is_pressed and key == 'd':
            self.x = self.x + self.geschwindigkeit #mit Geschwindigkeit nach rechts bewegen
        #x-Wert einschränken, sodass Spieler nicht aus dem Spielfeld rauskommt
        self.x = constrain(self.x, self.breite / 2, width - self.breite / 2)

    def schießen(self):
        if key_is_pressed and key == ' ': #mit Leertaste schießen
            return Geschoss(self.x, self.y)

class Geschoss:
    #Attribute der Klasse festlegen
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.geschwindigkeit = 5

    #Rechteck für das Geschoss erzeugen
    def anzeigen(self):
        fill(255, 0, 0)
        rect(self.x, self.y, 3, 10)

    #Geschosse bewegen sich nur nach oben
    def bewegen(self):
        self.y = self.y - self.geschwindigkeit

class Alien:
    #Attribute der Klasse festlegen
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.breite = 40
        self.hoehe = 20
        self.geschwindigkeit = 1

    #Alien als Rechteck anzeigen
    def anzeigen(self):
        fill(0, 255, 0)
        rect(self.x, self.y, self.breite, self.hoehe)

    #Bewegung der Aliens festlegen
    def bewegen(self):
        self.x = self.x + self.geschwindigkeit
        if self.x > width - self.breite / 2 or self.x < self.breite / 2:
            self.geschwindigkeit = -self.geschwindigkeit
            self.y = self.y + self.hoehe

class Spiel:
    #Spieler und Aliens erzeugen
    def __init__(self):
        self.spieler = Spieler()
        self.geschosse = []
        self.aliens = []
        for i in range(4):
            for j in range(6):
                self.aliens.append(Alien(60 + j * 80, 50 + i * 40))

    #neues Geschoss am Spieler erzeugen
    def geschoss_hinzufuegen(self):
        geschoss = self.spieler.schießen()
        if geschoss:
            self.geschosse.append(geschoss)

    #kontrollieren ob ein Alien getroffen wurde
    def kollisionen_checken(self):
        for geschoss in self.geschosse:
            for alien in self.aliens:
                if (geschoss.x > alien.x - alien.breite / 2 and
                    geschoss.x < alien.x + alien.breite / 2 and
                    geschoss.y > alien.y - alien.hoehe / 2 and
                    geschoss.y < alien.y + alien.hoehe / 2):
                    self.geschosse.remove(geschoss)
                    self.aliens.remove(alien)

    #Geschoss nach oben weiterbewegen, Geschosse außerhalb des Spiels entfernen
    def aktualisieren_geschosse(self):
        for geschoss in self.geschosse:
            geschoss.bewegen()
            if geschoss.y < 0:
                self.geschosse.remove(geschoss)

    #Spieler hat gewonnen, wenn alle Aliens getroffen wurden
    def hat_gewonnen(self):
        return len(self.aliens) == 0

    #Spieler hat verloren, wenn Alien den Spieler erreicht hat
    def hat_verloren(self):
        for alien in self.aliens:
            if alien.y + alien.hoehe >= self.spieler.y:
                return True
        return False

#ein neues Spiel erstellen
spiel = Spiel()

#Größe des Spielfelds festlegen
def setup():
    size(600, 600)

#Befehle die dauerhaft ausgeführt werden
def draw():
    background(0)
    spiel.spieler.anzeigen()
    spiel.spieler.bewegen()
    spiel.geschoss_hinzufuegen()

    #alle Geschosse anzeigen
    for geschoss in spiel.geschosse:
        geschoss.anzeigen()

    #Aliens weiterbewegen
    for alien in spiel.aliens:
        alien.anzeigen()
        alien.bewegen()

    #checken ob es kollisionen gibt und geschosse akutalisieren
    spiel.kollisionen_checken()
    spiel.aktualisieren_geschosse()

    #checken ob Spieler gewonnen der verloren hat
    if spiel.hat_gewonnen():
        fill(0, 255, 0)
        text("Gewonnen!", width/2 - 50, height/2)
        no_loop()

    if spiel.hat_verloren():
        fill(255, 0, 0)
        text("Verloren!", width/2 - 50, height/2)
        no_loop()

run()
