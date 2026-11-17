#ChildNodes zur Root hinzufügen
#Objekt genau untersuchen
#über View -> Variables und Object Inspektor anschalten
#Objekt weiter untersuchen

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

    def add_child(self, data):
        if self.root == None:
            print("Es kann kann Kind-Knoten eingefügt werden, weil es keinen Wurzel-Knoten gibt.")
            return
        else:
            self.root.children.append(TreeNode(data))
            
            
tree1 = Tree()
tree1.add_root("Hans")
tree1.add_child("Brigitte")
tree1.add_child("Dieter")
print(tree1.root.children)
print(tree1.root.children[0])
print(tree1.root.children[0].data)



