# Database

- Use a local SQLite database, accessed through Python's `sqlite3`.
- Persist subscriptions across restarts, with unique RSS feed URLs.
- Use parameterized queries and transactions for writes.
- Keep the database file out of version control.
- Store data in `data/podlite.db`, created on first use.

## Subscriptions

| Column | SQLite type | Constraints |
| --- | --- | --- |
| `id` | INTEGER | PRIMARY KEY |
| `feed_url` | TEXT | NOT NULL, UNIQUE |
| `title` | TEXT | NOT NULL |
| `cover_url` | TEXT | Nullable |
| `description` | TEXT | Nullable |

Missing covers and descriptions are stored as NULL.
