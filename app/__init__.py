
from flask import Flask, Blueprint

from . import main, api

def create_app():
	app = Flask(__name__)


	app.register_blueprint(main.main_bp)
	app.register_blueprint(api.api_bp, url_prefix="/api")

	return app
