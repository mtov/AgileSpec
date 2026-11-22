# Story 4: Design

- `podlite/database.py`: add `unsubscribe(podcast_id)` using
  a parameterized DELETE within a transaction. Ignore missing IDs.
- `podlite/service.py`: add `unsubscribe(podcast_id)` and translate
  storage errors into `SubscriptionError`.
- `app.py`: track the pending unsubscribe action in session state.
  After success, clear it and refresh Home.
- Reuse the existing schema; unsubscribing does not require RSS retrieval.
