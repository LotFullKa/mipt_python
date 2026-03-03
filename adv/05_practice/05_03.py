from functools import wraps
from time import sleep

def retry(attempts, delay):
    def outer(func):
        counter = 0
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                nonlocal counter
                counter += 1
                return func(*args, **kwargs)
            except Exception as e:
                if(counter > attempts):
                    raise e
                print(f"Попытка {counter} завершилась неудачей: {e}. Повтор через {delay} сек")
                sleep(delay)
                return inner(*args, **kwargs)
        return inner
    return outer


@retry(5, 2)
def func(a, b):
    raise ValueError("Случайная ошибка")

func(1, 5)