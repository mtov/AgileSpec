import sqlite3

import pytest

from podlite import database, feeds, service

URL = "https://example.com/rss"


def test_subscribe_trim_and_reload(monkeypatch):
    podcast = service.subscribe(f"  {URL}  ")
    assert podcast["title"] == "Sample Podcast"
    assert database.DB_PATH.is_file()
    # A new read uses a new connection and never retrieves the feed.
    monkeypatch.setattr(feeds, "fetch_podcast", lambda url: pytest.fail("Refetched feed"))
    saved = service.list_subscriptions()
    assert len(saved) == 1
    assert saved[0]["feed_url"] == URL
    assert saved[0]["description"] == "Hello listeners & friends."
    assert saved[0]["cover_url"] == "https://example.com/cover.png"


def test_duplicate_is_not_fetched_or_saved(monkeypatch):
    service.subscribe(URL)
    monkeypatch.setattr(feeds, "fetch_podcast", lambda url: pytest.fail("Refetched feed"))
    with pytest.raises(service.SubscriptionError, match="already subscribed"):
        service.subscribe(f" {URL} ")
    assert len(service.list_subscriptions()) == 1


@pytest.mark.parametrize("url", [
    "", "  ", "example.com/rss", "ftp://example.com/rss", "https://",
    "https://bad host/rss", "https://[broken", "https://example.com:bad/rss",
])
def test_invalid_urls(url):
    with pytest.raises(service.SubscriptionError, match="valid HTTP"):
        service.subscribe(url)
    assert service.list_subscriptions() == []


def test_bad_feed_is_not_saved(monkeypatch):
    def fail(url):
        raise feeds.FeedError("Invalid feed")
    monkeypatch.setattr(feeds, "fetch_podcast", fail)
    with pytest.raises(service.SubscriptionError, match="Invalid feed"):
        service.subscribe(URL)
    assert service.list_subscriptions() == []


@pytest.mark.parametrize("operation", ["list_subscriptions", "add_subscription"])
@pytest.mark.parametrize("error", [sqlite3.OperationalError("database error"), OSError("disk error")])
def test_database_failures(monkeypatch, operation, error):
    def fail(*args):
        raise error
    monkeypatch.setattr(database, operation, fail)
    with pytest.raises(service.SubscriptionError, match="Could not"):
        service.subscribe(URL)


def test_database_unique_constraint():
    podcast = service.subscribe(URL)
    with pytest.raises(sqlite3.IntegrityError):
        database.add_subscription(URL, podcast)
    assert len(service.list_subscriptions()) == 1


def test_missing_values_are_null_and_list_is_ordered(monkeypatch):
    monkeypatch.setattr(feeds, "fetch_podcast", lambda url: {
        "title": url, "cover_url": None, "description": None,
    })
    service.subscribe(URL)
    service.subscribe("http://example.com/other")
    rows = service.list_subscriptions()
    assert [row["feed_url"] for row in rows] == [URL, "http://example.com/other"]
    assert rows[0]["cover_url"] is None
    assert rows[0]["description"] is None


@pytest.mark.parametrize("url", [None, "", "file:///tmp/cover", "https://["])
def test_missing_or_invalid_cover(url):
    assert service.get_cover(url) is None


def test_unavailable_cover(monkeypatch):
    def fail(url):
        raise OSError("Unavailable")
    monkeypatch.setattr(feeds, "fetch_cover", fail)
    assert service.get_cover("https://example.com/missing") is None
