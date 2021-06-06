from functools import wraps


def protect_iteration(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if not self.is_iter:
            raise ValueError
        return func(*args, **kwargs)
    return wrapper