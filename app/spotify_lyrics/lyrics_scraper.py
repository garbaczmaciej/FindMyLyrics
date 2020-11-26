"""

INTRODUCTION
	A module usef for parsing and scraping the web for lyrics of a song

CLASSESS
	-WebLyricsParser(): a class containing only staticmethods, used for parsing the webpage content, it is used by WebLyricsScraper

		PUBLIC METHODS:
			-parse_google_lyrics(google_soup:BeautifulSoup) -> str
			-parse_google_links(google_soup:BeautifulSoup) -> list
			-parse_links_to_tekstowo(google_links:list) -> list
			-parse_tekstowo_lyrics(tekstowo_soup:BeautifulSoup) -> str

	-WebLyricsScraper(): a class used for scraping the web for lyrics, it has only classmethods ,it uses WebLyricsParser staticmethods

		PUBLIC METHODS:
			-find_lyrics(cls, song:spotify_lyrics.objects.SpotifySong) -> spotify_lyrics.objects.Lyrics
			-get_google_lyrics_url(cls, song:spotify_lyrics.objects.SpotifySong) -> str
			-

"""

from urllib.parse import quote, unquote

# In order for it to work you need an lxml package
import requests
from bs4 import BeautifulSoup

from .objects import SpotifySong, Lyrics
from .exceptions import LyricsNotFound
from .utils import request_page


class WebLyricsParser:
	@staticmethod
	def parse_google_lyrics(google_soup: BeautifulSoup) -> str:
		google_lyrics_unparsed = google_soup.find('div', class_='hwc')
		if not google_lyrics_unparsed:
			return ""

		try:
			google_lyrics = str(google_lyrics_unparsed)[88:-24]
			return google_lyrics

		except IndexError:
			return ""

	@staticmethod
	def parse_google_links(google_soup: BeautifulSoup) -> list:
		google_a_tags = google_soup.find_all("a", href=True)
		google_links = [a_tag['href'][7:] for a_tag in google_a_tags if
						len(a_tag.text) > 0 and a_tag['href'][:7] == "/url?q="]
		return google_links

	@staticmethod
	def parse_links_to_tekstowo(google_links: list) -> list:
		tekstowo_links = [link for link in google_links if "tekstowo.pl" in link]
		return tekstowo_links

	@staticmethod
	def parse_tekstowo_lyrics(tekstowo_soup: BeautifulSoup) -> str:
		lyrics = tekstowo_soup.find("div", {"id": "songText"})
		try:

			# Formatting tekstowo lyrics, they have weird format
			lyrics = str(lyrics).replace("<br/>", "")
			lyrics = lyrics[80:lyrics.find("<p>") - 4]

			return lyrics.strip()
		except IndexError:
			return ""


class WebLyricsScraper:
	GOOGLE_SEARCH_URL = r"https://www.google.com/search?q="
	GOOGLE_REQUEST_HEADERS = {"Accept-Encoding": "gzip"}

	@classmethod
	def find_lyrics(cls, song: SpotifySong) -> Lyrics:
		google_lyrics_url = cls.get_google_lyrics_url(song)
		google_result_page = request_page(google_lyrics_url, headers=cls.GOOGLE_REQUEST_HEADERS)
		google_soup = BeautifulSoup(google_result_page, "lxml")

		google_lyrics = WebLyricsParser.parse_google_lyrics(google_soup)
		if len(google_lyrics.split()) > 0:
			return Lyrics(google_lyrics, google_lyrics_url)

		google_links = WebLyricsParser.parse_google_links(google_soup)
		tekstowo_links = WebLyricsParser.parse_links_to_tekstowo(google_links)

		for tekstowo_link in tekstowo_links:
			tekstowo_content = request_page(tekstowo_link)
			tekstowo_soup = BeautifulSoup(tekstowo_content, "lxml")

			tekstowo_lyrics = WebLyricsParser.parse_tekstowo_lyrics(tekstowo_soup)
			if len(tekstowo_lyrics.split()) > 0:
				return Lyrics(tekstowo_lyrics, tekstowo_link)

		raise LyricsNotFound("Lyrics not found in available resources")

	@classmethod
	def get_google_lyrics_url(cls, song: SpotifySong) -> str:
		search_phrase = f"{', '.join(song.artists)} - {song.name} tekst"
		lyrics_url = cls.GOOGLE_SEARCH_URL + quote(search_phrase)

		return lyrics_url
