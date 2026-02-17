import re

from enum import Enum

class GrowthStage(Enum):
    SEED = 0
    SPROUT = 1
    VEGETATIVE = 2
    BUDDING = 3
    FLOWERING= 4
    RIPENING = 5
    SPOILED = 6

class ValidationError(Exception):
    pass

TOTAL_FARM_AREA = 1.0

class Crop:
    # Петров Владислав
    def __init__(self, id: str, seed_date: str, area: float, growth_stage: GrowthStage = GrowthStage.SEED):
        self.__id = id
        # re
        if re.match(r'(\d{4})-(\d{2})-(\d{2})', seed_date):
            self.__seed_date =  seed_date
        else:
            raise ValidationError()
        global TOTAL_FARM_AREA
        TOTAL_FARM_AREA += area
        self.__area = area
        self.__stage = growth_stage

    # Павликов Сергей
    @property
    def seed_date(self) -> str:
        return self.__seed_date

    @seed_date.setter
    def seed_date(self, date :  str) -> None:
        if not isinstance(date, str) or not re.match(r'(\d{4})-(\d{2})-(\d{2})', date):
            return ValueError("Incorrect date")
        self.__seed_date = date



    def __eq__(self, other : Crop) -> bool:
        if not isinstance(other, Crop):
            return NotImplemented
        return self.__id == other.__id and self.__area == other.__area and self.__stage == other.__stage and self.__seed_date == other.__seed_date

    def __del__(self) -> None:
        global TOTAL_FARM_AREA
        TOTAL_FARM_AREA -= self.__area

    # Власов Алексей
    def get_area(self) -> float:
        return self.__area

    # Кильметов Данил
    @property
    def area(self):
        return self.__area

    # Кильметов Данил
    @area.setter
    def area(self, val: float):
        if isinstance(val, float):
            self.__area = val

    def get_id(self) -> str:
        return self.__id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, vall: str):
        if isinstance(vall, str):
            self.__id = vall
        else:
            raise TypeError("vall is not str")

    def __repr__(self):
        return f"""Crop(
        id={self.__id}
        seed_date={self.__seed_date}
        area={self.__area}
        growth_stage={self.__stage}
        )"""


    #Кильметов Данил
    def get_crop_yield(self) -> float:
        "Возвращает что-то там"
        return 4.5 * self.__area


    @classmethod
    def from_dict(cls, d: dict):
        return Crop(**d)

    def is_harvested(self):
        return self.__stage == GrowthStage.RIPENING
