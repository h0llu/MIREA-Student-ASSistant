import requests # запросы на сайт с расписанием
import xlrd # парсинг .xlsx файлов
import os # есть ли файл с такой группой
import re
from bs4 import BeautifulSoup # парсинг HTML-страницы с расписанием
from dbworker import Schedule_last_request # для хранения последней запрошенной группы

class Schedule:
    schedule_db = Schedule_last_request()

    # удаляет уже имеющиеся файлы с расписанием
    # скачивает новые
    def update(self):
        # создать директорию, если не существует
        if not os.path.exists("/home/h0llu/Everything/University/2 course/4 semester/TRPP/Project/src/Excels/"):
            os.makedirs("/home/h0llu/Everything/University/2 course/4 semester/TRPP/Project/src/Excels")


        page = requests.get('https://www.mirea.ru/schedule/')
        soup = BeautifulSoup(page.text, 'html.parser')

        # тег, содержащий в себе списки по разным формам обучения
        # будем обрабатывать только бакалавриат
        ul = soup.find('ul', 'uk-switcher')
        bac = ul.contents[1]

        self.__download__(bac)

    # сохраняет все .xlsx
    def __download__(self, soup):
        # так как на сайте может быть расписание сессии
        # отберем только расписание занятий
        # для этого найдем все теги "Расписание занятий"
        classes_or_exams = soup.findAll('b', text='Расписание занятий:')
        
        # здесь будут храниться ссылки на .xlsx
        links = []
        
        # далее в соответствии с вёрсткой (уебанской) сайта находим все ссылки
        # которые находятся под одним "Расписание занятий"
        # но до следующего такого тега
        # сохраняем ссылки в список
        for i in range(len(classes_or_exams)):
                new_tag = classes_or_exams[i].parent.findNextSibling('div').findNextSibling('div')
                while new_tag is not None and new_tag.contents[1].name == 'a':
                    links.append(new_tag.contents[1])
                    new_tag = new_tag.findNextSibling('div')
                    # отбираем только очников, потому что заочники СОСУТ ЖОПУ
                    # (при парсинге .xlsx возникает проблема, так как заочники учатся на 7-8 парах)
                    if new_tag is not None and 'Очная форма:' == new_tag.contents[1].text:
                        new_tag = new_tag.findNextSibling('div')

        # удалим очно-заочников (они тоже сосут)
        links = [link['href'] for link in links if 'О-З' not in link['href'][link['href'].rfind('/') + 1:]]
        
        # теперь в списке links находятся ссылки
        # сохраним все найденные файлы в директории Schedule/Excels/
        for link in links:
            # будем сохранять файлы разных факультетов в разные папки
            # папки будут называться по первой букве групп
            # которые учатся на этом факультете
            new_name = ''
            
            if 'ИИНТЕГУ' in link:
                new_name = 'Г'
            elif 'ИИТ' in link:
                new_name = 'И'
            elif 'КБиСП' in link:
                new_name = 'Б'
            elif 'ИК' in link:
                new_name = 'К'
            elif 'ИРТС' in link:
                new_name = 'Р'
            elif 'ИТХТ' in link:
                new_name = 'Х'
            elif 'ИЭП' in link:
                new_name = 'У'
            elif 'ФТИ_Стромынка' in link:
                new_name = 'Т'
            elif 'ФТИ' in link:
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

            path = "/home/h0llu/Everything/University/2 course/4 semester/TRPP/Project/src/Excels/" + new_name + '.xlsx'
            f = open(path, 'wb')
            resp = requests.get(link)
            f.write(resp.content)
            f.close()

    # проверить, есть ли такая группа в файлах
    # есть есть, тогда сохраним колонку, чтобы потом заново не искать её
    # если нет, тогда либо нет такой группы
    # либо это тупые аспирантики, либо это группы-дубликаты (в разных корпусах с одним названием)
    def is_valid_group(self, user_id, group) -> bool:
        path = f"/home/h0llu/Everything/University/2 course/4 semester/TRPP/Project/src/Excels/{group[0]}{group[-2:]}.xlsx"
        if not os.path.exists(path):
            return False
        sheet = xlrd.open_workbook(path).sheet_by_index(0)
        for col in range(0, sheet.ncols):
            if group in str(sheet.cell_value(1, col)):
                self.schedule_db.set_group(user_id, group, col)
                return True
        return False
    
    # найти группу среди файлов
    def __find__(self, group, group_col, weekday, weektype):
        sheet = xlrd.open_workbook(f"/home/h0llu/Everything/University/2 course/4 semester/TRPP/Project/src/Excels/{group[0]}{group[-2:]}.xlsx").sheet_by_index(0)
        # на всякий случай проверим, верно ли введена группа
        assert group in str(sheet.cell_value(1, group_col)), \
                f'{group} not in {str(sheet.cell_value(rowx=1, colx=group_col))}'

        # информация для вывода
        lessons = []

        for i in range(weekday * 12 + 3, weekday * 12 + 15):
            # находим соответствующую неделю и ячейку с парами
            if re.match(r'^[А-Як1-9].*', sheet.cell_value(i, group_col)) and \
                weektype == i % 2:
                lesson = {}
                lesson['lesson_order'] = ((i - 3) % 12) // 2 + 1
                lesson['lesson_classroom'] = sheet.cell_value(i, group_col + 3).replace('\n', '/')
                lesson['lesson_type'] = sheet.cell_value(i, group_col + 1).replace('\n', '/')
                lesson['lesson_title'] = sheet.cell_value(i, group_col).replace('\n', '/')
                lesson['lesson_teacher'] = sheet.cell_value(i, group_col + 2).replace('\n', '/')
                lessons.append(lesson)
        
        return lessons

    # возвращает строку для вывода в чате
    # расписание на день weekday (weektype неделя)
    def get_schedule(self, user_id, weekday, weektype):
        # если weekday - воскресенье
        if weekday == 6:
            return 'Выходной день'

        lessons = self.__find__(self.schedule_db.get_group(user_id),
                                self.schedule_db.get_col(user_id),
                                weekday, weektype)
    
        if len(lessons) == 0:
            return 'Пары отсутствуют'

        result = ''
        for lesson in lessons:
            if lesson['lesson_title'] == '':
                continue
            output = '{0} пара | {1} | {2}'.format(lesson['lesson_order'],
                                                   lesson['lesson_title'],
                                                   lesson['lesson_type'])
            if lesson['lesson_classroom'] is not None:
                output += ' | {0}'.format(lesson['lesson_classroom'])
            if lesson['lesson_teacher'] is not None:
                output += ' | {0}'.format(lesson['lesson_teacher'])
            output += '\n\n'
            result += output
        return result

