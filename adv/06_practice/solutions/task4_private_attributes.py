"""
Задача 4: Метакласс для приватных атрибутов

Метакласс, который делает все атрибуты приватными, 
а уже приватные оставляет такими, какие они есть.
"""


class PrivateAttributesMeta(type):
    """Метакласс, который делает все атрибуты приватными."""
    
    def __new__(mcs, name, bases, namespace, **kwargs):
        new_namespace = {}
        
        for attr_name, attr_value in namespace.items():
            # Специальные методы (__init__, __str__ и т.д.) не трогаем
            if attr_name.startswith('__') and attr_name.endswith('__'):
                new_namespace[attr_name] = attr_value
            # Уже приватные атрибуты (начинаются с _) оставляем как есть
            elif attr_name.startswith('_'):
                new_namespace[attr_name] = attr_value
            # Публичные атрибуты делаем приватными
            else:
                new_namespace[f'_{attr_name}'] = attr_value
        
        return super().__new__(mcs, name, bases, new_namespace, **kwargs)


# Примеры использования
if __name__ == "__main__":
    # Пример 1: Базовый класс с метаклассом
    class MyClass(metaclass=PrivateAttributesMeta):
        public_attr = "I should be private"
        _already_private = "I stay private"
        __special__ = "I stay special"
        
        def public_method(self):
            return "This method becomes private"
        
        def _private_method(self):
            return "This stays private"
    
    # Проверяем атрибуты
    print("Attributes of MyClass:")
    for attr in dir(MyClass):
        if not attr.startswith('__') or attr.endswith('__'):
            print(f"  {attr}")
    
    # Публичные атрибуты стали приватными
    print(f"\nHas '_public_attr': {hasattr(MyClass, '_public_attr')}")  # True
    print(f"Has 'public_attr': {hasattr(MyClass, 'public_attr')}")  # False
    
    print(f"Has '_public_method': {hasattr(MyClass, '_public_method')}")  # True
    print(f"Has 'public_method': {hasattr(MyClass, 'public_method')}")  # False
    
    # Уже приватные остались приватными
    print(f"Has '_already_private': {hasattr(MyClass, '_already_private')}")  # True
    print(f"Has '_private_method': {hasattr(MyClass, '_private_method')}")  # True
    
    # Пример 2: Класс с различными типами атрибутов
    class Person(metaclass=PrivateAttributesMeta):
        name = "John"  # станет _name
        age = 30  # станет _age
        _salary = 50000  # останется _salary
        __doc__ = "Person class"  # останется __doc__
        
        def get_info(self):  # станет _get_info
            return f"{self._name}, {self._age}"
        
        def _calculate_tax(self):  # останется _calculate_tax
            return self._salary * 0.13
    
    print("\n\nPerson class attributes:")
    person_attrs = [attr for attr in dir(Person) if not attr.startswith('__')]
    for attr in person_attrs:
        print(f"  {attr}")
    
    # Создаем экземпляр
    person = Person()
    
    # Доступ к атрибутам через приватные имена
    print(f"\nAccessing _name: {Person._name}")  # John
    print(f"Accessing _age: {Person._age}")  # 30
    print(f"Accessing _salary: {Person._salary}")  # 50000
    
    # Пример 3: Класс с методами
    class Calculator(metaclass=PrivateAttributesMeta):
        pi = 3.14159  # станет _pi
        
        def add(self, a, b):  # станет _add
            return a + b
        
        def multiply(self, a, b):  # станет _multiply
            return a * b
        
        def _internal_compute(self, x):  # останется _internal_compute
            return x * self._pi
    
    calc = Calculator()
    
    print("\n\nCalculator methods:")
    print(f"Has '_add': {hasattr(calc, '_add')}")  # True
    print(f"Has 'add': {hasattr(calc, 'add')}")  # False
    
    # Вызываем приватные методы
    result = calc._add(5, 3)
    print(f"calc._add(5, 3) = {result}")  # 8
    
    result = calc._multiply(4, 7)
    print(f"calc._multiply(4, 7) = {result}")  # 28
    
    result = calc._internal_compute(2)
    print(f"calc._internal_compute(2) = {result:.5f}")  # 6.28318
    
    # Пример 4: Проверка, что специальные методы не затронуты
    class SpecialMethods(metaclass=PrivateAttributesMeta):
        value = 42  # станет _value
        
        def __init__(self, x):  # останется __init__
            self.x = x  # атрибут экземпляра
        
        def __str__(self):  # останется __str__
            return f"SpecialMethods({self.x})"
        
        def __repr__(self):  # останется __repr__
            return f"SpecialMethods(x={self.x})"
    
    obj = SpecialMethods(100)
    print(f"\n\nSpecialMethods object: {obj}")  # Работает __str__
    print(f"repr: {repr(obj)}")  # Работает __repr__
    print(f"Class _value: {SpecialMethods._value}")  # 42
