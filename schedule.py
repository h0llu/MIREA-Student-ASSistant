import requests # запросы на сайт с расписанием
from bs4 import BeautifulSoup # парсинг HTML-страницы с расписанием
import xlrd # парсинг .xlsx файлов

class Schedule:
    # при валидации сохраняем путь к файлу и колонку с группой
    # чтобы потом не искать их заново
    __xlsx_path__ = ''
    __group_col__ = 0

    # удаляет уже имеющиеся файлы с расписанием
    # скачивает новые
    def update(self):
        page = requests.get('https://www.mirea.ru/schedule/')
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # тег, содержащий в себе списки по разным формам обучения
        # будем обрабатывать только бакалавриат
        ul = soup.find('ul', 'uk-switcher')
        bac = ul.contents[1]

        # в файл записываются пути до всех .xlsx 
        paths = open('xlsx_paths', 'w')
        self.__download__(bac, paths)
        paths.close()

    # сохраняет все .xlsx
    def __download__(self, soup, paths):
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
            first_letter = ''
            
            if 'ИИНТЕГУ' in link:
                first_letter = 'Г'
            elif 'ИИТ' in link:
                first_letter = 'И'
            elif 'КБиСП' in link:
                first_letter = 'Б'
            elif 'ИК' in link:
                first_letter = 'К'
            elif 'ИРТС' in link:
                first_letter = 'Р'
            elif 'ИТХТ' in link:
                first_letter = 'Х'
            elif 'ИЭП' in link:
                first_letter = 'У'
            elif 'ФТИ' in link:
                first_letter = 'Э'
            elif 'ФТИ_Стромынка' in link:
                first_letter = 'Т'

            path = 'Excels/' + first_letter + '/' + link[link.rfind('/') + 1:]
            paths.write(path + '\n')
            f = open(path, 'wb')
            resp = requests.get(link)
            f.write(resp.content)
            f.close()

    # проверить, есть ли такая группа в файлах
    # есть есть, тогда сохраним колонку, чтобы потом заново не искать её
    # если нет, тогда либо нет такой группы
    # либо это тупые аспирантики, либо это группы-дубликаты (в разных корпусах с одним названием)
    def is_valid_group(self, group) -> bool:
        paths = open('xlsx_paths', 'r')
        s = ''
        s.find
        for path in paths:
            if group[0] == path[path.find('/') + 1]:
                sheet = xlrd.open_workbook(path[:-1]).sheet_by_index(0)
                for col in range(0, sheet.ncols):
                    if group in str(sheet.cell_value(1, col)):
                        self.__xlsx_path__ = path[:-1]
                        self.__group_col__ = col
                        return True
        
        return False
    
    # найти группу среди файлов
    def get_group(self, group, weekday, weektype):
        sheet = xlrd.open_workbook(self.__xlsx_path__).sheet_by_index(0)
        # на всякий случай проверим
        assert group in str(sheet.cell_value(1, self.__group_col__)), \
                f'{group} not in {str(sheet.cell_value(rowx=1, colx=self.__group_col__))}'
        # выберем нужные строки по дню недели
        start, end = {
            0: (3, 15),
            1: (15, 27),
            2: (27, 39),
            3: (39, 51),
            4: (51, 63),
            5: (63, 75)}.get(weekday)

        # информация для вывода
        lessons = []

        for i in range(start, end):
            # находим соответствующую неделю и непустую ячейку
            if sheet.cell_value(i, self.__group_col__) != '' and \
                weektype == i % 2:
                lesson = {}
                lesson['lesson_order'] = ((i - 3) % 12) // 2 + 1
                lesson['lesson_classroom'] = sheet.cell_value(i, self.__group_col__ + 3).replace('\n', ' ')
                lesson['lesson_type'] = sheet.cell_value(i, self.__group_col__ + 1).replace('\n', ' ')
                lesson['lesson_title'] = sheet.cell_value(i, self.__group_col__).replace('\n', ' ')
                lesson['lesson_teacher'] = sheet.cell_value(i, self.__group_col__ + 2).replace('\n', ' ')
                lessons.append(lesson)
        
        return lessons

    def display_schedule(self, group, weekday, weektype):
        lessons = self.get_group(group, weekday, weektype)
    
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
            if lesson['lesson_teacher'] is None:
                output += ' | {0}'.format(lesson['lesson_teacher'])
            output += '\n'
            
            result += output

        return result
