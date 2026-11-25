class TreeNode():
    def __init__(self, data):
        self.data = data
        self.children = []
        
class Tree():
    def __init__(self):
        self.root = None
        
    def add_root(self, node):
        if self.root == None:
            self.root = node
        else:
            raise Exception("Es gibt schon einen Wurzel-Knoten")

stammbaum = Tree()
hans = TreeNode("Hans")
stammbaum.add_root(hans)
print(stammbaum.root)
print(stammbaum.root.data)
