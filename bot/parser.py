import requests

from bs4 import BeautifulSoup
from collections import namedtuple


def find_song(message):
    q = "+".join(message.split(' '))
    URL = f"https://amdm.ru/search/?q={q}"

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml')

    if 'Ничего не найдено' == soup.find('article', class_='g-padding-left').find('h1').text:
        return 'Ничего не найдено'

    table = soup.find('table', class_='items')
    list_tr = table.findAll('tr')[1:10]
    list_of_tracks = []
    Track = namedtuple('Track', ['name', 'link'])
    for tr in list_tr:
        td = tr.find('td', class_='artist_name')
        list_a = td.findAll('a', class_='artist')
        list_of_tracks.append(Track(name=list_a[0].text+' - '+list_a[1].text, link=str(list_a[1]).split('"')[3]))

    return list_of_tracks


def get_accords(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('title').text

    pre = soup.find('pre', class_='field__podbor_new podbor__text')
    return {'title': title, 'chords': pre.text}
