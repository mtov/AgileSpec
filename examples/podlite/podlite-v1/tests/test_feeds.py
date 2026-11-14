from io import BytesIO
from urllib.error import URLError

import pytest

from podlite import feeds


def use_xml(monkeypatch, xml):
    monkeypatch.setattr(feeds, "urlopen", lambda *a, **k: BytesIO(xml))


def test_metadata():
    assert feeds.fetch_podcast("https://example.com/rss") == {
        "title": "Sample Podcast",
        "cover_url": "https://example.com/cover.png",
        "description": "Hello listeners & friends.",
    }


def test_rss_cover_and_blank_description(monkeypatch):
    use_xml(monkeypatch, b"""<rss><channel><title>Test</title>
        <description>   </description>
        <image><url>https://example.com/rss.png</url></image>
        </channel></rss>""")
    podcast = feeds.fetch_podcast("http://example.com/rss")
    assert podcast["cover_url"] == "https://example.com/rss.png"
    assert podcast["description"] is None


def test_missing_optional_metadata(monkeypatch):
    use_xml(monkeypatch, b"<rss><channel><title>Test</title></channel></rss>")
    assert feeds.fetch_podcast("https://example.com/rss") == {
        "title": "Test", "description": None, "cover_url": None,
    }


def test_itunes_cover_takes_priority(monkeypatch):
    use_xml(monkeypatch, b"""<rss xmlns:itunes=
        "http://www.itunes.com/dtds/podcast-1.0.dtd"><channel>
        <title>Test</title><itunes:image href="https://example.com/itunes"/>
        <image><url>https://example.com/rss</url></image></channel></rss>""")
    assert feeds.fetch_podcast("https://example.com/rss")["cover_url"].endswith("itunes")


@pytest.mark.parametrize("xml", [
    b"not xml", b"<rss>", b"<html/>", b"<rss/>",
    b'<?xml version="1.0" encoding="unknown"?><rss/>',
    b"<rss><channel/></rss>",
    b"<rss><channel><title>  </title></channel></rss>",
])
def test_invalid_feed_or_missing_title(monkeypatch, xml):
    use_xml(monkeypatch, xml)
    with pytest.raises(feeds.FeedError):
        feeds.fetch_podcast("https://example.com/rss")


@pytest.mark.parametrize("error", [URLError("offline"), TimeoutError("timeout")])
def test_request_failure(monkeypatch, error):
    def fail(*args, **kwargs):
        raise error
    monkeypatch.setattr(feeds, "urlopen", fail)
    with pytest.raises(feeds.FeedError, match="retrieve"):
        feeds.fetch_podcast("https://example.com/rss")


def test_plain_text():
    assert feeds.plain_text(
        "<p>One &amp; two</p><p>Three</p><script>hidden()</script>"
    ) == "One & two Three"
