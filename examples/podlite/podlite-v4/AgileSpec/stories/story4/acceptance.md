# Story 4: Unsubscribe from a Podcast

As a listener, I want to unsubscribe from a podcast.

## Normal Case

- Unsubscribe from a podcast on Home after confirming the action.
- Delete the subscription from SQLite and refresh the podcast list.
- Keep other subscriptions unchanged and stay unsubscribed after restarting.

## Edge Cases

- Cancel unsubscribing: keep the subscription.
- Unsubscribe from the last podcast: show the existing empty state.
- Subscription no longer exists: refresh the list.
- If unsubscribing fails, show an error and keep the subscription.
