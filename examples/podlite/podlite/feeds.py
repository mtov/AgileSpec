"""Fetch and parse podcast RSS feeds."""

import urllib.request
import xml.etree.ElementTree as ET
from datetime import UTC
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit


class DescriptionParser(HTMLParser):
    """Extract readable text without rendering feed HTML."""

    def __init__(self):
        super().__init__()
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.hidden += 1
        if tag in ("p", "div", "br", "li"):
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.hidden = max(0, self.hidden - 1)
        if tag in ("p", "div", "li"):
            self.parts.append(" ")

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def plain_text(element):
    if element is None:
        return ""
    markup = (element.text or "") + "".join(
        ET.tostring(child, encoding="unicode", method="html") for child in element
    )
    parser = DescriptionParser()
    parser.feed(markup)
    parser.close()
    return " ".join("".join(parser.parts).split())


def cover_url(element, feed_url):
    image = element.find("{http://www.itunes.com/dtds/podcast-1.0.dtd}image")
    candidates = [
        image.get("href", "") if image is not None else "",
        element.findtext("image/url", default=""),
    ]
    for candidate in candidates:
        if not candidate.strip():
            continue
        try:
            resolved = urljoin(feed_url, candidate.strip())
            parts = urlsplit(resolved)
            if parts.scheme in ("http", "https") and parts.hostname:
                return resolved
        except ValueError:
            continue
    return None


class FeedError(ValueError):
    """A feed could not be fetched or validated."""


def fetch_rss(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Podlite/0.1"})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            content = response.read()
    except (OSError, ValueError) as error:
        raise FeedError("Could not fetch the feed. Check the URL and try again.") from error

    try:
        root = ET.fromstring(content)
    except (ET.ParseError, LookupError) as error:
        raise FeedError("The feed contains invalid XML.") from error

    if root.tag != "rss" or root.get("version") != "2.0":
        raise FeedError("Enter a valid RSS 2.0 podcast feed.")
    title = root.findtext("channel/title", default="").strip()
    if not title:
        raise FeedError("The feed must include a podcast title.")
    return root


def fetch_podcast(url):
    root = fetch_rss(url)
    return {
        "title": root.findtext("channel/title").strip(),
        "image_url": cover_url(root.find("channel"), url),
        "description": plain_text(root.find("channel/description")),
    }


def publication_date(value):
    try:
        date = parsedate_to_datetime(value)
        if date.tzinfo is None:
            date = date.replace(tzinfo=UTC)
        return date.astimezone(UTC)
    except (ValueError, TypeError, OverflowError):
        return None


def fetch_episodes(url):
    root = fetch_rss(url)
    return [
        {
            "title": (item.findtext("title") or "").strip() or "Untitled episode",
            "description": plain_text(item.find("description")) or "No description available",
            "image_url": cover_url(item, url),
            "published_at": publication_date(item.findtext("pubDate", default="")),
        }
        for item in root.findall("channel/item")
    ]
