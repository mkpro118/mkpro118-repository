from time import perf_counter as pc
from os import getpid
from psutil import Process
from concurrent.futures import ThreadPoolExecutor, as_completed


def cur_mem():
    return Process(getpid()).memory_info().rss / (1024 ** 2)


def track_time(func):
    def wrapper(*args, **kwargs):
        start = pc()
        result = func(*args, **kwargs)
        print(f'\nTime Taken by {func.__name__}:\t\t {pc() - start} seconds')
        return result
    return wrapper


def track_memory(func):
    def wrapper(*args, **kwargs):
        start = cur_mem()
        result = func(*args, **kwargs)
        print(f'\n\nMemory Used by {func.__name__}:\t\t {cur_mem() - start} Mb')
        return result
    return wrapper


def track_memory_and_time(func):
    def wrapper(*args, **kwargs):
        start_memory = cur_mem()
        start_time = pc()
        result = func(*args, **kwargs)
        print(f'\nMemory Used by {func.__name__}:\t\t {cur_mem() - start_memory} Mb')
        print(f'\nTime Taken by {func.__name__}:\t\t {pc() - start_time} seconds')
        return result
    return wrapper


def method_call_counter(func):
    '''
    The counter can be accessed using func.counter
    '''
    def wrapper(*args, **kwargs):
        wrapper._counter += 1
        wrapper.counter = f'\nFunction {func.__qualname__} was called:\t\t {wrapper._counter} times'
        return func(*args, **kwargs)
    wrapper._counter = 0
    wrapper.counter = ''
    return wrapper


def track_total_time(func):
    def wrapper(*args, **kwargs):
        start = pc()
        result = func(*args, **kwargs)
        end = pc()
        wrapper.total_time += end - start
        wrapper.total_time_list.append(end - start)
        return result
    wrapper.total_time = 0
    wrapper.total_time_list = []
    return wrapper


def multiply_threads(*args, **kwargs):
    threads = int(kwargs.get('threads', 10))

    def inner(func):
        def wrapper(*args, **kwargs):
            with ThreadPoolExecutor() as executor:
                _ = [executor.submit(func, i) for i in range(1, threads + 1)]
                for i in as_completed(_):
                    a, b = i.result()
                    print(a, b, sep='\n')
            return
        return wrapper
    return inner
