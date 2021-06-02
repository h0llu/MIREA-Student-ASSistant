"""Работа с состояниями пользователей в диалоге
'none': ввод игнорируется
'group': ввод группы
'from': ввод первой аудитории (откуда)
'to': ввод второй аудитории (куда)
'name': ввод имени препода
'description': ввод описания препода"""
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
    return state[0] if state is not None else 'none'

def set_state(user_id: int, state: str) -> None:
    db.insert('states', {'id': user_id, 'state': state})
