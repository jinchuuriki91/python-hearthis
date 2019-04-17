# python-hearthis
Unofficial Python client for hearthis.io API https://hearthis.at/api-v2/
## Dependencies
- [Requests](https://github.com/kennethreitz/requests) - package required for making requests

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
# returns list of all genres
response = heart.all_genres()
```
