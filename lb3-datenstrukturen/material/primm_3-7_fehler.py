# PRIMM 3.7 – Fehler finden: als_matrix liefert vier gleiche Zeilen.

graph = {"A": ["B", "C"], "B": ["C"], "C": ["A"], "D": ["C"]}


def als_matrix(graph):
    knoten = list(graph)
    n = len(knoten)
    m = [[0] * n] * n
    for u in graph:
        for v in graph[u]:
            m[knoten.index(u)][knoten.index(v)] = 1
    return m


for zeile in als_matrix(graph):
    print(zeile)
# erwartet:
# [0, 1, 1, 0]
# [0, 0, 1, 0]
# [1, 0, 0, 0]
# [0, 0, 1, 0]
