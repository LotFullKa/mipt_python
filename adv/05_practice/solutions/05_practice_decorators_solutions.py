"""
Решения задач по декораторам
МФТИ ФПМИ - Практикум Python - Продвинутый Поток
Семинар 5: Декораторы - практика
"""

import time
from functools import wraps


# ============================================================================
# Задача 1. Функция-замыкание get_formula
# ============================================================================

def get_formula(a, b):
    """
    Возвращает функцию, которая вычисляет ax^2 + by^2
    
    Args:
        a: коэффициент при x^2
        b: коэффициент при y^2
    
    Returns:
        Функция, принимающая x и y
    """
    def formula(x, y):
        return a * x**2 + b * y**2
    return formula


# Пример использования:
# f = get_formula(2, 3)
# print(f(1, 2))  # 2*1^2 + 3*2^2 = 2 + 12 = 14


# ============================================================================
# Задача 2. Декоратор trace для трассировки возвращаемого значения
# ============================================================================

def trace(func):
    """
    Декоратор, который выводит информацию о возвращаемом значении функции
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} вернула значение {result}")
        return result
    return wrapper


# Пример использования:
# @trace
# def add(a, b):
#     return a + b
# 
# add(2, 3)  # Выведет: Функция add вернула значение 5


# ============================================================================
# Задача 3. Декоратор retry с повторными попытками
# ============================================================================

def retry(attempts, delay):
    """
    Параметризованный декоратор для повторных попыток выполнения функции
    
    Args:
        attempts: количество попыток
        delay: задержка между попытками в секундах
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < attempts:
                        print(f"Попытка {attempt} завершилась неудачей: {e}. Повтор через {delay} сек...")
                        time.sleep(delay)
            # Если все попытки исчерпаны, выбрасываем последнее исключение
            raise last_exception
        return wrapper
    return decorator


# Пример использования:
# @retry(attempts=3, delay=1)
# def unstable_function():
#     import random
#     if random.random() < 0.7:
#         raise ValueError("Случайная ошибка")
#     return "Успех!"


# ============================================================================
# Задача 4. Регистрация команд с использованием декоратора
# ============================================================================

# Глобальный реестр команд
command_registry = {}


def register_command(func):
    """
    Декоратор для регистрации функций в глобальном реестре команд
    """
    command_registry[func.__name__] = func
    return func


def run_command(name):
    """
    Вызывает зарегистрированную команду по имени
    
    Args:
        name: имя команды
    """
    if name in command_registry:
        return command_registry[name]()
    else:
        raise ValueError(f"Команда '{name}' не найдена в реестре")


# Пример использования:
# @register_command
# def hello():
#     print("Hello, World!")
# 
# @register_command
# def goodbye():
#     print("Goodbye!")
# 
# run_command("hello")  # Выведет: Hello, World!


# ============================================================================
# Классы для задач 5-8
# ============================================================================

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Segment:
    def __init__(self, st, end):
        self.st = st
        self.end = end


# ============================================================================
# Задача 5. Функция color_everyone как декоратор класса
# ============================================================================

def color_everyone(cls):
    """
    Декоратор класса, добавляющий атрибут color и метод __repr__
    """
    # Добавляем атрибут класса
    cls.color = "red"
    
    # Сохраняем оригинальный __repr__, если он есть
    original_repr = cls.__repr__ if hasattr(cls, '__repr__') else None
    
    # Добавляем новый __repr__
    def new_repr(self):
        class_name = self.__class__.__name__.lower()
        return f"{self.__class__.color} {class_name}"
    
    cls.__repr__ = new_repr
    return cls


# Пример использования:
# @color_everyone
# class Triangle:
#     def __init__(self, a, b, c):
#         self.a = a
#         self.b = b
#         self.c = c
# 
# t = Triangle(3, 4, 5)
# print(t)  # red triangle


# ============================================================================
# Задача 6. Декоратор add_color для метода __init__
# ============================================================================

def add_color(init_func):
    """
    Декоратор для __init__, добавляющий атрибут color объектам
    """
    @wraps(init_func)
    def wrapper(self, *args, color="red", **kwargs):
        init_func(self, *args, **kwargs)
        self.color = color
    return wrapper


# Пример использования:
# class Circle:
#     @add_color
#     def __init__(self, radius):
#         self.radius = radius
# 
# c = Circle(5)
# print(c.color)  # red
# c2 = Circle(10, color="blue")
# print(c2.color)  # blue


# ============================================================================
# Задача 7. Декоратор colored для класса (изменяет __init__)
# ============================================================================

def colored(cls):
    """
    Декоратор класса, изменяющий __init__ для добавления атрибута color
    """
    original_init = cls.__init__
    
    @wraps(original_init)
    def new_init(self, *args, color="red", **kwargs):
        original_init(self, *args, **kwargs)
        self.color = color
    
    cls.__init__ = new_init
    return cls


# Пример использования:
# @colored
# class Rectangle:
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
# 
# r = Rectangle(10, 20)
# print(r.color)  # red
# r2 = Rectangle(5, 15, color="green")
# print(r2.color)  # green


# ============================================================================
# Задача 8. Параметризованный декоратор colored
# ============================================================================

def colored_parametrized(default_color="red"):
    """
    Параметризованный декоратор класса с настраиваемым цветом по умолчанию
    
    Args:
        default_color: цвет по умолчанию
    """
    def decorator(cls):
        original_init = cls.__init__
        
        @wraps(original_init)
        def new_init(self, *args, color=default_color, **kwargs):
            original_init(self, *args, **kwargs)
            self.color = color
        
        cls.__init__ = new_init
        return cls
    return decorator


# Пример использования:
# @colored_parametrized("blue")
# class Square:
#     def __init__(self, side):
#         self.side = side
# 
# s = Square(10)
# print(s.color)  # blue
# s2 = Square(5, color="yellow")
# print(s2.color)  # yellow


# ============================================================================
# Задача 9. Декоратор singleton
# ============================================================================

def singleton(cls):
    """
    Декоратор singleton - гарантирует, что класс имеет только один экземпляр
    
    Работа при наследовании:
    - Каждый класс будет иметь свой собственный экземпляр
    - Наследники не будут делить экземпляр с родителем
    
    Работа с классовыми методами:
    - Да, работает нормально, так как мы не меняем сами методы
    """
    instances = {}
    
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


# Пример использования:
# @singleton
# class Database:
#     def __init__(self, connection_string):
#         self.connection_string = connection_string
#         print(f"Создано подключение: {connection_string}")
# 
# db1 = Database("localhost:5432")
# db2 = Database("другой_адрес")  # Не создаст новое подключение
# print(db1 is db2)  # True


# ============================================================================
# Задача 10. Декоратор hide для приватизации атрибутов
# ============================================================================

def hide(*attrs_to_hide):
    """
    Декоратор класса, делающий указанные атрибуты приватными
    
    Args:
        *attrs_to_hide: имена атрибутов для приватизации
    """
    def decorator(cls):
        original_init = cls.__init__
        
        @wraps(original_init)
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            # Переименовываем указанные атрибуты с name mangling
            for attr in attrs_to_hide:
                if hasattr(self, attr):
                    value = getattr(self, attr)
                    delattr(self, attr)
                    # Используем name mangling: _ClassName__attrname
                    mangled_name = f"_{cls.__name__}__{attr}"
                    setattr(self, mangled_name, value)
        
        cls.__init__ = new_init
        return cls
    return decorator


# Пример использования:
# @hide("password", "secret_key")
# class User:
#     def __init__(self, username, password, secret_key):
#         self.username = username
#         self.password = password
#         self.secret_key = secret_key
# 
# u = User("admin", "12345", "abc")
# print(u.username)  # admin
# # print(u.password)  # AttributeError
# print(u._User__password)  # 12345 (name mangling)


# ============================================================================
# Задача 11. Декоратор hide_all (без inspect)
# ============================================================================

def hide_all(cls):
    """
    Декоратор класса, делающий все атрибуты объекта приватными
    (кроме методов)
    
    Использует callable() для определения методов
    """
    original_init = cls.__init__
    
    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        # Получаем все атрибуты объекта
        attrs = list(self.__dict__.keys())
        for attr in attrs:
            if not attr.startswith('_'):  # Не трогаем уже приватные
                value = getattr(self, attr)
                # Проверяем, что это не метод
                if not callable(value):
                    delattr(self, attr)
                    # Используем name mangling: _ClassName__attrname
                    mangled_name = f"_{cls.__name__}__{attr}"
                    setattr(self, mangled_name, value)
    
    cls.__init__ = new_init
    return cls


# Пример использования:
# @hide_all
# class BankAccount:
#     def __init__(self, account_number, balance):
#         self.account_number = account_number
#         self.balance = balance
#     
#     def get_balance(self):
#         return self.__balance
# 
# acc = BankAccount("123456", 1000)
# # print(acc.balance)  # AttributeError
# print(acc._BankAccount__balance)  # 1000


# ============================================================================
# Задача 12. Декоратор my_abstract и функция is_abstract
# ============================================================================

def my_abstract(method):
    """
    Декоратор, помечающий метод как абстрактный
    """
    method.__is_abstract = True
    return method


def is_abstract(cls):
    """
    Проверяет, есть ли у класса абстрактные методы
    
    Args:
        cls: класс для проверки
    
    Returns:
        True, если есть хотя бы один абстрактный метод
    """
    for attr_name in dir(cls):
        # Пропускаем магические методы и приватные атрибуты
        if attr_name.startswith('_'):
            continue
        
        attr = getattr(cls, attr_name)
        # Проверяем, что это callable и имеет метку __is_abstract
        if callable(attr) and hasattr(attr, '__is_abstract') and attr.__is_abstract:
            return True
    
    return False


# Пример использования:
# class Shape:
#     @my_abstract
#     def area(self):
#         pass
#     
#     def perimeter(self):
#         pass
# 
# class Circle(Shape):
#     def __init__(self, radius):
#         self.radius = radius
#     
#     def area(self):
#         return 3.14 * self.radius ** 2
# 
# print(is_abstract(Shape))   # True
# print(is_abstract(Circle))  # False (если переопределили area без декоратора)


# ============================================================================
# Демонстрация всех решений
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Демонстрация решений задач по декораторам")
    print("=" * 70)
    
    # Задача 1
    print("\n--- Задача 1: Замыкание get_formula ---")
    f = get_formula(2, 3)
    print(f"f(1, 2) = {f(1, 2)}")  # 2*1^2 + 3*2^2 = 14
    
    # Задача 2
    print("\n--- Задача 2: Декоратор trace ---")
    @trace
    def multiply(a, b):
        return a * b
    
    result = multiply(4, 5)
    
    # Задача 3
    print("\n--- Задача 3: Декоратор retry ---")
    attempt_counter = [0]
    
    @retry(attempts=3, delay=0.5)
    def sometimes_fails():
        attempt_counter[0] += 1
        if attempt_counter[0] < 2:
            raise ValueError("Ошибка!")
        return "Успех!"
    
    try:
        result = sometimes_fails()
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Все попытки исчерпаны: {e}")
    
    # Задача 4
    print("\n--- Задача 4: Регистрация команд ---")
    command_registry.clear()  # Очищаем реестр
    
    @register_command
    def greet():
        return "Привет!"
    
    @register_command
    def farewell():
        return "До свидания!"
    
    print(f"Команды в реестре: {list(command_registry.keys())}")
    print(f"run_command('greet'): {run_command('greet')}")
    
    # Задача 5
    print("\n--- Задача 5: Декоратор color_everyone ---")
    @color_everyone
    class Triangle:
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c
    
    t = Triangle(3, 4, 5)
    print(f"Triangle: {t}")
    
    # Задача 6
    print("\n--- Задача 6: Декоратор add_color ---")
    class Circle:
        @add_color
        def __init__(self, radius):
            self.radius = radius
    
    c1 = Circle(5)
    c2 = Circle(10, color="blue")
    print(f"Circle 1 color: {c1.color}")
    print(f"Circle 2 color: {c2.color}")
    
    # Задача 7
    print("\n--- Задача 7: Декоратор colored ---")
    @colored
    class Rectangle:
        def __init__(self, width, height):
            self.width = width
            self.height = height
    
    r1 = Rectangle(10, 20)
    r2 = Rectangle(5, 15, color="green")
    print(f"Rectangle 1 color: {r1.color}")
    print(f"Rectangle 2 color: {r2.color}")
    
    # Задача 8
    print("\n--- Задача 8: Параметризованный colored ---")
    @colored_parametrized("purple")
    class Square:
        def __init__(self, side):
            self.side = side
    
    s1 = Square(10)
    s2 = Square(5, color="yellow")
    print(f"Square 1 color: {s1.color}")
    print(f"Square 2 color: {s2.color}")
    
    # Задача 9
    print("\n--- Задача 9: Декоратор singleton ---")
    @singleton
    class Database:
        def __init__(self, name):
            self.name = name
            print(f"Создан экземпляр Database: {name}")
    
    db1 = Database("DB1")
    db2 = Database("DB2")
    print(f"db1 is db2: {db1 is db2}")
    print(f"db1.name: {db1.name}")
    
    # Задача 10
    print("\n--- Задача 10: Декоратор hide ---")
    @hide("password", "secret")
    class Account:
        def __init__(self, username, password, secret):
            self.username = username
            self.password = password
            self.secret = secret
    
    acc = Account("user", "pass123", "secret456")
    print(f"Username: {acc.username}")
    print(f"Has 'password' attr: {hasattr(acc, 'password')}")
    print(f"Has '__password' attr: {hasattr(acc, '_Account__password')}")
    
    # Задача 11
    print("\n--- Задача 11: Декоратор hide_all ---")
    @hide_all
    class SecureData:
        def __init__(self, data1, data2):
            self.data1 = data1
            self.data2 = data2
        
        def get_data(self):
            return f"{self.__data1}, {self.__data2}"
    
    sd = SecureData("value1", "value2")
    print(f"Has 'data1' attr: {hasattr(sd, 'data1')}")
    print(f"Has '__data1' mangled attr: {hasattr(sd, '_SecureData__data1')}")
    # Метод get_data использует self.__data1, что автоматически преобразуется в self._SecureData__data1
    print(f"get_data(): {sd.get_data()}")
    
    # Задача 12
    print("\n--- Задача 12: Декоратор my_abstract ---")
    class AbstractShape:
        @my_abstract
        def area(self):
            pass
        
        def description(self):
            return "Shape"
    
    class ConcreteCircle:
        def area(self):
            return 3.14
    
    print(f"AbstractShape is abstract: {is_abstract(AbstractShape)}")
    print(f"ConcreteCircle is abstract: {is_abstract(ConcreteCircle)}")
    
    print("\n" + "=" * 70)
    print("Все задачи выполнены!")
    print("=" * 70)
