from os import path, getcwd

from flask import Blueprint, render_template, send_from_directory, abort

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')


@main.route('/', methods=['GET'])
def index():
	return render_template('index.html')


@main.route('/static/<path:filename>')
def serve_static(filename: str):
	static_dir = path.normpath(path.join(path.dirname(getcwd()), 'app', 'static'))

	# abort if user is trying to access files outside static file
	if ".." in path.normpath(filename).split(path.sep):
		abort(403)

	return send_from_directory(static_dir, filename)


@main.route('/song/<string:song_id>', methods=['GET'])
def song(song_id):
	return render_template('song-lyrics-page.html', song_id=song_id)
