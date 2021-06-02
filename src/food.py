"""Работа с едой"""
from typing import Dict, List, NamedTuple

import db

class Food(NamedTuple):
    """Структура единицы пищи из Виктории"""
    name: str
    price: int
    sale: int


# допишу позже