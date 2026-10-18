---
paths:
  - "**/*.py"
---
# Python

## Boundaries and types
- Pydantic models at every boundary: request and response bodies, WebSocket frames, MCP tool arguments and results, database rows, LLM structured output. `Model.model_validate(raw)` right after deserializing; field access happens on the model.
- Settings are a pydantic-settings class. With `extra="ignore"` a typo in an env var name fails silently, so check the name when a value is missing.

## Types
- `Optional[X]` and `dict[str, X]`. `Mapping` and `Sequence` for parameters you only read. A TypedDict or dataclass for a JSON-shaped value that stays inside this service; a Pydantic model for anything that crosses a boundary.

## Docstrings
- Google style: a summary line in the imperative, a blank line, then `Args:`, `Returns:`, `Raises:` as needed. Types stay in the hints, never repeated in the docstring. Private helpers and tests need only the summary line, and only when the name does not already say it.

## Failure handling
- Telemetry and capture paths (observability, usage, audit) never raise into the request path. Wrap them; log a WARNING with where, why, and what happens next.
- On a validation error at a boundary: log at WARNING with the function name, the error, and a sanitized snippet, then take the documented fail-soft path. Never silent.

## Logging
- `log = logging.getLogger(__name__)`. No `print` in production paths.
- WARNING and ERROR lines say where (`module.function`), why, and what happens next. Include request, session and user ids when you have them, as key=value. Never log secrets.
- The root logger is configured once, at the top of the entry module, before any module-level logger is created.

## Async and boot
- FastAPI and asyncio throughout. Do not block the event loop. `httpx` for HTTP, the async SQLAlchemy engine for Postgres.
- Never add a network call at import time; put it in the lifespan. Boot side effects (pools, warm-ups, health probes) fail soft in development and hard where the deployment says so.
