# Coding standards

- Minimal code. No speculative abstractions. No options nobody asked for.
- Prefer editing an existing file to adding one.
- Delete what is unused. No dead branches.
- Every exported function, component and type carries a one-line summary in the language's own doc format (JSDoc in TypeScript), then `@param` and `@returns` only when they say something the signature does not. Comments are single line and only where the code cannot say it. No comment blocks. No commented-out code.
- Every change is verifiable. If you cannot test it, say so before shipping it.
- Every value that crosses a boundary (HTTP response, WebSocket event, form data, storage, URL params, LLM output) is parsed into a typed shape (a Zod schema, or the generated contract types) right after it is read. Field access happens on the parsed value. Never `any` or `Record<string, unknown>` for a known shape.
- Treat LLM output as untrusted data: check the type before you call a method on it.
- A type that another repo reads or writes, or could later, lives in the shared contract package first (if this project has one), then is imported or generated here. Never define it here now and move it later. When in doubt it is shared; say so in the plan before writing it.
- Secrets never appear in code, logs, tests, or chat. `.env` files and key material are off limits; a hook enforces this. Anything prefixed for the client bundle is public by definition; never put a secret there.
- TypeScript `strict` is on. No `any`, no `as unknown as`, no `@ts-ignore`. Named exports. Function components with hooks; no classes. `bun run check` (format, lint, types) is the gate.
- Match the surrounding code's style, not its gaps. New and changed code is fully typed even when older files are not.
