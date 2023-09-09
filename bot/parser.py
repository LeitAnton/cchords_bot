import os
import requests

from bs4 import BeautifulSoup
from models import Song, TemporaryBuffer


message_len = 4096


def get_accords(link: str) -> dict[str, str]:
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('title').text

    pre_text = soup.find('pre', class_='field__podbor_new podbor__text').text

    separated_text = []
    part = ''
    for line in pre_text.split('\n'):
        if len(f'{part}{os.linesep}{line}') <= message_len:
            part += f'{os.linesep}{line}'
        else:
            separated_text.append(part)
            part = f'{os.linesep}{line}'
    separated_text.append(part)

    return {'title': title, 'chords': separated_text}


def find_songs_on_site_am_dm(message, database) -> [list[TemporaryBuffer], None]:
    url = f"https://amdm.ru/search/?q={'+'.join(message.split(' '))}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    if 'Ничего не найдено' == soup.find('article', class_='g-padding-left').find('h1').text:
        return None

    list_tr = soup.find('table', class_='items').findAll('tr')[1:10]

    songs = []

    for tr in list_tr:
        list_a = tr.find('td', class_='artist_name').findAll('a', class_='artist')
        song = Song(list_a[0].text, list_a[1].text, str(list_a[1]).split('"')[3])
        if song not in songs:
            songs.append(song)

    database.save_into_database(songs)

    temporary = []
    for song in database.get_songs(songs=songs):
        temporary.append(TemporaryBuffer(song.song_id, song.artist_name, song.song_name, song.link))

    return temporary
