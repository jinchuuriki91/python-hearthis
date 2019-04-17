# Python imports
import json
from requests import request


class Hearthis(object):

    def __init__(self, requests_timeout=None):
        self.base_url = "https://api-v2.hearthis.at"
        self.requests_timeout = None

    def _request(self, method, url, payload, **kwargs):
        # kwargs = dict(params=params)
        kwargs["timeout"] = self.requests_timeout
        if not url.startswith("http"):
            url = self.base_url + url

        headers = {
            "Content-Type": "application/json"
        }
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
        return self._request("GET", "/categories/", None)
