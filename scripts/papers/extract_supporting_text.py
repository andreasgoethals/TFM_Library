#!/usr/bin/env python
"""Generate or verify text for explicitly selected supporting references.

Supporting references are outside the Zotero-mirrored TFM corpus in papers/.
Their manifest records the exact Zotero PDF hash and the generated text hash.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'supporting-references' / 'manifest.json'
SUPPORT = (ROOT / 'supporting-references').resolve()

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()

def local_path(value: str) -> Path:
    path = (ROOT / value).resolve()
    if not path.is_relative_to(SUPPORT):
        raise ValueError(f'Supporting path is outside the intended directory: {value}')
    return path

def cleaner():
    spec = importlib.util.spec_from_file_location('tfm_paper_extractor', Path(__file__).with_name('extract_paper_text.py'))
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot load the existing extraction helper')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module._strip_line_number_gutters

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--all', action='store_true', help='Generate all listed text extracts')
    mode.add_argument('--check', action='store_true', help='Check PDF and text hashes without writing')
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    records = manifest['sources']
    assert len({r['zotero_item_key'] for r in records}) == len(records)
    issues = []
    if args.all:
        from pypdf import PdfReader
        strip_gutters = cleaner()
    for record in records:
        pdf, output = local_path(record['pdf']), local_path(record['text'])
        if not pdf.is_file() or sha256(pdf) != record['pdf_sha256']:
            issues.append(f"Missing or changed PDF: {record['pdf']}")
            continue
        if args.all:
            reader = PdfReader(str(pdf), strict=True)
            body = '\n\n'.join(page.extract_text() or '' for page in reader.pages)
            body = ''.join(ch for ch in body if ch in '\n\t' or ord(ch) >= 32)
            body = strip_gutters(body)
            if len(body.strip()) < 500:
                issues.append(f"Insufficient extractable text: {record['pdf']}")
                continue
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(body, encoding='utf-8', newline='\n')
            record['text_sha256'] = sha256(output)
            record['pages'] = len(reader.pages)
        elif not output.is_file():
            issues.append(f"Missing text: {record['text']}")
        elif sha256(output) != record.get('text_sha256'):
            issues.append(f"Changed or stale text: {record['text']}")
        else:
            raw = output.read_bytes()
            try:
                body = raw.decode('utf-8')
                if len(body.strip()) < 500 or b'\r' in raw or any(b < 9 or b == 11 or 13 < b < 32 for b in raw):
                    issues.append(f"Text quality issue: {record['text']}")
            except UnicodeDecodeError:
                issues.append(f"Non-UTF-8 text: {record['text']}")
    if args.all and not issues:
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    for issue in issues:
        print(issue)
    print(f'{len(records)} supporting references; {len(issues)} issue(s)')
    return 1 if issues else 0

if __name__ == '__main__':
    raise SystemExit(main())
