from flask import abort, Blueprint, render_template, request, Response
from .generator import create_feed, NotAPlaylistException

views = Blueprint("views", __name__, url_prefix="/")

@views.errorhandler(NotAPlaylistException)
def not_a_playlist(e):
	return str(e), 406

@views.route("/")
def index():
	return render_template("index.html")

@views.route("/feed")
def feed():
	url = request.args.get("url")
	if not url:
		abort(400)
	feed = create_feed(url)
	return Response(feed.rss(), mimetype='application/rss+xml')
