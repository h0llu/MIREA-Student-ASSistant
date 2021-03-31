import telebot

# Класс для хранения всех кнопок в каждом из узлов дерева диалогов
class Keyboard:
    """Keyboard class

    :param pr: param pararam
    """    

    # Кнопки главного меню
    def start_menu(self):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Расписание', 'Еда в Виктории')
        markup.row('Расписание по подпискам', 'Найти аудиторию')
        markup.row('Игры', 'Список полезных аудиторий')
        markup.row('Информация о преподавателях', 'Время пар')
        return markup

    # Кнопки расписания (дата по группе)
    def group_date(self, is_subscribed):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('На сегодня', 'На завтра')
        if not is_subscribed:
            markup.row('Подписаться на группу')
        else:
            markup.row('Отписаться от группы')
        markup.row('Вернуться назад')
        markup.row('Главное меню')
        return markup

    # подписки
    def subs(self, groups):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        for group in groups:
            markup.row(group[0])
        markup.row('Вернуться назад')
        markup.row('Главное меню')
        return markup

    # Список игр
    def games_list(self):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Крестики-нолики')
        markup.row('Морской бой')
        markup.row('Ещё что-нибудь')
        markup.row('Вернуться назад')
        markup.row('Главное меню')
        return markup

    # Стандартные кнопки для узлов диалога, где нужно писать текст
    def standard(self):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Вернуться назад')
        markup.row('Главное меню')
        return markup