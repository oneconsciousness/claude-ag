---
name: verify
description: Run the checks that make "done" true before reporting a task complete. No side effects beyond running tests.
---
# Verify before saying done

1. Tests. Run what CI runs, from the repo root: `uv run pytest`. Report the exact counts. A failure is reported as a failure, with the output.
2. Read back. Read `git diff` for every file you changed. Check each hunk does what the task asked and nothing more.
3. Side effects. For every function, class, field or constant you changed or removed, grep the repo for other users. Fix or list them.
4. Secrets. Scan the diff for keys, tokens, passwords, connection strings. None may be in it.
5. Contract check, when the change sends data across a boundary (HTTP, WebSocket, MCP, database, a shared contract package): read the receiving side's type definition first, not the docs, and cast explicitly.
6. Full-flow trace, when the change spans two services, or both a live path and a history path: name each hop and confirm the sender's shape matches the receiver's at each one.
7. Plan adherence, when working from a written plan: diff your output against the plan's fields, columns and names. Anything missing or extra is a bug until the human says otherwise.

Then report: what was verified, what was not, and why.
