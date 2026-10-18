---
name: verify
description: Run the checks that make "done" true before reporting a task complete. No side effects beyond running tests.
---
# Verify before saying done

1. Gates. Run what CI runs, from the frontend root: `bun run check && bun run test && bun run build`. Report the exact counts. A failure is reported as a failure, with the output.
2. Read back. Read `git diff` for every file you changed. Check each hunk does what the task asked and nothing more.
3. Side effects. For every function, component, type or constant you changed or removed, grep the repo for other users. Fix or list them.
4. Secrets. Scan the diff for keys, tokens, passwords, URLs with credentials. None may be in it. Anything prefixed for the client bundle is public.
5. Contract check, when the change reads data across a boundary (HTTP, WebSocket, storage, URL params, a generated contract): read the sending side's type definition first, not the docs, and parse explicitly.
6. Full-flow trace, when the change spans the live path and the history or reload path: name each hop and confirm the shape matches at each one. Run the component through the state transition that hits any early return.
7. Plan adherence, when working from a written plan: diff your output against the plan's fields, props and names. Anything missing or extra is a bug until the human says otherwise.

Then report: what was verified, what was not, and why.
