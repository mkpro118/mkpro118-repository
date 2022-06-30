from functools import wraps
from inspect import getfullargspec


def type_safe(func):
    specs = getfullargspec(func)
    annotations = specs.annotations
    annotations = annotations.get

    kw_filter = lambda y: lambda x: x not in y

    def validate_types(*args):
        errors = []
        for req, real in args:
            try:
                assert isinstance(real, annotations(req, object))
            except AssertionError:
                errors.append((
                    f'Required type {annotations(req)}',
                    f"for parameter '{req}'",
                    f", got {type(real)} instead!",
                ))
        if len(errors) > 0:
            max_l = [max(map(lambda x: len(x[i]), errors)) for i in range(3)]
            r = lambda x, i: x + ' ' * (max_l[i] - len(x))
            errors = map(lambda x: (r(x[0], 0), r(x[1], 1), r(x[2], 2),), errors)
            errors = '\n'.join(map(lambda x: ' '.join(x), errors))
            raise TypeError(
                f'Function <{func.__qualname__}> invoked with incorrect types\n'
                f'{"-" * (sum(max_l) + 2)}\n'
                f"{errors}\n"
                f'{"-" * (sum(max_l) + 2)}\n'
            )

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Validate the positional arguments
        validate_types(*zip(filter(kw_filter(kwargs), specs.args), args))

        # Validate the keyword argument
        validate_types(kwargs.items())

        result = func(*args, **kwargs)
        validate_types(('return', result, ))

        return result

    return wrapper
