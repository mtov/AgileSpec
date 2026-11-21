from io import BytesIO
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from podlite import database, feeds, service

URL = "https://example.com/rss"
AUDIO = "https://example.com/episode.mp3"
APP = Path(__file__).resolve().parent.parent / "app.py"


def episode_feed(monkeypatch, enclosures):
    xml = ("<rss><channel><item><title>Episode</title>" + enclosures
           + "</item></channel></rss>").encode()
    requested = []

    def open_request(request, timeout):
        requested.append(request.full_url)
        assert request.full_url == URL, "The server must not download audio."
        return BytesIO(xml)

    monkeypatch.setattr(feeds, "urlopen", open_request)
    return requested


@pytest.mark.parametrize("mime_type", ["audio/mpeg", "audio/ogg", "audio/mp4", ""])
def test_audio_metadata_reaches_service(monkeypatch, mime_type):
    service.subscribe(URL)
    podcast = service.list_subscriptions()[0]
    requested = episode_feed(
        monkeypatch, f'<enclosure url="{AUDIO}" type="{mime_type}"/>')
    episode = service.list_episodes(podcast["id"])[0]
    assert episode["audio_url"] == AUDIO
    assert episode["audio_type"] == (mime_type or None)
    assert requested == [URL]
    with database._connect() as connection:
        tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    assert [row[0] for row in tables] == ["subscriptions"]


@pytest.mark.parametrize("enclosures", [
    "", '<enclosure/>',
    '<enclosure url="ftp://example.com/episode.mp3" type="audio/mpeg"/>',
    '<enclosure url="javascript:alert(1)" type="audio/mpeg"/>',
    '<enclosure url="https:///episode.mp3" type="audio/mpeg"/>',
    '<enclosure url="https://example.com:bad/episode.mp3" type="audio/mpeg"/>',
    '<enclosure url="https://[broken/episode.mp3" type="audio/mpeg"/>',
    '<enclosure url="https://example.com/episode one.mp3" type="audio/mpeg"/>',
    '<enclosure url="https://example.com/video.mp4" type="video/mp4"/>',
])
def test_missing_or_invalid_audio(monkeypatch, enclosures):
    episode_feed(monkeypatch, enclosures)
    episode = feeds.fetch_episodes(URL)[0]
    assert episode["audio_url"] is None
    assert episode["audio_type"] is None
    assert episode["title"] == "Episode"


def test_audio_enclosure_selection(monkeypatch):
    episode_feed(monkeypatch,
                 '<enclosure url="https://example.com/cover.png" type="image/png"/>'
                 '<enclosure url="invalid" type="audio/mpeg"/>'
                 f'<enclosure url="  {AUDIO}  " type=" AUDIO/MPEG "/>'
                 '<enclosure url="https://example.com/second.mp3" type="audio/mpeg"/>')
    episode = feeds.fetch_episodes(URL)[0]
    assert episode["audio_url"] == AUDIO
    assert episode["audio_type"] == "audio/mpeg"


@pytest.mark.parametrize("audio_url", [
    AUDIO, "https://example.com/missing.mp3", "https://example.com/unsupported.audio",
])
def test_player_uses_remote_audio_without_autoplay(monkeypatch, audio_url):
    service.subscribe(URL)
    requested = episode_feed(monkeypatch,
                             f'<enclosure url="{audio_url}" type="audio/mpeg"/>')
    app = AppTest.from_file(str(APP)).run()
    app.button(key="episodes_1").click().run()
    assert not app.exception
    players = app.get("audio")
    assert len(players) == 1
    assert players[0].proto.url == audio_url
    assert not players[0].proto.autoplay
    assert audio_url not in requested
    app.button[0].click().run()
    assert app.header[0].value == "My Podcasts"


@pytest.mark.parametrize("missing_audio", [
    "", '<enclosure url="invalid" type="audio/mpeg"/>',
])
def test_unavailable_audio_does_not_hide_other_episodes(monkeypatch, missing_audio):
    service.subscribe(URL)
    xml = (f'<rss><channel><item><title>Missing</title>{missing_audio}</item>'
           f'<item><title>Playable</title><enclosure url="{AUDIO}" '
           'type="audio/mpeg"/></item></channel></rss>').encode()
    monkeypatch.setattr(feeds, "urlopen", lambda *a, **k: BytesIO(xml))
    app = AppTest.from_file(str(APP)).run()
    app.button(key="episodes_1").click().run()
    assert not app.exception
    assert [item.value for item in app.subheader] == ["Missing", "Playable"]
    assert any(item.value == "Audio unavailable" for item in app.caption)
    assert len(app.get("audio")) == 1
