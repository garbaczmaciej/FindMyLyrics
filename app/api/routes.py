
from flask import Blueprint, jsonify

from .spotify_api_manager import get_song_data

api = Blueprint('api', __name__)


@api.route('/song/<string:song_id>', methods=["GET"])
def song_lyrics(song_id):
	return jsonify(get_song_data(song_id))
