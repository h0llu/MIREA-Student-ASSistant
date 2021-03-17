import sqlite3, os

# Хранит ID пользователя и его состояние в дереве диалогов
class Users:
    __path__ = 'Databases/Users.db'
    def __init__(self):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute('DELETE FROM Users')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                    (id INTEGER NOT NULL PRIMARY KEY,
                    state INTEGER NOT NULL)
                    ''')
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
    __group__ = ''
    def get_con_cursor(self):
        con = sqlite3.connect(self.__path__)
        return con, con.cursor()

    def set_group(self, group):
        group = group.replace('.', '_').replace('-', '_').replace('/', '_')
        self.__group__ = group.replace(' ', '_').replace('(', '_').replace(')', '_')

    def set_lessons(self, len, group,
    weekdays, weektypes, titles, types, orders, classrooms, teachers):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()

        group = group.replace(',', '').replace('.', '_').replace('-', '_').replace('\n', '_')
        group = group.replace(' ', '_').replace('(', '_').replace(')', '_').replace('/', '_')

        # создаем новую таблицу под группу
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {group}
        (lesson_weekday INTEGER NOT NULL,
        lesson_weektype INTEGER NOT NULL,
        lesson_title TEXT NOT NULL,
        lesson_type TEXT,
        lesson_order INTEGER NOT NULL,
        lesson_classroom TEXT,
        lesson_teacher TEXT)
        ''')

        # открываем транзакцию
        cursor.execute('BEGIN TRANSACTION')
        for i in range(0, len):
            cursor.execute(f'INSERT INTO {group} VALUES (?,?,?,?,?,?,?)', 
            [weekdays[i], weektypes[i], titles[i],
            types[i], orders[i], classrooms[i], teachers[i]])

        # завершаем транзакцию
        cursor.execute('COMMIT')

    def get_lesson(self, weekday, weektype):
        if self.curr_group_name == '':
            return
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        cursor.execute(f'''SELECT * FROM {self.curr_group_name} WHERE
        ( lesson_weekday = {weekday} AND lesson_weektype = {weektype})''')
        return cursor.fetchall()

    def is_valid_group(self, group):
        con = sqlite3.connect(self.__path__)
        cursor = con.cursor()
        group = group.replace('.', '_').replace('-', '_').replace('/', '_')
        group = group.replace(' ', '_').replace('(', '_').replace(')', '_')
        cursor.execute(f"SELECT name FROM sqlite_master WHERE name = '{group}'")
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