import os

import telebot

from parser import find_songs_am_dm, get_accords

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('/find_chords')
keyboard1.row('/back')

TRACKLIST = {}


@bot.message_handler(commands=['start'])
def start_messages(message):
    bot.send_message(message.from_user.id, "What do you want to do?", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def after_text(message):
    if message.text == '/find_chords':
        msg = bot.send_message(message.from_user.id, 'Enter track name:', reply_markup=keyboard1)
        bot.register_next_step_handler(msg, find_tracklist)
    elif message.text == '/back':
        start_messages(message)


def find_tracklist(message):
    name_link = find_songs_am_dm(message.text)
    if name_link is None:
        return bot.send_message(message.from_user.id, 'Nothing found', reply_markup=keyboard)

    songs = {}
    for index, elem in enumerate(name_link.keys()):
        TRACKLIST[str(index)] = name_link[elem]
        songs[elem] = {'callback_data': str(index)}

    tracks_keyboard = telebot.util.quick_markup(songs, row_width=2)
    bot.send_message(message.from_user.id, 'Choose from the list below ', reply_markup=tracks_keyboard)


@bot.callback_query_handler(func=lambda callback: True)
def check_callback_data(callback):
    track = get_accords(str(TRACKLIST[callback.data]))
    bot.send_message(callback.from_user.id, track['title'])
    # bot.send_message(callback.from_user.id, track['chords'], reply_markup=keyboard)
    for elem in track['chords']:
        bot.send_message(callback.from_user.id, elem, reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
