# Tech Stack

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

## Implementation Decisions

- Setup: `venv` + `pip`; pinned dependencies in `requirements.txt` and
  `requirements-dev.txt` (tests).
- Planned playback: native `st.audio`; no autoplay or automatic progress tracking.
- Runtime: local; SQLite stored in `data/podlite.db` (excluded from Git).
