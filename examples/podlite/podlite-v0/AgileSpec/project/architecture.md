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

- UI: renders screens and handles user input.
- Services: handle application logic and RSS feeds.
- Persistence: reads and writes local data.

The UI accesses persistence through services.
