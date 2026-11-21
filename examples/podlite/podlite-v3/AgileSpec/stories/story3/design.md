# Story 3: Design

- `podlite/feeds.py`: extract the audio URL and MIME type from the
  episode's RSS `enclosure`. Accept HTTP or HTTPS URLs.
- `podlite/service.py`: include audio metadata in the episode list.
- `app.py`: use `st.audio` with autoplay disabled.
- Let the browser handle playback controls and errors.
- Stream audio directly from its URL without storing audio files.
