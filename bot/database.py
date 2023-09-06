import time

from typing import Any
from models import User, Song, Favorite, TemporaryBuffer, History
from utils import CustomList


def create_tables(connection, cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user
    (
        user_id  INT PRIMARY KEY,
        username VARCHAR(255) NOT NULL
    );""")
    print('Table user started')
    time.sleep(1)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS song
    (
        song_id     INTEGER PRIMARY KEY AUTOINCREMENT,
        artist_name VARCHAR(255),
        song_name   VARCHAR(255),
        link        TEXT
    );""")
    time.sleep(1)
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS un_song_id ON song (artist_name, song_name);")
    print('Table song started')
    time.sleep(1)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favorite
    (
        favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER NOT NULL,
        song_id     INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES user(user_id),
        FOREIGN KEY(song_id) REFERENCES song(song_id)
    );""")
    time.sleep(1)
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS un_fav_id ON favorite (user_id, song_id);")
    print('Table favorite started')
    time.sleep(1)

    cursor.execute("""
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
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS un_his_id ON history (user_id, song_id);")
    print('Table history started')
    time.sleep(1)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS temporary_buffer
    (
        temporary_id INTEGER PRIMARY KEY NOT NULL,
        artist_name  VARCHAR(255),
        song_name    VARCHAR(255),
        link         TEXT
    );""")
    time.sleep(1)
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS un_tem_id ON temporary_buffer (artist_name, song_name);")
    print('Table temporary_buffer started')

    connection.commit()


class Serializer:
    @staticmethod
    def serialize_to_models(type_of_data: [User, Song, Favorite, History, TemporaryBuffer], data: Any) -> CustomList:
        result = CustomList()
        if type_of_data == User:
            for user_id, username in data:
                result.append(User(user_id, username))

        elif type_of_data == Song:
            for song_id, artist_name, song_name, link in data:
                result.append(Song(artist_name, song_name, link, song_id))

        elif type_of_data == Favorite:
            for favorite_id, user_id, song_id in data:
                result.append(Favorite(user_id, song_id, favorite_id))

        elif type_of_data == History:
            for history_id, song_id, user_id, viewing_time in data:
                result.append(History(history_id, user_id, song_id, viewing_time))

        elif type_of_data == TemporaryBuffer:
            for temporary_id, artist_name, song_name, link in data:
                result.append(TemporaryBuffer(temporary_id, artist_name, song_name, link))

        if result == CustomList():
            return None

        return result


class Database:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def save_into_database(self, objects: CustomList[Any]) -> str:
        try:
            values = ''
            if type(objects[0]) == User:
                for element in objects:
                    values += f"({element.user_id}, '{element.username}'), "

                self.cursor.execute("INSERT INTO user (user_id, username) " +
                                    f"VALUES {values[:-2]}" +
                                    "on conflict do nothing;")
                self.connection.commit()

            elif type(objects[0]) == Song:
                for element in objects:
                    values += f"""("{element.artist_name.replace('"', "'")}", 
                            "{element.song_name.replace('"', "'")}", 
                            "{element.link.replace('"', "'")}"), """
                self.cursor.execute("INSERT INTO song (artist_name, song_name, link) " +
                                    f"VALUES {values[:-2]}" +
                                    "on conflict do nothing;")
                self.connection.commit()

            elif type(objects[0]) == Favorite:
                for element in objects:
                    values += f"({element.user_id}, {element.song_id}), "

                self.cursor.execute("INSERT INTO favorite (user_id, song_id) " +
                                    f"VALUES {values[:-2]}" +
                                    "on conflict do nothing;")
                self.connection.commit()

            elif type(objects[0]) == History:
                for element in objects:
                    values += f"""({element.user_id}, {element.song_id}, datetime('now')), """
                self.cursor.execute("INSERT INTO history (user_id, song_id, viewing_time) " +
                                    f"VALUES {values[:-2]}" +
                                    "on conflict do nothing;")
                self.connection.commit()

            elif type(objects[0]) == TemporaryBuffer:
                for element in objects:
                    values += f"""
                    ("{element.temporary_id}", "{element.artist_name.replace('"', "'")}", 
                    "{element.song_name.replace('"', "'")}", "{element.link.replace('"', "'")}"), """

                self.cursor.execute("INSERT INTO temporary_buffer (temporary_id, artist_name, song_name, link) " +
                                    f"VALUES {values[:-2]}" +
                                    "on conflict do nothing;")
                self.connection.commit()
            return 'Added'

        except IndexError:
            return 'List is empty'

    def get_users(self, user_id: int = None) -> CustomList[User]:
        if user_id:
            self.cursor.execute(f"""SELECT user_id, username FROM user
                                   WHERE user_id = {user_id};""")
        else:
            self.cursor.execute("""SELECT user_id, username FROM user;""")
        return Serializer.serialize_to_models(User, self.cursor.fetchall())

    def get_songs(self, songs: CustomList[Song] = None, song_id_list: list[int] = None) -> CustomList[Song]:
        if songs:
            where = ''
            for song in songs:
                where += f"""("{song.artist_name.replace('"', "'")}", "{song.song_name.replace('"', "'")}"), """
            self.cursor.execute("SELECT * FROM song " +
                                f"WHERE (artist_name, song_name) in ({where[:-2]});")
        elif song_id_list:
            where = ''
            for elem in song_id_list:
                where += f"'{elem}', "
            self.cursor.execute(f"""SELECT song_id, artist_name, song_name, link
                                           FROM song
                                               WHERE song_id in ({where[:-2]});""")
        else:
            self.cursor.execute("""SELECT song_id, artist_name, song_name, link 
                                   FROM song;""")
        return Serializer.serialize_to_models(Song, self.cursor.fetchall())

    def get_favorites(self, favorite_id: int = None, user_id: int = None, song_id: int = None) -> CustomList[Favorite]:
        query = """SELECT favorite_id, user_id, song_id FROM favorite """
        if user_id:
            self.cursor.execute(query + f"WHERE user_id = {user_id};")
        elif song_id:
            self.cursor.execute(query + f"WHERE song_id = {song_id};")
        elif favorite_id:
            self.cursor.execute(query + f"WHERE favorite_id = {favorite_id};")
        else:
            self.cursor.execute(query + ";")
        return Serializer.serialize_to_models(Favorite, self.cursor.fetchall())

    def get_history(self, user_id: int):
        self.cursor.execute(f"""SELECT history_id, user_id, song_id, viewing_time
                                FROM history
                                WHERE user_id = {user_id};""")
        return Serializer.serialize_to_models(History, self.cursor.fetchall())

    def get_temporary_buffer(self) -> CustomList[TemporaryBuffer]:
        self.cursor.execute("""SELECT temporary_id, artist_name, song_name, link 
                               FROM temporary_buffer;""")
        return Serializer.serialize_to_models(TemporaryBuffer, self.cursor.fetchall())

    def clear_temporary_buffer(self):
        self.cursor.execute("DELETE FROM temporary_buffer;")
        self.connection.commit()

    def delete_favorite(self, favorite: Favorite):
        self.cursor.execute(f"""DELETE FROM favorite
                                WHERE favorite.user_id = {favorite.user_id} 
                                    AND favorite.song_id = {favorite.song_id}""")
        self.connection.commit()
