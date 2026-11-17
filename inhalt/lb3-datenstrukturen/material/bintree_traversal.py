class TreeNode():
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

class BinaryTree():
    def __init__(self):
        self.root = None

    def add_root(self, data):
        if self.root is None:
            self.root = TreeNode(data)
        else:
            raise Exception("Es gibt bereits einen Wurzel-Knoten.")

    def print_tree(self, node=None):
        if node is None:
            node = self.root
            
        if node:
            print(node.data)
            if node.left:
                self.print_tree(node.left)
            if node.right:
                self.print_tree(node.right)

    def in_order(self, node=None):
        if node is None:
            node = self.root
            
        if node:
            if node.left:
                self.in_order(node.left)
                
            print(node.data)
            
            if node.right:
                self.in_order(node.right)

    def add_child(self, data, node=None):
        if node is None:
            node = self.root

        if data < node.data:
            if node.left is None:
                node.left = TreeNode(data)
            else:
                self.add_child(data, node.left)
        elif data > node.data:
            if node.right is None:
                node.right = TreeNode(data)
            else:
                self.add_child(data, node.right)

bst = BinaryTree()
bst.add_root(8)
bst.add_child(3)
bst.add_child(10)
bst.add_child(14)
bst.add_child(1)
bst.add_child(6)
print("pre order:")
bst.print_tree()
print("____________")
print("in order:")
bst.in_order()