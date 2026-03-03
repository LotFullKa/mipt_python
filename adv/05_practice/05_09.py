def singleton(cls):
    instance = {}
    old_new = cls.__new__
    
    def inner(*args, **kwargs):
        if cls in set(instance.keys()):
            return instance[cls]
        instance[cls] = old_new(cls)
        return instance[cls]

    cls.__new__ = inner
    return cls


def singleton2(cls):
    instance = {}
    def inner(*args, **kwargs):
        if cls in set(instance.keys()):
            return instance[cls]
        instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    
    return inner

@singleton2
class Point():
    def __init__(self, value):
        self.value = value

p1 = Point(1)
print(p1.value)
p2 = Point(2)
print(p2.value)
print(p1.value)