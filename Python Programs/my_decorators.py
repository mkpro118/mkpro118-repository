class Decorators:
    class Sentinel:
        '''
        Used to instantiate sentinel objects for missing values.
        '''
        pass

    @staticmethod
    def __meta(cls):
        '''
        Defines the __init__ and _run methods for the decorator classes.
        '''
        from asyncio import iscoroutinefunction as _is_async, run as _run

        def _filter_checks(x):
            '''
            Used to filter out the attributes that aren't callable
            or part of the class's magic methods or properties
            '''
            return not any([
                x.startswith('__'),
                callable(cls.__dict__.get(x, None)),
                isinstance(cls.__dict__.get(x, None), property),
            ])

        _attrs = filter(_filter_checks, dir(cls))
        attrs = dict([(i, cls.__dict__[i]) for i in _attrs])

        def __meta_init(self, fn):
            '''
            Defines the __init__ function for classes
            '''
            nonlocal _is_async
            nonlocal _run
            self.fn = fn
            self._async = _is_async(fn)
            self._, self.result = None, None
            self.__name__ = fn.__name__
            (self.__setattr__(key, value) for key, value in attrs.items())

        def __meta_run(self, *args, **kwargs):
            '''
            Defines the _run function for classes
            '''
            self.result = _run(self.fn(*args, **kwargs)) if self._async else self.fn(*args, **kwargs)
        cls.__init__ = __meta_init
        cls._run = __meta_run
        return cls

    def export(fn):
        import sys as _sys
        mod = _sys.modules[fn.__module__]
        if hasattr(mod, '__all__'):
            mod.__all__.append(fn.__name__)
        else:
            mod.__all__ = [fn.__name__]
        return fn

    @staticmethod
    def track_time(func):
        '''
        Tracks the time of execution of any method.
        The method returns a TrackTime object,
        whose __call__ method is used to run the function.
        The object also has an `time` property, which can used to get a
        floating point value in seconds of the time of execution.
        '''
        from time import perf_counter as pc

        @Decorators.__meta
        class TrackTime:
            '''
            Wraps the function in a callable object.
            Objects have a `time` property, which return the time elapsed
            in seconds during the execution of the function.

            Ex:
            >>> @Decorators.track_time
            ... def func():
            ...     from time import sleep
            ...     sleep(2)
            ...
            >>> func()
            func took 2.00575240 seconds to execute
            '''

            def __call__(self, *args, **kwargs):
                self._ = pc()
                self._run(*args, **kwargs)
                self._ = pc() - self._
                print(f'{self.fn.__name__} took {self._:.8f} seconds to execute')
                return self.result

            @property
            def time(self):
                return self._

            @time.setter
            def time(self, value):
                raise ValueError('Cannot Set the time taken by the function to execute')

        return TrackTime(func)

    @staticmethod
    def track_memory(func):
        '''
        Tracks the memory used in the of execution of any method.
        The method returns a TrackMemory object,
        whose __call__ method is used to run the function.
        The object also has an `memory` property, which can used to get a
        floating point value in MB of the memory of execution.
        '''
        from psutil import Process as _Process
        from os import getpid as _getpid

        def _cur_mem():
            '''
            Gets the memory being used at the current moment by the current process.
            Used before and after the execution of the function
            to determine the difference between the memory used before and after,
            which is the memory used by the current function call.
            '''
            return _Process(_getpid()).memory_info().rss / (1024 ** 2)

        @Decorators.__meta
        class TrackMemory:
            '''
            Wraps the function in a callable object.
            Objects have a `memory` property, which returns the memory used
            in MB during the execution of the function

            Ex:
            >>> @Decorators.track_memory
            ... def func():
            ...     x = [None] * int(1e4)
            ...     y = [None] * int(2e3)
            ...     del x
            ...     del y
            ...
            >>> func()
            func used 0.08984375 MB to execute
            '''

            def __call__(self, *args, **kwargs):
                self._ = _cur_mem()
                self._run(*args, **kwargs)
                self._ = _cur_mem() - self._
                print(f'{self.fn.__name__} used {self._:.8f} MB to execute')
                return self.result

            @property
            def memory(self):
                return self._

            @memory.setter
            def memory(self, value):
                raise ValueError('Cannot Set the memory taken by the function to execute')

        return TrackMemory(func)

    @staticmethod
    def method_call_counter(func):
        '''
        Tracks the number of times the function is called
        '''
        @Decorators.__meta
        class MethodCallCounter:
            '''
            Wraps the function in the MethodCallCounter object which
            has a `counter` property which holds the number of calls
            made the the function.
            '''
            ctr = 0

            def __call__(self, *args, **kwargs):
                self.ctr += 1
                self._run(*args, **kwargs)
                return self.result

            @property
            def counter(self):
                return self.ctr

            @counter.setter
            def counter(self, value):
                raise ValueError('Cannot Set the number of executions of the function')

        return MethodCallCounter(func)

    @staticmethod
    def track_individual_time(func):
        '''
        Tracks the time for each individual function call.
        '''
        from time import perf_counter as pc

        @Decorators.__meta
        class TrackIndividualTime:
            '''
            Wraps the function in the TrackIndividualTime object which
            has a `individual_time_list` property, a list containing
            the time of execution of each function call.
            '''
            __ = []

            def __call__(self, *args, **kwargs):
                self._ = pc()
                self._run(*args, **kwargs)
                self._ = pc() - self._
                self.__.append(self._)
                return self.result

            @property
            def individual_time_list(self):
                return self.__

            @individual_time_list.setter
            def individual_time_list(self, value):
                raise ValueError('Cannot Set the time taken by a function call')

        return TrackIndividualTime(func)

    @staticmethod
    def memoize(func):
        '''
        Caches the calculated results of the function according
        to the arguments passed.

        Warning, should not be used on impure functions.
        '''

        @Decorators.__meta
        class Memoize:
            '''
            Wraps the function in the Memoize object which
            has a `cache` property, a dictionary of all cached values,
            and a purge(key=Decorators.Sentinel()) function, which clears
            a particular cache if a key is provided, otherwise clears the
            entire cache of the function.
            '''
            c = {}

            def __call__(self, *args):
                try:
                    return self.c[(args)]
                except KeyError:
                    return self.__missing(args)

            def __missing(self, key):
                self._run(*key)
                self.c[key] = self.result
                return self.c[key]

            def purge(self, key=Decorators.Sentinel()):
                try:
                    return self.c.pop(key)
                except KeyError:
                    self.c.clear()

            @property
            def cache(self):
                return self.cache

        return Memoize(func)

    @staticmethod
    def warn(msg=''):
        '''
        Prints a warning message before executing the function
        '''
        def _warn(func):
            @Decorators.__meta
            class Warn:
                '''
                Wraps the function in the Warn object which prints
                a warning before the execution of the function.
                '''

                def __call__(self, *args, **kwargs):
                    print(f'WARNING: {self.fn.__name__} : {msg}')
                    self._run(*args, **kwargs)
                    return self.result
            return Warn(func)
        return _warn


if __name__ == '__main__':
    @Decorators.track_individual_time
    @Decorators.memoize
    def fact(n):
        if n <= 1:
            return 1
        return n * fact(n - 1)

    @Decorators.warn('This can take a lil while')
    @Decorators.track_time
    def main(n):
        return fact(n)

    print('digits in factorial of 36:', len(f'{main(36)}'))
    print('digits in factorial of 46:', len(f'{main(46)}'))
    print(fact.individual_time_list)
    # main took 0.00017710 seconds to execute
    # digits in factorial of 36: 42
    # main took 0.00001270 seconds to execute
    # digits in factorial of 46: 58
