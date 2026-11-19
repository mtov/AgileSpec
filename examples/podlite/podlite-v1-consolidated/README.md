# PodLite v1 — Consolidation

[PodLite](../README.md) | [AgileSpec](../../../README.md)

Project specs updated from the approved story 1 implementation.
Consolidation approved; story 1 is complete in the backlog.

As a listener, I want to subscribe using an RSS URL and keep the podcast
in my list.

## Project Specs

Architecture, UI, and database documentation reflect the implementation.
Story 1 is complete; the remaining stories are planned:

- [backlog.md](AgileSpec/project/backlog.md)
- [architecture.md](AgileSpec/project/architecture.md)
- [ui.md](AgileSpec/project/ui.md)
- [database.md](AgileSpec/project/database.md)
- [definition-of-done.md](AgileSpec/project/definition-of-done.md)

## User Story Specs

- [acceptance.md](AgileSpec/stories/story1/acceptance.md)
- [design.md](AgileSpec/stories/story1/design.md)
- [views.md](AgileSpec/stories/story1/views.md)
- [tables.md](AgileSpec/stories/story1/tables.md)

## What Was Consolidated?

Changes relative to `podlite-v1`: `-` removed, `+` added.

### architecture.md

Identified the modules responsible for the interface, application logic,
RSS feeds, and persistence. This connects the architectural structure to
the source code and clarifies where each responsibility is implemented.

```diff
--- podlite-v1/architecture.md
+++ podlite-v1-consolidated/architecture.md
@@ -16,3 +16,4 @@
-- UI: renders screens and handles user input.
-- Services: handle application logic and RSS feeds.
-- Persistence: reads and writes local data.
+- `app.py`: Streamlit interface.
+- `podlite/service.py`: application logic.
+- `podlite/feeds.py`: RSS and podcast metadata.
+- `podlite/database.py`: SQLite persistence.
```

### ui.md

Added the home screen structure and metadata fallbacks. Podcast cards
show the cover, title, and plain-text description.

```diff
--- podlite-v1/ui.md
+++ podlite-v1-consolidated/ui.md
@@ -5,0 +6,6 @@
+- Use fallbacks for missing covers and descriptions.
+
+## Home
+
+A subscription form followed by podcast cards with cover, title, and
+plain-text description.
```

### database.md

Documented the database location and the structure of the
`subscriptions` table. Missing covers and descriptions are stored as NULL.

```diff
--- podlite-v1/database.md
+++ podlite-v1-consolidated/database.md
@@ -5,0 +6,13 @@
+- Store data in `data/podlite.db`, created on first use.
+
+## Subscriptions
+
+| Column | SQLite type | Constraints |
+| --- | --- | --- |
+| `id` | INTEGER | PRIMARY KEY |
+| `feed_url` | TEXT | NOT NULL, UNIQUE |
+| `title` | TEXT | NOT NULL |
+| `cover_url` | TEXT | Nullable |
+| `description` | TEXT | Nullable |
+
+Missing covers and descriptions are stored as NULL.
```
