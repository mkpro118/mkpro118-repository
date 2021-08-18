from time import perf_counter as pc
from os import getpid
from psutil import Process
from functools import wraps
from asyncio import iscoroutinefunction as is_async


def cur_mem():
    return Process(getpid()).memory_info().rss / (1024 ** 2)


def track_time(func):
    if is_async(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            print(f'INFO:track_time: tracking time of execution of {func.__name__}')
            start = pc()
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                raise e
            else:
                return result
            finally:
                print(f'INFO:track_time: Time Taken by {func.__name__}:\t\t {pc() - start} seconds')
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f'INFO:track_time: tracking time of execution of {func.__name__}')
            start = pc()
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                raise e
            else:
                return result
            finally:
                print(f'INFO:track_time: Time Taken by {func.__name__}:\t\t {pc() - start} seconds')
    return wrapper


def track_memory(func):
    if is_async(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            print(f'INFO:track_memory: tracking memory used in execution of {func.__name__}')
            start = cur_mem()
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                raise e
            else:
                return result
            finally:
                print(f'INFO:track_memory: Memory Used by {func.__name__}:\t\t {cur_mem() - start} Mb')
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f'INFO:track_memory: tracking memory used in execution of {func.__name__}')
            start = cur_mem()
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                raise e
            else:
                return result
            finally:
                print(f'INFO:track_memory: Memory Used by {func.__name__}:\t\t {cur_mem() - start} Mb')
    return wrapper


def method_call_counter(func):
    '''
    The counter can be accessed using func.counter (replace func with your function name)
    '''
    if is_async(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            wrapper._counter += 1
            wrapper.counter = f'Function {func.__qualname__} was called:\t\t {wrapper._counter} times'
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                raise e
            else:
                return result
            finally:
                pass
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper._counter += 1
            wrapper.counter = f'Function {func.__qualname__} was called:\t\t {wrapper._counter} times'
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
    '''
    The total time can be accessed using func.total_time (replace func with your function name)
    The individual time for each call can be accessed as a list using func.total_time_list
    '''
    if is_async(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = pc()
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                raise e
            else:
                return result
            finally:
                end = pc()
                wrapper.total_time += end - start
                wrapper.total_time_list.append(end - start)
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = pc()
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                raise e
            else:
                return result
            finally:
                end = pc()
                wrapper.total_time += end - start
                wrapper.total_time_list.append(end - start)

    wrapper.total_time = 0
    wrapper.total_time_list = []
    return wrapper
