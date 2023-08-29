import os

import telebot

from parser import find_song

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
    for i in list_of_tuples:
        keys = tracklist_dict.keys()
        if i.name not in keys and len(keys) != 5:
            # tracklist_dict[i.name] = {'url': i.link}
            tracklist_dict[i.name] = {'url': i.link}

    keyboard_tracklist = telebot.util.quick_markup(tracklist_dict, row_width=2)
    # keyboard_tracklist = telebot.types.ReplyKeyboardMarkup(row_width=2)
    # for i in list_of_tuples[:5]:
    #     keyboard_tracklist.add(i.name)
    bot.send_message(message.from_user.id, 'Choose from the list below ', reply_markup=keyboard_tracklist)


@bot.callback_query_handler(func=lambda callback: True)
def check_callback_data(callback):
    print(callback.data)


bot.polling(none_stop=True, interval=0)
