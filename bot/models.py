class User:
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username

    def __str__(self):
        return f"{'{'}'user_id': {self.user_id}, 'username': {self.username}{'}'}"


class Song:
    def __init__(self, artist_name: str, song_name: str, link: str, song_id: int = None):
        self.artist_name = artist_name
        self.song_name = song_name
        self.link = link
        self.song_id = song_id

    def __str__(self):
        return f"{'{'}'artist_name': {self.artist_name}, 'song_name': {self.song_name}, 'link': {self.link}{'}'}"


class Favorite:
    def __init__(self, user_id: int, song_id: int, favorite_id: int = None):
        self.user_id = user_id
        self.song_id = song_id
        self.favorite_id = favorite_id

    def __str__(self):
        return f"{'{'}'user_id': {self.user_id}, 'song_id': {self.song_id}, 'favorite_id': {self.favorite_id}{'}'}"


