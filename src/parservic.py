# кнопки
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# напитки:  вода, сок и чай
#           тут кола классическая (<= 0.5 л), фанта, спрайт, 
#                       сок (палпи), фьюзти (1 вкус), липтон (1 вкус), вода свят. ист (газ. и без газа)
#           всего: 10 наименований
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# снеки: шоколадные батончики, чипсеки и сухареки
#        всего: 21 наименование
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# хлебобулки: булочки и прочая выпечка
#             всего: 18 наименований
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# мама не одобрит: энергетики
#                  тут Red Bull, Drive Me, Gorilla, Adrenaline Rush, Burn
#                  всего: 7 наименований
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

##############################################################################################

import requests
from bs4 import BeautifulSoup

HEADERS = {'user-agent': 
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
           'accept':
           'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

# URL - ссылка на страницу
# params - опциональный аргумент, принимающий доп. инфу о странице (номер страницы); по умолчанию params=None
def get_html(url, params=None):
    # вернет содержимое html-страницы
    return requests.get(url, headers=HEADERS, params=params, verify=False)

# url - ссылка на раздел магазина
def get_pages_count(url):
    # Я ПЫТАЛСЯ ПОСЧИТАТЬ КОЛ-ВО СТРАНИЦ НОРМАЛЬНО, НО ТАМ САЙТ ГОВНА
    # получить кол-во страниц магазина
    if(url.find('voda_soki_napitki')): # раздел НАПИТКИ
        if(url.find('soki_nektary_smuzi_2')): # раздел с соками
            return 9 # кол-во стр у соков
        elif (url.find('gazirovannye_napitki_limonady')): # раздел с газ. напитками
            return 7 # кол-во стр у газ. напитков
        elif (url.find('kholodnyy_chay_kofe_1')): # раздел с чаем
            return 2 # кол-во стр у чая
        elif (url.find('voda')): # раздел с водой
            return 7 # кол-во стр у воды
    elif (url.find('chipsy_sukhariki_sneki_1')): # раздел СНЕКИ (чиспы)
        return 8 # кол-во стр у чипсов и сухариков
    elif (url.find('shokolad_pasty_1')): # раздел СНЕКИ (шоколадные батончики) 
        return 12 # кол-во стр у шоколадок
    elif (url.find('khleb_bulochki_lepeshki_lavash_1')): # раздел ХЛЕБОБУЛКИ
        return 7 # кол-во стр у хлеба
    elif (url.find('energeticheskie_napitki')): # раздел МАМА НЕ ОДОБРИТ (раздел с энергетиками)
        return 1 # кол-во стр у энергетиков

# html - html-код страницы
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='card-product product-container')
    goods = []
    for item in items:
        # проверка существования скидки и корректная запись старой и новой цены
        if (item.find('div', class_='card-product__price card-product__price_new')): # скидка есть
            # запись старой цены
            price = item.find('div', class_='card-product__old-price').get_text(strip=True)
            # запись цены со скидкой
            sale = item.find('div', class_='card-product__price card-product__price_new').get_text(strip=True)
        else: # скидки нет
            sale = ''
            price = item.find('div', class_='card-product__price').get_text(strip=True)
        # добавление информации о товарах
        goods.append({
            'title': item.find('a', class_='card-product__title-link product-name').get_text(),
            'price': price,
            'sale': sale
        })
    return goods

# удаление повторяющихся эл-тов списка
def delete_repeat(items):
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            if items[i].get('title') == items[j].get('title'):
                items[j].clear()
    return list(filter(None, items))


##############################################################################################
# НАПИТКИ
##############################################################################################
URL_JUICE = 'https://www.victoria-group.ru/catalog/voda_soki_napitki/soki_nektary_smuzi_2/'

URL_GAS = 'https://www.victoria-group.ru/catalog/voda_soki_napitki/gazirovannye_napitki_limonady/'

URL_TEA = 'https://www.victoria-group.ru/catalog/voda_soki_napitki/kholodnyy_chay_kofe_1/'

URL_WATER = 'https://www.victoria-group.ru/catalog/voda_soki_napitki/voda/'

def parse_juice(url):
    html = get_html(url)
    if (html.status_code == 200): # все ОК
        # получить контент страницы
        goods = []
        pages_count = get_pages_count(url) # получить кол-во страниц раздела
        for page in range(1, pages_count+1):
            html = get_html(url, params={'PAGEN_2': page})
            goods.extend(get_content(html.text)) # добавить в список новые данные
    else: # все не ОК
        print('Error!')

    ##############################################################################################
    # фильтрация от ненужных товаров
    ##############################################################################################

    #print('len before: ', len(goods))
    #input()

    # добавлять только Pulpy
    for good in goods:
        if 'Pulpy' in good.get('title'):
            if 'Pulpy Тропический' in good.get('title'):
                temp = good['title'].split(',')
                good['title'] = 'Pulpy Тропический' + temp[1] + ',' + temp[2]
                #good['title'] = 'Pulpy Тропический'
            elif 'Pulpy Апельсин' in good.get('title'):
                temp = good['title'].split(',')
                good['title'] = 'Pulpy Апельсин' + temp[1] + ',' + temp[2]
                #good['title'] = 'Pulpy Апельсин'
            else:
                good.clear()
        else:
            good.clear()

    goods = list(filter(None, goods)) # удаление пустых словарей

    #print(goods)
    #print('len after: ', len(goods))
    #input()

    # цена >= 80 руб -> удалить
    for good in goods:
        if (good.get('sale') == ''): # если скидки нет
            temp = good.get('price')[:-2] # обрубить "Р." в конце
        else: # есть скидка на товар
            temp = good.get('sale')[:-2] # обрубить "Р." в конце
        if (float(temp) >= 80): #############################################################################
            # удалить элемент
            good.clear()

    goods = list(filter(None, goods)) # удаление пустых словарей

    #print(goods)
    #print('len: ', len(goods))
    #input()

    # остаются только палпи по 0.45 (апельсин и тропический)

    return goods

def parse_gas(url):
    html = get_html(url)
    if (html.status_code == 200): # все ОК
        # получить контент страницы
        goods = []
        pages_count = get_pages_count(url) # получить кол-во страниц раздела
        for page in range(1, pages_count+1):
            html = get_html(url, params={'PAGEN_2': page})
            goods.extend(get_content(html.text)) # добавить в список новые данные
    else: # все не ОК
        print('Error!')

    ##############################################################################################
    # фильтрация от ненужных товаров
    ##############################################################################################
    # оставить классическую колу

    #print('len before: ', len(goods))
    #input()

    # цена >= 70 руб -> удалить
    for good in goods:
        if 'Coca-Cola' in good.get('title') or \
            'Sprite сильногазированный' in good.get('title') or \
            'Fanta Апельсин' in good.get('title'):
            if (good.get('sale') == ''): # если скидки нет
                temp = good.get('price')[:-2] # обрубить "Р." в конце
            else: # есть скидка на товар
                temp = good.get('sale')[:-2] # обрубить "Р." в конце
            if (float(temp) >= 70):
                # удалить элемент
                good.clear()
        else:
            good.clear()

    goods = list(filter(None, goods)) # удаление пустых словарей

    #print(goods)
    #print('len after price: ', len(goods))
    #input()

    # добавлять только классическую колу
    for good in goods:
        # привести (мл) к (л)
        good['title'] = good['title'].replace('500 мл', '0,5 л')
        # менять название
        if 'Coca-Cola сильногазированный' in good.get('title'):
            temp = good['title'].split(',')
            good['title'] = 'Coca-Cola Classic' + temp[1] + ',' + temp[2]
        elif 'Sprite' in good.get('title'):
            temp = good['title'].split(',')
            good['title'] = 'Sprite' + temp[1] + ',' + temp[2]
        elif 'Fanta' in good.get('title'):
            temp = good['title'].split(',')
            good['title'] = 'Fanta Апельсин' + temp[1] + ',' + temp[2]
        else:
            good.clear()

    goods = list(filter(None, goods)) # удаление пустых словарей

    #print(goods)
    #print('len after: ', len(goods))
    #input()

    goods = delete_repeat(goods)
    #print(goods)
    #print(len(goods))

    # в результате остаются 6 наименований: классическая кола, спрайт и фанта по 0.33 и 0.5
    return goods

def parse_tea(url):
    html = get_html(url)
    if (html.status_code == 200): # все ОК
        # получить контент страницы
        goods = []
        pages_count = get_pages_count(url) # получить кол-во страниц раздела
        for page in range(1, pages_count+1):
            html = get_html(url, params={'PAGEN_2': page})
            goods.extend(get_content(html.text)) # добавить в список новые данные
    else: # все не ОК
        print('Error!')

    ##############################################################################################
    # фильтрация от ненужных товаров
    ##############################################################################################
    # выбрать Lipton и Neatea

    #print('len before: ', len(goods))
    #input()

    # цена >= 90 руб -> удалить
    for good in goods:
        if ('Lipton' in good.get('title') or 'FuzeTea' in good.get('title')) and \
            ('0,5' in good.get('title')):
            if (good.get('sale') == ''): # если скидки нет
                temp = good.get('price')[:-2] # обрубить "Р." в конце
            else: # есть скидка на товар
                temp = good.get('sale')[:-2] # обрубить "Р." в конце
            if (float(temp) >= 90):
                # удалить элемент
                good.clear()
        else:
            good.clear()

    goods = list(filter(None, goods)) # удаление пустых словарей

    #print(goods)
    #print('len after price: ', len(goods))
    #input()

    for good in goods:
        # менять название
        if 'FuzeTea Лимон' in good.get('title'):
            temp = good['title'].split(',')
            good['title'] = 'Чай черный FuzeTea Лимон' + temp[1] + ',' + temp[2]
        elif ('Чай Lipton' in good.get('title')) and ('черный' in good.get('title')):
            temp = good['title'].split(',')
            good['title'] = 'Чай черный Lipton Лимон' + temp[1] + ',' + temp[2]
        else:
            good.clear()

    goods = list(filter(None, goods)) # удаление пустых словарей

    #print(goods)
    #print('len after: ', len(goods))
    #input()

    #print('delte rep')

    goods = delete_repeat(goods)

    #print(goods)
    #print(len(goods))

    # на выходе 2 наименования: черный липтон и черный фьюзти

    return goods

def parse_water(url):
    html = get_html(url)
    if (html.status_code == 200): # все ОК
        # получить контент страницы
        goods = []
        pages_count = get_pages_count(url) # получить кол-во страниц раздела
        for page in range(1, pages_count+1):
            html = get_html(url, params={'PAGEN_2': page})
            goods.extend(get_content(html.text)) # добавить в список новые данные
    else: # все не ОК
        print('Error!')

    ##############################################################################################
    # фильтрация от ненужных товаров
    ##############################################################################################

    #print('len before: ', len(goods))
    #input()

    # святой источник == 0.5
    for good in goods:
        if ('Вода питьевая Святой Источник негазированная, 0,5 л' in good.get('title')) or \
            ('Вода питьевая Святой Источник газированная, 0,5 л' in good.get('title')):
            if (good.get('sale') == ''): # если скидки нет
                temp = good.get('price')[:-2] # обрубить "Р." в конце
            else: # есть скидка на товар
                temp = good.get('sale')[:-2] # обрубить "Р." в конце
        else:
            good.clear()

    goods = list(filter(None, goods)) # удаление пустых словарей

    #print(goods)
    #print('len after price: ', len(goods))
    #input()

    for good in goods:
        # менять название
        if 'негазированная' in good.get('title'):
            temp = good['title'].split(',')
            good['title'] = 'Святой Источник негазированная' + temp[1] + ',' + temp[2]
        elif 'газированная' in good.get('title'):
            temp = good['title'].split(',')
            good['title'] = 'Святой Источник газированная' + temp[1] + ',' + temp[2]
        else:
            good.clear()

    goods = list(filter(None, goods)) # удаление пустых словарей

    #print(goods)
    #print('len after: ', len(goods))
    #input()

    #print('delte rep')

    goods = delete_repeat(goods)

    #print(goods)
    #print(len(goods))

    # на выходе 2 наименования: вода 0.5 с газом и без

    return goods

# парсинг раздела "напитки"
def parse_drinks():
    # добавление результатов парсинга в список
    goods = []
    goods.extend(parse_juice(URL_JUICE))
    goods.extend(parse_gas(URL_GAS))
    goods.extend(parse_tea(URL_TEA))
    goods.extend(parse_water(URL_WATER))
    
    return goods


# a = parse_drinks()
# print(a)
# print(len(a))

##############################################################################################
# ЭНЕРГЕТИКИ (МАМА НЕ ОДОБРИТ)
##############################################################################################

URL_ENERGY = 'https://www.victoria-group.ru/catalog/voda_soki_napitki/energeticheskie_napitki/'

def parse_energy(url):
    html = get_html(url)
    if (html.status_code == 200): # все ОК
        # получить контент страницы
        goods = []
        pages_count = get_pages_count(url) # получить кол-во страниц раздела
        for page in range(1, pages_count+1):
            html = get_html(url, params={'PAGEN_2': page})
            goods.extend(get_content(html.text)) # добавить в список новые данные
    else: # все не ОК
        print('Error!')

    ##############################################################################################
    # фильтрация от ненужных товаров
    ##############################################################################################

    #print('len before: ', len(goods))
    #input()

    # взять только Red Bull, Drive Me, Gorilla, Adrenaline Rush, Burn
    for good in goods:
        if ('Red Bull' in good.get('title')) or \
            ('Drive Me Яблоко-Карамбола' in good.get('title')) or \
            ('Gorilla' in good.get('title')) or \
            ('Burn' in good.get('title')) or \
            ('Adrenaline Rush Абсолютная Энергия' in good.get('title')):
            if (good.get('sale') == ''): # если скидки нет
                temp = good.get('price')[:-2] # обрубить "Р." в конце
            else: # есть скидка на товар
                temp = good.get('sale')[:-2] # обрубить "Р." в конце
        else:
            good.clear()

    goods = list(filter(None, goods)) # удаление пустых словарей

    #print(goods)
    #print('len after price: ', len(goods))
    #input()

    for good in goods:
        # менять название
        if 'Red Bull' in good.get('title'):
            temp = good['title'].split(',')
            good['title'] = 'Red Bull' + temp[1] + ',' + temp[2]
        elif 'Drive Me Яблоко-Карамбола' in good.get('title'):
            temp = good['title'].split(',')
            good['title'] = 'Drive Me Яблоко-Карамбола' + temp[1] + ',' + temp[2]
        elif 'Gorilla' in good.get('title'):
            temp = good['title'].split(',')
            good['title'] = 'Gorilla' + temp[1] + ',' + temp[2]
        elif 'Adrenaline Rush Абсолютная Энергия' in good.get('title'):
            temp = good['title'].split(',')
            good['title'] = 'Adrenaline Rush' + temp[1] + ',' + temp[2]
        elif 'Burn' in good.get('title'):
            # привести (мл) к (л)
            good['title'] = good['title'].replace('449 мл', '0,449 л')
            temp = good['title'].split(',')
            if 'Яблоко-киви' in good.get('title'):
                good['title'] = 'Burn Яблоко-киви' + temp[1] + ',' + temp[2]
            elif 'Тропический микс' in good.get('title'):
                good['title'] = 'Burn Тропический микс' + temp[1] + ',' + temp[2]
            elif 'Original' in good.get('title'):
                good['title'] = 'Burn Original' + temp[1] + ',' + temp[2]
        else:
            good.clear()

    goods = list(filter(None, goods)) # удаление пустых словарей

    #print(goods)
    #print('len after: ', len(goods))
    #input()

    #print('delte rep')

    goods = delete_repeat(goods)

    #print(goods)
    #print(len(goods))

    # на выходе 7 наименований: Red Bull, Drive Me, Gorilla, Adrenaline Rush, Burn

    return goods

# a = parse_energy(URL_ENERGY)
# print(a)
# print(len(a))


##############################################################################################
# СНЕКИ
##############################################################################################

URL_CHIPS = 'https://www.victoria-group.ru/catalog/makarony_krupy_muka_maslo/chipsy_sukhariki_sneki_1/'

URL_CHOCOBARS = 'https://www.victoria-group.ru/catalog/khleb_torty_sladosti/shokolad_pasty_1/'

def parse_chips(url):
    html = get_html(url)
    if (html.status_code == 200): # все ОК
        # получить контент страницы
        goods = []
        pages_count = get_pages_count(url) # получить кол-во страниц раздела
        for page in range(1, pages_count+1):
            html = get_html(url, params={'PAGEN_2': page})
            goods.extend(get_content(html.text)) # добавить в список новые данные
    else: # все не ОК
        print('Error!')

    ##############################################################################################
    # фильтрация от ненужных товаров
    ##############################################################################################

    #print('len before: ', len(goods))
    #input()

    # взять только чипсы и сухарики
    for good in goods:
        if ("Lay's" in good.get('title')) or \
            ('Хрусteam' in good.get('title')):
            if (good.get('sale') == ''): # если скидки нет
                temp = good.get('price')[:-2] # обрубить "Р." в конце
            else: # есть скидка на товар
                temp = good.get('sale')[:-2] # обрубить "Р." в конце
            if (float(temp) >= 80):
                # удалить элемент
                good.clear()
        else:
            good.clear()

    goods = list(filter(None, goods)) # удаление пустых словарей

    #print(goods)
    #print('len after price: ', len(goods))
    #input()

    for good in goods:
        # удалить те, что весят >= 70 г
        temp = good['title'].split()
        temp = temp[-2]
        if (int(temp) >= 70):
            good.clear()

    goods = list(filter(None, goods)) # удаление пустых словарей

    #print(goods)
    #print('len after: ', len(goods))
    #input()

    #print('delte rep')

    goods = delete_repeat(goods)

    #print(goods)
    #print(len(goods))

    # на выходе 13 наименований: чипсы лэйс и сухарики хрустим

    return goods

def parse_chocobars(url):
    html = get_html(url)
    if (html.status_code == 200): # все ОК
        # получить контент страницы
        goods = []
        pages_count = get_pages_count(url) # получить кол-во страниц раздела
        for page in range(1, pages_count+1):
            html = get_html(url, params={'PAGEN_2': page})
            goods.extend(get_content(html.text)) # добавить в список новые данные
    else: # все не ОК
        print('Error!')

    ##############################################################################################
    # фильтрация от ненужных товаров
    ##############################################################################################

    #print('len before: ', len(goods))
    #input()

    # взять только сникерс, баунти, твикс, марс, кит-кат
    for good in goods:
        if ('Mars' in good.get('title')) or \
            ('Picnic' in good.get('title')) or \
            ('Kit Kat' in good.get('title')) or \
            ('Bounty' in good.get('title')) or \
            ('Snickers' in good.get('title')) or \
            ('Twix' in good.get('title')):
            if (good.get('sale') == ''): # если скидки нет
                temp = good.get('price')[:-2] # обрубить "Р." в конце
            else: # есть скидка на товар
                temp = good.get('sale')[:-2] # обрубить "Р." в конце
            # удалить те, что дороже 60 руб
            if (float(temp) >= 60):
                # удалить элемент
                good.clear()
        else:
            good.clear()

    goods = list(filter(None, goods)) # удаление пустых словарей

    #print(goods)
    #print('len after price: ', len(goods))
    #input()

    #print('delte rep')

    goods = delete_repeat(goods)

    #print(goods)
    #print(len(goods))

    # на выходе 8 наименований: сникерс, марс, твикс, баунти, кит-кат

    return goods

def parse_snacks():
    goods = []
    goods.extend(parse_chips(URL_CHIPS))
    goods.extend(parse_chocobars(URL_CHOCOBARS))

    return goods

# a = parse_snacks()
# print(a)
# print(len(a))

##############################################################################################
# ХЛЕБОБУЛКИ
##############################################################################################

URL_BREAD = 'https://www.victoria-group.ru/catalog/khleb_torty_sladosti/khleb_bulochki_lepeshki_lavash_1/'

def parse_bread(url):
    html = get_html(url)
    if (html.status_code == 200): # все ОК
        # получить контент страницы
        goods = []
        pages_count = get_pages_count(url) # получить кол-во страниц раздела
        for page in range(1, pages_count+1):
            html = get_html(url, params={'PAGEN_2': page})
            goods.extend(get_content(html.text)) # добавить в список новые данные
    else: # все не ОК
        print('Error!')

    ##############################################################################################
    # фильтрация от ненужных товаров
    ##############################################################################################

    #print('len before: ', len(goods))
    #input()

    # взять только выпечку и булки
    for good in goods:
        if ('Сочник' in good.get('title')) or \
            ('Слойка' in good.get('title')) or \
            ('Коржик' in good.get('title')) or \
            ('Рулет' in good.get('title')) or \
            ('ПЕЧЕНЬЕ' in good.get('title')) or \
            ('Ватрушка' in good.get('title')) or \
            ('Конвертик' in good.get('title')) or \
            ('Слоёночка' in good.get('title')) or \
            ('Кекс' in good.get('title')):
            if (good.get('sale') == ''): # если скидки нет
                temp = good.get('price')[:-2] # обрубить "Р." в конце
            else: # есть скидка на товар
                temp = good.get('sale')[:-2] # обрубить "Р." в конце
            # удалить те, что дороже 60 руб
            if (float(temp) >= 60):
                # удалить элемент
                good.clear()
        else:
            good.clear()

    goods = list(filter(None, goods)) # удаление пустых словарей

    #print(goods)
    #print('len after price: ', len(goods))
    #input()

    #print('delte rep')

    goods = delete_repeat(goods)

    #print(goods)
    #print(len(goods))

    # на выходе  наименований: булки и выпечка прочая

    return goods

# a = parse_bread(URL_BREAD)
# print(a)
# print(len(a))


##############################################################################################
# ТЕСТОВЫЙ ВЫВОД ВСЕХ РЕЗУЛЬТАТОВ
##############################################################################################

# выполни test() посмотри формат вывода
# каждая функция parse_* возвращает готовый результат по разделам

def test():
    goods = []

    goods.extend(parse_drinks())
    goods.extend(parse_snacks())
    goods.extend(parse_energy(URL_ENERGY))
    goods.extend(parse_bread(URL_BREAD))

    return goods

import time
start_time = time.time()

a = test()
print(a)
print('Кол-во наименований: ',len(a))

print('Выполнилось за:')
print("--- %s seconds ---" % (time.time() - start_time))