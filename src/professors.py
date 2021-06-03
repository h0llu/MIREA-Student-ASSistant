"""Работа с описанием преподавателей"""
from typing import List, NamedTuple

import db


def init() -> None:
    """Создать изначальную таблицу"""
    stmt = '''CREATE TABLE IF NOT EXISTS professors
        (name TEXT,
        description TEXT)'''
    db.execute_stmt(stmt)

def get_descriptions(name: str) -> List[str]:
    """Получить все описания по преподавателю"""
    profs = db.fetchall(f'SELECT description FROM professors WHERE name="{name}"')
    return [prof[0] for prof in profs]

def add_name(name: str) -> None:
    """Добавить временное имя"""
    db.insert('professors', {
        'name': name,
        'description': 'Temp'
    })

def add_description(description: str) -> None:
    """Добавить описание преподавателю"""
    stmt = 'SELECT name FROM professors WHERE description="Temp"'
    name = db.fetchone(stmt)[0]
    stmt = 'DELETE FROM professors WHERE description="Temp"'
    db.execute_stmt(stmt)
    db.insert('professors', {
        'name': name,
        'description': description
    })

def get_professors() -> List[str]:
    """Возвращает имена всех преподавателей"""
    profs = db.fetchall('SELECT name FROM professors')
    
    return list(set([prof[0] for prof in profs]))
