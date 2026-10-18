# {{PROJECT_NAME}}

<!-- template:
This file is the first thing Claude Code reads in every session. It is a constitution, not documentation.
Keep it under 200 lines. Keep only facts that will still be true in six months. HTML comment blocks like
this one are stripped before the model sees the file, so leave them in or delete them as you like.

Fill every {{TOKEN}}. Then delete the lines that do not apply. Each section below says what belongs in it.
Put in: commands Claude cannot guess, style rules that differ from the defaults, test instructions, repo
etiquette, architectural decisions, environment quirks, gotchas.
Leave out: anything derivable from the code (file lists, directory trees), standard language conventions,
long tutorials, API documentation (link it), anything that changes every sprint.
Two nested files go deeper and load only when a file under them is touched: `src/types/CLAUDE.md` and
`src/components/CLAUDE.md`. Keep the component tree and the type catalogue there, not here.
Run `/doctor` after editing; it audits this file for stale or conflicting rules.
-->

{{PROJECT_SUMMARY}}

<!-- template: one paragraph. What the app is, how it is served (SPA, static entries, under which path),
the framework decisions stated as absences too ("No Next.js, no router library"), and what this repo does
NOT own (the API, the shared contract package). -->

## Read first
- `CONTRIBUTING.md`: branches and merges (§1), the kind-stop protocol (§8), secrets rules (§12), screenshot review (§13).
- `src/types/CLAUDE.md` for the type conventions and `src/components/CLAUDE.md` for the component tree. Read the one that covers the files you are about to touch.
- `.claude/rules/`: topic rules. The path-scoped ones load when you touch matching files.
- Skills: `/repo-sync` at the start of a session, `/verify` before saying done, `/claude-docs-check` then `/raise-pr` to open a PR.

## Commands
```bash
bun install --frozen-lockfile     # Bun {{BUN_VERSION}} (packageManager), Node {{NODE_VERSION}} or newer
bun run dev                       # http://localhost:5173{{BASE_PATH}}
bun run check                     # format, lint and types (Oxfmt, Oxlint, tsc)
bun run test                      # Vitest, jsdom, src/test/setup.ts
bun run build                     # into dist/
```
<!-- template: the exact scripts CI runs, each with a short comment. If a script wraps a tool with its own
CLI (`vp`, `vite`, `next`), say which, so the agent can read that tool's docs. -->

## Config
- Nothing environment-specific is baked into the build. Each entry loads `config.js`, which sets `window.{{RUNTIME_CONFIG_GLOBAL}}`; read it only through `src/lib/runtime-config.ts`. In dev the dev server writes it from the local env file; in deployed environments the deploy writes it.
- Never read or edit `.env` files or key material. A hook blocks it. Ask the human for a value instead.
- `.mcp.json` configures Claude Code's own MCP servers (docs lookups, GitHub). It is not the app's config.
<!-- template: how runtime config reaches the page, which keys exist and which are required, where tests
set it, and the one module allowed to read it. If the project bakes config in at build time instead, say
so and name the public prefix. -->

## Entries and runtime config
- Base path `{{BASE_PATH}}` is hard-coded in `vite.config.ts`. `index.html` mounts `src/entries/{{PRIMARY_ENTRY}}/`.
- Root-absolute public assets go through `assetUrl()` in `src/lib/asset-url.ts`; never write `/images/...` in code.
<!-- template: one bullet per entry (full page, embed, widget), the URL each serves at, and any side-effect
import an entry must keep (registries, polyfills) with the symptom when it is missing. -->

## Where things are
- `src/entries/`: the HTML entries and the shared `bootstrap.tsx`.
- `src/components/`: the UI tree (see its CLAUDE.md). `src/components/ui/`: generated primitives, regenerate rather than hand-edit.
- `src/lib/`: runtime config, the API fetch wrapper, the tool registry, design tokens. `src/stores/` and `src/contexts/`: shared state. `src/hooks/`: reusable hooks.
- `src/types/`: domain types and the generated contract (see its CLAUDE.md). `src/test/`: Vitest setup.
<!-- template: one bullet per key folder and what it owns. No directory trees, no line numbers. -->

## Gotchas
- `tsconfig.json` is strict. Do not weaken it in a feature PR.
- Every REST call goes through `src/lib/api/fetch-api.ts`, not bare `fetch`, so errors are classified and reported once.
- Tailwind is pinned to `{{TAILWIND_MAJOR}}`; components carry version-specific workarounds, so do not upgrade casually.
<!-- template: facts that break things if "fixed". Each bullet says what not to do and why. Examples from
real repos: "navigation writes the URL with history.replaceState on purpose; a router navigation caused a
reload loop", "a preload error is reported but never reloads the page; a reload would end a live call". -->

## Branches and deploy
- Work on a branch off `main`. PR to `main`, squash-merge. Releases are `vX.Y.Z` tags; a tag is never moved.
- CI runs on every PR: `bun run check`, `bun run test`, `bun run build`{{EXTRA_CI_JOBS}}. A push to `main` deploys through `{{DEPLOY_WORKFLOW}}`; rollback is `{{ROLLBACK_COMMAND}}`.
- A PR that changes the UI gets a preview at `{{PREVIEW_HOST_PATTERN}}`; say in the PR what to look at there.
- Guards: a hook blocks commits and pushes on `main`, force pushes, `--no-verify` and tag moves. `git push` and `gh pr create` always ask. PR titles must be Conventional Commits. A PR also needs a docs decision from `/claude-docs-check`.
<!-- template: the branch flow, the CI gates by name, what a push deploys and how (build once, promote the
same artifact), how to roll back, preview hosts, and the active hook guards. -->

## Scope
Change only what the task names. Do not fix nearby code or add tests the change does not need. Unrelated problems go in a one-line follow-up note.
