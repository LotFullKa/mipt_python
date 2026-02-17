from enum import Enum

class Season(Enum):
    WINTER = 0
    SUMMER = 1

class SeasonalMixin:
    def __init__(self):
        self.__season = None

    @property
    def season(self):
        return self.__season

    @season.setter
    def season(self, val):
        self.__season = val

    def seasonal_bonus(self):
        return self.__season == Season.SUMMER
