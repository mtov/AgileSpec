# Story 3: Play Episodes

As a listener, I want to play, pause, and move through an episode so
that I can control my listening.

## Normal Case

- Play an episode from the Episodes page.
- Pause and continue playback.
- Move forward or backward using the playback progress bar.
- Start playback only when the listener requests it.

## Edge Cases

- Missing or invalid audio URL: show "Audio unavailable" for that episode.
- Unavailable or unsupported audio: the player indicates a playback
  failure; other episodes remain accessible.
- Seeking may be limited by the browser or audio server.
