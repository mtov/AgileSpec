# Story 2: Design

- `app.py`: navigate between Home and Episodes using session state.
- `podlite/service.py`: `list_episodes(podcast_id)` retrieves the
  subscription and requests its feed.
- `podlite/feeds.py`: reuse RSS retrieval and extract the first
  20 episodes in feed order.
- Read title, description, pubDate, and `itunes:image`.
  Fall back to `content:encoded` for descriptions.
- Convert HTML to plain text and dates to YYYY-MM-DD.
- Fetch episodes when opening or reloading the page, without
  storing them in SQLite.
