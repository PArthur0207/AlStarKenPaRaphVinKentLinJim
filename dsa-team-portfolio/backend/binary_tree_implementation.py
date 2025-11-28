from .binary_tree import Node, BinaryTree

class BinaryTreeManager:
    """Binary tree manager for web interaction."""

    def __init__(self):
        self.tree = BinaryTree()

    def add_node(self, parent_value, side, new_value):
        """Add a node to the tree."""
        if self.tree.root is None:
            self.tree.root = Node(new_value)
            return f"Root node '{new_value}' added."

        parent_node = self.find_node(parent_value)
        if not parent_node:
            return f"Parent node '{parent_value}' not found."

        if side.lower() == "left":
            if parent_node.left is None:
                self.tree.insert_left(parent_node, new_value)
                return f"Node '{new_value}' added to left of '{parent_value}'."
            else:
                return f"Left child of '{parent_value}' already exists."
        elif side.lower() == "right":
            if parent_node.right is None:
                self.tree.insert_right(parent_node, new_value)
                return f"Node '{new_value}' added to right of '{parent_value}'."
            else:
                return f"Right child of '{parent_value}' already exists."
        else:
            return "Side must be 'left' or 'right'."

    def find_node(self, value):
        """Return node object with the given value."""
        items = self.tree.inorder_traversal(self.tree.root, "")
        if items:
            for item in items:
                if item == value:
                    return item
            return None
        return None

    def delete_node_by_value(self, value):
        """Delete a node by value and return a message."""
        if not self.tree.root:
            return "Tree is empty."
        msg = self.tree.delete_node(self.tree.root, value)
        return msg

    def search_node(self, value):
        """Search for a node by value and return a message."""
        if self.tree.search(self.tree.root, value):
            return f"Node '{value}' found in the tree."
        else:
            return f"Node '{value}' not found in the tree."
        
    def replace_node(self, old_value, new_value):
        """Replace the value of a node with a new value."""
        node = self.find_node(old_value)
        if not node:
            return f"Node '{old_value}' not found."
        node.value = new_value
        return f"Node '{old_value}' replaced with '{new_value}'."
