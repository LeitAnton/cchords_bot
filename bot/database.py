import sqlite3

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
    cur.execute("""CREATE TABLE IF NOT EXISTS user (
                                    user_id INT PRIMARY KEY,
                                    username VARCHAR(255)
                                    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS favorite (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    user_id INT,
                                    song_id INT
                                    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS song (
                                    song_id INT AUTO_INCREMENT PRIMARY KEY,
                                    artist_name VARCHAR(255),
                                    song_name VARCHAR(255),
                                    link VARCHAR(255)
                                    );""")


def add_user(user_id, username):
    cur.execute(f"""INSERT INTO user (user_id, username)
                    VALUES ({user_id}, {username});""")


def add_song(artist_name, song_name, link):
    cur.execute(f"""INSERT INTO song (artist_name, 
                                      song_name, 
                                      link
                                      )
                    VALUES ({artist_name},  
                             {song_name},
                             {link}
                             );""")


def get_songs():
    cur.execute("""SELECT song_id, artist_name, song_name, link 
                   FROM song;""")


def get_users():
    cur.execute("""SELECT user_id, username 
                   FROM user;""")


def get_favorites(user_id=None, song_id=None):
    if user_id:
        cur.execute(f"""SELECT favorite_id, user_id, song_id
                        FROM favorite
                        WHERE user_id = {user_id};""")
    elif song_id:
        cur.execute(f"""SELECT favorite_id, user_id, song_id
                        FROM favorite
                        WHERE song_id = {song_id};""")
    else:
        cur.execute(f"""SELECT favorite_id, user_id, song_id
                        FROM favorite;""")
