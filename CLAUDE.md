# claude-ag

Two copy-in Claude Code templates: `backend-python/` and `frontend-typescript/`. Each holds a `.claude/` directory, a templated `CLAUDE.md` and `CONTRIBUTING.md`, a `.gitignore` block and example files. `README.md` is the adoption guide and the token list.

## Rules for editing the templates
- Generic only. No product, company, vendor integration, hostname, colleague name or dated in-flight state anywhere under the template folders. `tests/test_structure.py` fails on a list of forbidden words; extend the list when you strip a new one.
- Values a repo must supply are `{{UPPER_SNAKE}}` tokens in `CLAUDE.md` and `CONTRIBUTING.md` only. Hook parameters live in the `# --- config ---` block at the top of each script. Add a new token to the table in `README.md` in the same change.
- Guidance for the adopter goes in `<!-- template: -->` HTML comments; Claude Code strips them before the model sees the file. The non-comment part of every `CLAUDE.md` stays under 200 lines.
- The shared files listed in `tests/test_structure.py` are byte-identical across both templates. Edit one, copy to the other, run the tests.
- Hooks are Python 3.10+, standard library only, and read Claude Code's hook payload from stdin. Every behaviour change gets a case in `tests/test_hooks.py`.
- Section numbers in `CONTRIBUTING.md` are load-bearing: `CLAUDE.md` and the hooks' `SECTION_REF` strings cite §1, §8 and §12. Keep them when you edit.

## Commands
```bash
python3 -m unittest discover tests -v    # what "done" means here; needs git, uvx and bunx for the full run
```

## Scope
Change only what the task names. Unrelated problems go in a one-line follow-up note.
