import os

import telebot

from parser import find_song, get_accords

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('/find_chords')
keyboard1.row('/back')


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
    list_of_tuples = find_song(message.text)
    if type(list_of_tuples) == str:
        return bot.send_message(message.from_user.id, 'Nothing found', reply_markup=keyboard)

    tracklist_dict = {}
    for i, elem in enumerate(list_of_tuples):
        keys = tracklist_dict.keys()
        if elem.name not in keys and len(keys) != 5:
            tracklist_dict[elem.name] = {'callback_data': str(i)}

    keyboard_tracklist = telebot.util.quick_markup(tracklist_dict, row_width=2)
    bot.send_message(message.from_user.id, 'Choose from the list below ', reply_markup=keyboard_tracklist)


@bot.callback_query_handler(func=lambda callback: True)
def check_callback_data(callback):
    track = get_accords('https'+str(callback.data))
    bot.send_message(callback.from_user.id, track['title'])
    bot.send_message(callback.from_user.id, track['chords'])


bot.polling(none_stop=True, interval=0)
