from os import environ

from ..spotify_lyrics import spotify_api, lyrics_scraper
from ..spotify_lyrics.objects import merge_song_and_lyrics_to_dict
from ..spotify_lyrics.exceptions import *


CLIENT_ID = environ["CLIENT_ID"]
CLIENT_SECRET = environ["CLIENT_SECRET"]
TOKEN_PATH = r"app/private/spotify_access_key.json"


def create_error_dict(error_type: str, error_message: str) -> dict:
	error_dict = dict()

	error_dict['error'] = True
	error_dict['error_type'] = error_type
	error_dict['error_message'] = error_message

	return error_dict


def get_song_data(song_id:str) -> dict:
	try:
		response = get_song_and_lyrics(song_id)

	except (SpotifyRequestError, ServerScrapingError) as error:
		response = create_error_dict(str(type(error)), "Something went wrong on our side!")

	except (SpotifyIdError, SpotifyTrackNotFound) as error:
		response = create_error_dict(str(type(error)), "We could not find your song")

	except LyricsNotFound as error:
		response = create_error_dict(str(type(error)), "We could not find lyrics of your song")

	finally:
		return response


def get_song_and_lyrics(song_id:str) -> dict:
	spotify_token = spotify_api.SpotifyToken(CLIENT_ID, CLIENT_SECRET, TOKEN_PATH)
	spotify_client = spotify_api.SpotifyAPI(spotify_token)

	song = spotify_client.get_song(song_id)
	lyrics = lyrics_scraper.WebLyricsScraper.find_lyrics(song)

	return merge_song_and_lyrics_to_dict(song, lyrics)
