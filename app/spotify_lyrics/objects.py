from json import dumps

from .exceptions import SpotifyIdError
from .utils import extract_source_name


class Jsonable:
    def get_dict_representation(self) -> dict:
        return dict()

    def to_json(self):
        dict_representation = self.get_dict_representation()
        json_song = dumps(dict_representation)

        return json_song


class SpotifySong(Jsonable):
    __slots__ = ['name', 'artists', 'duration', 'is_explicit', 'spotify_url', 'album']

    def __init__(self, track_data: dict):
        if not self.is_song_playable(track_data):
            raise SpotifyIdError("Song is not playable")

        self.name = track_data['name']
        artists_unparsed = track_data['artists']
        self.artists = [artist['name'] for artist in artists_unparsed]

        self.duration = int(track_data['duration_ms'] / 1000)
        self.is_explicit = track_data['explicit']

        album_data = track_data['album']

        self.album = {
            'name': album_data['name'],
            'url': album_data['href'],
            'images': album_data['images'],
        }

    def __str__(self):
        return f'SpotifySong(artists="{", ".join(self.artists)}", song_name="{self.name}", is_explicit={self.is_explicit}, duration={self.duration}s)'

    def __repr__(self):
        return f'SpotifySong(artists="{", ".join(self.artists)}", song_name="{self.name}")'

    def get_dict_representation(self):
        dict_representation = {
            "name": self.name,
            "artists": self.artists,
            "duration": self.duration,
            "is_explicit": self.is_explicit,
            "album": self.album,
        }
        return dict_representation

    @staticmethod
    def is_song_playable(track_data: dict):
        return not track_data['is_local']


class Lyrics(Jsonable):
    __slots__ = ['lyrics', 'source_url', 'source_name']

    def __init__(self, lyrics: str, source_url: str):
        self.lyrics = lyrics
        self.source_url = source_url
        if len(source_url) > 0:
            self.source_name = extract_source_name(source_url)
        else:
            self.source_name = source_url

    def get_dict_representation(self):
        dict_representation = {'lyrics_source_url': self.source_url, 'lyrics_source_name': self.source_name,
                               'lyrics': self.lyrics}
        return dict_representation


def merge_song_and_lyrics_to_dict(song: SpotifySong, lyrics: Lyrics) -> dict:
    dict_representation = dict(**song.get_dict_representation(), **lyrics.get_dict_representation())
    dict_representation['error_occurred'] = False
    return dict_representation
