---
paths:
  - "src/components/**"
  - "src/hooks/**"
  - "src/stores/**"
  - "src/contexts/**"
---
# React

- Function components with hooks. Every hook (`useState`, `useRef`, `useMemo`, `useCallback`, `useEffect`) is declared before any conditional `return`. Hooks run in the same order every render; a hook after `if (...) return null` is a crash waiting to happen. `react-hooks/rules-of-hooks` is an error.
- State visible to more than one component flows through the store or context, never through local state. `useState` is for purely local affordances: hover, open/closed, transient form values.
- Browser-only state (`localStorage`, `matchMedia`, window size) is read through `useSyncExternalStore` with a server snapshot that does not consult the browser, never inside a `useState` initializer. Setting state inside an effect to mirror a value is an error.
- When a parent must scroll or focus a child, expose an imperative handle with `forwardRef` and `useImperativeHandle`. The handle's interface lives in `src/types/`.
- Styling: Tailwind utilities first. Inline `style` only for design tokens the utility layer cannot express. Global CSS only when the target renders in a portal that component-scoped styles cannot reach.
- `src/components/ui/` holds the generated primitives (shadcn or equivalent). Regenerate, do not hand-edit. A forked primitive gets a `.custom.tsx` suffix and a header comment saying why.
- Side effects that record what the user did (analytics, engagement) ride on the event and never block or cancel it.
- One default export per component file is acceptable where the codebase already does it; everything else is a named export.
