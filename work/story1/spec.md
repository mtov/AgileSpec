# Story 1 — Add a Podcast

As a listener, I want to add a podcast by its RSS URL so that I can access its episodes.

## Acceptance Criteria

### Normal Flow

- Enter an HTTP or HTTPS feed URL and submit it.
- For a valid podcast RSS feed, add the podcast and show its cover, title, and description.
- Save subscriptions in SQLite and restore them when the app restarts.
- Show loading feedback while adding and a success message with the podcast title.

### Edge Cases

- Prevent duplicate feed URLs and show a clear error.
- Use a default cover when none is provided and "No description available" for
  missing or empty descriptions.
- With no subscriptions, prompt the listener to add a podcast.
- Show a clear error for an invalid URL, an unreachable feed, or invalid podcast RSS;
  keep existing podcasts unchanged.
- Show a clear error for database failures.
