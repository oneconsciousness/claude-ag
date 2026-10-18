# frontend-typescript

Claude Code setup for a TypeScript web app: Vite, React, Bun, Vitest, Oxlint and Oxfmt through `bun run check`, Tailwind, Zod at the boundaries.

What is in here:

- `.claude/settings.json`: committed permissions and hook wiring.
- `.claude/hooks/`: the same six Python hooks as the backend template. `lint.py` runs `bunx oxlint` per file; an eslint repo swaps the `LINTERS` entry in its config block.
- `.claude/rules/`: three rules that always load (working agreement, coding standards, git and PRs) and three path-scoped ones (typescript, react, testing).
- `.claude/agents/`: `reviewer` and `docs-keeper`.
- `.claude/skills/`: `repo-sync`, `verify`, `claude-docs-check` (with its `map.json`), `raise-pr`.
- `CLAUDE.md`, `src/types/CLAUDE.md`, `src/components/CLAUDE.md` and `CONTRIBUTING.md`: templates with `{{TOKENS}}` and `<!-- template: -->` guidance. The two nested files load only when a file under them is touched.
- `.gitignore`: the block to append. `.mcp.json.example` and `.claude/settings.local.json.example`: optional.

## Adopt it

1. Copy this folder's contents into the frontend root (the folder that holds `package.json`). `cp -R frontend-typescript/. <repo>/` keeps the dotfiles. In a monorepo, put `.claude/` and `CLAUDE.md` at the repo root instead and prefix the rule `paths` and the `map.json` paths with the frontend folder.
2. Fill every `{{TOKEN}}` in the three `CLAUDE.md` files and `CONTRIBUTING.md`. `grep -rn '{{' CLAUDE.md src/*/CLAUDE.md CONTRIBUTING.md` must come back empty. The root README of this repo lists every token.
3. Set the config block at the top of each hook if the defaults do not fit: `PROTECTED` and `BASE` in `branch-protection.py`, `ALLOWED_TYPES` in `pr-title.py`, `SKIP` and `LINTERS` in `lint.py`.
4. Edit `.claude/skills/claude-docs-check/map.json` so its `paths` match the repo's real files.
5. Append `.gitignore` to the repo's `.gitignore`. Rename `.mcp.json.example` to `.mcp.json` if you want the docs and GitHub MCP servers, and `settings.local.json.example` to `settings.local.json` to enable them for yourself.
6. Run `claude` in the repo, then `/doctor`. Type `/` and check that `repo-sync`, `verify`, `claude-docs-check` and `raise-pr` are listed.
7. Delete or keep the `<!-- template: -->` comments. Claude Code strips them before the model sees the file; they cost nothing.

Next.js, pnpm or eslint: change the Commands block in `CLAUDE.md`, the gates in `.claude/rules/testing.md` and the verify skill, the `allow` list in `settings.json`, and the `LINTERS` entry in `lint.py` (the `eslint` function is already there). Add a note on hydration-safe browser state to `react.md` if the app server-renders; the `useSyncExternalStore` rule already covers it.
