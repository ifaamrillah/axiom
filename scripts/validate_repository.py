#!/usr/bin/env python3
"""Validate Axiom's portable Markdown assets; this is maintainer tooling, not a CLI runtime."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []  # advisory only; never change the exit code
REQUIRED_SKILLS = {
    "axiom-orchestrator", "architecture-design", "code-review", "codebase-exploration",
    "codebase-onboarding", "debugging", "e2e-testing", "implementation", "product-discovery",
    "project-documentation", "release-management", "requirements-analysis", "security-audit",
    "skill-evaluator", "skill-factory", "task-planning", "tdd", "technical-research",
    "testing", "ui-ux-design", "verification-before-completion", "spec-analysis",
    "quality-constraints", "writing-quality", "performance-optimization", "ci-and-observability",
}
SKILL_MAX_LINES = 250
# obra/superpowers caps skills below 20,000 bytes because Claude Code truncates long skills it
# re-attaches after compaction (their finding; not reproduced here). Axiom skills are far below it.
SKILL_MAX_BYTES = 20_000
REQUIRED_WORKFLOWS = {
    "bug-fix", "codebase-onboarding", "feature-development", "performance-audit",
    "refactoring", "release", "security-audit",
}


SKILLS_ROOT = ROOT / ".agents" / "skills"
# Skills-only installs (for example `npx skills`) copy skill directories and nothing else,
# so templates a skill fills are bundled under its assets/. The repository copy stays the
# source; each bundled copy must match it byte for byte. Run with --sync to refresh copies.
BUNDLED_ASSETS = {
    "axiom-orchestrator/assets/handoff.md": "templates/workflows/HANDOFF.md",
    "axiom-orchestrator/assets/workflow-state.md": "templates/workflows/workflow-state.md",
    "axiom-orchestrator/assets/prompts/implementer.md": "agents/prompts/implementer.md",
    "axiom-orchestrator/assets/prompts/task-reviewer.md": "agents/prompts/task-reviewer.md",
    "axiom-orchestrator/assets/prompts/fix-loop.md": "agents/prompts/fix-loop.md",
    "product-discovery/assets/brief.md": "templates/discovery/brief.md",
    "project-documentation/assets/agents-md-block.md": "templates/project/agents-md-block.md",
    "quality-constraints/assets/constitution.md": "templates/project/constitution.md",
    "quality-constraints/assets/constraints.md": "templates/project/constraints.md",
    "quality-constraints/assets/definition-of-done.md": "core/standards/definition-of-done.md",
    "requirements-analysis/assets/spec.md": "templates/specifications/spec.md",
    "requirements-analysis/assets/requirements.md": "templates/specifications/requirements.md",
    "requirements-analysis/assets/change.md": "templates/specifications/change.md",
    "task-planning/assets/PLAN.md": "templates/workflows/PLAN.md",
    "task-planning/assets/TASK.md": "templates/workflows/TASK.md",
    "ui-ux-design/assets/master.md": "templates/design/master.md",
    "ui-ux-design/assets/brief.md": "templates/design/brief.md",
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
        else:
            block = re.search(r"(?ms)^description:(.*?)(?=^[a-z_-]+:|\Z)", front)
            desc_text = " ".join(block.group(1).split()) if block else ""
            if not re.search(r"\bUse (?:when|for|before|during|after|to)\b", desc_text):
                fail(f"{relative}: description needs a trigger clause such as 'Use when ...'")
        if len(parts[2].strip()) < 100:
            fail(f"{relative}: skill body is unexpectedly short")
        line_count = len(text.splitlines())
        if line_count > SKILL_MAX_LINES:
            fail(f"{relative}: {line_count} lines exceeds the {SKILL_MAX_LINES}-line budget; move depth to references/")
        size = len(text.encode("utf-8"))
        if size > SKILL_MAX_BYTES:
            fail(f"{relative}: {size} bytes exceeds the {SKILL_MAX_BYTES}-byte budget; move depth to references/")
        check_reference_reachability(path, text)


def check_reference_reachability(skill_path: Path, skill_text: str) -> None:
    """Every file under a skill's references/ must be linked from SKILL.md or a sibling reference."""
    ref_dir = skill_path.parent / "references"
    if not ref_dir.is_dir():
        return
    corpus = skill_text + "".join(p.read_text(encoding="utf-8") for p in ref_dir.glob("*.md"))
    for ref in sorted(ref_dir.iterdir()):
        if not ref.is_file():
            continue
        linked_from_skill = f"references/{ref.name}" in skill_text
        linked_from_sibling = f"({ref.name}" in corpus or f"({ref.name}#" in corpus
        if not (linked_from_skill or linked_from_sibling):
            fail(f"{ref.relative_to(ROOT).as_posix()}: orphan reference; link it from SKILL.md")


# Advisory: a SKILL.md line that opens with a prohibition ("Don't", "Do not", "Never") and,
# in the same sentence, names a writing style. Prohibitions about how to compose output were
# reported by obra/superpowers to backfire (not measured by Axiom); a positive recipe is the
# suggested rewrite. Prohibitions of one concrete act ("Never run git checkout") do not match.
COMPOSITION_PROHIBITION = re.compile(
    r"^\s*(?:[-*]\s+|\d+\.\s+)?[*_]*(?:don['\u2019]t|do not|never)\b[^.\n]{0,60}?"
    r"\b(?:verbose|wordy|long-winded|lengthy|long|over-?explain\w*|explain\w*|overthink\w*|ramble|elaborate)\b",
    re.IGNORECASE,
)


def phrasing_warnings(text: str) -> list[tuple[int, str]]:
    """Return (line number, line) for lines that look like composition prohibitions."""
    return [(number, line.strip()) for number, line in enumerate(text.splitlines(), 1)
            if COMPOSITION_PROHIBITION.search(line)]


def check_phrasing() -> None:
    for path in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
        for number, line in phrasing_warnings(path.read_text(encoding="utf-8")):
            WARNINGS.append(f"{path.relative_to(ROOT).as_posix()}:{number}: composition prohibition; "
                            f"consider a positive recipe: {line[:100]}")


def check_json() -> None:
    for source in ROOT.rglob("*.json"):
        if ".git" in source.parts or "node_modules" in source.parts:
            continue
        try:
            json.loads(source.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            fail(f"{source.relative_to(ROOT)}: invalid JSON ({error})")


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


FENCE = re.compile(r"(?ms)^[ \t]*(```|~~~).*?^[ \t]*\1[^\n]*$")


def strip_fenced_code(text: str) -> str:
    """Links inside fenced code blocks are not rendered (for example eval transcripts quoting a file)."""
    return FENCE.sub("", text)


def check_local_links() -> None:
    # Inline Markdown links; external URLs and mailto links are not filesystem paths.
    pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
    for source in ROOT.rglob("*.md"):
        if ".git" in source.parts:
            continue
        text = strip_fenced_code(source.read_text(encoding="utf-8"))
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


def check_skill_self_containment() -> None:
    """Links inside a skill must resolve within .agents/skills/; name repository files as plain text."""
    # Inline links and images, plus reference-style definitions such as "[x]: ../path".
    inline = re.compile(r"\[[^\]]*\]\(([^)\s]+)[^)]*\)")
    reference = re.compile(r"(?m)^\s*\[[^\]]+\]:\s*(\S+)")
    for source in SKILLS_ROOT.rglob("*.md"):
        text = source.read_text(encoding="utf-8")
        for target in inline.findall(text) + reference.findall(text):
            target = target.strip().strip("<>").split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (source.parent / target).resolve()
            if SKILLS_ROOT not in resolved.parents:
                fail(f"{source.relative_to(ROOT)}: link '{target}' leaves .agents/skills/ and breaks "
                     "skills-only installs; bundle the file under assets/ or name it as plain text")


def check_bundled_assets(sync: bool) -> None:
    for bundled, source in BUNDLED_ASSETS.items():
        copy, original = SKILLS_ROOT / bundled, ROOT / source
        if not original.is_file():
            fail(f"{source}: bundled asset source missing")
            continue
        if sync:
            copy.parent.mkdir(parents=True, exist_ok=True)
            copy.write_bytes(original.read_bytes())
        elif not copy.is_file() or copy.read_bytes() != original.read_bytes():
            fail(f".agents/skills/{bundled}: differs from {source}; run "
                 "`python3 scripts/validate_repository.py --sync`")


VERSION_RE = r"(\d+\.\d+\.\d+)"


def check_version() -> None:
    """One version in four places (ADR-0005), plus release notes for it."""
    manifest = ROOT / ".claude-plugin" / "plugin.json"
    if not manifest.exists():
        return
    version = json.loads(manifest.read_text(encoding="utf-8")).get("version")
    if not version or not re.fullmatch(VERSION_RE, str(version)):
        fail(".claude-plugin/plugin.json: 'version' must be set as MAJOR.MINOR.PATCH")
        return
    places = {
        ".agents/skills/axiom-orchestrator/references/kernel.md": r"(?m)^# Axiom Kernel \(v" + VERSION_RE + r"\)$",
        "templates/project/agents-md-block.md": r"<!-- axiom:begin v" + VERSION_RE + r" -->",
        "CHANGELOG.md": r"(?m)^## \[" + VERSION_RE + r"\]",
    }
    for relative, pattern in places.items():
        path = ROOT / relative
        found = re.search(pattern, path.read_text(encoding="utf-8")) if path.exists() else None
        if not found:
            fail(f"{relative}: version marker missing (expected v{version})")
        elif found.group(1) != version:
            fail(f"{relative}: version {found.group(1)} does not match plugin.json {version}")
    notes = ROOT / "docs" / "releases" / f"v{version}.md"
    if not notes.exists():
        fail(f"docs/releases/v{version}.md: release notes missing for the current version")


def main() -> int:
    check_bundled_assets(sync="--sync" in sys.argv[1:])
    check_skills()
    check_skill_self_containment()
    check_workflows()
    check_local_links()
    check_json()
    check_version()
    check_phrasing()
    for warning in WARNINGS:
        print(f"WARNING: {warning}")
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
