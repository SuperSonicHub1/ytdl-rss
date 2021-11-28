__version__ = '1.0.0'

from flask import Flask

def create_app():
	app = Flask(__name__)

	from .views import views
	app.register_blueprint(views)

	return app
