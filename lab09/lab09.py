#changes

from unittest import TestCase
import random

class HBStree:
    """This is an immutable binary search tree with history.
    Each insert and delete operation creates a new version of the tree. The data
    structure allows past versions to be accessed.
    """

    class INode(tuple):
        """
        This is the class for an immutable node. Do not
        modify this code.
        """
        __slots__ = []
        def __new__(cls, val, left, right):
            return tuple.__new__(cls, (val, left, right))

        @property
        def val(self):
            return tuple.__getitem__(self, 0)

        @property
        def left(self):
            return tuple.__getitem__(self, 1)

        @property
        def right(self):
            return tuple.__getitem__(self, 2)

        def __getitem__(self, item):
            raise TypeError

    def __init__(self):
        """
        Create a new tree that initially consists of one
        versions that is the empty tree.
        """
        self.root_versions = [None]

    def num_versions(self):
        """
        Return the number of versions in the tree.
        """
        return len(self.root_versions)

    def __getitem__(self, key):
        """
        Returns key if key exists in the current version of the tree. Raise a
        KeyError, if key does not exist.
        """
        # BEGIN SOLUTION
        node = self.root_versions[-1]
        while True:
            if node == None:
                raise KeyError
            elif key == node.val:
                return key
            elif key > node.val:
                node = node.right
            elif key < node.val:
                node = node.left
        # END SOLUTION

    def __contains__(self, el):
        """
        Return True if el exists in the current version of the tree.
        """
        # BEGIN SOLUTION
        node = self.root_versions[-1]
        while True:
            if node == None:
                return False
            elif el == node.val:
                return True
            elif el > node.val:
                node = node.right
            elif el < node.val:
                node = node.left
        # END SOLUTION

    def insert(self,key):
        """
        Adds key to the tree, creating a new version of the
        tree. If key already exists, then do nothing and refrain
        from creating a new version.
        """
        # BEGIN SOLUTION
        if len(self.root_versions) == 1:
            self.root_versions.append(self.INode(key, None, None))
            return
        node = self.root_versions[-1]
        changeNode = [node]
        while True:
            left = True
            right = True
            if node == None:
                break
            if key == node.val:
                return
            if node.left == None:
                left = False
                if key < node.val:
                    changeNode.append([node, -1])
                    break
            if node.right == None:
                right = False
                if key > node.val:
                    changeNode.append([node, 1])
                    break
            if left and key < node.val:
                changeNode.append([node, -1])
                node = node.left
            if right and key > node.val:
                changeNode.append([node, 1])
                node = node.right

        newNode = self.INode(key, None, None)
        for index in range(len(changeNode) - 1, 0, -1):
            tempNode = changeNode[index]
            if tempNode[1] == -1:
                newNode = self.INode(tempNode[0].val, newNode, tempNode[0].right)
            else:
                newNode = self.INode(tempNode[0].val, tempNode[0].left, newNode)

        self.root_versions.append(newNode)
        # END SOLUTION

    def deleteHelper(self, node):
        if node.left == None and node.left == None:
            return None
        elif node.left == None:
            newNode = self.INode(node.right.val, node.right.left, node.right.right)
            return newNode
        elif node.right == None:
            newNode = self.INode(node.left.val, node.left.left, node.left.right)
            return newNode
        else:
            if node.left.right != None:
                newNode = self.INode(node.left.right.val, node.left, self.deleteHelper(node.right))
            else:
                newNode = self.INode(node.left.val, node.left, self.deleteHelper(node.right))
                
    def delete(self,key):
        """Delete key from the tree, creating a new version of the tree. If key does not exist in the current version of the tree, then do nothing and refrain from creating a new version."""
        # BEGIN SOLUTION
        if key in self:
            node = self.root_versions[-1]
            changeNode = []
            while True:
                if node == None or key == node.val:
                    deletedNode = node
                    break
                if node.left != None and key < node.val:
                    changeNode.append([node, -1])
                    node = node.left
                if node.right != None and key > node.val:
                    changeNode.append([node, 1])
                    node = node.right

            postNodes = []
            if node.left != None:
                node = node.left
                while node.right != None:
                    postNodes.append(node)
                    node = node.right
            newNode = None
            if len(postNodes) != 0:
                for index in range(len(postNodes) - 1, 0, -1):
                    newNode = self.INode(postNodes[index].val, postNodes[index].left, newNode)
                newNode = self.INode(node.val, deletedNode.left, newNode)
            else:
                newNode = deletedNode.right
            for index in range(len(changeNode) - 1 , -1, -1):
                if changeNode[index][1] == -1:
                    newNode = self.INode(changeNode[index][0].val, newNode, changeNode[index][0].right)
                else:
                    newNode = self.INode(changeNode[index][0].val, changeNode[index][0].left, newNode)
            self.root_versions.append(newNode)
        # END SOLUTION

    @staticmethod
    def subtree_size(node):
        """
        Returns the number of nodes in the subtree rooted at node.
        """
        if not node:
            return 0
        else:
            return 1 + HBStree.subtree_size(node.left) + HBStree.subtree_size(node.right)

    def __len__(self):
        """
        Return the nuber of nodes in the current version of the tree.
        """
        return HBStree.subtree_size(self.get_current_root())

    @staticmethod
    def all_nodes(r, nodes):
        """
        Adds all nodes of the subtree rooted at r to set nodes.
        """
        if r:
            nodes.add(r)
            HBStree.all_nodes(r.left, nodes)
            HBStree.all_nodes(r.right, nodes)

    def total_size(self):
        """
        Return the total number of nodes in all versions of the tree.
        """
        nodes = set()
        for i in self.root_versions:
            HBStree.all_nodes(i, nodes)
        return len(nodes)

    def share_factor(self):
        """
        Calculates the degree of sharing between versions of this tree as the
        sum of the number of nodes per version divided by the number of nodes
        the data structure (recall that nodes can be shared across versions).
        """
        t = self.total_size()
        sumsizes = sum([ HBStree.subtree_size(r) for r in self.root_versions ])
        return sumsizes / t

    def get_current_root(self):
        """
        Return the root node of the current version of the tree.
        """
        return self.root_versions[-1]

    def __iter__(self):
        """
        Returns an iterator for the current version of the
        BS-tree that returns the values stored in the tree in
        increasing order.
        """
        return self.version_iter()

    def getAll(self, node):
        if node == None:
            return None
        allVals = [node.val]
        if node.left != None:
            allVals = self.getAll(node.left) + allVals
        if node.right != None:
            allVals += self.getAll(node.right)
        return allVals
        


    def version_iter(self, timetravel=0):
        """
        Return an iterator that allows sorted access to the nodes of a past
        version of the tree. Parameter timetravel determines how many versions
        we should go back. The default 0 accesses the current version of the
        BS-tree.
        """
        if timetravel < 0 or timetravel >= len(self.root_versions):
            raise IndexError(f"valid versions for time travel are 0 to {len(self.root_versions) -1}, but was {timetravel}")
        # BEGIN SOLUTION
        version = self.root_versions[len(self.root_versions) - timetravel - 1]
        if version == None:
            yield 
        else:
            values = self.getAll(version)
            for val in values:
                yield val
        # END SOLUTION

    @staticmethod
    def stringify_subtree(root):
        """
        Creates a string representation of the tree rooted at root.
        """
        height = HBStree.height(root)
        width=4 * pow(2,height)
        nodes = [(root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n,level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height-1:
                    nodes.extend([(None, level+1), (None, level+1)])
                repr_str += '{val:^{width}}'.format(val='-', width=width//2**level)
            elif n:
                if n.left or level < height-1:
                    nodes.append((n.left, level+1))
                if n.right or level < height-1:
                    nodes.append((n.right, level+1))
                repr_str += '{val:^{width}}'.format(val=n.val, width=width//2**level)
        return repr_str

    @staticmethod
    def height(root):
        """
        Returns the height of the longest branch of a tree rooted at root.
        """
        def height_rec(n):
            if not n:
                return 0
            else:
                return max(1+height_rec(n.left), 1+height_rec(n.right))
        return height_rec(root)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        """
        Generates a stirng representation of all versions of the tree.
        """
        s = ""
        for t in range(0, len(self.root_versions)):
            r = self.root_versions[t]
            s += (80 * "=") + f"\nVersion: {t}\n" + (80 * "=") + f"\n{HBStree.stringify_subtree(r)}\n"
        return s

################################################################################
# TEST CASES
################################################################################
def check_inserted(vals):
    tc = TestCase()
    t = HBStree()

    print(f"test inserting {vals}")

    for v in vals:
        t.insert(v)

    for i in range(0,len(vals) + 1):
        sortel = [ v for v in t.version_iter(len(vals) - i) ]
        sortval = sorted(vals[0:i])
        for j in range(0,i):
            tc.assertEqual(sortval[j],sortel[j])
    return t

# 20 points
def test_insert_1():
    check_inserted([3,1,5])
    check_inserted([1,2,3,4,5,6])
    check_inserted([6,5,4,3,2,1])
    check_inserted([11,51,1,6,89,123,4,2,3,5,7])

# 20 points
def test_insert_2():
    for i in range(0,10):
        vals = [ random.randint(0,100) for i in range(0,100) ]
        vals = list(set(vals))
        random.shuffle(vals)
        check_inserted(vals)

# 10 points
def test_lookup():
    for i in range(0,10):
        vals = [ random.randint(0,100) for i in range(0,100) ]
        vals = list(set(vals))
        random.shuffle(vals)
        t = check_inserted(vals)
        tc = TestCase()
        for v in vals:
            tc.assertTrue(v in t)
        for v in [ random.randint(101,1000) for i in range(0,100) ]:
            tc.assertFalse(v in t)

def insert_check_delete(vals):
    tc = TestCase()
    t = HBStree()

    print(f"test inserting and deleting {vals}")

    for v in vals:
        t.insert(v)

    todo = sorted(vals)
    for i in range(0,len(vals)):
        t.delete(todo[0])
        del todo[0]
        sortel = [ v for v in t.version_iter() ]
        sortval = sorted(todo)
        for j in range(0,len(sortval)):
            tc.assertEqual(sortval[j],sortel[j])

# 20 points
def test_delete_1():
    insert_check_delete([1,2,3,4,5])
    insert_check_delete([2,5,1,7,6,4])

# 20 points
def test_delete_2():
    for i in range(0,10):
        vals = [ random.randint(0,100) for i in range(0,100) ]
        vals = list(set(vals))
        random.shuffle(vals)
        insert_check_delete(vals)

# 10 points
def test_corner_cases():
    tc = TestCase()
    t = HBStree()

    # insert multiple times
    for i in range(0,10,2):
        for j in range(0,3):
            t.insert(i)

    tc.assertEqual(t.num_versions(), len(range(0,10,2)) + 1)

    t = HBStree()

    for i in range(0,5):
        t.insert(3 * i)

    for i in range(0,5):
        t.delete(0)

    tc.assertEqual(t.num_versions(), len(range(0,5)) + 2)

    with tc.assertRaises(KeyError):
        t[0]

    with tc.assertRaises(IndexError):
        it = t.version_iter(-1)
        next(it)

    with tc.assertRaises(IndexError):
        it = t.version_iter(10)
        next(it)


################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "#" + "\n" + f.__name__ + "\n" + 80 * "#" + "\n")

def say_success():
    print("----> SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    for t in [test_insert_1,
              test_insert_2,
              test_lookup,
              test_delete_1,
              test_delete_2,
              test_corner_cases]:
        say_test(t)
        t()
        say_success()
    print(80 * "#" + "\nALL TEST CASES FINISHED SUCCESSFULLY!\n" + 80 * "#")

if __name__ == '__main__':
    main()
