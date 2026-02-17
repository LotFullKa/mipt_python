"""
Тесты для задачи 4: добавление property для доступа к приватным атрибутам.

Тестируемая функциональность:
- Все тесты из задачи 3
- Property геттеры (id, seed_date, area)
- Property сеттеры с валидацией:
  - id: проверка типа str
  - area: проверка типа float и >= 0.0
  - seed_date: проверка типа str и формата "ГГГГ-ММ-ДД"
"""

import pytest
from src import Crop, TOTAL_FARM_AREA


class TestPropertyGetters:
    """Тесты property геттеров."""

    def test_id_property_getter(self):
        """Тест получения id через property."""
        crop = Crop("WHEAT-001", "2024-03-15", 10.0)
        assert crop.id == "WHEAT-001"
        assert crop.id == crop.get_id()

    def test_seed_date_property_getter(self):
        """Тест получения seed_date через property."""
        crop = Crop("CORN-002", "2024-04-01", 15.0)
        assert crop.seed_date == "2024-04-01"
        assert crop.seed_date == crop.get_seed_date()

    def test_area_property_getter(self):
        """Тест получения area через property."""
        crop = Crop("BARLEY-003", "2024-05-10", 20.5)
        assert crop.area == 20.5
        assert crop.area == crop.get_area()

    def test_all_properties_accessible(self):
        """Тест что все property доступны."""
        crop = Crop("WHEAT-004", "2024-03-15", 10.0)
        # Не должно вызывать исключений
        _ = crop.id
        _ = crop.seed_date
        _ = crop.area


class TestIdPropertySetter:
    """Тесты property сеттера для id."""

    def test_id_setter_valid_string(self):
        """Тест установки валидного id."""
        crop = Crop("WHEAT-005", "2024-03-15", 10.0)
        crop.id = "CORN-005"
        assert crop.id == "CORN-005"

    def test_id_setter_empty_string(self):
        """Тест установки пустой строки."""
        crop = Crop("WHEAT-006", "2024-03-15", 10.0)
        crop.id = ""
        assert crop.id == ""

    def test_id_setter_invalid_type_int(self):
        """Тест установки id неверного типа (int)."""
        crop = Crop("WHEAT-007", "2024-03-15", 10.0)
        with pytest.raises(TypeError):
            crop.id = 123

    def test_id_setter_invalid_type_float(self):
        """Тест установки id неверного типа (float)."""
        crop = Crop("WHEAT-008", "2024-03-15", 10.0)
        with pytest.raises(TypeError):
            crop.id = 123.45

    def test_id_setter_invalid_type_none(self):
        """Тест установки id неверного типа (None)."""
        crop = Crop("WHEAT-009", "2024-03-15", 10.0)
        with pytest.raises(TypeError):
            crop.id = None

    def test_id_setter_invalid_type_list(self):
        """Тест установки id неверного типа (list)."""
        crop = Crop("WHEAT-010", "2024-03-15", 10.0)
        with pytest.raises(TypeError):
            crop.id = ["WHEAT-010"]


class TestSeedDatePropertySetter:
    """Тесты property сеттера для seed_date."""

    def test_seed_date_setter_valid_format(self):
        """Тест установки валидной даты."""
        crop = Crop("WHEAT-011", "2024-03-15", 10.0)
        crop.seed_date = "2024-04-20"
        assert crop.seed_date == "2024-04-20"

    def test_seed_date_setter_different_valid_dates(self):
        """Тест установки различных валидных дат."""
        crop = Crop("WHEAT-012", "2024-03-15", 10.0)

        valid_dates = ["2024-01-01", "2024-12-31", "2023-06-15", "2025-09-30"]
        for date in valid_dates:
            crop.seed_date = date
            assert crop.seed_date == date

    def test_seed_date_setter_invalid_type_int(self):
        """Тест установки даты неверного типа (int)."""
        crop = Crop("WHEAT-013", "2024-03-15", 10.0)
        with pytest.raises(TypeError):
            crop.seed_date = 20240315

    def test_seed_date_setter_invalid_type_none(self):
        """Тест установки даты неверного типа (None)."""
        crop = Crop("WHEAT-014", "2024-03-15", 10.0)
        with pytest.raises(TypeError):
            crop.seed_date = None

    def test_seed_date_setter_invalid_format_wrong_separator(self):
        """Тест установки даты с неверным разделителем."""
        crop = Crop("WHEAT-015", "2024-03-15", 10.0)
        with pytest.raises(ValueError):
            crop.seed_date = "2024/03/15"

    def test_seed_date_setter_invalid_format_no_separator(self):
        """Тест установки даты без разделителя."""
        crop = Crop("WHEAT-016", "2024-03-15", 10.0)
        with pytest.raises(ValueError):
            crop.seed_date = "20240315"

    def test_seed_date_setter_invalid_format_wrong_order(self):
        """Тест установки даты в неверном порядке."""
        crop = Crop("WHEAT-017", "2024-03-15", 10.0)
        with pytest.raises(ValueError):
            crop.seed_date = "15-03-2024"

    def test_seed_date_setter_invalid_format_short_year(self):
        """Тест установки даты с коротким годом."""
        crop = Crop("WHEAT-018", "2024-03-15", 10.0)
        with pytest.raises(ValueError):
            crop.seed_date = "24-03-15"

    def test_seed_date_setter_invalid_format_extra_chars(self):
        """Тест установки даты с лишними символами."""
        crop = Crop("WHEAT-019", "2024-03-15", 10.0)
        with pytest.raises(ValueError):
            crop.seed_date = "2024-03-15T00:00:00"


class TestAreaPropertySetter:
    """Тесты property сеттера для area."""

    def test_area_setter_valid_float(self):
        """Тест установки валидной площади (float)."""
        crop = Crop("WHEAT-020", "2024-03-15", 10.0)
        crop.area = 15.5
        assert crop.area == 15.5

    def test_area_setter_valid_int(self):
        """Тест установки валидной площади (int)."""
        crop = Crop("WHEAT-021", "2024-03-15", 10.0)
        crop.area = 20
        assert crop.area == 20.0

    def test_area_setter_zero(self):
        """Тест установки нулевой площади."""
        crop = Crop("WHEAT-022", "2024-03-15", 10.0)
        crop.area = 0.0
        assert crop.area == 0.0

    def test_area_setter_large_value(self):
        """Тест установки большой площади."""
        crop = Crop("WHEAT-023", "2024-03-15", 10.0)
        crop.area = 1000.0
        assert crop.area == 1000.0

    def test_area_setter_negative_value(self):
        """Тест установки отрицательной площади."""
        crop = Crop("WHEAT-024", "2024-03-15", 10.0)
        with pytest.raises(ValueError):
            crop.area = -5.0

    def test_area_setter_invalid_type_string(self):
        """Тест установки площади неверного типа (string)."""
        crop = Crop("WHEAT-025", "2024-03-15", 10.0)
        with pytest.raises(TypeError):
            crop.area = "10.0"

    def test_area_setter_invalid_type_none(self):
        """Тест установки площади неверного типа (None)."""
        crop = Crop("WHEAT-026", "2024-03-15", 10.0)
        with pytest.raises(TypeError):
            crop.area = None

    def test_area_setter_invalid_type_list(self):
        """Тест установки площади неверного типа (list)."""
        crop = Crop("WHEAT-027", "2024-03-15", 10.0)
        with pytest.raises(TypeError):
            crop.area = [10.0]

    def test_area_setter_updates_total_farm_area(self):
        """Тест что изменение площади обновляет TOTAL_FARM_AREA."""
        global TOTAL_FARM_AREA
        initial_area = TOTAL_FARM_AREA

        crop = Crop("WHEAT-028", "2024-03-15", 10.0)
        assert TOTAL_FARM_AREA == initial_area + 10.0

        crop.area = 20.0
        assert TOTAL_FARM_AREA == initial_area + 20.0

        crop.area = 5.0
        assert TOTAL_FARM_AREA == initial_area + 5.0

        del crop
        assert TOTAL_FARM_AREA == initial_area


class TestCropBasic:
    """Тесты базовой функциональности класса Crop."""

    def test_crop_creation(self):
        """Тест создания объекта Crop."""
        crop = Crop("WHEAT-029", "2024-03-15", 10.5, 0)
        assert crop.get_id() == "WHEAT-029"
        assert crop.get_seed_date() == "2024-03-15"
        assert crop.get_area() == 10.5

    def test_get_crop_yield(self):
        """Тест метода get_crop_yield."""
        crop = Crop("WHEAT-030", "2024-03-15", 10.0)
        assert crop.get_crop_yield() == 45.0


class TestCropRepr:
    """Тесты метода __repr__."""

    def test_repr_basic(self):
        """Тест базового представления объекта."""
        crop = Crop("WHEAT-031", "2024-03-15", 10.5, 2)
        repr_str = repr(crop)
        assert "WHEAT-031" in repr_str


class TestCropEquality:
    """Тесты метода __eq__."""

    def test_eq_same_values(self):
        """Тест равенства объектов с одинаковыми значениями."""
        crop1 = Crop("WHEAT-032", "2024-03-15", 10.0, 2)
        crop2 = Crop("WHEAT-032", "2024-03-15", 10.0, 2)
        assert crop1 == crop2


class TestFromDict:
    """Тесты классового метода from_dict."""

    def test_from_dict_basic(self):
        """Тест создания объекта из словаря."""
        data = {
            'id': 'WHEAT-033',
            'seed_date': '2024-03-15',
            'area': 10.5,
            'growth_stage': 2
        }
        crop = Crop.from_dict(data)

        assert crop.id == 'WHEAT-033'
        assert crop.seed_date == '2024-03-15'
        assert crop.area == 10.5
