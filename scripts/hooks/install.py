#!/usr/bin/env python
"""Install (or remove) this repository's git hooks.

Git does not track `.git/hooks/`, so a hook committed to the repository
does nothing until someone points git at it. This does that by setting
``core.hooksPath`` to ``scripts/hooks`` — one local config value, no
copied files that can silently drift from the version in git.

``core.hooksPath`` redirects **all** hooks for this repository, so if you
later add another hook it must live in the same folder. That is the trade
for having the hook itself under version control, and it is the right one
here: there is exactly one hook, and it should be reviewable.

Usage::

    python scripts/hooks/install.py            # install
    python scripts/hooks/install.py --status   # what is configured now
    python scripts/hooks/install.py --uninstall

Nothing here is required to use the library — the same checks run from
``maintain.py``. The hook only moves them earlier.
"""

from __future__ import annotations

import argparse
import os
import stat
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.library import ROOT  # noqa: E402

HOOKS = Path(__file__).resolve().parent
REL = "scripts/hooks"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(ROOT), capture_output=True,
                          text=True, encoding="utf-8").stdout.strip()


def current() -> str:
    return git("config", "--local", "--get", "core.hooksPath")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--uninstall", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args(argv)

    bar = "-" * 70
    print(bar)
    if args.status:
        now = current()
        print(f"  core.hooksPath = {now or '(unset — hooks are not installed)'}")
        for h in sorted(HOOKS.iterdir()):
            if h.is_file() and not h.suffix:
                print(f"  available hook: {h.name}")
        print(bar)
        return 0

    if args.uninstall:
        subprocess.run(["git", "config", "--local", "--unset", "core.hooksPath"],
                       cwd=str(ROOT))
        print("  Removed core.hooksPath. The hooks no longer run.")
        print(bar)
        return 0

    subprocess.run(["git", "config", "--local", "core.hooksPath", REL],
                   cwd=str(ROOT), check=True)
    # Git for Windows runs hooks through its bundled sh, which honours the
    # executable bit on platforms that have one; setting it is harmless
    # where it is meaningless.
    for h in HOOKS.iterdir():
        if h.is_file() and not h.suffix:
            os.chmod(h, os.stat(h).st_mode | stat.S_IXUSR | stat.S_IXGRP)

    print(f"  core.hooksPath -> {REL}")
    print("  Installed. Every commit now runs the offline document checks")
    print("  (and the symbol check when a document or dump is staged).")
    print()
    print("  Bypass once :  git commit --no-verify")
    print("  Remove      :  python scripts/hooks/install.py --uninstall")
    print(bar)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
