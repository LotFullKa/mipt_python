"""
Тесты для задачи 7: добавление класса SeasonalMixin для учета сезонных особенностей.

Тестируемая функциональность:
- Все тесты из задачи 6
- Класс SeasonalMixin с __init__, set_season и seasonal_bonus
"""

import pytest
from src import Crop, Cabbage, Rubus, SeasonalMixin, GrowthStage, TOTAL_FARM_AREA


class TestSeasonalMixinBasic:
    """Тесты базовой функциональности SeasonalMixin."""

    def test_seasonal_mixin_exists(self):
        """Тест что класс SeasonalMixin существует."""
        assert SeasonalMixin is not None

    def test_seasonal_mixin_init(self):
        """Тест инициализации SeasonalMixin."""
        mixin = SeasonalMixin()
        assert hasattr(mixin, 'season')
        assert mixin.season is None

    def test_seasonal_mixin_has_methods(self):
        """Тест что SeasonalMixin имеет необходимые методы."""
        mixin = SeasonalMixin()
        assert hasattr(mixin, 'set_season')
        assert hasattr(mixin, 'seasonal_bonus')
        assert callable(mixin.set_season)
        assert callable(mixin.seasonal_bonus)


class TestSeasonalMixinSetSeason:
    """Тесты метода set_season."""

    def test_set_season_spring(self):
        """Тест установки весеннего сезона."""
        mixin = SeasonalMixin()
        mixin.set_season('весна')
        assert mixin.season == 'весна'

    def test_set_season_summer(self):
        """Тест установки летнего сезона."""
        mixin = SeasonalMixin()
        mixin.set_season('лето')
        assert mixin.season == 'лето'

    def test_set_season_autumn(self):
        """Тест установки осеннего сезона."""
        mixin = SeasonalMixin()
        mixin.set_season('осень')
        assert mixin.season == 'осень'

    def test_set_season_winter(self):
        """Тест установки зимнего сезона."""
        mixin = SeasonalMixin()
        mixin.set_season('зима')
        assert mixin.season == 'зима'

    def test_set_season_changes_value(self):
        """Тест изменения сезона."""
        mixin = SeasonalMixin()
        mixin.set_season('весна')
        assert mixin.season == 'весна'

        mixin.set_season('лето')
        assert mixin.season == 'лето'

    def test_set_season_custom_value(self):
        """Тест установки произвольного значения сезона."""
        mixin = SeasonalMixin()
        mixin.set_season('межсезонье')
        assert mixin.season == 'межсезонье'


class TestSeasonalMixinBonus:
    """Тесты метода seasonal_bonus."""

    def test_seasonal_bonus_spring(self):
        """Тест бонуса для весны."""
        mixin = SeasonalMixin()
        mixin.set_season('весна')
        assert mixin.seasonal_bonus() == 1.1

    def test_seasonal_bonus_summer(self):
        """Тест бонуса для лета."""
        mixin = SeasonalMixin()
        mixin.set_season('лето')
        assert mixin.seasonal_bonus() == 1.2

    def test_seasonal_bonus_autumn(self):
        """Тест бонуса для осени."""
        mixin = SeasonalMixin()
        mixin.set_season('осень')
        assert mixin.seasonal_bonus() == 1.0

    def test_seasonal_bonus_winter(self):
        """Тест бонуса для зимы."""
        mixin = SeasonalMixin()
        mixin.set_season('зима')
        assert mixin.seasonal_bonus() == 0.8

    def test_seasonal_bonus_no_season(self):
        """Тест бонуса когда сезон не установлен."""
        mixin = SeasonalMixin()
        assert mixin.seasonal_bonus() == 1.0

    def test_seasonal_bonus_unknown_season(self):
        """Тест бонуса для неизвестного сезона."""
        mixin = SeasonalMixin()
        mixin.set_season('неизвестный')
        assert mixin.seasonal_bonus() == 1.0

    def test_seasonal_bonus_returns_float(self):
        """Тест что seasonal_bonus возвращает float."""
        mixin = SeasonalMixin()
        mixin.set_season('весна')
        result = mixin.seasonal_bonus()
        assert isinstance(result, float)


class TestSeasonalMixinWithCrop:
    """Тесты использования SeasonalMixin с классом Crop."""

    def test_seasonal_crop_creation(self):
        """Тест создания культуры с сезонным миксином."""
        class SeasonalCrop(SeasonalMixin, Crop):
            pass

        crop = SeasonalCrop("WHEAT-001", "2024-03-15", 10.0)
        assert hasattr(crop, 'season')
        assert crop.season is None

    def test_seasonal_crop_set_season(self):
        """Тест установки сезона для культуры."""
        class SeasonalCrop(SeasonalMixin, Crop):
            pass

        crop = SeasonalCrop("WHEAT-002", "2024-03-15", 10.0)
        crop.set_season('весна')
        assert crop.season == 'весна'

    def test_seasonal_crop_bonus(self):
        """Тест получения бонуса для культуры."""
        class SeasonalCrop(SeasonalMixin, Crop):
            pass

        crop = SeasonalCrop("WHEAT-003", "2024-03-15", 10.0)
        crop.set_season('лето')
        assert crop.seasonal_bonus() == 1.2

    def test_seasonal_crop_has_crop_methods(self):
        """Тест что сезонная культура имеет методы Crop."""
        class SeasonalCrop(SeasonalMixin, Crop):
            pass

        crop = SeasonalCrop("WHEAT-004", "2024-03-15", 10.0)
        assert crop.get_id() == "WHEAT-004"
        assert crop.get_crop_yield() == 45.0

    def test_seasonal_crop_yield_with_bonus(self):
        """Тест расчета урожайности с учетом сезонного бонуса."""
        class SeasonalCrop(SeasonalMixin, Crop):
            def get_crop_yield_with_bonus(self):
                return self.get_crop_yield() * self.seasonal_bonus()

        crop = SeasonalCrop("WHEAT-005", "2024-03-15", 10.0)
        crop.set_season('весна')
        # base_yield = 4.5 * 10.0 = 45.0
        # with_bonus = 45.0 * 1.1 = 49.5
        assert crop.get_crop_yield_with_bonus() == 49.5


class TestSeasonalMixinWithCabbage:
    """Тесты использования SeasonalMixin с классом Cabbage."""

    def test_seasonal_cabbage_creation(self):
        """Тест создания капусты с сезонным миксином."""
        class SeasonalCabbage(SeasonalMixin, Cabbage):
            pass

        cabbage = SeasonalCabbage("CAB-001", "2024-03-15", 10.0)
        assert hasattr(cabbage, 'season')
        assert cabbage.season is None

    def test_seasonal_cabbage_set_season(self):
        """Тест установки сезона для капусты."""
        class SeasonalCabbage(SeasonalMixin, Cabbage):
            pass

        cabbage = SeasonalCabbage("CAB-002", "2024-03-15", 10.0)
        cabbage.set_season('осень')
        assert cabbage.season == 'осень'

    def test_seasonal_cabbage_head_amount(self):
        """Тест расчета количества кочанов для сезонной капусты."""
        class SeasonalCabbage(SeasonalMixin, Cabbage):
            pass

        cabbage = SeasonalCabbage("CAB-003", "2024-03-15", 10.0)
        assert cabbage.head_amount() == 15.0

    def test_seasonal_cabbage_bonus(self):
        """Тест получения бонуса для капусты."""
        class SeasonalCabbage(SeasonalMixin, Cabbage):
            pass

        cabbage = SeasonalCabbage("CAB-004", "2024-03-15", 10.0)
        cabbage.set_season('весна')
        assert cabbage.seasonal_bonus() == 1.1


class TestSeasonalMixinWithRubus:
    """Тесты использования SeasonalMixin с классом Rubus."""

    def test_seasonal_rubus_creation(self):
        """Тест создания Rubus с сезонным миксином."""
        class SeasonalRubus(SeasonalMixin, Rubus):
            pass

        rubus = SeasonalRubus("RUB-001", "2024-03-15", 10.0, "малина")
        assert hasattr(rubus, 'season')
        assert rubus.season is None

    def test_seasonal_rubus_set_season(self):
        """Тест установки сезона для Rubus."""
        class SeasonalRubus(SeasonalMixin, Rubus):
            pass

        rubus = SeasonalRubus("RUB-002", "2024-03-15", 10.0, "ежевика")
        rubus.set_season('лето')
        assert rubus.season == 'лето'

    def test_seasonal_rubus_type(self):
        """Тест получения типа для сезонного Rubus."""
        class SeasonalRubus(SeasonalMixin, Rubus):
            pass

        rubus = SeasonalRubus("RUB-003", "2024-03-15", 10.0, "ежемалина")
        assert rubus.get_type() == "ежемалина"

    def test_seasonal_rubus_bonus(self):
        """Тест получения бонуса для Rubus."""
        class SeasonalRubus(SeasonalMixin, Rubus):
            pass

        rubus = SeasonalRubus("RUB-004", "2024-03-15", 10.0, "малина")
        rubus.set_season('зима')
        assert rubus.seasonal_bonus() == 0.8


class TestCropBasic:
    """Тесты базовой функциональности класса Crop."""

    def test_crop_creation(self):
        """Тест создания объекта Crop."""
        crop = Crop("WHEAT-006", "2024-03-15", 10.5, 0)
        assert crop.get_id() == "WHEAT-006"

    def test_is_harvested(self):
        """Тест метода is_harvested."""
        crop1 = Crop("WHEAT-007", "2024-03-15", 10.0, 0)
        assert crop1.is_harvested() == 0

        crop2 = Crop("WHEAT-008", "2024-03-15", 10.0, 5)
        assert crop2.is_harvested() == 1


class TestCabbageBasic:
    """Тесты базовой функциональности класса Cabbage."""

    def test_cabbage_head_amount(self):
        """Тест расчета количества кочанов."""
        cabbage = Cabbage("CAB-005", "2024-03-15", 10.0)
        assert cabbage.head_amount() == 15.0


class TestRubusBasic:
    """Тесты базовой функциональности класса Rubus."""

    def test_rubus_type(self):
        """Тест получения типа Rubus."""
        rubus = Rubus("RUB-005", "2024-03-15", 10.0, "малина")
        assert rubus.get_type() == "малина"


class TestTotalFarmArea:
    """Тесты глобальной переменной TOTAL_FARM_AREA."""

    def test_total_farm_area_with_seasonal_crop(self):
        """Тест TOTAL_FARM_AREA с сезонной культурой."""
        class SeasonalCrop(SeasonalMixin, Crop):
            pass

        global TOTAL_FARM_AREA
        initial_area = TOTAL_FARM_AREA

        crop = SeasonalCrop("WHEAT-009", "2024-03-15", 15.0)
        assert TOTAL_FARM_AREA == initial_area + 15.0

        del crop
        assert TOTAL_FARM_AREA == initial_area
