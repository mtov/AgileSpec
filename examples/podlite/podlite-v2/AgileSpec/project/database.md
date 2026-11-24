# Database

- Use a local SQLite database, accessed through Python's `sqlite3`.
- Use parameterized queries and transactions for writes.
- Keep the database file out of version control.
- Store data in `data/podlite.db`, created on first use.
- Store missing optional metadata as NULL, not UI fallback values.
