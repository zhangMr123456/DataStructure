"""二叉树"""

NODE_LIST = [
    {'oneself': 'A', 'left': 'B', 'right': 'C', 'is_root': True, "data": {}},
    {'oneself': 'B', 'left': 'D', 'right': 'E', 'is_root': False, "data": None},
    {'oneself': 'D', 'left': None, 'right': None, 'is_root': False, "data": (1, 2, 4)},
    {'oneself': 'E', 'left': 'H', 'right': None, 'is_root': False, "data": "654"},
    {'oneself': 'H', 'left': None, 'right': None, 'is_root': False, "data": "1"},
    {'oneself': 'C', 'left': 'F', 'right': 'G', 'is_root': False, "data": "3"},
    {'oneself': 'F', 'left': None, 'right': None, 'is_root': False, "data": "5"},
    {'oneself': 'G', 'left': 'I', 'right': 'J', 'is_root': False, "data": "1"},
    {'oneself': 'I', 'left': None, 'right': None, 'is_root': False, "data": "4"},
    {'oneself': 'J', 'left': None, 'right': None, 'is_root': False, "data": lambda x: x},
]