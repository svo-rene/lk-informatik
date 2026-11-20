def datensaetzeAusText(text):

    # erzeugt aus einem String mit Zeilenumbruchzeichen
    # eine Liste von Datensaetzen; jeder Datensatz ist selbst eine Liste
    # [name, vorname, strasse, plz, ort]

    zeilen = text.split('\n')
    liste = []
    for zeile in zeilen:
        teile = zeile.split(',')
        name = teile[0]
        vorname = teile[1]
        strasse = teile[2]
        plz = teile[3]
        ort = teile[4]
        datensatz = [name, vorname, strasse, plz, ort]
        liste.append(datensatz)
    return liste


def textAusDatensaetzen(liste):

    # erzeugt aus einer Liste von Datensaetzen einen String:
    # die Werte eines Datensatzes werden mit Komma getrennt,
    # die Datensaetze mit dem Zeilenumbruchzeichen \n

    text = ''
    for i in range(len(liste)):
        d = liste[i]
        zeile = d[0] + ',' + d[1] + ',' + d[2] + ',' + d[3] + ',' + d[4]
        if i == 0:
            text = zeile
        else:
            text = text + '\n' + zeile
    return text


def textAusDatei(dateiname):

    # laedt einen Text aus einer Datei und gibt ihn als
    # Zeichenkette zurueck
    # beachte: setzt die Codierung iso-8859-1 voraus

    datei = open(dateiname, 'r', encoding='iso-8859-1')
    text = datei.read()
    datei.close()
    return text


def textInDateiSpeichern(dateiname, text):

    # speichert eine Zeichenkette in einer Datei
    # beachte: benutzt die Codierung iso-8859-1

    datei = open(dateiname, 'w', encoding='iso-8859-1')
    datei.write(text)
    datei.close()
