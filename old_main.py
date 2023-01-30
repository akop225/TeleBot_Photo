import random

import telebot
import urllib.request
from selenium import webdriver
import time
import sqlite3


bot = telebot.TeleBot('5468702833:AAGS0zvI_rXxlYh9yOnnGDBAxYbquoDA7Q0')
number_of_photo = [1]
# driver = webdriver.Chrome()


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    photo = telebot.types.KeyboardButton('Наложить водяной знак')
    end = telebot.types.KeyboardButton('Отмена')

    markup.add(photo, end)
    msg = bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!', reply_markup=markup)
    bot.register_next_step_handler(msg, search)


@bot.message_handler(content_types='text')
def search(message):
    mesg = message.text.lower()
    if ("знак") in mesg:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        end = telebot.types.KeyboardButton('Отмена')
        markup.add(end)
        msg = bot.send_message(message.chat.id, "Отправьте фотографию", reply_markup=markup)
        bot.register_next_step_handler(msg, remake_photo)

    elif mesg in ('отмена', 'cancel'):
        msg = telebot.types.ReplyKeyboardRemove()
        bot.send_photo(message.chat.id, open('bye.jpg', 'rb'), reply_markup=msg, caption='До скорых встреч!')
    else:
        bot.send_message(message.chat.id, 'Если хотите выйти, просто нажмите на нопку отмены')

@bot.message_handler(content_types=['photo'])
def remake_photo(message):
    mesg = message.photo.file_id
    print(mesg)




bot.polling(none_stop=True)