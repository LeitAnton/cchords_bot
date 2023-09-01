import os
import sqlite3
import telebot

from parser import find_songs_am_dm, get_accords
from database import create_tables

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

try:
    con = sqlite3.connect("../database.sqlite")
    cur = con.cursor()
    create_tables()

    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/find_chords', '/favorite', 'history', 'language')
    keyboard1.row('/back')

    TRACKLIST = {}


    @bot.message_handler(commands=['start'])
    def start_messages(message):
        bot.send_message(message.from_user.id, "What do you want to do?", reply_markup=keyboard)


    @bot.message_handler(content_types=['text'])
    def after_text(message):
        match message.text:
            case '/find_chords':
                msg = bot.send_message(message.from_user.id, 'Enter track name:', reply_markup=keyboard1)
                bot.register_next_step_handler(msg, find_tracklist)
            case '/favorite':
                bot.send_message(message.from_user.id, 'Your favorite:')
                favorite(message)
            case '/history':
                bot.send_message(message.from_user.id, 'History:', reply_markup=keyboard)
                pass
            case 'language':
                bot.send_message(message.from_user.id, 'Language:', reply_markup=keyboard)
                pass
            case '/back':
                start_messages(message)


    def find_tracklist(message):
        name_link = find_songs_am_dm(message.text)
        if name_link is None:
            return bot.send_message(message.from_user.id, 'Nothing found', reply_markup=keyboard)

        songs = {}
        print(name_link)
        for index, elem in enumerate(name_link.keys()):
            TRACKLIST[str(index)] = name_link[elem]
            songs[elem] = {'callback_data': f"find%{index}"}

        tracks_keyboard = telebot.util.quick_markup(songs, row_width=2)
        bot.send_message(message.from_user.id, 'Choose from the list below ', reply_markup=tracks_keyboard)


    def favorite(message):
        songs = {'Макс Корж - Напалм': 'https://amdm.ru/akkordi/maks_korzh/164782/napalm/',
                 'Макс Корж - 17 лет': 'https://amdm.ru/akkordi/maks_korzh/174154/17_let/',
                 'Макс Корж - Не говорите другу никогда': 'https://amdm.ru/akkordi/maks_korzh/188936/ne_govorite_drugu_nikogda/',
                 'Макс Корж - Young haze': 'https://amdm.ru/akkordi/maks_korzh/190649/young_haze/',
                 'Макс Корж - Снадобье': 'https://amdm.ru/akkordi/maks_korzh/190651/snadobe/'}

        for index, elem in enumerate(songs.keys()):
            TRACKLIST[str(index)] = songs[elem]
            songs[elem] = {'callback_data': f"find%{index}"}

        tracks_keyboard = telebot.util.quick_markup(songs, row_width=2)
        bot.send_message(message.from_user.id, 'Choose from the list below ', reply_markup=tracks_keyboard)
        pass


    @bot.callback_query_handler(func=lambda callback: True)
    def check_callback_data(callback):
        prefix, index = callback.data.split('%')
        match prefix:
            case 'find':
                track = get_accords(str(TRACKLIST[index]))
                bot.send_message(callback.from_user.id, track['chords'], reply_markup=keyboard)


    bot.polling(none_stop=True, interval=0)

finally:
    con.close()
