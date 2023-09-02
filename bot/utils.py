from models import Song


class CustomList(list):
    def not_in_list(self, element_to_check):
        if type(element_to_check) == Song:
            for element_of_list in self:
                if (element_to_check.artist_name == element_of_list.artist_name
                        and element_to_check.song_name == element_of_list.song_name):
                    return False
            return True

    def keys(self):
        try:
            if type(self[0]) == Song:
                return [song.artist_name + ' - ' + song.song_name for song in self]

        except IndexError:
            return None
