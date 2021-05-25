from util import parameter_calibration
from typing import List, Dict


class TreeNode:
    """树节点"""

    def __init__(self, val):
        self.val, self.left, self.right, self.data = val, None, None, None


class BinaryTree:
    """二叉树"""

    def __init__(self, root):
        self._root = root

    def left_sequence_traversal(self):
        """左序遍历"""
        val_list, stack = [], [self._root]
        while stack:
            node = stack.pop()
            while node:
                val_list.append({node.val: node.data})
                if node.right:
                    stack.append(node.right)
                node = node.left
        return val_list

    def right_sequence_traversal(self):
        """右序遍历"""
        val_list, stack = [], [self._root]
        while stack:
            node = stack.pop()
            while node:
                val_list.append({node.val: node.data})
                if node.left:
                    stack.append(node.left)
                node = node.right
        return val_list

    def in_sequence_traversal(self):
        """中序遍历"""
        pass

    def sequence_traversal(self):
        """层序遍历"""
        val_list, stack = [], [self._root]
        while stack:
            node = stack.pop()
            val_list.append({node.val: node.data})
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return val_list

    @classmethod
    def build_from(cls, data: List[Dict[str, object]]) -> object:
        """
        :param data: 数据
            example: [{'oneself': 'A', 'left': 'B', 'right': 'C', 'is_root': True, "data": {}}, ...]
        :return: 所有节点的值
        """
        node_list, root_node = {}, None
        for node in data:
            val = node["oneself"]
            node_list[val] = TreeNode(val=val)
            node_list[val].data = node["data"]
        for node in data:
            val, left, right, root = node["oneself"], node["left"], node["right"], node["is_root"]
            node_list[val].left = node_list.get(left, None)
            node_list[val].right = node_list.get(right, None)
            if root:
                root_node = node_list[val]
        return cls(root_node)


class SearchTrees:
    """
    二叉查找树

    规则:
        若左子树不空，则左子树上所有结点的值均小于或等于它的根结点的值
        若右子树不空，则右子树上所有结点的值均大于它的根结点的值
        左、右子树也分别为二叉排序树
    """
    def __init__(self, root):
        self._root = root

    @classmethod
    @parameter_calibration
    def build_from(cls, data: List[int]) -> object:
        """
        :param data: 数据
            example: [1, 2, 3, 4, 5, 6]
        :return: 搜索树对象
        """
        pass


if __name__ == '__main__':
    from TestData import NODE_LIST

    binary_tree = BinaryTree.build_from(NODE_LIST)
    print(binary_tree.sequence_traversal())

