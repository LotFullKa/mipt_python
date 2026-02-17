"""
Тесты для задачи 5: добавление Enum для стадий роста и метода is_harvested.

Тестируемая функциональность:
- Все тесты из задачи 4
- Enum для стадий роста (0-5)
- Метод is_harvested (0 для стадий 0-4, 1 для стадии 5)
"""

import pytest
from src import Crop, GrowthStage, TOTAL_FARM_AREA


class TestGrowthStageEnum:
    """Тесты перечисления GrowthStage."""

    def test_growth_stage_enum_exists(self):
        """Тест что перечисление GrowthStage существует."""
        assert issubclass(GrowthStage, Enum)

    def test_growth_stage_values(self):
        """Тест значений перечисления."""
        assert GrowthStage.SEED.value == 0
        assert GrowthStage.SPROUT.value == 1
        assert GrowthStage.VEGETATIVE.value == 2
        assert GrowthStage.BUDDING.value == 3
        assert GrowthStage.FLOWERING.value == 4
        assert GrowthStage.RIPENING.value == 5

    def test_growth_stage_count(self):
        """Тест количества стадий роста."""
        assert len(GrowthStage) == 6

    def test_growth_stage_from_value(self):
        """Тест создания стадии из значения."""
        for i in range(6):
            stage = GrowthStage(i)
            assert stage.value == i

    def test_growth_stage_invalid_value(self):
        """Тест создания стадии с неверным значением."""
        with pytest.raises(ValueError):
            GrowthStage(6)
        with pytest.raises(ValueError):
            GrowthStage(-1)


class TestIsHarvested:
    """Тесты метода is_harvested."""

    def test_is_harvested_stage_0(self):
        """Тест is_harvested для стадии 0 (SEED)."""
        crop = Crop("WHEAT-001", "2024-03-15", 10.0, 0)
        assert crop.is_harvested() == 0

    def test_is_harvested_stage_1(self):
        """Тест is_harvested для стадии 1 (SPROUT)."""
        crop = Crop("WHEAT-002", "2024-03-15", 10.0, 1)
        assert crop.is_harvested() == 0

    def test_is_harvested_stage_2(self):
        """Тест is_harvested для стадии 2 (VEGETATIVE)."""
        crop = Crop("WHEAT-003", "2024-03-15", 10.0, 2)
        assert crop.is_harvested() == 0

    def test_is_harvested_stage_3(self):
        """Тест is_harvested для стадии 3 (BUDDING)."""
        crop = Crop("WHEAT-004", "2024-03-15", 10.0, 3)
        assert crop.is_harvested() == 0

    def test_is_harvested_stage_4(self):
        """Тест is_harvested для стадии 4 (FLOWERING)."""
        crop = Crop("WHEAT-005", "2024-03-15", 10.0, 4)
        assert crop.is_harvested() == 0

    def test_is_harvested_stage_5(self):
        """Тест is_harvested для стадии 5 (RIPENING)."""
        crop = Crop("WHEAT-006", "2024-03-15", 10.0, 5)
        assert crop.is_harvested() == 1

    def test_is_harvested_returns_int(self):
        """Тест что is_harvested возвращает int."""
        crop1 = Crop("WHEAT-007", "2024-03-15", 10.0, 0)
        crop2 = Crop("WHEAT-008", "2024-03-15", 10.0, 5)

        assert isinstance(crop1.is_harvested(), int)
        assert isinstance(crop2.is_harvested(), int)

    def test_is_harvested_all_stages(self):
        """Тест is_harvested для всех стадий."""
        expected = [0, 0, 0, 0, 0, 1]

        for stage, expected_result in enumerate(expected):
            crop = Crop(f"WHEAT-{stage+9}", "2024-03-15", 10.0, stage)
            assert crop.is_harvested() == expected_result


class TestCropWithGrowthStage:
    """Тесты класса Crop с использованием GrowthStage."""

    def test_crop_creation_with_growth_stage(self):
        """Тест создания культуры с указанием стадии роста."""
        crop = Crop("WHEAT-015", "2024-03-15", 10.0, 3)
        assert crop.get_id() == "WHEAT-015"

    def test_crop_default_growth_stage(self):
        """Тест создания культуры без указания стадии (должна быть 0)."""
        crop = Crop("WHEAT-016", "2024-03-15", 10.0)
        assert crop.is_harvested() == 0

    def test_crop_repr_with_growth_stage(self):
        """Тест repr с указанием стадии роста."""
        crop = Crop("WHEAT-017", "2024-03-15", 10.0, 2)
        repr_str = repr(crop)
        assert "2" in repr_str

    def test_crop_equality_different_growth_stages(self):
        """Тест неравенства культур с разными стадиями роста."""
        crop1 = Crop("WHEAT-018", "2024-03-15", 10.0, 2)
        crop2 = Crop("WHEAT-018", "2024-03-15", 10.0, 3)
        assert crop1 != crop2

    def test_crop_equality_same_growth_stages(self):
        """Тест равенства культур с одинаковыми стадиями роста."""
        crop1 = Crop("WHEAT-019", "2024-03-15", 10.0, 4)
        crop2 = Crop("WHEAT-019", "2024-03-15", 10.0, 4)
        assert crop1 == crop2


class TestPropertyGetters:
    """Тесты property геттеров."""

    def test_id_property_getter(self):
        """Тест получения id через property."""
        crop = Crop("WHEAT-020", "2024-03-15", 10.0)
        assert crop.id == "WHEAT-020"

    def test_seed_date_property_getter(self):
        """Тест получения seed_date через property."""
        crop = Crop("CORN-021", "2024-04-01", 15.0)
        assert crop.seed_date == "2024-04-01"

    def test_area_property_getter(self):
        """Тест получения area через property."""
        crop = Crop("BARLEY-022", "2024-05-10", 20.5)
        assert crop.area == 20.5


class TestPropertySetters:
    """Тесты property сеттеров."""

    def test_id_setter_valid(self):
        """Тест установки валидного id."""
        crop = Crop("WHEAT-023", "2024-03-15", 10.0)
        crop.id = "CORN-023"
        assert crop.id == "CORN-023"

    def test_id_setter_invalid_type(self):
        """Тест установки id неверного типа."""
        crop = Crop("WHEAT-024", "2024-03-15", 10.0)
        with pytest.raises(TypeError):
            crop.id = 123

    def test_seed_date_setter_valid(self):
        """Тест установки валидной даты."""
        crop = Crop("WHEAT-025", "2024-03-15", 10.0)
        crop.seed_date = "2024-04-20"
        assert crop.seed_date == "2024-04-20"

    def test_seed_date_setter_invalid_format(self):
        """Тест установки даты с неверным форматом."""
        crop = Crop("WHEAT-026", "2024-03-15", 10.0)
        with pytest.raises(ValueError):
            crop.seed_date = "2024/03/15"

    def test_area_setter_valid(self):
        """Тест установки валидной площади."""
        crop = Crop("WHEAT-027", "2024-03-15", 10.0)
        crop.area = 15.5
        assert crop.area == 15.5

    def test_area_setter_negative(self):
        """Тест установки отрицательной площади."""
        crop = Crop("WHEAT-028", "2024-03-15", 10.0)
        with pytest.raises(ValueError):
            crop.area = -5.0


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


class TestFromDict:
    """Тесты классового метода from_dict."""

    def test_from_dict_basic(self):
        """Тест создания объекта из словаря."""
        data = {
            'id': 'WHEAT-031',
            'seed_date': '2024-03-15',
            'area': 10.5,
            'growth_stage': 2
        }
        crop = Crop.from_dict(data)

        assert crop.id == 'WHEAT-031'
        assert crop.seed_date == '2024-03-15'
        assert crop.area == 10.5
        assert crop.is_harvested() == 0

    def test_from_dict_with_ripening_stage(self):
        """Тест создания объекта из словаря со стадией созревания."""
        data = {
            'id': 'WHEAT-032',
            'seed_date': '2024-03-15',
            'area': 10.5,
            'growth_stage': 5
        }
        crop = Crop.from_dict(data)
        assert crop.is_harvested() == 1


class TestTotalFarmArea:
    """Тесты глобальной переменной TOTAL_FARM_AREA."""

    def test_total_farm_area_increases_on_init(self):
        """Тест увеличения TOTAL_FARM_AREA при создании объекта."""
        global TOTAL_FARM_AREA
        initial_area = TOTAL_FARM_AREA

        crop = Crop("WHEAT-033", "2024-03-15", 15.0)
        assert TOTAL_FARM_AREA == initial_area + 15.0

        del crop

    def test_total_farm_area_decreases_on_del(self):
        """Тест уменьшения TOTAL_FARM_AREA при удалении объекта."""
        global TOTAL_FARM_AREA
        initial_area = TOTAL_FARM_AREA

        crop = Crop("CORN-034", "2024-04-01", 20.0)
        assert TOTAL_FARM_AREA == initial_area + 20.0

        del crop
        assert TOTAL_FARM_AREA == initial_area
