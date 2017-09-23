from functools import wraps


def call_counter(func):
    @wraps(func)
    def helper(*args, **kwargs):
        helper.calls += 1
        return func(*args, **kwargs)
    helper.calls = 0
    return helper


@call_counter
def less(a, b):
    """
    Determines whether first element is less then the second, and increments the comparison count.
    :param a:
    :param b:
    :return:
    """
    return a < b


@call_counter
def greater(a, b):
    """
    Determines whether first element is bigger then the second, and increments the comparison count.
    :param a:
    :param b:
    :return:
    """
    return a > b
