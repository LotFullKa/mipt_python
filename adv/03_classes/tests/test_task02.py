"""
Тесты для задачи 2: добавление методов __repr__ и __eq__ к классу Crop.

Тестируемая функциональность:
- Все тесты из задачи 1
- Метод __repr__ (читаемое представление объекта)
- Метод __eq__ (сравнение двух объектов Crop)
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
        assert crop.get_crop_yield() == 45.0

        crop2 = Crop("CORN-006", "2024-04-01", 20.0)
        assert crop2.get_crop_yield() == 90.0


class TestCropRepr:
    """Тесты метода __repr__."""

    def test_repr_basic(self):
        """Тест базового представления объекта."""
        crop = Crop("WHEAT-007", "2024-03-15", 10.5, 2)
        repr_str = repr(crop)
        assert "WHEAT-007" in repr_str
        assert "2024-03-15" in repr_str
        assert "10.5" in repr_str
        assert "2" in repr_str

    def test_repr_format(self):
        """Тест формата представления."""
        crop = Crop("CORN-008", "2024-04-01", 5.0, 0)
        repr_str = repr(crop)
        assert repr_str.startswith("Crop(")
        assert repr_str.endswith(")")
        assert "id=" in repr_str
        assert "seed_date=" in repr_str
        assert "area=" in repr_str
        assert "growth_stage=" in repr_str

    def test_repr_different_values(self):
        """Тест представления с разными значениями."""
        crop1 = Crop("WHEAT-009", "2024-01-01", 1.0, 0)
        crop2 = Crop("BARLEY-010", "2024-12-31", 100.0, 5)

        repr1 = repr(crop1)
        repr2 = repr(crop2)

        assert repr1 != repr2
        assert "WHEAT-009" in repr1
        assert "BARLEY-010" in repr2


class TestCropEquality:
    """Тесты метода __eq__."""

    def test_eq_same_values(self):
        """Тест равенства объектов с одинаковыми значениями."""
        crop1 = Crop("WHEAT-011", "2024-03-15", 10.0, 2)
        crop2 = Crop("WHEAT-011", "2024-03-15", 10.0, 2)
        assert crop1 == crop2

    def test_eq_different_id(self):
        """Тест неравенства при разных id."""
        crop1 = Crop("WHEAT-012", "2024-03-15", 10.0, 2)
        crop2 = Crop("CORN-012", "2024-03-15", 10.0, 2)
        assert crop1 != crop2

    def test_eq_different_seed_date(self):
        """Тест неравенства при разных датах засева."""
        crop1 = Crop("WHEAT-013", "2024-03-15", 10.0, 2)
        crop2 = Crop("WHEAT-013", "2024-04-15", 10.0, 2)
        assert crop1 != crop2

    def test_eq_different_area(self):
        """Тест неравенства при разных площадях."""
        crop1 = Crop("WHEAT-014", "2024-03-15", 10.0, 2)
        crop2 = Crop("WHEAT-014", "2024-03-15", 15.0, 2)
        assert crop1 != crop2

    def test_eq_different_growth_stage(self):
        """Тест неравенства при разных стадиях роста."""
        crop1 = Crop("WHEAT-015", "2024-03-15", 10.0, 2)
        crop2 = Crop("WHEAT-015", "2024-03-15", 10.0, 3)
        assert crop1 != crop2

    def test_eq_with_non_crop(self):
        """Тест сравнения с объектом другого типа."""
        crop = Crop("WHEAT-016", "2024-03-15", 10.0, 2)
        assert crop != "not a crop"
        assert crop != 123
        assert crop != None
        assert crop != {"id": "WHEAT-016"}

    def test_eq_reflexive(self):
        """Тест рефлексивности (объект равен самому себе)."""
        crop = Crop("WHEAT-017", "2024-03-15", 10.0, 2)
        assert crop == crop

    def test_eq_symmetric(self):
        """Тест симметричности (если a == b, то b == a)."""
        crop1 = Crop("WHEAT-018", "2024-03-15", 10.0, 2)
        crop2 = Crop("WHEAT-018", "2024-03-15", 10.0, 2)
        assert crop1 == crop2
        assert crop2 == crop1

    def test_eq_transitive(self):
        """Тест транзитивности (если a == b и b == c, то a == c)."""
        crop1 = Crop("WHEAT-019", "2024-03-15", 10.0, 2)
        crop2 = Crop("WHEAT-019", "2024-03-15", 10.0, 2)
        crop3 = Crop("WHEAT-019", "2024-03-15", 10.0, 2)
        assert crop1 == crop2
        assert crop2 == crop3
        assert crop1 == crop3


# class TestTotalFarmArea:
#     """Тесты глобальной переменной TOTAL_FARM_AREA."""

#     def test_total_farm_area_increases_on_init(self):
#         """Тест увеличения TOTAL_FARM_AREA при создании объекта."""
#         global TOTAL_FARM_AREA
#         initial_area = TOTAL_FARM_AREA

#         crop = Crop("WHEAT-020", "2024-03-15", 15.0)
#         assert TOTAL_FARM_AREA == initial_area + 15.0

#         del crop

#     def test_total_farm_area_decreases_on_del(self):
#         """Тест уменьшения TOTAL_FARM_AREA при удалении объекта."""
#         global TOTAL_FARM_AREA
#         initial_area = TOTAL_FARM_AREA

#         crop = Crop("CORN-021", "2024-04-01", 20.0)
#         assert TOTAL_FARM_AREA == initial_area + 20.0

#         del crop
#         assert TOTAL_FARM_AREA == initial_area
