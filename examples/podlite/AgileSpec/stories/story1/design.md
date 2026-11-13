# Story 1 — Design

## Implementation

- `app.py`: render the subscription interface; load saved subscriptions on each run.
- `podlite/service.py`: validate HTTP/HTTPS URLs, trim whitespace, check duplicates,
  fetch the feed, and save only after validation succeeds.
- `podlite/feeds.py`: fetch with `urllib.request` and a timeout; parse RSS 2.0 with
  `xml.etree.ElementTree`. Read the channel title, description, and cover URL
  (`itunes:image`, falling back to `image/url`). Require a title; allow missing
  cover/description and an empty episode list. Convert HTML descriptions to plain
  text using Python's standard library.
- `podlite/storage.py`: persist and retrieve subscriptions using parameterized
  queries and transactions. Apply the schema changes defined in [tables.md](tables.md).
