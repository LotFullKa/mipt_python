"""
Тесты для задачи 3: добавление классового метода from_dict.

Тестируемая функциональность:
- Все тесты из задачи 2
- Классовый метод from_dict для создания объекта из словаря
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


class TestCropRepr:
    """Тесты метода __repr__."""

    def test_repr_basic(self):
        """Тест базового представления объекта."""
        crop = Crop("WHEAT-006", "2024-03-15", 10.5, 2)
        repr_str = repr(crop)
        assert "WHEAT-006" in repr_str
        assert "2024-03-15" in repr_str
        assert "10.5" in repr_str

    def test_repr_format(self):
        """Тест формата представления."""
        crop = Crop("CORN-007", "2024-04-01", 5.0, 0)
        repr_str = repr(crop)
        assert repr_str.startswith("Crop(")
        assert repr_str.endswith(")")


class TestCropEquality:
    """Тесты метода __eq__."""

    def test_eq_same_values(self):
        """Тест равенства объектов с одинаковыми значениями."""
        crop1 = Crop("WHEAT-008", "2024-03-15", 10.0, 2)
        crop2 = Crop("WHEAT-008", "2024-03-15", 10.0, 2)
        assert crop1 == crop2

    def test_eq_different_id(self):
        """Тест неравенства при разных id."""
        crop1 = Crop("WHEAT-009", "2024-03-15", 10.0, 2)
        crop2 = Crop("CORN-009", "2024-03-15", 10.0, 2)
        assert crop1 != crop2

    def test_eq_with_non_crop(self):
        """Тест сравнения с объектом другого типа."""
        crop = Crop("WHEAT-010", "2024-03-15", 10.0, 2)
        assert crop != "not a crop"
        assert crop != 123


class TestFromDict:
    """Тесты классового метода from_dict."""

    def test_from_dict_basic(self):
        """Тест создания объекта из словаря с полными данными."""
        data = {
            'id': 'WHEAT-011',
            'seed_date': '2024-03-15',
            'area': 10.5,
            'growth_stage': 2
        }
        crop = Crop.from_dict(data)

        assert crop.get_id() == 'WHEAT-011'
        assert crop.get_seed_date() == '2024-03-15'
        assert crop.get_area() == 10.5

    def test_from_dict_without_growth_stage(self):
        """Тест создания объекта из словаря без growth_stage (должен быть 0)."""
        data = {
            'id': 'CORN-012',
            'seed_date': '2024-04-01',
            'area': 15.0
        }
        crop = Crop.from_dict(data)

        assert crop.get_id() == 'CORN-012'
        assert crop.get_seed_date() == '2024-04-01'
        assert crop.get_area() == 15.0

    def test_from_dict_equals_regular_init(self):
        """Тест что from_dict создает объект эквивалентный обычному __init__."""
        data = {
            'id': 'BARLEY-013',
            'seed_date': '2024-05-10',
            'area': 8.0,
            'growth_stage': 3
        }
        crop1 = Crop.from_dict(data)
        crop2 = Crop('BARLEY-013', '2024-05-10', 8.0, 3)

        assert crop1 == crop2

    def test_from_dict_multiple_objects(self):
        """Тест создания нескольких объектов из словарей."""
        data_list = [
            {'id': 'WHEAT-014', 'seed_date': '2024-03-15', 'area': 10.0, 'growth_stage': 1},
            {'id': 'CORN-015', 'seed_date': '2024-04-01', 'area': 15.0, 'growth_stage': 2},
            {'id': 'BARLEY-016', 'seed_date': '2024-05-10', 'area': 5.0, 'growth_stage': 0}
        ]

        crops = [Crop.from_dict(data) for data in data_list]

        assert len(crops) == 3
        assert crops[0].get_id() == 'WHEAT-014'
        assert crops[1].get_id() == 'CORN-015'
        assert crops[2].get_id() == 'BARLEY-016'

    def test_from_dict_with_zero_area(self):
        """Тест создания объекта с нулевой площадью."""
        data = {
            'id': 'WHEAT-017',
            'seed_date': '2024-03-15',
            'area': 0.0,
            'growth_stage': 0
        }
        crop = Crop.from_dict(data)

        assert crop.get_area() == 0.0
        assert crop.get_crop_yield() == 0.0

    def test_from_dict_with_large_area(self):
        """Тест создания объекта с большой площадью."""
        data = {
            'id': 'WHEAT-018',
            'seed_date': '2024-03-15',
            'area': 1000.0,
            'growth_stage': 5
        }
        crop = Crop.from_dict(data)

        assert crop.get_area() == 1000.0
        assert crop.get_crop_yield() == 4500.0

    # def test_from_dict_updates_total_farm_area(self):
    #     """Тест что from_dict обновляет TOTAL_FARM_AREA."""
    #     global TOTAL_FARM_AREA
    #     initial_area = TOTAL_FARM_AREA

    #     data = {
    #         'id': 'WHEAT-019',
    #         'seed_date': '2024-03-15',
    #         'area': 25.0,
    #         'growth_stage': 1
    #     }
    #     crop = Crop.from_dict(data)

    #     assert TOTAL_FARM_AREA == initial_area + 25.0

    #     del crop
    #     assert TOTAL_FARM_AREA == initial_area

    def test_from_dict_is_classmethod(self):
        """Тест что from_dict является классовым методом."""
        assert hasattr(Crop.from_dict, '__self__')
        assert Crop.from_dict.__self__ is Crop


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
