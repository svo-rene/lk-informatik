#rekursive Print Methode schreiben
#über Einrückungen die Ansicht verbessern
#über Reihenfolge der Ausgabe auf Art der Traversierung schließen -> Tiefensuche

class TreeNode():
    def __init__(self, data):
        self.data = data
        self.children = []
        
class Tree():
    def __init__(self):
        self.root = None
        
    def add_root(self, data):
        if self.root == None:
            self.root = TreeNode(data)
        else:
            print("Es gibt schon einen Wurzel-Knoten.")
        

    def add_child(self, parent, data):
        if self.root is None:
            print("Es kann kein Kind-Knoten eingefügt werden, da es keinen Wurzel-Knoten gibt.")
            return
        else:
            self.__add_child_recursive(self.root, parent, data)
    
    
    def __add_child_recursive(self, current_node, parent, data):
        if current_node.data == parent:
            current_node.children.append(TreeNode(data))
        else:
            for child_node in current_node.children:
                self.__add_child_recursive(child_node, parent, data)
                
    def print_tree(self, node=None):
        if node is None:
            node = self.root
        print(node.data)
        for child in node.children:
            self.print_tree(child)
            
    def print_tree_structure(self, node=None, level=0):
        if node is None:
            node = self.root
        print("  " * level + node.data)
        for child in node.children:
            self.print_tree_structure(child, level + 1)
            
            
tree1 = Tree()
tree1.add_root("Hans")
tree1.add_child("Hans", "Brigitte")
tree1.add_child("Hans", "Dieter")
tree1.add_child("Brigitte", "Petra")



tree1.print_tree()
print("----------")
tree1.print_tree_structure()




