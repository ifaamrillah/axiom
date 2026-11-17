"""Unit tests for scripts/run_evals.py parsing and grading helpers (no host calls)."""

import json
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

- "The build is broken, fix it"
- "test passes alone but fails in suite"

## Should not trigger

- "Review my PR" → `code-review`

## Behavior

### B1: Root cause first

- Prompt: "Fix apply_discount"
- Fixture: `evaluations/fixtures/discount-bug`
- Expect: Reproduces before editing
- Expect: Names the divisor bug
- Fail if: Edits before reproduction
"""


class ParseCaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "debugging.md"
        self.path.write_text(CASE, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_parses_triggers_and_owner(self):
        case = run_evals.parse_case(self.path)
        self.assertEqual(case.skill, "debugging")
        self.assertEqual(case.positive, ["The build is broken, fix it", "test passes alone but fails in suite"])
        self.assertEqual(case.negative, [("Review my PR", "code-review")])

    def test_parses_behavior_fields(self):
        behavior = run_evals.parse_case(self.path).behaviors[0]
        self.assertEqual(behavior.case_id, "B1")
        self.assertEqual(behavior.prompt, "Fix apply_discount")
        self.assertEqual(behavior.fixture, "evaluations/fixtures/discount-bug")
        self.assertEqual(len(behavior.expect), 2)
        self.assertEqual(behavior.fail_if, ["Edits before reproduction"])


class InvokedSkillsTest(unittest.TestCase):
    def test_extracts_skill_tool_use_and_strips_namespace(self):
        events = [
            {"type": "system", "subtype": "init"},
            {"type": "assistant", "message": {"content": [
                {"type": "text", "text": "Using debugging"},
                {"type": "tool_use", "name": "Skill", "input": {"skill": "axiom:debugging"}},
            ]}},
            {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "name": "Read", "input": {"file_path": "x"}},
            ]}},
            "not json",
        ]
        stream = "\n".join(e if isinstance(e, str) else json.dumps(e) for e in events)
        self.assertEqual(run_evals.invoked_skills(stream), ["debugging"])

    def test_no_invocation(self):
        self.assertEqual(run_evals.invoked_skills('{"type":"result","result":"hi"}'), [])


class RepositoryCasesTest(unittest.TestCase):
    def test_kernel_block_carries_rules_without_project_facts(self):
        block = run_evals.kernel_block()
        self.assertIn("Reproduce before fixing", block)
        self.assertIn("## Routing", block)
        self.assertNotIn("## Project facts", block)

    def test_workspace_kernel_toggle(self):
        import shutil
        with_kernel = run_evals.prepare_workspace("", kernel=True)
        without = run_evals.prepare_workspace("", kernel=False)
        try:
            self.assertTrue((with_kernel / "CLAUDE.md").exists())
            self.assertTrue((with_kernel / "AGENTS.md").exists())
            self.assertFalse((without / "CLAUDE.md").exists())
        finally:
            shutil.rmtree(with_kernel)
            shutil.rmtree(without)

    def test_tool_trace_attaches_results(self):
        stream = "\n".join([
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "python3 -m unittest"}}]}}),
            json.dumps({"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "t1", "content": "FAILED (failures=1)"}]}}),
        ])
        trace = run_evals.tool_trace(stream)
        self.assertEqual(len(trace), 1)
        self.assertIn("python3 -m unittest", trace[0])
        self.assertIn("FAILED (failures=1)", trace[0])

    def test_accept_alias_parsed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.md"
            path.write_text("---\nskill: codebase-onboarding\naccept: project-onboarding\n---\n", encoding="utf-8")
            case = run_evals.parse_case(path)
        self.assertEqual(case.accept, ["project-onboarding"])

    def test_repository_cases_are_valid(self):
        self.assertEqual(run_evals.check(run_evals.load_cases()), [])


class GraderTest(unittest.TestCase):
    """grade() must accept only well-formed boolean verdicts; anything else is ungraded."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        path = Path(tmp.name) / "debugging.md"
        path.write_text(CASE, encoding="utf-8")
        self.behavior = run_evals.parse_case(path).behaviors[0]
        self.args = type("Args", (), {"grader_model": None, "timeout": 5})()
        self.original = run_evals.run_host
        self.addCleanup(setattr, run_evals, "run_host", self.original)

    def grade_reply(self, reply: str):
        stream = json.dumps({"type": "result", "subtype": "success", "result": reply})
        run_evals.run_host = lambda cmd, cwd, timeout: (0, stream)
        return run_evals.grade(self.behavior, "1. Bash: x", "final", self.args)

    def test_valid_pass_and_fail(self):
        self.assertTrue(self.grade_reply('{"expect": [true, true], "fail_if": [false], "reason": "ok"}')["pass"])
        self.assertFalse(self.grade_reply('{"expect": [true, false], "fail_if": [false]}')["pass"])
        self.assertFalse(self.grade_reply('{"expect": [true, true], "fail_if": [true]}')["pass"])

    def test_malformed_replies_are_ungraded(self):
        for reply in ('{"expect": [1, 1], "fail_if": [null]}',
                      '{"expect": ["true", "true"], "fail_if": ["false"]}',
                      '{"expect": [true], "fail_if": [false]}',
                      '{"expect": "ab", "fail_if": [false]}',
                      'no json here'):
            with self.subTest(reply=reply):
                self.assertIsNone(self.grade_reply(reply))


class RunCompletedTest(unittest.TestCase):
    def test_budget_stop_is_not_completed(self):
        for subtype, expected in (("success", True), ("error_max_turns", True),
                                  ("error_max_budget_usd", False), ("error_during_execution", False)):
            with self.subTest(subtype=subtype):
                stream = json.dumps({"type": "result", "subtype": subtype})
                self.assertEqual(run_evals.run_completed(stream), expected)

    def test_usage_limit_is_not_completed(self):
        stream = json.dumps({"type": "result", "subtype": "success", "is_error": True,
                             "result": "You've hit your 5-hour limit"})
        self.assertFalse(run_evals.run_completed(stream))


class WriteResultsTest(unittest.TestCase):
    def test_never_overwrites(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        original = run_evals.RESULTS_DIR, run_evals.host_version
        self.addCleanup(lambda: (setattr(run_evals, "RESULTS_DIR", original[0]),
                                 setattr(run_evals, "host_version", original[1])))
        run_evals.RESULTS_DIR = Path(tmp.name)
        run_evals.host_version = lambda host: "test"
        args = type("Args", (), {"host": "claude-code", "model": None, "skill": None, "max_turns": 1,
                                 "repeat": 1, "grade": False, "grader_model": None, "no_isolate": False,
                                 "no_kernel": False, "budget": 0})()
        first = run_evals.write_results("trigger", args, "one")
        second = run_evals.write_results("trigger", args, "two")
        self.assertNotEqual(first, second)
        self.assertIn("one", first.read_text(encoding="utf-8"))
        self.assertIn("two", second.read_text(encoding="utf-8"))


class CodexStreamTest(unittest.TestCase):
    def stream(self, command, output="ok", final="done"):
        events = [
            {"type": "item.started", "item": {"type": "command_execution", "command": command}},
            {"type": "item.completed", "item": {"type": "command_execution", "command": command,
                                                "aggregated_output": output}},
            {"type": "item.completed", "item": {"type": "agent_message", "text": final}},
            {"type": "turn.completed"},
        ]
        return "\n".join(json.dumps(e) for e in events)

    def test_project_skill_read_counts_and_home_skill_does_not(self):
        home = str(Path.home())
        cmd = (f"cat {home}/.agents/skills/personal/SKILL.md && "
               "cat /tmp/axiom-eval-x/.agents/skills/debugging/SKILL.md && cat .agents/skills/tdd/SKILL.md")
        stream = self.stream(cmd)
        self.assertEqual(run_evals.invoked_skills(stream), ["debugging", "tdd"])
        self.assertTrue(run_evals.run_completed(stream))
        self.assertEqual(run_evals._final_text(stream), "done")
        self.assertIn("Shell:", run_evals.tool_trace(stream)[0])

    def test_failed_turn_is_not_completed(self):
        self.assertFalse(run_evals.run_completed(json.dumps({"type": "turn.failed"})))


class RoutingReportTest(unittest.TestCase):
    def _case(self, skill, positive, negative=()):
        return run_evals.CaseFile(path=Path(f"{skill}.md"), skill=skill,
                                  positive=list(positive), negative=list(negative))

    def test_ranks_matching_description_first(self):
        docs = {"debugging": "Find the root cause of a failing test or bug before fixing",
                "release-management": "Prepare a release, changelog, version tag, and rollout"}
        cases = [self._case("debugging", ["the failing test has a bug"],
                            [("cut a release with a changelog", "release-management")])]
        errors, misses, stats = run_evals.routing_report(cases, docs)
        self.assertEqual(errors, [])
        self.assertEqual(misses, [])
        self.assertEqual((stats["top1"], stats["negative_clear"]), (1, 1))

    def test_near_identical_descriptions_collide(self):
        docs = {"alpha": "Review a diff for defects and missing tests",
                "beta": "Review a diff for defects and missing tests now"}
        errors, _, _ = run_evals.routing_report([], docs)
        self.assertEqual(len(errors), 1)
        self.assertIn("alpha and beta", errors[0])

    def test_tokens_drop_stopwords_and_suffixes(self):
        self.assertEqual(run_evals._tokens("Use when the tests are failing"), ["test", "fail"])



class UsageTest(unittest.TestCase):
    def test_claude_result_usage_includes_cache(self):
        stream = json.dumps({"type": "result", "subtype": "success", "usage": {
            "input_tokens": 10, "cache_creation_input_tokens": 100, "cache_read_input_tokens": 1000,
            "output_tokens": 7}})
        self.assertEqual(run_evals.run_usage(stream), (1110, 7))

    def test_codex_turns_are_summed(self):
        turn = json.dumps({"type": "turn.completed", "usage": {"input_tokens": 50, "output_tokens": 5}})
        self.assertEqual(run_evals.run_usage(turn + "\n" + turn), (100, 10))

    def test_missing_usage_is_none(self):
        self.assertIsNone(run_evals.run_usage(json.dumps({"type": "result", "subtype": "success"})))


if __name__ == "__main__":
    unittest.main()
