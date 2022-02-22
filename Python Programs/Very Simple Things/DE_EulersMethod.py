from functools import wraps


def repeat(count: int = 5, step_size: float = 0.5) -> callable:
    '''
    This is a highly custom decorator.
    Only applicable under this special case.
    '''
    def decorator(func: callable) -> callable:
        @wraps(func)
        def wrapper(f: callable, x0: float, y0: float, /, *, x1: float = None) -> None:
            for _ in range(1, count + 1):
                x1 = x0 + step_size
                y0 = func(f, x0, y0, x1=x1)
                print(f'Steps: {_} / {count} | {x1 = } | {x0 = } | y = {y0}')
                x0 += 0.5
        return wrapper
    return decorator


def f(x: float, y: float) -> float:
    # Change the function as required
    return y - 3 * x


@repeat(count=4, step_size=0.5)  # Change this as required
def y(f: callable, x0: float, y0: float, /, *, x1: float = None) -> float:
    # User do not need to input x1, it's inferred from step size
    # Nothing needs to be changed here
    return f(x0, y0) * (x1 - x0) + y0


if __name__ == '__main__':
    # Change as required
    x0 = 1
    # Change as required
    x1 = 1.5
    # Change as required
    y0 = 0

    # This will auto run all iterations
    y(f, x0, y0)
