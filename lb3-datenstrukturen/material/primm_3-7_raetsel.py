# PRIMM 3.7 – Was macht raetsel?
# Erst auf Papier vorhersagen, dann ausführen (F5), dann mit dem Debugger untersuchen (Strg+F5).

# gerichteter Graph als Adjazenzliste: zu jedem Knoten die Liste seiner Nachfolger
graph = {"A": ["B", "C"], "B": ["C"], "C": ["A"], "D": ["C"]}


def raetsel(graph):
    zaehler = {}
    for u in graph:
        zaehler[u] = 0
    for u in graph:
        for v in graph[u]:
            zaehler[v] = zaehler[v] + 1
    return zaehler


print(raetsel(graph))
