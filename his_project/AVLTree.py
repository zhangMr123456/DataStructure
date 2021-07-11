from his_project.STrees import SearchTrees
from his_project.util import random_number
from third_party.pybst.draw import plot_tree


class AVLTreeNode(object):
    def __init__(self,
                 key,
                 left=None,
                 right=None,
                 data=None,
                 parent=None,
                 height=1,
                 balance=0
                 ):
        """
        :param key: id值,索引值
        :param left: 左节点指向
        :param right: 有节点指向
        :param data: 存储的数据
        :param parent: 父类
        :param height: 当前高度
        :param balance: 平衡因子 = 左子树节点数 - 右字数节点数
        """
        self.key, self.left, self.right, self.data, self.parent, self.height, self.balance = \
            key, left, right, data, parent, height, balance


class AVLTree(SearchTrees):

    def update_height(self, node):
        """更新当前节点高度"""
        node.height = self.get_height(node)
        if node.parent:
            self.update_height(node.parent)

    def update_balance(self, node):
        """更新当前节点的平衡因子"""
        node.balance = (node.left.height if node.left else -1) - (node.right.height if node.right else -1)
        if node.parent:
            self.update_balance(node.parent)

    def insert(self, root, key: int, parent):
        if root is None:
            root = AVLTreeNode(key, parent=parent)
        else:
            if key < root.key:
                root.left = self.insert(root.left, key, root)
            elif key > root.key:
                root.right = self.insert(root.right, key, root)

        self.update_balance(root)
        self.update_height(root)
        return root

    def recursive_build(self, data: set):
        root = AVLTreeNode(data.pop())
        while data:
            value = data.pop()
            root = self.insert(root=root, key=value, parent=None)
        self.Root = root

    def equilibrium_conversion(self, check_node=None):
        if check_node is None:
            # 从最左边开始检查
            check_node = self.min()
        node_list = [check_node]
        while node_list:
            check_node = node_list.pop()
            if abs(check_node.balance) > 1:
                ...
            else:
                node_list.append(check_node.parent)


if __name__ == '__main__':
    lis = random_number(length=15, max_value=20)
    avl = AVLTree()
    avl.recursive_build(lis)
    plot_tree(avl)
