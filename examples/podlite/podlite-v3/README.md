# PodLite v3

[PodLite](../README.md) | [AgileSpec](../../../README.md)

As a listener, I want to play, pause, and move through an episode.

## Project Specs

- [backlog.md](AgileSpec/project/backlog.md)
- [definition-of-done.md](AgileSpec/project/definition-of-done.md)
- [architecture.md](AgileSpec/project/architecture.md)
- [ui.md](AgileSpec/project/ui.md)
- [database.md](AgileSpec/project/database.md)

## User Story Spec

- [acceptance.md](AgileSpec/stories/story3/acceptance.md): expected behavior.
- [design.md](AgileSpec/stories/story3/design.md): implementation decisions.
- [views.md](AgileSpec/stories/story3/views.md): audio controls and layout.

No `tables.md` is needed: playback does not change the database.

## Consolidation

Story 3 consolidated and approved. `architecture.md` records direct
audio playback, and `ui.md` specifies that playback starts only on user
request. Story 3 is marked complete in `backlog.md`.

Changes relative to `podlite-v2`: `-` removed, `+` added.

No new persistence conventions were needed; `database.md` is unchanged.

### architecture.md

Recorded direct audio playback without storing audio files.

```diff
--- podlite-v2/architecture.md
+++ podlite-v3/architecture.md
@@ -22,0 +23,2 @@
+
+Use `st.audio` to play audio from RSS URLs without storing audio files.
```

### ui.md

Recorded that playback starts only on user request.

```diff
--- podlite-v2/ui.md
+++ podlite-v3/ui.md
@@ -8,0 +9 @@
+- Start audio playback only on user request.
```

## Screenshot

<p align="center">
  <img src="screenshot-v3.png" alt="PodLite episode audio player"
       width="480">
</p>

## Run

From the repository root:

```bash
cd examples/podlite/podlite-v3
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m streamlit run app.py
```

Run tests with `python -m pytest` from the same directory.
The database is local to this version at `data/podlite.db`.
