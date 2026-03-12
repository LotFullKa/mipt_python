"""
Задача 1: Дескриптор Validator

Дескриптор, который проверяет на соответствие типу, переданному в init.
"""


class Validator:
    """Дескриптор для валидации типа значения."""
    
    def __init__(self, expected_type):
        self.expected_type = expected_type
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = f"_{name}"
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name, None)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"Expected {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        setattr(instance, self.name, value)


class Integer(Validator):
    """Дескриптор для валидации целых чисел."""
    
    def __init__(self):
        super().__init__(int)


# Примеры использования
if __name__ == "__main__":
    class Person:
        age = Integer()
        
        def __init__(self, age):
            self.age = age
    
    # Корректное использование
    person = Person(25)
    print(f"Age: {person.age}")  # Age: 25
    
    person.age = 30
    print(f"Updated age: {person.age}")  # Updated age: 30
    
    # Попытка установить неверный тип
    try:
        person.age = "thirty"
    except TypeError as e:
        print(f"Error: {e}")  # Error: Expected int, got str
    
    # Еще один пример с несколькими дескрипторами
    class String(Validator):
        def __init__(self):
            super().__init__(str)
    
    class Float(Validator):
        def __init__(self):
            super().__init__(float)
    
    class Product:
        name = String()
        price = Float()
        quantity = Integer()
        
        def __init__(self, name, price, quantity):
            self.name = name
            self.price = price
            self.quantity = quantity
        
        def __repr__(self):
            return f"Product(name={self.name}, price={self.price}, quantity={self.quantity})"
    
    # Корректное использование
    product = Product("Laptop", 999.99, 5)
    print(product)  # Product(name=Laptop, price=999.99, quantity=5)
    
    # Попытка установить неверные типы
    try:
        product.price = "expensive"
    except TypeError as e:
        print(f"Error: {e}")  # Error: Expected float, got str
    
    try:
        product.quantity = 10.5
    except TypeError as e:
        print(f"Error: {e}")  # Error: Expected int, got float
