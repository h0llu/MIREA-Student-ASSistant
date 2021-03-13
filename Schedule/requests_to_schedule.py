# запросы на сайт, сохранение .xslx 
import requests
from bs4 import BeautifulSoup

# функция, вызываемая извне
# загружает файлы с расписанием
def update():
    page = requests.get('https://www.mirea.ru/schedule/')
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # тег, содержащий в себе списки по разным формам обучения
    # будем обрабатывать только бакалавриат, магистратуру и аспирантуру
    ul = soup.find('ul', 'uk-switcher')
    bac = ul.contents[1]
    mag = ul.contents[3]
    asp = ul.contents[5]

    download_xsl(bac)
    download_xsl(mag)
    download_xsl(asp)

# сохраняет все .xslx бакалавриата
def download_xsl(soup):
    # так как на сайте может быть расписание сессии
    # отберем только расписание занятий
    # для этого найдем все теги "Расписание занятий"
    classes_or_exams = soup.findAll('b', text='Расписание занятий:')
    
    # здесь будут храниться ссылки на .xslx
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
                if new_tag is not None and 'форма' in new_tag.contents[1].text:
                    new_tag = new_tag.findNextSibling('div')

    # теперь в списке links находятся теги ссылок
    # сохраним все найденные файлы в директории Schedule/Excels/
    for link in links:
        path = 'Schedule/Excels/' + link['href'][link['href'].rfind('/') + 1:]
        f = open(path, 'wb')
        resp = requests.get(link['href'])
        f.write(resp.content)
        f.close()

update()