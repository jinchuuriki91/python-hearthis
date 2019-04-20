# python-hearthis
Unofficial Python library for hearthis.io API https://hearthis.at/api-v2/
## Dependencies
- [Requests](https://github.com/kennethreitz/requests) - package required for making requests

## Installation
If you already have [Python](http://www.python.org/) on your system you can install the library simply by downloading the distribution, unpack it and install in the usual fashion:

```bash
python setup.py install
```

You can also install it using a popular package manager with

```bash
pip install python-hearthis
```

## Quick Start
```python
import hearthis

kwargs = {
    "email": "foo@bar.com",
    "password": "foobar"
}
heart = hearthis.Hearthis(**kwargs)
```

## Available APIs
- Feed
```python
# returns hearthis user feed
response = heart.feed()
```
|Parameter|Value|Default|Description|
|---|---|---|---|
|page|int|1|page to how|
|count|int|5|entries per page (max: 20)|
|duration|int|-|duration (+/- 5 minutes)|
|type|str|-|[empty] / popular / new|
|category|str|-|[empty] / house / drumandbass / etc. - see genre API|
|show_feed_start|str|2019-04-10|Start Date|
|show_feed_end|str|2019-04-17|End Date|

- All Genres
```python
response = heart.all_genres()
```

- Genre List
```python
response = heart.genre_list()
```
|Parameter|Value|Default|Description|
|---|---|---|---|
|genre|str|-|Genre from All Genres API|
|page|int|1|page to how|
|count|int|5|entries per page (max: 20)|
|duration|int|-|duration (+/- 5 minutes)|

- Single Artist
```python
response = heart.artist()
```

- Single Artist Follow/Unfollow
```python
response = heart.artist_follow_unfollow()
```
|Parameter|Value|Default|Description|
|---|---|---|---|
|artist_id|int|-|ID of artist|

- Artist List
```python
response = heart.artist_list()
```
|Parameter|Value|Default|Description|
|---|---|---|---|
|artist|str|1|Artist username|
|type|str|["tracks", "user", "playlists"]||
|page|int|1|page to how|
|count|int|5|entries per page (max: 20)|

- Track
```python
response = heart.track()
```
|Parameter|Value|Default|Description|
|---|---|---|---|
|track_uri|str|-|Track URI|

- Track Like/Unlike
```python
response = heart.track_like_unlike()
```
|Parameter|Value|Default|Description|
|---|---|---|---|
|track_id|int|-|ID of track|

- Add Playlist
```python
response = heart.add_playlist()
```
|Parameter|Value|Default|Description|
|---|---|---|---|
|name|str|-|Name of track|
|track_id|int|-|ID of track (optional)|

- Add Existing playlist track
```python
response = heart.add_playlist_track()
```
|Parameter|Value|Default|Description|
|---|---|---|---|
|playlist_id|int|-|ID of playlist|
|track_id|int|-|ID of track|

- Delete Track and Playlist
```python
response = heart.delete_playlist()
```
|Parameter|Value|Default|Description|
|---|---|---|---|
|playlist_id|int|-|ID of playlist|
|track_id|int|-|ID of track (optional)|