"""Local subscription storage."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "podlite.db"


def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY,
                feed_url TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                cover_url TEXT,
                description TEXT
            )
        """)
    except sqlite3.Error:
        connection.close()
        raise
    return connection


def add_subscription(feed_url, podcast):
    connection = _connect()
    try:
        with connection:
            connection.execute(
                """INSERT INTO subscriptions
                   (feed_url, title, cover_url, description)
                   VALUES (?, ?, ?, ?)""",
                (feed_url, podcast["title"], podcast["cover_url"],
                 podcast["description"]),
            )
    finally:
        connection.close()


def list_subscriptions():
    connection = _connect()
    try:
        return [dict(row) for row in connection.execute(
            "SELECT * FROM subscriptions ORDER BY id"
        )]
    finally:
        connection.close()
