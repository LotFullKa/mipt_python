"""
Задача 2: Класс Organism с __init_subclass__

Класс Organism с __init_subclass__, который поддерживает список созданных 
классов-растений и классов-животных в зависимости от миксинов.
"""


class PlantMixin:
    """Миксин для растений."""
    pass


class AnimalMixin:
    """Миксин для животных."""
    pass


class Organism:
    """Базовый класс для организмов."""
    
    plants = []
    animals = []
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # Проверяем, является ли класс растением
        if any(issubclass(base, PlantMixin) for base in cls.__bases__):
            Organism.plants.append(cls)
        
        # Проверяем, является ли класс животным
        if any(issubclass(base, AnimalMixin) for base in cls.__bases__):
            Organism.animals.append(cls)
    
    @classmethod
    def get_plants(cls):
        """Возвращает список всех классов-растений."""
        return cls.plants
    
    @classmethod
    def get_animals(cls):
        """Возвращает список всех классов-животных."""
        return cls.animals
    
    @classmethod
    def reset(cls):
        """Сбрасывает списки растений и животных."""
        cls.plants = []
        cls.animals = []


# Примеры использования
if __name__ == "__main__":
    # Создаем классы растений
    class Rose(PlantMixin, Organism):
        def __init__(self, color):
            self.color = color
    
    class Oak(PlantMixin, Organism):
        def __init__(self, age):
            self.age = age
    
    class Tulip(PlantMixin, Organism):
        def __init__(self, height):
            self.height = height
    
    # Создаем классы животных
    class Dog(AnimalMixin, Organism):
        def __init__(self, name):
            self.name = name
    
    class Cat(AnimalMixin, Organism):
        def __init__(self, name):
            self.name = name
    
    class Bird(AnimalMixin, Organism):
        def __init__(self, species):
            self.species = species
    
    # Проверяем списки
    print("Plants:", [cls.__name__ for cls in Organism.get_plants()])
    # Plants: ['Rose', 'Oak', 'Tulip']
    
    print("Animals:", [cls.__name__ for cls in Organism.get_animals()])
    # Animals: ['Dog', 'Cat', 'Bird']
    
    # Создаем экземпляры
    rose = Rose("red")
    dog = Dog("Buddy")
    
    print(f"\nCreated rose with color: {rose.color}")
    print(f"Created dog with name: {dog.name}")
    
    # Проверяем, что списки не изменились после создания экземпляров
    print(f"\nTotal plant classes: {len(Organism.get_plants())}")
    print(f"Total animal classes: {len(Organism.get_animals())}")
    
    # Создаем еще один класс растения
    class Cactus(PlantMixin, Organism):
        def __init__(self, spines):
            self.spines = spines
    
    print(f"\nAfter adding Cactus:")
    print("Plants:", [cls.__name__ for cls in Organism.get_plants()])
    # Plants: ['Rose', 'Oak', 'Tulip', 'Cactus']
