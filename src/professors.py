"""Работа с описанием преподавателей"""
from typing import List, NamedTuple

import db

class Professor(NamedTuple):
    """Структура преподавателя"""
    name: str
    description: List[str]


def get_description(name: str) -> Professor:
    """Получить все описания по преподавателю"""
    profs = db.fetchall(f'SELECT description FROM professors WHERE professor={name}')
    return Professor(name, [prof[0] for prof in profs])

def add_description(name: str, description: str) -> None:
    """Добавить описание преподавателю"""
    db.insert('professors', {
        'professor': name,
        'description': description
    })

def get_professors() -> List[str]:
    """Возвращает имена всех преподавателей"""
    profs = db.fetchall('SELECT professor FROM professors')

    return [prof[0] for prof in profs]
