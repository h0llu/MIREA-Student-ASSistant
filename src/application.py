import datetime
import telebot
from keyboard import Keyboard # Выкладки кнопок для разных узлов диалогов
from config import TOKEN # Токен бота
from config import States # Возможные состояния пользователей в дереве диалогов
from schedule import Schedule # работа с расписанием
import dbworker # Классы для работы с БД

if __name__ == '__main__':
    # БД с состояниями пользователей в дереве диалогов
    users_db = dbworker.Users()
    # БД для хранения последнего запроса пользователя (группа)
    schedule_db = dbworker.Schedule_last_request()
    # БД с подписками пользователей
    subs_db = dbworker.Subs()
    # работа с расписанием
    schedule = Schedule()
    # Кнопки для каждого из узлов диалога
    keyboard = Keyboard()

    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(func=lambda msg: not users_db.is_user(msg.from_user.id))
    @bot.message_handler(func=lambda msg: msg.text == 'Главное меню')
    @bot.message_handler(commands=['start'])
    def start_menu(msg):
        bot.send_message(msg.chat.id, 'Выберите пункт меню:', reply_markup=keyboard.start_menu())
        users_db.set_state(msg.from_user.id,  States.S_START.value)

    # вызвать предыдущий обработчик
    @bot.message_handler(func=lambda msg: msg.text == 'Вернуться назад')
    def come_back(msg):
        state = users_db.get_state(msg.from_user.id) // 10
        
        if state == States.S_START.value:
            start_menu(msg)
        elif state == States.S_TIMETABLE.value:
            timetable(msg)
        elif state == States.S_SUB_TIMETABLE.value:
            sub_timetable(msg)
        elif state == States.S_FOOD.value:
            food(msg)
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

    # ___________
    # РАСПИСАНИЕ
    # ___________

    @bot.message_handler(func=lambda msg: msg.text == 'Расписание')
    def timetable(msg):
        bot.send_message(msg.chat.id, 'Введите группу:', reply_markup=keyboard.standard())
        users_db.set_state(msg.from_user.id, States.S_TIMETABLE.value)

    @bot.message_handler(func=lambda msg: users_db.get_state(msg.from_user.id)
                                    == States.S_TIMETABLE.value)
    def group_date(msg):
        # если такая группа есть в БД,
        # тогда установим текущую группу для последующих запросов
        if schedule.is_valid_group(msg.from_user.id, msg.text):
            bot.send_message(msg.chat.id, 'Введите дату (dd.mm):',
            reply_markup=keyboard.group_date(subs_db.is_subscribed(msg.from_user.id, msg.text)))
            users_db.set_state(msg.from_user.id, States.S_GROUP_DATE.value)
        
        # возвращаем юзера не предыдущий шаг
        else:
            bot.send_message(msg.chat.id, 'Группы не существует!')
            timetable(msg)

    @bot.message_handler(func=lambda msg: users_db.get_state(msg.from_user.id) 
                                    == States.S_GROUP_DATE.value)
    def group_timetable(msg):
        # имя группы, которое ввел юзер на прошлом шаге
        group_name = schedule_db.get_group(msg.from_user.id)
        date = None
        # вывод расписания на сегодня
        if msg.text == 'На сегодня':
            date = datetime.date.today()        
        
        # вывод расписания на завтра
        elif msg.text == 'На завтра':
            date = datetime.date.today() + datetime.timedelta(days=1)

        elif msg.text == 'Подписаться на группу':
            if subs_db.is_subscribed(msg.from_user.id, group_name):
                bot.send_message(msg.chat.id,
                f'Вы уже подписаны на группу {group_name}')
            else:
                subs_db.set_group(msg.from_user.id, group_name)
                bot.send_message(msg.chat.id,
                f'Вы успешно подписались на группу {group_name}',
                reply_markup=keyboard.group_date(True))
            return

        elif msg.text == 'Отписаться от группы':
            if subs_db.is_subscribed(msg.from_user.id, group_name):
                subs_db.del_group(msg.from_user.id, group_name)
                bot.send_message(msg.chat.id, f'Вы успешно отписались от группы {group_name}',
                reply_markup=keyboard.group_date(False))
            else:
                bot.send_message(msg.chat.id, f'Вы не подписаны на группу {group_name}')
            return

        # попробуем найти %d.%m
        # иначе вернем юзера не предыдущий шаг
        else:
            try:
                date = datetime.datetime.strptime(msg.text + '.2021', '%d.%m.%Y')
            except:
                bot.send_message(msg.from_user.id, 'Неверный ввод!')
                msg.text = group_name
                group_date(msg)
                return
        weekday = date.weekday()
        weektype = (date.isocalendar()[1] + 1) % 2
        output = schedule.get_schedule(msg.from_user.id, weekday, weektype)
        bot.send_message(msg.chat.id, output)


    # ______________________
    # РАСПИСАНИЕ ПО ПОДПИСКЕ
    # ______________________

    @bot.message_handler(func=lambda msg: msg.text == 'Расписание по подпискам')
    def sub_timetable(msg):
        if len(subs_db.get_groups(msg.from_user.id)) == 0:
            bot.send_message(msg.chat.id, 'У вас нет подписок!', reply_markup=keyboard.standard())
        else:
            bot.send_message(msg.chat.id, 'Выберите группу из списка подписок:',
            reply_markup=keyboard.subs(subs_db.get_groups(msg.from_user.id)))
        users_db.set_state(msg.from_user.id, States.S_SUB_TIMETABLE.value)

    @bot.message_handler(func=lambda msg: users_db.get_state(msg.from_user.id)
                                    == States.S_SUB_TIMETABLE.value)
    def sub_group_date(msg):
        if subs_db.is_subscribed(msg.from_user.id, msg.text):
            schedule.is_valid_group(msg.from_user.id, msg.text)
            bot.send_message(msg.chat.id, 'Введите дату (dd.mm):', reply_markup=keyboard.group_date(True))
            users_db.set_state(msg.from_user.id, States.S_SUB_GROUP_DATE.value)
            
        else:
            bot.send_message(msg.chat.id, 'Выберите группу из списка подписок!')
            sub_timetable(msg)

    @bot.message_handler(func=lambda msg: users_db.get_state(msg.from_user.id)
                                    == States.S_SUB_GROUP_DATE.value)
    def sub_group_timetable(msg):
        group_name = schedule_db.get_group(msg.from_user.id)
        date = None
        # вывод расписания на сегодня
        if msg.text == 'На сегодня':
            date = datetime.date.today()        
        
        # вывод расписания на завтра
        elif msg.text == 'На завтра':
            date = datetime.date.today() + datetime.timedelta(days=1)

        elif msg.text == 'Подписаться на группу':
            if subs_db.is_subscribed(msg.from_user.id, group_name):
                bot.send_message(msg.chat.id,
                f'Вы уже подписаны на группу {group_name}')
            else:
                subs_db.set_group(msg.from_user.id, group_name)
                bot.send_message(msg.chat.id,
                f'Вы успешно подписались на группу {group_name}',
                reply_markup=keyboard.group_date(True))
            return

        elif msg.text == 'Отписаться от группы':
            if subs_db.is_subscribed(msg.from_user.id, group_name):
                subs_db.del_group(msg.from_user.id, group_name)
                bot.send_message(msg.chat.id, f'Вы успешно отписались от группы {group_name}',
                reply_markup=keyboard.group_date(False))
            else:
                bot.send_message(msg.chat.id, f'Вы не подписаны на группу {group_name}')
            return

        # попробуем найти %d.%m
        # иначе вернем юзера не предыдущий шаг
        else:
            try:
                date = datetime.datetime.strptime(msg.text + '.2021', '%d.%m.%Y')
            except:
                bot.send_message(msg.from_user.id, 'Неверный ввод!')
                msg.text = group_name
                sub_group_date(msg)
                return
        weekday = date.weekday()
        weektype = (date.isocalendar()[1] + 1) % 2
        output = schedule.get_schedule(msg.from_user.id, weekday, weektype)
        bot.send_message(msg.chat.id, output)
    # _________________
    # ЕДА В ВИКТОРИИ
    # _________________

    @bot.message_handler(func=lambda msg: msg.text == 'Еда в Виктории')
    def food(msg):
        # получить еду с сайта, вывести в удобном виде
        bot.send_message(msg.chat.id, 'На стадии разработки', reply_markup=keyboard.standard())
        users_db.set_state(msg.from_user.id, States.S_FOOD.value)

    # _____
    # ИГРЫ
    # _____

    @bot.message_handler(func=lambda msg: msg.text == 'Игры')
    def games(msg):
        # bot.send_message(msg.chat.id, 'Введите название игры:', reply_markup=keyboard.games_list())
        # users_db.set_state(msg.from_user.id, States.S_GAMES.value)

        bot.send_message(msg.chat.id, 'На стадии разработки', reply_markup=keyboard.standard())

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

    @bot.message_handler(func=lambda msg: msg.text == 'Найти аудиторию')
    def find(msg):
        # bot.send_message(msg.chat.id, 'Введите номер аудитории:', reply_markup=keyboard.standard())
        # users_db.set_state(msg.from_user.id, States.S_FIND.value)

        bot.send_message(msg.chat.id, 'На стадии разработки', reply_markup=keyboard.standard())

    @bot.message_handler(func=lambda msg: users_db.get_state(msg.from_user.id)
                                    == States.S_FIND.value)
    def find_place(msg):
        # тут нужно найти аудиторию
        users_db.set_state(msg.from_user.id, States.S_FIND_PLACE.value)

    # __________________________
    # СПИСОК ПОЛЕЗНЫХ АУДИТОРИЙ
    # __________________________

    @bot.message_handler(func=lambda msg: msg.text == 'Список полезных аудиторий')
    def useful(msg):
        # вывести заранее сделанный список полезных аудиторий
        # users_db.set_state(msg.from_user.id, States.S_USEFUL.value)

        bot.send_message(msg.chat.id, 'На стадии разработки', reply_markup=keyboard.standard())

    # ____________________________
    # ИНФОРМАЦИЯ О ПРЕПОДАВАТЕЛЯХ
    # ____________________________

    @bot.message_handler(func=lambda msg: msg.text == 'Информация о преподавателях')
    def professor(msg):
        # bot.send_message(msg.chat.id, '''Введите имя преподавателя в виде
    # Иванов И.И.''', reply_markup=keyboard.standard())
        # users_db.set_state(msg.from_user.id, States.S_PROFESSOR.value)

        bot.send_message(msg.chat.id, 'На стадии разработки', reply_markup=keyboard.standard())

    @bot.message_handler(func=lambda msg: users_db.get_state(msg.from_user.id)
                                    == States.S_PROFESSOR.value)
    def professor_name(msg):
        # вывод информации о преподавателе
        users_db.set_state(msg.from_user.id, States.S_PROFESSOR_NAME.value)

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


        bot.polling()
