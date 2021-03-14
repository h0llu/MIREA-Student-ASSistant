# запросы на сайт, сохранение .xlsx 
import requests
from bs4 import BeautifulSoup
# для удаления старых файлов
import os

# функция, вызываемая извне
# загружает файлы с расписанием
def update():
    # удалим все скаченные файлы
    files = os.listdir('Schedule/Excels')
    for f in files:
        os.remove('Schedule/Excels/' + f)
    page = requests.get('https://www.mirea.ru/schedule/')
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # тег, содержащий в себе списки по разным формам обучения
    # будем обрабатывать только бакалавриат, магистратуру
    ul = soup.find('ul', 'uk-switcher')
    bac = ul.contents[1]
    mag = ul.contents[3]

    # в файл записываются пути до всех .xlsx 
    paths = open('Schedule/xsl_paths', 'w')
    download_xlsx(bac, paths)
    download_xlsx(mag, paths)
    paths.close()

# сохраняет все .xlsx
def download_xlsx(soup, paths):
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
        path = 'Schedule/Excels/' + link[link.rfind('/') + 1:]
        paths.write(path + '\n')
        f = open(path, 'wb')
        resp = requests.get(link)
        f.write(resp.content)
        f.close()

update()