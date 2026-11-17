#ChildNodes über Angabe von parent einfügen können
#rekursive Methode schreiben
#über Debug Modus rekursion nachvollziehen
#Objekt genau untersuchen


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
                
        
            
            
tree1 = Tree()
tree1.add_root("Hans")
tree1.add_child("Hans", "Brigitte")
tree1.add_child("Hans", "Dieter")
tree1.add_child("Brigitte", "Petra")



print(tree1.root.children)
print(tree1.root.children[0])
print(tree1.root.children[0].children)
print(tree1.root.children[0].children[0].data)



