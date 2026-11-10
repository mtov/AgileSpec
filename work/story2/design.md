# Story 2 — Design

## Implementation

- `app.py`: render two separate views, controlled by the current page and selected
  podcast ID in `st.session_state`. Resolve episode covers
  in order: episode image, saved podcast image, default image.
- Fetch on opening the episodes page; replace the previous list and reset its visible
  count. Keep both in session state so pagination does not refetch the feed.
- `podlite/service.py`: load the selected subscription, retrieve its episodes, and
  sort newest first, with undated episodes last. Preserve feed order for equal dates.
- `podlite/feeds.py`: reuse RSS validation and plain-text conversion; read each
  item's title, description, `pubDate`, and cover (`itunes:image`, then `image/url`).
  Return `None` for missing or invalid cover URLs; apply text fallbacks from `spec.md`.
  Parse dates with `email.utils.parsedate_to_datetime`,
  normalize to UTC (assume UTC when no timezone is provided), and treat invalid
  dates as missing.
- `podlite/storage.py`: retrieve the selected subscription by ID; no schema changes.

## Data

Episodes remain in session memory: `title`, `description`, `image_url`, and `published_at`
(UTC datetime or `None`).
