"""Работа с подписками на группы"""
from typing import Dict, List

import db


def init() -> None:
    stmt = """CREATE TABLE IF NOT EXISTS subs
        (user_id INTEGER,
        group_name TEXT)"""
    db.execute_stmt(stmt)

def set_group(user_id: int, group_name: str) -> None:
    db.insert('subs', {'user_id': user_id, 'group_name': group_name})

def get_groups(user_id: int) -> List[Dict]:
    stmt = f'SELECT group_name FROM subs WHERE user_id={user_id}'
    groups = db.fetchall(stmt)
    return [group[0] for group in groups]

def del_group(user_id: int, group_name: str) -> None:
    stmt = f'DELETE FROM subs WHERE (user_id = {user_id} AND group_name = "{group_name}")'
    db.execute_stmt(stmt)

def is_subscribed(user_id: int, group_name: str) -> None:
    stmt = f'''SELECT 1 FROM subs WHERE (user_id = {user_id}
        AND group_name = "{group_name}") limit 1'''
    return db.fetchone(stmt) is not None
