import requests
import datetime

from bs4 import BeautifulSoup
from models import Song
from utils import CustomList


class Parser:
    @staticmethod
    def get_accords(self, link):
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('title').text

        pre = soup.find('pre', class_='field__podbor_new podbor__text')
        # return {'title': title, 'chords': [i for i in pre.text.split('\n\n') if i != '']}
        return {'title': title, 'chords': pre.text}

    def __init__(self, database):
        self.database = database

    def find_songs_am_dm(self, message):
        URL = f"https://amdm.ru/search/?q={'+'.join(message.split(' '))}"
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'lxml')
        if 'Ничего не найдено' == soup.find('article', class_='g-padding-left').find('h1').text:
            return None

        list_tr = soup.find('table', class_='items').findAll('tr')[1:10]

        songs = CustomList()
        for tr in list_tr:
            list_a = tr.find('td', class_='artist_name').findAll('a', class_='artist')
            song = Song(list_a[0].text, list_a[1].text, str(list_a[1]).split('"')[3])
            print(song)
            if songs.not_in_list(song):
                songs.append(song)

            self.database.save_into_database(songs)

        return songs
