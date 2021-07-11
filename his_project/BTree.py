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

    def __init__(self, root=None):
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

    def get_height(self, *args):
        """获取二叉树高度"""
        if len(args) == 0:
            node = self.Root
        else:
            node = args[0]
        if not node or (node.left is None and node.right is None):
            return 1
        return 1 + max(self.get_height(node.left), self.get_height(node.right))



