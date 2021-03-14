import xlrd

# базовая функция
# отвечает за парсинг файлов
# читает из пути из xsl_paths
# передает каждый путь на вход parse_file()
def parse(group, weekday, weektype):
    paths = open('Schedule/xsl_paths', 'r')

    for path in paths:
        lessons = parse_file(group, weekday, weektype, path[:-1])
        if lessons is not None:
            paths.close()
            return lessons
    return None

# открывает файл с расписанием
# находит колонку с определенной группой
# передает на вход parse_group()
def parse_file(group, weekday, weektype, path):
    print(path)
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)

    for col in range(sheet.ncols):
        # ищем ячейку, в которой хранится название группы
        if group in str(sheet.cell_value(rowx=1, colx=col)):
            print(sheet.cell_value(rowx=1, colx=col))
            return parse_group(weekday, weektype, sheet, col)
    return None          

# парсит колонку с группой, которую передала parse_file()
# вытаскивает:
# (день недели, вид недели, названия предмета,
# вид занятия, номер пары, аудитория, преподаватель)
def parse_group(weekday, weektype, sheet, group_col):
    lessons = []
    start, end = get_row_by_weekday(weekday)
    if (weektype == 2):
        start += 1

    for i in range(start, end, 2):
        if sheet.cell_value(rowx=i, colx=group_col) != '':
            lesson = {}
            lesson['lesson_title'] = sheet.cell_value(rowx=i, colx=group_col)
            lesson['lesson_type'] = sheet.cell_value(rowx=i, colx=group_col + 1)
            lesson['lesson_order'] = str(int(sheet.cell_value(rowx=(i - (i + 1) % 2), colx=1)))
            lesson['lesson_classroom'] = sheet.cell_value(rowx=i, colx=group_col + 3)
            lesson['lesson_teacher'] = sheet.cell_value(rowx=i, colx=group_col + 2)

            lessons.append(lesson)
    
    return lessons

#  возвращает номер строки для определенного дня с учетом построения эксельки
def get_row_by_weekday(weekday):
    if (weekday == 'Понедельник'):
        return 3, 15
    if (weekday == 'Вторник'):
        return 15, 27
    if (weekday == 'Среда'):
        return 27, 39
    if (weekday == 'Четверг'):
        return 39, 51
    if (weekday == 'Пятница'):
        return 51, 63
    if (weekday == 'Суббота'):
        return 63, 76

def get_weekday_by_row(row):
    if row < 15:
        return 'Понедельник'
    if row < 27:
        return 'Вторник'
    if row < 39:
        return 'Среда'
    if row < 51:
        return 'Четверг'
    if row < 63:
        return 'Пятница'
    if row < 75:
        return 'Суббота'

# lessons = parse('ИНБО-05-19', 'Понедельник', 2)
# for lesson in lessons:
        # print('{0} пара | {1} | {2} | {3} - {4}'.format(lesson['lesson_order'], lesson['lesson_type'],
        # lesson['lesson_classroom'], lesson['lesson_title'], lesson['lesson_teacher']))
