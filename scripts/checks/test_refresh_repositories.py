"""Regression for ordered Git ignore negation being lost by the scraper."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "dumps"))
import refresh_repositories as refresh


class RefreshTests(unittest.TestCase):
    def test_tracked_reports_and_configs_survive_upstream_negated_ignore_rules(self):
        from gitingest import ingest
        from loguru import logger
        logger.disable("gitingest")
        entry = refresh.REPOSITORIES["On Finetuning Tabular Foundation Models.txt"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "--quiet", str(root)], check=True)
            (root / "exp/run").mkdir(parents=True)
            (root / "data").mkdir()
            sources = {
                ".gitignore": "exp/**/*.*\n!exp/**/report.json\n!exp/**/*.toml\n",
                "exp/run/report.json": '{"score": 0.9}\n',
                "exp/run/config.toml": "seed = 0\n",
                "model.py": "def predict(): pass\n",
                "data/private.json": '{"excluded": true}\n',
                "exp/run/weights.pt": "not source\n",
            }
            for name, content in sources.items():
                (root / name).write_text(content)
            _, _, content = ingest(source=str(root), output=None, **refresh.entry_patterns(entry))
            for name in ("exp/run/report.json", "exp/run/config.toml", "model.py"):
                self.assertIn(f"FILE: {name}", content)
            self.assertNotIn("FILE: data/private.json", content)
            self.assertNotIn("FILE: exp/run/weights.pt", content)


if __name__ == "__main__":
    unittest.main()
