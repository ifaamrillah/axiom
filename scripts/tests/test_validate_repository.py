"""Unit tests for the skills-only install checks in scripts/validate_repository.py."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import validate_repository as vr  # noqa: E402


class SkillChecksTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.skills = self.root / ".agents" / "skills"
        (self.skills / "demo" / "assets").mkdir(parents=True)
        (self.root / "templates").mkdir()
        (self.root / "templates" / "t.md").write_text("template\n", encoding="utf-8")
        saved = vr.ROOT, vr.SKILLS_ROOT, vr.BUNDLED_ASSETS, list(vr.ERRORS)
        self.addCleanup(self.restore, saved)
        vr.ROOT, vr.SKILLS_ROOT = self.root, self.skills
        vr.BUNDLED_ASSETS = {"demo/assets/t.md": "templates/t.md"}
        vr.ERRORS.clear()

    @staticmethod
    def restore(saved):
        vr.ROOT, vr.SKILLS_ROOT, vr.BUNDLED_ASSETS = saved[0], saved[1], saved[2]
        vr.ERRORS[:] = saved[3]

    def write_skill(self, body: str):
        (self.skills / "demo" / "SKILL.md").write_text(body, encoding="utf-8")

    def test_links_leaving_skills_are_rejected_in_every_form(self):
        for body in ("[x](../../../templates/t.md)", "![i](../../../templates/t.md)",
                     "[ref]: ../../../templates/t.md"):
            with self.subTest(body=body):
                vr.ERRORS.clear()
                self.write_skill(body + "\n")
                vr.check_skill_self_containment()
                self.assertEqual(len(vr.ERRORS), 1)

    def test_links_inside_skills_and_urls_pass(self):
        (self.skills / "other").mkdir()
        (self.skills / "other" / "SKILL.md").write_text("x\n", encoding="utf-8")
        self.write_skill("[a](../other/SKILL.md) [b](assets/t.md) [c](https://example.com)\n")
        vr.check_skill_self_containment()
        self.assertEqual(vr.ERRORS, [])

    def test_bundled_asset_drift_and_sync(self):
        vr.check_bundled_assets(sync=False)
        self.assertEqual(len(vr.ERRORS), 1)  # copy missing
        vr.ERRORS.clear()
        vr.check_bundled_assets(sync=True)
        self.assertEqual(vr.ERRORS, [])
        (self.skills / "demo" / "assets" / "t.md").write_text("edited\n", encoding="utf-8")
        vr.check_bundled_assets(sync=False)
        self.assertEqual(len(vr.ERRORS), 1)



class VersionCheckTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        saved = vr.ROOT, list(vr.ERRORS)
        self.addCleanup(self.restore, saved)
        vr.ROOT = self.root
        vr.ERRORS.clear()
        self.write(".claude-plugin/plugin.json", '{"name": "axiom", "version": "1.2.3"}')
        self.write(".agents/skills/axiom-orchestrator/references/kernel.md", "# Axiom Kernel (v1.2.3)\n")
        self.write("templates/project/agents-md-block.md", "<!-- axiom:begin v1.2.3 -->\n")
        self.write("CHANGELOG.md", "## [Unreleased]\n\n## [1.2.3] - 2026-01-01\n")
        self.write("docs/releases/v1.2.3.md", "# notes\n")

    @staticmethod
    def restore(saved):
        vr.ROOT = saved[0]
        vr.ERRORS[:] = saved[1]

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_consistent_versions_pass(self):
        vr.check_version()
        self.assertEqual(vr.ERRORS, [])

    def test_mismatch_and_missing_notes_fail(self):
        self.write("CHANGELOG.md", "## [Unreleased]\n\n## [1.2.2] - 2026-01-01\n")
        (self.root / "docs/releases/v1.2.3.md").unlink()
        vr.check_version()
        self.assertEqual(len(vr.ERRORS), 2)
        self.assertIn("1.2.2 does not match", vr.ERRORS[0])
        self.assertIn("release notes missing", vr.ERRORS[1])


if __name__ == "__main__":
    unittest.main()
