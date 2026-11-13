# Architecture

## Tech Stack

| Technology | Purpose |
| --- | --- |
| Python 3.14 | Application language. |
| Streamlit 1.67.0 | Web interface. |
| SQLite (`sqlite3`) | Data persistence. |
| `urllib.request` | RSS feed fetching. |
| `xml.etree.ElementTree` | RSS XML parsing. |
| `html.parser` | Plain-text descriptions. |
| `email.utils` | Episode publication date parsing. |
| pytest 9.2.0 | Automated tests. |

RSS and SQLite use Python's standard library.

### Environment and Runtime

- Setup: `venv` + `pip`; pinned dependencies in `requirements.txt` and
  `requirements-dev.txt` (tests).
- Planned playback: native `st.audio`; no autoplay or automatic progress tracking.
- Runtime: local; SQLite stored in `data/podlite.db` (excluded from Git).

## Decisions

- One local Streamlit app, with separate modules for logic, feeds, and storage.
- UI calls the service, which uses feed and storage modules independently of Streamlit.
- SQLite stores subscriptions with titles, cover URLs, and plain-text descriptions.
- Separate subscription and episode views, with navigation stored in session state.
- "See Episodes" opens a podcast's episodes; "Back to Podcasts" returns to subscriptions.
- Fetch RSS on subscription or opening the episode view; keep episodes in session memory.
- Show episodes newest first, initially 10; "Load more" reveals 10 more without refetching.
- Episode cards show cover, title, UTC date, and plain-text description; missing
  episode covers fall back to the podcast cover, then the default image.
- Playback, refresh, and played status belong to later stories.
- Tests use sample feeds and temporary databases; errors appear in the UI.

## Structure

```text
app.py          # Subscriptions and episode browsing
podlite/
  service.py    # Application logic
  feeds.py      # RSS fetching and parsing
  storage.py    # SQLite access
tests/          # pytest tests
assets/         # Default podcast cover
data/           # Local database; excluded from Git
```
