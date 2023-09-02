import time

from typing import Any
from models import User, Song, Favorite, TemporaryBuffer
from utils import CustomList


class Database:
    @staticmethod
    def serialize_to_models(type_of_data, data):
        result = CustomList()
        if type_of_data == User:
            for user_id, username in data:
                result.append(User(user_id, username))
            return result

        elif type_of_data == Song:
            for song_id, artist_name, song_name, link in data:
                result.append(Song(artist_name, song_name, link, song_id))
            return result

        elif type_of_data == Favorite:
            for favorite_id, user_id, song_id in data:
                result.append(Favorite(user_id, song_id, favorite_id))
            return result

        elif type_of_data == TemporaryBuffer:
            for temporary_id, artist_name, song_name, link in data:
                result.append(TemporaryBuffer(temporary_id, artist_name, song_name, link))
            return result

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS user
        (
            user_id  INT PRIMARY KEY,
            username VARCHAR(255) NOT NULL
        );""")
        print('Table user started')
        time.sleep(1)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS song
        (
            song_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_name VARCHAR(255),
            song_name   VARCHAR(255),
            link        TEXT
        );""")
        time.sleep(1)
        self.cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS un_song_id ON song (artist_name, song_name);")
        print('Table song started')
        time.sleep(1)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite
        (
            favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            song_id     INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES user(user_id),
            FOREIGN KEY(song_id) REFERENCES song(song_id)
        );""")
        time.sleep(1)
        self.cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS un_fav_id ON favorite (user_id, song_id);")
        print('Table favorite started')
        time.sleep(1)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS history
        (
            history_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            song_id      INTEGER NOT NULL,
            viewing_time VARCHAR(26),
            FOREIGN KEY(user_id) REFERENCES user(user_id),
            FOREIGN KEY(song_id) REFERENCES song(song_id)
        );""")
        time.sleep(1)
        self.cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS un_his_id ON history (user_id, song_id);")
        print('Table history started')
        time.sleep(1)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS temporary_buffer
        (
            temporary_id INTEGER PRIMARY KEY NOT NULL,
            artist_name  VARCHAR(255),
            song_name    VARCHAR(255),
            link         TEXT
        );""")
        time.sleep(1)
        self.cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS un_tem_id ON temporary_buffer (artist_name, song_name);")
        print('Table temporary_buffer started')

        self.connection.commit()

    def save_into_database(self, some_object):
        try:
            values = ''
            if type(some_object[0]) == User:
                for element in some_object:
                    values += f"({element.user_id}, '{element.username}'), "

                self.cursor.execute("INSERT INTO user (user_id, username) " +
                                    f"VALUES {values[:-2]}" +
                                    "on conflict do nothing;")
                self.connection.commit()

            elif type(some_object[0]) == Song:
                for element in some_object:
                    values += f"""("{element.artist_name}", "{element.song_name}", "{element.link}"), """

                self.cursor.execute("INSERT INTO song (artist_name, song_name, link) " +
                                    f"VALUES {values[:-2]}" +
                                    "on conflict do nothing;")
                self.connection.commit()

            elif type(some_object[0]) == Favorite:
                for element in some_object:
                    values += f"({element.user_id}, {element.song_id}), "

                self.cursor.execute("INSERT INTO favorite (user_id, song_id) " +
                                    f"VALUES {values[:-2]}" +
                                    "on conflict do nothing;")
                self.connection.commit()

            elif type(some_object[0]) == TemporaryBuffer:
                for element in some_object:
                    values += f"""
                    ("{element.temporary_id}", "{element.artist_name}", "{element.song_name}", "{element.link}"), """

                self.cursor.execute("INSERT INTO temporary_buffer (temporary_id, artist_name, song_name, link) " +
                                    f"VALUES {values[:-2]}" +
                                    "on conflict do nothing;")
                self.connection.commit()

        except IndexError:
            return 'List is empty'

    def get_users(self) -> list[dict[str, Any]]:
        self.cursor.execute("""SELECT user_id, username FROM user;""")
        return self.serialize_to_models(User, self.cursor.fetchall())

    def get_songs(self, song_id: list = None, songs: CustomList = None) -> list[dict[str, Any]]:
        if songs:
            where = ''
            for song in songs:
                where += f"""("{song.artist_name}", "{song.song_name}"), """
            self.cursor.execute("SELECT * FROM song " +
                                f"WHERE (artist_name, song_name) in ({where[:-2]});")
        elif song_id:
            where = ''
            for elem in song_id:
                where += f"'{elem}', "
            print(f"""SELECT song_id, artist_name, song_name, link 
                                           FROM song
                                               WHERE song_id in ({where[:-2]});""")
            self.cursor.execute(f"""SELECT song_id, artist_name, song_name, link 
                                           FROM song
                                               WHERE song_id in ({where[:-2]});""")
        else:
            self.cursor.execute("""SELECT song_id, artist_name, song_name, link 
                                   FROM song;""")
        return self.serialize_to_models(Song, self.cursor.fetchall())

    def get_favorites(self, favorite_id: int = None, user_id: int = None, song_id: int = None) -> list[dict[str, Any]]:
        query = """SELECT favorite_id, user_id, song_id FROM favorite """
        if user_id:
            self.cursor.execute(query + f"WHERE user_id = {user_id};")
        elif song_id:
            self.cursor.execute(query + f"WHERE song_id = {song_id};")
        elif favorite_id:
            self.cursor.execute(query + f"WHERE favorite_id = {favorite_id};")
        else:
            self.cursor.execute(query + ";")
        return self.serialize_to_models(Favorite, self.cursor.fetchall())

    def get_temporary_buffer(self) -> list[dict[str, Any]]:
        self.cursor.execute("""SELECT temporary_id, artist_name, song_name, link 
                               FROM temporary_buffer;""")
        return self.serialize_to_models(TemporaryBuffer, self.cursor.fetchall())

    def clear_temporary_buffer(self):
        self.cursor.execute("DELETE FROM temporary_buffer;")
        self.connection.commit()
