# Story 1: Tables

Create `subscriptions` if it does not exist.

| Column | SQLite type | Constraints |
| --- | --- | --- |
| `id` | INTEGER | PRIMARY KEY |
| `feed_url` | TEXT | NOT NULL, UNIQUE |
| `title` | TEXT | NOT NULL |
| `cover_url` | TEXT | Nullable |
| `description` | TEXT | Nullable |

SQLite assigns IDs. Store trimmed feed URLs and use NULL for missing
covers or descriptions. Do not store UI fallbacks.
