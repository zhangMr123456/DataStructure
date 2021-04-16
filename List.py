import heapq

class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None

    def __next__(self):
        return self.next


class SinglyLinkedList:
    """单向链表, 先进先出"""

    def __init__(self):
        self._last_obj = None
        self._first_obj = None
        self._current = None
        self.count = 0
        self._current_next = None

    def add(self, x):
        node = ListNode(x)
        if self._current:
            self._current.next = node
        else:
            self._first_obj = node
            self._current_next = node
        self._current = node
        self._last_obj = node

    def pop(self):
        if self._first_obj:
            val = self._first_obj.val
            if self._first_obj.next:
                self._first_obj = self._first_obj.next
            else:
                self._first_obj.val = None
            return val

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
        while True:
            node_list.append(current.val)
            if not current.next:
                break
            current = current.next
        return f"<SinglyLinkedList {node_list}>"


if __name__ == '__main__':
    pass