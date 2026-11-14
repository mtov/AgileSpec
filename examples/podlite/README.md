# PodLite

PodLite will demonstrate AgileSpec through a podcast player using Python,
Streamlit, and SQLite. Development will start with RSS subscriptions and
episode browsing, followed by audio playback.

This directory will contain its code, tests, and specifications.

## Setup

From the repository root:

```bash
cd examples/podlite
python3 -m venv .venv
source .venv/bin/activate
```

After the application and tests are implemented:

```bash
python -m pip install -r requirements-dev.txt
python -m streamlit run app.py
python -m pytest
```
