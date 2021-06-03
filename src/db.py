import os

from typing import Dict, List, Tuple
import sqlite3


def insert(table:str, col_values: Dict):
    conn = sqlite3.connect(os.path.abspath('db/mirea.db'))
    cursor = conn.cursor()
    
    columns = ', '.join(col_values.keys())
    values = [tuple(col_values.values())]
    placeholders = ', '.join( '?' * len(col_values.keys()) )
    cursor.executemany(
        f'INSERT OR REPLACE INTO {table}'
        f'({columns})'
        f'VALUES ({placeholders})',
        values)
    conn.commit()


def fetchone(stmt: str) -> Tuple:
    conn = sqlite3.connect(os.path.abspath('db/mirea.db'))
    cursor = conn.cursor()
    
    cursor.execute(stmt)
    return cursor.fetchone()


def fetchall(stmt: str) -> List[Tuple]:
    conn = sqlite3.connect(os.path.abspath('db/mirea.db'))
    cursor = conn.cursor()
    
    cursor.execute(stmt)
    return cursor.fetchall()


def delete(table: str, row_id: int) -> None:
    conn = sqlite3.connect(os.path.abspath('db/mirea.db'))
    cursor = conn.cursor()
    
    row_id = int(row_id)
    cursor.execute(f'DELETE FROM {table} where id={row_id}')
    conn.commit()


def execute_stmt(stmt: str, values: List = []) -> None:
    conn = sqlite3.connect(os.path.abspath('db/mirea.db'))
    cursor = conn.cursor()
    
    cursor.execute(stmt, values)
    conn.commit()
