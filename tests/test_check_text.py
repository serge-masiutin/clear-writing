"""Public behavior of the offline checker."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/clear-writing/scripts/check_text.py"
spec = importlib.util.spec_from_file_location("check_text", SCRIPT)
check_text = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = check_text
spec.loader.exec_module(check_text)


class CheckTextTest(unittest.TestCase):
    def test_short_text_has_findings_but_no_misleading_scores(self):
        result = check_text.analyze("Это очень важный отчёт.", "ru")
        self.assertIsNone(result["cleanliness"]["score"])
        self.assertIsNone(result["readability"]["score"])
        self.assertEqual("ru_intensifier", result["findings"][0]["rule"])
        self.assertEqual(2, len(result["warnings"]))

    def test_cleanliness_counts_overlapping_words_once(self):
        text = ("У нас есть уникальная возможность. " * 10).strip()
        result = check_text.analyze(text, "ru")
        self.assertEqual(50, result["word_count"])
        self.assertEqual(20, result["cleanliness"]["flagged_words"])
        self.assertEqual(6.0, result["cleanliness"]["score"])
        self.assertEqual({"ru_cliche", "ru_evaluation"}, {item["rule"] for item in result["findings"]})

    def test_more_filler_reduces_cleanliness(self):
        clean = "The team sent the report to the client. " * 8
        padded = "It should be noted that the team sent the report to the client. " * 8
        self.assertGreater(check_text.analyze(clean, "en")["cleanliness"]["score"],
                           check_text.analyze(padded, "en")["cleanliness"]["score"])

    def test_output_cap_does_not_hide_matches_from_score(self):
        result = check_text.analyze("Very good. " * 120, "en")
        self.assertEqual(5.0, result["cleanliness"]["score"])
        self.assertEqual(100, len(result["findings"]))
        self.assertEqual(20, result["omitted_findings"])
        self.assertEqual(120, result["cleanliness"]["flagged_words"])

    def test_longer_sentences_reduce_readability_in_both_languages(self):
        samples = (
            ("en", "The team sent the report. " * 12,
             "The team sent the detailed report to the client after the final review and several lengthy meetings. " * 6),
            ("ru", "Команда отправила отчёт клиенту. " * 13,
             "Команда отправила подробный отчёт клиенту после окончательной проверки и нескольких продолжительных совещаний. " * 6),
        )
        for language, easy, hard in samples:
            with self.subTest(language=language):
                self.assertGreater(check_text.analyze(easy, language)["readability"]["reading_ease"],
                                   check_text.analyze(hard, language)["readability"]["reading_ease"])

    def test_finds_long_sentences_without_treating_them_as_cleanliness_flags(self):
        text = ("The team checked every step of the process with the client before "
                "the final report was sent to the people who requested the review. " * 3)
        result = check_text.analyze(text, "en")
        self.assertEqual(10.0, result["cleanliness"]["score"])
        self.assertEqual([], result["readability"]["long_sentences"])
        long_text = ("The team " + "carefully reviewed " * 17 + "the report. ") * 3
        self.assertEqual(3, len(check_text.analyze(long_text, "en")["readability"]["long_sentences"]))

    def test_rejects_empty_and_mismatched_input(self):
        for text, language in ((" ", "ru"), ("Only English words here.", "ru")):
            with self.subTest(text=text), self.assertRaises(ValueError):
                check_text.analyze(text, language)

    def test_cli_emits_json_without_source_excerpts(self):
        source = "The unique secret phrase appears here. " * 9
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--language", "en"],
            input=source, text=True, capture_output=True, check=True,
        )
        result = json.loads(completed.stdout)
        self.assertEqual("1", result["method_version"])
        self.assertNotIn("secret phrase", completed.stdout)
        self.assertEqual("", completed.stderr)

    def test_cli_reads_utf8_file(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "article.txt"
            source.write_text("Команда подготовила отчёт. " * 15, encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "--language", "ru", "--file", str(source)],
                text=True, capture_output=True, check=True,
            )
        self.assertEqual("ru", json.loads(completed.stdout)["language"])


if __name__ == "__main__":
    unittest.main()
