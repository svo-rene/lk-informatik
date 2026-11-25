# PRIMM 3.10 – Fehler finden: Am Ende stehen nur leere Listen in ergebnisse.


def sammeln(n, folge, ergebnisse):
    if len(folge) == n:
        ergebnisse.append(folge)
        return
    for ziffer in [0, 1]:
        if len(folge) > 0 and folge[-1] == 1 and ziffer == 1:
            continue
        folge.append(ziffer)
        sammeln(n, folge, ergebnisse)
        folge.pop()


ergebnisse = []
sammeln(3, [], ergebnisse)
print(ergebnisse)
# erwartet: [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 0, 1]]
