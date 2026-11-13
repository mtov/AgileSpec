# Environment Setup

Goal: prepare the local development environment.

- [x] Create a `.venv` virtual environment.
- [x] Add pinned dependencies to `requirements.txt` and `requirements-dev.txt`.
- [x] Install Streamlit and pytest in `.venv`.
- [x] Add `.venv/`, `data/`, Python caches, and pytest caches to `.gitignore`.
- [x] Verify Streamlit starts with a temporary smoke app.
- [x] Verify pytest runs with a temporary smoke test.

Done when both checks pass and the temporary files are removed.

## Execution Log

- 2026-11-10: Created `.venv` (Python 3.14.7), pinned requirements, and `.gitignore`.
- Installed Streamlit 1.67.0 and pytest 9.2.0; dependency check passed.
- Streamlit health: HTTP 200; pytest: 1 passed. Server stopped; temporary files removed.
