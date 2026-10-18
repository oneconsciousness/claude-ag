---
paths:
  - "src/**/*.ts"
  - "src/**/*.tsx"
---
# TypeScript

- `strict` is on in `tsconfig.json`. No `any`, no `as unknown as`, no `@ts-ignore`. Named exports. Function components with hooks; no classes.
- Every boundary is a Zod schema (or a generated contract type) under `src/lib/schema/`: API responses, WebSocket events, form data, storage, URL params. `parse`, or `safeParse` with a typed error path, right after reading; field access on the parsed value.
- Schema modules stay client-safe: Zod and its siblings only. A schema file that pulls in a server-only dependency breaks the client bundle.
- Domain types live in `src/types/`, reachable from any layer. Never define a cross-cutting type inside `components/`; hooks and stores that need it would create a dependency cycle.
- Enums are `as const` objects, not `enum`, for tree-shaking and narrowing. Always use the typed constant: `UIState.CHAT`, never the string `'chat'`.
- Discriminated unions are closed. Switch on the discriminant for narrowing. Represent unknown variants with a synthesized `{ type: 'unknown'; raw }` member, never a `{ type: string }` catch-all, which widens the discriminant and kills narrowing for every variant.
- Generated files (`src/types/generated/**` or wherever the generator writes) are never edited by hand. Regenerate in the same PR that changes the source, and keep a drift check in CI.
- Environment values are read through one helper module, never raw `import.meta.env` or `process.env` in components. Build-time values are public; a secret never goes there.
- JSDoc: a summary line on every exported function, component and type. `@param` and `@returns` only when they say something the signature does not.
- Arithmetic and formatting live in exported pure helpers a test can reach, not inline in markup.
- Filenames are kebab-case. Tests sit next to the code they test as `<name>.test.ts(x)`.
