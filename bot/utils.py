from models import Song, TemporaryBuffer


class CustomList(list):
    def not_in_list(self, element_to_check) -> bool:
        if type(element_to_check) == Song:
            for element_of_list in self:
                if (element_to_check.artist_name == element_of_list.artist_name
                        and element_to_check.song_name == element_of_list.song_name):
                    return False
            return True

    def keys(self) -> list:
        try:
            if type(self[0]) in (Song, TemporaryBuffer):
                return [str(song) for song in self]

        except IndexError:
            return list()


def create_tracks_keyboard(temporary: CustomList) -> list[list[dict]]:
    result = []
    for name in temporary.keys():
        result.append([{'text': str(name)}])
    return result
