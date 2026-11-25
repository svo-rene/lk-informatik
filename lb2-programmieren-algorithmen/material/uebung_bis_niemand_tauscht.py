# Übung 2: Bis niemand mehr tauscht
def durchlauf(liste):
    for i in range(len(liste) - 1):
        if liste[i] > liste[i + 1]:
            temp = liste[i]
            liste[i] = liste[i + 1]
            liste[i + 1] = temp


def sortiere(liste):
    # dein Code
    pass


zahlen = [5, 2, 9, 1, 7]
sortiere(zahlen)
print(zahlen)
