import  telebot
import Users # здесь происходят все операции с данными о пользователях

bot = telebot.TeleBot('ТОКЕН')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, этот бот пока ничего не может, но скоро научиться!')

@bot.message_handler(content_types=['text'])
def answer_to_text(message):
    user = Users.check(message.from_user.id)


bot.polling()