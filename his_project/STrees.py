from copy import copy

from his_project.BTree import BinaryTree, TreeNode
from his_project.util import random_number
from third_party.pybst.draw import plot_tree


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
        value = data.pop()
        root = TreeNode(value)
        while data:
            value = data.pop()
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
            """具体删除逻辑"""
            # 取出要删除的节点的父节点
            parent_tag, parent = self.get_father_son(current_node)

            # 如果存左右节点都存在的情况
            if current_node.left and current_node.right:
                # 获取左右元素那个元素多删除那边
                left_count = self.get_element_count(current_node.left)
                right_count = self.get_element_count(current_node.right)
                # 如果左边大于右边, 取左边最大值进行替换,为了保持搜索树特性
                if left_count >= right_count:
                    largest_element = self.max(current_node.left)
                # 如果右边数目多,那就取右边最小值进行替换,为了保持搜索树特性
                else:
                    largest_element = self.min(current_node.right)
                # 当前节点的值和最大值进行替换
                self._switch_nodes(current_node, largest_element)
                # 删除操作
                processing_to_delete(largest_element)
                return current_node
            # 如果要删除的节点存在左节点但是不存在有节点, 就将左节点的值向上移
            elif current_node.left and not current_node.right:
                current_node = current_node.left
            # 如果要删除的节点存在有节点但是不存在左节点,那就把右节点的值向上移
            elif not current_node.left and current_node.right:
                current_node = current_node.right
            # 如果被删除的节点左右子树都不存在那就直接清除
            elif not current_node.left and not current_node.right:
                current_node = None

            # 将父节点对值进行重新绑定
            if parent is not None:
                # 父和子绑定是双向的所以需要双向重新绑定
                setattr(parent, parent_tag, current_node)
                if current_node is not None:
                    current_node.parent = parent
            else:
                if current_node is not None:
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
    _data = random_number(is_generator=False, length=10, max_value=100)
    # _data = {70, 37, 51, 93, 59}
    tree = SearchTrees.recursive_build(data=_data)
    # print(_data)
    plot_tree(tree)
    # for item in _data:
    #     if tree.Root:
    #         tree.delete(item)
