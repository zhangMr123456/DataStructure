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
    tem_node = []

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

    def equilibrium_conversion(self, check_node=None, is_valid=False):
        """旋转操作
        :param check_node: 需要执行旋转的值
        解答思路:
            - 从左到右,从下至上进行检查旋转
            - 检查到平衡因子大于 1 的节点(等于2 或者 -2, 总有一个节点属于)进行旋转
            - 判断属于需要旋转的四种类型中的哪一种,进行分别处理
            - 处理完之后向上检查

        旋转思路:
            - LL类型, 都是左边的,然后向右进行旋转, 注意在 LL 类型旋转的时候值可能不止 3 个
                3            2
               2   旋转     1  3
              1
            - RR类型, 都是在右边然后向左进行旋转, 在 RR 类型旋转的时候值也不止 3 个
              1
               2   旋转      2
                3          1  3
            - LR类型, 先把底部的进行旋转,转化问题类型为 LL 类型,然后再进行旋转
                3           3
               1   旋转     2     旋转     2
                2          1            1  3
            - RL类型, 先把底部的值进行旋转,转化问题类型为 RR 类型,然后再进行旋转
              1            1
               3   旋转     2    旋转      2
              2             3           1  3
            - 拐点类型, 当进行 RR 和 LL 类型的时候, 旋转操作可以携带拐点一起旋转
                 2                1
                1  3    旋转     0  2
               0               -1   3
             -1
            - 阻挠旋转点,类型 再进行 LL 和 RR 类型旋转的时候,有分支阻挠旋转,那么就先将这个值去掉,然后旋转完成之后重新插入
                     4                   2
                  2     6    旋转     1     4
                1  3                0     3   6
              0
              此例过程中 3 阻挠了整体的旋转, 那就先将 3 给拿下来, 然后旋转完成之后再进行插入, 如果 3 也是一个分支操作一样
        """
        if is_valid:
            return
        is_valid = True
        def ll(node):
            node1, node2, node3 = node.left.left, node.left, node
            node1.parent = node2
            node3.parent = node2
            node3.left = None
            node2.left = node1
            if node2.right:
                node2.right.parent = None
                self.tem_node.append(node2.right.key)
            node2.right = node3
            print("ll")
            return node2, node1, node3

        def rr(node):
            node1, node2, node3 = node, node.right, node.right.right
            node1.parent = node2
            node3.parent = node2
            node.right = None
            if node2.left:
                node2.left.parent = None
                self.tem_node.append(node2.left.key)
            node2.left = node1
            node2.right = node3
            print("rr")
            return node2, node1, node3

        def lr(node):
            node1, node2, node3 = node.left, node.left.right, node
            node1.parent = node2
            node3.parent = node2
            node2.left = node1
            node2.right = node3
            print("lr")
            return node2, node1, node3

        def rl(node):
            node1, node2, node3 = node, node.right.left, node.right
            node1.parent = node2
            node3.parent = node2
            node2.left = node1
            node2.right = node3
            print("rl")
            return node2, node1, node3

        def determine(node):
            """判断当前节点属于那种情况"""
            if node.left:
                if node.left.left:
                    return ll(node)
                elif node.left.right:
                    return lr(node)
            elif node.right:
                if node.right.right:
                    return rr(node)
                elif node.right.left:
                    return rl(node)
            raise

        if check_node is None:
            check_node = self.Root
        node_list = [check_node]
        while node_list:
            check_node = node_list.pop()
            if check_node is None:
                print(self.Root)
            if check_node.balance == 2 or check_node.balance == -2:
                tag, parent = self.get_father_son(check_node)
                node, node_left, node_right = determine(check_node)
                # 双向绑定
                if tag is not None:
                    setattr(parent, tag, node)
                    node.parent = parent
                else:
                    node.parent = None
                # 对平衡因子和高度进行更新
                self.update_height(node_left)
                self.update_height(node_right)
                self.update_balance(node_left)
                self.update_balance(node_right)
                is_valid = False
                break
            if check_node.left:
                node_list.append(check_node.left)
            if check_node.right:
                node_list.append(check_node.left)
        plot_tree(self)
        return self.equilibrium_conversion(is_valid=is_valid)


if __name__ == '__main__':
    # lis = random_number(length=15, max_value=20)
    # lis = [8, 2, 1, 11, 17, 16, 2, 14, 15, 18, 17, 1, 18]
    lis = [0, 2, 1, 16, 2, 14, 15, 18, 17]
    avl = AVLTree()
    avl.recursive_build(lis)
    avl.equilibrium_conversion()
    print(avl)