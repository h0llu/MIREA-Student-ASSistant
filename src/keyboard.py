"""Callback-кнопки и их информация (JSON)"""
from typing import List
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def start():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton('📅Расписание', callback_data=str({
            'h': 'schedule1',
            'p': 'None'
        })),
               InlineKeyboardButton('✅Подписки', callback_data=str({
            'h': 'sub1',
            'p': 'None'
        })),
               InlineKeyboardButton('🏪Виктория', callback_data=str({
                   'h': 'vic1',
                   'p': 'None'
               })),
               InlineKeyboardButton('🔍Поиск аудитории', callback_data=str({
            'h': 'search',
            'p': 'None'
        })),
               InlineKeyboardButton('👤Преподаватели', callback_data=str({
            'h': 'prof1',
            'p': 'None'
        })),
               InlineKeyboardButton('🚪Полезные аудитории', callback_data=str({
            'h': 'useful_list',
            'p': 'None'
        })))
    markup.add(InlineKeyboardButton('❌Закрыть', callback_data=str({
            'h': 'close',
            'p': 'None'
        })), row_width=1)
    return markup

def schedule1():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('↩Назад', callback_data=str({
            'h': 'previous',
            'p': 'start'
        })),
               InlineKeyboardButton('❌Закрыть', callback_data=str({
                   'h': 'close',
                   'p': 'start'
        })))
    return markup

def schedule2(g: str, unsub: bool = False):
    markup = InlineKeyboardMarkup(row_width=7)
    markup.add(InlineKeyboardButton('1️⃣', callback_data=str({'h': 'None'})),
               InlineKeyboardButton('Пн', callback_data=str({
            'h': 's3',
            'g': g,
            'w': 1,
            'd': 0})),
               InlineKeyboardButton('Вт', callback_data=str({
            'h': 's3',
            'g': g,
            'w': 1,
            'd': 1})),
               InlineKeyboardButton('Ср', callback_data=str({
            'h': 's3',
            'g': g,
            'w': 1,
            'd': 2})),
               InlineKeyboardButton('Чт', callback_data=str({
            'h': 's3',
            'g': g,
            'w': 1,
            'd': 3})),
               InlineKeyboardButton('Пт', callback_data=str({
            'h': 's3',
            'p': 'None',
            'w': 1,
            'd': 4})),
               InlineKeyboardButton('Сб', callback_data=str({
            'h': 's3',
            'g': g,
            'w': 1,
            'd': 5})))
    markup.add(InlineKeyboardButton('2️⃣', callback_data=str({'h': 'None'})),
               InlineKeyboardButton('Пн', callback_data=str({
            'h': 's3',
            'g': g,
            'w': 0,
            'd': 0 })),
               InlineKeyboardButton('Вт', callback_data=str({
            'h': 's3',
            'g': g,
            'w': 0,
            'd': 1})),
               InlineKeyboardButton('Ср', callback_data=str({
            'h': 's3',
            'g': g,
            'w': 0,
            'd': 2})),
               InlineKeyboardButton('Чт', callback_data=str({
            'h': 's3',
            'g': g,
            'w': 0,
            'd': 3})),
               InlineKeyboardButton('Пт', callback_data=str({
            'h': 's3',
            'g': g,
            'w': 0,
            'd': 4})),
               InlineKeyboardButton('Сб', callback_data=str({
            'h': 's3',
            'g': g,
            'w': 0,
            'd': 5})))
    if not unsub:
        markup.add(InlineKeyboardButton('Подписаться на группу', callback_data=str({
            'h': 'sub_in_sch',
            'p': 'None',
            'g': g
        })), row_width=1)
    else:
        markup.add(InlineKeyboardButton('Отписаться от группы', callback_data=str({
            'h': 'unsub_in_sch',
            'p': 'None',
            'g': g
        })), row_width=1)
    markup.add(InlineKeyboardButton('Главное меню', callback_data=str({
            'h': 'previous',
            'p': 'start'
        })),
               InlineKeyboardButton('❌Закрыть', callback_data=str({
            'h': 'close',
            'p': 'None'
        })), row_width=1)
    return markup

def sub1(groups: List):
    markup = InlineKeyboardMarkup(row_width=1)
    for group in groups:
        markup.add(InlineKeyboardButton(group, callback_data=str({
            'h': 'sub2',
            'p': 'start',
            'g': group
        })))
    
    markup.add(InlineKeyboardButton('↩Назад', callback_data=str({
            'h': 'previous',
            'p': 'start'
        })),
               InlineKeyboardButton('❌Закрыть', callback_data=str({
                   'h': 'close',
                   'p': 'None'
        })))
    return markup

def sub1_basic():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('↩Назад', callback_data=str({
            'h': 'previous',
            'p': 'start'
        })),
               InlineKeyboardButton('❌Закрыть', callback_data=str({
                   'h': 'close',
                   'p': 'start'
        })))
    return markup

def vic1():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('🍼Энергетики', callback_data=str({
        'h': 'vic2',
        'p': 'None',
        'c': 'energy'
    })),
               InlineKeyboardButton('🍞Булочки', callback_data=str({
        'h': 'vic2',
        'p': 'None',
        'c': 'bread'
    })),
               InlineKeyboardButton('🍫Снеки', callback_data=str({
        'h': 'vic2',
        'p': 'None',
        'c': 'snack'
    })),
               InlineKeyboardButton('🥤Чай, газировка, сок, вода', callback_data=str({
        'h': 'vic2',
        'p': 'None',
        'c': 'drink'
    })),
               InlineKeyboardButton('↩Назад', callback_data=str({
        'h': 'previous',
        'p': 'start'
    })),
               InlineKeyboardButton('❌Закрыть', callback_data=str({
        'h': 'close',
        'p': 'start'
    })))
    return markup

def prof1():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton('📖Почитать', callback_data=str({
        'h': 'prof2',
        'p': 'None',
        'ch': 'read'
    })),
               InlineKeyboardButton('🖊Написать', callback_data=str({
        'h': 'prof2',
        'p': 'None',
        'ch': 'write'
    })))
    markup.add(InlineKeyboardButton('↩Назад', callback_data=str({
        'h': 'previous',
        'p': 'start'
    })),
               InlineKeyboardButton('❌Закрыть', callback_data=str({
        'h': 'close',
        'p': 'start'
    })), row_width=1)
    return markup

def prof_list(professors: List[str]):
    markup = InlineKeyboardMarkup(row_width=1)
    for prof in professors:
        markup.add(InlineKeyboardButton(prof, callback_data=str({
            'h': 'prof_desc',
            'prof': prof
        })))
    markup.add(InlineKeyboardButton('❌Закрыть', callback_data=str({
            'h': 'close',
            'p': 'start'
        })))
    return markup

def basic():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton('Главное меню', callback_data=str({
            'h': 'previous',
            'p': 'start'
        })),
               InlineKeyboardButton('❌Закрыть', callback_data=str({
                   'h': 'close',
                   'p': 'start'
        })))
