class TreeNode():
    def __init__(self, data):
        self.data = data
        self.children = []
        
    def app_child(self, child):
        self.children.append(child)
        
    def print_tree(self):
        print(self.data)
        if not self.children:  # Überprüfen, ob die Liste der Kinder leer ist
            return
        for child in self.children:
            child.print_tree()           
        
    def breadth_first_print(self, current_level=None):
            if current_level is None:
                current_level = self

            print(current_level.data)

            next_level = None  # Dies wird verwendet, um den ersten Knoten auf der nächsten Ebene zu speichern

            for child in current_level.children:
                if next_level is None:
                    next_level = child  # Der erste Knoten auf der nächsten Ebene wird gespeichert
                else:
                    next_level.app_child(child)  # Fügt das Kind am Ende der nächsten Ebene hinzu

            if next_level is not None:
                self.breadth_first_print(next_level)  # Rufe die Methode rekursiv für die nächste Ebene auf
                
                
hans = TreeNode("Hans")

brigitte = TreeNode("Brigitte")
walter = TreeNode("Walter")

sybille = TreeNode("Sybille")
erhard = TreeNode("Erhard")
frank = TreeNode("Frank")

martha = TreeNode("Martha")

hans.app_child(brigitte)
hans.app_child(walter)

walter.app_child(martha)

brigitte.app_child(sybille)
brigitte.app_child(erhard)
brigitte.app_child(frank)


hans.print_tree()

print("_________________")
hans.breadth_first_print()

