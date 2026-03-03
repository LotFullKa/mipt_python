def add_color(func, color):
    if (func.__name__ != "__init__"):
        raise ValueError("Function is not init")

    def inner(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self.color = color
    return inner

def colored(color = "red"):    
    def outer(cls):
        cls.__init__ = add_color(cls.__init__, color)
        return cls
    return outer

@colored("blue")
class Point:
    def __init__(self, x, y, **kwargs):
        self.x = x
        self.y = y


print(Point(1, 2, color="NONE COLOR").color)