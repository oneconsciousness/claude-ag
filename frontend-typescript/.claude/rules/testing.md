---
paths:
  - "src/**/*.test.ts"
  - "src/**/*.test.tsx"
  - "src/test/**"
  - "vite.config.ts"
  - "vitest.config.ts"
---
# Tests

- Run what CI runs, from the frontend root: `bun run check` (format, lint, types), `bun run test` (Vitest, jsdom, `src/test/setup.ts`), `bun run build`. All three gate every PR.
- `src/test/setup.ts` sets the runtime config and any globals a component expects. Nothing in the unit suite opens a socket; mock at the boundary (`fetch`, the WebSocket, storage), not inside the code under test.
- Tests sit next to the code as `<name>.test.ts(x)`. New behaviour gets a test in the same PR. A reducer or helper is tested exhaustively as a function; a view is tested by rendering it and asserting on text and roles, not on class names.
- Browser smoke tests (Playwright) run in CI and the deploy, not in `bun run test`. A change to one changes its fixture.
- Screenshot review follows `CONTRIBUTING.md` § 13: review several captures before reporting.
- Report results as they are. "128 passed" means you saw it.
