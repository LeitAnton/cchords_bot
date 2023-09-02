import telebot

from database import User, Favorite, Song


class TelegramBOT:
    def __init__(self, token, database, parser):
        self.parser = parser
        self.database = database

        self.channel = telebot.TeleBot(token, parse_mode=None)
        print('Bot started')

        self.tracks_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)

        self.keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        self.keyboard.row('/find_chords', '/favorite', '/history')

        self.keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
        self.keyboard1.row('/back')

        self.favorit_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        self.favorit_keyboard.row('/yes', '/now')

        self.channel.add_message_handler(dict(
            function=lambda msg, obj=self: obj.start_handler,
            filters=dict(
                commands=['start', 'back'],
            )
        ))

        self.channel.add_message_handler(dict(
            function=lambda msg, obj=self: obj.after_text(msg),
            filters=dict(
                commands=['find_chords', 'favorite', 'history'],
            )
        ))

        self.channel.polling()

    def start_handler(self, message):
        print("START command")
        self.channel.send_message(message.from_user.id, "Добро пожаловать в бота Chords BOT",
                                  reply_markup=self.keyboard)

    def after_text(self, message):
        match message.text:
            case '/find_chords':
                msg = self.channel.send_message(message.from_user.id, 'Enter track name:',
                                                reply_markup=self.keyboard1)
                self.channel.register_next_step_handler(msg, self.find_tracklist)
            case '/favorite':
                self.channel.send_message(message.from_user.id, 'Your favorite:', reply_markup=self.keyboard1)
                self.view_favorite(message)
            case '/history':
                self.channel.send_message(message.from_user.id, 'History:', reply_markup=self.keyboard)
                self.channel.register_next_step_handler(message, self.history)

    def find_tracklist(self, message):
        self.channel.send_message(message.from_user.id, 'Find song ', reply_markup=self.keyboard)

        self.name_link = self.parser.find_songs_am_dm(message.text)

        if self.name_link is None:
            return self.channel.send_message(message.from_user.id, 'Nothing found', reply_markup=self.keyboard)

        for name in self.name_link.keys():
            self.tracks_keyboard.add(name)

        msg = self.channel.send_message(message.from_user.id, 'Choose from the list below ',
                                        reply_markup=self.tracks_keyboard)
        self.channel.register_next_step_handler(msg, self.viewing_chords, type='find')

    def view_favorite(self, message):
        pass

    def history(self, message):
        self.channel.send_message(message.from_user.id, 'HISTORY ', reply_markup=self.keyboard)

    def viewing_chords(self, message, type):
        match type:
            case 'find':
                track = self.parser.get_accords(self.name_link[message.text])

        self.channel.send_message(message.from_user.id, track['chords'])
        msg = self.channel.send_message(message.from_user.id, 'Add to favorite?', reply_markup=self.favorit_keyboard)
        self.channel.register_next_step_handler(msg, self.add_to_favorite, track=track)

    def add_to_favorite(self, message, track):
        pass
