# PRIMM 3.9 – Dijkstra beobachten
# Erst auf Papier vorhersagen, dann ausführen (F5), dann mit dem Debugger untersuchen (Strg+F5).

graph = {
    "S": {"A": 5, "B": 1},
    "A": {"S": 5, "B": 2, "Z": 1},
    "B": {"S": 1, "A": 2, "Z": 6},
    "Z": {"A": 1, "B": 6},
}


def dijkstra(graph, start, dist, vorgaenger):
    # Vorbereitung: alle Distanzen unendlich, kein Vorgänger, noch nichts fertig
    for k in graph:
        dist[k] = float("inf")
        vorgaenger[k] = None
    dist[start] = 0
    fertig = []

    while len(fertig) < len(graph):
        # 1. unter den offenen Knoten den mit der kleinsten Distanz suchen
        u = None
        for k in graph:
            if k not in fertig:
                if u is None or dist[k] < dist[u]:
                    u = k
        # 2. u wird fertig: seine Distanz ist endgültig
        fertig.append(u)
        # 3. Kanten zu offenen Nachbarn relaxieren
        for v in graph[u]:
            w = graph[u][v]                  # Gewicht der Kante u–v
            if v not in fertig and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                vorgaenger[v] = u


dist = {}                     # dijkstra füllt diese beiden Dictionaries
vorgaenger = {}
dijkstra(graph, "S", dist, vorgaenger)
print(dist)
print(vorgaenger)
