from inspect import signature
import random
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

            if not isinstance(value, _type):
                raise TypeError(f'Argument {item} must be {_type}')
        return func(*args, **kwargs)

    return wrapper


def random_number(length=100, is_generator=True, min_value=0, max_value=9999999):
    """一个生成器对象
    :param length: 生成的长度
    :param is_generator: 是否是一个生成器
    :param min_value: 最小值
    :param max_value: 最大值
    :return: Generator or list
    """
    # print(is_generator)
    # if is_generator:
    #     for i in range(length):
    #         yield random.randint(min_value, max_value)
    # else:
    digital_list = []
    for i in range(length):
        digital_list.append(random.randint(min_value, max_value))
    return digital_list
