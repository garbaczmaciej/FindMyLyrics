"""

INTRODUCTION
    A package used for finding lyrics of a song, given the spotify URL


REQUIREMENTS
    You need to obtain a client id and client secret from spotify API page in order for spotify_api module to work


    PACKAGE MODULES:
    - spotify_api:  a module used for connecting with spotify_api

    - lyrics_scraper: a module used for parsing and scraping the web for lyrics of a song

    - objects: a module containing objects used in this package

    - exceptions: a module containing exceptions used in this package

    - utils: utilities used in this package

"""

from . import lyrics_scraper
from . import spotify_api
from . import objects
from . import exceptions
from . import utils
