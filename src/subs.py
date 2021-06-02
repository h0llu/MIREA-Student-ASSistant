"""Работа с подписками на группы"""
from typing import Dict, List

import db


def init() -> None:
    stmt = """CREATE TABLE IF NOT EXISTS subs
        (group_id INTEGER PRIMARY KEY,
        group_name TEXT)"""
    db.execute_stmt(stmt)

def set_group(group_id: int, group_name: str) -> None:
    db.insert('subs', {'group_id': group_id, 'group_name': group_name})

def get_groups(group_id: int) -> List[Dict]:
    stmt = f'SELECT group_name FROM subs WHERE group_id={group_id}'
    return db.fetchall(stmt)

def del_group(group_id: int, group_name: str) -> None:
    stmt = f'DELETE FROM Groups WHERE (group_id = {group_id} AND group_name = "{group_name}")'
    db.execute_stmt(stmt)

def is_subscribed(group_id: int, group_name: str) -> None:
    stmt = f'''SELECT 1 FROM Groups WHERE (group_id = {group_id}
        AND group_name = "{group_name}") limit 1'''
    return db.fetchone(stmt) is not None
