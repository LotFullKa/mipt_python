
def color_everyone(cls):
    cls.color = "red"

    def __repr__(self):
        return f"{self.color} {self.__class__.__name__}"

    cls.__repr__ = __repr__
    return cls
        

@color_everyone
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

@color_everyone
class Segment:
    def __init__(self, st, end):
        self.st = st
        self.end = end

print(f"{Segment(1, 2)}")
print(f"{Point(1, 2)}")