"""Непосредственно запускаемый сервер бота"""
from os import stat
from typing import Dict
from flask import Flask, request
import json
import telebot
import os

from config import TOKEN
import food
import schedule
import states
import search
import subs
import keyboard
import professors


def d(obj: str) -> Dict:
    return json.loads(obj.replace("'", '"'))


bot = telebot.TeleBot(TOKEN)
professors.init()
food.init()
states.init()
subs.init()



# __________________
# Информация о боте
# __________________
@bot.message_handler(commands=['help'])
def info(msg):
    text = '''Привет!
Я *бот-помощник студента МИРЭА*!
С моей помощью ты можешь:
• Посмотреть расписание на день
• Построить текстовый маршрут до нужной аудитории
• Посмотреть подборку самого необходимого из Виктории
• Просмотреть список полезных аудиторий
• Увидеть, что думают студенты о преподавателях
• Оставить свой комментарий о преподе!

Введи */start*, чтобы начать работу с ботом'''
    bot.send_message(msg.chat.id, text, parse_mode='Markdown')


# ____________________
# Стартовое сообщение
# ____________________
@bot.message_handler(commands=['start'])
def start(msg):
    states.set_state(msg.from_user.id, 'None')

    text = 'Кнопки ниже помогут тебе найти твой путь ниндзя!\n\n'
    text += '*Расписание* - посмотри расписание на конкретный день\n\n'
    text += '*Подписки* - подпишись на свою группу, чтобы не вводить название\n\n'
    text += '*Поиск аудитории* - я построю маршрут до нужной тебе аудитории \
и расскажу, как туда дойти\n\n'
    text += '*Преподаватели* - посмотри отзывы о преподах и напиши свой\n\n'
    text += '*Полезные аудитории* - найди нужную тебе аудиторию\n\n'
    text += '*Время пар* - посмотри, когда тебе на пару'
    bot.send_message(msg.chat.id, text, reply_markup=keyboard.start(), parse_mode='Markdown')


# ________________
# Вернуться назад
# ________________
@bot.callback_query_handler(func=lambda call: d(call.data).get('h') == 'previous')
def previous(call):
    bot.delete_message(call.from_user.id, call.message.message_id)
    eval(d(call.data)['p'] + '(call.message)')


# __________________
# Закрыть сообщение
# __________________
@bot.callback_query_handler(func=lambda call: d(call.data).get('h') == 'close')
def close(call):
    bot.delete_message(call.from_user.id, call.message.message_id)


# ___________
# Расписание
# ___________
@bot.callback_query_handler(func=lambda call: d(call.data).get('h') == 'schedule1')
def schedule1(call):
    states.set_state(call.from_user.id, 'Group')
    text = 'Введи название группы\n'
    text += 'Например, ИНБО-05-19, инбо0519'
    bot.edit_message_text(text, call.from_user.id, call.message.message_id,
        reply_markup=keyboard.schedule1())

@bot.message_handler(func=lambda msg: states.get_state(msg.from_user.id) == 'Group')
def schedule2(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    bot.delete_message(msg.chat.id, msg.message_id - 1)

    formatted = schedule.format_groupname(msg.text)
    if not schedule.is_valid_group(formatted):
        bot.send_message(msg.chat.id, f'Группа {msg.text} не существует!\n\
Введи название группы в виде ИНБО-05-19', reply_markup=keyboard.schedule1())
        return

    text = f'Расписание для группы {formatted}\nВыбери день недели'
    subscribed = subs.is_subscribed(msg.from_user.id, formatted)
    bot.send_message(msg.chat.id, text, reply_markup=keyboard.schedule2(formatted, subscribed))

@bot.callback_query_handler(func=lambda call: d(call.data).get('h') == 's3')
def schedule3(call):
    info = d(call.data)
    weekday = schedule.get_schedule(info['g'], info['d'], info['w'])
    bot.edit_message_text(weekday, call.from_user.id, call.message.message_id)


# _________
# Подписки
# _________
@bot.callback_query_handler(func=lambda call: d(call.data).get('h') == 'sub_in_sch')
def sub_in_schedule(call):
    subs.set_group(call.from_user.id, d(call.data).get('g'))
    call.message.text = call.message.text.lstrip('Ты успешно отписался от группы!\n\n')
    text = 'Ты успешно подписался на группу!\n\n' + call.message.text
    bot.edit_message_text(text, call.from_user.id, call.message.message_id,
        reply_markup=keyboard.schedule2(d(call.data).get('g'), True))

@bot.callback_query_handler(func=lambda call: d(call.data).get('h') == 'unsub_in_sch')
def unsub_in_schedule(call):
    subs.del_group(call.from_user.id, d(call.data).get('g'))
    call.message.text = call.message.text.lstrip('Ты успешно подписался на группу!\n\n')
    text = 'Ты успешно отписался от группы!\n\n' + call.message.text
    bot.edit_message_text(text, call.from_user.id, call.message.message_id,
        reply_markup=keyboard.schedule2(d(call.data).get('g'), False))

@bot.callback_query_handler(func=lambda call: d(call.data).get('h') == 'sub1')
def sub1(call):
    if len(subs.get_groups(call.from_user.id)) == 0:
        bot.edit_message_text('У тебя нет подписок', call.from_user.id, call.message.message_id,
            reply_markup=keyboard.sub1_basic())
        return

    bot.edit_message_text('Выбери группу из списка подписок', call.from_user.id,
        call.message.message_id,reply_markup=keyboard.sub1(subs.get_groups(call.from_user.id)))

@bot.callback_query_handler(func=lambda call: d(call.data).get('h') == 'sub2')
def sub2(call):
    group = d(call.data).get('g')
    text = f'Расписание для группы {group}\nВыбери день недели'
    subscribed = subs.is_subscribed(call.from_user.id, group)
    bot.edit_message_text(text, call.from_user.id, call.message.message_id,
        reply_markup=keyboard.schedule2(group, subscribed))


# _________
# Виктория
# _________
@bot.callback_query_handler(func=lambda call: d(call.data).get('h') == 'vic1')
def vic1(call):
    bot.edit_message_text('Выбери категорию', call.from_user.id, call.message.message_id,
        reply_markup=keyboard.vic1())

@bot.callback_query_handler(func=lambda call: d(call.data).get('h') == 'vic2')
def vic2(call):
    f = food.get_food(d(call.data).get('c'))
    text = ''
    for havka in f:
        text += f'*Название*: {havka[0]}\n'
        if havka[2] == '':
            text += f'*Цена*: {havka[1]}\n\n'
        else:
            text += f'*Цена*: {havka[2]}\n\n'
    bot.edit_message_text(text, call.from_user.id, call.message.message_id, parse_mode='Markdown')


# ______________
# Преподаватели
# ______________
@bot.callback_query_handler(func=lambda call: d(call.data).get('h') == 'prof1')
def prof1(call):
    bot.edit_message_text('Почитать комментарии или добавить свой?',
        call.from_user.id, call.message.message_id, reply_markup=keyboard.prof1())

@bot.callback_query_handler(func=lambda call: d(call.data).get('h') == 'prof2')
def prof2(call):
    if d(call.data).get('ch') == 'read':
        bot.edit_message_text('Выбери преподавателя из списка', call.from_user.id,
            call.message.message_id, reply_markup=keyboard.prof_list(professors.get_professors()))
        return
    else:
        states.set_state(call.from_user.id, 'Name')
        bot.edit_message_text('Введи имя преподавателя', call.from_user.id,
            call.message.message_id, reply_markup=keyboard.basic())

@bot.callback_query_handler(func=lambda call: d(call.data).get('h') == 'prof_desc')
def prof_desc(call):
    decriptions = professors.get_descriptions(d(call.data).get('prof'))
    res = f'*{d(call.data).get("prof")}*\n\n'
    for desc in decriptions:
        res += f'"{desc}"\n\n'
    bot.edit_message_text(res, call.from_user.id, call.message.message_id, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: states.get_state(msg.from_user.id) == 'Name')
def prof_name(msg):
    states.set_state(msg.from_user.id, 'Description')
    professors.add_name(msg.text)
    bot.delete_message(msg.chat.id, msg.message_id)
    bot.delete_message(msg.chat.id, msg.message_id - 1)
    bot.send_message(msg.chat.id, 'Введи описание преподавателя', reply_markup=keyboard.basic())

@bot.message_handler(func=lambda msg: states.get_state(msg.from_user.id) == 'Description')
def write_desc(msg):
    states.set_state(msg.from_user.id, 'None')
    professors.add_description(msg.text)
    bot.delete_message(msg.chat.id, msg.message_id)
    bot.delete_message(msg.chat.id, msg.message_id - 1)
    bot.send_message(msg.chat.id, 'Описание успешно добавлено')


# ________________
# Поиск аудитории
# ________________


# __________________________
# Список полезных аудиторий
# __________________________
@bot.callback_query_handler(func=lambda call: d(call.data).get('h') == 'useful_list')
def audience_list(call):
    text = '''А-126 - мед. кабинет
А-168 - Управление по воспитательной и социальной работе
А-415 - Казанцева Л.В.
А-416 - Зуев А.С.
А-417 - Учебный отдел ИТ
Г-426 - Дзержинский Р.И.'''
    bot.edit_message_text(text, call.from_user.id, call.message.message_id)



def main():
    if 'HEROKU' in list(os.environ.keys()):
        server = Flask(__name__)

        @server.route('/bot', methods=['POST'])
        def getMessage():
            bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
            return '!', 200

        @server.route('/')
        def webhook():
            bot.remove_webhook()
            bot.set_webhook(url='https://mirea-assistant-bot.herokuapp.com/bot')
            return '?', 200
        server.run(host='0.0.0.0', port=os.environ.get('PORT', 80))
    else:
        bot.remove_webhook()
        bot.polling()

if __name__ == '__main__':
    main()
