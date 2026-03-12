class Validator:    
    def __set_name__(self, owner, name):
        self._name = name
        self._owner = owner

    def __init__(self, cls):
        self._cls = cls

    def __set__(self, obj, value):
        if not isinstance(value, self._cls):
            raise TypeError()
        obj.__dict__[self._name] = value

    def __get__(self, instance, owner):
        print("Iamhere")
        return owner.__dict__[self._name]


class Integer(Validator):
    def __init__(self):
        super().__init__(int)


class P:
    val=Integer()


print(P.val)
