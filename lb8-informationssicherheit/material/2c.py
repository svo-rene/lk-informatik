def verschiebe(buchstabe, abstand):
    # Konvertiere den übergebenen Buchstaben in Kleinbuchstaben
    buchstabe = buchstabe.lower()
    start = ord('a')
    end = ord('z')

    # Konvertiere den Buchstaben in seinen ASCII-Wert
    buchstabe_ascii = ord(buchstabe)
    
    # Verschiebe den ASCII-Wert um den angegebenen Abstand
    neuer_ascii = (buchstabe_ascii - start + abstand) % 26 + start
    
    # Konvertiere den verschobenen ASCII-Wert zurück in einen Buchstaben
    return chr(neuer_ascii)

def verschluesseln(satz, abstand):
    # Initialisiere eine leere Zeichenkette für den verschlüsselten Satz
    verschluesselter_satz = ""
    
    # Iteriere über jeden Buchstaben im Satz
    for buchstabe in satz:
        # Verschiebe nur Buchstaben und lasse andere Zeichen unverändert
        if buchstabe.isalpha():
            verschluesselter_satz += verschiebe(buchstabe, abstand)
        else:
            verschluesselter_satz += buchstabe
    
    return verschluesselter_satz
def entschluesseln(satz,abstand):
    # Entschlüsseln bedeutet, den negativen Abstand zu verwenden
    return verschluesseln(satz, -abstand)

# Beispiel
satz = "Hallo, wie geht es dir?"
abstand = 3
crypt=(verschluesseln(satz, abstand))
print(entschluesseln(crypt, abstand))