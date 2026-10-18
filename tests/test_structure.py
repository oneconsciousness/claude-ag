"""Structural checks on both templates: JSON, frontmatter, forbidden words, length budgets, cross-template sync."""
import json
import os
import py_compile
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ("backend-python", "frontend-typescript")

# Files that must be byte-identical in both templates.
SHARED = (
    ".claude/hooks/branch-protection.py",
    ".claude/hooks/env-protection.py",
    ".claude/hooks/secrets-protection.py",
    ".claude/hooks/pr-title.py",
    ".claude/hooks/docs-check.py",
    ".claude/hooks/lint.py",
    ".claude/agents/docs-keeper.md",
    ".claude/rules/working-agreement.md",
    ".claude/rules/git-and-prs.md",
    ".claude/skills/raise-pr/SKILL.md",
    ".claude/skills/repo-sync/SKILL.md",
    ".claude/skills/claude-docs-check/SKILL.md",
    ".claude/settings.local.json.example",
    ".mcp.json.example",
    ".gitignore",
)

# Product, vendor, infrastructure and person names that must never appear in a template.
FORBIDDEN = re.compile(
    r"(?i)\b(hubspot|sara|aol|aolf|artofliving|art of living|the-art-of-living|qdrant|openai realtime|"
    r"realtime api|cloudfront|fargate|ecs|aol_schemas|arun|swapnil|akshat|aolf\.app)\b"
)

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
COMMENT = re.compile(r"<!--.*?-->", re.S)


def files_under(path: Path) -> list[Path]:
    """Every regular file under path, skipping caches."""
    return [p for p in path.rglob("*") if p.is_file() and "__pycache__" not in p.parts]


def frontmatter(path: Path) -> dict[str, str]:
    """Top-level `key: value` pairs of a markdown file's YAML frontmatter, or {} without one."""
    m = FRONTMATTER.match(path.read_text())
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if line and not line.startswith((" ", "-")) and ":" in line:
            key, _, value = line.partition(":")
            out[key.strip()] = value.strip()
    return out


class Json(unittest.TestCase):
    """Every JSON file parses and settings reference real hooks."""

    def test_json_files_parse(self) -> None:
        for t in TEMPLATES:
            for rel in (".claude/settings.json", ".claude/settings.local.json.example", ".claude/skills/claude-docs-check/map.json", ".mcp.json.example"):
                with self.subTest(template=t, file=rel):
                    json.loads((ROOT / t / rel).read_text())

    def test_settings_hooks_exist_and_are_wired(self) -> None:
        for t in TEMPLATES:
            settings = json.loads((ROOT / t / ".claude" / "settings.json").read_text())
            referenced: set[str] = set()
            for event in settings["hooks"].values():
                for entry in event:
                    for hook in entry["hooks"]:
                        m = re.search(r"/\.claude/hooks/([a-z-]+\.py)", hook["command"])
                        self.assertIsNotNone(m, hook["command"])
                        referenced.add(m.group(1))
            on_disk = {p.name for p in (ROOT / t / ".claude" / "hooks").glob("*.py")}
            self.assertEqual(referenced, on_disk, f"{t}: settings.json and hooks/ disagree")

    def test_map_json_shape(self) -> None:
        for t in TEMPLATES:
            spec = json.loads((ROOT / t / ".claude" / "skills" / "claude-docs-check" / "map.json").read_text())
            self.assertEqual(spec["base"], "main")
            self.assertIn(".claude/", spec["artifact_prefixes"])
            for trigger in spec["triggers"]:
                self.assertTrue(trigger["paths"] and trigger["artifacts"])


class Hooks(unittest.TestCase):
    """Hooks compile and declare their config block."""

    def test_compile(self) -> None:
        for t in TEMPLATES:
            for p in (ROOT / t / ".claude" / "hooks").glob("*.py"):
                with self.subTest(template=t, hook=p.name):
                    py_compile.compile(str(p), doraise=True)

    def test_config_blocks(self) -> None:
        expected = {
            "branch-protection.py": ("PROTECTED", "BASE", "SECTION_REF", "TAG_RE"),
            "pr-title.py": ("ALLOWED_TYPES",),
            "docs-check.py": ("DEFAULT_BASE",),
            "lint.py": ("SKIP", "LINTERS"),
        }
        for t in TEMPLATES:
            for hook, names in expected.items():
                text = (ROOT / t / ".claude" / "hooks" / hook).read_text()
                self.assertIn("# --- config ---", text, f"{t}/{hook}")
                for name in names:
                    self.assertIsNotNone(re.search(rf"^{name} = ", text, re.M), f"{t}/{hook} lacks {name}")


class Markdown(unittest.TestCase):
    """Agents, skills and rules carry the frontmatter Claude Code expects."""

    def test_agents(self) -> None:
        for t in TEMPLATES:
            for p in (ROOT / t / ".claude" / "agents").glob("*.md"):
                fm = frontmatter(p)
                self.assertEqual(fm.get("name"), p.stem, p)
                self.assertTrue(fm.get("description"), p)
                self.assertTrue(fm.get("tools"), p)

    def test_skills(self) -> None:
        for t in TEMPLATES:
            for p in (ROOT / t / ".claude" / "skills").glob("*/SKILL.md"):
                fm = frontmatter(p)
                self.assertEqual(fm.get("name"), p.parent.name, p)
                self.assertTrue(fm.get("description"), p)

    def test_rules(self) -> None:
        unscoped = {"working-agreement.md", "coding-standards.md", "git-and-prs.md"}
        for t in TEMPLATES:
            for p in (ROOT / t / ".claude" / "rules").glob("*.md"):
                fm = frontmatter(p)
                if p.name in unscoped:
                    self.assertEqual(fm, {}, f"{p} should load unconditionally")
                else:
                    self.assertIn("paths", fm, f"{p} needs a paths: list")
                    self.assertRegex(p.read_text(), r'paths:\n(  - ".+"\n)+', p)

    def test_claude_md_length(self) -> None:
        for t in TEMPLATES:
            for p in (ROOT / t).rglob("CLAUDE.md"):
                body = COMMENT.sub("", p.read_text())
                lines = [line for line in body.splitlines() if line.strip()]
                self.assertLessEqual(len(lines), 200, p)

    def test_tokens_only_in_templates(self) -> None:
        for t in TEMPLATES:
            for p in files_under(ROOT / t / ".claude"):
                self.assertNotIn("{{", p.read_text(), f"{p} carries a {{{{TOKEN}}}}; hook config belongs in the config block")

    def test_tokens_are_documented(self) -> None:
        readme = (ROOT / "README.md").read_text()
        for t in TEMPLATES:
            for p in files_under(ROOT / t):
                if p.suffix != ".md":
                    continue
                for token in set(re.findall(r"\{\{[A-Z_]+\}\}", p.read_text())) - {"{{TOKEN}}", "{{TOKENS}}", "{{UPPER_SNAKE}}"}:
                    self.assertIn(token, readme, f"{token} in {p} is not in the README token table")


class Generic(unittest.TestCase):
    """No product, vendor or person names under the templates or docs."""

    def test_forbidden_words(self) -> None:
        for base in (*TEMPLATES, "docs"):
            for p in files_under(ROOT / base):
                for n, line in enumerate(p.read_text().splitlines(), 1):
                    m = FORBIDDEN.search(line)
                    self.assertIsNone(m, f"{p}:{n}: {m.group(0) if m else ''}")

    def test_no_secrets_or_personal_paths(self) -> None:
        pattern = re.compile(r"(sk-[A-Za-z0-9]{10,}|ghp_[A-Za-z0-9]{10,}|/Users/[a-z]+/|AKIA[0-9A-Z]{16})")
        for base in (*TEMPLATES, "docs", "README.md", "CLAUDE.md"):
            path = ROOT / base
            for p in (files_under(path) if path.is_dir() else [path]):
                self.assertIsNone(pattern.search(p.read_text()), p)


class Sync(unittest.TestCase):
    """Shared files are byte-identical across the two templates."""

    def test_shared_files_identical(self) -> None:
        a, b = (ROOT / t for t in TEMPLATES)
        for rel in SHARED:
            with self.subTest(file=rel):
                self.assertEqual((a / rel).read_bytes(), (b / rel).read_bytes(), f"{rel} differs between templates")

    def test_same_skill_and_agent_sets(self) -> None:
        a, b = (ROOT / t for t in TEMPLATES)
        self.assertEqual({p.name for p in (a / ".claude" / "agents").iterdir()}, {p.name for p in (b / ".claude" / "agents").iterdir()})
        self.assertEqual({p.name for p in (a / ".claude" / "skills").iterdir()}, {p.name for p in (b / ".claude" / "skills").iterdir()})
        self.assertEqual({p.name for p in (a / ".claude" / "hooks").iterdir() if p.suffix == ".py"}, {p.name for p in (b / ".claude" / "hooks").iterdir() if p.suffix == ".py"})


if __name__ == "__main__":
    unittest.main()
