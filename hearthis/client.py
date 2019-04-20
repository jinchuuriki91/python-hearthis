# Python imports
from requests import Session
from json import JSONDecodeError


class Hearthis(object):

    SEARCH_TYPE = ["tracks", "user", "playlists"]
    FEED_TYPE = ["popular", "new"]
    ARTIST_LIST_TYPE = ["likes", "playlists", "tracks"]

    def __init__(
            self, email=None, password=None, requests_timeout=None,
            requests_session=None):

        self.base_url = "https://api-v2.hearthis.at"
        self.is_logged_in = False
        self.default_page = 1
        self.default_count = 5
        self.default_duration = 5  # 5 minutes
        self.requests_timeout = requests_timeout
        self._user_meta = dict()

        if isinstance(requests_session, Session):
            self._session = requests_session
        else:
            self._session = Session()

        if email and password:
            self.login(email, password)
            self.is_logged_in = True

    def _request(self, method, url, payload=None, params=None):
        kwargs = dict()
        kwargs["timeout"] = self.requests_timeout
        if not url.startswith("http"):
            url = self.base_url + url

        if params:
            kwargs["params"] = params
        if payload:
            kwargs["data"] = payload
        req = self._session.request(method, url, **kwargs)

        try:
            req.raise_for_status()
        except Exception as exc:
            raise exc
        finally:
            req.connection.close()

        try:
            return req.json()
        except JSONDecodeError:
            return req.content

    def login(self, email, password):
        payload = {
            "email": email,
            "password": password
        }
        resp = self._request("POST", "/login/", payload=payload)
        if "success" in resp:
            raise Exception(resp["message"])
        self._user_meta = resp
        return resp

    def logout(self):
        return self._request("GET", "/logout/")

    def feed(
            self, page=None, count=None, duration=None, type="", category="",
            show_feed_start="", show_feed_end=""):
        params = {
            "page": page if page else self.default_page,
            "count": count if count else self.default_count,
            "duration": duration if duration else self.default_duration,
            "type": type,
            "category": category,
            "show-feed-start": show_feed_start,
            "show-feed-end": show_feed_end
        }
        return self._request("GET", "/feed/", params=params)

    def search(
            self, query, type="tracks", page=None, count=None, duration=None):

        if type not in self.SEARCH_TYPE:
            raise Exception("Invalid search type")
        params = {
            "t": query,
            "type": type,
            "page": page if page else self.default_page,
            "count": count if count else self.default_count,
            "duration": duration if duration else self.default_duration
        }
        return self._request("GET", "/search", params=params)

    def user_history(self, page=None, count=None):
        if not self.is_logged_in:
            raise Exception("Log in required")

        params = {
            "page": page if page else self.default_page,
            "count": count if count else self.default_count
        }
        return self._request("GET", "/v2.2/htry/", params=params)

    def all_genres(self):
        return self._request("GET", "/categories/")

    def genre_list(self, genre, page=None, count=None, duration=None):
        params = {
            "page": page if page else self.default_page,
            "count": count if count else self.default_count,
            "duration": duration if duration else self.default_duration
        }
        return self._request("GET", "/categories/%s/" % genre, params=params)

    def artist(self, artist):
        return self._request("GET", "/%s/" % artist)

    def artist_follow_unfollow(self, artist_id):
        payload = {
            "action": "follow",
            "userid": artist_id
        }
        return self._request(
            "POST", "/user_ajax_function.php", payload=payload)

    def artist_list(self, artist, type="tracks", page=None, count=None):

        if type not in self.ARTIST_LIST_TYPE:
            raise Exception("Invalid list type")

        params = {
            "type": type,
            "page": page if page else self.default_page,
            "count": count if count else self.default_count
        }
        return self._request("GET", "/%s/" % artist, params=params)

    def track(self, track_uri):
        return self._request("GET", track_uri)

    def track_like_unlike(self, track_id):
        params = {
            "action": "likes",
            "trackid": track_id
        }
        return self._request(
            "GET", "/trackimgcnt.php", params=params)

    def add_playlist(self, name, track_id=None):
        payload = {
            "action": "add",
            "new_set": name
        }
        if track_id:
            payload["track_id"] = track_id
        return self._request("POST", "/set_ajax_add.php", payload=payload)

    def add_playlist_track(self, playlist_id, track_id):
        payload = {
            "action": "add",
            "id": track_id,
            "setid": playlist_id
        }
        return self._request("POST", "/set_ajax_add.php", payload=payload)

    def sort_playlist(self, playlist_id, track_id_arr):
        payload = {
            "action": "sort",
            "track_light__move": track_id_arr,
            "set_id": playlist_id
        }
        return self._request("POST", "/set_ajax_edit.php", payload=payload)

    def delete_playlist(self, playlist_id, track_id=None):
        if track_id:
            payload = {
                "action": "deleteentry",
                "id": track_id,
                "set_id": playlist_id
            }
        else:
            payload = {
                "action": "delete",
                "set": playlist_id
            }
        return self._request("POST", "/set_ajax_edit.php", payload=payload)
