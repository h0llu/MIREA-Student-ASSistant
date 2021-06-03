"""Работа с расписанием"""
import os
import requests

from typing import List, NamedTuple
import shutil
import re

from bs4 import BeautifulSoup
import xlrd


class Lesson(NamedTuple):
    """Структура занятия"""
    order: int
    title: str
    teacher: str
    classroom: str
    kind: str

class Weekday(NamedTuple):
    """Структура учебного дня"""
    group: str
    day: int
    week: int
    lessons: List[Lesson]


def get_schedule(group_name: str, day: int, week: int) -> Weekday:
    sheet = xlrd.open_workbook(
        f'{os.path.abspath("src/xlsx")}/{group_name[0]}{group_name[-2:]}.xlsx').sheet_by_index(0)
    # колонка с группой
    column = None
    for col in range(0, sheet.ncols):
        if group_name in str(sheet.cell_value(1, col)):
            column = col
    lessons = []
    for i in range(day * 12 + 3, day * 12 + 15):
        # находим соответствующую неделю и ячейку с парами
        if re.match(r'^[А-Як1-9].*', sheet.cell_value(i, column)) and week == i % 2:
            order = ((i - 3) % 12) // 2 + 1
            classroom = sheet.cell_value(i, column + 3).replace('\n', '/')
            kind = sheet.cell_value(i, column + 1).replace('\n', '/')
            title = sheet.cell_value(i, column).replace('\n', '/')
            teacher = sheet.cell_value(i, column + 2).replace('\n', '/')
            lessons.append(Lesson(order, title, teacher, classroom, kind))
    return output(Weekday(group_name, day, week, lessons))

def is_valid_group(group_name: str) -> bool:
    """Есть ли такая группа в скачанных файлах"""
    if group_name is None:
        return False
    path = f'{os.path.abspath("src/xlsx")}/{group_name[0]}{group_name[-2:]}.xlsx'
    if not os.path.exists(path):
        return False
    sheet = xlrd.open_workbook(path).sheet_by_index(0)
    for col in range(0, sheet.ncols):
        if group_name in str(sheet.cell_value(1, col)):
            return True
    return False

def format_groupname(raw_group_name: str) -> str:
    """Приводит группу к нужному формату
    изменяет маленькие буквы на большие
    и добавляет тире
    НЕ ИЗМЕНЯЕТ ЦИФРЫ, ЕСЛИ ЦИФРА ТОЛЬКО ОДНА"""
    if not re.match(r'[А-Яа-я]{4}\-?[0-9]{2}\-?[0-9]{2}', raw_group_name):
        return None
    
    group = raw_group_name.upper()
    if group[4] != '-':
        group = group[:4] + '-' + group[4:]
    if group[7] != '-':
        group = group[:7] + '-' + group[7:]
    return group

def output(weekday: Weekday) -> str:
    if len(weekday.lessons) == 0:
        return 'Пары отсутствуют'
    result = ''
    for lesson in weekday.lessons:
        if lesson.title == '':
            continue
        output = '{0} пара | {1} | {2}'.format(lesson.order, lesson.title, lesson.kind)
        if lesson.classroom != '':
            output += ' | {0}'.format(lesson.classroom)
        if lesson.teacher != '':
            output += ' | {0}'.format(lesson.teacher)
        output += '\n\n'
        result += output
    return result

def update_schedule() -> None:
    """Удалить старые файлы, загрузить новые"""
    if os.path.exists(os.path.abspath('src/xlsx')):
        shutil.rmtree(os.path.abspath('src/xlsx'))
    os.makedirs(os.path.abspath('src/xlsx'))

    page = requests.get('https://www.mirea.ru/schedule/')
    soup = BeautifulSoup(page.text, 'html.parser')
    ul = soup.find('ul', 'uk-switcher')
    # скачиваем бакалавров
    bac = ul.contents[1]
    download_schedule(bac)

def download_schedule(soup) -> None:
    """Загрузить расписание в папку xlsx/"""
    # отберем только расписание занятий
    classes = soup.findAll('b', text='Расписание занятий:')
    
    # ссылки на .xlsx
    links = []
    
    # далее в соответствии с вёрсткой сайта находим все ссылки
    # которые находятся под одним "Расписание занятий"
    # но до следующего такого тега
    for i in range(len(classes)):
            new_tag = classes[i].parent.findNextSibling('div').findNextSibling('div')
            while new_tag is not None and new_tag.contents[1].name == 'a':
                links.append(new_tag.contents[1])
                new_tag = new_tag.findNextSibling('div')
                # отбираем только очников
                if new_tag is not None and 'Очная форма:' == new_tag.contents[1].text:
                    new_tag = new_tag.findNextSibling('div')

    # удалим очно-заочников
    links = [link['href'] for link in links if 'О-З' not in link['href'][link['href'].rfind('/') + 1:]]
    
    # дадим файлам новые названия
    # чтобы при поиске было удобнее
    for link in links:
        new_name = ''
        # новые названия для файлов
        if 'ИИНТЕГУ' in link:
            new_name = 'Г'
        if 'ИИТ' in link:
            new_name = 'И'
        if 'КБиСП' in link:
            new_name = 'Б'
        if 'ИК' in link:
            new_name = 'К'
        if 'ИРТС' in link:
            new_name = 'Р'
        if 'ИТХТ' in link:
            new_name = 'Х'
        if 'ИЭП' in link:
            new_name = 'У'
        if 'ФТИ_Стромынка' in link:
            new_name = 'Т'
        if 'ФТИ' in link:
            new_name = 'Э'
        if '1к' in link or '1 курс' in link:
            new_name += '20'
        elif '2к' in link or '2 курс' in link:
            new_name += '19'
        elif '3к' in link or '3 курс' in link:
            new_name += '18'
        elif '4к' in link or '4 курс' in link:
            new_name += '17'
        elif '5к' in link or '5 курс' in link:
            new_name += '16'
        # сохраним все найденные файлы в директории xlsx/
        path = os.path.abspath('src/xlsx') + '/' + new_name + '.xlsx'
        f = open(path, 'wb')
        resp = requests.get(link)
        f.write(resp.content)
        f.close()
