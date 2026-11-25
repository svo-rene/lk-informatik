# PRIMM 3.8 – Fehler finden: bfs liefert manche Knoten doppelt.

from queue_knoten import Queue   # Schlange mit Knoten aus Seite 3.2 (Datei in denselben Ordner legen)

class Graph:
    def __init__(self, size):
        self.size = size
        self.graph = []
        for i in range(size):
            self.graph.append([])

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def bfs(self, start):
        visited = [False] * self.size
        queue = Queue()
        queue.enqueue(start)
        reihenfolge = []
        while not queue.is_empty():
            current = queue.dequeue()
            visited[current] = True
            reihenfolge.append(current)
            for n in self.graph[current]:
                if not visited[n]:
                    queue.enqueue(n)
        return reihenfolge


h = Graph(4)
h.add_edge(0, 1)
h.add_edge(0, 2)
h.add_edge(1, 2)
h.add_edge(2, 3)
print(h.bfs(0))      # erwartet: [0, 1, 2, 3]
