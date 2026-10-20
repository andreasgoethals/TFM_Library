from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

DUMPS = Path(__file__).resolve().parents[1] / "dumps"
sys.path.insert(0, str(DUMPS))
import refresh_external_sources as external


class ExternalSourceTests(unittest.TestCase):
    def test_archived_runs_are_excluded_while_active_config_and_source_remain(self):
        snapshot = external.source_snapshot
        patterns = snapshot.entry_patterns(snapshot.REPOSITORIES["TabForestPFN.txt"])
        self.assertFalse(snapshot._selected("outputs_done/run/config.yaml", 10, patterns))
        self.assertTrue(snapshot._selected("config/main.yaml", 10, patterns))
        self.assertTrue(snapshot._selected("tabularbench/model/model.py", 10, patterns))

    def test_partial_export_and_download_failure_do_not_produce_a_snapshot(self):
        with patch.object(external, "get", return_value="# unavailable"):
            with self.assertRaises(ValueError):
                external.docs()
        incomplete = "\n".join(f"Source: https://docs.priorlabs.ai/guide-{i}" for i in range(30))
        with patch.object(external, "get", return_value=incomplete):
            with self.assertRaises(ValueError):
                external.docs()
        with patch.object(external, "get", side_effect=OSError("network unavailable")):
            with self.assertRaises(OSError):
                external.docs()

    def test_shrink_or_swap_failure_preserves_previous_good_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "snapshot.txt"
            target.write_text("original" * 1000)
            before = target.read_bytes()
            with self.assertRaises(ValueError):
                external.replace(target, "tiny")
            with patch.object(external.os, "replace", side_effect=OSError("locked")):
                with self.assertRaises(OSError):
                    external.replace(target, "replacement" * 1000)
            self.assertEqual(target.read_bytes(), before)
            self.assertEqual(list(Path(directory).iterdir()), [target])

    def test_model_cards_resolve_immutable_revisions(self):
        seen = []
        def get(url):
            seen.append(url)
            return '{"sha":"reviewed-sha"}' if "/api/" in url else "TabPFN source " * 200
        with patch.object(external, "get", get):
            result = external.cards()
        self.assertEqual(sum("/raw/reviewed-sha/" in url for url in seen), 2)
        self.assertIn("SHA-256:", result)


if __name__ == "__main__":
    unittest.main()
