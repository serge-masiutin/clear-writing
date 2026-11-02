"""Проверки переносимого пакета."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/clear-writing"


class SkillPackageTest(unittest.TestCase):
    def test_language_editions_have_the_same_files(self):
        inventories = [{path.relative_to(SKILL / language) for path in
                        (SKILL / language).rglob("*.md")} for language in ("ru", "en")]
        self.assertEqual(inventories[0], inventories[1])
        self.assertEqual(12, len(inventories[0]))

    def test_frontmatter_and_technical_routing(self):
        entry = (SKILL / "SKILL.md").read_text()
        self.assertTrue(entry.startswith("---\nname: clear-writing\ndescription: "))
        self.assertIn('version: "10"', entry)
        for language in ("ru", "en"):
            self.assertIn(f"({language}/technical.md)", entry)
            self.assertIn("(technical.md)", (SKILL / language / "guide.md").read_text())

    def test_relative_markdown_links_exist(self):
        for source in ROOT.rglob("*.md"):
            if ".git" in source.relative_to(ROOT).parts:
                continue
            for target in re.findall(r"\]\(([^\s)]+)\)", source.read_text()):
                if ":" in target or target.startswith("#"):
                    continue
                with self.subTest(source=source, target=target):
                    self.assertTrue((source.parent / target.split("#")[0]).exists())


if __name__ == "__main__":
    unittest.main()
