"""SQLite subscription storage."""

import sqlite3
from contextlib import closing
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "podlite.db"


def connect(db_path=None):
    path = Path(db_path) if db_path is not None else DEFAULT_DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    with connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS podcasts ("
            "id INTEGER PRIMARY KEY, feed_url TEXT NOT NULL UNIQUE, "
            "title TEXT NOT NULL, image_url TEXT, "
            "description TEXT NOT NULL DEFAULT '')"
        )
        columns = {row["name"] for row in connection.execute("PRAGMA table_info(podcasts)")}
        if "image_url" not in columns:
            connection.execute("ALTER TABLE podcasts ADD COLUMN image_url TEXT")
        if "description" not in columns:
            connection.execute(
                "ALTER TABLE podcasts ADD COLUMN description TEXT NOT NULL DEFAULT ''"
            )
    return connection


def list_podcasts(db_path=None):
    with closing(connect(db_path)) as connection:
        return [dict(row) for row in connection.execute("SELECT * FROM podcasts ORDER BY id")]


def has_subscription(feed_url, db_path=None):
    with closing(connect(db_path)) as connection:
        return connection.execute(
            "SELECT 1 FROM podcasts WHERE feed_url = ?", (feed_url,)
        ).fetchone() is not None


def get_podcast(podcast_id, db_path=None):
    with closing(connect(db_path)) as connection:
        row = connection.execute(
            "SELECT * FROM podcasts WHERE id = ?", (podcast_id,)
        ).fetchone()
        return dict(row) if row is not None else None


def save_subscription(feed_url, title, db_path=None, *, image_url=None, description=""):
    with closing(connect(db_path)) as connection, connection:
        connection.execute(
            "INSERT INTO podcasts (feed_url, title, image_url, description) VALUES (?, ?, ?, ?)",
            (feed_url, title, image_url, description),
        )
