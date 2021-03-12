import sqlite3

# Хранит ID пользователя и его состояние в дереве диалогов
class Users:
    __path__ = 'Databases/Users.db'
    def create_table(self):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                    (id INTEGER NOT NULL PRIMARY KEY,
                    state INTEGER NOT NULL)
                    ''')
        con.commit()

    def set_state(self, user_id, state):
        print('set state', state)
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('INSERT OR REPLACE INTO Users VALUES (?,?)', [user_id, state])
        con.commit()

    def get_state(self, user_id):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'SELECT state FROM Users WHERE id = {user_id}')
        con.commit()
        state = cursor.fetchone()[0]
        print('get state:', state)
        return state

# Хранит ID пользователя и группы, на которые он подписан
class Users_subs:
    __path__ = 'Databases/Users_subs.db'
    def create_table(self):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Groups
        (id INTEGER NOT NULL,
        group TEXT NOT NULL)''')
        con.commit()

    def set_group(self, id, group):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('INSERT OR REPLACE INTO Groups VALUES (?, ?)', [id, group])
        con.commit()

    def get_groups(self, id):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'SELECT group FROM Groups WHERE id = {id}')
        con.commit()
        return cursor.fetchall()

# Хранит имя преподавателя и его описание
class Professors:
    __path__ = 'Databases/Professors.db'
    def create_table(self):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Professors
        (name TEXT NOT NULL PRIMARY KEY,
        description TEXT NOT NULL)''')
        con.commit()

    def set_description(self, name, description):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('INSERT OR REPLACE INTO Professors VALUES (?, ?)', [name, description])
        con.commit()

    def add_description(self, name, add):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'SELECT description FROM Professors WHERE name = {name}')
        description = cursor.fetchone()[0]
        description += '\n' + add
        cursor.execute('INSERT OR REPLACE INTO Professors VALUES (?, ?)', [name, description])
        con.commit()

# Хранит скидки (просто еду) из Виктории
class Victoria:
    __path__ = 'Databases/Victoria.db'
    def create_table(self):
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
        cursor.execute('INSERT OR REPLACE INTO Victoria VALUES (?, ?, ?)', [name, price, weight])
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

# Хранит расписание всех групп
class Groups:
    pass