from inspect import signature
from typing import List, Dict


def parameter_calibration(func):
    """
    参数校验, 通过声明的显式格式来进行校验

    example:
        @parameter_calibration
        def function(b: str, c: list):
            pass

        if __name__ == '__main__':
            function(1, [1, 2])

    output:
        TypeError: Argument b must be <class 'str'>
    """

    def wrapper(*args, **kwargs):
        sig = signature(func)
        bound_types = sig.parameters
        parameter = sig.bind(*args, **kwargs).arguments.items()
        for item, value in parameter:
            _type = bound_types.get(item).annotation
            print(_type)
            if not isinstance(value, _type):
                raise TypeError(f'Argument {item} must be {_type}')
        return func(*args, **kwargs)

    return wrapper
