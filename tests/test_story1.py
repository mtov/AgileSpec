import io
import sqlite3
import urllib.error
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from podlite import feeds, service, storage

APP = Path(__file__).resolve().parent.parent / "app.py"
URL = "https://example.com/feed.xml"
RSS = b'<rss version="2.0"><channel><title>Example Podcast</title></channel></rss>'


@pytest.fixture
def database(tmp_path):
    return tmp_path / "data" / "podlite.db"


@pytest.fixture
def http(monkeypatch):
    calls = []

    def fetch(request, timeout):
        calls.append((request.full_url, timeout))
        return io.BytesIO(RSS)

    monkeypatch.setattr(feeds.urllib.request, "urlopen", fetch)
    return calls


def test_add_persists_after_reopening(database, http):
    assert service.add_podcast(f"  {URL}  ", database) == "Example Podcast"
    assert http == [(URL, 10)]
    assert service.list_podcasts(database) == [
        {"id": 1, "feed_url": URL, "title": "Example Podcast",
         "image_url": None, "description": ""}
    ]
    with sqlite3.connect(database) as reopened:
        assert reopened.execute("SELECT title FROM podcasts").fetchone() == ("Example Podcast",)


@pytest.mark.parametrize("url", ["", "text", "ftp://example.com/feed", "https://", "https://[", "https://example.com:bad/feed", "https://exa mple.com", "https://example.com/\nfeed"])
def test_invalid_url_does_not_fetch_or_change_subscriptions(url, database, http):
    storage.save_subscription(URL, "Existing", database)
    before = service.list_podcasts(database)
    with pytest.raises(service.PodcastError, match="HTTP or HTTPS"):
        service.add_podcast(url, database)
    assert not http
    assert service.list_podcasts(database) == before


def test_duplicate_does_not_fetch_again(database, http):
    service.add_podcast(URL, database)
    with pytest.raises(service.PodcastError, match="already subscribed"):
        service.add_podcast(f" {URL} ", database)
    assert len(http) == 1
    assert len(service.list_podcasts(database)) == 1
    with pytest.raises(sqlite3.IntegrityError):
        storage.save_subscription(URL, "Duplicate", database)


@pytest.mark.parametrize("content", [b"not xml", b"<html/>", b'<rss version="1.0"><channel><title>Old</title></channel></rss>', b'<rss version="2.0"/>', b'<rss version="2.0"><channel><title> </title></channel></rss>'])
def test_invalid_feed_preserves_existing_subscriptions(content, database, monkeypatch):
    storage.save_subscription(URL, "Existing", database)
    before = service.list_podcasts(database)
    monkeypatch.setattr(feeds.urllib.request, "urlopen", lambda *a, **kw: io.BytesIO(content))
    with pytest.raises(service.PodcastError):
        service.add_podcast("https://example.com/invalid.xml", database)
    assert service.list_podcasts(database) == before


@pytest.mark.parametrize("failure", [urllib.error.URLError("offline"), urllib.error.HTTPError(URL, 404, "Not found", {}, None), TimeoutError("timeout")])
def test_fetch_failure_preserves_existing_subscriptions(failure, database, monkeypatch):
    storage.save_subscription(URL, "Existing", database)
    before = service.list_podcasts(database)

    def fail(*args, **kwargs):
        raise failure

    monkeypatch.setattr(feeds.urllib.request, "urlopen", fail)
    with pytest.raises(service.PodcastError, match="Could not fetch"):
        service.add_podcast("https://example.com/unreachable.xml", database)
    assert service.list_podcasts(database) == before


def test_parameterized_title(database):
    title = "Podcast'); DROP TABLE podcasts; --"
    storage.save_subscription(URL, title, database)
    assert service.list_podcasts(database)[0]["title"] == title


def test_database_failure_has_clear_message(tmp_path, http):
    blocked = tmp_path / "not-a-directory"
    blocked.write_text("file")
    with pytest.raises(service.PodcastError, match="Could not save"):
        service.add_podcast(URL, blocked / "podlite.db")
    with pytest.raises(service.PodcastError, match="Could not load"):
        service.list_podcasts(blocked / "podlite.db")


def test_ui_add_duplicate_and_reload(database, http, monkeypatch):
    monkeypatch.setattr(storage, "DEFAULT_DB_PATH", database)
    app = AppTest.from_file(APP).run()
    assert not app.exception
    assert "No podcasts" in app.info[0].value
    app.text_input[0].set_value(URL)
    app.button[0].click().run()
    assert not app.exception
    assert app.success[0].value == "Added: Example Podcast"
    assert any(item.value == "Example Podcast" for item in app.markdown)
    app.button[0].click().run()
    assert "already subscribed" in app.error[0].value
    restarted = AppTest.from_file(APP).run()
    assert not restarted.exception
    assert any(item.value == "Example Podcast" for item in restarted.markdown)


def test_ui_invalid_url(database, monkeypatch):
    monkeypatch.setattr(storage, "DEFAULT_DB_PATH", database)
    app = AppTest.from_file(APP).run()
    app.text_input[0].set_value("invalid")
    app.button[0].click().run()
    assert not app.exception
    assert "HTTP or HTTPS" in app.error[0].value
