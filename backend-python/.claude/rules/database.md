---
paths:
  - "alembic/**"
  - "db/**"
  - "**/migrations/**"
---
# Database

- Schema changes go through a new migration file, numbered after the last one. Never edit a migration that has been applied anywhere. Never change the database by hand.
- Run migrations with `uv run alembic upgrade head`. Deployed environments run them as a one-shot step before the service updates.
- A column added to a table that already has rows gets no `server_default` when the default would read as a measurement: NULL means "predates the column", 0 means "measured and zero".
- Every query is parameterized. Index any column used in WHERE or JOIN.
- Observability and audit writes are fire-and-forget and fail soft. They never block the request path.
