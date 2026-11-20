class TreeNode():
    def __init__(self, data):
        self.data = data
        self.children = []

class Tree():
    def __init__(self):
        self.root = None

    def add_root(self, node):
        if self.root is None:
            self.root = node
        else:
            raise Exception("Es gibt schon einen Wurzel-Knoten")

    def add_child(self, parent_data, child_data):
        if self.root is None:
            raise Exception("Es gibt noch keinen Wurzel-Knoten")
        self.__find_and_append(self.root, parent_data, child_data)

    def __find_and_append(self, current_node, parent_data, child_data):
        if current_node.data == parent_data:
            current_node.children.append(TreeNode(child_data))
        else:
            for child in current_node.children:
                self.__find_and_append(child, parent_data, child_data)
 
    def print_tree(self):
        if self.root is not None:
            self.__print_tree(self.root)

    def __print_tree(self, current_node, depth=0):
        print("  " * depth + current_node.data)
        for child in current_node.children:
            self.__print_tree(child, depth + 1)




# Beispiel-Nutzung:
tree = Tree()
tree.add_root(TreeNode("Hans"))
tree.add_child("Hans", "Brigitte")
tree.add_child("Hans", "Walter")
tree.add_child("Walter", "Martha")
tree.add_child("Brigitte", "Sybille")
tree.add_child("Brigitte", "Erhard")
tree.add_child("Brigitte", "Frank")

tree.print_tree()