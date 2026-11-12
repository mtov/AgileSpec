# Database

SQLite file: `data/podlite.db`, excluded from Git. Access is handled by
`podlite/storage.py` using `sqlite3`, parameterized queries, and write transactions.

## Schema

`podcasts` stores one row per subscription.

| Column | Type | Constraints / Default | Meaning |
| --- | --- | --- | --- |
| `id` | INTEGER | PRIMARY KEY | Locally generated subscription identifier. |
| `feed_url` | TEXT | NOT NULL, UNIQUE | RSS URL; prevents duplicate subscriptions. |
| `title` | TEXT | NOT NULL | Podcast title from the feed. |
| `image_url` | TEXT | Nullable; defaults to NULL | Podcast cover URL, not the image file. |
| `description` | TEXT | NOT NULL, DEFAULT `''` | Plain-text podcast description. |

There are no other tables or foreign keys. Episodes and their metadata remain in
session memory; audio and image files are not stored in SQLite.

The database is created automatically and updated while preserving existing subscriptions.
