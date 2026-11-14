# Architecture

PodLite will be a local web application for subscribing to podcasts,
browsing episodes, and playing audio, without login.

## Technology Stack

- Python for application logic.
- Streamlit for the web interface.
- SQLite for local persistence.
- Python standard library for fetching and parsing RSS feeds.
- pytest for automated tests.

## Structure

- `app.py`: Streamlit interface.
- `podlite/service.py`: application logic.
- `podlite/feeds.py`: RSS and podcast metadata.
- `podlite/database.py`: SQLite persistence.

The UI accesses persistence through services.
