import telebot
import logging

from parser import find_songs_on_site_am_dm, get_accords
from utils import CustomList, create_tracks_keyboard
from models import User, Song, Favorite, TemporaryBuffer, History


class TelegramBOT:
    def __init__(self, token, database):
        self.database = database

        self.channel = telebot.TeleBot(token, parse_mode=None)
        logging.info('Bot started')

        self.keyboard = telebot.types.ReplyKeyboardMarkup(True)
        self.keyboard.row('/find_chords', '/favorite', '/history')

        self.vote_favorite_keyboard = telebot.types.ReplyKeyboardMarkup(True)
        self.vote_favorite_keyboard.row('yes', 'no')

        self.channel.add_message_handler(dict(
            function=lambda msg, obj=self: obj.on_main_command(msg),
            filters=dict(
                commands=['start', 'find_chords', 'favorite', 'history'],
            )
        ))

        self.channel.polling()

    def on_main_command(self, message):
        match message.text:
            case '/start':
                self.channel.send_message(message.from_user.id, 'Welcome to Chords bot!')
                self.start_handling(message)

            case '/find_chords':
                msg = self.channel.send_message(message.from_user.id, 'Enter track name:')
                self.channel.register_next_step_handler(msg, self.find_songs)

            case '/favorite':
                self.channel.send_message(message.from_user.id, 'Your favorite:')
                self.view_favorite(message)

            case '/history':
                self.channel.send_message(message.from_user.id, 'History:', reply_markup=self.keyboard)
                self.view_history(message)

    def start_handling(self, message):
        user = User(message.from_user.id, message.from_user.username)
        self.database.save_into_database(CustomList([user]))
        self.channel.send_message(message.from_user.id, "What do you want to do?",
                                  reply_markup=self.keyboard)

    def find_songs(self, message):
        self.channel.send_message(message.from_user.id, 'Find song...', reply_markup=self.keyboard)
        founded_songs = find_songs_on_site_am_dm(message.text, self.database)
        if founded_songs is None:
            return self.channel.send_message(message.from_user.id, 'Nothing found', reply_markup=self.keyboard)
        else:
            self.database.save_into_database(founded_songs)
        return self.view_tracklist(message)

    def view_favorite(self, message):
        favorite = self.database.get_favorites()
        if favorite is None:
            return self.channel.send_message(message.from_user.id, 'Favorite is empty', reply_markup=self.keyboard)

        songs = self.database.get_songs(song_id_list=[elem.song_id for elem in favorite])
        return self.view_tracklist(message, songs)

    def view_history(self, message):
        history = self.database.get_history(message.from_user.id)
        if history is None:
            return self.channel.send_message(message.from_user.id, 'History is empty', reply_markup=self.keyboard)

        song_id_list = list(set([elem.song_id for elem in history]))
        songs = self.database.get_songs(song_id_list=song_id_list)
        return self.view_tracklist(message, songs)

    def view_tracklist(self, message, songs: CustomList[Song] = None):
        if songs is None:
            temporary = self.database.get_temporary_buffer()
        else:
            temporary = CustomList()
            for song in songs:
                temporary.append(TemporaryBuffer(song.song_id, song.artist_name, song.song_name, song.link))

            self.database.save_into_database(temporary)
        tracks_keyboard = telebot.types.ReplyKeyboardMarkup(True)
        tracks_keyboard.keyboard = [[{'text': '/back'}]] + create_tracks_keyboard(temporary)

        msg = self.channel.send_message(message.from_user.id, 'Choose from the list below ',
                                        reply_markup=tracks_keyboard)

        # return self.channel.register_next_step_handler(msg, self.view_chords)
        return self.channel.register_next_step_handler(msg, self.check_answer, tracks_keyboard=tracks_keyboard)

    def check_answer(self, message, tracks_keyboard):
        if [{'text': message.text}] in tracks_keyboard.keyboard:
            if message.text == '/back':
                return self.start_handling(message)
            return self.view_chords(message)
        else:
            msg = self.channel.send_message(message.from_user.id, 'Not from list', reply_markup=tracks_keyboard)
            return self.channel.register_next_step_handler(msg, self.check_answer, tracks_keyboard=tracks_keyboard)

    def view_chords(self, message):
        songs = self.database.get_temporary_buffer()
        track = {}
        for song in songs:
            if message.text == str(song):
                track = get_accords(song.link)
                history = History(message.from_user.id, song.temporary_id)
                self.database.save_into_database(CustomList([history]))
                break

        for part in track['chords']:
            self.channel.send_message(message.from_user.id, part)

        msg = self.channel.send_message(message.from_user.id, 'Add to favorite?',
                                        reply_markup=self.vote_favorite_keyboard)
        return self.channel.register_next_step_handler(msg, self.add_to_favorite, name_of_added_track=message.text)

    def add_to_favorite(self, message, name_of_added_track):
        temporary_songs = self.database.get_temporary_buffer()
        favorite = CustomList()
        for song in temporary_songs:
            if name_of_added_track == str(song):
                favorite.append(Favorite(message.from_user.id, song.temporary_id))
                break

        if message.text == 'yes':
            self.database.save_into_database(favorite)
            self.channel.send_message(message.from_user.id, 'Song added!')

        elif message.text == 'no':
            self.database.delete_favorite(favorite[0])
            self.channel.send_message(message.from_user.id, 'Song deleted from favorite!')

        self.database.clear_temporary_buffer()
        return self.start_handling(message)
