import time

from typing import Any
from models import User, Song, Favorite


class Database:
    @staticmethod
    def get_users(self) -> list[dict[str, Any]]:
        self.cursor.execute("""SELECT user_id, username FROM user;""")
        result = []
        for user_id, username in self.cursor.fetchall():
            result.append(
                {'user_id': user_id,
                 'username': username}
            )
        return result

    @staticmethod
    def get_songs(self) -> list[dict[str, Any]]:
        self.cursor.execute("""SELECT song_id, artist_name, song_name, link 
                       FROM song;""")
        result = []
        for song_id, artist_name, song_name, link in self.cursor.fetchall():
            result.append(
                {'song_id': song_id,
                 'artist_name': artist_name,
                 'song_name': song_name,
                 'link': link}
            )
        return result

    @staticmethod
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

        result = []
        for favorite_id, user_id, song_id in self.cursor.fetchall():
            result.append(
                {'favorite_id': favorite_id,
                 'user_id': user_id,
                 'song_id': song_id}
            )
        return result

    @staticmethod
    def save_into_database(self, some_object):
        if type(some_object) == User:
            self.cursor.execute(f"""SELECT *
                            FROM user
                            WHERE song.user_id = {some_object.user_id}""")

            if not self.cursor.fetchall():
                self.cursor.execute(f"""INSERT INTO user (user_id, username)
                                VALUES ({some_object.user_id}, '{some_object.username}');""")
                self.connection.commit()
                return 'Added'
            return 'Already exist'

        elif type(some_object) == Favorite:
            self.cursor.execute(f"""SELECT *
                            FROM favorite
                            WHERE favorite.favorite_id = '{some_object.favorite_id}'
                              AND favorite.song_id = '{some_object.song_id}'""")

            if not self.cursor.fetchall():
                self.cursor.execute(f"""INSERT INTO favorite (user_id, song_id)
                                VALUES ({some_object.user_id}, '{some_object.song_id}');""")
                self.connection.commit()
                return 'Added'
            return 'Already exist'

        elif type(some_object) == Song:
            self.cursor.execute(f"""SELECT *
                            FROM song
                            WHERE song.song_name = '{some_object.song_name}'
                              AND song.artist_name = '{some_object.artist_name}'""")

            if not self.cursor.fetchall():
                self.cursor.execute(f"""INSERT INTO song (artist_name, song_name, link)
                                VALUES ('{some_object.artist_name}', '{some_object.song_name}', '{some_object.link}');
                                """)
                self.connection.commit()
                return 'Added'
            return 'Already exist'

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
        print('Table song started')
        time.sleep(1)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite
        (
            id      INT AUTO_INCREMENT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            song_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES user(user_id),
            FOREIGN KEY(song_id) REFERENCES song(song_id)
        );""")
        print('Table favorite started')
        time.sleep(1)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS history
        (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            song_id      INTEGER NOT NULL,
            viewing_time VARCHAR(26),
            FOREIGN KEY(user_id) REFERENCES user(user_id),
            FOREIGN KEY(song_id) REFERENCES song(song_id)
        );""")
        print('Table history started')
        self.connection.commit()

