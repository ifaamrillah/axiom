"""Unit tests for the advisory composition-prohibition warning in scripts/validate_repository.py."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import validate_repository as vr  # noqa: E402


class PhrasingWarningTest(unittest.TestCase):
    def test_composition_prohibitions_are_flagged(self):
        for line in ("Don't be verbose.", "- Do not over-explain the fix", "Never write long answers",
                     "1. **Never** overthink small tasks", "Don’t explain what the code does",
                     "do not be wordy"):
            with self.subTest(line=line):
                self.assertEqual(len(vr.phrasing_warnings(line)), 1)

    def test_concrete_prohibitions_and_recipes_pass(self):
        for line in ("Never run `git checkout <file>` on a file with uncommitted edits.",
                     "Do not edit skills without approval.",
                     "Answer in one sentence, then list the evidence.",
                     "Keep explanations short.",
                     "Never claim a test ran. Explain what you saw instead."):
            with self.subTest(line=line):
                self.assertEqual(vr.phrasing_warnings(line), [])

    def test_reports_line_numbers(self):
        self.assertEqual(vr.phrasing_warnings("ok\n- Don't be verbose\n"), [(2, "- Don't be verbose")])

    def test_warnings_do_not_become_errors(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name).resolve()
        skills = root / ".agents" / "skills"
        (skills / "demo").mkdir(parents=True)
        (skills / "demo" / "SKILL.md").write_text("Don't be verbose.\n", encoding="utf-8")
        saved = vr.ROOT, vr.SKILLS_ROOT, list(vr.ERRORS), list(vr.WARNINGS)
        self.addCleanup(self.restore, saved)
        vr.ROOT, vr.SKILLS_ROOT = root, skills
        vr.ERRORS.clear()
        vr.WARNINGS.clear()
        vr.check_phrasing()
        self.assertEqual(vr.ERRORS, [])
        self.assertEqual(len(vr.WARNINGS), 1)
        self.assertIn(".agents/skills/demo/SKILL.md:1:", vr.WARNINGS[0])

    @staticmethod
    def restore(saved):
        vr.ROOT, vr.SKILLS_ROOT = saved[0], saved[1]
        vr.ERRORS[:] = saved[2]
        vr.WARNINGS[:] = saved[3]


class FencedLinkTest(unittest.TestCase):
    def test_links_in_fences_are_ignored_and_others_kept(self):
        text = "See [a](a.md).\n\n```text\nBack to [SKILL.md](../SKILL.md)\n```\n\nAnd [b](b.md).\n"
        stripped = vr.strip_fenced_code(text)
        self.assertIn("[a](a.md)", stripped)
        self.assertIn("[b](b.md)", stripped)
        self.assertNotIn("../SKILL.md", stripped)


if __name__ == "__main__":
    unittest.main()
