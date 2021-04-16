class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.left = None


class SinglyLinkedList:
    """
    单向链表, 先进先出
    example:
        lis = SinglyLinkedList()
        lis.add(1)
        lis.add("2")
        lis.add(True)
        lis.add({1, 2, 3})
        lis.add([12, 34, 56])
        print(lis)
        for item in lis:
            print(item)
    output:
        <SinglyLinkedList [1, '2', True, {1, 2, 3}, [12, 34, 56]]>
        1
        2
        True
        {1, 2, 3}
        [12, 34, 56]
    """

    def __init__(self):
        self._last_obj = None
        self._first_obj = None
        self._current = None
        self._count = 0
        self._current_next = None

    def __len__(self):
        return self._count

    def add(self, x):
        node = ListNode(x)
        if self._current:
            self._current.next = node
        else:
            self._first_obj = node
            self._current_next = node
        self._current = node
        self._last_obj = node
        self._count += 1

    def pop(self):
        if self._first_obj:
            val = self._first_obj.val
            self._count -= 1
            if self._first_obj.next:
                self._first_obj = self._first_obj.next
            else:
                self.__init__()
            return val

    def get_iter(self):
        _current_next = self._current_next
        while _current_next.next:
            yield _current_next.val
            _current_next = _current_next.next
        yield _current_next.val


    def __next__(self):
        """链表迭代器先入先出, 可重复迭代"""
        current_next = self._current_next
        if current_next:
            self._current_next = self._current_next.next
            return current_next.val
        self._current_next = self._first_obj
        raise StopIteration()

    def __iter__(self):
        return self

    def __str__(self):
        current = self._first_obj
        node_list = []
        while current.next:
            node_list.append(current.val)
            current = current.next
        node_list.append(current.val)
        return f"<SinglyLinkedList {node_list}>"


class DoubleLinkedList:
    """
    双向链表
    example:
         dll = DoubleLinkedList()
        dll.leftadd("1")
        dll.leftadd("2")
        dll.rightadd("2")
        dll.rightadd("2")
        for item in dll:
            print("item: ", item)
        print("len: ", len(dll))
        print(dll.leftpop())
        print("len: ", len(dll))
        print(dll.leftpop())
        print("len: ", len(dll))
        print(dll.leftpop())
        print(dll.rightpop())
        print(dll.rightpop())
    output:
        item:  2
        item:  1
        item:  2
        item:  2
        len:  4
        2
        len:  3
        1
        len:  2
        2
        2
        None
    """

    def __init__(self):
        self._last_obj = None
        self._first_obj = None
        self._current_next = None
        self._count = 0

    def __len__(self):
        return self._count

    def leftadd(self, x):
        node = ListNode(x)
        if self._count:
            node.next = self._first_obj
            self._first_obj.left = node
            self._first_obj = node
            self._current_next = node
        else:
            self._first_obj = node
            self._last_obj = node
            self._current_next = node
        self._count += 1

    def rightadd(self, x):
        node = ListNode(x)
        if self._count:
            node.left = self._last_obj
            self._last_obj.next = node
            self._last_obj = node
        else:
            self._first_obj = node
            self._last_obj = node
            self._current_next = node
        self._count += 1

    def leftpop(self):
        if self._first_obj:
            val = self._first_obj.val
            self._count -= 1
            if self._first_obj.next:
                self._first_obj = self._first_obj.next
                self._first_obj.left = None
            else:
                self.__init__()
            return val

    def rightpop(self):
        if self._last_obj:
            val = self._last_obj.val
            self._count -= 1
            if self._last_obj.left:
                self._last_obj = self._last_obj.left
                self._last_obj.next = None
            else:
                self.__init__()
            return val

    def get_iter(self):
        _current_next = self._current_next
        while _current_next.next:
            yield _current_next.val
            _current_next = _current_next.next
        yield _current_next.val

    def __next__(self):
        """链表迭代器先入先出, 可重复迭代"""
        _current_next = self._current_next
        if _current_next:
            self._current_next = self._current_next.next
            return _current_next.val
        self._current_next = self._first_obj
        raise StopIteration()

    def __iter__(self):
        return self

    def __str__(self):
        current = self._first_obj
        node_list = []
        while True:
            node_list.append(current.val)
            if not current.next:
                break
            current = current.next
        return f"<DoubleLinkedList {node_list}>"

