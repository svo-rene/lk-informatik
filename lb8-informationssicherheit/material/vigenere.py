def verschiebe(buchstabe, abstand):
    # Konvertiere den übergebenen Buchstaben in Kleinbuchstaben
    buchstabe = buchstabe.lower()
    start = ord('a')

    # Konvertiere den Buchstaben in seinen ASCII-Wert
    buchstabe_ascii = ord(buchstabe)

    # Verschiebe den ASCII-Wert um den angegebenen Abstand
    neuer_ascii = (buchstabe_ascii - start + abstand) % 26 + start

    # Konvertiere den verschobenen ASCII-Wert zurück in einen Buchstaben
    return chr(neuer_ascii)


def ist_buchstabe(zeichen):
    return 'a' <= zeichen.lower() <= 'z'


def vigenere_encrypt(plain_text, key):
    encrypted_text = ""
    key_length = len(key)
    j = 0
    for char in plain_text:
        if ist_buchstabe(char):
            key_char = key[j % key_length]
            shift = ord(key_char.lower()) - ord('a')
            encrypted_text += verschiebe(char, shift)
            j += 1
        else:
            encrypted_text += char
    return encrypted_text


def vigenere_decrypt(encrypted_text, key):
    decrypted_text = ""
    key_length = len(key)
    j = 0
    for char in encrypted_text:
        if ist_buchstabe(char):
            key_char = key[j % key_length]
            shift = ord(key_char.lower()) - ord('a')
            decrypted_text += verschiebe(char, -shift)
            j += 1
        else:
            decrypted_text += char
    return decrypted_text


# Test
plain_text = "Hallo. Wie geht es dir?"
key = "Blume"
encrypted_text = vigenere_encrypt(plain_text, key)
decrypted_text = vigenere_decrypt(encrypted_text, key)

print(f"Klartext:       {plain_text}")
print(f"Geheimtext:     {encrypted_text}")
print(f"Entschlüsselt:  {decrypted_text}")
