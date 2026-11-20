# PRIMM 3.9 – Fehler finden: dijkstra liefert zu kleine Entfernungen.

graph = {
    "S": {"A": 5, "B": 1},
    "A": {"S": 5, "B": 2, "Z": 1},
    "B": {"S": 1, "A": 2, "Z": 6},
    "Z": {"A": 1, "B": 6},
}


def dijkstra(graph, start, dist):
    for k in graph:
        dist[k] = float("inf")
    dist[start] = 0
    fertig = []
    while len(fertig) < len(graph):
        u = None
        for k in graph:
            if k not in fertig:
                if u is None or dist[k] < dist[u]:
                    u = k
        fertig.append(u)
        for v in graph[u]:
            w = graph[u][v]
            if v not in fertig and w < dist[v]:
                dist[v] = w


dist = {}
dijkstra(graph, "S", dist)
print(dist)   # erwartet: {'S': 0, 'A': 3, 'B': 1, 'Z': 4}
