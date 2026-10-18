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
Run `/doctor` after editing; it audits this file for stale or conflicting rules.
-->

{{PROJECT_SUMMARY}}

<!-- template: one paragraph. What the service is, the main parts and their roles, and what this repo does
NOT own (the sibling services, the shared contract package, the frontend). Example shape:
"A FastAPI service in `app/` that <does X> for <product>. Postgres through SQLAlchemy and alembic. Calls
the <sibling> service for <Y>; that logic lives there, not here." -->

## Read first
- `CONTRIBUTING.md`: branches and merges (§1), the kind-stop protocol (§8), secrets rules (§12).
- `.claude/rules/`: topic rules. The path-scoped ones load when you touch matching files.
- Skills: `/repo-sync` at the start of a session, `/verify` before saying done, `/claude-docs-check` then `/raise-pr` to open a PR.
<!-- template: add the one or two design documents a new agent must read before changing anything, with
their decision numbers if they have them. Nothing else. -->

## Commands
```bash
uv sync --extra dev                       # what CI and the Dockerfile run
uv run uvicorn {{APP_MODULE}}:app --reload   # http://localhost:8000
uv run alembic upgrade head               # migrations
uv run pytest                             # what CI runs; pytest.ini sets testpaths
uv run ruff check . && uv run ruff format --check .
```
<!-- template: the exact commands CI runs, one per line, each with a short comment. If a command must run
from a particular directory, say so. Docker build lines go here too when the build context is unusual. -->

## Config
- `{{SETTINGS_MODULE}}` reads env and the env file through pydantic-settings. Required: `{{REQUIRED_ENV_VARS}}`. `.env.example` lists the rest.
- Never read or edit `.env` files or key material. A hook blocks it. Ask the human for a value instead.
- `.mcp.json` configures Claude Code's own MCP servers (docs lookups, GitHub). It is not the runtime's config.
<!-- template: where settings are read, which variables are required, which switch picks between modes
(local vs remote dependencies), and anything that is read at request time rather than at boot. -->

## Where things are
- `{{ENTRY_MODULE}}`: the app, `lifespan`, root logger setup, the routers.
- `{{SETTINGS_MODULE}}`: settings.
- `api/`: the routers. `db/`: database access and migrations in `alembic/versions/`. `tests/`: the suite, mirroring the packages.
<!-- template: one bullet per key module and what it owns. No directory trees, no line numbers; those rot.
A reader should be able to find the entry point, the settings, the data layer, the integrations and the
tests from this list alone. -->

## Gotchas
- The root logger is configured at the top of the entry module before any module-level logger. Log shipping depends on that order.
- Settings are not cached on purpose, so env edits are picked up in dev. Leave it.
<!-- template: facts that break things if "fixed". Each bullet says what not to do and why. Examples from
real repos: "the greeting filter lives in both the prompt and the manager; change both or neither",
"the first WebSocket frame must be the settings frame, anything else is dropped". -->

## Branches and deploy
- Work on a branch off `main`. PR to `main`, squash-merge. Releases are `vX.Y.Z` tags; a tag is never moved.
- CI runs on every PR: `{{CI_JOBS}}`. A push to `main` deploys through `{{DEPLOY_WORKFLOW}}`.
- Guards: a hook blocks commits and pushes on `main`, force pushes, `--no-verify` and tag moves. `git push` and `gh pr create` always ask. PR titles must be Conventional Commits. A PR also needs a docs decision from `/claude-docs-check`.
<!-- template: the branch flow, the CI gates by name, what a push to each branch deploys, how to roll back,
and the active hook guards. If the project promotes through several environments, describe the chain
here and in CONTRIBUTING.md appendix B. -->

## Scope
Change only what the task names. Do not fix nearby code or add tests the change does not need. Unrelated problems go in a one-line follow-up note.
