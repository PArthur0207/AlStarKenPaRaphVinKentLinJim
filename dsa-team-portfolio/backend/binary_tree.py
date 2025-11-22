class Node:
    """A node in a binary tree."""
    def __init__(self, value,left=None, right=None):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    """A binary tree data structure."""
    def __init__(self, root_value=None):
        self.root = Node(root_value) if root_value is not None else None

    def insert_left(self, current_node, value):
        """Insert a node as the left child of the current node."""
        if current_node.left is None:
            current_node.left = Node(value)
        else:
            new_node = Node(value)
            new_node.left = current_node.left
            current_node.left = new_node

    def insert_right(self, current_node, value):
        """Insert a node as the right child of the current node."""
        if current_node.right is None:
            current_node.right = Node(value)
        else:
            new_node = Node(value)
            new_node.right = current_node.right
            current_node.right = new_node

    def preorder_traversal(self, start,traversal):
        """Traverse the tree in preorder (root, left, right)."""
        if start:
            traversal += (str(start.value) + " ")
            traversal = self.preorder_traversal(start.left,traversal)
            traversal = self.preorder_traversal(start.right,traversal)
        return traversal    

    def inorder_traversal(self, start,traversal):
        """Traverse the tree in inorder (left, root, right)."""
        if start:
            traversal = self.inorder_traversal(start.left,traversal)
            traversal += (str(start.value) + " ")
            traversal = self.inorder_traversal(start.right,traversal)
        return traversal    

    def postorder_traversal(self, start,traversal):
        """Traverse the tree in postorder (left, right, root)."""
        if start:
            traversal = self.postorder_traversal(start.left,traversal)
            traversal = self.postorder_traversal(start.right,traversal)
            traversal += (str(start.value) + " ")
        return traversal 

    def search(self, root, find):
        """Search for a specific node in the tree."""
        if root is None:
            return False   
        if root.value == find:
            return True   
        left_check = self.search(root.left, find)
        if left_check:
            return True
        right_check = self.search(root.right, find)
        return right_check

    def delete_node(self, root, value):
        """Removing a node while maintaining the tree structure."""
        if root is None:
            return "Tree is empty"

        # Deleting the root
        if root.value == value:
            if root.left:
                new_root = root.left
                # Attach root's right child to the rightmost node of new_root
                rightmost = new_root
                while rightmost.right:
                    rightmost = rightmost.right
                rightmost.right = root.right
                self.root = new_root
            else:
                self.root = root.right  # promote right if no left
            return f"Deleted {value}"

        # Search for parent of the node to delete
        parent_queue = [root]
        while parent_queue:
            parent = parent_queue.pop(0)
            # Check left child
            if parent.left and parent.left.value == value:
                node_to_delete = parent.left
                if node_to_delete.left:
                    parent.left = node_to_delete.left
                    # attach right child of deleted node to rightmost of new left child
                    rightmost = parent.left
                    while rightmost.right:
                        rightmost = rightmost.right
                    rightmost.right = node_to_delete.right
                else:
                    parent.left = node_to_delete.right  # promote right if no left
                return f"Deleted {value}"
            # Check right child
            if parent.right and parent.right.value == value:
                node_to_delete = parent.right
                if node_to_delete.left:
                    parent.right = node_to_delete.left
                    # attach right child of deleted node to rightmost of new left child
                    rightmost = parent.right
                    while rightmost.right:
                        rightmost = rightmost.right
                    rightmost.right = node_to_delete.right
                else:
                    parent.right = node_to_delete.right  # promote right if no left
                return f"Deleted {value}"
            # Add children to queue
            if parent.left:
                parent_queue.append(parent.left)
            if parent.right:
                parent_queue.append(parent.right)

        return "Item not found in the tree"



# Example usage
if __name__ == "__main__":
   
    tree = BinaryTree("R")
    
    # Insert nodes
    tree.insert_left(tree.root, "A")
    tree.insert_right(tree.root, "B")
    tree.insert_left(tree.root.left, "C")
    tree.insert_right(tree.root.left, "D")
    tree.insert_left(tree.root.right, "E")
    tree.insert_right(tree.root.right, "F")
    tree.insert_left(tree.root.right.right, "G")
    
    print()

    print("Preorder traversal: " + tree.preorder_traversal(tree.root,""))
    ##tree.preorder_traversal(tree.root,"")
    print("\n\nInorder traversal: " + tree.inorder_traversal(tree.root,""))
    # tree.inorder_traversal(tree.root)
    print("\n\nPostorder traversal: " + tree.postorder_traversal(tree.root,""))
    # tree.postorder_traversal(tree.root)
    print("\n\nSearch for F: " + str(tree.search(tree.root, "F")))
    # Search for F in the binary tree
    print("\n\nDelete A: " + str(tree.delete_node(tree.root, "A")))
    # Delete A from the Binary tree
    print("\n\nPostorder traversal: " + tree.postorder_traversal(tree.root,""))
    # Show the binary tree after A was deleted
