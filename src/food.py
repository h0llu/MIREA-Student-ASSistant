"""Работа с едой"""
from typing import Dict, List, NamedTuple

from parservic import parse_drinks, parse_snacks, parse_energy, parse_bread
import db

class Food(NamedTuple):
    """Структура единицы пищи из Виктории"""
    category: str
    name: str
    price: str
    sale: str


def init() -> None:
    stmt = '''CREATE TABLE IF NOT EXISTS victoria
        (category text,
        title text,
        price text,
        sale text)'''
    db.execute_stmt(stmt)

def get_food(category: str) -> List[Food]:
    """Получить еду по категории"""
    
    stmt = f'SELECT * FROM victoria WHERE category="{category}"'
    foods = db.fetchall(stmt)
    return([food[1:] for food in foods])

def update_vic() -> None:
    """Обновить БД, скачать инфу с сайта"""
    drinks = parse_drinks()
    snacks = parse_snacks()
    energies = parse_energy()
    breads = parse_bread()

    for drink in drinks:
        db.insert('victoria', {
            'category': 'drink',
            'title': drink.get('title'),
            'price': drink.get('price'),
            'sale': drink.get('sale')
        })
    for snack in snacks:
        db.insert('victoria', {
            'category': 'snack',
            'title': snack.get('title'),
            'price': snack.get('price'),
            'sale': snack.get('sale')
        })
    for energy in energies:
        db.insert('victoria', {
            'category': 'energy',
            'title': energy.get('title'),
            'price': energy.get('price'),
            'sale': energy.get('sale')
        })
    for bread in breads:
        db.insert('victoria', {
            'category': 'bread',
            'title': bread.get('title'),
            'price': bread.get('price'),
            'sale': bread.get('sale')
        })
