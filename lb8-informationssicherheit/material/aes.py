# Mini-AES-8 mit Zeichenketten
# ============================

# Hex-Zeichen-Liste
HEX = ["0", "1", "2", "3", "4", "5", "6", "7",
       "8", "9", "A", "B", "C", "D", "E", "F"]

# S-Box: Substitutionstabelle
SBOX = ["E", "4", "D", "1",
        "2", "F", "B", "8",
        "3", "A", "6", "C",
        "5", "9", "0", "7"]

# Tabelle: Zuordnung Hex-Zeichen -> 4-Bit-Binärstring
HEX_TO_BIN = {
    "0": "0000", "1": "0001", "2": "0010", "3": "0011",
    "4": "0100", "5": "0101", "6": "0110", "7": "0111",
    "8": "1000", "9": "1001", "A": "1010", "B": "1011",
    "C": "1100", "D": "1101", "E": "1110", "F": "1111"
}


BIN_TO_HEX = {
    "0000": "0", "0001": "1", "0010": "2", "0011": "3",
    "0100": "4", "0101": "5", "0110": "6", "0111": "7",
    "1000": "8", "1001": "9", "1010": "A", "1011": "B",
    "1100": "C", "1101": "D", "1110": "E", "1111": "F"
}


# ---------------------------------------------------
# Aufgabe 1: SubBytes
# ---------------------------------------------------
def sub_bytes_hex(byte_str):
    """
    Schritte:
    1. Zerlege byte_str in zwei Zeichen (oberes und unteres Nibble).
    2. Bestimme für jedes Zeichen den Index in der Liste HEX.
    3. Nutze diesen Index, um in der SBOX das neue Zeichen zu holen.
    4. Setze beide neuen Zeichen zu einem 2-stelligen String zusammen.
    """
    
# ---------------------------------------------------
# Aufgabe 2: Permutation
# ---------------------------------------------------
def permute_hex(byte_str):
    """
    Vertausche die beiden Nibbles eines Bytes.
    """

    
# ---------------------------------------------------
# Hilfsfunktion: XOR für ein Nibble
# ---------------------------------------------------
def xor_hex_digit(a, b):
    """
    Schritte:
    1. Hole dir die 4-Bit-Binärstrings von a und b
       mit HEX_TO_BIN[a] und HEX_TO_BIN[b].
    2. Gehe über alle 4 Bit:
       - wenn die Bits gleich sind, hänge "0" an das Ergebnis
       - wenn die Bits verschieden sind, hänge "1" an das Ergebnis
    3. Wandle den 4-Bit-Ergebnisstring mit BIN_TO_HEX zurück in ein Hex-Zeichen.
    """
    bin_a = HEX_TO_BIN[a]
    bin_b = HEX_TO_BIN[b]
    result_bits = ""

    for i in range(4):
        if bin_a[i] == bin_b[i]:
            result_bits += "0"
        else:
            result_bits += "1"

    return BIN_TO_HEX[result_bits]


# ---------------------------------------------------
# Aufgabe 3: AddRoundKey
# ---------------------------------------------------
def add_round_key_hex(byte_str, key_str):
    """
    Idee:
    - oberes Nibble von byte_str mit oberem Nibble von key_str XORen
    - unteres Nibble von byte_str mit unterem Nibble von key_str XORen
    - beide Ergebnis-Nibbles zu einem neuen 2-stelligen String zusammensetzen
    """
    

# ---------------------------------------------------
# Aufgabe 4: Alles zusammen – encrypt_hex
# ---------------------------------------------------
def encrypt_hex(plaintext_hex, key_hex):
    """
    Schritte:
    1. SubBytes
    2. Permutation
    3. AddRoundKey
    """
   

# Test (wenn alles fertig ist):
# Erwartung: "91"
print(encrypt_hex("3A", "F0"))
