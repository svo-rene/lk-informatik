# Schlange (Queue) mit Knoten – wie auf Kursseite 3.2, Beispiel 2.
# Diese Datei in denselben Ordner legen wie das Programm, das sie benutzt.
# Dann holt man die Klasse mit:  from queue_knoten import Queue


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        self.__head = None    # vorn: hier wird entnommen
        self.__tail = None    # hinten: hier wird eingefügt

    def is_empty(self):
        return self.__head is None

    def enqueue(self, data):
        neu = Node(data)
        if self.__tail is None:         # Schlange war leer
            self.__head = neu
        else:
            self.__tail.next = neu
        self.__tail = neu

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue aus leerer Schlange")
        data = self.__head.data
        self.__head = self.__head.next
        if self.__head is None:         # letztes Element entnommen
            self.__tail = None
        return data

    def peek(self):
        if self.is_empty():
            raise IndexError("peek auf leerer Schlange")
        return self.__head.data


if __name__ == "__main__":
    # Testzeilen: laufen nur beim direkten Start (F5), nicht beim import
    q = Queue()
    for auftrag in ["Brief.pdf", "Foto.jpg", "Referat.docx"]:
        q.enqueue(auftrag)
    print(q.dequeue())   # Brief.pdf
    print(q.peek())      # Foto.jpg
