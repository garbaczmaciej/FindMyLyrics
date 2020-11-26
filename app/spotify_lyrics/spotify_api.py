"""

INTRODUCTION
	A module used for connecting with spotify_api

REQUIREMENTS
	You need to obtain a client id and client secret from spotify API page in order for this module to work

CLASSES
	- SpotifyToken(client_id:str, client_secret:str, serialization_path:str) - SpotifyToken object is used by SpotifyAPI,
		serialization_path is a physical path where you can store a serialized token(JSON format)

		PUBLIC METHODS:
			- to_json(self) -> str
			- _deserialize(self)
			- serialize(self)
			- is_access_key_expired(self) -> bool
			- update_access_key(self)
			- update_access_key_if_expired(self)

	- SpotifyAPI(token:SpotifyToken): SpotifyAPI object is used for communicating with SpotifyAPI

		PUBLIC METHODS:
			- get_song(self, spotify_url:str) -> spotify_lyrics.objects.SpotifySong
			- get_track_data(self, track_id:str) -> dict

"""

import base64
import datetime
import json

import requests

from .utils import get_json_from_file, convert_str_to_datetime, is_request_valid
from .objects import SpotifySong
from .exceptions import SpotifyRequestError, SpotifyIdError, SpotifyTrackNotFound


class SpotifyToken:
	REQUEST_URL = r"https://accounts.spotify.com/api/token"
	REQUEST_DATA = {'grant_type' : 'client_credentials'}
	DATETIME_PATTERN = "%m/%d/%y %H:%M:%S"

	__slots__ = ['_request_header', '_serialization_path','_access_key_expiration', 'access_key']

	def __init__(self, client_id: str, client_secret: str, serialization_path: str):
		client_credentials = f"{client_id}:{client_secret}"
		client_credentials_base64 = base64.b64encode(client_credentials.encode())
		self._request_header = {"Authorization": f"Basic {client_credentials_base64.decode()}"}

		self._serialization_path = serialization_path

		try:
			deserialized_token = self._deserialize()
			self._access_key_expiration = deserialized_token['access_key_expiration']
			self.access_key = deserialized_token['access_key']
			self.update_access_key_if_expired()

		except FileNotFoundError as error:
			self.update_access_key()

	def to_json(self) -> str:
		date_str = self._access_key_expiration.strftime(self.DATETIME_PATTERN)
		dict_representation = {'access_key_expiration' : date_str, 'access_key' : self.access_key}
		json_token = json.dumps(dict_representation)
		return json_token

	def update_access_key_if_expired(self) -> None:
		if self._is_access_key_expired():
			self.update_access_key()

	def update_access_key(self) -> None:
		token_request = requests.post(self.REQUEST_URL, data=self.REQUEST_DATA, headers=self._request_header)

		if not is_request_valid(token_request):
			raise SpotifyRequestError("Error occured while requesting spotify API token")

		token = token_request.json()

		self._access_key_expiration = datetime.datetime.now() + datetime.timedelta(seconds=token['expires_in'])
		self.access_key = token['access_token']

		self._serialize()

	def _is_access_key_expired(self) -> bool:
		return self._access_key_expiration <= datetime.datetime.now() + datetime.timedelta(minutes=2)

	def _deserialize(self) -> dict:
		deserialized_token = get_json_from_file(self._serialization_path)
		deserialized_token['access_key_expiration'] = convert_str_to_datetime(deserialized_token['access_key_expiration'], self.DATETIME_PATTERN)
		return deserialized_token

	def _serialize(self) -> None:
		json_token = self.to_json()
		with open(self._serialization_path, "w") as file:
			file.write(json_token)


class SpotifyAPI:
	TRACK_REQUEST_URL = "https://api.spotify.com/v1/tracks/"
	TRACK_ID_LENGTH = 22

	__slots__ = ['token']

	def __init__(self, token:SpotifyToken):
		self.token = token

	def get_song(self, track_id: str) -> SpotifySong:
		track_data = self.get_track_data(track_id)
		song = SpotifySong(track_data)
		return song

	def get_track_data(self, track_id) -> dict:
		self.token.update_access_key_if_expired()

		spotify_request_url = self.TRACK_REQUEST_URL + track_id
		track_request = requests.get(spotify_request_url, headers = self._get_track_request_header())

		if not is_request_valid(track_request):
			raise SpotifyIdError("SpotifySong could not be found")

		track_data = track_request.json()
		return track_data

	def _get_track_request_header(self) -> dict:
		return {"Authorization": f"Bearer {self.token.access_key}"}
