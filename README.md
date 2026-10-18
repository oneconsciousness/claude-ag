# claude-ag

Reusable Claude Code setup, as two copy-in templates:

| Folder | For | Stack defaults |
|---|---|---|
| `backend-python/` | a Python service | FastAPI, Pydantic, SQLAlchemy + alembic, pytest, ruff, uv |
| `frontend-typescript/` | a TypeScript web app | Vite, React, Bun, Vitest, Oxlint/Oxfmt, Tailwind, Zod |

Each folder is complete on its own: a `.claude/` directory (settings, hooks, rules, agents, skills), a templated `CLAUDE.md` and `CONTRIBUTING.md`, a `.gitignore` block and two optional example files. Nothing in here names a product, a vendor integration or a person; a test enforces that.

## What the kit does

- **Hooks** (Python, run by Claude Code before and after tool calls): block commits and pushes on protected branches, force pushes, `--no-verify` and release-tag moves; block reading or writing `.env` files and key material; reject PR titles that are not Conventional Commits; block `gh pr create` until the branch carries a docs decision; report lint findings on the lines an edit changed.
- **Rules** (`.claude/rules/*.md`): three that load every session (working agreement, coding standards, git and PRs) and three scoped by `paths:` frontmatter that load when a matching file is touched.
- **Agents**: `reviewer` (adversarial review of a branch or PR) and `docs-keeper` (keeps CLAUDE.md and the rules true to the code).
- **Skills**: `/repo-sync` at session start, `/verify` before saying done, `/claude-docs-check` then `/raise-pr` to open a PR. `raise-pr` shows a card and waits for a yes.
- **CLAUDE.md and CONTRIBUTING.md templates**: `{{TOKENS}}` mark values to fill; `<!-- template: -->` comments explain what each section is for and are stripped before the model sees the file.

## Adopt a template

Each template folder has a README with the exact steps. In short: copy the folder's contents into the repo, fill the tokens, adjust the config block at the top of each hook, point `map.json` at the repo's real paths, append the `.gitignore` block, run `claude` and `/doctor`.

## Tokens

| Token | Where | Meaning |
|---|---|---|
| `{{PROJECT_NAME}}` | CLAUDE.md, CONTRIBUTING.md | repo name |
| `{{PROJECT_SUMMARY}}` | CLAUDE.md | one paragraph: what it is, the parts, what it does not own |
| `{{APP_MODULE}}`, `{{ENTRY_MODULE}}`, `{{SETTINGS_MODULE}}`, `{{REQUIRED_ENV_VARS}}` | backend CLAUDE.md | entry point, settings and required env |
| `{{CI_JOBS}}`, `{{DEPLOY_WORKFLOW}}`, `{{ROLLBACK_COMMAND}}`, `{{EXTRA_CI_JOBS}}` | CLAUDE.md, CONTRIBUTING.md §1 | CI gates, deploy trigger, rollback |
| `{{BUN_VERSION}}`, `{{NODE_VERSION}}`, `{{BASE_PATH}}`, `{{PRIMARY_ENTRY}}`, `{{RUNTIME_CONFIG_GLOBAL}}`, `{{TAILWIND_MAJOR}}`, `{{PREVIEW_HOST_PATTERN}}` | frontend CLAUDE.md | toolchain and serving facts |
| `{{APP_TYPES_FILE}}`, `{{STATE_ENUM}}`, `{{STATE_VALUES}}`, `{{MESSAGE_TYPE}}`, `{{IMPERATIVE_HANDLE}}`, `{{HANDLE_METHODS}}`, `{{TYPES_GENERATOR_COMMAND}}`, `{{GENERATED_FILE}}`, `{{GENERATED_EXPORTS}}`, `{{SERVER_EVENT_UNION}}`, `{{CLIENT_EVENT_UNION}}` | `src/types/CLAUDE.md` | the type catalogue |
| `{{COMPONENTS_SUMMARY}}`, `{{LAYOUT_COMPONENT}}`, `{{LIST_COMPONENT}}`, `{{ITEM_COMPONENT}}`, `{{STORE}}` | `src/components/CLAUDE.md` | the component tree |
| `{{INTEGRATION_BRANCH}}`, `{{STAGING_BRANCH}}`, `{{PROD_BRANCH}}`, `{{STAGING_DEPLOY_WORKFLOW}}`, `{{PROD_DEPLOY_WORKFLOW}}` | CONTRIBUTING.md appendix B | only for multi-environment promotion |

Hook parameters are not tokens; they sit in a `# --- config ---` block at the top of each script: `PROTECTED`, `BASE`, `SECTION_REF`, `TAG_RE` (branch-protection), `ALLOWED_TYPES` (pr-title), `DEFAULT_BASE` (docs-check), `SKIP` and `LINTERS` (lint).

## Branch model

The default is a single protected `main`, PRs squash-merged, releases as `vX.Y.Z` tags. A project that promotes through several environments follows CONTRIBUTING.md appendix B: add the branches to `PROTECTED`, set `BASE` and the `map.json` base to the integration branch, and update the git rule and the raise-pr skill.

## Keeping the two templates in sync

The hooks, `docs-keeper`, the working agreement, the git rule, and the `raise-pr`, `repo-sync` and `claude-docs-check` skills are byte-identical in both folders. Change one and copy it to the other; `tests/test_structure.py` fails on drift.

## Tests

```bash
python3 -m unittest discover tests -v
```

`test_hooks.py` pipes Claude Code payloads into every hook and checks the allow/deny decision. `test_structure.py` checks JSON validity, frontmatter, forbidden words, CLAUDE.md length and cross-template sync. The lint tests skip when `uvx` or `bunx` is not on the PATH.

## Plugins

The folders are plugin-shaped: `skills/`, `agents/` and `hooks/` are the same layout a Claude Code plugin uses. Adding a `.claude-plugin/plugin.json` would make a template installable with `claude plugin install` instead of copied. Not done yet.

## Sources

Built from the Claude Code docs at code.claude.com/docs (memory, settings, hooks, skills, sub-agents, plugins, best practices) and from the kit that grew across four production repos. The hook fixes made while templating: `git push -n` (dry run) is no longer mistaken for `--no-verify`, branch names are derived from one tuple instead of being repeated in regex literals, and the secrets hook covers key material and credential files, not only `.env`.

## License

MIT.
