import telebot

from utils import CustomList
from models import User, Song, Favorite, TemporaryBuffer


class TelegramBOT:
    def __init__(self, token, database, parser):
        self.parser = parser
        self.database = database

        self.channel = telebot.TeleBot(token, parse_mode=None)
        print('Bot started')

        self.keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        self.keyboard.row('/find_chords', '/favorite', '/history')

        self.vote_favorite_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        self.vote_favorite_keyboard.row('yes', 'no')

        self.channel.add_message_handler(dict(
            function=lambda msg, obj=self: obj.after_text(msg),
            filters=dict(
                commands=['start', 'find_chords', 'favorite', 'history'],
            )
        ))

        self.channel.polling()

    def after_text(self, message):
        match message.text:
            case '/start':
                self.start_handler(message)

            case '/find_chords':
                msg = self.channel.send_message(message.from_user.id, 'Enter track name:')
                self.channel.register_next_step_handler(msg, self.view_tracklist)

            case '/favorite':
                self.view_tracklist(message)

            case '/history':
                self.channel.send_message(message.from_user.id, 'History:', reply_markup=self.keyboard)
                self.channel.register_next_step_handler(message, self.history)

    def start_handler(self, message):
        user = User(message.from_user.id, message.from_user.username)
        self.database.save_into_database([user])
        self.channel.send_message(message.from_user.id, "What do you want to do?",
                                  reply_markup=self.keyboard)

    def view_tracklist(self, message):
        self.channel.send_message(message.from_user.id, 'Find song ', reply_markup=self.keyboard)

        self.parser.find_songs_am_dm(message.text)
        temporary = self.database.get_temporary_buffer()

        if temporary is None:
            return self.channel.send_message(message.from_user.id, 'Nothing found', reply_markup=self.keyboard)

        tracks_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        for name in temporary.keys():
            tracks_keyboard.add(str(name))

        msg = self.channel.send_message(message.from_user.id, 'Choose from the list below ',
                                        reply_markup=tracks_keyboard)
        self.channel.register_next_step_handler(msg, self.viewing_chords, type_of_request='find')

    def view_favorite(self, message):
        self.channel.send_message(message.from_user.id, 'Your favorite:')

        favorite = self.database.get_favorites()
        songs = self.database.get_songs(song_id=[elem.song_id for elem in favorite])
        print(songs)
        tracks_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        for name in songs.keys():
            tracks_keyboard.add(name)

        msg = self.channel.send_message(message.from_user.id, 'Choose from the list below ',
                                        reply_markup=tracks_keyboard)
        self.channel.register_next_step_handler(msg, self.viewing_chords, type_of_request='favorite')

    def history(self, message):
        self.channel.send_message(message.from_user.id, 'HISTORY ', reply_markup=self.keyboard)

    def viewing_chords(self, message, type_of_request):
        match type_of_request:
            case 'find':
                songs = self.database.get_temporary_buffer()
                for song in songs:
                    if message.text == str(song):
                        track = self.parser.get_accords(song.link)
                        break

            case 'favorite':
                songs = self.database.get_favorites()

        for song in songs:
            if message.text == str(song):
                track = self.parser.get_accords(song.link)
                break

        self.channel.send_message(message.from_user.id, track['chords'])
        msg = self.channel.send_message(message.from_user.id, 'Add to favorite?',
                                        reply_markup=self.vote_favorite_keyboard)
        self.channel.register_next_step_handler(msg, self.add_to_favorite, name_of_added_track=message.text)

    def add_to_favorite(self, message, name_of_added_track):
        if message.text == 'yes':
            songs = self.database.get_temporary_buffer()

            for song in songs:
                if name_of_added_track == str(song):
                    some = CustomList()
                    favorite = Favorite(message.from_user.id, song.temporary_id)
                    some.append(favorite)
                    self.database.save_into_database(some)
                    self.channel.send_message(message.from_user.id, 'Song added!',
                                              reply_markup=self.keyboard)
                    break

        elif message.text == 'no':
            self.start_handler(message)

        self.database.clear_temporary_buffer()
