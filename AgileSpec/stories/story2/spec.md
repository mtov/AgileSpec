# Story 2 — Browse Episodes

As a listener, I want to browse a podcast's episodes so that I can choose what to hear.

## Acceptance Criteria

### Normal Case

- Open a subscribed podcast's episodes on a separate page and return without changing subscriptions.
- Show each episode's cover, title, publication date, and plain-text description.
- List episodes from newest to oldest by publication date.
- Show 10 episodes per batch; reset to the first 10 whenever the episodes page opens.
- Show loading feedback while fetching the feed.

### Edge Cases

- With no subscriptions, prompt the listener to add a podcast.
- Show "No episodes available" for an empty feed; hide "Load more" when all episodes are visible.
- Use "Untitled episode" and "No description available" for missing or empty text.
- Show "Date unavailable" for missing or invalid dates; place those episodes last.
- Use the podcast's cover when an episode has none; use the default cover when neither is available.
- Show a clear error if the feed cannot be fetched or parsed; preserve subscriptions.
- Allow returning to subscriptions even when the feed is empty or fails to load.
