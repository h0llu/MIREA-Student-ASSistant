"""Работа с состояниями пользователей в диалоге
'None': ввод игнорируется
'Group': ввод группы
'From': ввод первой аудитории (откуда)
'To': ввод второй аудитории (куда)
'Name': ввод имени препода
'Description': ввод описания препода"""
import db


def init() -> None:
    stmt = """CREATE TABLE IF NOT EXISTS states
        (id INTEGER PRIMARY KEY,
        state TEXT)"""
    db.execute_stmt(stmt)
    db.execute_stmt('DELETE FROM states')

def get_state(user_id: int) -> str:
    stmt = f'SELECT state FROM states WHERE id={user_id}'
    state = db.fetchone(stmt)
    return state[0] if state is not None else 'None'

def set_state(user_id: int, state: str) -> None:
    db.insert('states', {'id': user_id, 'state': state})
