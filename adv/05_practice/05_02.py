from functools import wraps

def tracer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print(f"{func.__name__} была вызвана с аргументами {args}{kwargs}")
        return func(*args, **kwargs)

    return inner


@tracer
def func(a, b):
    return a + b

func(1, 5)