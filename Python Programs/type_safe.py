from functools import wraps
from inspect import getfullargspec


def type_safe(func: callable):
    '''
    This decorator ensures type safety over type annotated functions
    '''
    # Argument inspection
    specs = getfullargspec(func)
    
    # Function to get items from the annotation dictionary
    # annotations is actually the callable `get` method of a dict object
    annotations = specs.annotations.get

    # Keyword argument filter
    kw_filter = lambda y: lambda x: x not in y

    def validate_types(*args: tuple[tuple]):
        '''
        Validates the types from the tuples in args
        '''
        # List of type errors, to show all errors at once
        errors = []
        
        # Iterating over args and validating each component
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
            # Error Message formatting
            max_l = [max(map(lambda x: len(x[i]), errors)) for i in range(3)]
            r = lambda x, i: x + ' ' * (max_l[i] - len(x))
            errors = map(lambda x: (r(x[0], 0), r(x[1], 1), r(x[2], 2),), errors)
            errors = '\n'.join(map(lambda x: ' '.join(x), errors))
            
            # Raising a TypeError with the formatted error message
            raise TypeError(
                f'Function <{func.__qualname__}> invoked with incorrect types\n'
                f'{"-" * (sum(max_l) + 2)}\n'
                f"{errors}\n"
                f'{"-" * (sum(max_l) + 2)}\n'
            )

    @wraps(func)
    def wrapper(*args, **kwargs):
        '''
        Wrapper Function over `func` to provide type safety checks
        '''
        # Validate the positional arguments
        validate_types(*zip(filter(kw_filter(kwargs), specs.args), args))

        # Validate the keyword argument
        validate_types(kwargs.items())

        # Calculate the result of func
        result = func(*args, **kwargs)
        
        # Validate the return type
        validate_types(('return', result, ))

        # Return the result
        return result

    # Return wrapper function
    return wrapper
