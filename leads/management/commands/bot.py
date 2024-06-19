import telebot
from telebot import types
from django.conf import settings

bot = telebot.TeleBot(settings.BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет, {0.first_name}!\nЯ <b>{1.first_name}</b>, твой личный помощник по покупкам. Я здесь, чтобы помочь тебе находить лучшие предложения, сравнивать цены и делать покупки проще и выгоднее.\nЧем могу помочь сегодня?".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

bot.remove_webhook()
bot.set_webhook(url=settings.BOT_PROXY_URL)

def start_bot():
    bot.polling()