#!/usr/bin/env python
"""Run every maintenance task for this library and print one report.

Stages, in order (cheap checks first so failures surface fast):

===============  ==============================================  ==========
Stage            What it does                                    Mutating?
===============  ==============================================  ==========
``text``         fill in any missing ``papers/text/**`` files     yes
``zotero``       compare ``papers/`` with the Zotero collection   no
``versions``     ask arXiv whether newer paper versions exist     no
``repos``        re-dump every ``repositories/*.txt``             yes
===============  ==============================================  ==========

``repos`` runs last because it is by far the slowest (network clones of
every upstream repository) and the least urgent.

Usage::

    python scripts/maintain.py                    # everything
    python scripts/maintain.py --check-only       # no writes anywhere
    python scripts/maintain.py --skip repos       # everything but the dumps
    python scripts/maintain.py --only zotero      # a single stage

Exit code is 0 only if every stage reported clean.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = _ROOT / "scripts"

# stage -> (argv, mutating, one-line description)
STAGES: dict[str, tuple[list[str], bool, str]] = {
    "text": ([sys.executable, str(_SCRIPTS / "extract_paper_text.py"), "--all"],
             True, "extract text for any paper missing it"),
    "zotero": ([sys.executable, str(_SCRIPTS / "check_zotero_sync.py")],
               False, "Zotero <-> library consistency"),
    "versions": ([sys.executable, str(_SCRIPTS / "check_paper_versions.py")],
                 False, "newer arXiv versions of held papers"),
    "repos": ([sys.executable, str(_SCRIPTS / "refresh_repositories.py")],
              True, "re-dump repositories/*.txt from upstream"),
}

# read-only substitute used by --check-only
CHECK_ONLY_OVERRIDE: dict[str, list[str]] = {
    "text": [sys.executable, str(_SCRIPTS / "extract_paper_text.py"), "--check"],
}


def run_stage(name: str, argv: list[str]) -> tuple[int, float, str]:
    t0 = time.monotonic()
    proc = subprocess.run(argv, cwd=_ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, time.monotonic() - t0, out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check-only", action="store_true",
                    help="run nothing that writes: report only")
    ap.add_argument("--skip", action="append", default=[], metavar="STAGE",
                    choices=list(STAGES), help="skip a stage (repeatable)")
    ap.add_argument("--only", action="append", default=[], metavar="STAGE",
                    choices=list(STAGES), help="run only this stage (repeatable)")
    ap.add_argument("--quiet", action="store_true",
                    help="suppress per-stage output, print the summary only")
    args = ap.parse_args(argv)

    selected = [s for s in STAGES
                if (not args.only or s in args.only) and s not in args.skip]
    if args.check_only:
        selected = [s for s in selected
                    if not STAGES[s][1] or s in CHECK_ONLY_OVERRIDE]

    bar = "=" * 78
    print(bar)
    print("  TFM Library maintenance"
          f"{'  (check-only: nothing will be written)' if args.check_only else ''}")
    print(f"  stages: {', '.join(selected) or '(none)'}")
    print(bar, flush=True)

    results: list[tuple[str, int, float]] = []
    for name in selected:
        cmd, _, desc = STAGES[name]
        if args.check_only and name in CHECK_ONLY_OVERRIDE:
            cmd = CHECK_ONLY_OVERRIDE[name]
        print(f"\n>>> [{name}] {desc}", flush=True)
        code, secs, out = run_stage(name, cmd)
        if not args.quiet and out.strip():
            print("\n".join("    " + l for l in out.rstrip().split("\n")))
        print(f"    ({'clean' if code == 0 else f'issues (exit {code})'}"
              f" in {secs:.1f}s)", flush=True)
        results.append((name, code, secs))

    print(f"\n{bar}")
    print("  SUMMARY")
    print(bar)
    if not results:
        print("  no stages selected")
        return 0
    width = max(len(n) for n, _, _ in results)
    for name, code, secs in results:
        status = "   OK    " if code == 0 else "ATTENTION"
        print(f"  [{status}]  {name.ljust(width)}   {secs:6.1f}s"
              f"   {STAGES[name][2]}")
    failed = [n for n, c, _ in results if c != 0]
    print(bar)
    if failed:
        print(f"  {len(failed)} stage(s) need attention: {', '.join(failed)}")
        print("  Scroll up for the detail — nothing was fixed automatically")
        print("  except missing text extractions.")
    else:
        print("  Everything is consistent.")
    print(bar)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
