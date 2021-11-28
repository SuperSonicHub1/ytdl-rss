from youtube_dl import YoutubeDL
from rfeed import Item, Feed, Guid
from datetime import datetime
from html import escape

# Make a logger to more easily catch errors
ytdl_opts = {
	"quiet": True,
	"dump_single_json": True,
}

ytdl = YoutubeDL(ytdl_opts)

class NotAPlaylistException(Exception):
	pass

def create_item(entry: dict):
	item_info = {}
	# "title" is the only required field
	item_info["title"] = entry["title"]
	item_info["author"] = entry.get("uploader")
	item_info["categories"] = entry.get("tags")

	# Generate descripption
	description = ""
	thumbnail = entry.get("thumbnail")
	if thumbnail:
		description += f"<img src='{escape(thumbnail)}'>\n"
	description += entry.get("description") or ""
	item_info["description"] = description

	url = entry.get("webpage_url") or entry.get("url")
	if url:
		item_info["link"] = url
		item_info["guid"] = Guid(url)

	timestamp = entry.get("timestamp")
	if timestamp != None:
		item_info["pubDate"] = datetime.fromtimestamp(timestamp)

	return Item(**item_info)

def create_feed(url) -> Feed:
	playlist = ytdl.extract_info(url, download=False)

	if playlist.get("_type") != "playlist":
		raise NotAPlaylistException(f"URL {url} doesn't return a playlist.")

	feed_items = map(create_item, playlist["entries"])

	feed_info = {}
	feed_info["title"] = playlist.get("title")
	feed_info["link"] = playlist.get("webpage_url")

	# Generate description
	description = ""
	description += playlist.get("title")
	description += f" {playlist.get('uploader')}\n"

	feed_info["description"] = description
	feed_info["items"] = feed_items

	return Feed(**feed_info)
