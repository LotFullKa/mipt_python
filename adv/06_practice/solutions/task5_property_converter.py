"""
Задача 5: Property Converter

Метакласс PropertyConverter, который автоматически создает property 
для методов get_* и set_*.
"""


class PropertyConverterMeta(type):
    """
    Метакласс, который конвертирует get_* и set_* методы в property.
    
    Для каждой пары методов get_name и set_name создается property с именем name.
    Если есть только get_name, создается read-only property.
    """
    
    def __new__(mcs, name, bases, namespace, **kwargs):
        # Словарь для хранения найденных getter'ов и setter'ов
        properties = {}
        
        # Собираем все атрибуты из базовых классов и текущего namespace
        all_attrs = {}
        for base in bases:
            all_attrs.update({k: v for k, v in base.__dict__.items()})
        all_attrs.update(namespace)
        
        # Ищем методы get_* и set_*
        for attr_name, attr_value in all_attrs.items():
            if callable(attr_value):
                if attr_name.startswith('get_') and not attr_name.startswith('get__'):
                    # Нашли getter
                    prop_name = attr_name[4:]  # Убираем префикс 'get_'
                    if prop_name not in properties:
                        properties[prop_name] = {'getter': None, 'setter': None}
                    properties[prop_name]['getter'] = attr_value
                
                elif attr_name.startswith('set_') and not attr_name.startswith('set__'):
                    # Нашли setter
                    prop_name = attr_name[4:]  # Убираем префикс 'set_'
                    if prop_name not in properties:
                        properties[prop_name] = {'getter': None, 'setter': None}
                    properties[prop_name]['setter'] = attr_value
        
        # Создаем property для каждой найденной пары
        for prop_name, methods in properties.items():
            getter = methods['getter']
            setter = methods['setter']
            
            if getter is not None:
                # Создаем property
                if setter is not None:
                    # Есть и getter, и setter
                    namespace[prop_name] = property(
                        lambda self, g=getter: g(self),
                        lambda self, value, s=setter: s(self, value)
                    )
                else:
                    # Только getter (read-only)
                    namespace[prop_name] = property(
                        lambda self, g=getter: g(self)
                    )
        
        return super().__new__(mcs, name, bases, namespace, **kwargs)


class PropertyConverter(metaclass=PropertyConverterMeta):
    """
    Базовый класс с метаклассом PropertyConverter.
    
    Добавляет __getattr__ и __setattr__ для предотвращения ошибок typing.
    """
    
    def __getattr__(self, name):
        # Этот метод вызывается только если атрибут не найден обычным способом
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        # Стандартное поведение для установки атрибутов
        object.__setattr__(self, name, value)


# Примеры использования
if __name__ == "__main__":
    # Пример из условия задачи
    class OldAndNasty:
        def __init__(self, temperature):
            self._temperature = temperature
        
        def get_temperature(self):
            return self._temperature
        
        def set_temperature(self, temperature):
            if temperature <= 0:
                raise ValueError("Temperature below zero is not allowed")
            self._temperature = temperature
    
    class NewAndShiny(OldAndNasty, PropertyConverter):
        pass
    
    # Старые функции работают
    new_obj = NewAndShiny(100)
    new_obj.set_temperature(10)
    print(f"Temperature after set_temperature(10): {new_obj.get_temperature()}")  # 10
    
    try:
        new_obj.set_temperature(-1)
    except ValueError:
        print("Did not set negative temperature via set_temperature")
    
    # Но есть property
    print(f"Temperature via property: {new_obj.temperature}")  # 10
    new_obj.temperature = 50
    print(f"Temperature after property assignment: {new_obj.temperature}")  # 50
    
    try:
        new_obj.temperature = -1
    except ValueError:
        print("Did not set negative temperature via property")
    
    # Дополнительные примеры
    print("\n--- Additional Examples ---\n")
    
    # Пример 2: Класс с несколькими свойствами
    class Person:
        def __init__(self, name, age):
            self._name = name
            self._age = age
        
        def get_name(self):
            return self._name
        
        def set_name(self, name):
            if not isinstance(name, str):
                raise TypeError("Name must be a string")
            self._name = name
        
        def get_age(self):
            return self._age
        
        def set_age(self, age):
            if not isinstance(age, int) or age < 0:
                raise ValueError("Age must be a non-negative integer")
            self._age = age
    
    class ModernPerson(Person, PropertyConverter):
        pass
    
    person = ModernPerson("Alice", 30)
    print(f"Name: {person.name}, Age: {person.age}")  # Name: Alice, Age: 30
    
    person.name = "Bob"
    person.age = 35
    print(f"Updated - Name: {person.name}, Age: {person.age}")  # Name: Bob, Age: 35
    
    try:
        person.age = -5
    except ValueError as e:
        print(f"Error setting age: {e}")
    
    # Пример 3: Read-only property (только getter)
    class ReadOnlyExample:
        def __init__(self, value):
            self._value = value
        
        def get_value(self):
            return self._value
    
    class ModernReadOnly(ReadOnlyExample, PropertyConverter):
        pass
    
    ro = ModernReadOnly(42)
    print(f"\nRead-only value: {ro.value}")  # 42
    
    # Попытка установить значение через property вызовет ошибку
    try:
        ro.value = 100
    except AttributeError as e:
        print(f"Cannot set read-only property: can't set attribute")
    
    # Пример 4: Множественные свойства
    class Rectangle:
        def __init__(self, width, height):
            self._width = width
            self._height = height
        
        def get_width(self):
            return self._width
        
        def set_width(self, width):
            if width <= 0:
                raise ValueError("Width must be positive")
            self._width = width
        
        def get_height(self):
            return self._height
        
        def set_height(self, height):
            if height <= 0:
                raise ValueError("Height must be positive")
            self._height = height
        
        def get_area(self):
            return self._width * self._height
    
    class ModernRectangle(Rectangle, PropertyConverter):
        pass
    
    rect = ModernRectangle(10, 20)
    print(f"\nRectangle: width={rect.width}, height={rect.height}, area={rect.area}")
    
    rect.width = 15
    rect.height = 25
    print(f"Updated Rectangle: width={rect.width}, height={rect.height}, area={rect.area}")
