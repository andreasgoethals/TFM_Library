"""Offline fixtures for document neutrality and quiet-mode reporting."""
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_docs as docs  # noqa: E402


class DocumentCheckTests(unittest.TestCase):
    def test_project_names_are_matched_case_insensitively(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for doc in docs.NEUTRAL_DOCS:
                (root / doc).write_text("# Neutral\n", encoding="utf-8")
            (root / "SYNTHESIS.md").write_text("See creditpfn/notes and CREDITICL.\n", encoding="utf-8")
            report = docs.Report()
            with patch.object(docs, "_ROOT", root):
                docs.check_neutrality(report)
        self.assertEqual(len(report.problems), 2)
        self.assertTrue(all("SYNTHESIS.md" in problem for problem in report.problems))

    def test_quiet_mode_still_lists_each_problem(self):
        def fail(report):
            report.fail("fixture problem")
        output = io.StringIO()
        with patch.object(docs, "check_coverage", return_value={"PDFs": 0}), \
             patch.object(docs, "check_links_and_anchors"), \
             patch.object(docs, "check_changelog"), \
             patch.object(docs, "check_neutrality", side_effect=fail), \
             patch.object(docs, "check_placeholders"), \
             contextlib.redirect_stdout(output):
            self.assertEqual(docs.main(["--quiet"]), 1)
        text = output.getvalue()
        self.assertIn("[PROBLEM] fixture problem", text)
        self.assertIn("1 problem(s).", text)
        self.assertNotIn("PDFs", text)


if __name__ == "__main__":
    unittest.main()
