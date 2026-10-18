#!/usr/bin/env python3
"""PostToolUse hook for Edit, Write, MultiEdit and NotebookEdit. Lints the edited file and reports findings on the lines that changed.

Python: `uvx ruff check` isolated with the E, F and ANN rule sets, minus E501. TypeScript: `bunx oxlint` with the repo's config.
Report only: it never rewrites the file and never blocks (the edit already happened). Exit 2 sends the findings to Claude.
Findings are limited to lines that differ from HEAD; a new file is checked whole. A missing tool keeps the hook quiet.
Whole-project gates (type checks, `bun run check`, the test suite) do not run here; `/verify` runs them.
"""
import json
import os
import re
import subprocess
import sys

Finding = tuple[int, int, str, str]

HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def ruff(root: str, path: str) -> list[Finding]:
    """Run ruff on one file and return (row, col, code, message) tuples."""
    run = subprocess.run(
        ["uvx", "ruff", "check", "--quiet", "--isolated", "--select", "E,F,ANN", "--ignore", "E501", "--output-format", "json", path],
        cwd=root, capture_output=True, text=True, timeout=75,
    )
    return [(f["location"]["row"], f["location"]["column"], f["code"], f["message"]) for f in json.loads(run.stdout or "[]")]


def oxlint(root: str, path: str) -> list[Finding]:
    """Run oxlint on one file and return (row, col, code, message) tuples."""
    run = subprocess.run(["bunx", "oxlint", "--format", "json", path], cwd=root, capture_output=True, text=True, timeout=80)
    raw = json.loads(run.stdout or "{}")
    diagnostics = raw.get("diagnostics", []) if isinstance(raw, dict) else raw
    out: list[Finding] = []
    for d in diagnostics:
        span = (d.get("labels") or [{}])[0].get("span") or {}
        out.append((span.get("line") or 0, span.get("column") or 0, d.get("code") or "error", d.get("message", "")))
    return out


def eslint(root: str, path: str) -> list[Finding]:
    """Run eslint on one file and return (row, col, code, message) tuples. Swap into LINTERS for an eslint repo."""
    run = subprocess.run(["bunx", "eslint", "--format", "json", path], cwd=root, capture_output=True, text=True, timeout=80)
    out: list[Finding] = []
    for f in json.loads(run.stdout or "[]"):
        for m in f.get("messages", []):
            out.append((m.get("line") or 0, m.get("column") or 0, m.get("ruleId") or "error", m.get("message", "")))
    return out


# --- config ---------------------------------------------------------------
SKIP = (".venv/", "node_modules/", "dist/", "build/", "_temp/", "_ignore/")
LINTERS = {".py": ruff, ".ts": oxlint, ".tsx": oxlint}  # eslint repos: {".ts": eslint, ".tsx": eslint}
# --------------------------------------------------------------------------


def changed_lines(root: str, rel: str) -> set[int] | None:
    """Line numbers that differ from HEAD, or None when the whole file counts."""
    try:
        if subprocess.run(["git", "-C", root, "ls-files", "--error-unmatch", rel], capture_output=True, timeout=10).returncode != 0:
            return None
        diff = subprocess.run(["git", "-C", root, "diff", "-U0", "HEAD", "--", rel], capture_output=True, text=True, timeout=10).stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    lines: set[int] = set()
    for m in (HUNK_RE.match(line) for line in diff.splitlines()):
        if m:
            start, count = int(m.group(1)), int(m.group(2) or 1)
            lines.update(range(start, start + max(count, 1)))
    return lines


def main() -> None:
    """Read the hook payload, lint the file, report on stderr with exit 2."""
    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        sys.exit(0)
    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    root = payload.get("cwd") or os.getcwd()
    rel = os.path.relpath(path, root) if os.path.isabs(path) else path
    if rel.startswith(SKIP) or not os.path.isfile(path):
        sys.exit(0)
    linter = LINTERS.get(os.path.splitext(rel)[1])
    if linter is None:
        sys.exit(0)
    try:
        findings = linter(root, path)
    except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError, KeyError, TypeError):
        sys.exit(0)
    keep = changed_lines(root, rel)
    rows = [f for f in findings if keep is None or f[0] in keep]
    if not rows:
        sys.exit(0)
    scope = "whole file (new)" if keep is None else "changed lines only"
    body = "\n".join(f"{rel}:{r}:{c}: {code} {msg}" for r, c, code, msg in rows[:40])
    more = f"\n... {len(rows) - 40} more" if len(rows) > 40 else ""
    print(f"lint findings in {rel}, {scope} (report only, fix what applies):\n{body}{more}", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
