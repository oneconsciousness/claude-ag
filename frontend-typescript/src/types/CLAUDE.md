# Types — CLAUDE.md

<!-- template:
This file loads only when Claude touches a file under `src/types/`. It is the catalogue of the domain types
and the rules for adding one. Keep every entry one line: name, the values or fields, and what reads it.
Delete an entry in the same PR that deletes the type; `/claude-docs-check` maps `src/types/*` here.
-->

## Architecture

Domain types live in `src/types/` so they are reachable from any layer (hooks, contexts, components, libs). Never define a cross-cutting domain type inside `components/`; that creates a dependency cycle when hooks or contexts need it.

### App-only types (`src/types/{{APP_TYPES_FILE}}.ts`)

`as const` objects, for tree-shakeability and narrowing:

- `{{STATE_ENUM}}`: `{{STATE_VALUES}}`. <!-- template: one line per enum: name, values, one-phrase meaning of any value that is not obvious. -->

Interfaces:

- `{{MESSAGE_TYPE}}`: one item in the main list; role, content, optional tool fields.
- `{{IMPERATIVE_HANDLE}}`: imperative handle a child exposes to a parent; the only methods are `{{HANDLE_METHODS}}`.

### Generated contract (`src/types/generated/`)

Written by `{{TYPES_GENERATOR_COMMAND}}` from the shared contract package; committed here; never hand-edited. A contract change regenerates these files in the same PR, and CI fails on drift.

- `{{GENERATED_FILE}}`: `{{GENERATED_EXPORTS}}`. Re-exported under stable local names from the app-only file, so consumers never import the generated path.

### Discriminated unions

- `{{SERVER_EVENT_UNION}}`: closed union of typed event variants. Switch on `event.type` for narrowing. Unrecognized events become a client-synthesized `{ type: 'unknown'; raw }` variant, never a `{ type: string }` catch-all, which would widen the discriminant and kill narrowing for every variant.
- `{{CLIENT_EVENT_UNION}}`: the messages this app sends.

## Conventions

- Always use the typed constant: `{{STATE_ENUM}}.X`, never the string literal.
- A new server event is added to the server union. A new tool result adds both its component-type constant and its tool-name constant.
- Shapes the contract already covers come through the generated re-exports; do not hand-roll them.
- Cross-layer interfaces (imperative handles, callback signatures several components consume) live here, not next to a single component.
