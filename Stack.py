class Stack(list):
    """Python 中可以使用 列表来表示栈"""
    def get_iter(self):
        for item in self:
            yield item
