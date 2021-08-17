from time import perf_counter as pc
from os import getpid
from psutil import Process


def cur_mem():
    return Process(getpid()).memory_info().rss / 1024


def track_time(func):
    def wrapper(*args, **kwargs):
        start = pc()
        result = func(*args, **kwargs)
        print(f'\nTime Taken by {func.__name__}:\t\t {pc() - start} seconds\n')
        return result
    return wrapper


def track_memory(func):
    def wrapper(*args, **kwargs):
        start = cur_mem()
        result = func(*args, **kwargs)
        print(f'\nMemory Used by {func.__name__}:\t\t {cur_mem() - start} Mb\n')
        return result
    return wrapper


def track_memory_and_time(func):
    def wrapper(*args, **kwargs):
        start_memory = cur_mem()
        start_time = pc()
        result = func(*args, **kwargs)
        print(f'\nMemory Used by {func.__name__}:\t\t {cur_mem() - start_memory} Mb\n')
        print(f'\nTime Taken by {func.__name__}:\t\t {pc() - start_time} seconds\n')
        return result
    return wrapper


def method_call_counter(func):
    '''
    The counter can be accessed using func.counter
    '''
    def wrapper(*args, **kwargs):
        wrapper._counter += 1
        wrapper.counter = f'Function {func.__qualname__} was called:\t\t {wrapper._counter} times'
        return func(*args, **kwargs)
    wrapper._counter = 0
    wrapper.counter = ''
    return wrapper
