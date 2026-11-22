# Story 2: Browse Episodes

As a listener, I want to see a podcast's episodes.

## Normal Case

- Open episodes from a subscribed podcast.
- Show up to 20 episodes in feed order, with title, publication date,
  cover, and plain-text description.
- Return to the subscription list.

## Edge Cases

- Empty feed: show "No episodes available".
- Unavailable or invalid feed: show an error and allow retry or return.
- Missing title: "Untitled episode". Missing or invalid date:
  "Date unavailable". Empty description: "No description available".
- Missing or unavailable cover: try the podcast cover, then the default.
- If the selected subscription no longer exists, show an error.
