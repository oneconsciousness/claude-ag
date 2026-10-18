# `src/components/` — CLAUDE.md

<!-- template:
This file loads only when Claude touches a file under `src/components/`. It describes the tree, the
rendering pipeline, what the tree reaches outside itself, and the recipe for the most common addition.
No directory tree: list the folders and the files that matter as bullets, each with what it owns. A tree
rots the first time someone renames a file; a bullet list survives a rename.
-->

{{COMPONENTS_SUMMARY}}

<!-- template: two sentences. Which entry mounts which top-level component, and what framework is NOT in
play ("plain SPA, no Next.js, no router"). -->

## What is here

- `{{LAYOUT_COMPONENT}}.tsx`: the chrome shell.
- `{{LIST_COMPONENT}}.tsx`: the scrollable main surface; exposes `{{IMPERATIVE_HANDLE}}`.
- `{{ITEM_COMPONENT}}.tsx`: renders one item.
- `content/`: renderers for tool results, resolved through the registry.
- `primitives/`: shared atoms. `ui/`: generated primitives (shadcn or equivalent), regenerate rather than hand-edit.
<!-- template: one bullet per folder and per top-level file that a reader must know about. -->

## Rendering pipeline

`{{STORE}}` holds all state. The pipeline: store → page (reads the store, routes by UI state) → layout (chrome) → list surface (receives the imperative handle) → item (one per entry) → `content/<kind>` renderer, resolved at render time through the registry.

<!-- template: name the component at each hop. Note any third-party component deliberately NOT used and
why, so nobody reintroduces it. -->

## Cross-directory dependencies

- `@/stores/*` or `@/contexts/*`: the single source of truth for state. Intent actions feed the connection layer.
- `@/machines/*`: the connection state machine, a pure reducer with a driver hook; the reducer is unit-tested exhaustively.
- `@/hooks/*`: reusable behaviour.
- `@/lib/tool-registry`: runtime lookup of tool name → renderer; `@/lib/tool-registrations` is the side-effect import that fills it.
- `@/lib/design-tokens`: constants for the few inline styles.
- `@/types/*`: domain and state types.
<!-- template: one bullet per module outside this tree that components import, with what it provides. -->

## Conventions

- Filenames kebab-case.
- One default export per component file where the tree already does it; helpers next to it are named exports.
- Styling: Tailwind utilities first; design tokens through the configured utility names; inline `style` only for values the utility layer cannot express; global CSS only for targets inside a portal.
- State: never local state for anything another component reads; it flows through the store. `useState` is for purely local affordances.
- Imperative handles: `forwardRef` + `useImperativeHandle`, interface in `src/types/`.
- Hooks before any early return.

## Adding a new tool renderer

1. Add the constant to the tool-name enum in `src/types/`.
2. Create the renderer under `content/`.
3. Register it in `src/lib/tool-registrations.ts`.

No change in the item component; it resolves the renderer at render time through the registry.
