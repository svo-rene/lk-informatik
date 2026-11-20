class Node():
    def __init__(self, data=None, nextNode=None):
        self.data = data
        self.nextNode = nextNode
        
class LinkedList():
    def __init__(self):
        self.head = None
        
    def insert_at_start(self, data):
        self.head = Node(data, self.head)
        
    def insert_at_end(self, data):
        newNode = Node(data)
        
        if not self.head:
            self.head = newNode
            return
        current = self.head
        
        while current.nextNode:
            current = current.nextNode
        current.nextNode = newNode
        
    def print_ll(self):
        # Eine eigene Laufvariable verwenden: self.head darf beim Ausgeben
        # nicht verändert werden, sonst ist die Liste danach leer.
        ll_str = ""
        current = self.head
        while current:
            ll_str = ll_str + str(current.data) + "--->"
            current = current.nextNode
        print(ll_str + "None")

ll = LinkedList()
ll.insert_at_start("kiwi")
ll.insert_at_start("apfel")
ll.insert_at_end("butter")
ll.insert_at_end("banane")
ll.print_ll()
ll.print_ll()   # zweiter Aufruf: die Liste ist unverändert