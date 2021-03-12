import sqlite3

# Хранит ID пользователя и его состояние в дереве диалогов
class Users:
    def create_table(self):
        con = sqlite3.connect('Users.db')
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                    (id INTEGER NOT NULL PRIMARY KEY,
                    state INTEGER)
                    ''')
        con.commit()

    def get_state(self, user_id):
        con = sqlite3.connect('Users.db')
        cursor = con.cursor()
        cursor.execute(f'SELECT state FROM Users WHERE id = {user_id}')
        con.commit()
        state = cursor.fetchone()[0]
        print('get state:', state)
        return state
        

    def set_state(self, user_id, state):
        print('set state', state)
        con = sqlite3.connect('Users.db')
        cursor = con.cursor()
        cursor.execute('INSERT OR REPLACE INTO Users VALUES (?,?)', [user_id, state])
        con.commit()

# Хранит ID пользователя и группы, на которые он подписан
class Users_subs:
    pass

# Хранит имя преподавателя и его описание
class Professors:
    pass

# Хранит расписание всех групп
class Groups:
    pass