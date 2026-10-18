# Git and pull requests

## Branches
- Work on a branch off `main`: `feature/<name>`, `fix/<name>`, `chore/<name>`, `docs/<name>`, `refactor/<name>`, `perf/<name>`, `test/<name>`. Lowercase, hyphens, no personal names.
- Never commit on `main`. Never force-push a shared branch. Never `--no-verify`. A hook blocks all three.
- Releases are `vX.Y.Z` tags on `main`. A tag is never moved or deleted; a wrong tag is fixed by cutting the next version. A hook blocks tag moves.

## Commits
- One logical change per commit. Conventional Commits: `type(scope): subject`. Types: feat, fix, chore, docs, refactor, perf, test, ci, build, revert, release. Subject starts lowercase, no trailing period, imperative mood.
- The body says why, not what.
- Add `Refs: #<issue>`, `Refs: discussion #<n>` or `Refs: docs/plans/<file>.md` when there is one.

## Pull requests
- Run `/raise-pr`. It shows the card (title, branch, base, assignee, summary) and waits for a yes.
- The title follows the commit format. A hook blocks titles that do not.
- Assignee is the human whose git identity is on the commits. No reviewers unless the human names them. No label.
- Description: what, why, how to test, risks and rollback. Link sources instead of restating them.
- Merge: squash-and-merge. The reviewer has the final call.
- `git push` and `gh pr create` always ask before running. That is intended.
