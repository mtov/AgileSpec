import io
import sqlite3
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from podlite import feeds, service, storage

APP = Path(__file__).resolve().parent.parent / "app.py"
URL = "https://example.com/feed.xml"
IMAGE = "https://example.com/cover.jpg"


@pytest.fixture
def database(tmp_path, monkeypatch):
    path = tmp_path / "podlite.db"
    monkeypatch.setattr(storage, "DEFAULT_DB_PATH", path)
    return path


def mock_feed(monkeypatch, channel):
    xml = (
        '<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">'
        '<channel><title>Example Podcast</title>' + channel + '</channel></rss>'
    ).encode()
    monkeypatch.setattr(
        feeds.urllib.request, "urlopen", lambda *a, **kw: io.BytesIO(xml)
    )


@pytest.mark.parametrize(
    "images, expected",
    [
        ('<itunes:image href="https://example.com/itunes.jpg"/>'
         '<image><url>https://example.com/rss.jpg</url></image>',
         "https://example.com/itunes.jpg"),
        ('<image><url>https://example.com/rss.jpg</url></image>',
         "https://example.com/rss.jpg"),
        ('<itunes:image href=" "/><image><url>/cover.jpg</url></image>', IMAGE),
        ('<itunes:image href="file:///cover.jpg"/>', None),
        ('<itunes:image href="https://["/>', None),
        ("", None),
    ],
)
def test_cover_selection(images, expected, monkeypatch):
    mock_feed(monkeypatch, images)
    assert feeds.fetch_podcast(URL)["image_url"] == expected


@pytest.mark.parametrize(
    "description, expected",
    [
        ("<description> A simple description. </description>", "A simple description."),
        ("<description><![CDATA[<p>News &amp; ideas.</p><p>Every week.</p>]]></description>",
         "News & ideas. Every week."),
        ("<description><p>First</p><p>Second</p></description>", "First Second"),
        ("<description><![CDATA[<script>alert(1)</script><style>p{}</style>Safe]]></description>", "Safe"),
        ("<description><![CDATA[<p> </p>]]></description>", ""),
        ("", ""),
    ],
)
def test_plain_description(description, expected, monkeypatch):
    mock_feed(monkeypatch, description)
    assert feeds.fetch_podcast(URL)["description"] == expected


def test_metadata_persistence_and_ui(database, monkeypatch):
    mock_feed(
        monkeypatch,
        f'<itunes:image href="{IMAGE}"/>'
        '<description><![CDATA[<p>News &amp; ideas.</p>]]></description>',
    )
    app = AppTest.from_file(APP).run()
    app.text_input[0].set_value(URL)
    app.button[0].click().run()
    assert not app.exception
    assert app.success[0].value == "Added: Example Podcast"

    # A new app session reads metadata from disk without fetching the feed again.
    def offline(*args, **kwargs):
        raise AssertionError("Saved metadata should not need a feed request")

    monkeypatch.setattr(feeds.urllib.request, "urlopen", offline)
    restarted = AppTest.from_file(APP).run()
    assert not restarted.exception
    assert restarted.text[0].value == "News & ideas."
    assert restarted.get("image")[0].proto.imgs[0].url == IMAGE
    row = service.list_podcasts(database)[0]
    assert row["image_url"] == IMAGE
    assert row["description"] == "News & ideas."


def test_legacy_migration_and_fallback_ui(database):
    with sqlite3.connect(database) as connection:
        connection.execute(
            "CREATE TABLE podcasts (id INTEGER PRIMARY KEY, "
            "feed_url TEXT NOT NULL UNIQUE, title TEXT NOT NULL)"
        )
        connection.execute(
            "INSERT INTO podcasts (id, feed_url, title) VALUES (?, ?, ?)",
            (7, URL, "Existing Podcast"),
        )
    assert service.list_podcasts(database) == [
        {"id": 7, "feed_url": URL, "title": "Existing Podcast",
         "image_url": None, "description": ""}
    ]
    # Repeated initialization preserves the row and its uniqueness constraint.
    app = AppTest.from_file(APP).run()
    assert not app.exception
    assert app.text[0].value == "No description available"
    assert len(app.get("image")) == 1
    assert "svg" in app.get("image")[0].proto.imgs[0].url
    assert any(item.value == "Existing Podcast" for item in app.markdown)
    with pytest.raises(service.PodcastError, match="already subscribed"):
        service.add_podcast(URL, database)
    storage.save_subscription(
        "https://example.com/new.xml", "New", database,
        image_url=IMAGE, description="New description",
    )
    assert service.list_podcasts(database)[1]["description"] == "New description"
