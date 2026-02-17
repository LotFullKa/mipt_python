"""
Тесты для задачи 8: добавление миксина Cruciferous для крестоцветных культур.

Тестируемая функциональность:
- Все тесты из задачи 7
- Миксин Cruciferous с приватными полями days_after_chem, is_infested
- Абстрактный метод can_be_harvested
- Класс Cabbage с Cruciferous:
  - Атрибут класса days_bef_harves_after_chem = 40
  - Метод can_be_harvested_after_chem
  - Метод apply_chemicals
"""

import pytest
from src import Crop, Cabbage, Rubus, SeasonalMixin, Cruciferous, GrowthStage, TOTAL_FARM_AREA


class TestCruciferousMixinBasic:
    """Тесты базовой функциональности миксина Cruciferous."""

    def test_cruciferous_is_abstract(self):
        """Тест что Cruciferous является абстрактным классом."""
        assert issubclass(Cruciferous, ABC)

    def test_cruciferous_has_abstract_method(self):
        """Тест что Cruciferous имеет абстрактный метод can_be_harvested."""
        assert hasattr(Cruciferous, 'can_be_harvested')
        assert getattr(Cruciferous.can_be_harvested, '__isabstractmethod__', False)

    def test_cruciferous_cannot_be_instantiated(self):
        """Тест что Cruciferous нельзя инстанцировать напрямую."""
        with pytest.raises(TypeError):
            Cruciferous()


class TestCruciferousFields:
    """Тесты приватных полей миксина Cruciferous."""

    def test_cabbage_has_days_after_chem(self):
        """Тест что капуста имеет поле days_after_chem."""
        cabbage = Cabbage("CAB-001", "2024-03-15", 10.0)
        assert hasattr(cabbage, '_Cruciferous__days_after_chem')

    def test_cabbage_has_is_infested(self):
        """Тест что капуста имеет поле is_infested."""
        cabbage = Cabbage("CAB-002", "2024-03-15", 10.0)
        assert hasattr(cabbage, '_Cruciferous__is_infested')

    def test_cabbage_initial_days_after_chem(self):
        """Тест начального значения days_after_chem."""
        cabbage = Cabbage("CAB-003", "2024-03-15", 10.0)
        assert cabbage.get_days_after_chem() == 0

    def test_cabbage_initial_is_infested(self):
        """Тест начального значения is_infested."""
        cabbage = Cabbage("CAB-004", "2024-03-15", 10.0)
        assert cabbage.get_is_infested() == 0

    def test_set_days_after_chem(self):
        """Тест установки days_after_chem."""
        cabbage = Cabbage("CAB-005", "2024-03-15", 10.0)
        cabbage.set_days_after_chem(10)
        assert cabbage.get_days_after_chem() == 10

    def test_set_is_infested(self):
        """Тест установки is_infested."""
        cabbage = Cabbage("CAB-006", "2024-03-15", 10.0)
        cabbage.set_is_infested(1)
        assert cabbage.get_is_infested() == 1


class TestCabbageWithCruciferous:
    """Тесты класса Cabbage с миксином Cruciferous."""

    def test_cabbage_is_cruciferous(self):
        """Тест что Cabbage наследуется от Cruciferous."""
        cabbage = Cabbage("CAB-007", "2024-03-15", 10.0)
        assert isinstance(cabbage, Cruciferous)
        assert isinstance(cabbage, Crop)
        assert isinstance(cabbage, Cabbage)

    def test_cabbage_has_class_attribute(self):
        """Тест что Cabbage имеет атрибут класса days_bef_harves_after_chem."""
        assert hasattr(Cabbage, 'days_bef_harves_after_chem')
        assert Cabbage.days_bef_harves_after_chem == 40

    def test_cabbage_class_attribute_value(self):
        """Тест значения атрибута класса."""
        cabbage = Cabbage("CAB-008", "2024-03-15", 10.0)
        assert cabbage.days_bef_harves_after_chem == 40

    def test_cabbage_has_can_be_harvested(self):
        """Тест что Cabbage имеет метод can_be_harvested."""
        cabbage = Cabbage("CAB-009", "2024-03-15", 10.0)
        assert hasattr(cabbage, 'can_be_harvested')
        assert callable(cabbage.can_be_harvested)

    def test_cabbage_has_can_be_harvested_after_chem(self):
        """Тест что Cabbage имеет метод can_be_harvested_after_chem."""
        cabbage = Cabbage("CAB-010", "2024-03-15", 10.0)
        assert hasattr(cabbage, 'can_be_harvested_after_chem')
        assert callable(cabbage.can_be_harvested_after_chem)

    def test_cabbage_has_apply_chemicals(self):
        """Тест что Cabbage имеет метод apply_chemicals."""
        cabbage = Cabbage("CAB-011", "2024-03-15", 10.0)
        assert hasattr(cabbage, 'apply_chemicals')
        assert callable(cabbage.apply_chemicals)


class TestCabbageCanBeHarvested:
    """Тесты метода can_be_harvested класса Cabbage."""

    def test_can_be_harvested_not_ready(self):
        """Тест что незрелая капуста не готова к сбору."""
        cabbage = Cabbage("CAB-012", "2024-03-15", 10.0, 0)
        assert cabbage.can_be_harvested() is False

    def test_can_be_harvested_ready(self):
        """Тест что зрелая капуста готова к сбору."""
        cabbage = Cabbage("CAB-013", "2024-03-15", 10.0, 5)
        assert cabbage.can_be_harvested() is True

    def test_can_be_harvested_different_stages(self):
        """Тест can_be_harvested для разных стадий роста."""
        for stage in range(5):
            cabbage = Cabbage(f"CAB-{14+stage}", "2024-03-15", 10.0, stage)
            assert cabbage.can_be_harvested() is False

        cabbage_ripe = Cabbage("CAB-019", "2024-03-15", 10.0, 5)
        assert cabbage_ripe.can_be_harvested() is True


class TestCabbageCanBeHarvestedAfterChem:
    """Тесты метода can_be_harvested_after_chem."""

    def test_can_be_harvested_after_chem_initial(self):
        """Тест что сразу после создания нельзя собирать урожай."""
        cabbage = Cabbage("CAB-020", "2024-03-15", 10.0)
        assert cabbage.can_be_harvested_after_chem() is False

    def test_can_be_harvested_after_chem_before_threshold(self):
        """Тест что до истечения 40 дней нельзя собирать урожай."""
        cabbage = Cabbage("CAB-021", "2024-03-15", 10.0)
        cabbage.set_days_after_chem(39)
        assert cabbage.can_be_harvested_after_chem() is False

    def test_can_be_harvested_after_chem_at_threshold(self):
        """Тест что ровно через 40 дней можно собирать урожай."""
        cabbage = Cabbage("CAB-022", "2024-03-15", 10.0)
        cabbage.set_days_after_chem(40)
        assert cabbage.can_be_harvested_after_chem() is True

    def test_can_be_harvested_after_chem_after_threshold(self):
        """Тест что после 40 дней можно собирать урожай."""
        cabbage = Cabbage("CAB-023", "2024-03-15", 10.0)
        cabbage.set_days_after_chem(50)
        assert cabbage.can_be_harvested_after_chem() is True

    def test_can_be_harvested_after_chem_various_days(self):
        """Тест для различных значений дней."""
        test_cases = [
            (0, False),
            (10, False),
            (20, False),
            (30, False),
            (39, False),
            (40, True),
            (41, True),
            (100, True)
        ]

        for days, expected in test_cases:
            cabbage = Cabbage(f"CAB-{24+days}", "2024-03-15", 10.0)
            cabbage.set_days_after_chem(days)
            assert cabbage.can_be_harvested_after_chem() is expected


class TestCabbageApplyChemicals:
    """Тесты метода apply_chemicals."""

    def test_apply_chemicals_resets_days(self):
        """Тест что apply_chemicals сбрасывает days_after_chem."""
        cabbage = Cabbage("CAB-124", "2024-03-15", 10.0)
        cabbage.set_days_after_chem(50)
        cabbage.apply_chemicals()
        assert cabbage.get_days_after_chem() == 0

    def test_apply_chemicals_resets_infested(self):
        """Тест что apply_chemicals сбрасывает is_infested."""
        cabbage = Cabbage("CAB-125", "2024-03-15", 10.0)
        cabbage.set_is_infested(1)
        cabbage.apply_chemicals()
        assert cabbage.get_is_infested() == 0

    def test_apply_chemicals_resets_both(self):
        """Тест что apply_chemicals сбрасывает оба поля."""
        cabbage = Cabbage("CAB-126", "2024-03-15", 10.0)
        cabbage.set_days_after_chem(30)
        cabbage.set_is_infested(1)

        cabbage.apply_chemicals()

        assert cabbage.get_days_after_chem() == 0
        assert cabbage.get_is_infested() == 0

    def test_apply_chemicals_multiple_times(self):
        """Тест многократного применения химикатов."""
        cabbage = Cabbage("CAB-127", "2024-03-15", 10.0)

        cabbage.set_days_after_chem(20)
        cabbage.apply_chemicals()
        assert cabbage.get_days_after_chem() == 0

        cabbage.set_days_after_chem(30)
        cabbage.apply_chemicals()
        assert cabbage.get_days_after_chem() == 0


class TestCabbageInfestation:
    """Тесты работы с заражением вредителями."""

    def test_infestation_scenario(self):
        """Тест сценария заражения и обработки."""
        cabbage = Cabbage("CAB-128", "2024-03-15", 10.0)

        # Изначально не заражена
        assert cabbage.get_is_infested() == 0

        # Заражение
        cabbage.set_is_infested(1)
        assert cabbage.get_is_infested() == 1

        # Обработка химикатами
        cabbage.apply_chemicals()
        assert cabbage.get_is_infested() == 0
        assert cabbage.get_days_after_chem() == 0


class TestCabbageHarvestScenario:
    """Тесты полного сценария сбора урожая."""

    def test_full_harvest_scenario(self):
        """Тест полного сценария от посадки до сбора урожая."""
        # Создание капусты
        cabbage = Cabbage("CAB-129", "2024-03-15", 10.0, 0)

        # Изначально не готова к сбору
        assert cabbage.can_be_harvested() is False

        # Заражение вредителями
        cabbage.set_is_infested(1)

        # Обработка химикатами
        cabbage.apply_chemicals()
        assert cabbage.get_is_infested() == 0
        assert cabbage.get_days_after_chem() == 0

        # Сразу после обработки нельзя собирать
        assert cabbage.can_be_harvested_after_chem() is False

        # Проходит 40 дней
        cabbage.set_days_after_chem(40)
        assert cabbage.can_be_harvested_after_chem() is True

        # Но культура еще не созрела
        assert cabbage.can_be_harvested() is False


class TestCropBasic:
    """Тесты базовой функциональности класса Crop."""

    def test_crop_creation(self):
        """Тест создания объекта Crop."""
        crop = Crop("WHEAT-001", "2024-03-15", 10.5, 0)
        assert crop.get_id() == "WHEAT-001"


class TestRubusBasic:
    """Тесты базовой функциональности класса Rubus."""

    def test_rubus_type(self):
        """Тест получения типа Rubus."""
        rubus = Rubus("RUB-001", "2024-03-15", 10.0, "малина")
        assert rubus.get_type() == "малина"


class TestTotalFarmArea:
    """Тесты глобальной переменной TOTAL_FARM_AREA."""

    def test_total_farm_area_with_cabbage(self):
        """Тест TOTAL_FARM_AREA с капустой."""
        global TOTAL_FARM_AREA
        initial_area = TOTAL_FARM_AREA

        cabbage = Cabbage("CAB-130", "2024-03-15", 15.0)
        assert TOTAL_FARM_AREA == initial_area + 15.0

        del cabbage
        assert TOTAL_FARM_AREA == initial_area
