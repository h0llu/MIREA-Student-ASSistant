from config import db_file
import sqlite3

def set_con():
    con = sqlite3.connect(db_file)
    cursor = con.cursor()
    return con, cursor

def create_table():
    con, cursor = set_con()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                  (id INTEGER NOT NULL PRIMARY KEY,
                   state INTEGER)
                   ''')
    con.commit()

def get_state(user_id):
    con, cursor = set_con()
    cursor.execute(f'SELECT state FROM Users WHERE id = {user_id}')
    returned = cursor.fetchone()
    con.commit()
    return returned[0]
    

def set_state(user_id, state):
    con, cursor = set_con()
    cursor.execute('INSERT OR REPLACE INTO Users VALUES (?,?)', [user_id, state])
    con.commit()
