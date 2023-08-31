import sqlite3

con = sqlite3.connect("../database.sqlite")
cur = con.cursor()

#
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
#


def start_base():
    cur.execute("""CREATE TABLE IF NOT EXISTS user (
                                    user_id INT PRIMARY KEY,
                                    username VARCHAR(255),
                                    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS favorite (
                                    id INT PRIMARY KEY,
                                    user_id INT,
                                    song_id INT
                                    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS song (
                                    song_id INT PRIMARY KEY,
                                    artist_name VARCHAR(255),
                                    song_name VARCHAR(255),
                                    link VARCHAR(255)
                                    );""")


def add_user(user_id, username):
    cur.execute(f"""INSERT INTO user (user_id, username)
                    VALUES ({user_id}, {username});""")


def add_song(artist_name, song_name, link):
    cur.execute(f"""INSERT INTO song (song_id,
                                      artist_name, 
                                      song_name, 
                                      link
                                      )
                    VALUES ((SELECT COUNT(*) FROM song)+1,
                             {artist_name},  
                             {song_name},
                             {link}
                             );""")


def select_songs():
    cur.execute("""SELECT song_id, artist_name, song_name, link 
                   FROM song;""")


def select_users():
    cur.execute("""SELECT song_id, artist_name, song_name, link 
                   FROM song;""")
