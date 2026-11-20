# PRIMM 3.8 – Was macht raetsel?
# Erst auf Papier vorhersagen, dann ausführen (F5), dann mit dem Debugger untersuchen (Strg+F5).

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

    def raetsel(self, start):
        visited = [False] * self.size
        queue = Queue()
        queue.enqueue(start)
        visited[start] = True
        anzahl = 0
        while not queue.is_empty():
            current = queue.dequeue()
            anzahl = anzahl + 1
            for n in self.graph[current]:
                if not visited[n]:
                    visited[n] = True
                    queue.enqueue(n)
        return anzahl == self.size


g = Graph(5)
g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(3, 4)
print(g.raetsel(0))
print(g.raetsel(3))
