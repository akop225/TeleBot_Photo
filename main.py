import random
import sqlite3
import time

import telebot
from PIL import Image, ImageDraw, ImageFont
from telebot.types import InputMediaPhoto
import os
import state
import SizesAndPrices

PERCENTS = [i for i in range(10, 101, 10)]


bot = telebot.TeleBot('5468702833:AAGS0zvI_rXxlYh9yOnnGDBAxYbquoDA7Q0')

con = sqlite3.connect('telebot_data.db')
cur = con.cursor()
cur.execute("""Create TABLE IF NOT EXISTS states(
        chat_id INT,
        numb_of_state INT,
        percent_of_sight INT);
        """)
cur.execute("""Create TABLE IF NOT EXISTS SizesAndPrices(
        chat_id INT,
        min_size INT,
        max_size INT,
        price INT);
        """)
con.commit()

@bot.message_handler(content_types=['photo', 'text'])
def main(message):
    chat_id = message.chat.id
    print(message)
    nstate = state.get_state(chat_id)

    if nstate == 0:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        photo = telebot.types.KeyboardButton('Наложить водяной знак')
        price = telebot.types.KeyboardButton('Прайс')
        markup.add(photo, price)
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!', reply_markup=markup)
        nstate += 1
        state.update_state(chat_id, nstate)

##### ВОДЯНОЙ ЗНАК #####

    elif nstate == 1 and message.content_type == 'text' and message.text.strip() == 'Наложить водяной знак':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        change = [telebot.types.KeyboardButton(f'{i}') for i in range(10, 101, 10)]

        end = telebot.types.KeyboardButton('Выход')
        markup.add(change[0], change[1], change[2], change[3], change[4], change[5], change[6], change[7], change[8],
                   change[9], end)
        bot.send_message(message.chat.id, "Введите процент прозрачности", reply_markup=markup)
        nstate += 1
        state.update_state(chat_id, nstate)

    elif nstate == 2 and message.content_type == 'text' and message.text.isdigit() and not (0 < int(message.text.strip()) < 100):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        change = [telebot.types.KeyboardButton(f'{i}') for i in range(10, 101, 10)]

        end = telebot.types.KeyboardButton('Выход')
        markup.add(change[0], change[1], change[2], change[3], change[4], change[5], change[6], change[7], change[8],
                   change[9], end)
        bot.send_message(message.chat.id, "Вы ввели неправильный процент прозрачности!\n"
                                          "Введите число от 0 до 100", reply_markup=markup)

    elif nstate == 2 and message.content_type == 'text' and message.text.isdigit() and int(message.text) in PERCENTS:
        state.update_percent_of_sight(chat_id, int(message.text.strip()))
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        change = telebot.types.KeyboardButton('Изменить прозрачность')

        end = telebot.types.KeyboardButton('Выход')
        markup.add(change, end)
        bot.send_message(message.chat.id, "Отправьте фотографию", reply_markup=markup)
        nstate += 1
        state.update_state(chat_id, nstate)

    elif nstate == 3 and message.content_type == 'photo':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        change = telebot.types.KeyboardButton('Изменить прозрачность')

        end = telebot.types.KeyboardButton('Выход')
        markup.add(change, end)

        try:
            time.sleep(0.5)
            file_info = bot.get_file(message.photo[-1].file_id)
            download_file = bot.download_file(file_info.file_path)

            with open('user_photo.png', 'wb') as user_photo:
                user_photo.write(download_file)
            image = Image.open("user_photo.png").convert("RGBA")

            size = 150

            logo = Image.new('RGBA', image.size, (0, 0, 0, 0))
            font = ImageFont.truetype("edosz.ttf", size)
            d = ImageDraw.Draw(logo)
            sight = state.get_percent_of_sight(chat_id)
            d.text((logo.width // 2 - (size * 4 // 3), logo.height // 2 - (size * 4 // 3)), 'J U S T\nP E A K',
                   fill=(255, 255, 255, int(255 * sight / 100)), font=font)
            combined = Image.alpha_composite(image, logo)
            bot.send_photo(message.chat.id, combined, reply_markup=markup)
        except:
            bot.send_message(chat_id, 'В коде произошла ошибка... Попробуйте еще раз', reply_markup=markup)

    elif nstate == 3 and message.content_type == 'text' and message.text.strip() == 'Изменить прозрачность':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        change = [telebot.types.KeyboardButton(f'{i}') for i in range(10, 101, 10)]

        end = telebot.types.KeyboardButton('Выход')
        markup.add(change[0], change[1], change[2], change[3], change[4], change[5], change[6], change[7], change[8],
                   change[9], end)
        bot.send_message(message.chat.id, "Введите процент прозрачности", reply_markup=markup)
        state.update_state(chat_id, nstate - 1)

##### PRICE #####

    elif nstate == 1 and message.content_type == 'text' and message.text.strip() == 'Прайс':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        change = [telebot.types.KeyboardButton(f'{i}') for i in range(36, 46)]

        end = telebot.types.KeyboardButton('Назад')
        markup.add(change[0], change[1], change[2], change[3], change[4], change[5], change[6], change[7], change[8],
                   change[9], end)
        bot.send_message(message.chat.id, "Введите наименьший размер", reply_markup=markup)
        
        SizesAndPrices.start_price_and_size(chat_id)
        nstate += 1
        state.update_state(chat_id, nstate)
    
    elif nstate == 2 and message.content_type == 'text' and message.text.strip() == 'Назад':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        photo = telebot.types.KeyboardButton('Наложить водяной знак')
        price = telebot.types.KeyboardButton('Прайс')
        markup.add(photo, price)
        bot.send_message(message.chat.id, f'Чего желаете?',
                         reply_markup=markup)
        
        nstate = 1
        state.update_state(chat_id, nstate)

    elif nstate == 2 and message.content_type == 'text' and message.text.isdigit():
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        change = [telebot.types.KeyboardButton(f'{i}') for i in range(36, 46)]

        end = telebot.types.KeyboardButton('Назад')
        markup.add(change[0], change[1], change[2], change[3], change[4], change[5], change[6], change[7], change[8],
                   change[9], end)
        bot.send_message(message.chat.id, "Введите наибольший размер", reply_markup=markup)
        
        SizesAndPrices.update_min_size(chat_id, int(message.text.strip()))
        nstate += 1
        state.update_state(chat_id, nstate)

    elif nstate == 3 and message.content_type == 'text' and message.text.strip() == 'Назад':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        change = [telebot.types.KeyboardButton(f'{i}') for i in range(36, 46)]

        end = telebot.types.KeyboardButton('Назад')
        markup.add(change[0], change[1], change[2], change[3], change[4], change[5], change[6], change[7], change[8],
                   change[9], end)
        bot.send_message(message.chat.id, "Введите наименьший размер", reply_markup=markup)

        nstate = 2
        state.update_state(chat_id, nstate)
        
    elif nstate == 3 and message.content_type == 'text' and message.text.isdigit():
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        end = telebot.types.KeyboardButton('Назад')
        markup.add(end)
        bot.send_message(message.chat.id, 'Введите цену', reply_markup=markup)
        
        SizesAndPrices.update_max_size(chat_id, int(message.text.strip()))
        nstate += 1
        state.update_state(chat_id, nstate)

    elif nstate == 4 and message.content_type == 'text' and message.text.strip() == 'Назад':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        change = [telebot.types.KeyboardButton(f'{i}') for i in range(36, 46)]

        end = telebot.types.KeyboardButton('Назад')
        markup.add(change[0], change[1], change[2], change[3], change[4], change[5], change[6], change[7], change[8],
                   change[9], end)
        bot.send_message(message.chat.id, "Введите наибольший размер", reply_markup=markup)

        nstate = 3
        state.update_state(chat_id, nstate)

    elif nstate == 4 and message.content_type == 'text' and message.text.isdigit():
        SizesAndPrices.update_price(chat_id, int(message.text.strip()))

        msg = f'Размерный ряд: {SizesAndPrices.get_min_size(chat_id)}-{SizesAndPrices.get_max_size(chat_id)}\n\nЦена: ' \
              f'{SizesAndPrices.get_price(chat_id)} ₽\n\nПо заказу и вопросам пишите @justpeaker'

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        photo = telebot.types.KeyboardButton('Наложить водяной знак')
        price = telebot.types.KeyboardButton('Прайс')
        markup.add(photo, price)
        bot.send_message(message.chat.id, msg,
                         reply_markup=markup)
        nstate = 1
        state.update_state(chat_id, nstate)

    elif message.content_type == 'text' and message.text.strip() == 'Выход':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        start = telebot.types.KeyboardButton('Начать')
        markup.add(start)
        bot.send_message(message.chat.id, 'До скорых встреч!', reply_markup=markup)
        nstate = 0
        state.update_state(chat_id, nstate)

    else:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        photo = telebot.types.KeyboardButton('Наложить водяной знак')
        price = telebot.types.KeyboardButton('Прайс')
        markup.add(photo, price)
        bot.send_message(message.chat.id, f'Вы ввели что-то нереальное и магическое!\n'
                                          f'Возвращаю Вас в начальное меню',
                         reply_markup=markup)
        nstate = 1
        state.update_state(chat_id, nstate)


# @bot.message_handler(commands=['start', 'go'])
# def start(message):
#     markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     photo = telebot.types.KeyboardButton('Наложить водяной знак')
#     end = telebot.types.KeyboardButton('Отмена')
#
#     markup.add(photo, end)
#     msg = bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!', reply_markup=markup)
#     bot.register_next_step_handler(msg, search)
#
#
# @bot.message_handler(content_types='text')
# def search(message):
#     mesg = message.text.lower()
#     if ("знак") in mesg:
#         markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
#         change = [telebot.types.KeyboardButton(f'{i}') for i in range(10, 101, 10)]
#         end = telebot.types.KeyboardButton('Отмена')
#         markup.add(change[0], change[1], change[2], change[3], change[4], change[5], change[6], change[7], change[8],
#                    change[9], end)
#         msg = bot.send_message(message.chat.id, "Введите процент прозрачности", reply_markup=markup)
#         bot.register_next_step_handler(msg, remake_photo)
#
#     elif mesg in ('go', 'го', 'давай', "заводись", "начать"):
#         markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#         photo = telebot.types.KeyboardButton('Наложить водяной знак')
#         end = telebot.types.KeyboardButton('Отмена')
#
#         markup.add(photo, end)
#         msg = bot.send_message(message.chat.id,
#                                f'Привет, {message.from_user.first_name} {message.from_user.last_name}!',
#                                reply_markup=markup)
#         bot.register_next_step_handler(msg, search)
#
#     elif 'изменить' in message.text.lower():
#         markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
#         change = [telebot.types.KeyboardButton(f'{i}') for i in range(10, 101, 10)]
#         end = telebot.types.KeyboardButton('Отмена')
#         markup.add(change[0], change[1], change[2], change[3], change[4], change[5], change[6], change[7], change[8],
#                    change[9], end)
#         msg = bot.send_message(message.chat.id, "Введите процент прозрачности", reply_markup=markup)
#         bot.register_next_step_handler(msg, remake_photo)
#
#     elif mesg in ('отмена', 'cancel'):
#         markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#         start = telebot.types.KeyboardButton('Начать')
#         markup.add(start)
#         m = bot.send_message(message.chat.id, 'До скорых встреч!', reply_markup=markup)
#         bot.register_next_step_handler(m, search)
#     else:
#         bot.send_message(message.chat.id, 'Если хотите выйти, просто нажмите на нопку отмены')
#
#
# procent_of_sight = [35]
# LIST_OF_IMAGES = []
# last_media = ''
#
# @bot.message_handler(content_types=['photo', 'text'])
# def remake_photo(message):
#     global last_media, LIST_OF_IMAGES
#     if message.content_type == "text":
#         if str(parse(message.text)).isdigit():
#             procent_of_sight[0] = parse(message.text)
#             markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#             change = telebot.types.KeyboardButton('Изменить прозрачность')
#             end = telebot.types.KeyboardButton('Отмена')
#             markup.add(change, end)
#             msg = bot.send_message(message.chat.id, "Отправьте фотографию", reply_markup=markup)
#             bot.register_next_step_handler(msg, remake_photo)
#         elif 'изменить' in message.text.lower():
#             markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
#             change = [telebot.types.KeyboardButton(f'{i}') for i in range(10, 101, 10)]
#             end = telebot.types.KeyboardButton('Отмена')
#             markup.add(change[0], change[1], change[2], change[3], change[4], change[5], change[6], change[7], change[8], change[9], end)
#             msg = bot.send_message(message.chat.id, "Введите процент прозрачности", reply_markup=markup)
#             bot.register_next_step_handler(msg, remake_photo)
#
#         elif message.text.lower() in ('отмена', 'cancel'):
#             markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#             start = telebot.types.KeyboardButton('Начать')
#             markup.add(start)
#             m = bot.send_message(message.chat.id, 'До скорых встреч!', reply_markup=markup)
#             bot.register_next_step_handler(m, search)
#         else:
#             bot.send_message(message.chat.id, 'Если хотите выйти, просто нажмите на нопку отмены')
#     else:
#         file_info = bot.get_file(message.photo[-1].file_id)
#         download_file = bot.download_file(file_info.file_path)
#
#         with open('user_photo.png', 'wb') as user_photo:
#             user_photo.write(download_file)
#         image = Image.open("user_photo.png").convert("RGBA")
#
#         size = 150
#
#         logo = Image.new('RGBA', image.size, (0, 0, 0, 0))
#         font = ImageFont.truetype("edosz.ttf", size)
#         d = ImageDraw.Draw(logo)
#         sight = procent_of_sight[0]
#         d.text((logo.width // 2 - (size * 4 // 3), logo.height // 2 - (size * 4 // 3)), 'J U S T\nP E A K',
#                fill=(255, 255, 255, int(255 * sight / 100)), font=font)
#         combined = Image.alpha_composite(image, logo)
#         bot.send_photo(message.chat.id, combined)


bot.polling(none_stop=True)