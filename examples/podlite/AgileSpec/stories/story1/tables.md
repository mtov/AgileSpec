# Story 1 — Tables

## podcasts

Create one row per subscription in `data/podlite.db`.

| Column | Definition |
| --- | --- |
| `id` | INTEGER PRIMARY KEY |
| `feed_url` | TEXT NOT NULL UNIQUE |
| `title` | TEXT NOT NULL |
| `image_url` | TEXT, nullable |
| `description` | TEXT NOT NULL DEFAULT `''` |

No relationships or foreign keys are required by this story. For older databases,
add missing `image_url` and `description` columns without losing subscriptions.
Existing rows receive NULL and an empty description; migration does not refetch feeds.
