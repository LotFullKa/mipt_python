"""
Тесты для задачи 6: добавление классов-наследников Cabbage и Rubus.

Тестируемая функциональность:
- Все тесты из задачи 5
- Класс Cabbage с методом head_amount (crop_yield / 3)
- Класс Rubus с приватным полем тип (малина, ежевика, ежемалина)
"""

import pytest
from src import Crop, Cabbage, Rubus, GrowthStage, TOTAL_FARM_AREA


class TestCabbageInheritance:
    """Тесты наследования класса Cabbage."""

    def test_cabbage_is_crop(self):
        """Тест что Cabbage наследуется от Crop."""
        cabbage = Cabbage("CAB-001", "2024-03-15", 10.0)
        assert isinstance(cabbage, Crop)
        assert isinstance(cabbage, Cabbage)

    def test_cabbage_has_crop_methods(self):
        """Тест что Cabbage имеет методы Crop."""
        cabbage = Cabbage("CAB-002", "2024-03-15", 10.0)
        assert hasattr(cabbage, 'get_id')
        assert hasattr(cabbage, 'get_seed_date')
        assert hasattr(cabbage, 'get_area')
        assert hasattr(cabbage, 'get_crop_yield')
        assert hasattr(cabbage, 'is_harvested')

    def test_cabbage_creation(self):
        """Тест создания объекта Cabbage."""
        cabbage = Cabbage("CAB-003", "2024-03-15", 10.0, 2)
        assert cabbage.get_id() == "CAB-003"
        assert cabbage.get_seed_date() == "2024-03-15"
        assert cabbage.get_area() == 10.0

    def test_cabbage_crop_yield(self):
        """Тест расчета урожайности капусты."""
        cabbage = Cabbage("CAB-004", "2024-03-15", 10.0)
        assert cabbage.get_crop_yield() == 45.0  # 4.5 * 10.0


class TestCabbageHeadAmount:
    """Тесты метода head_amount класса Cabbage."""

    def test_head_amount_basic(self):
        """Тест базового расчета количества кочанов."""
        cabbage = Cabbage("CAB-005", "2024-03-15", 10.0)
        # crop_yield = 4.5 * 10.0 = 45.0
        # head_amount = 45.0 / 3.0 = 15.0
        assert cabbage.head_amount() == 15.0

    def test_head_amount_different_areas(self):
        """Тест расчета для разных площадей."""
        cabbage1 = Cabbage("CAB-006", "2024-03-15", 6.0)
        # crop_yield = 4.5 * 6.0 = 27.0
        # head_amount = 27.0 / 3.0 = 9.0
        assert cabbage1.head_amount() == 9.0

        cabbage2 = Cabbage("CAB-007", "2024-03-15", 20.0)
        # crop_yield = 4.5 * 20.0 = 90.0
        # head_amount = 90.0 / 3.0 = 30.0
        assert cabbage2.head_amount() == 30.0

    def test_head_amount_zero_area(self):
        """Тест расчета при нулевой площади."""
        cabbage = Cabbage("CAB-008", "2024-03-15", 0.0)
        assert cabbage.head_amount() == 0.0

    def test_head_amount_fractional(self):
        """Тест расчета с дробным результатом."""
        cabbage = Cabbage("CAB-009", "2024-03-15", 5.0)
        # crop_yield = 4.5 * 5.0 = 22.5
        # head_amount = 22.5 / 3.0 = 7.5
        assert cabbage.head_amount() == 7.5

    def test_head_amount_returns_float(self):
        """Тест что head_amount возвращает float."""
        cabbage = Cabbage("CAB-010", "2024-03-15", 10.0)
        result = cabbage.head_amount()
        assert isinstance(result, float)

    def test_head_amount_large_area(self):
        """Тест расчета для большой площади."""
        cabbage = Cabbage("CAB-011", "2024-03-15", 100.0)
        # crop_yield = 4.5 * 100.0 = 450.0
        # head_amount = 450.0 / 3.0 = 150.0
        assert cabbage.head_amount() == 150.0


class TestRubusInheritance:
    """Тесты наследования класса Rubus."""

    def test_rubus_is_crop(self):
        """Тест что Rubus наследуется от Crop."""
        rubus = Rubus("RUB-001", "2024-03-15", 10.0, "малина")
        assert isinstance(rubus, Crop)
        assert isinstance(rubus, Rubus)

    def test_rubus_has_crop_methods(self):
        """Тест что Rubus имеет методы Crop."""
        rubus = Rubus("RUB-002", "2024-03-15", 10.0, "ежевика")
        assert hasattr(rubus, 'get_id')
        assert hasattr(rubus, 'get_seed_date')
        assert hasattr(rubus, 'get_area')
        assert hasattr(rubus, 'get_crop_yield')
        assert hasattr(rubus, 'is_harvested')

    def test_rubus_creation(self):
        """Тест создания объекта Rubus."""
        rubus = Rubus("RUB-003", "2024-03-15", 10.0, "малина", 2)
        assert rubus.get_id() == "RUB-003"
        assert rubus.get_seed_date() == "2024-03-15"
        assert rubus.get_area() == 10.0

    def test_rubus_crop_yield(self):
        """Тест расчета урожайности Rubus."""
        rubus = Rubus("RUB-004", "2024-03-15", 10.0, "ежевика")
        assert rubus.get_crop_yield() == 45.0  # 4.5 * 10.0


class TestRubusType:
    """Тесты приватного поля type класса Rubus."""

    def test_rubus_type_raspberry(self):
        """Тест создания малины."""
        rubus = Rubus("RUB-005", "2024-03-15", 10.0, "малина")
        assert rubus.get_type() == "малина"

    def test_rubus_type_blackberry(self):
        """Тест создания ежевики."""
        rubus = Rubus("RUB-006", "2024-03-15", 10.0, "ежевика")
        assert rubus.get_type() == "ежевика"

    def test_rubus_type_hybrid(self):
        """Тест создания ежемалины."""
        rubus = Rubus("RUB-007", "2024-03-15", 10.0, "ежемалина")
        assert rubus.get_type() == "ежемалина"

    def test_rubus_type_is_private(self):
        """Тест что поле type приватное."""
        rubus = Rubus("RUB-008", "2024-03-15", 10.0, "малина")
        # Приватное поле не должно быть доступно напрямую
        assert not hasattr(rubus, 'type')
        # Но должно быть доступно через name mangling
        assert hasattr(rubus, '_Rubus__type')

    def test_rubus_different_types(self):
        """Тест создания разных типов Rubus."""
        rubus1 = Rubus("RUB-009", "2024-03-15", 10.0, "малина")
        rubus2 = Rubus("RUB-010", "2024-03-15", 10.0, "ежевика")
        rubus3 = Rubus("RUB-011", "2024-03-15", 10.0, "ежемалина")

        assert rubus1.get_type() == "малина"
        assert rubus2.get_type() == "ежевика"
        assert rubus3.get_type() == "ежемалина"

    def test_rubus_type_with_growth_stage(self):
        """Тест создания Rubus с указанием стадии роста."""
        rubus = Rubus("RUB-012", "2024-03-15", 10.0, "малина", 3)
        assert rubus.get_type() == "малина"
        assert rubus.is_harvested() == 0


class TestCabbageProperties:
    """Тесты property для Cabbage."""

    def test_cabbage_id_property(self):
        """Тест property id для Cabbage."""
        cabbage = Cabbage("CAB-012", "2024-03-15", 10.0)
        assert cabbage.id == "CAB-012"

        cabbage.id = "CAB-NEW"
        assert cabbage.id == "CAB-NEW"

    def test_cabbage_seed_date_property(self):
        """Тест property seed_date для Cabbage."""
        cabbage = Cabbage("CAB-013", "2024-03-15", 10.0)
        assert cabbage.seed_date == "2024-03-15"

        cabbage.seed_date = "2024-04-20"
        assert cabbage.seed_date == "2024-04-20"

    def test_cabbage_area_property(self):
        """Тест property area для Cabbage."""
        cabbage = Cabbage("CAB-014", "2024-03-15", 10.0)
        assert cabbage.area == 10.0

        cabbage.area = 15.0
        assert cabbage.area == 15.0


class TestRubusProperties:
    """Тесты property для Rubus."""

    def test_rubus_id_property(self):
        """Тест property id для Rubus."""
        rubus = Rubus("RUB-013", "2024-03-15", 10.0, "малина")
        assert rubus.id == "RUB-013"

        rubus.id = "RUB-NEW"
        assert rubus.id == "RUB-NEW"

    def test_rubus_seed_date_property(self):
        """Тест property seed_date для Rubus."""
        rubus = Rubus("RUB-014", "2024-03-15", 10.0, "ежевика")
        assert rubus.seed_date == "2024-03-15"

        rubus.seed_date = "2024-04-20"
        assert rubus.seed_date == "2024-04-20"

    def test_rubus_area_property(self):
        """Тест property area для Rubus."""
        rubus = Rubus("RUB-015", "2024-03-15", 10.0, "ежемалина")
        assert rubus.area == 10.0

        rubus.area = 15.0
        assert rubus.area == 15.0


class TestCropBasic:
    """Тесты базовой функциональности класса Crop."""

    def test_crop_creation(self):
        """Тест создания объекта Crop."""
        crop = Crop("WHEAT-001", "2024-03-15", 10.5, 0)
        assert crop.get_id() == "WHEAT-001"

    def test_is_harvested(self):
        """Тест метода is_harvested."""
        crop1 = Crop("WHEAT-002", "2024-03-15", 10.0, 0)
        assert crop1.is_harvested() == 0

        crop2 = Crop("WHEAT-003", "2024-03-15", 10.0, 5)
        assert crop2.is_harvested() == 1


class TestTotalFarmArea:
    """Тесты глобальной переменной TOTAL_FARM_AREA."""

    def test_total_farm_area_with_cabbage(self):
        """Тест TOTAL_FARM_AREA с капустой."""
        global TOTAL_FARM_AREA
        initial_area = TOTAL_FARM_AREA

        cabbage = Cabbage("CAB-015", "2024-03-15", 15.0)
        assert TOTAL_FARM_AREA == initial_area + 15.0

        del cabbage
        assert TOTAL_FARM_AREA == initial_area

    def test_total_farm_area_with_rubus(self):
        """Тест TOTAL_FARM_AREA с Rubus."""
        global TOTAL_FARM_AREA
        initial_area = TOTAL_FARM_AREA

        rubus = Rubus("RUB-016", "2024-03-15", 20.0, "малина")
        assert TOTAL_FARM_AREA == initial_area + 20.0

        del rubus
        assert TOTAL_FARM_AREA == initial_area

    def test_total_farm_area_mixed_crops(self):
        """Тест TOTAL_FARM_AREA со смешанными культурами."""
        global TOTAL_FARM_AREA
        initial_area = TOTAL_FARM_AREA

        crop = Crop("WHEAT-004", "2024-03-15", 10.0)
        cabbage = Cabbage("CAB-016", "2024-03-15", 15.0)
        rubus = Rubus("RUB-017", "2024-03-15", 5.0, "ежевика")

        assert TOTAL_FARM_AREA == initial_area + 30.0

        del crop
        del cabbage
        del rubus
        assert TOTAL_FARM_AREA == initial_area
