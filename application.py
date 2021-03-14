from Schedule.display_schedule import display_schedule
from time import strptime
from keyboard import Keyboard # Выкладки кнопок для разных узлов диалогов
from config import TOKEN # Токен бота
from config import States # Возможные состояния пользователей в дереве диалогов
from Schedule.display_schedule import display_schedule
import dbworker # Классы для работы с БД
import datetime
import telebot

# Таблица с состояниями пользователей в дереве диалогов
users_db = dbworker.Users()
# БД с расписаниями для каждой группы
schedule_db = dbworker.Schedule()

# Кнопки для каждого из узлов диалога
keyboard = Keyboard()
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda msg: msg.text == 'Главное меню')
@bot.message_handler(commands=['start'])
def start_menu(msg):
    bot.send_message(msg.chat.id, 'Выберите пункт меню:', reply_markup=keyboard.start_menu())
    users_db.set_state(msg.from_user.id,  States.S_START.value)

# вызвать предыдущий обработчик
@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    msg.text == 'Вернуться назад')
def come_back(msg):
    state = users_db.get_state(msg.from_user.id) // 10
    
    if state == States.S_START.value:
        start_menu(msg)
    elif state == States.S_TIMETABLE.value:
        timetable(msg)
    elif state == States.S_GROUP_DATE.value:
        timetable(msg)
    elif state == States.S_SUB_TIMETABLE.value:
        sub_timetable(msg)
    elif state == States.S_SUB_GROUP_DATE.value:
        sub_group_date(msg)
    elif state == States.S_SUB_GROUP_TIMETABLE.value:
        sub_group_timetable(msg)
    elif state == States.S_DISCOUNT.value:
        discount(msg)
    elif state == States.S_GAMES.value:
        games(msg)
    elif state == States.S_RUN_GAMES.value:
        run_games(msg)
    elif state == States.S_FIND.value:
        find(msg)
    elif state == States.S_FIND_PLACE.value:
        find_place(msg)
    elif state == States.S_USEFUL.value:
        useful(msg)
    elif state == States.S_PROFESSOR.value:
        professor(msg)
    elif state == States.S_PROFESSOR_NAME.value:
        professor_name(msg)
    elif state == States.S_CLASSES_TIME.value:
        classes_time(msg)

# ___________
# РАСПИСАНИЕ
# ___________

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    msg.text == 'Расписание')
def timetable(msg):
    bot.send_message(msg.chat.id, 'Введите группу:', reply_markup=keyboard.standard())
    users_db.set_state(msg.from_user.id, States.S_TIMETABLE.value)

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    users_db.get_state(msg.from_user.id) == States.S_TIMETABLE.value)
def group_date(msg):
    # если такая группа есть в БД,
    # тогда установим текущую группу для последующих запросов
    if schedule_db.is_valid_group(msg.text):
        schedule_db.curr_group_name = msg.text
        bot.send_message(msg.chat.id, 'Введите дату (dd.mm):', reply_markup=keyboard.group_date())
        users_db.set_state(msg.from_user.id, States.S_GROUP_DATE.value)
    
    # возвращаем юзера не предыдущий шаг
    else:
        bot.send_message(msg.chat.id, 'Группы не существует!')
        timetable(msg)

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    users_db.get_state(msg.from_user.id) == States.S_GROUP_DATE.value)
def group_timetable(msg):
    date = None
    # вывод расписания на сегодня
    if msg.text == 'На сегодня':
        date = datetime.date.today()        
    
    # вывод расписания на завтра
    elif msg.text == 'На завтра':
        date = datetime.date.today() + datetime.timedelta(days=1)

    elif msg.text == 'Подписаться на группу':
        # добавить в таблицу информацию о подписке на группу
        group_timetable(msg)
        return

    # попробуем найти %d.%m
    # иначе вернем юзера не предыдущий шаг
    else:
        try:
            date = datetime.datetime.strptime(msg.text + '.2021', '%d.%m.%Y')
        except:
            bot.send_message(msg.chat.id, 'Неверный ввод!')
            group_date(schedule_db.curr_group_name)
    weekday = date.weekday()
    weektype = date.isocalendar()[1] % 2 + 1
    print(schedule_db.curr_group_name, weekday, weektype)
    schedule_db.get_lesson(schedule_db.curr_group_name, weekday, weektype)
    # lessons = display_schedule(schedule_db.get_lesson(schedule_db.curr_group_name, weekday, weektype))
    # bot.send_message(msg.chat.id, lessons, reply_markup=None)
    users_db.set_state(msg.from_user.id, States.S_GROUP_TIMETABLE.value)


# ______________________
# РАСПИСАНИЕ ПО ПОДПИСКЕ
# ______________________

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    msg.text == 'Расписание по подписке')
def sub_timetable(msg):
    # запрос к таблице с подписками
    # по полученным группам отправить запросы, распарсить .xlsx
    # иначе вывести "подписок нет" и не изменять состояние
    users_db.set_state(msg.from_user.id, States.S_SUB_TIMETABLE.value)

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    users_db.get_state(msg.from_user.id) == States.S_SUB_TIMETABLE.value)
def sub_group_date(msg):
    bot.send_message(msg.chat.id, 'Введите дату:', reply_markup=keyboard.group_date())
    users_db.set_state(msg.from_user.id, States.S_SUB_GROUP_TIMETABLE.value)

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    users_db.get_state(msg.from_user.id) == States.S_SUB_GROUP_DATE.value)
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
    users_db.set_state(msg.from_user.id, States.S_SUB_GROUP_TIMETABLE.value)

# _________________
# СКИДКИ В ВИКТОРИИ
# _________________

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    msg.text == 'Скидки в Виктории')
def discount(msg):
    # получить скидки с сайта, вывести в удобном виде только нужные
    # может, не только скидки, но и дешевая готовая еда (например, булки)
    bot.send_message(msg.chat.id, 'Их пока нет', reply_markup=keyboard.standard())
    users_db.set_state(msg.from_user.id, States.S_DISCOUNT.value)

# _____
# ИГРЫ
# _____

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    msg.text == 'Игры')
def games(msg):
    bot.send_message(msg.chat.id, 'Введите название игры:', reply_markup=keyboard.games_list())
    users_db.set_state(msg.from_user.id, States.S_GAMES.value)

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    users_db.get_state(msg.from_user.id) == States.S_GAMES.value)
def run_games(msg):
    if msg.text == 'Крестики-нолики':
        pass
    elif msg.text == 'Морской бой':
        pass
    else:
        pass
    users_db.set_state(msg.from_user.id, States.S_RUN_GAMES.value)

# ________________
# НАЙТИ АУДИТОРИЮ
# ________________

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    msg.text == 'Найти аудиторию')
def find(msg):
    bot.send_message(msg.chat.id, 'Введите номер аудитории:', reply_markup=keyboard.standard())
    users_db.set_state(msg.from_user.id, States.S_FIND.value)

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    users_db.get_state(msg.from_user.id) == States.S_FIND.value)
def find_place(msg):
    # тут нужно найти аудиторию
    # может, нарисовать карту
    users_db.set_state(msg.from_user.id, States.S_FIND_PLACE.value)

# __________________________
# СПИСОК ПОЛЕЗНЫХ АУДИТОРИЙ
# __________________________

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    msg.text == 'Список полезных аудиторий')
def useful(msg):
    # вывести заранее сделанный список полезных аудиторий
    users_db.set_state(msg.from_user.id, States.S_USEFUL.value)

# ____________________________
# ИНФОРМАЦИЯ О ПРЕПОДАВАТЕЛЯХ
# ____________________________

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    msg.text == 'Информация о преподавателях')
def professor(msg):
    bot.send_message(msg.chat.id, '''Введите имя преподавателя в виде
Иванов И.И.''', reply_markup=keyboard.standard())
    users_db.set_state(msg.from_user.id, States.S_PROFESSOR.value)

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    users_db.get_state(msg.from_user.id) == States.S_PROFESSOR.value)
def professor_name(msg):
    # вывод информации о преподавателе
    # скорее всего, имеет смысл хранить такую информацию в таблице
    # возможно, стоит добавить возможность добавления информации о преподавателях
    users_db.set_state(msg.from_user.id, States.S_PROFESSOR_NAME.value)

# __________
# ВРЕМЯ ПАР
# __________

@bot.message_handler(func=lambda msg: users_db.is_user(msg.from_user.id) and
                    msg.text == 'Время пар')
def classes_time(msg):
    time = '''1 пара   09:00 - 10:30
2 пара   10:40 - 12:10
3 пара   12:40 - 14:10
4 пара   14:20 - 15:50
5 пара   16:20 - 17:50
6 пара   18:00 - 19:30'''
    bot.send_message(msg.chat.id, time)
    users_db.set_state(msg.from_user.id, States.S_CLASSES_TIME.value)


bot.polling()
