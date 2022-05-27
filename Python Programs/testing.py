try:
    from my_decorators import export
except ImportError:
    def export(func: callable):
        import sys as _sys
        mod = _sys.modules[func.__module__]
        if hasattr(mod, '__all__'):
            mod.__all__.append(func.__name__)
        else:
            mod.__all__ = [func.__name__]
        return func

import functools


def _equals(x: object, y: object, strict: bool = False):
    def _dict_equals(_x: object, _y: object, strict: bool):
        _keys_x, _keys_y = _x.keys(), _y.keys()
        if not strict:
            _keys_x, _keys_y = sorted(_keys_x), sorted(_keys_y)
        if not _keys_x == _keys_y:
            return False
        return all([_equals(_x[_], _y[_], strict) for _ in _keys_x])

    def _iterable_equals(_x: object, _y: object, strict: bool):
        if not len(_x) == len(_y):
            return False
        return all([_equals(_1, _2, strict) for _1, _2 in zip(_x, _y)])

    try:
        assert isinstance(x, type(y))
    except AssertionError:
        return False

    try:
        assert isinstance(x, str)
        return x == y if not strict else x is y
    except AssertionError:
        pass

    try:
        assert isinstance(x, dict)
        return _dict_equals(x, y, strict)
    except AssertionError:
        pass

    try:
        _1, _2 = list(iter(x)), list(iter(y))
        if not strict:
            _1, _2 = sorted(_1), sorted(_2)
        return _iterable_equals(_1, _2, strict)
    except TypeError:
        pass

    return x is y if strict else x == y


@export
def describe(msg: str = ''):
    def decorator(func: callable):
        print(msg)
        return func
    return decorator


@export
def assert_equals(expected: object, *args: tuple[object], alternate: tuple = (),
                  strict: bool = False, **kwargs: dict[object]):
    '''
    Strict mode enables checking for equality using `is` instead of `==`
    The order of dictionaries and iterables are considered in strict mode.
    '''
    def decorator(func: callable):
        nonlocal expected, strict, alternate
        print()
        actual = func(*args, **kwargs)
        eq = _equals(expected, actual, strict)
        try:
            assert isinstance(alternate, tuple)
            alternate = list(alternate)
        except AssertionError:
            alternate = [alternate]
        while not eq and len(alternate) > 0:
            eq = _equals(_ := alternate.pop(), actual, strict)
            expected = _
        print(f'{func.__name__} {"passed ✅" if eq else "FAILED ❌"} ({args= }',
              f'{kwargs= }). Expected: {expected} | Actual: {actual} ({strict=})')
        print()
        return func
    return decorator

# Example Usage
if __name__ == '__main__':
    @assert_equals(26, 12, 2, strict=True)
    @assert_equals(18, 3, 6)
    @assert_equals(15, 5, 3)
    @describe('Testing multiplication of two numbers')
    def mult(a, b):
        return a * b
