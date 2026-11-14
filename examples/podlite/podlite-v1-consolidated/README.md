# PodLite v1 — Consolidation

[PodLite](../README.md) | [AgileSpec](../../../README.md)

Project specs updated from the approved story 1 implementation.
Consolidation awaits review; the story remains unchecked in the backlog.

As a listener, I want to subscribe using an RSS URL and keep the podcast
in my list.

## Project Specs

Architecture, UI, and database documentation reflect the implementation.
The backlog and shared Definition of Done await final completion approval:

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

```diff
--- podlite-v1/ui.md
+++ podlite-v1-consolidated/ui.md
@@ -6,0 +7,6 @@
+- Use fallbacks for missing covers and descriptions.
+
+## Home
+
+A subscription form followed by podcast cards with cover, title, and
+plain-text description.
```

### database.md

```diff
--- podlite-v1/database.md
+++ podlite-v1-consolidated/database.md
@@ -6,0 +7,13 @@
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
