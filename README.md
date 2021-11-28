# youtube-dl RSS

An RSS feed generator for the playlists of the web powered by
[the titular command-line tool](https://ytdl-org.github.io/youtube-dl/).

## Install
```bash
poetry install
# For the lazy...
python3 main.py
# For the more upstanding
gunicorn 'ytdl_rss:create_app()'
```
