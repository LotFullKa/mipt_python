"""
Тесты для задачи 1: базовый класс Crop с приватными атрибутами.

Тестируемая функциональность:
- Глобальная переменная TOTAL_FARM_AREA (изменение в __init__ и __del__)
- Создание объекта Crop с приватными атрибутами
- Методы get_id, get_seed_date, get_area
- Метод get_crop_yield (4.5 * площадь)
"""

import pytest
from src import Crop, TOTAL_FARM_AREA


class TestCropBasic:
    """Тесты базовой функциональности класса Crop."""

    def test_crop_creation(self):
        """Тест создания объекта Crop."""
        crop = Crop("WHEAT-001", "2024-03-15", 10.5, 0)
        assert crop.get_id() == "WHEAT-001"
        assert crop.get_seed_date() == "2024-03-15"
        assert crop.get_area() == 10.5

    def test_get_id(self):
        """Тест метода get_id."""
        crop = Crop("CORN-002", "2024-04-01", 5.0)
        assert crop.get_id() == "CORN-002"

    def test_get_seed_date(self):
        """Тест метода get_seed_date."""
        crop = Crop("WHEAT-003", "2024-05-10", 8.0)
        assert crop.get_seed_date() == "2024-05-10"

    def test_get_area(self):
        """Тест метода get_area."""
        crop = Crop("BARLEY-004", "2024-06-20", 12.5)
        assert crop.get_area() == 12.5

    def test_get_crop_yield(self):
        """Тест метода get_crop_yield (4.5 * площадь)."""
        crop = Crop("WHEAT-005", "2024-03-15", 10.0)
        assert crop.get_crop_yield() == 45.0  # 4.5 * 10.0

        crop2 = Crop("CORN-006", "2024-04-01", 20.0)
        assert crop2.get_crop_yield() == 90.0  # 4.5 * 20.0

    def test_private_attributes(self):
        """Тест что атрибуты действительно приватные."""
        crop = Crop("WHEAT-007", "2024-03-15", 10.0)
        # Приватные атрибуты не должны быть доступны напрямую
        assert not hasattr(crop, 'id')
        assert not hasattr(crop, 'seed_date')
        assert not hasattr(crop, 'area')
        # Но должны быть доступны через name mangling
        assert hasattr(crop, '_Crop__id')
        assert hasattr(crop, '_Crop__seed_date')
        assert hasattr(crop, '_Crop__area')


class TestTotalFarmArea:
    """Тесты глобальной переменной TOTAL_FARM_AREA."""

    def test_total_farm_area_increases_on_init(self):
        """Тест увеличения TOTAL_FARM_AREA при создании объекта."""
        global TOTAL_FARM_AREA
        initial_area = TOTAL_FARM_AREA

        crop = Crop("WHEAT-008", "2024-03-15", 15.0)
        assert TOTAL_FARM_AREA == initial_area + 15.0

        # Очистка
        del crop

    def test_total_farm_area_decreases_on_del(self):
        """Тест уменьшения TOTAL_FARM_AREA при удалении объекта."""
        global TOTAL_FARM_AREA
        initial_area = TOTAL_FARM_AREA

        crop = Crop("CORN-009", "2024-04-01", 20.0)
        assert TOTAL_FARM_AREA == initial_area + 20.0

        del crop
        assert TOTAL_FARM_AREA == initial_area

    def test_total_farm_area_multiple_crops(self):
        """Тест TOTAL_FARM_AREA с несколькими культурами."""
        global TOTAL_FARM_AREA
        initial_area = TOTAL_FARM_AREA

        crop1 = Crop("WHEAT-010", "2024-03-15", 10.0)
        crop2 = Crop("CORN-011", "2024-04-01", 15.0)
        crop3 = Crop("BARLEY-012", "2024-05-10", 5.0)

        assert TOTAL_FARM_AREA == initial_area + 30.0

        del crop1
        assert TOTAL_FARM_AREA == initial_area + 20.0

        del crop2
        assert TOTAL_FARM_AREA == initial_area + 5.0

        del crop3
        assert TOTAL_FARM_AREA == initial_area


class TestCropYieldCalculations:
    """Тесты расчета урожайности."""

    def test_yield_zero_area(self):
        """Тест урожайности при нулевой площади."""
        crop = Crop("WHEAT-013", "2024-03-15", 0.0)
        assert crop.get_crop_yield() == 0.0

    def test_yield_small_area(self):
        """Тест урожайности при малой площади."""
        crop = Crop("WHEAT-014", "2024-03-15", 0.5)
        assert crop.get_crop_yield() == 2.25  # 4.5 * 0.5

    def test_yield_large_area(self):
        """Тест урожайности при большой площади."""
        crop = Crop("WHEAT-015", "2024-03-15", 100.0)
        assert crop.get_crop_yield() == 450.0  # 4.5 * 100.0

    def test_yield_fractional_area(self):
        """Тест урожайности при дробной площади."""
        crop = Crop("WHEAT-016", "2024-03-15", 7.3)
        assert crop.get_crop_yield() == pytest.approx(32.85)  # 4.5 * 7.3
