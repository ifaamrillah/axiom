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

    def test_repository_cases_are_valid(self):
        self.assertEqual(run_evals.check(run_evals.load_cases()), [])


if __name__ == "__main__":
    unittest.main()
