def add_color(func):
    if (func.__name__ != "__init__"):
        raise ValueError("Function is not init")

    def inner(self, *args, **kwargs):
        self.color = "red"
        func(self, *args, **kwargs)
    return inner

    

class Point:
    @add_color
    def __init__(self, x, y):
        self.x = x
        self.y = y


print(Point(1, 2).color)
print(Point.color)