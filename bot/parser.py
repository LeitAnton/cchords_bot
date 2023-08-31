import requests

from bs4 import BeautifulSoup
from collections import namedtuple


def find_songs_am_dm(message):
    URL = f"https://amdm.ru/search/?q={'+'.join(message.split(' '))}"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml')

    if 'Ничего не найдено' == soup.find('article', class_='g-padding-left').find('h1').text:
        return None

    list_tr = soup.find('table', class_='items').findAll('tr')[1:10]
    songs = {}
    for tr in list_tr:
        list_a = tr.find('td', class_='artist_name').findAll('a', class_='artist')
        named = list_a[0].text + ' - ' + list_a[1].text
        if named not in songs.keys() and len(songs.keys()) < 5:
            songs[named] = str(list_a[1]).split('"')[3]

    return songs


def find_songs_my_chords(message):
    URL = f"https://mychords.net/ru/search?q={'+'.join(message.split(' '))}&src=1&sortby=rel&resorder=desc&page=1"
    print(URL)
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml')
    print(soup)
    print(soup.findAll('div', class_='f-message f-message-warning'))

    return 'Yes'


print(find_songs_my_chords('Love'))


def get_accords(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('title').text

    pre = soup.find('pre', class_='field__podbor_new podbor__text')
    return {'title': title, 'chords': [i for i in pre.text.split('\n\n') if i != '']}
