"""Refresh official docs, model cards and the filtered TabForestPFN source tree."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlparse
from urllib.request import Request, urlopen

sys.dont_write_bytecode = True
import source_snapshot

ROOT = Path(__file__).resolve().parents[2]
DOCS_SOURCE = "https://docs.priorlabs.ai/llms-full.txt"


def get(url):
    with urlopen(Request(url, headers={"User-Agent": "tfm-library-maintenance/1.0"}), timeout=60) as response:
        body = response.read(10_000_001)
    if len(body) > 10_000_000:
        raise ValueError(f"Oversized source: {url}")
    text = body.decode("utf-8")
    if re.search(r"<!doctype html|<html\b", text[:500], re.I):
        raise ValueError(f"Expected source text, received HTML: {url}")
    return text


def docs():
    # The provider's complete export avoids navigation links that redirect to
    # marketing HTML rather than actual documentation pages.
    body = get(DOCS_SOURCE)
    urls = sorted(set(re.findall(r"(?m)^Source: (https://docs\.priorlabs\.ai/\S+)", body)))
    required = {"overview", "models", "capabilities/classification"}
    if len(urls) < 20 or not required <= {urlparse(url).path.lstrip("/") for url in urls}:
        raise ValueError("Incomplete official documentation export")
    header = {"source": DOCS_SOURCE, "retrieved_utc": datetime.now(timezone.utc).isoformat(),
              "source_pages": urls, "sha256": hashlib.sha256(body.encode()).hexdigest(),
              "note": "Official complete Markdown export; no Git revision is published."}
    body = re.sub(r"(?m)^Source: (https://docs\.priorlabs\.ai/\S+)",
                  lambda m: f"FILE: {urlparse(m[1]).path.lstrip('/')}.md\nSource: {m[1]}", body)
    return "TFM Library official documentation snapshot\n" + json.dumps(header, indent=2) + "\n\n" + body


def cards():
    parts = []
    for slug in ["Prior-Labs/tabpfn_2_5", "Prior-Labs/tabpfn_2_6"]:
        info = json.loads(get(f"https://huggingface.co/api/models/{slug}"))
        revision = info["sha"]
        url = f"https://huggingface.co/{slug}/raw/{revision}/README.md"
        body = get(url)
        if len(body) < 1000 or "tabpfn" not in body.casefold():
            raise ValueError(f"Incomplete model card: {slug}")
        parts.append(f"MODEL: {slug}\nRevision: {revision}\nSource: {url}\n"
                     f"SHA-256: {hashlib.sha256(body.encode()).hexdigest()}\n\n{body}")
    return "TFM Library official model cards\n\n" + "\n\n".join(parts)


def replace(target: Path, content: str, *, force_shrink=False):
    """Never replace a good snapshot with an empty, partial or unexpectedly tiny result."""
    body = content.encode("utf-8")
    if len(body) < 1000 or (target.exists() and not force_shrink and len(body) < target.stat().st_size * 0.5):
        raise ValueError(f"Shrink guard: preserve {target.name} until the source change is reviewed")
    if source_snapshot.unchanged_except_timestamp(body, target):
        return  # Only retrieved_utc differs: leave the existing snapshot untouched.
    fd, name = tempfile.mkstemp(prefix=".source-", suffix=".tmp", dir=target.parent)
    os.close(fd)
    temp = Path(name)
    try:
        temp.write_bytes(body)
        os.replace(temp, target)
    finally:
        temp.unlink(missing_ok=True)


def update_inventory_counts():
    path = ROOT / "REPOSITORIES.md"
    text = path.read_text(encoding="utf-8")
    def row(match):
        snapshot = ROOT / "repositories" / match[1]
        if not snapshot.is_file():
            return match[0]
        with snapshot.open(encoding="utf-8") as stream:
            count = sum(1 for _ in stream)
        return f"| `{match[1]}` | {count:,} |"
    updated = re.sub(r"\| `([^`]+\.txt)` \| [\d,]+ \|", row, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8", newline="\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", choices=["docs", "cards", "tabforest"], action="append")
    parser.add_argument("--force-shrink", action="store_true",
                        help="Accept a reviewed source reduction; still reject incomplete sources")
    args = parser.parse_args(argv)
    try:
        from loguru import logger
        logger.disable("gitingest")
    except ImportError:
        pass
    result = subprocess.run(["git", "rev-parse", "--show-superproject-working-tree"],
                            cwd=ROOT, capture_output=True, text=True)
    if result.returncode or result.stdout.strip():
        parser.error("Refresh only in an independent canonical checkout")
    failures = 0
    for name in args.only or ["docs", "cards", "tabforest"]:
        try:
            if name == "tabforest":
                entry = source_snapshot.REPOSITORIES["TabForestPFN.txt"]
                result = source_snapshot.refresh_one(
                    "TabForestPFN.txt", entry["url"], repositories_dir=ROOT / "repositories",
                    patterns=source_snapshot.entry_patterns(entry), force_shrink=args.force_shrink)
                if result.status != "OK":
                    raise ValueError(result.reason)
            else:
                filename = "TabPFN Docs.txt" if name == "docs" else "Huggingface TabPFN.txt"
                replace(ROOT / "repositories" / filename, docs() if name == "docs" else cards(),
                        force_shrink=args.force_shrink)
            print(f"[OK] {name}", flush=True)
        except Exception as exc:
            failures += 1
            print(f"[FAIL] {name}: {exc}; existing snapshot preserved", flush=True)
    if not failures:
        update_inventory_counts()
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
