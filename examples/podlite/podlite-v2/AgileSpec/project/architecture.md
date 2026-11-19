# Architecture

PodLite is a local podcast application without login.

## Technology Stack

- Python for application logic.
- Streamlit for the web interface.
- SQLite for local persistence.
- Python standard library for fetching and parsing RSS feeds.
- pytest for automated tests.

## Structure

- `app.py`: Streamlit pages and navigation using session state.
- `podlite/service.py`: application logic.
- `podlite/feeds.py`: RSS, podcast metadata, and episode metadata.
- `podlite/database.py`: SQLite persistence.

The UI accesses persistence through services.

Episodes are read from RSS on demand and are not stored in SQLite.
