import telebot

# Класс для хранения всех кнопок в каждом из узлов дерева диалогов
class Keyboard:
    # Храним телебота, чтобы создавать Markup'ы
    def __init__(self, bot):
        self.bot = bot

    # Кнопки главного меню
    def start_menu(self):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Расписание', 'Скидки в Виктории')
        markup.row('Расписание по подпискам', 'Найти аудиторию')
        markup.row('Игры', 'Список полезных аудиторий')
        markup.row('Информация о преподавателях', 'Время пар')
        return markup

    # Кнопки расписания (дата по группе)
    def group_date(self):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('На сегодня', 'На завтра')
        markup.row('Подписаться на группу')
        markup.row('Вернуться назад')
        markup.row('Главное меню')
        return markup

    # Список игр
    def games_list(self):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Крестики-нолики')
        markup.row('Морской бой')
        markup.row('Ещё что-нибудь')
        return markup

    # Стандартные кнопки для узлов диалога, где нужно писать текст
    def standard(self):
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('Вернуться назад')
        markup.row('Главное меню')
        return markup