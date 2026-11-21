from http.client import IncompleteRead
from io import BytesIO
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from podlite import database, feeds, service

URL = "https://example.com/rss"
APP = Path(__file__).resolve().parent.parent / "app.py"


def xml_response(monkeypatch, items):
    xml = ("<rss xmlns:itunes=\"http://www.itunes.com/dtds/podcast-1.0.dtd\" "
           "xmlns:content=\"http://purl.org/rss/1.0/modules/content/\">"
           "<channel><title>Podcast</title>" + items + "</channel></rss>").encode()
    monkeypatch.setattr(feeds, "urlopen", lambda *args, **kwargs: BytesIO(xml))


def test_episode_metadata(monkeypatch):
    xml_response(monkeypatch, """<item><title>First</title>
        <description><![CDATA[<p>A &amp; B</p>]]></description>
        <pubDate>Tue, 10 Nov 2026 12:00:00 GMT</pubDate>
        <itunes:image href="https://example.com/episode.png"/></item>""")
    assert feeds.fetch_episodes(URL) == [{
        "title": "First", "description": "A & B", "date": "2026-11-10",
        "cover_url": "https://example.com/episode.png",
        "audio_url": None, "audio_type": None,
    }]


def test_limit_preserves_feed_order(monkeypatch):
    titles = list(range(25, 0, -1))
    xml_response(monkeypatch, ''.join(f'<item><title>{i}</title></item>' for i in titles))
    episodes = feeds.fetch_episodes(URL)
    assert len(episodes) == 20
    assert [episode["title"] for episode in episodes] == [str(i) for i in titles[:20]]


@pytest.mark.parametrize("date", ["", "not a date", "Tue, 99 Nov 2026 00:00:00 GMT"])
def test_missing_metadata_and_invalid_dates(monkeypatch, date):
    xml_response(monkeypatch, f'<item><title> </title><pubDate>{date}</pubDate></item>')
    assert feeds.fetch_episodes(URL) == [{
        "title": "Untitled episode", "description": None,
        "date": None, "cover_url": None,
        "audio_url": None, "audio_type": None,
    }]


def test_encoded_description(monkeypatch):
    xml_response(monkeypatch, '<item><description> </description>'
                 '<content:encoded><![CDATA[<b>Full text</b>]]></content:encoded></item>')
    assert feeds.fetch_episodes(URL)[0]["description"] == "Full text"


def test_empty_feed(monkeypatch):
    xml_response(monkeypatch, "")
    assert feeds.fetch_episodes(URL) == []


def test_unknown_subscription_does_not_fetch(monkeypatch):
    monkeypatch.setattr(feeds, "fetch_episodes", lambda url: pytest.fail("Unknown feed fetched"))
    with pytest.raises(service.SubscriptionError, match="not found"):
        service.list_episodes(999)


def test_feed_error_keeps_subscription(monkeypatch):
    service.subscribe(URL)
    before = service.list_subscriptions()
    monkeypatch.setattr(feeds, "urlopen", lambda *args, **kwargs: BytesIO(b'not rss'))
    with pytest.raises(service.SubscriptionError, match="valid RSS"):
        service.list_episodes(before[0]["id"])
    assert service.list_subscriptions() == before


def test_episodes_are_not_stored(monkeypatch):
    service.subscribe(URL)
    podcast = service.list_subscriptions()[0]
    xml_response(monkeypatch, '<item><title>One</title></item>')
    assert service.list_episodes(podcast["id"])[0]["title"] == "One"
    xml_response(monkeypatch, '<item><title>Two</title></item>')
    assert service.list_episodes(podcast["id"])[0]["title"] == "Two"
    with database._connect() as connection:
        tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    assert [row[0] for row in tables] == ["subscriptions"]


def open_episodes(monkeypatch, items):
    service.subscribe(URL)
    xml_response(monkeypatch, items)
    app = AppTest.from_file(str(APP)).run()
    app.button(key="episodes_1").click().run()
    assert not app.exception
    return app


def test_navigation_and_metadata_fallbacks(monkeypatch):
    app = open_episodes(monkeypatch, '<item/>')
    assert app.header[0].value == "Sample Podcast"
    assert app.subheader[0].value == "Untitled episode"
    assert app.text[0].value == "No description available"
    assert any(caption.value == "Date unavailable" for caption in app.caption)
    assert not app.text_input
    app.button[0].click().run()
    assert not app.exception
    assert app.header[0].value == "My Podcasts"
    assert len(service.list_subscriptions()) == 1


def test_empty_page(monkeypatch):
    app = open_episodes(monkeypatch, "")
    assert app.info[0].value == "No episodes available"


def test_error_retry_and_return(monkeypatch):
    app = open_episodes(monkeypatch, '<item/>')
    monkeypatch.setattr(feeds, "urlopen", lambda *a, **k: BytesIO(b'broken'))
    app.button[1].click().run()
    assert not app.exception
    assert "valid RSS" in app.error[0].value
    assert not app.info
    xml_response(monkeypatch, '<item><title>Recovered</title></item>')
    app.button[1].click().run()
    assert not app.exception
    assert not app.error
    assert app.subheader[0].value == "Recovered"
    app.button[0].click().run()
    assert app.header[0].value == "My Podcasts"


@pytest.mark.parametrize("operation", ["fetch_episodes", "fetch_podcast"])
def test_interrupted_response(monkeypatch, operation):
    def fail(*args, **kwargs):
        raise IncompleteRead(b'<rss>', 100)
    monkeypatch.setattr(feeds, "urlopen", fail)
    with pytest.raises(feeds.FeedError, match="retrieve"):
        getattr(feeds, operation)(URL)


def test_unavailable_episode_cover_uses_podcast_cover(monkeypatch):
    import streamlit as st
    st.cache_data.clear()
    service.subscribe(URL)
    xml_response(monkeypatch, '<item><itunes:image href="https://example.com/missing.png"/></item>')
    requested = []
    def cover(url):
        requested.append(url)
        # Valid 1x1 PNG from the existing offline fixture.
        from conftest import PNG
        return PNG if url == "https://example.com/cover.png" else None
    monkeypatch.setattr(service, "get_cover", cover)
    app = AppTest.from_file(str(APP)).run()
    app.button(key="episodes_1").click().run()
    assert not app.exception
    assert "https://example.com/missing.png" in requested
    assert not app.get("image")[0].proto.imgs[0].url.startswith("data:image/svg")
