from functools import wraps
from my_decorators import export


def _equals(x, y, strict=False):
    def _dict_equals(_x, _y, strict):
        _keys_x, _keys_y = _x.keys(), _y.keys()
        if not strict:
            _keys_x, _keys_y = sorted(_keys_x), sorted(_keys_y)
        if not _keys_x == _keys_y:
            return False
        return all([_equals(_x[_], _y[_], strict) for _ in _keys_x])

    def _iterable_equals(_x, _y, strict):
        if not len(_x) == len(_y):
            return False
        return all([_equals(_1, _2, strict) for _1, _2 in zip(_x, _y)])

    try:
        assert type(x) == type(y)
    except AssertionError:
        return False

    try:
        assert type(x) is dict
    except AssertionError:
        pass
    else:
        return _dict_equals(x, y, strict)

    try:
        _1, _2 = list(iter(x)), list(iter(y))
        if not strict:
            _1, _2 = sorted(_1), sorted(_2)
    except TypeError:
        pass
    else:
        return _iterable_equals(_1, _2, strict)

    return x is y if strict else x == y


@export
def describe(msg=''):
    def decorator(func):
        print(msg)
        return func
    return decorator


@export
def assert_equals(expected, *args, strict=False, **kwargs):
    '''
    Strict mode enables checking for equality using `is` instead of `==`
    The order of dictionaries and iterables are considered in strict mode.
    '''
    def decorator(func):
        print()
        actual = func(*args, **kwargs)
        eq = _equals(expected, actual, strict)
        print(f'{func.__name__} {"passed" if eq else "FAILED"} ({args= }',
              f'{kwargs= }). Expected: {expected} | Actual: {actual} ({strict=})')
        print()
        return func
    return decorator


# Example Usage
@assert_equals(26, 13, 2, strict=True)
@assert_equals(18, 3, 6, strict=False)
@assert_equals(15, 5, 3, strict=False)
@describe('Testing multiplication of two numbers')
def mult(a, b):
    return a * b
