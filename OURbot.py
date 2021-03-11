import telebot
import Users # здесь происходят все операции с данными о пользователях

bot = telebot.TeleBot('1625713494:AAEafifP5xHlVFC2wb7jcaWpHJHL4H2csWQ')

@bot.message_handler(commands=['start'])
def start_message(message):
    Users.create(message.chat.id)
    bot.send_message(message.chat.id, 'Привет, этот бот пока ничего не может, но скоро научиться!')

@bot.message_handler(content_types=['text'])
def answer_to_text(message):
    user_locate = Users.check(message.from_user.id)
    bot.send_message(message.chat.id, str(user_locate))

bot.polling()
