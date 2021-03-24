import sqlite3


# Хранит ID пользователя и его состояние в дереве диалогов
class Users:
    __path__ = 'Mirea-Stud-Assistant/Databases/Users.db'
    def __init__(self):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                    (id INTEGER NOT NULL PRIMARY KEY,
                    state INTEGER NOT NULL)
                    ''')
        cursor.execute('DELETE FROM Users')
        con.commit()

    def set_state(self, user_id, state):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('INSERT OR REPLACE INTO Users VALUES (?,?)', [user_id, state])
        con.commit()

    def get_state(self, user_id):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'SELECT state FROM Users WHERE id = {user_id}')
        con.commit()
        return cursor.fetchone()[0]

    def is_user(self, user_id):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'SELECT * FROM Users WHERE id = {user_id}')
        return cursor.fetchone() is not None

# Хранит последнюю запрошенную от каждого из пользователей
class Schedule_last_request:
    __path__ = 'Mirea-Stud-Assistant/Databases/Schedule.db'
    def __init__(self):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Schedule
                       (user_id INTEGER NOT NULL PRIMARY KEY,
                        last_group TEXT NOT NULL,
                        last_group_col INTEGER NOT NULL)''')
        con.commit()

    def set_group(self, id, group, group_col):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('INSERT OR REPLACE INTO Schedule VALUES (?,?,?)',
        [id, group, group_col])
        con.commit()

    def get_group(self, id):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'SELECT last_group FROM Schedule WHERE user_id = {id}')
        return cursor.fetchone()[0]

    def get_col(self, id):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'SELECT last_group_col FROM Schedule WHERE user_id = {id}')
        return cursor.fetchone()[0]

# Хранит ID пользователя и группы, на которые он подписан
class Subs:
    __path__ = 'Mirea-Stud-Assistant/Databases/Subs.db'
    def __init__(self):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Groups
                       (id INTEGER NOT NULL,
                        group_name TEXT NOT NULL)''')
        con.commit()

    def set_group(self, id, group):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('INSERT OR REPLACE INTO Groups VALUES (?,?)', [id, group])
        con.commit()

    def get_groups(self, id):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'SELECT group_name FROM Groups WHERE id = {id}')
        con.commit()
        return cursor.fetchall()

    def is_subscribed(self, id, group):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'SELECT 1 FROM Groups WHERE (id = {id} AND group_name = "{group}") limit 1')
        return cursor.fetchone() is not None
        

    def del_group(self, id, group):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'DELETE FROM Groups WHERE (id = {id} AND group_name = "{group}")')
        con.commit()

# Хранит имя преподавателя и его описание
class Professors:
    __path__ = 'Mirea-Stud-Assistant/Databases/Professors.db'
    def __init__(self):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Professors
        (name TEXT NOT NULL PRIMARY KEY,
        description TEXT NOT NULL)''')
        con.commit()

    def set_description(self, name, description):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('INSERT OR REPLACE INTO Professors VALUES (?,?)', [name, description])
        con.commit()

    def add_description(self, name, add):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'SELECT description FROM Professors WHERE name = {name}')
        description = cursor.fetchone()[0]
        description += '\n' + add
        cursor.execute('INSERT OR REPLACE INTO Professors VALUES (?,?)', [name, description])
        con.commit()

    def get_description(self, name):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'SELECT description FROM Professors WHERE name = {name}')
        con.commit()
        return cursor.fetchone()[0]

# Хранит скидки (просто еду) из Виктории
class Victoria:
    __path__ = 'Mirea-Stud-Assistant/Databases/Victoria.db'
    def __init__(self):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Victoria
                    (name TEXT NOT NULL PRIMARY KEY,
                    price INTEGER NOT NULL,
                    weight INTEGER NOT NULL)''')
        con.commit()

    def set_food(self, name, price, weight):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('INSERT OR REPLACE INTO Victoria VALUES (?,?,?)', [name, price, weight])
        con.commit()

    def get_food(self, name):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'SELECT * FROM Victoria WHERE name = {name}')
        con.commit()
        return cursor.fetchone()

    def get_all_food(self):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('SELECT * FROM Victoria')
        con.commit()
        return cursor.fetchall()

