#!/usr/bin/env python3
"""Maintainer tooling for Axiom skill evaluations.

Not a user-facing CLI and not a workflow runtime (see ADR-0004). It parses the
Markdown cases in evaluations/cases/, checks them structurally, and can run
trigger cases headlessly against a host that the maintainer has installed and
authenticated. Results are written as Markdown evidence under evaluations/results/.

Usage:
  python3 scripts/run_evals.py --check
  python3 scripts/run_evals.py --list
  python3 scripts/run_evals.py --host claude-code --kind trigger [--skill NAME] [--model M] [--dry-run]
  python3 scripts/run_evals.py --host claude-code --kind behavior --skill NAME [--dry-run]

Running cases invokes the host and spends the maintainer's model quota. Use
--dry-run to print the commands without running them.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = ROOT / "evaluations" / "cases"
RESULTS_DIR = ROOT / "evaluations" / "results"
SKILLS_DIR = ROOT / ".agents" / "skills"
SUPPORTED_HOSTS = ("claude-code",)


@dataclass
class Behavior:
    case_id: str
    title: str
    prompt: str = ""
    fixture: str = ""
    expect: list[str] = field(default_factory=list)
    fail_if: list[str] = field(default_factory=list)


@dataclass
class CaseFile:
    path: Path
    skill: str
    fixture: str = ""
    positive: list[str] = field(default_factory=list)
    negative: list[tuple[str, str]] = field(default_factory=list)
    behaviors: list[Behavior] = field(default_factory=list)


def _section(text: str, heading: str) -> str:
    match = re.search(rf"(?ms)^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", text)
    return match.group(1) if match else ""


def _bullets(block: str) -> list[str]:
    return [line[2:].strip() for line in block.splitlines() if line.startswith("- ")]


def parse_case(path: Path) -> CaseFile:
    text = path.read_text(encoding="utf-8")
    front = re.match(r"(?s)^---\n(.*?)\n---\n", text)
    skill = ""
    if front:
        found = re.search(r"(?m)^skill:\s*([a-z0-9-]+)\s*$", front.group(1))
        skill = found.group(1) if found else ""
        fixture_match = re.search(r"(?m)^fixture:\s*(\S+)\s*$", front.group(1))
        fixture = fixture_match.group(1) if fixture_match else ""
    else:
        fixture = ""
    case = CaseFile(path=path, skill=skill, fixture=fixture)
    case.positive = [_strip_quotes(b) for b in _bullets(_section(text, "Should trigger"))]
    for bullet in _bullets(_section(text, "Should not trigger")):
        prompt, _, owner = bullet.partition("→")
        case.negative.append((_strip_quotes(prompt.strip()), owner.strip().strip("`")))
    behavior_block = _section(text, "Behavior")
    for match in re.finditer(r"(?ms)^### ([A-Za-z0-9_-]+):\s*(.+?)\n(.*?)(?=^### |\Z)", behavior_block):
        behavior = Behavior(case_id=match.group(1), title=match.group(2).strip())
        for bullet in _bullets(match.group(3)):
            key, _, value = bullet.partition(":")
            key, value = key.strip().lower(), value.strip()
            if key == "prompt":
                behavior.prompt = _strip_quotes(value)
            elif key == "fixture":
                behavior.fixture = value.strip("`")
            elif key == "expect":
                behavior.expect.append(value)
            elif key == "fail if":
                behavior.fail_if.append(value)
        case.behaviors.append(behavior)
    return case


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def load_cases() -> list[CaseFile]:
    return [parse_case(p) for p in sorted(CASES_DIR.glob("*.md")) if p.name != "README.md"]


def check(cases: list[CaseFile]) -> list[str]:
    errors: list[str] = []
    skills = {p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md")}
    for case in cases:
        rel = case.path.relative_to(ROOT).as_posix()
        if not case.skill:
            errors.append(f"{rel}: frontmatter 'skill:' missing")
            continue
        if case.fixture and not (ROOT / case.fixture).exists():
            errors.append(f"{rel}: trigger fixture missing: {case.fixture}")
        if case.skill not in skills:
            errors.append(f"{rel}: unknown skill '{case.skill}'")
        if case.path.stem != case.skill:
            errors.append(f"{rel}: file name must match skill '{case.skill}'")
        if len(case.positive) < 2:
            errors.append(f"{rel}: needs at least 2 'Should trigger' prompts")
        if len(case.negative) < 1:
            errors.append(f"{rel}: needs at least 1 'Should not trigger' prompt")
        for prompt, owner in case.negative:
            if not owner:
                errors.append(f"{rel}: negative prompt lacks '→ owner': {prompt[:50]}")
            elif owner != "none" and owner not in skills:
                errors.append(f"{rel}: negative owner '{owner}' is not a skill")
        if not case.behaviors:
            errors.append(f"{rel}: needs at least 1 Behavior case")
        for behavior in case.behaviors:
            if not behavior.prompt or not behavior.expect:
                errors.append(f"{rel}: behavior {behavior.case_id} needs Prompt and Expect")
            if behavior.fixture and not (ROOT / behavior.fixture).exists():
                errors.append(f"{rel}: behavior {behavior.case_id} fixture missing: {behavior.fixture}")
    return errors


KERNEL = SKILLS_DIR / "axiom-orchestrator" / "references" / "kernel.md"


def kernel_block() -> str:
    """Behavior, Routing, and Proportionality sections, as the project-instructions block installs them."""
    text = KERNEL.read_text(encoding="utf-8")
    start = text.index("## Behavior")
    end = text.index("## Project facts")
    return "<!-- axiom:begin -->\n# Axiom\n\n" + text[start:end].rstrip() + "\n<!-- axiom:end -->\n"


def prepare_workspace(fixture: str, kernel: bool = True) -> Path:
    """Create an isolated project: optional fixture copy, skills in the host path, and,
    by default, the kernel in the project instructions files as a documented install does."""
    workdir = Path(tempfile.mkdtemp(prefix="axiom-eval-"))
    if fixture:
        shutil.copytree(ROOT / fixture, workdir, dirs_exist_ok=True)
    shutil.copytree(SKILLS_DIR, workdir / ".claude" / "skills")
    shutil.copytree(SKILLS_DIR, workdir / ".agents" / "skills")
    if kernel:
        block = kernel_block()
        for name in ("CLAUDE.md", "AGENTS.md"):
            (workdir / name).write_text(block, encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=workdir, check=False)
    return workdir


# Trigger runs only need to observe the first skill decision: read-only tools plus Skill.
TRIGGER_TOOLS = "Skill,Read,Glob,Grep"
# Behavior runs work inside a disposable fixture copy; shell access is limited to test commands.
BEHAVIOR_ALLOWED = ["Skill", "Read", "Glob", "Grep", "Edit", "Write",
                    "Bash(python3 -m unittest:*)", "Bash(python3 -c:*)", "Bash(git status:*)",
                    "Bash(git diff:*)", "Bash(ls:*)"]


def host_command(host: str, prompt: str, model: str | None, max_turns: int,
                 kind: str = "trigger", budget: float | None = None,
                 isolate: bool = True) -> list[str]:
    if host != "claude-code":
        raise SystemExit(f"Host '{host}' is not supported yet; supported: {', '.join(SUPPORTED_HOSTS)}")
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--max-turns", str(max_turns)]
    if isolate:
        # Skip the maintainer's user-level settings (personal hooks, plugins, permissions)
        # so results reflect Axiom plus the host, not one machine's customizations.
        cmd += ["--setting-sources", "project,local"]
    if kind == "trigger":
        cmd += ["--tools", TRIGGER_TOOLS]
    else:
        cmd += ["--permission-mode", "acceptEdits", "--allowedTools", *BEHAVIOR_ALLOWED]
    if budget:
        cmd += ["--max-budget-usd", str(budget)]
    if model:
        cmd += ["--model", model]
    return cmd


def run_completed(stream: str) -> bool:
    """True when the host produced a final result event (including max-turn stops)."""
    for line in stream.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict) and event.get("type") == "result":
            return True
    return False


def invoked_skills(stream: str) -> list[str]:
    """Extract skill names from Claude Code stream-json tool_use blocks named 'Skill'."""
    names: list[str] = []
    for line in stream.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = event.get("message") if isinstance(event, dict) else None
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                skill = str((block.get("input") or {}).get("skill", ""))
                names.append(skill.split(":")[-1])
    return names


def run_host(cmd: list[str], cwd: Path, timeout: int) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout + proc.stderr
    except FileNotFoundError:
        return 127, f"host executable not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s"


def run_triggers(cases: list[CaseFile], args: argparse.Namespace) -> list[str]:
    rows: list[str] = []
    for case in cases:
        items = [(p, True, case.skill) for p in case.positive] + [(p, False, o) for p, o in case.negative]
        for prompt, should, owner in items:
            cmd = host_command(args.host, prompt, args.model, args.max_turns, "trigger",
                               args.budget, not args.no_isolate)
            if args.dry_run:
                print(" ".join(cmd[:2]) + f" {json.dumps(prompt)} " + " ".join(cmd[3:]))
                continue
            workdir = prepare_workspace(case.fixture, not args.no_kernel)
            code, out = run_host(cmd, workdir, args.timeout)
            shutil.rmtree(workdir, ignore_errors=True)
            used = invoked_skills(out)
            hit = case.skill in used
            if not used and not run_completed(out):
                verdict = f"error (exit {code})"
            else:
                verdict = "pass" if hit == should else "fail"
            rows.append(f"| {case.skill} | {'+' if should else '−'} | {prompt[:70]} | "
                        f"{owner} | {', '.join(used) or '—'} | {verdict} |")
            print(rows[-1])
    return rows


def run_behaviors(cases: list[CaseFile], args: argparse.Namespace) -> list[str]:
    sections: list[str] = []
    for case in cases:
        for behavior in case.behaviors:
            cmd = host_command(args.host, behavior.prompt, args.model, args.max_turns, "behavior",
                               args.budget, not args.no_isolate)
            if args.dry_run:
                print(f"[{case.skill}/{behavior.case_id}] fixture={behavior.fixture or 'none'} "
                      f"claude -p {json.dumps(behavior.prompt)[:80]}…")
                continue
            workdir = prepare_workspace(behavior.fixture, not args.no_kernel)
            code, out = run_host(cmd, workdir, args.timeout)
            shutil.rmtree(workdir, ignore_errors=True)
            final = _final_text(out)
            checks = "\n".join(f"- [ ] {e}" for e in behavior.expect)
            fails = "\n".join(f"- [ ] (must be false) {f}" for f in behavior.fail_if) or "- none listed"
            trace = "\n".join(f"{i}. {c}" for i, c in enumerate(tool_trace(out), 1)) or "(no tool calls)"
            sections.append(
                f"### {case.skill}/{behavior.case_id}: {behavior.title}\n\n"
                f"- Exit code: {code}\n- Skills invoked: {', '.join(invoked_skills(out)) or 'none'}\n\n"
                f"Tool calls in order:\n\n```text\n{trace}\n```\n\n"
                f"Expectations (grade by reading the transcript):\n\n{checks}\n\nFailure signals:\n\n{fails}\n\n"
                f"Final answer:\n\n```text\n{final[:4000]}\n```\n")
            print(f"ran {case.skill}/{behavior.case_id}: exit {code}")
    return sections


def tool_trace(stream: str, limit: int = 60) -> list[str]:
    """Ordered tool calls (name + short input) so graders can check sequencing claims."""
    calls: list[str] = []
    for line in stream.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = event.get("message") if isinstance(event, dict) else None
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, list) or event.get("type") != "assistant":
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                data = block.get("input") or {}
                detail = data.get("command") or data.get("file_path") or data.get("skill") or data.get("pattern") or ""
                calls.append(f"{block.get('name')}: {str(detail)[:120]}")
    return calls[:limit]


def _final_text(stream: str) -> str:
    for line in reversed(stream.splitlines()):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict) and event.get("type") == "result":
            return str(event.get("result", ""))
    return stream[-4000:]


def host_version(host: str) -> str:
    code, out = run_host(["claude", "--version"], ROOT, 30) if host == "claude-code" else (1, "")
    return out.strip() if code == 0 else "unknown"


def write_results(kind: str, args: argparse.Namespace, body: str) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d-%H%M")
    path = RESULTS_DIR / f"{stamp}-{args.host}-{kind}.md"
    n = 2
    while path.exists():  # several runs can finish within one minute; never overwrite a record
        path = RESULTS_DIR / f"{stamp}-{args.host}-{kind}-{n}.md"
        n += 1
    header = (f"# Eval run: {kind} on {args.host}\n\n"
              f"- Date: {dt.datetime.now().isoformat(timespec='minutes')}\n"
              f"- Host version: {host_version(args.host)}\n- Model: {args.model or 'host default'}\n"
              f"- Skill filter: {args.skill or 'all'}\n- Max turns: {args.max_turns}\n"
              f"- Isolation: {'user settings excluded' if not args.no_isolate else 'user settings loaded'}\n"
              f"- Kernel in project instructions: {'no' if args.no_kernel else 'yes'}\n"
              f"- Per-run budget cap (USD): {args.budget or 'none'}\n"
              f"- Runner: scripts/run_evals.py\n\n")
    path.write_text(header + body, encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="validate case files only")
    parser.add_argument("--list", action="store_true", help="list cases")
    parser.add_argument("--host", choices=SUPPORTED_HOSTS)
    parser.add_argument("--kind", choices=("trigger", "behavior"), default="trigger")
    parser.add_argument("--skill")
    parser.add_argument("--model")
    parser.add_argument("--max-turns", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--budget", type=float, default=0.5,
                        help="per-run spend cap in USD passed to the host (0 disables)")
    parser.add_argument("--no-isolate", action="store_true",
                        help="also load the maintainer's user-level host settings")
    parser.add_argument("--no-kernel", action="store_true",
                        help="omit the kernel block from CLAUDE.md/AGENTS.md (measure skills alone)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cases = load_cases()
    errors = check(cases)
    if args.check or not args.host:
        if args.list:
            for case in cases:
                print(f"{case.skill}: {len(case.positive)} positive, {len(case.negative)} negative, "
                      f"{len(case.behaviors)} behavior")
        for error in errors:
            print(f"ERROR: {error}")
        if errors:
            print(f"Eval case check failed with {len(errors)} error(s).")
            return 1
        print(f"Eval case check passed: {len(cases)} case files.")
        return 0
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.skill:
        cases = [c for c in cases if c.skill == args.skill]
        if not cases:
            print(f"No cases for skill '{args.skill}'.")
            return 1
    if args.kind == "trigger":
        rows = run_triggers(cases, args)
        if args.dry_run:
            return 0
        passed = sum(1 for r in rows if r.endswith("| pass |"))
        body = ("| Skill | Expect | Prompt | Owner | Invoked | Verdict |\n|---|---|---|---|---|---|\n"
                + "\n".join(rows) + f"\n\nSummary: {passed}/{len(rows)} pass.\n")
    else:
        sections = run_behaviors(cases, args)
        if args.dry_run:
            return 0
        body = "Behavior transcripts need human grading; unchecked boxes are not passes.\n\n" + "\n".join(sections)
    print(f"Results written to {write_results(args.kind, args, body).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
