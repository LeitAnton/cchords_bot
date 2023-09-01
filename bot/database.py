import sqlite3
from typing import List, Dict, Any

con = sqlite3.connect("../database.sqlite")
cur = con.cursor()


#     Telegram user
#     {'id': 576195008,
#     'is_bot': False,
#     'first_name': 'Антон',
#     'username': 'x_phanton',
#     'last_name': None,
#     'language_code': 'en',
#     'can_join_groups': None,
#     'can_read_all_group_messages': None,
#     'supports_inline_queries': None,
#     'is_premium': None,
#     'added_to_attachment_menu': None}

def create_tables():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user
    (
        user_id  INT PRIMARY KEY,
        username VARCHAR(255)
    );
    
    CREATE TABLE IF NOT EXISTS favorite
    (
        id      INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT,
        song_id INT
    );
    CREATE TABLE IF NOT EXISTS song
    (
        song_id     INT PRIMARY KEY AUTO_INCREMENT,
        artist_name VARCHAR(255),
        song_name   VARCHAR(255),
        link        VARCHAR(255)
    );""")
    con.commit()


class User:
    @staticmethod
    def get_users() -> list[dict[str, Any]]:
        cur.execute("""SELECT user_id, username FROM user;""")
        result = []
        for user_id, username in cur.fetchall():
            result.append(
                {'user_id': user_id,
                 'username': username}
            )
        return result

    def __int__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def save_into_database(self):
        cur.execute(f"""INSERT INTO user (user_id, username)
                        VALUES ({self.user_id}, '{self.username}');""")
        con.commit()


class Song:
    @staticmethod
    def get_songs() -> list[dict[str, Any]]:
        cur.execute("""SELECT song_id, artist_name, song_name, link 
                       FROM song;""")
        result = []
        for song_id, artist_name, song_name, link in cur.fetchall():
            result.append(
                {'song_id': song_id,
                 'artist_name': artist_name,
                 'song_name': song_name,
                 'link': link}
            )
        return result

    def __int__(self, artist_name: str, song_name: str, link: str):
        self.artist_name = artist_name
        self.song_name = song_name
        self.link = link

    def save_into_database(self):
        cur.execute(f"""INSERT INTO song (artist_name, song_name, link)
                        VALUES ('{self.artist_name}', '{self.song_name}', '{self.link}');""")
        con.commit()


class Favorite:
    @staticmethod
    def get_favorites(favorite_id: int = None, user_id: int = None, song_id: int = None) -> list[dict[str, Any]]:
        query = """SELECT favorite_id, user_id, song_id FROM favorite """
        if user_id:
            cur.execute(query + f"WHERE user_id = {user_id};")
        elif song_id:
            cur.execute(query + f"WHERE song_id = {song_id};")
        elif favorite_id:
            cur.execute(query + f"WHERE song_id = {favorite_id};")
        else:
            cur.execute(query + ";")

        result = []
        for favorite_id, user_id, song_id in cur.fetchall():
            result.append(
                {'favorite_id': favorite_id,
                 'user_id': user_id,
                 'song_id': song_id}
            )
        return result

    def __init__(self, user_id: int, song_id: int, favorite_id: int = None,):
        self.user_id = user_id
        self.song_id = song_id
        self.favorite_id = favorite_id

