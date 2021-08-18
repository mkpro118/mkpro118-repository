from time import perf_counter as pc
from os import getpid
from psutil import Process
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps


def cur_mem():
    return Process(getpid()).memory_info().rss / (1024 ** 2)


def track_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = pc()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e)
        else:
            return result
        finally:
            print(f'\nTime Taken by {func.__name__}:\t\t {pc() - start} seconds')
    return wrapper


def track_memory(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = cur_mem()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e)
        else:
            return result
        finally:
            print(f'\n\nMemory Used by {func.__name__}:\t\t {cur_mem() - start} Mb')
    return wrapper


def track_memory_and_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_memory = cur_mem()
        start_time = pc()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e)
        else:
            return result
        finally:
            print(f'\nMemory Used by {func.__name__}:\t\t {cur_mem() - start_memory} Mb')
            print(f'\nTime Taken by {func.__name__}:\t\t {pc() - start_time} seconds')

    return wrapper


def method_call_counter(func):
    '''
    The counter can be accessed using func.counter
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper._counter += 1
        wrapper.counter = f'\nFunction {func.__qualname__} was called:\t\t {wrapper._counter} times'
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            raise e
        else:
            return result
        finally:
            pass
    wrapper._counter = 0
    wrapper.counter = ''
    return wrapper


def track_total_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = pc()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e)
        else:
            return result
        finally:
            end = pc()
            wrapper.total_time += end - start
            wrapper.total_time_list.append(end - start)

    wrapper.total_time = 0
    wrapper.total_time_list = []
    return wrapper


def multiply_threads(*args, **kwargs):
    threads = int(kwargs.get('threads', 10))

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with ThreadPoolExecutor() as executor:
                try:
                    _ = [executor.submit(func, i) for i in range(1, threads + 1)]
                    for i in as_completed(_):
                        a, b = i.result()
                        print(a, b, sep='\n')
                except Exception as e:
                    raise e
            return
        return wrapper
    return inner
