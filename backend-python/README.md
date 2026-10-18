# backend-python

Claude Code setup for a Python service: FastAPI, Pydantic, SQLAlchemy with alembic, pytest, ruff, uv.

What is in here:

- `.claude/settings.json`: committed permissions and hook wiring.
- `.claude/hooks/`: six Python hooks (branch and tag protection, `.env` and secrets protection, PR title check, docs-decision check, per-file lint).
- `.claude/rules/`: three rules that always load (working agreement, coding standards, git and PRs) and three path-scoped ones (python, testing, database).
- `.claude/agents/`: `reviewer` and `docs-keeper`.
- `.claude/skills/`: `repo-sync`, `verify`, `claude-docs-check` (with its `map.json`), `raise-pr`.
- `CLAUDE.md` and `CONTRIBUTING.md`: templates with `{{TOKENS}}` and `<!-- template: -->` guidance.
- `.gitignore`: the block to append. `.mcp.json.example` and `.claude/settings.local.json.example`: optional.

## Adopt it

1. Copy this folder's contents into the repo root. `cp -R backend-python/. <repo>/` keeps the dotfiles.
2. Fill every `{{TOKEN}}` in `CLAUDE.md` and `CONTRIBUTING.md`. `grep -rn '{{' CLAUDE.md CONTRIBUTING.md` must come back empty. The root README of this repo lists every token.
3. Set the config block at the top of each hook if the defaults do not fit: `PROTECTED` and `BASE` in `branch-protection.py`, `ALLOWED_TYPES` in `pr-title.py`, `SKIP` and `LINTERS` in `lint.py`.
4. Edit `.claude/skills/claude-docs-check/map.json` so its `paths` match the repo's real files.
5. Append `.gitignore` to the repo's `.gitignore`. Rename `.mcp.json.example` to `.mcp.json` if you want the docs and GitHub MCP servers, and `settings.local.json.example` to `settings.local.json` to enable them for yourself.
6. Run `claude` in the repo, then `/doctor`. Type `/` and check that `repo-sync`, `verify`, `claude-docs-check` and `raise-pr` are listed.
7. Delete or keep the `<!-- template: -->` comments. Claude Code strips them before the model sees the file; they cost nothing.

Multi-environment promotion (dev → staging → prod) is described in `CONTRIBUTING.md` appendix B with the hook and skill changes it needs.
