import xlrd, re

# следующие импорты нужны для импорта из родительского каталога
import sys
from pathlib import Path
# чтобы можно было импортировать из родительского каталога
sys.path[0] = str(Path(sys.path[0]).parent)
from dbworker import Schedule

# базовая функция
# отвечает за парсинг всех файлов
# читает из пути из xsl_paths
# передает каждый путь на вход parse_file()
def parse():
    # объект для работы с БД расписания
    schedule_db = Schedule()
    # удаляем таблицы, которые уже были в БД
    # т.к. данная функция вызывается только при полном обновлении расписания
    schedule_db.delete_all_tables()
    
    # файл со всеми путями до файлов расписания
    paths = open('Schedule/xsl_paths', 'r')

    for path in paths:
        parse_file(schedule_db, path[:-1])

# открывает файл с расписанием
# находит колонку с определенной группой
# передает на вход parse_group()
def parse_file(schedule_db, path):
    print(path)
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)

    for col in range(sheet.ncols):
        # т.к. в МИРЭА не могут симметрично размещать колонки
        # а еще обязательно нужно дописать в название группы какое-нибудь говно (в некоторых файлах)
        # приходится находить колонку с группой по регулярке
        if re.match(r'[А-Я]{4}-[0-9]{2}-[0-9]{2}', str(sheet.cell_value(rowx=1, colx=col))):
            print(sheet.cell_value(rowx=1, colx=col))
            parse_group(schedule_db, sheet, col)

# парсит колонку с группой, которую передала parse_file()
# вытаскивает:
# (день недели, вид недели, названия предмета,
# вид занятия, номер пары, аудитория, преподаватель)
# записывает эти данные в таблицу группы
def parse_group(schedule_db, sheet, group_col):
    # т.к. в названии группы может быть не только название группы (спасибо, мирэа)
    # находим по шаблону только название
    group = re.match(r'[А-Я]{4}-[0-9]{2}-[0-9]{2}', str(sheet.cell_value(rowx=1, colx=group_col))).group(0)
    
    # в БД для каждой группы создается отдельная таблица
    # в названии которой не могут присутствовать -
    # поэтому заменяем их на _
    group = group.replace('-', '_')

    # нарушаем все принципы ООП ради производительности
    # и выполняем SQL-операции прямо отсюда
    # если вызывать метод класса для вставки в таблицу,
    # тогда каждая операция будет выполняться отдельно
    # и запись всех данных в таблицу будет занимать время, стремящееся к бесконечности
    # если же заносить все данные в одной транзакции, тогда всё происходит довольно быстро
    con, cursor = schedule_db.get_con_cursor()

    # создаем новую таблицу под группу
    cursor.execute(f'''CREATE TABLE {group}
    (lesson_weekday INTEGER NOT NULL,
    lesson_weektype INTEGER NOT NULL,
    lesson_title TEXT NOT NULL,
    lesson_type TEXT NOT NULL,
    lesson_order INTEGER NOT NULL,
    lesson_classroom TEXT NOT NULL,
    lesson_teacher TEXT NOT NULL)
    ''')

    # начинаем транзакцию
    cursor.execute('BEGIN')
    # для групп, у которых максимум 6 пар
    # в таблице строка 3 - первая пара понедельника
    # строка 74 - последняя пара субботы
    for i in range(3, 74):

        # для каждой пары находим все необходимые данные
        # и записываем в таблицу группы
        if sheet.cell_value(rowx=i, colx=group_col) != '':
            weekday = get_weekday_by_row(row=i)
            weektype = 1 if sheet.cell_value(rowx=i, colx=4) == 'I' else 0
            title = sheet.cell_value(rowx=i, colx=group_col)
            type = sheet.cell_value(rowx=i, colx=group_col + 1)
            order = get_order_by_row(row=i)
            classroom = sheet.cell_value(rowx=i, colx=group_col + 3)
            teacher = sheet.cell_value(rowx=i, colx=group_col + 2)
            cursor.execute(f'INSERT INTO {group} VALUES (?,?,?,?,?,?,?)', [weekday, weektype, title, type, order, classroom, teacher])
    con.commit()

# находит день недели по текущей строке (исходя из файлов расписания)
# 0 - понедельник, 6 - воскресенье (как в datetime)
def get_weekday_by_row(row):
    if row < 15:
        return 0
    if row < 27:
        return 1
    if row < 39:
        return 2
    if row < 51:
        return 3
    if row < 63:
        return 4
    if row < 75:
        return 5

# т.к. в некоторых файлах столбец А пропущен (СПАСИБО, МИРЭА)
# приходится номер пары искать по столбцу
# исходя из принципов построения файлов расписания
def get_order_by_row(row):
    order = (row - 3) % 12
    if order == 0 or order == 1:
        return 1
    if order == 2 or order == 3:
        return 2
    if order == 4 or order == 5:
        return 3
    if order == 6 or order == 7:
        return 4
    if order == 8 or order == 9:
        return 5
    if order == 10 or order == 11:
        return 6


parse()