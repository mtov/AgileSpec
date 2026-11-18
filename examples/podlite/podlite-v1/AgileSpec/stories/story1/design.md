# Story 1: Design

## Modules

- `app.py`: Streamlit form, subscription list, and feedback.
- `podlite/service.py`: validate URLs and coordinate feeds and storage.
- `podlite/feeds.py`: fetch RSS and extract podcast metadata.
- `podlite/database.py`: initialize the database, save, and list
  subscriptions.

## Decisions

- Trim URLs; otherwise compare them as entered.
- Fetch feeds with `urllib.request` and a 10-second timeout; parse with
  `xml.etree.ElementTree`.
- Prefer `itunes:image` for covers, then the RSS channel image.
- Convert description HTML to plain text using the standard library.
- Save metadata in `data/podlite.db`; create it on first use.
- List saved subscriptions in insertion order without refetching feeds.

Test using temporary databases and mocked feed requests.
