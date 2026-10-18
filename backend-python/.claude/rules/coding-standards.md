# Coding standards

- Minimal code. No speculative abstractions. No options nobody asked for.
- Prefer editing an existing file to adding one.
- Delete what is unused. No dead branches.
- Every public class, method and function carries a one-line summary in the language's own doc format (Google-style docstrings in Python), then sections only when they add something the signature does not say. Comments are single line and only where the code cannot say it. No comment blocks. No commented-out code.
- Every change is verifiable. If you cannot test it, say so before shipping it.
- Every value that crosses a boundary (HTTP, WebSocket, MCP, database row, file, LLM output) is a typed model. Validate right after deserializing. Never `dict[str, Any]` for a known shape.
- Treat LLM output as untrusted data: check the type before you call a method on it.
- A type that another repo reads or writes, or could later, lives in the shared contract package first (if this project has one), then is imported here. Never define it here now and move it later. When in doubt it is shared; say so in the plan before writing it.
- Secrets never appear in code, logs, tests, or chat. `.env` files and key material are off limits; a hook enforces this.
- Type hints on every parameter and return value, in tests too. No bare `dict`, `list`, `tuple` or `Any` where the shape is known: use `dict[str, X]`, a dataclass, a TypedDict, or a Pydantic model. `Any` is allowed only for an untrusted input at the edge, and the next line validates it into a type.
- Match the surrounding code's style, not its gaps. New and changed code is fully typed even when older files are not.
