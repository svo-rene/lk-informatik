#TreeNode Klasse und Tree Klasse
#Hinzufügen einer Root
#Untersuchen der Instanz

class TreeNode():
    def __init__(self, data):
        self.data = data
        self.children = []
        
class Tree():
    def __init__(self):
        self.root = None
        
    def insert(self, data):
        if self.root == None:
            self.root = TreeNode(data)
        else:
            print("Es gibt schon einen Wurzel-Knoten.")
            
tree1 = Tree()
tree1.insert("Hans")
print(tree1.root)
print(tree1.root.data)
print(tree1.root.children)
