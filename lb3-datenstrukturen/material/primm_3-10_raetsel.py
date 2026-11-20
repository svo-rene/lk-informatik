# PRIMM 3.10 – Was macht raetsel?
# Erst auf Papier vorhersagen, dann ausführen (F5), dann mit dem Debugger untersuchen (Strg+F5).


def raetsel(n, folge):
    if len(folge) == n:
        print(folge)
        return 1
    anzahl = 0
    for ziffer in [0, 1]:
        if len(folge) > 0 and folge[-1] == 1 and ziffer == 1:
            continue
        folge.append(ziffer)
        anzahl = anzahl + raetsel(n, folge)
        folge.pop()
    return anzahl


print(raetsel(3, []))
