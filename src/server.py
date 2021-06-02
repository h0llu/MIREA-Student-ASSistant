import telebot

from outdated.config import TOKEN


bot = telebot.TeleBot(TOKEN)

# Тут handlers

bot.polling()