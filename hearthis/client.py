# Python imports
import json
from requests import request


class Hearthis(object):

    def __init__(self, requests_timeout=None):
        self.base_url = "https://api-v2.hearthis.at"
        self.default_page = 1
        self.default_count = 5
        self.requests_timeout = requests_timeout

    def _request(self, method, url, payload=None, params=None):
        kwargs = dict()
        kwargs["timeout"] = self.requests_timeout
        if not url.startswith("http"):
            url = self.base_url + url

        headers = {
            "Content-Type": "application/json"
        }

        if params:
            kwargs = dict(params=params)
        if payload:
            kwargs["data"] = json.dumps(payload)

        req = request(method, url, headers=headers, **kwargs)

        try:
            req.raise_for_status()
        except Exception as exc:
            raise exc
        finally:
            req.connection.close()

        return req.json()

    def all_genres(self):
        return self._request("GET", "/categories/")

    def genre_list(self, genre, page=None, count=None, duration=None):
        params = dict()
        params["page"] = page if page else self.default_page
        params["count"] = count if count else self.default_count
        if duration:
            params["duration"] = duration

        return self._request("GET", "/categories/%s/" % genre, payload=params)

    def single_artist(self, artist):
        return self._request("GET", "/%s/" % artist)
