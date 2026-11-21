"""Application actions called by the UI."""

import sqlite3
from http.client import HTTPException
from urllib.parse import urlsplit

from podlite import database, feeds


class SubscriptionError(ValueError):
    pass


def _validate_url(url):
    url = url.strip()
    try:
        parts = urlsplit(url)
        valid = parts.scheme in ("http", "https") and parts.hostname
        parts.port  # Also reject malformed port numbers.
        valid = valid and not any(character.isspace() for character in url)
    except ValueError:
        valid = False
    if not valid:
        raise SubscriptionError("Enter a valid HTTP or HTTPS RSS feed URL.")
    return url


def list_subscriptions():
    try:
        return database.list_subscriptions()
    except (sqlite3.Error, OSError) as exc:
        raise SubscriptionError("Could not load subscriptions.") from exc


def subscribe(url):
    url = _validate_url(url)
    if any(item["feed_url"] == url for item in list_subscriptions()):
        raise SubscriptionError("You are already subscribed to this podcast.")
    try:
        podcast = feeds.fetch_podcast(url)
        database.add_subscription(url, podcast)
    except feeds.FeedError as exc:
        raise SubscriptionError(str(exc)) from exc
    except sqlite3.IntegrityError as exc:
        raise SubscriptionError("You are already subscribed to this podcast.") from exc
    except (sqlite3.Error, OSError) as exc:
        raise SubscriptionError("Could not save the subscription.") from exc
    return podcast


def get_cover(url):
    if not url:
        return None
    try:
        return feeds.fetch_cover(url)
    except (OSError, ValueError, HTTPException):
        return None


def list_episodes(podcast_id):
    podcast = next((item for item in list_subscriptions()
                    if item["id"] == podcast_id), None)
    if podcast is None:
        raise SubscriptionError("Podcast subscription not found.")
    try:
        return feeds.fetch_episodes(podcast["feed_url"])
    except feeds.FeedError as exc:
        raise SubscriptionError(str(exc)) from exc
