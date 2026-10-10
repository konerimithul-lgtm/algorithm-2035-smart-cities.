"""B-Tree and Red-Black Tree comparison for Algorithm 2035.
Both structures support insertion and search. Implementations are educational.
"""
from __future__ import annotations


class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []


class BTree:
    def __init__(self, degree=2):
        if degree < 2:
            raise ValueError("B-Tree minimum degree must be at least 2.")
        self.t = degree
        self.root = BTreeNode()

    def search(self, key):
        node = self.root
        while True:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i < len(node.keys) and key == node.keys[i]:
                return True
            if node.leaf:
                return False
            node = node.children[i]

    def insert(self, key):
        if self.search(key):
            return
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_nonfull(new_root, key)
        else:
            self._insert_nonfull(root, key)

    def _split_child(self, parent, i):
        t = self.t
        full = parent.children[i]
        right = BTreeNode(leaf=full.leaf)
        median = full.keys[t - 1]
        right.keys = full.keys[t:]
        full.keys = full.keys[:t - 1]
        if not full.leaf:
            right.children = full.children[t:]
            full.children = full.children[:t]
        parent.children.insert(i + 1, right)
        parent.keys.insert(i, median)

    def _insert_nonfull(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(key)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_nonfull(node.children[i], key)


RED, BLACK = True, False


class RBNode:
    def __init__(self, key=None, color=BLACK):
        self.key, self.color = key, color
        self.left = self.right = self.parent = None


class RedBlackTree:
    def __init__(self):
        self.nil = RBNode()
        self.root = self.nil

    def search(self, key):
        cur = self.root
        while cur != self.nil:
            if key == cur.key:
                return True
            cur = cur.left if key < cur.key else cur.right
        return False

    def insert(self, key):
        z = RBNode(key, RED)
        z.left = z.right = self.nil
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if key == x.key:
                return
            x = x.left if key < x.key else x.right
        z.parent = y
        if y == self.nil:
            self.root = z
        elif key < y.key:
            y.left = z
        else:
            y.right = z
        self._fix_insert(z)

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.nil:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def _fix_insert(self, z):
        while z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
        self.root.color = BLACK
