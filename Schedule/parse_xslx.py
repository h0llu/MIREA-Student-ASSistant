import xlrd
import re

# следующие импорты нужны для импорта dbworker из родительского каталога
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

    # parse_file(schedule_db, paths.readline()[:-1])
    for path in paths:
        parse_file(schedule_db, path[:-1])

# открывает файл с расписанием
# находит колонку с определенной группой
# передает на вход parse_group()
def parse_file(schedule_db, path):
    sheet = xlrd.open_workbook(path).sheet_by_index(0)
    for col in range(0, sheet.ncols):
        # т.к. в МИРЭА не могут симметрично размещать колонки
        # а еще обязательно нужно дописать в название группы какое-нибудь говно (в некоторых файлах)
        # приходится находить колонку с группой по регулярке
        if re.match(r'[А-Я]{4}-[0-9]{2}-[0-9]{2}', str(sheet.cell_value(rowx=1, colx=col))):
            parse_group(schedule_db, sheet, col)

# парсит колонку с группой, которую передала parse_file()
# вытаскивает:
# (день недели, вид недели, названия предмета,
# вид занятия, номер пары, аудитория, преподаватель)
# записывает эти данные в таблицу группы
def parse_group(schedule_db, sheet, col):
    group = sheet.cell_value(rowx=1, colx=col)

    weekdays = []
    weektypes = []
    titles = []
    types = []
    orders = []
    classrooms = []
    teachers = []
    
    # для групп, у которых максимум 6 пар
    # в таблице строка 3 - первая пара понедельника
    # строка 74 - последняя пара субботы
    for i in range(3, 74):
        # для каждой пары находим все необходимые данные
        # и записываем в список
        # затем записываем в таблицу
        if re.match(r'^[А-Як1-9]+', str(sheet.cell_value(rowx=i, colx=col))):
            weekdays.append(get_weekday_by_row(rowx=i))
            weektypes.append(1 if sheet.cell_value(rowx=i, colx=4) == 'I' else 0)
            titles.append(sheet.cell_value(rowx=i, colx=col))
            types.append(sheet.cell_value(rowx=i, colx=col + 1))
            orders.append(get_order_by_row(rowx=i))
            classrooms.append(sheet.cell_value(rowx=i, colx=col + 3))
            teachers.append(sheet.cell_value(rowx=i, colx=col + 2))
    schedule_db.set_lessons(len(weekdays), group, weekdays, weektypes, titles,
    types, orders, classrooms, teachers)

# находит день недели по текущей строке (исходя из файлов расписания)
# 0 - понедельник, 6 - воскресенье (как в datetime)
def get_weekday_by_row(rowx):
    if rowx < 15:
        return 0
    if rowx < 27:
        return 1
    if rowx < 39:
        return 2
    if rowx < 51:
        return 3
    if rowx < 63:
        return 4
    if rowx < 75:
        return 5

# т.к. в некоторых файлах столбец А пропущен (СПАСИБО, МИРЭА)
# приходится номер пары искать по столбцу
# исходя из принципов построения файлов расписания
def get_order_by_row(rowx):
    order = (rowx - 3) % 12
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