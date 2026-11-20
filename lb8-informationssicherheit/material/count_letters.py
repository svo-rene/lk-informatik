def count_letters(text):
    from collections import Counter
    # Zählt nur alphabetische Zeichen und ignoriert Leerzeichen und andere Zeichen
    filtered_text = ''.join(filter(str.isalpha, text))
    letter_counts = Counter(filtered_text.upper())  # Konvertiere alles in Großbuchstaben für eine einheitliche Zählung
    return dict(sorted(letter_counts.items(), key=lambda item: item[1], reverse=True))

encrypted_text = ".."

# Buchstabenhäufigkeit im verschlüsselten Text
letter_frequencies = count_letters(encrypted_text)
print(letter_frequencies)