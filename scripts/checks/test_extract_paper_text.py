"""Offline fixture: a replaced PDF must not keep its stale text extraction."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "papers"))
import extract_paper_text as extraction  # noqa: E402


def write_pdf(path, text):
    from pypdf import PdfWriter
    from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject
    writer = PdfWriter()
    page = writer.add_blank_page(width=500, height=500)
    font = DictionaryObject({NameObject("/Type"): NameObject("/Font"),
                             NameObject("/Subtype"): NameObject("/Type1"),
                             NameObject("/BaseFont"): NameObject("/Helvetica")})
    page[NameObject("/Resources")] = DictionaryObject(
        {NameObject("/Font"): DictionaryObject({NameObject("/F1"): writer._add_object(font)})})
    stream = DecodedStreamObject()
    stream.set_data(("BT /F1 10 Tf 10 450 Td (" + text + ") Tj ET").encode("ascii"))
    page[NameObject("/Contents")] = writer._add_object(stream)
    with path.open("wb") as output:
        writer.write(output)


class ExtractionTests(unittest.TestCase):
    def test_replaced_pdf_is_reported_then_regenerated(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            papers = root / "papers"
            pdf = papers / "2026" / "06_Fixture_Tabular_Model.pdf"
            pdf.parent.mkdir(parents=True)
            write_pdf(pdf, "Original tabular fixture text.")

            def run(*args):
                with patch.object(sys, "argv", ["extract_paper_text.py", *args]), \
                     contextlib.redirect_stdout(io.StringIO()) as output:
                    return extraction.main(), output.getvalue()

            with patch.multiple(extraction, _ROOT=root, _PAPERS=papers, _TEXT=papers / "text"):
                self.assertEqual(run("--all")[0], 0)
                text = extraction.text_path_for(pdf)
                self.assertIn("Original tabular", text.read_text(encoding="utf-8"))
                self.assertEqual(run("--check")[0], 0)
                write_pdf(pdf, "Replacement tabular revision text.")
                before = text.read_bytes()
                code, output = run("--check")
                self.assertEqual(code, 1)
                self.assertIn("STALE TEXT", output)
                self.assertEqual(text.read_bytes(), before)
                self.assertEqual(run("--all")[0], 0)
                self.assertIn("Replacement tabular revision", text.read_text(encoding="utf-8"))
                sources = json.loads((papers / "text_sources.json").read_text(encoding="utf-8"))["sources"]
                self.assertEqual(sources["2026/" + pdf.name], hashlib.sha256(pdf.read_bytes()).hexdigest())
                self.assertEqual(run("--check")[0], 0)


if __name__ == "__main__":
    unittest.main()
