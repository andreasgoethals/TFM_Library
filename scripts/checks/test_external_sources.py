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

    def test_timestamp_only_change_leaves_snapshot_untouched(self):
        def snapshot(stamp, body):
            return 'Header\n{\n  "source": "x",\n  "retrieved_utc": "' + stamp + '",\n  "sha256": "y"\n}\n\n' + body * 200
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "snapshot.txt"
            target.write_bytes(snapshot("2026-01-01T00:00:00+00:00", "same content\n").encode())
            before = (target.read_bytes(), target.stat().st_mtime_ns)
            with patch.object(external.os, "replace", side_effect=AssertionError("must not rewrite")):
                external.replace(target, snapshot("2026-10-20T12:34:56.123456+00:00", "same content\n"))
            self.assertEqual((target.read_bytes(), target.stat().st_mtime_ns), before)
            external.replace(target, snapshot("2026-10-20T12:34:56+00:00", "changed content\n"))
            self.assertIn(b"changed content", target.read_bytes())
            self.assertEqual(list(Path(directory).iterdir()), [target])

    def test_unknown_size_oversized_and_binary_files_are_recorded_not_fatal(self):
        snapshot = external.source_snapshot
        bodies = {"main.py": b"print('kept')\n", "big.json": b"x" * 20, "latin.md": b"caf\xe9\n"}
        files = [{"path": path, "size": None, "url": path} for path in bodies]
        provenance = {"upstream": "https://github.com/example/source", "revision": "abc123",
                      "revision_date": "2026-10-20", "slug": "example/source"}
        def get(url, timeout, max_bytes=None):
            if max_bytes is not None and len(bodies[url]) > max_bytes:
                raise snapshot.OversizedFile(url)
            return bodies[url], {}
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "Fixture.txt"
            with patch.object(snapshot, "_remote_tree", return_value=(provenance, files)), \
                 patch.object(snapshot, "_get", side_effect=get), \
                 patch.object(snapshot, "_MAX_FILE_BYTES", 16):
                snapshot._write_snapshot("https://github.com/example/source", target,
                                         timeout=5, patterns=snapshot.entry_patterns({}))
            text = target.read_text(encoding="utf-8")
        self.assertIn("FILE: main.py\n", text)
        self.assertIn('"skipped": "exceeds 16 bytes"', text)
        self.assertIn('"skipped": "not UTF-8 text"', text)
        self.assertIn('"included_files": 1', text)

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
