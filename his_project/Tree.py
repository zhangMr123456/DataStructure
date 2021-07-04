from typing import List, Dict
from copy import copy
from his_project.util import random_number
from third_party.pybst.draw import plot_tree


class TreeNode:
    """树节点"""

    def __init__(self, key, left=None, right=None, data=None, parent=None):
        self.key, self.left, self.right, self.data, self.parent = key, left, right, data, parent


class BinaryTree:
    """二叉树"""

    def __init__(self, root):
        self.Root = root
        self._temp = None

    def left_sequence_traversal(self):
        """左序遍历"""
        val_list, stack = [], [self.Root]
        while stack:
            node = stack.pop()
            while node:
                val_list.append({node.key: node.data})
                if node.right:
                    stack.append(node.right)
                node = node.left
        return val_list

    def right_sequence_traversal(self):
        """右序遍历"""
        val_list, stack = [], [self.Root]
        while stack:
            node = stack.pop()
            while node:
                val_list.append({node.key: node.data})
                if node.left:
                    stack.append(node.left)
                node = node.right
        return val_list

    def in_sequence_traversal(self):
        """中序遍历"""
        pass

    def sequence_traversal(self):
        """层序遍历"""
        val_list, stack = [], [self.Root]
        while stack:
            node = stack.pop()
            val_list.append({node.key: node.data})
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return val_list

    def get_element_count(self, *args):
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

    @classmethod
    def build_from(cls, data: List[Dict[str, object]]) -> object:
        """
        :param data: 数据
            example: [{'oneself': 'A', 'left': 'B', 'right': 'C', 'is_root': True, "data": {}}, ...]
        :return: 所有节点的值
        """
        node_list, root_node = {}, None
        for node in data:
            key = node["oneself"]
            node_list[key] = TreeNode(key=key)
            node_list[key].data = node["data"]
        for node in data:
            key, left, right, root = node["oneself"], node["left"], node["right"], node["is_root"]
            node_list[key].left = node_list.get(left, None)
            node_list[key].right = node_list.get(right, None)
            if root:
                root_node = node_list[key]
        return cls(root_node)


class SearchTrees(BinaryTree):
    """二叉查找树

    规则:
        若左子树不空，则左子树上所有结点的值均小于或等于它的根结点的值
        若右子树不空，则右子树上所有结点的值均大于它的根结点的值
        左、右子树也分别为二叉排序树
    """

    @classmethod
    def build_from(cls, data: list) -> object:
        """
        :param data: 数据
            example: [1, 2, 3, 4, 5, 6]
        :return: 搜索树对象
        """
        value = data.pop(0)
        root = TreeNode(key=value)

        while data:
            value = data.pop(0)
            stack = [root]

            while stack:
                node = stack.pop(0)
                if node.left:
                    stack.append(node.left)
                else:
                    if value < node.key:
                        node.left = TreeNode(key=value, parent=node)
                        break

                if node.right:
                    stack.append(node.right)
                else:
                    if value > node.key:
                        node.right = TreeNode(key=value, parent=node)
                        break
        return cls(root)

    def search(self, k):
        """搜索树根据给出的值进行搜索

        :param k: 需要搜索的值
        :return: TreeNode
        """
        starting_node = copy(self.Root)
        while starting_node and starting_node.key != k:
            if starting_node.key > k:
                starting_node = starting_node.left
            else:
                starting_node = starting_node.right
        return starting_node

    def min(self, node=None):
        """获取二叉搜索树中的最小值

        :return: TreeNode
        """
        if node is None:
            node = self.Root
        while node.left:
            node = node.left
        return node

    def max(self, node=None) -> object:
        """获取二叉搜索树中的最大值

        :return: TreeNode
        """
        if node is None:
            node = self.Root
        while node.right:
            node = node.right
        return node

    @classmethod
    def recursive_build(cls, data: set) -> object:
        data = list(data)
        value = data.pop(0)
        root = TreeNode(value)
        while data:
            value = data.pop(0)
            root = cls.insert(root=root, key=value, parent=None)
        return cls(root)

    @staticmethod
    def insert(root, key: int, parent):
        new_t = TreeNode(key, parent=parent)
        if root is None:
            root = new_t
        else:
            if key < root.key:
                root.left = SearchTrees.insert(root.left, key, root)
            elif key > root.key:
                root.right = SearchTrees.insert(root.right, key, root)
        return root

    def _switch_nodes(self, node1, node2):
        """
        :param node1: 需要替换的 Node1
        :param node2: 被替换的 Node2
        :return: None
        """
        node2.key, node1.key, = node1.key, node2.key
        # 判断当值1为root的时候, 处理父级情况
        if node1.key == self.Root.key:
            node1.parent = node2.parent
        # 判断当值2为Root的时候
        elif node2.key == self.Root.key:
            node2.parent = node1.parent
        else:
            node2.parent, node1.parent = node1.parent, node2.parent

    def get_father_son(self, node):
        """获取父子关系"""
        parent = node.parent
        if parent is None:
            return None, None
        if parent.left == node:
            return "left", parent
        else:
            return "right", parent

    def delete(self, value):
        """
        :param value:  需要删除的值
        :return: 返回 root 对象

        删除二叉搜索树的时候分为几种情况:

        - 当左右子树都不存在的情况
            直接删除

        - 当之后一个子树存在的情况
            把那一个子树网上移一层,覆盖(等同于删除)掉要删除的节点

        - 当左右节点都存在的情况
            1. 判断要删除的节点的左右字数谁的节点多,那边节点多找那边替补(用于平衡二叉树)
            2. 节点多的那边取最大值, 和要删除值进行替换(替换删除的方法,比节点上移的方式操作节点更少,更快)
            3. 取得的最大值和要删除的节点进行位置替换(替换的作用就是将要删除的节点转化为只有一个子节点(或者没有子节点)的节点进行删除操作)
            4. 替换完之后删除替换后的(之前要删除的节点),如果这个节点有子树或者无子树都按照前两种情况进行删除了
        """
        node_list = [self.Root]

        def processing_to_delete(current_node):
            parent_tag, parent = self.get_father_son(current_node)

            if current_node.left and current_node.right:
                left_count = self.get_element_count(current_node.left)
                right_count = self.get_element_count(current_node.right)
                if left_count >= right_count:
                    largest_element = self.max(current_node.left)
                else:
                    largest_element = self.min(current_node.right)
                # 需要替换的值和最大值进行替换
                self._switch_nodes(current_node, largest_element)
                processing_to_delete(largest_element)
                return current_node

            elif current_node.left and not current_node.right:
                current_node = current_node.left

            elif not current_node.left and current_node.right:
                current_node = current_node.right

            elif not current_node.left and not current_node.right:
                current_node = None

            if parent is not None:
                # 父和子绑定是双向的所以需要双向重新绑定
                setattr(parent, parent_tag, current_node)
                if current_node is not None:
                    current_node.parent = parent
            else:
                current_node.parent = None
            return current_node

        # 判断当删除节点为Root的时候
        if self.Root.key == value:
            self.Root = processing_to_delete(self.Root)
            return

        while node_list:
            node = node_list.pop(0)
            if node.left:
                if node.left.key == value:
                    node.left = processing_to_delete(node.left)
                    return
                node_list.append(node.left)
            if node.right:
                if node.right.key == value:
                    node.right = processing_to_delete(node.right)
                    return
                node_list.append(node.right)


if __name__ == '__main__':
    """
    删除左子树有右子树的情况出问题
    删除右子树有左子树的情况直接删掉
    """
    # _data = random_number(is_generator=False, length=10, max_value=100)
    _data = [6, 46, 17, 24, 26, 29, 79, 63, 86, 89]
    tree = SearchTrees.recursive_build(data=set(_data))
    plot_tree(tree)
    for item in _data:
        if item == 46:
            print(item)
        tree.delete(item)
        plot_tree(tree)
        # a = tree.sequence_traversal()
        # print(f"删除{item},当前长度{len(a)},当前剩余{a}")
