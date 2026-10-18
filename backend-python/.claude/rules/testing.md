---
paths:
  - "tests/**"
  - "pytest.ini"
  - "pyproject.toml"
  - "conftest.py"
---
# Tests

- Run what CI runs, from the repo root: `uv run pytest`. `pytest.ini` (or the `[tool.pytest.ini_options]` table) sets `asyncio_mode = auto`, so async tests need no marker, and `testpaths`, so collection never descends into unrelated trees.
- `tests/conftest.py` stubs every required API key and neutralises `.env`. Nothing in the unit suite opens a socket.
- Integration tests run only when `TEST_DATABASE_URL` points at a database; without it they skip. CI starts the database service and runs migrations before pytest, so a migration that fails there fails the PR.
- Tests live under `tests/<package>/`, mirroring the code. New behaviour gets a test in the same PR.
- Mock at the boundary (the HTTP client, the model provider, the database), not inside the code under test.
- Report results as they are. "281 passed" means you saw it.
