
class User:
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username


class Song:
    def __init__(self, artist_name: str, song_name: str, link: str):
        self.artist_name = artist_name
        self.song_name = song_name
        self.link = link


class Favorite:
    def __init__(self, user_id: int, song_id: int, favorite_id: int = None):
        self.user_id = user_id
        self.song_id = song_id
        self.favorite_id = favorite_id
