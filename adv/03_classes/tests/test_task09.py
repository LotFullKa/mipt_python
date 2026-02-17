"""
Тесты для задачи 9: статический метод создания класса на основе параметров.

Тестируемая функциональность:
- Все тесты из задачи 8
- Статический метод создания класса на основе названия, методов и атрибутов
- Сравнение двух способов создания класса (копирование vs создание нового)
"""

import pytest
from src import Crop, Cabbage, Rubus, SeasonalMixin, Cruciferous, GrowthStage, TOTAL_FARM_AREA


class TestCreateClassBasic:
    """Тесты базовой функциональности статического метода create_class."""

    def test_create_class_exists(self):
        """Тест что метод create_class существует."""
        assert hasattr(Crop, 'create_class')
        assert callable(Crop.create_class)

    def test_create_class_is_static(self):
        """Тест что create_class является статическим методом."""
        assert isinstance(Crop.__dict__['create_class'], staticmethod)

    def test_create_simple_class(self):
        """Тест создания простого класса."""
        NewCrop = Crop.create_class('NewCrop')
        assert NewCrop is not None
        assert NewCrop.__name__ == 'NewCrop'

    def test_created_class_is_subclass(self):
        """Тест что созданный класс является подклассом Crop."""
        NewCrop = Crop.create_class('NewCrop')
        assert issubclass(NewCrop, Crop)

    def test_created_class_can_be_instantiated(self):
        """Тест что созданный класс можно инстанцировать."""
        NewCrop = Crop.create_class('NewCrop')
        instance = NewCrop("TEST-001", "2024-03-15", 10.0)
        assert isinstance(instance, NewCrop)
        assert isinstance(instance, Crop)


class TestCreateClassWithMethods:
    """Тесты создания класса с методами."""

    def test_create_class_with_method(self):
        """Тест создания класса с пользовательским методом."""
        def custom_method(self):
            return "custom"

        NewCrop = Crop.create_class('NewCrop', methods={'custom_method': custom_method})
        instance = NewCrop("TEST-002", "2024-03-15", 10.0)

        assert hasattr(instance, 'custom_method')
        assert instance.custom_method() == "custom"

    def test_create_class_with_multiple_methods(self):
        """Тест создания класса с несколькими методами."""
        def method1(self):
            return "method1"

        def method2(self):
            return "method2"

        NewCrop = Crop.create_class('NewCrop', methods={
            'method1': method1,
            'method2': method2
        })
        instance = NewCrop("TEST-003", "2024-03-15", 10.0)

        assert instance.method1() == "method1"
        assert instance.method2() == "method2"

    def test_create_class_override_method(self):
        """Тест переопределения метода базового класса."""
        def get_crop_yield(self):
            return 10.0 * self.get_area()

        NewCrop = Crop.create_class('NewCrop', methods={'get_crop_yield': get_crop_yield})
        instance = NewCrop("TEST-004", "2024-03-15", 10.0)

        # Новый метод должен вернуть 10.0 * 10.0 = 100.0 вместо 4.5 * 10.0 = 45.0
        assert instance.get_crop_yield() == 100.0


class TestCreateClassWithAttributes:
    """Тесты создания класса с атрибутами."""

    def test_create_class_with_class_attribute(self):
        """Тест создания класса с атрибутом класса."""
        NewCrop = Crop.create_class('NewCrop', class_attrs={'crop_type': 'grain'})

        assert hasattr(NewCrop, 'crop_type')
        assert NewCrop.crop_type == 'grain'

    def test_create_class_with_multiple_attributes(self):
        """Тест создания класса с несколькими атрибутами."""
        NewCrop = Crop.create_class('NewCrop', class_attrs={
            'crop_type': 'vegetable',
            'harvest_season': 'autumn',
            'min_temperature': 5
        })

        assert NewCrop.crop_type == 'vegetable'
        assert NewCrop.harvest_season == 'autumn'
        assert NewCrop.min_temperature == 5

    def test_instance_can_access_class_attributes(self):
        """Тест что экземпляр может получить доступ к атрибутам класса."""
        NewCrop = Crop.create_class('NewCrop', class_attrs={'crop_type': 'fruit'})
        instance = NewCrop("TEST-005", "2024-03-15", 10.0)

        assert instance.crop_type == 'fruit'


class TestCreateClassWithBases:
    """Тесты создания класса с пользовательскими базовыми классами."""

    def test_create_class_with_custom_base(self):
        """Тест создания класса с пользовательским базовым классом."""
        NewCrop = Crop.create_class('NewCrop', bases=(Cabbage,))

        assert issubclass(NewCrop, Cabbage)
        assert issubclass(NewCrop, Crop)

    def test_create_class_with_multiple_bases(self):
        """Тест создания класса с несколькими базовыми классами."""
        NewCrop = Crop.create_class('NewCrop', bases=(SeasonalMixin, Crop))
        instance = NewCrop("TEST-006", "2024-03-15", 10.0)

        assert isinstance(instance, SeasonalMixin)
        assert isinstance(instance, Crop)
        assert hasattr(instance, 'set_season')
        assert hasattr(instance, 'seasonal_bonus')

    def test_created_class_inherits_methods(self):
        """Тест что созданный класс наследует методы базовых классов."""
        NewCrop = Crop.create_class('NewCrop', bases=(Cabbage,))
        instance = NewCrop("TEST-007", "2024-03-15", 10.0)

        assert hasattr(instance, 'head_amount')
        assert instance.head_amount() == 15.0  # 4.5 * 10.0 / 3.0


class TestCreateClassComplex:
    """Тесты создания сложных классов."""

    def test_create_class_with_all_parameters(self):
        """Тест создания класса со всеми параметрами."""
        def custom_yield(self):
            return self.get_area() * 6.0

        NewCrop = Crop.create_class(
            'NewCrop',
            bases=(Crop,),
            methods={'get_crop_yield': custom_yield},
            class_attrs={'crop_type': 'special'}
        )

        instance = NewCrop("TEST-008", "2024-03-15", 10.0)

        assert NewCrop.__name__ == 'NewCrop'
        assert NewCrop.crop_type == 'special'
        assert instance.get_crop_yield() == 60.0

    def test_create_tomato_class(self):
        """Тест создания класса Tomato с помощью create_class."""
        def fruit_count(self):
            return self.get_crop_yield() / 0.2  # средний вес помидора 200г

        Tomato = Crop.create_class(
            'Tomato',
            methods={'fruit_count': fruit_count},
            class_attrs={'crop_type': 'vegetable', 'color': 'red'}
        )

        tomato = Tomato("TOM-001", "2024-03-15", 10.0)

        assert tomato.crop_type == 'vegetable'
        assert tomato.color == 'red'
        assert tomato.fruit_count() == 225.0  # 45.0 / 0.2


class TestCompareClassCreationMethods:
    """Тесты сравнения двух способов создания класса."""

    def test_traditional_vs_dynamic_creation(self):
        """Тест сравнения традиционного и динамического создания класса."""
        # Традиционный способ
        class TraditionalCrop(Crop):
            crop_type = 'grain'

            def special_method(self):
                return "traditional"

        # Динамический способ
        def special_method(self):
            return "traditional"

        DynamicCrop = Crop.create_class(
            'DynamicCrop',
            methods={'special_method': special_method},
            class_attrs={'crop_type': 'grain'}
        )

        # Оба класса должны быть подклассами Crop
        assert issubclass(TraditionalCrop, Crop)
        assert issubclass(DynamicCrop, Crop)

        # Создание экземпляров
        trad = TraditionalCrop("TRAD-001", "2024-03-15", 10.0)
        dyn = DynamicCrop("DYN-001", "2024-03-15", 10.0)

        # Оба должны иметь одинаковые атрибуты и методы
        assert trad.crop_type == dyn.crop_type
        assert trad.special_method() == dyn.special_method()
        assert trad.get_crop_yield() == dyn.get_crop_yield()

    def test_copy_class_structure(self):
        """Тест копирования структуры класса."""
        # Исходный класс
        class OriginalCrop(Crop):
            harvest_time = 90

            def days_to_harvest(self):
                return self.harvest_time

        # Копирование через create_class
        def days_to_harvest(self):
            return self.harvest_time

        CopiedCrop = Crop.create_class(
            'CopiedCrop',
            methods={'days_to_harvest': days_to_harvest},
            class_attrs={'harvest_time': 90}
        )

        orig = OriginalCrop("ORIG-001", "2024-03-15", 10.0)
        copy = CopiedCrop("COPY-001", "2024-03-15", 10.0)

        assert orig.harvest_time == copy.harvest_time
        assert orig.days_to_harvest() == copy.days_to_harvest()

    def test_dynamic_class_modification(self):
        """Тест что динамически созданный класс можно модифицировать."""
        NewCrop = Crop.create_class('NewCrop', class_attrs={'version': 1})

        # Добавление нового атрибута
        NewCrop.version = 2

        instance = NewCrop("TEST-009", "2024-03-15", 10.0)
        assert instance.version == 2


class TestCreateClassEdgeCases:
    """Тесты граничных случаев создания классов."""

    def test_create_class_empty_methods(self):
        """Тест создания класса с пустым словарем методов."""
        NewCrop = Crop.create_class('NewCrop', methods={})
        instance = NewCrop("TEST-010", "2024-03-15", 10.0)

        assert isinstance(instance, Crop)

    def test_create_class_empty_attributes(self):
        """Тест создания класса с пустым словарем атрибутов."""
        NewCrop = Crop.create_class('NewCrop', class_attrs={})
        instance = NewCrop("TEST-011", "2024-03-15", 10.0)

        assert isinstance(instance, Crop)

    def test_create_class_none_parameters(self):
        """Тест создания класса с None параметрами."""
        NewCrop = Crop.create_class('NewCrop', bases=None, methods=None, class_attrs=None)
        instance = NewCrop("TEST-012", "2024-03-15", 10.0)

        assert isinstance(instance, Crop)


class TestCropBasic:
    """Тесты базовой функциональности класса Crop."""

    def test_crop_creation(self):
        """Тест создания объекта Crop."""
        crop = Crop("WHEAT-001", "2024-03-15", 10.5, 0)
        assert crop.get_id() == "WHEAT-001"


class TestCabbageBasic:
    """Тесты базовой функциональности класса Cabbage."""

    def test_cabbage_can_be_harvested(self):
        """Тест метода can_be_harvested."""
        cabbage = Cabbage("CAB-001", "2024-03-15", 10.0, 5)
        assert cabbage.can_be_harvested() is True


class TestTotalFarmArea:
    """Тесты глобальной переменной TOTAL_FARM_AREA."""

    def test_total_farm_area_with_dynamic_class(self):
        """Тест TOTAL_FARM_AREA с динамически созданным классом."""
        global TOTAL_FARM_AREA
        initial_area = TOTAL_FARM_AREA

        NewCrop = Crop.create_class('NewCrop')
        crop = NewCrop("TEST-013", "2024-03-15", 15.0)

        assert TOTAL_FARM_AREA == initial_area + 15.0

        del crop
        assert TOTAL_FARM_AREA == initial_area
