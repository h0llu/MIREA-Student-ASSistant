from keyboard import Keyboard
from config import TOKEN
from config import States
import Users # Состояние пользователя в дереве диалогов
import telebot

# Создание бота и таблицы состояний 
Users.create_table()
bot = telebot.TeleBot(TOKEN)
keyboard = Keyboard(bot)

@bot.message_handler(func=lambda msg: msg.text == 'Главное меню')
@bot.message_handler(commands=['start'])
def start_menu(msg):
    bot.send_message(msg.chat.id, 'Выберите пункт меню:', reply_markup=keyboard.start_menu())
    Users.set_state(msg.from_user.id,  States.S_START.value)

@bot.message_handler(func=lambda msg: msg.text == 'Вернуться назад')
def come_back(msg):
    # тут нужно вытащить предыдущее состояние
    pass

# ___________
# РАСПИСАНИЕ
# ___________

@bot.message_handler(func=lambda msg: msg.text == 'Расписание')
def timetable(msg):
    bot.send_message(msg.chat.id, 'Введите группу:', reply_markup=keyboard.standard())
    Users.set_state(msg.from_user.id, States.S_TIMETABLE.value)

@bot.message_handler(func=lambda msg: Users.get_state(msg.from_user.id) == States.S_TIMETABLE.value)
def group_date(msg):
    # проверка на существование введённой группы

    # тут должен отправляться запрос на сайт
    # и парситься .xlsx
    bot.send_message(msg.chat.id, 'Введите дату:', reply_markup=keyboard.group_date())
    Users.set_state(msg.from_user.id, States.S_GROUP_TIMETABLE.value)

@bot.message_handler(func=lambda msg: Users.get_state(msg.from_user.id) == States.S_GROUP_TIMETABLE.value)
def group_timetable(msg):
    if msg.text == 'На сегодня':
        # вывод расписания на сегодня
        Users.set_state(msg.from_user.id, States.S_GROUP_TIMETABLE.value)
    elif msg.text == 'На завтра':
        # вывод расписания на завтра
        Users.set_state(msg.from_user.id, States.S_GROUP_TIMETABLE.value)
    elif msg.text == 'Подписаться на группу':
        # добавить в таблицу информацию о подписке на группу
        pass
    else:
        # вывод расписания на нужную дату
        # тут парсинг даты, из даты получить день недели (четной/нечетной)
        Users.set_state(msg.from_user.id, States.S_GROUP_TIMETABLE.value)

# ______________________
# РАСПИСАНИЕ ПО ПОДПИСКЕ
# ______________________

@bot.message_handler(func=lambda msg: msg.text == 'Расписание по подписке')
def sub_timetable(msg):
    # запрос к таблице с подписками
    # по полученным группам отправить запросы, распарсить .xlsx
    # иначе вывести "подписок нет" и не изменять состояние
    Users.set_state(msg.from_user.id, States.S_SUB_TIMETABLE.value)

@bot.message_handler(func=lambda msg: Users.get_state(msg.from_user.id) == States.S_SUB_TIMETABLE.value)
def sub_group_date(msg):
    bot.send_message(msg.chat.id, 'Введите дату:', reply_markup=keyboard.group_date())
    Users.set_state(msg.from_user.id, States.S_SUB_GROUP_TIMETABLE.value)

@bot.message_handler(func=lambda msg: Users.get_state(msg.from_user.id) == States.S_SUB_GROUP_DATE.value)
def sub_group_timetable(msg):
    if msg.text == 'На сегодня':
        # вывод расписания на сегодня
        pass
    elif msg.text == 'На завтра':
        # вывод расписания на завтра
        pass
    else:
        # вывод расписания на нужную дату
        # тут парсинг даты, из даты получить день недели (четной/нечетной)
        pass
    Users.set_state(msg.from_user.id, States.S_SUB_GROUP_TIMETABLE.value)

# _________________
# СКИДКИ В ВИКТОРИИ
# _________________

@bot.message_handler(func=lambda msg: msg.text == 'Скидки в Виктории')
def discount(msg):
    # получить скидки с сайта, вывести в удобном виде только нужные
    # может, не только скидки, но и дешевая готовая еда (например, булки)
    bot.send_message(msg.chat.id, 'Их пока нет', reply_markup=keyboard.standard())
    Users.set_state(msg.from_user.id, States.S_DISCOUNT.value)

# _____
# ИГРЫ
# _____

@bot.message_handler(func=lambda msg: msg.text == 'Игры')
def games(msg):
    bot.send_message(msg.chat.id, 'Введите название игры:', reply_markup=keyboard.games_list())
    Users.set_state(msg.from_user.id, States.S_GAMES.value)

# ________________
# НАЙТИ АУДИТОРИЮ
# ________________

@bot.message_handler(func=lambda msg: msg.text == 'Найти аудиторию')
def find(msg):
    bot.send_message(msg.chat.id, 'Введите номер аудитории:', reply_markup=keyboard.standard())
    Users.set_state(msg.from_user.id, States.S_FIND.value)

# __________________________
# СПИСОК ПОЛЕЗНЫХ АУДИТОРИЙ
# __________________________

@bot.message_handler(func=lambda msg: msg.text == 'Список полезных аудиторий')
def useful(msg):
    Users.set_state(msg.from_user.id, States.S_USEFUL.value)

# ____________________________
# ИНФОРМАЦИЯ О ПРЕПОДАВАТЕЛЯХ
# ____________________________

@bot.message_handler(func=lambda msg: msg.text == 'Информация о преподавателях')
def professor(msg):
    Users.set_state(msg.from_user.id, States.S_PROFESSOR.value)

# __________
# ВРЕМЯ ПАР
# __________

@bot.message_handler(func=lambda msg: msg.text == 'Время пар')
def classes_time(msg):
    time = '''1 пара   09:00 - 10:30
2 пара   10:40 - 12:10
3 пара   12:40 - 14:10
4 пара   14:20 - 15:50
5 пара   16:20 - 17:50
6 пара   18:00 - 19:30'''
    bot.send_message(msg.chat.id, time)
    Users.set_state(msg.from_user.id, States.S_TIME.value)


bot.polling()
