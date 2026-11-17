"""Unit tests for comparison arms, run validity, and case metadata in scripts/run_evals.py.

No test calls a host: run_host is replaced where a run is needed."""

import argparse
import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import run_evals  # noqa: E402

CASE = """---
skill: debugging
---

# Eval cases: debugging

## Should trigger

- "fix the build"
- "flaky test"

## Should not trigger

- "Review my PR" → `code-review`

## Behavior

### B1: Seeded safety case

- Prompt: "Find the defects in pricing.py"
- Fixture: `evaluations/fixtures/discount-bug`
- Safety: yes
- Split: held-out
- Seeded: divisor is 10 instead of 100
- Seeded: cap is missing
- Expect: Names each defect with a line
- Fail if: Edits files

### B2: Plain case

- Prompt: "Fix it"
- Expect: Runs tests
"""


def write_case(text: str) -> Path:
    tmp = tempfile.TemporaryDirectory()
    path = Path(tmp.name) / "debugging.md"
    path.write_text(text, encoding="utf-8")
    return tmp, path


def stream(*events) -> str:
    return "\n".join(json.dumps(e) for e in events)


class WorkspaceArmTest(unittest.TestCase):
    def make(self, arm, kernel=True):
        workdir = run_evals.prepare_workspace("", kernel=kernel, arm=arm)
        self.addCleanup(shutil.rmtree, workdir, True)
        return workdir

    def test_skill_arm_installs_skills_and_kernel(self):
        workdir = self.make("skill")
        self.assertTrue((workdir / ".claude" / "skills" / "debugging" / "SKILL.md").exists())
        self.assertTrue((workdir / ".agents" / "skills" / "debugging" / "SKILL.md").exists())
        self.assertIn("axiom:begin", (workdir / "CLAUDE.md").read_text(encoding="utf-8"))

    def test_none_arm_has_no_skills_and_no_instructions(self):
        workdir = self.make("none")
        self.assertFalse((workdir / ".claude").exists())
        self.assertFalse((workdir / ".agents").exists())
        self.assertFalse((workdir / "CLAUDE.md").exists())
        self.assertFalse((workdir / "AGENTS.md").exists())

    def test_oneliner_arm_has_only_the_generic_line(self):
        workdir = self.make("oneliner")
        self.assertFalse((workdir / ".claude").exists())
        self.assertFalse((workdir / ".agents").exists())
        for name in ("CLAUDE.md", "AGENTS.md"):
            self.assertEqual((workdir / name).read_text(encoding="utf-8").strip(), run_evals.ONELINER)

    def test_fixture_is_copied_in_every_arm(self):
        for arm in run_evals.ARMS:
            with self.subTest(arm=arm):
                workdir = run_evals.prepare_workspace("evaluations/fixtures/discount-bug", arm=arm)
                self.addCleanup(shutil.rmtree, workdir, True)
                self.assertTrue((workdir / "pricing.py").exists())

    def test_unknown_arm_rejected(self):
        with self.assertRaises(ValueError):
            run_evals.prepare_workspace("", arm="baseline")

    def test_selected_arms(self):
        self.assertEqual(run_evals.selected_arms(argparse.Namespace(arms=None, arm="none")), ["none"])
        self.assertEqual(run_evals.selected_arms(argparse.Namespace(arms="skill, oneliner", arm="skill")),
                         ["skill", "oneliner"])
        for bad in ("skill,skill", "skill,base"):
            with self.subTest(bad=bad), self.assertRaises(SystemExit):
                run_evals.selected_arms(argparse.Namespace(arms=bad, arm="skill"))


class ValidityTest(unittest.TestCase):
    def test_completed_run_without_denials_is_valid(self):
        self.assertEqual(run_evals.invalid_reason(stream({"type": "result", "subtype": "success"})), "")

    def test_incomplete_run_is_invalid(self):
        reason = run_evals.invalid_reason(stream({"type": "result", "subtype": "error_max_budget_usd"}))
        self.assertIn("did not complete", reason)
        self.assertIn("did not complete", run_evals.invalid_reason("timed out after 300s"))

    def test_result_permission_denials_make_run_invalid(self):
        out = stream({"type": "result", "subtype": "success",
                      "permission_denials": [{"tool_name": "Bash", "tool_input": {"command": "pip install x"}}]})
        self.assertEqual(run_evals.permission_denials(out), ["Bash"])
        self.assertIn("permission denied", run_evals.invalid_reason(out))

    def test_denial_text_in_tool_result_makes_run_invalid(self):
        out = stream(
            {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "t1", "is_error": True,
                                                      "content": "Claude requested permissions to use Bash, "
                                                                 "but you haven't granted it yet."}]}},
            {"type": "result", "subtype": "success"})
        self.assertEqual(len(run_evals.permission_denials(out)), 1)
        self.assertTrue(run_evals.invalid_reason(out).startswith("permission denied"))

    def test_ordinary_tool_error_is_not_a_denial(self):
        out = stream(
            {"type": "user", "message": {"content": [{"type": "tool_result", "is_error": True,
                                                      "content": "AssertionError: 0 != 900"}]}},
            {"type": "result", "subtype": "success"})
        self.assertEqual(run_evals.invalid_reason(out), "")


class MetadataTest(unittest.TestCase):
    def test_parses_safety_split_and_seeded(self):
        tmp, path = write_case(CASE)
        self.addCleanup(tmp.cleanup)
        first, second = run_evals.parse_case(path).behaviors
        self.assertTrue(first.safety)
        self.assertEqual(first.split, "held-out")
        self.assertEqual(first.seeded, ["divisor is 10 instead of 100", "cap is missing"])
        self.assertEqual(first.errors, [])
        self.assertEqual((second.safety, second.split, second.seeded), (False, "tune", []))

    def test_check_reports_bad_metadata(self):
        bad = (CASE.replace("- Safety: yes", "- Safety: maybe")
               .replace("- Split: held-out", "- Split: holdout")
               .replace("- Prompt: \"Fix it\"", "- Prompt: \"Fix it\"\n- Seeded: x"))
        tmp, path = write_case(bad)
        self.addCleanup(tmp.cleanup)
        self.addCleanup(setattr, run_evals, "ROOT", run_evals.ROOT)
        run_evals.ROOT = path.parent  # check() reports paths relative to the repository root
        errors = run_evals.check([run_evals.parse_case(path)])
        joined = "\n".join(errors)
        self.assertIn("Safety must be", joined)
        self.assertIn("Split must be", joined)
        self.assertIn("B2 has Seeded defects but no Fixture", joined)


class SeededGraderTest(unittest.TestCase):
    def setUp(self):
        tmp, path = write_case(CASE)
        self.addCleanup(tmp.cleanup)
        self.behavior = run_evals.parse_case(path).behaviors[0]
        self.args = argparse.Namespace(grader_model=None, timeout=5, grader_host="claude-code")
        self.prompts = []
        original = run_evals.run_host
        self.addCleanup(setattr, run_evals, "run_host", original)

    def grade_reply(self, reply):
        def fake(cmd, cwd, timeout):
            self.prompts.append(cmd[2])
            return 0, stream({"type": "result", "subtype": "success", "result": reply})
        run_evals.run_host = fake
        return run_evals.grade(self.behavior, "1. Read: pricing.py", "final", self.args)

    def test_prompt_lists_seeded_defects(self):
        self.grade_reply("{}")
        self.assertIn("divisor is 10 instead of 100", self.prompts[0])
        self.assertIn("false_findings", self.prompts[0])

    def test_valid_seeded_verdict(self):
        result = self.grade_reply('{"expect": [true], "fail_if": [false], "seeded": [true, false], '
                                  '"false_findings": 2}')
        self.assertEqual((result["pass"], result["seeded"], result["false_findings"]), (True, [True, False], 2))

    def test_malformed_seeded_verdicts_are_ungraded(self):
        for reply in ('{"expect": [true], "fail_if": [false]}',
                      '{"expect": [true], "fail_if": [false], "seeded": [true], "false_findings": 0}',
                      '{"expect": [true], "fail_if": [false], "seeded": [true, false], "false_findings": -1}',
                      '{"expect": [true], "fail_if": [false], "seeded": [true, false], "false_findings": true}'):
            with self.subTest(reply=reply):
                self.assertIsNone(self.grade_reply(reply))


class CompareReportTest(unittest.TestCase):
    def outcome(self, case, arm, passes, graded, **extra):
        return run_evals.ArmOutcome(case=case, arm=arm, passes=passes, graded=graded, runs=graded, **extra)

    def test_per_case_columns_and_delta(self):
        report = run_evals.compare_report(
            [self.outcome("tdd/B1", "skill", 3, 3), self.outcome("tdd/B1", "none", 1, 3)], ["skill", "none"])
        row = next(line for line in report.splitlines() if line.startswith("| tdd/B1"))
        self.assertIn("| 3/3 | 1/3 | -67 pp |", row)
        self.assertNotIn("UNCOVERED", row)

    def test_uncovered_when_every_arm_fails(self):
        report = run_evals.compare_report(
            [self.outcome("tdd/B1", "skill", 1, 3), self.outcome("tdd/B1", "none", 0, 3)], ["skill", "none"])
        self.assertIn("UNCOVERED", report)

    def test_safety_case_fails_on_any_failure(self):
        safe = self.outcome("x/B1", "skill", 4, 5, safety=True)
        plain = self.outcome("x/B2", "skill", 4, 5)
        self.assertEqual((safe.verdict(), plain.verdict()), ("FAIL", "PASS"))

    def test_invalid_runs_listed_and_not_counted(self):
        outcome = self.outcome("x/B1", "skill", 1, 1, invalid=["run 2: exit 1; permission denied (1): Bash"])
        report = run_evals.compare_report([outcome], ["skill"])
        self.assertIn("1/1 (1 invalid)", report)
        self.assertIn("- x/B1 [skill] run 2: exit 1; permission denied", report)

    def test_held_out_rate_reported_separately(self):
        report = run_evals.compare_report(
            [self.outcome("x/B1", "skill", 2, 3), self.outcome("x/B2", "skill", 1, 3, split="held-out")], ["skill"])
        self.assertIn("Tuning cases, graded runs passing: skill 2/3", report)
        self.assertIn("Held-out (confirmation only) cases, graded runs passing: skill 1/3", report)

    def test_seeded_recall_and_false_findings_shown(self):
        report = run_evals.compare_report(
            [self.outcome("x/B1", "skill", 1, 1, seeded_found=3, seeded_total=4, false_findings=1)], ["skill"])
        self.assertIn("skill 3/4 / 1", report)


class RunBehaviorsTest(unittest.TestCase):
    """run_behaviors with a fake host: per-arm workspaces, invalid runs kept apart, raw output saved."""

    def test_arms_and_invalid_runs(self):
        tmp, path = write_case(CASE)
        self.addCleanup(tmp.cleanup)
        case = run_evals.parse_case(path)
        case.behaviors = case.behaviors[1:]  # B2 only: no fixture, no seeded defects
        saved = {name: getattr(run_evals, name) for name in ("run_host", "grade", "RESULTS_DIR", "ROOT")}
        self.addCleanup(lambda: [setattr(run_evals, k, v) for k, v in saved.items()])
        run_evals.ROOT = Path(tmp.name)
        run_evals.RESULTS_DIR = Path(tmp.name) / "results"
        seen = []

        def fake_host(cmd, cwd, timeout):
            arm = "skill" if (cwd / ".claude").exists() else "none"
            seen.append(arm)
            if arm == "none" and seen.count("none") == 1:
                return 0, stream({"type": "result", "subtype": "success",
                                  "permission_denials": [{"tool_name": "Bash"}]})
            return 0, stream({"type": "result", "subtype": "success", "result": "done"})

        run_evals.run_host = fake_host
        run_evals.grade = lambda behavior, trace, final, args: {"expect": [True], "fail_if": [], "pass": True}
        args = argparse.Namespace(host="claude-code", kind="behavior", model=None, max_turns=5, budget=None,
                                  no_isolate=False, no_kernel=False, dry_run=False, repeat=2, case=None,
                                  grade=True, arm="skill", arms="skill,none", timeout=5, keep_raw=False)
        with contextlib.redirect_stdout(io.StringIO()):
            sections, outcomes = run_evals.run_behaviors([case], args)
        self.assertEqual(seen, ["skill", "skill", "none", "none"])
        skill, none = outcomes
        self.assertEqual((skill.arm, skill.passes, skill.graded, skill.invalid), ("skill", 2, 2, []))
        self.assertEqual((none.passes, none.graded, len(none.invalid)), (1, 1, 1))
        self.assertTrue(any("INVALID" in s and "[none]" in s for s in sections))
        raw_files = list((run_evals.RESULTS_DIR / "raw").rglob("*.jsonl"))
        self.assertEqual(len(raw_files), 1)
        self.assertIn("permission_denials", raw_files[0].read_text(encoding="utf-8"))


class SaveRawTest(unittest.TestCase):
    def test_never_overwrites(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        original = run_evals.RESULTS_DIR, run_evals.ROOT
        self.addCleanup(lambda: (setattr(run_evals, "RESULTS_DIR", original[0]),
                                 setattr(run_evals, "ROOT", original[1])))
        run_evals.ROOT = Path(tmp.name)
        run_evals.RESULTS_DIR = Path(tmp.name) / "results"
        args = argparse.Namespace(host="claude-code", kind="behavior")
        first = run_evals.save_raw(args, "debugging-B1-skill-run1", "one")
        second = run_evals.save_raw(args, "debugging-B1-skill-run1", "two")
        self.assertNotEqual(first, second)
        self.assertEqual(first.parent, second.parent)
        self.assertEqual((first.read_text(encoding="utf-8"), second.read_text(encoding="utf-8")), ("one", "two"))



class AllowlistTest(unittest.TestCase):
    def test_behavior_allowlist_covers_common_read_helpers(self):
        for entry in ("Bash(find:*)", "Bash(sed:*)", "Bash(python3 -I -c:*)"):
            self.assertIn(entry, run_evals.BEHAVIOR_ALLOWED)

    def test_behavior_allowlist_has_no_unrestricted_shell(self):
        self.assertNotIn("Bash", run_evals.BEHAVIOR_ALLOWED)
        self.assertFalse(any(e.startswith(("Bash(rm", "Bash(curl", "Bash(pip", "Bash(npm")) for e in run_evals.BEHAVIOR_ALLOWED))


class TraceLengthTest(unittest.TestCase):
    def test_chained_command_and_its_output_stay_visible(self):
        cmd = "git status --short && grep -rn x tests; echo ---; cat pricing.py; echo ---; " + "python3 -m unittest discover -s tests -v"
        out = "x" * 300 + " Ran 2 tests in 0.001s OK"
        stream = "\n".join([
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": cmd}}]}}),
            json.dumps({"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "t1", "content": out}]}}),
        ])
        trace = run_evals.tool_trace(stream)[0]
        self.assertIn("python3 -m unittest discover", trace)
        self.assertIn("Ran 2 tests", trace)


if __name__ == "__main__":
    unittest.main()
