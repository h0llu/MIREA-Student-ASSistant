import sqlite3, os

# Хранит ID пользователя и его состояние в дереве диалогов
class Users:
    __path__ = 'Databases/Users.db'
    def __init__(self):
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
        return state

# Хранит ID пользователя и группы, на которые он подписан
class Users_subs:
    __path__ = 'Databases/Users_subs.db'
    def __init__(self):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Groups
        (id INTEGER NOT NULL,
        group TEXT NOT NULL)''')
        con.commit()

    def set_group(self, id, group):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('INSERT OR REPLACE INTO Groups VALUES (?,?)', [id, group])
        con.commit()

    def get_groups(self, id):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'SELECT group FROM Groups WHERE id = {id}')
        con.commit()
        return cursor.fetchall()

    def del_group(self, id, group):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'DELETE FROM Groups WHERE ( id = {id} AND group = {group} )')
        con.commit()

# Хранит расписание в виде
# (имя группы, день недели, вид недели, названия предмета,
# вид занятия, номер пары, аудитория, преподаватель)
class Schedule:
    __path__ = 'Databases/Schedule.db'
    def set_lesson(self, group, weekday, weektype, title, type, order, classroom, teacher):
        group = group.replace('-', '_')
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {group}
        (lesson_weekday TEXT NOT NULL,
        lesson_weektype TEXT NOT NULL,
        lesson_title TEXT NOT NULL,
        lesson_type TEXT NOT NULL,
        lesson_order INTEGER NOT NULL,
        lesson_classroom TEXT NOT NULL,
        lesson_teacher TEXT NOT NULL)
        ''')
        cursor.execute(f'INSERT INTO {group} VALUES (?,?,?,?,?,?,?)', [weekday, weektype, title, type, order, classroom, teacher])
        con.commit()

    def get_con_cursor(self):
        con = sqlite3.connect(self.__path__)
        return con, con.cursor()

    def get_lesson(self, group, weekday, weektype):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'''SELECT * FROM {group} WHERE
        ( lesson_weekday = {weekday} AND lesson_weektype = {weektype})''')
        return cursor.fetchall()

    def is_valid_group(self, group):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'SELECT * FROM {group}')
        if len(cursor.fetchall()) != 0:
            return True
        return False

    def delete_all_tables(self):
        if os.path.exists(self.__path__):
            os.remove(self.__path__)


# Хранит имя преподавателя и его описание
class Professors:
    __path__ = 'Databases/Professors.db'
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
    __path__ = 'Databases/Victoria.db'
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