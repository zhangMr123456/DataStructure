#!/usr/bin/env python
# Author: Tyler Sanderson <tylerbtbam@gmail.com>
#
# This file is part of PyBST.
#
# PyBST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyBST.  If not, see <http://www.gnu.org/licenses/>.

import collections


class Node:
    """Represents a node of a binary tree"""

    def __init__(self, key, value):
        self.left = None
        self.right = None
        self.parent = None
        self.key = key
        self.value = value


class BSTree:
    """
    BSTree implements an unbalanced Binary Search Tree.

    A Binary Search Tree is an ordered node based tree key structure
    in which each node has at most two children.

    For more information regarding BSTs, see:
    http://en.wikipedia.org/wiki/Binary_search_tree

    Constructors:

    BSTree() -> Creates a new empty Binary Search Tree
    BSTree(seq) -> Creates a new Binary Search Tree from the elements in sequence [(k1,v1),(k2,v2),...,(kn,vn)]
    """

    def __init__(self, *args):

        self.Root = None

        if len(args) == 1:  # 判断长度为1个参数直接取出开始插入
            if isinstance(args[0], collections.Iterable):
                for x in args[0]:
                    self.insert(x[0], x[1])
            else:
                raise TypeError(str(args[0]) + " is not iterable")

    def is_valid(self, *args):
        """
        T.is_valid(...) -> Boolean. Produces True if and only if
        T is a valid Binary Search Tree. Raises an exception otherwise.
        """
        if len(args) == 0:
            node = self.Root
        else:
            node = args[0]

        if not node:
            return True

        if node.left:
            if not node.left.parent == node:
                raise Exception("Left child of node " + str(node.key) + " is adopted by another node!")

        if node.right:
            if not node.right.parent == node:
                raise Exception("Right child of node " + str(node.key) + " is adopted by another node!")

        if node.parent and node.parent.left == node:
            if node.key > node.parent.key:
                raise Exception(
                    "Node " + str(node.key) + " is to the left of " + str(node.parent.key) + " but is larger")

        if node.parent and node.parent.right == node:
            if node.key < node.parent.key:
                raise Exception(
                    "Node " + str(node.key) + " is to the right of " + str(node.parent.key) + " but is smaller")

        return (self.is_valid(node.left) and self.is_valid(node.right))

    def preorder(self, *args):
        """
        T.preorder(...) -> Sequence. Produces a sequence of the Nodes
        in T, obtained in preorder.
        """
        if len(args) == 0:
            elements = []
            node = self.Root
        else:
            node = args[0]
            elements = args[1]

        elements.append(node)

        if node.left:
            self.preorder(node.left, elements)
        if node.right:
            self.preorder(node.right, elements)

        return elements

    def inorder(self, *args):
        """
        T.inorder(...) -> Sequence. Produces a sequence of the Nodes
        in T, obtained in inorder.
        """
        if len(args) == 0:
            elements = []
            node = self.Root
        else:
            node = args[0]
            elements = args[1]

        if node.left:
            self.inorder(node.left, elements)

        elements.append(node)

        if node.right:
            self.inorder(node.right, elements)

        return elements

    def postorder(self, *args):
        """
        T.postorder(...) -> Sequence. Produces a sequence of the Nodes
        in T, obtained in postorder.
        """
        if len(args) == 0:
            elements = []
            node = self.Root
        else:
            node = args[0]
            elements = args[1]

        if node.left:
            self.postorder(node.left, elements)

        if node.right:
            self.postorder(node.right, elements)

        elements.append(node)

        return elements

    def levelorder(self):
        """
        T.levelorder(...) -> Sequence. Produces a sequence of the Nodes
        in T, obtained in levelorder.
        """
        q = collections.deque()
        q.appendleft(self.Root)
        lst = []
        while len(q) != 0:
            removed = q.pop()
            lst.append(removed)
            visit = self.get_node(removed, self.Root)
            if visit.left:
                q.appendleft(visit.left)
            if visit.right:
                q.appendleft(visit.right)

        return lst

    def get_node(self, key, *args):
        """
        T.get_node(key,...) -> Node. Produces the Node in T with key
        attribute key. If there is no such node, produces None.
        """
        # args中如果没有传入开始节点那就使用root作为开始节点
        if len(args) == 0:
            start = self.Root
        # 如果传入那就使用args中的参数作为开始节点
        else:
            start = args[0]

        # 如果两者都不存在那就返回空
        if not start:
            return None
        # 判断开始的key和要判断的key是否相同
        if key == start.key:
            return start
        # 根据搜索树的性质如果要判断的key 大于开始的key, 那就往右找, 直到 start.right为None的时候返回
        elif key > start.key:
            return self.get_node(key, start.right)
        # 根据搜索树的性质如果要判断的key 小于开始的key, 那就往左,直到 start.left为None的时候返回
        else:
            return self.get_node(key, start.left)

    def insert(self, key, value, *args):
        """
        T.insert(key,value...) <==> T[key] = value. Inserts
        a new Node with key attribute key and value attribute
        value into T.
        """
        #  key 不能为数字判断
        if not isinstance(key, (int, float)):
            raise TypeError(str(key) + " is not a number")
        else:
            # 如果不存在 root 那就进行创建
            if not self.Root:
                self.Root = Node(key, value)
            # 判断是否传入root节点
            elif len(args) == 0:
                # 判断节点是否存在, 如果不存在那就进行创建
                if not self.get_node(key, self.Root):
                    self.insert(key, value, self.Root)
            # 如果有额外参数, 当传入 root值的时候
            else:
                # 创建一个新的 node 节点
                child = Node(key, value)
                # 找到父节点
                parent = args[0]
                # 如果当前值大于父节点的值
                if child.key > parent.key:
                    # 如果父节点不存在右边值
                    if not parent.right:
                        # 对当前节点和父节点设置对应关系
                        parent.right = child
                        # 当前节点父类指向父节点
                        child.parent = parent
                    # 当父节点存在右子节点的值
                    else:
                        self.insert(key, value, parent.right)
                # 当前值小于父节点的值往左边走
                else:
                    # 如果不存在左边值
                    if not parent.left:
                        # 设置对应关系
                        parent.left = child
                        child.parent = parent
                    # 如果存在左边值, 那就把左边的值作为下一层级父节点继续递归
                    else:
                        self.insert(key, value, parent.left)

    def insert_from(self, seq):
        """
        T.insert_from(seq). For every key, value pair in seq,
        inserts a new Node into T with key and value attributes
        as given.
        """
        if isinstance(seq, collections.Iterable):
            for x in seq:
                self.insert(x[0], x[1])
        else:
            raise TypeError(str(iter) + " is not iterable")

    def get_max(self, *args):
        """
        T.get_max(...) -> Node. Produces the Node that has the maximum
        key attribute in T.
        """
        if len(args) == 0:
            node = self.Root
        else:
            node = args[0]

        if not node.right:
            return node
        else:
            return self.get_max(node.right)

    def get_min(self, *args):
        """
        T.get_min(...) -> Node. Produces the Node that has the minimum
        key attribute in T.
        """
        if len(args) == 0:
            node = self.Root
        else:
            node = args[0]

        if not node.left:
            return node
        else:
            return self.get_min(node.left)

    def get_element_count(self, *args):
        """
        T.get_element_count(...) -> Nat. Produces the number of elements
        in T.
        """
        if len(args) == 0:
            node = self.Root
        else:
            node = args[0]

        left = 0
        right = 0

        if node:
            if node.left:
                left = self.get_element_count(node.left)
            if node.right:
                right = self.get_element_count(node.right)

            return 1 + left + right
        else:
            return 0

    def get_height(self, *args):
        """
        T.get_height(...) -> Nat. Produces the height of T, defined
        as one added to the height of the tallest subtree.
        """
        if len(args) == 0:
            node = self.Root
        else:
            node = args[0]

        if not node or (not node.left and not node.right):
            return 0
        else:
            return 1 + max(self.get_height(node.left), self.get_height(node.right))

    def _delete_leaf(self, node):
        """
        T._delete_leaf(node). Deletes node from T, treating it as a leaf.
        """
        par_node = node.parent

        if par_node:
            if par_node.left == node:
                par_node.left = None
            else:
                par_node.right = None

            del node

    def _delete_leaf_parent(self, node):
        """
        T._delete_leaf_parent(node). Deletes node from T, treating it
        as a node with only one child.
        """
        # 找到当前节点的父类通过父类进行删除
        par_node = node.parent
        #  判断当要删除的值是root的时候
        if node.key == self.Root.key:
            # 如果节点存在节点, 那就把右节点替换当前节点
            if node.right:
                self.Root = node.right
                node.right = None
            # 如果当前节点没有右节点,那就把当前节点替换为自己的左节点, 因为只有一个节点
            # 因为这是只有一个节点情况没有有肯定有左
            else:
                self.Root = node.left
                node.left = None
        # 如果当前节点不是root
        else:
            # 如果是父节点的右节点
            if par_node.right == node:
                if node.right:
                    # 对于父节点重新指向,指向当前的右节点, 删除节点
                    par_node.right = node.right
                    # 对于当前节点的右节点父节点重新指向
                    par_node.right.parent = par_node
                    node.right = None
                else:
                    par_node.right = node.left
                    par_node.right.parent = par_node
                    node.left = None
            # 如果是父节点的左节点
            else:

                if node.right:
                    par_node.left = node.right
                    par_node.left.parent = par_node
                    node.right = None
                else:
                    par_node.left = node.left
                    par_node.left.parent = par_node
                    node.left = None

        del node

    def _switch_nodes(self, node1, node2):
        """
        T._switch_nodes(node1,node2). Switches positions
        of node1 and node2 in T.
        """
        switch1 = node1
        switch2 = node2
        temp_key = switch1.key
        temp_value = switch1.value
        # 如果当前值为 root的话
        if switch1.key == self.Root.key:
            # 把root的key改为最大的key
            self.Root.key = node2.key
            # 把root的value改为最大的value
            self.Root.value = node2.value
            # 把临时的key 赋给最大值的key
            switch2.key = temp_key
            # 把临时的value 赋给最大值的value
            switch2.value = temp_value
        # 如果最大值为 root的话
        elif switch2.key == self.Root.key:
            switch1.key = self.Root.key
            self.Root.key = temp_key
            self.Root.value = temp_value
        # 当前值和最大值都不是root, 将两个值进行替换
        else:
            switch1.key = node2.key
            switch1.value = node2.value
            switch2.key = temp_key
            switch2.value = temp_value

    def _delete_node(self, node):
        """
        T._delete_node(node). Deletes node from T, treating it as
        a node with two children.
        """
        # 如果左子树高度大于右子树
        if self.get_height(node.left) > self.get_height(node.right):
            # 获取最大的子节点
            to_switch = self.get_max(node.left)
            # 将当前要删掉的 node 金额 最大值进行位置调换
            self._switch_nodes(node, to_switch)
            # 当当前值没有左右子的时候
            if not (to_switch.right or to_switch.left):
                to_delete = self.get_max(node.left)
                self._delete_leaf(to_delete)
            else:
                to_delete = self.get_max(node.left)
                self._delete_leaf_parent(to_delete)
        else:
            to_switch = self.get_min(node.right)
            self._switch_nodes(node, to_switch)

            if not (to_switch.right or to_switch.left):
                to_delete = self.get_min(node.right)
                self._delete_leaf(to_delete)
            else:
                to_delete = self.get_min(node.right)
                self._delete_leaf_parent(to_delete)

    def delete(self, key):
        """T.delete(key) <==> del T[key]. Deletes the node
        with key attribute key from T.
        """
        # 判断是否存在要删除的节点
        print(f"开始删除,删除前要删除的key: {key}")
        node = self.get_node(key, self.Root)
        # 如果存在再进行删除操作
        if node:
            # 当左右节点都不存在的情况
            if not (node.left or node.right):
                self._delete_leaf(node)
            # 当有一个存在的时候
            elif not (node.left and node.right):
                self._delete_leaf_parent(node)
            # 当左右节点都存在的时候
            else:
                self._delete_node(node)

    def delete_from(self, seq):
        """
        T.delete_from(seq). For every keyin seq, deletes
        the Node with that key attribute from T.
        """
        if isinstance(seq, collections.Iterable):
            for x in seq:
                self.delete(x)
        else:
            raise TypeError(str(iter) + " is not iterable")


if __name__ == '__main__':
    import random
    from draw import plot_tree

    data = [[random.randint(0, 99), random.randint(0, 99)] for item in range(10)]
    tree = BSTree(data)

    for key, value in data:
        tree.delete(key)
        plot_tree(tree)
