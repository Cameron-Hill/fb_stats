import warnings
import functools
import time


def suppress_warnings(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            x = func(*args, **kwargs)
        return x

    return wrapper
    
   
def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("\n*****",func.__name__,"*****\n")
        value = func(*args,**kwargs)
        print("\n*****",func.__name__,"*****\n")
        return value
    return wrapper


def time_this(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper


def raise_on_fail(exception):
    def try_this(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                raise exception
        return wrapper
    return try_this
