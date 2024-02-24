from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode, urlparse, parse_qs
from requests import get, post
from base64 import b64encode
from time import time
from json import loads, dumps
import webbrowser
import logging

from src.utils import fetch_content_path


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/callback"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            res = parse_qs(urlparse(self.path).query)
            if res.get('error') is not None:
                logging.error(SpotifyAPI.LOGGING_PREFIX + " An error has occurred while connecting to your spotify account")
                exit(1)

            self.server.code = res['code'][0]
            self._write("<html><body><h1>You can close this window</h1></body></html>")
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            self.server.error = "Invalid route used"
            self._write("<html><body><h1>Invalid route used</h1></body></html>")

    def _write(self, text):
        return self.wfile.write(text.encode("utf-8"))


class SpotifyAPI:
    LOGGING_PREFIX = "[SPOTIFY]"
    SPOTIFY_API_URL = "https://accounts.spotify.com"

    def __init__(self, client_id, client_secret, redirect_uri, server_port):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.port = int(server_port)

        self.refresh_token = ""
        self.token = ""
        self.expires = -1

    def fetch_token(self):
        url = self.SPOTIFY_API_URL + "/authorize?"
        url += urlencode({
            "scope": "user-read-playback-state user-read-currently-playing",
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri
        })

        if not self.load_token():
            server = self.start_server()
            webbrowser.open(url)
            server.handle_request()

            if server.code:
                self.retrieve_token(server.code)
            elif server.error:
                raise Exception(server.error)

    def load_token(self):
        try:
            with open(fetch_content_path("credentials.json"), "r") as f:
                data = loads(f.readline())

                if not data.get('refresh_token'):
                    logging.warning(self.LOGGING_PREFIX + " Cannot find refresh token...")
                    return False

                if not data.get('token'):
                    logging.warning(self.LOGGING_PREFIX + " Cannot find token...")
                    return False

                self.refresh_token = data['refresh_token']
                self.token = data['token']
                self.expires = data['expires']
                logging.info(self.LOGGING_PREFIX + " Use Spotify token from file")
                return True
        except OSError:
            logging.warning(self.LOGGING_PREFIX + " Could not use file to fetch Spotify token...")
        return False

    def save_token(self):
        try:
            with open(fetch_content_path("credentials.json"), "w") as outfile:
                outfile.write(dumps({
                    "refresh_token": self.refresh_token,
                    "token": self.token,
                    "expires": self.expires
                }, separators=(',', ':')))

                logging.info(self.LOGGING_PREFIX + " Spotify token saved")
                self.update_token_if_expired()
        except OSError:
            logging.warning(self.LOGGING_PREFIX + " Could not write Spotify token in a file...")

    def retrieve_token(self, code=None, refresh=False):
        if refresh:
            data = urlencode({
                "client_id": self.client_id,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token
            })
        else:
            data = urlencode({
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
            })

        headers = {
            "Authorization": f"Basic {b64encode((self.client_id + ':' + self.client_secret).encode()).decode()}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "Close"
        }

        req = post(
            'https://accounts.spotify.com/api/token',
            headers=headers,
            data=data
        )

        data = req.json()

        if data.get('refresh_token'):
            self.refresh_token = data['refresh_token']
        self.token = data['access_token']
        self.expires = (time() + data["expires_in"]) * 1000
        self.save_token()

    def update_token_if_expired(self):
        if self.expires <= int(time() * 1000):
            self.retrieve_token(refresh=True)

    def fetch_song(self):
        if self.token == "":
            return None

        self.update_token_if_expired()

        req = get(
            'https://api.spotify.com/v1/me/player/currently-playing',
            headers={
                "Authorization": "Bearer " + self.token,
                "Connection": "Close"
            }
        )

        if req.status_code == 429:
            logging.warning(self.LOGGING_PREFIX + " Rate limit exceeded! Please adjust the Spotify fetch delay")
            return None

        if req.status_code == 204:
            return None

        data = req.json()
        return {
            "progress": data["progress_ms"],
            "latency": int(req.elapsed.microseconds / 1000),
            "duration": data["item"]["duration_ms"],
            "artist": data["item"]["artists"][0]["name"],
            "paused": not data["is_playing"],
            "title": data["item"]["name"]
        }

    def start_server(self, handler=RequestHandler):
        server = HTTPServer(("localhost", self.port), handler)
        server.allow_reuse_address = True
        server.code = None
        server.error = None
        return server
