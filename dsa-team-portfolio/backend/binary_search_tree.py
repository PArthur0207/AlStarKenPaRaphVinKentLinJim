class Node:
    """A node in a binary tree."""
    def __init__(self, value,left=None, right=None):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """A binary search tree data structure with ordering property."""
    def __init__(self):
        self.root = None

    def insert(self, node, data):
        if node is None:
            return Node(data)
        else:
            if data < node.value:
                node.left = self.insert(node.left, data)
            elif data > node.value:
                node.right = self.insert(node.right, data)
        return node


    def search(self, node, target):
        """Search from a value in the BST"""
        if node:
            if node.value == target:
                return True
            elif node.value > target:
                return self.search(node.left, target)
            elif node.value < target:
                return self.search(node.right, target)
        return False
        

    def get_min_value(self, node):
        """Find the minimum value in the BST (leftmost node)."""
        if node is None:
            return None
        current = node
        while current.left is not None:
            current = current.left
        return current.value

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
    
    def delete(self, node, value):
        """ Add delete function here"""
        if node is None:
            return node
        
        if node.value > value:
            node.left = self.delete(node.left, value)
        elif node.value < value:
            node.right = self.delete(node.right, value)
        else:
            #Case 1: If no child
            if node.left is None and node.right is None:
                return None
            
            #Case 2: If one child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            
            #Case 3: If 2 children
            successor_value = self.get_min_value(node.right)
            node.value = successor_value
            node.right = self.delete(node.right, successor_value)

        return node

    def get_max_value(self, node):
        """Find the maximum value in the BST (rightmost node)"""
        if node is None:
            return None
        current = node
        while current.right is not None:
            current = current.right
        return current.value

    def find_height(self, node):
        """Find the height of the BST"""
        if node is None:
            return -1
        left_height = self.find_height(node.left)
        right_height = self.find_height(node.right)
        return max(left_height, right_height) + 1


# Example usage
if __name__ == "__main__":
   
    bst = BinarySearchTree()
    
        # Insert values
    values = [50, 30, 70, 20, 40, 60, 80, 25]
    print("Inserting values:", values)
    for val in values:
        bst.root = bst.insert(bst.root, val)


    # Display traversals
    print("\nInorder traversal (sorted):", bst.inorder_traversal(bst.root,""))
    # print("Preorder traversal:", bst.preorder_traversal(bst.root,""))
    # print("Postorder traversal:", bst.postorder_traversal(bst.root,""))

      # Search for values
    print("\nSearch for 40:", bst.search(bst.root,40))
    print("Search for 25:", bst.search(bst.root,25))
    
    # Get minimum value
    print("\nMinimum value:", bst.get_min_value(bst.root))

    #Get maximum value
    print("\nMaximum Value:", bst.get_max_value(bst.root))
    
    #Get height 
    print("\nThe height of the root:", bst.find_height(bst.root))

    #Delete root node and show
    bst.root = bst.delete(bst.root, 50)
    print("\nInorder traversal (sorted) after deleting root:", bst.inorder_traversal(bst.root, ""))
    print("Preorder traversal:", bst.preorder_traversal(bst.root,""))
