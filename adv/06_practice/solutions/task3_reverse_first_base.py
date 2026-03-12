"""
Задача 3: Метакласс ReverseFirstBaseMeta

Метакласс, который меняет порядок наследования: самый первый класс становится последним.
"""


class ReverseFirstBaseMeta(type):
    """Метакласс, который меняет порядок наследования."""
    
    def __new__(mcs, name, bases, namespace, **kwargs):
        # Если есть базовые классы, меняем порядок
        if bases:
            # Берем первый класс и перемещаем его в конец
            bases = bases[1:] + (bases[0],)
        
        return super().__new__(mcs, name, bases, namespace, **kwargs)


# Примеры использования
if __name__ == "__main__":
    # Создаем несколько базовых классов
    class A:
        def method(self):
            return "A"
        
        def method_a(self):
            return "from A"
    
    class B:
        def method(self):
            return "B"
        
        def method_b(self):
            return "from B"
    
    class C:
        def method(self):
            return "C"
        
        def method_c(self):
            return "from C"
    
    # Без метакласса: порядок A, B, C
    class NormalClass(A, B, C):
        pass
    
    print("Normal class MRO:")
    print([cls.__name__ for cls in NormalClass.__mro__])
    # ['NormalClass', 'A', 'B', 'C', 'object']
    
    obj_normal = NormalClass()
    print(f"method() returns: {obj_normal.method()}")  # A (первый в списке)
    
    # С метаклассом: порядок меняется на B, C, A
    class ReversedClass(A, B, C, metaclass=ReverseFirstBaseMeta):
        pass
    
    print("\nReversed class MRO:")
    print([cls.__name__ for cls in ReversedClass.__mro__])
    # ['ReversedClass', 'B', 'C', 'A', 'object']
    
    obj_reversed = ReversedClass()
    print(f"method() returns: {obj_reversed.method()}")  # B (теперь первый)
    
    # Более сложный пример
    class X:
        value = "X"
    
    class Y:
        value = "Y"
    
    class Z:
        value = "Z"
    
    class TestNormal(X, Y, Z):
        pass
    
    class TestReversed(X, Y, Z, metaclass=ReverseFirstBaseMeta):
        pass
    
    print(f"\nNormal: {TestNormal.value}")  # X
    print(f"Reversed: {TestReversed.value}")  # Y
    
    # Проверка MRO
    print("\nTestNormal MRO:", [cls.__name__ for cls in TestNormal.__mro__])
    # ['TestNormal', 'X', 'Y', 'Z', 'object']
    
    print("TestReversed MRO:", [cls.__name__ for cls in TestReversed.__mro__])
    # ['TestReversed', 'Y', 'Z', 'X', 'object']
    
    # Пример с методами
    class First:
        def greet(self):
            return "Hello from First"
    
    class Second:
        def greet(self):
            return "Hello from Second"
    
    class Third:
        def greet(self):
            return "Hello from Third"
    
    class Combined(First, Second, Third, metaclass=ReverseFirstBaseMeta):
        pass
    
    combined = Combined()
    print(f"\nCombined.greet(): {combined.greet()}")
    # Hello from Second (First переместился в конец)
