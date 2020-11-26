from datetime import datetime
from json import loads

from requests import models, get

from .exceptions import ServerScrapingError


def convert_str_to_datetime(date_string:str, datetime_pattern:str) -> datetime:
	date = datetime.strptime(date_string, datetime_pattern)
	return date


def get_json_from_file(file_path:str) -> dict:
	with open(file_path, 'r') as file:
		file_content = file.read()
	return loads(file_content)


def is_request_valid(request:models.Response) -> bool:
	return 200 <= request.status_code < 299

def request_page(url:str, **kwargs) -> str:
	page_request = get(url, **kwargs)

	if not is_request_valid(page_request):
		raise ServerScrapingError("Error occured while scraping the web")

	return page_request.content

def extract_source_name(source_url:str) -> str:
	source_name = source_url.split('//')[-1].split('/')[0]
	return source_name
