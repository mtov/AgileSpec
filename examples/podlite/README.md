# PodLite

PodLite demonstrates AgileSpec through a small podcast player using
Python, Streamlit, and SQLite. Each version has its own project specs
and backlog, capturing a development step.

## Versions

- [podlite-v0](podlite-v0/README.md): inception and initial project specs.
- [podlite-v1](podlite-v1/README.md): RSS subscriptions and local storage.
- [podlite-v1-consolidated](podlite-v1-consolidated/README.md): story 1
  consolidated and approved.
- [podlite-v2](podlite-v2/README.md): episode browsing, consolidated
  and approved.
- [podlite-v3](podlite-v3/README.md): audio playback, consolidated
  and approved.
- [podlite-v4](podlite-v4/README.md): unsubscribe, consolidated
  and approved.

## Setup and Run

From the repository root, enter the version you want to study and create
its Python environment. For v0:

```bash
cd examples/podlite/podlite-v0
python3 -m venv .venv
source .venv/bin/activate
```

Version v0 contains specifications only; there is no application to run
yet. To run the application, follow the
[v4 instructions](podlite-v4/README.md#run).
