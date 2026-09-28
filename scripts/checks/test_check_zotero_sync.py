"""Offline regressions for the live-API Zotero audit. No Zotero writes or reads."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import Mock, patch

import check_zotero_sync as sync


def item(key="PAPER001", title="First paper", date="2022"):
    return {"key": key, "meta": {"parsedDate": date}, "data": {
        "itemType": "conferencePaper", "title": title, "date": date,
        "creators": [{"creatorType": "author", "lastName": "Muller"}],
        "url": "https://example.org/paper",
    }}


class ReaderTests(unittest.TestCase):
    def test_pagination_keeps_items_after_first_hundred(self):
        reader = sync.ZoteroReader()
        first = [{"key": str(i)} for i in range(100)]
        with patch.object(reader, "get", side_effect=[first, [{"key": "100"}]]) as get:
            self.assertEqual(len(reader.all("/collections")), 101)
        self.assertEqual(get.call_args_list[1].args[0],
                         "/collections?limit=100&start=100")

    def test_collection_renumbering_and_ambiguity(self):
        reader = sync.ZoteroReader()
        target = {"key": "TFM", "data": {"name": "19. Tabular Foundation Models"}}
        with patch.object(reader, "all", return_value=[target]):
            self.assertEqual(reader.collection("tabular foundation models"), target)
        with patch.object(reader, "all", return_value=[target, target]):
            with self.assertRaises(ValueError):
                reader.collection(sync.DEFAULT_COLLECTION)

    def test_trash_notes_and_attachments_are_not_papers(self):
        reader = sync.ZoteroReader()
        dead = item("DELETED")
        dead["data"]["deleted"] = 1
        note = {"data": {"itemType": "note"}}
        attachment = {"data": {"itemType": "attachment"}}
        with patch.object(reader, "all", return_value=[dead, note, attachment, item()]):
            self.assertEqual(reader.items("TFM"), [item()])

    def test_both_attachment_types_resolve_via_file_url(self):
        reader = sync.ZoteroReader()
        pdfs = [{"key": key, "data": {"contentType": "application/pdf",
                                      "linkMode": mode}}
                for key, mode in [("LINKED", "linked_file"), ("STORED", "imported_file")]]
        dead = {"key": "TRASH", "data": {"contentType": "application/pdf", "deleted": 1}}
        with patch.object(reader, "all", return_value=pdfs + [dead]):
            self.assertEqual(reader.pdfs("PAPER001"), pdfs)
        with tempfile.TemporaryDirectory(prefix="tfm-sync-test-") as tmp:
            path = Path(tmp) / "paper with spaces.pdf"
            path.write_bytes(b"fixture")
            with patch.object(reader, "get", return_value=path.as_uri()):
                for pdf in pdfs:
                    self.assertEqual(reader.file_path(pdf["key"]), path)
        with patch.object(reader, "get", return_value="https://example.org/file.pdf"):
            with self.assertRaises(ValueError):
                reader.file_path("REMOTE")

    def test_api_failure_is_an_error_without_preferences_or_db_fallback(self):
        output = io.StringIO()
        with patch.object(sync.urllib.request, "urlopen",
                          side_effect=urllib.error.URLError("offline")), \
                patch.object(sync, "read_zotero_prefs") as prefs, \
                contextlib.redirect_stdout(output):
            self.assertEqual(sync.main(["--json"]), 2)
        prefs.assert_not_called()
        self.assertIn("No SQLite fallback", json.loads(output.getvalue())["error"])


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="tfm-sync-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "papers"
        self.pdf = self.root / "2021" / "12_Muller_et_al._First_paper.pdf"
        self.pdf.parent.mkdir(parents=True)
        self.pdf.write_bytes(b"fixture")
        self.text = self.root / "text" / "2021" / (self.pdf.stem + ".txt")
        self.text.parent.mkdir(parents=True)
        self.text.write_text("arXiv:2112.10510v1 [cs.LG] 20 Dec 2021", encoding="utf-8")
        patcher = patch.object(sync, "_PAPERS", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.reader = Mock(spec=sync.ZoteroReader)
        self.reader.items.return_value = [item()]
        self.reader.pdfs.return_value = [{"key": "PDF001"}]
        self.reader.file_path.return_value = self.pdf
        self.collection = {"key": "TFM", "data": {"name": "08. Tabular Foundation Models"}}

    def test_publication_date_does_not_override_confirmed_version_date(self):
        stats, report, notes = sync.compare(self.reader, self.collection)
        self.assertEqual(stats["matched"], 1)
        self.assertEqual(report.total, 0)
        self.assertEqual(len(notes), 1)
        self.assertIn("stored version 2021-12", notes[0])

    def test_wrong_filing_month_is_reported(self):
        self.text.write_text("arXiv:2112.10510v2 [cs.LG] 3 Jan 2022", encoding="utf-8")
        _, report, _ = sync.compare(self.reader, self.collection)
        self.assertIn("Filed date disagrees with stored arXiv version", report.sections)

    def test_unconfirmed_year_disagreement_remains_an_issue(self):
        self.text.write_text("Published at ICLR 2022", encoding="utf-8")
        _, report, _ = sync.compare(self.reader, self.collection)
        self.assertIn("Year mismatch without an arXiv version date", report.sections)

    def test_missing_paper_and_extra_library_pdf_are_both_reported(self):
        self.reader.items.return_value = [item(title="Completely unrelated research")]
        self.reader.pdfs.return_value = []
        stats, report, _ = sync.compare(self.reader, self.collection)
        self.assertEqual(stats["matched"], 0)
        self.assertIn("In Zotero collection but NOT in papers/", report.sections)
        self.assertIn("In papers/ but NOT in the Zotero collection", report.sections)
        self.assertIn("Zotero items with no PDF attachment", report.sections)

    def test_duplicate_matches_cannot_pass_as_one_to_one(self):
        self.reader.items.return_value = [item(), item(key="PAPER002")]
        _, report, _ = sync.compare(self.reader, self.collection)
        self.assertIn("Multiple Zotero items matched to one library PDF", report.sections)

    def test_broken_attachment_and_missing_extraction_are_reported(self):
        self.reader.file_path.return_value = self.root / "missing.pdf"
        self.text.unlink()
        _, report, _ = sync.compare(self.reader, self.collection)
        self.assertIn("Zotero attachment paths broken on disk", report.sections)
        self.assertIn("PDFs with no text extraction", report.sections)


if __name__ == "__main__":
    unittest.main()
