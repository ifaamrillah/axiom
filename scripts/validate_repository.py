#!/usr/bin/env python3
"""Validate Axiom's portable Markdown assets; this is maintainer tooling, not a CLI runtime."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
REQUIRED_SKILLS = {
    "axiom-orchestrator", "architecture-design", "code-review", "codebase-exploration",
    "codebase-onboarding", "debugging", "e2e-testing", "implementation", "product-discovery",
    "project-documentation", "release-management", "requirements-analysis", "security-audit",
    "skill-evaluator", "skill-factory", "task-planning", "tdd", "technical-research",
    "testing", "ui-ux-design",
}
REQUIRED_WORKFLOWS = {
    "bug-fix", "codebase-onboarding", "feature-development", "performance-audit",
    "refactoring", "release", "security-audit",
}


def fail(message: str) -> None:
    ERRORS.append(message)


def check_skills() -> None:
    skill_files = sorted((ROOT / ".agents/skills").glob("*/SKILL.md"))
    if not skill_files:
        fail("No canonical skills found under .agents/skills/*/SKILL.md")
    seen: set[str] = set()
    found = {path.parent.name for path in skill_files}
    for missing in sorted(REQUIRED_SKILLS - found):
        fail(f"Missing required lifecycle skill: {missing}")
    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT).as_posix()
        if not text.startswith("---\n"):
            fail(f"{relative}: missing YAML frontmatter")
            continue
        parts = text.split("---\n", 2)
        if len(parts) < 3:
            fail(f"{relative}: unterminated YAML frontmatter")
            continue
        front = parts[1]
        name = re.search(r"(?m)^name:\s*([^\n#]+)\s*$", front)
        desc = re.search(r"(?m)^description:\s*(?:>|\|)?\s*(?:\n|\S)", front)
        if not name:
            fail(f"{relative}: required frontmatter field 'name' missing")
        else:
            value = name.group(1).strip().strip("\"'")
            if value != path.parent.name:
                fail(f"{relative}: name '{value}' must match directory '{path.parent.name}'")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
                fail(f"{relative}: name must be lowercase kebab-case")
            if value in seen:
                fail(f"{relative}: duplicate skill name '{value}'")
            seen.add(value)
        if not desc:
            fail(f"{relative}: required frontmatter field 'description' missing")
        if len(parts[2].strip()) < 100:
            fail(f"{relative}: skill body is unexpectedly short")


def check_workflows() -> None:
    workflow_files = sorted((ROOT / "workflows").glob("*/WORKFLOW.md"))
    if not workflow_files:
        fail("No Markdown workflows found")
    found = {path.parent.name for path in workflow_files}
    for missing in sorted(REQUIRED_WORKFLOWS - found):
        fail(f"Missing required workflow: {missing}")
    for path in workflow_files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        if not text.startswith("# ") or "workflow" not in text.splitlines()[0].lower():
            fail(f"{rel}: first heading should identify a workflow")
        if len(text.splitlines()) < 8:
            fail(f"{rel}: workflow needs purpose/stage/gate guidance")
        lower = text.lower()
        for concept in ("metadata", "trigger", "inputs", "stage", "dependenc", "parallel", "quality", "recovery", "completion", "state"):
            if concept not in lower:
                fail(f"{rel}: missing {concept} guidance")
        stage_matches = list(re.finditer(r"(?m)^(?:###\s+\d+\.|\d+\.\s+\*\*)", text))
        if not stage_matches:
            fail(f"{rel}: stages must be an ordered list with named stages")
        for index, match in enumerate(stage_matches):
            end = stage_matches[index + 1].start() if index + 1 < len(stage_matches) else len(text)
            section = text[match.start():end].lower()
            label = text[match.start():text.find("\n", match.start())][:90]
            if "depend" not in section:
                fail(f"{rel}: stage lacks an explicit dependency: {label}")
            if "output" not in section:
                fail(f"{rel}: stage lacks an explicit output: {label}")
    for canonical in ("codebase-onboarding", "feature-development", "bug-fix", "refactoring", "security-audit", "performance-audit", "release"):
        if not (ROOT / "workflows" / canonical / "WORKFLOW.md").exists():
            fail(f"Missing required lifecycle workflow: {canonical}")


def check_local_links() -> None:
    # Inline Markdown links; external URLs and mailto links are not filesystem paths.
    pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
    for source in ROOT.rglob("*.md"):
        if ".git" in source.parts:
            continue
        text = source.read_text(encoding="utf-8")
        for target in pattern.findall(text):
            target = target.strip().strip("<>")
            if not target or target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue
            resolved = (source.parent / target).resolve()
            if not resolved.exists():
                fail(f"{source.relative_to(ROOT)}: broken local link '{target}'")


def main() -> int:
    check_skills()
    check_workflows()
    check_local_links()
    if ERRORS:
        for error in ERRORS:
            print(f"ERROR: {error}")
        print(f"Validation failed with {len(ERRORS)} error(s).")
        return 1
    skill_count = len(list((ROOT / ".agents/skills").glob("*/SKILL.md")))
    workflow_count = len(list((ROOT / "workflows").glob("*/WORKFLOW.md")))
    markdown_count = len(list(ROOT.rglob("*.md")))
    print(f"Validation passed: {skill_count} skills, {workflow_count} workflows, {markdown_count} Markdown files; local links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
