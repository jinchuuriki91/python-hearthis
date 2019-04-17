# Python imports
import json
from requests import Session


class Hearthis(object):

    SEARCH_TYPE = ["tracks", "user", "playlists"]

    def __init__(self, email=None, password=None, requests_timeout=None, requests_session=None):
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

        print(req.request.url)
        print(req.request.body)
        return req.json()

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

    def single_artist(self, artist):
        return self._request("GET", "/%s/" % artist)
