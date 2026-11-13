"""Subscription operations independent of the UI."""

import sqlite3
from datetime import UTC, datetime
from urllib.parse import urlsplit

from podlite import feeds, storage


class PodcastError(ValueError):
    """An operation failed with a user-facing explanation."""


def validate_url(value):
    url = value.strip()
    try:
        parts = urlsplit(url)
        valid = (
            parts.scheme in ("http", "https")
            and parts.hostname
            and (parts.port is None or parts.port > 0)
        )
    except ValueError:
        valid = False
    if not valid or any(character.isspace() or ord(character) < 32 for character in url):
        raise PodcastError("Enter a valid HTTP or HTTPS feed URL.")
    return url


def add_podcast(url, db_path=None):
    url = validate_url(url)
    try:
        if storage.has_subscription(url, db_path):
            raise PodcastError("This podcast is already subscribed.")
        podcast = feeds.fetch_podcast(url)
        storage.save_subscription(url, db_path=db_path, **podcast)
        return podcast["title"]
    except feeds.FeedError as error:
        raise PodcastError(str(error)) from error
    except sqlite3.IntegrityError as error:
        raise PodcastError("This podcast is already subscribed.") from error
    except (sqlite3.Error, OSError) as error:
        raise PodcastError("Could not save the subscription. Check database access.") from error


def list_podcasts(db_path=None):
    try:
        return storage.list_podcasts(db_path)
    except (sqlite3.Error, OSError) as error:
        raise PodcastError("Could not load subscriptions. Check database access.") from error


def list_episodes(podcast_id, db_path=None):
    try:
        podcast = storage.get_podcast(podcast_id, db_path)
    except (sqlite3.Error, OSError) as error:
        raise PodcastError("Could not load the subscription. Check database access.") from error
    if podcast is None:
        raise PodcastError("Podcast not found. Select a saved subscription.")
    try:
        episodes = feeds.fetch_episodes(podcast["feed_url"])
    except feeds.FeedError as error:
        raise PodcastError(str(error)) from error
    return sorted(
        episodes,
        key=lambda episode: (
            episode["published_at"] is not None,
            episode["published_at"] or datetime.min.replace(tzinfo=UTC),
        ),
        reverse=True,
    )
