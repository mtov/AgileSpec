"""RSS and cover retrieval using the Python standard library."""

import html
from email.utils import parsedate_to_datetime
from http.client import HTTPException
from html.parser import HTMLParser
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from xml.etree import ElementTree

ITUNES = "http://www.itunes.com/dtds/podcast-1.0.dtd"


class FeedError(ValueError):
    pass


class _PlainText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.hidden += 1
        elif not self.hidden and tag in ("p", "br", "div", "li"):
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.hidden = max(0, self.hidden - 1)
        elif not self.hidden and tag in ("p", "div", "li"):
            self.parts.append(" ")

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def plain_text(value):
    parser = _PlainText()
    parser.feed(value)
    parser.close()
    return " ".join(html.unescape("".join(parser.parts)).split())


def _download(url):
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise ValueError("An HTTP or HTTPS URL is required.")
    request = Request(url, headers={"User-Agent": "PodLite/1.0"})
    with urlopen(request, timeout=10) as response:
        return response.read()


def _read_channel(url):
    try:
        data = _download(url)
    except (OSError, ValueError, HTTPException) as exc:
        raise FeedError("Could not retrieve the RSS feed.") from exc
    try:
        root = ElementTree.fromstring(data)
    except (ElementTree.ParseError, LookupError, ValueError) as exc:
        raise FeedError("The URL does not contain a valid RSS feed.") from exc
    channel = root.find("channel") if root.tag == "rss" else None
    if channel is None:
        raise FeedError("The URL does not contain a valid RSS feed.")
    return channel


def fetch_podcast(url):
    channel = _read_channel(url)
    title = plain_text(channel.findtext("title", ""))
    if not title:
        raise FeedError("The RSS feed has no podcast title.")
    image = channel.find(f"{{{ITUNES}}}image")
    cover = image.get("href", "").strip() if image is not None else ""
    if not cover:
        cover = channel.findtext("image/url", "").strip()
    return {
        "title": title,
        "cover_url": cover or None,
        "description": plain_text(channel.findtext("description", "")) or None,
    }


def fetch_cover(url):
    return _download(url)


def _audio_metadata(item):
    for enclosure in item.findall("enclosure"):
        url = enclosure.get("url", "").strip()
        mime_type = enclosure.get("type", "").strip().lower()
        if mime_type and not mime_type.startswith("audio/"):
            continue
        try:
            parts = urlsplit(url)
            valid = parts.scheme in ("http", "https") and parts.hostname
            parts.port
            valid = valid and not any(character.isspace() for character in url)
        except ValueError:
            valid = False
        if valid:
            return url, mime_type or None
    return None, None


def fetch_episodes(url):
    channel = _read_channel(url)
    episodes = []
    for item in channel.findall("item")[:20]:
        image = item.find(f"{{{ITUNES}}}image")
        cover = image.get("href", "").strip() if image is not None else ""
        description = item.findtext("description", "")
        if not description.strip():
            description = item.findtext(
                "{http://purl.org/rss/1.0/modules/content/}encoded", ""
            )
        try:
            date = parsedate_to_datetime(item.findtext("pubDate", "")).date().isoformat()
        except (ValueError, TypeError, OverflowError):
            date = None
        audio_url, audio_type = _audio_metadata(item)
        episodes.append({
            "title": plain_text(item.findtext("title", "")) or "Untitled episode",
            "description": plain_text(description) or None,
            "cover_url": cover or None,
            "date": date,
            "audio_url": audio_url,
            "audio_type": audio_type,
        })
    return episodes
