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

        parent_node = self.find_node(self.tree.root, parent_value)
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

        return "Side must be 'left' or 'right'."

    def find_node(self, current, value):
        """Find a node using inorder traversal (left, root, right)."""
        if current is None:
            return None

        # Search left subtree
        found = self.find_node(current.left, value)
        if found:
            return found

        # Check current node
        if current.value == value:
            return current

        # Search right subtree
        return self.find_node(current.right, value)

    def delete_node_by_value(self, value):
        if not self.tree.root:
            return "Tree is empty."
        return self.tree.delete_node(self.tree.root, value)

    def search_node(self, value):
        if self.find_node(self.tree.root, value):
            return f"Node '{value}' found in the tree."
        return f"Node '{value}' not found in the tree."

    def replace_node(self, old_value, new_value):
        """Replace the value of a node using traversal search."""
        node = self.find_node(self.tree.root, old_value)
        if not node:
            return f"Node '{old_value}' not found."

        node.value = new_value
        return f"Node '{old_value}' replaced with '{new_value}'."
    
    def delete_all_nodes(self):
        """Delete the entire tree."""
        self.tree.root = None
        return "All nodes have been deleted. The tree is now empty."

