class User:
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username


class Song:
    def __init__(self, artist_name: str, song_name: str, link: str, song_id: int = None):
        self.artist_name = artist_name
        self.song_name = song_name
        self.link = link
        self.song_id = song_id

    def __str__(self):
        return f"{self.artist_name} - {self.song_name}"


class Favorite:
    def __init__(self, user_id: int, song_id: int, favorite_id: int = None):
        self.user_id = user_id
        self.song_id = song_id
        self.favorite_id = favorite_id


class History:
    def __init__(self, user_id: int, song_id: int, viewing_time: str = None, history_id: int = None):
        self.user_id = user_id
        self.song_id = song_id
        self.viewing_time = viewing_time
        self.history_id = history_id


class TemporaryBuffer:
    def __init__(self, temporary_id: int, artist_name: str, song_name: str, link: str):
        self.temporary_id = temporary_id
        self.artist_name = artist_name
        self.song_name = song_name
        self.link = link

    def __str__(self):
        return f"{self.artist_name} - {self.song_name}"
