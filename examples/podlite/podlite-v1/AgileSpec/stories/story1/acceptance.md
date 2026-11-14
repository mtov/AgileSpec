# Story 1: Subscribe to a Podcast

As a listener, I want to subscribe using an RSS URL and keep the podcast
in my list.

## Normal Case

- Submit a feed URL and receive confirmation with the podcast title.
- Show subscriptions with their title, cover, and plain-text
  description.
- Keep subscriptions available after restarting the application.

## Edge Cases

- Trim URL whitespace; reject empty, invalid, or duplicate URLs.
- Accept only HTTP or HTTPS URLs with a host.
- Show an error for unavailable or invalid RSS feeds, missing titles,
  or database failures. Do not report success or save invalid feeds.
- Missing or unavailable cover: show a default image.
- Empty description: show "No description available".
- Empty list: invite the listener to add a podcast.
