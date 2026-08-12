#!/usr/bin/env python
"""Push this library's current commit out to every downstream project.

**This folder is the ground truth.** The script finds every repository on
disk that embeds this library as a git submodule, and moves each one's pin
to the commit that is checked out *here*.

How it finds them
-----------------
It scans the search roots (default: the parent of this repository, i.e.
the folder holding all your projects) for ``.gitmodules`` files that
reference this repository's ``origin`` URL, matching on the normalised
``owner/name`` so that ``https://…/TFM_Library.git``, an SSH remote, and a
different capitalisation all resolve to the same library.

The safety rule that matters
----------------------------
A downstream pin is a **commit id that must exist on the remote**, because
that is where a collaborator's ``git submodule update --init`` will look
for it. So the script refuses to run when this repository has uncommitted
changes or unpushed commits — propagating then would either pin work that
nobody else can fetch, or silently pin a *stale* commit while your newest
work sits uncommitted. Override with ``--allow-dirty`` only if you know
why you want that.

What it does per project
------------------------
1. ``git fetch`` inside the submodule, so the target commit is available.
2. Check out this library's exact HEAD there (not ``--remote``, which
   would follow the branch tip and could differ from what you have).
3. Stage and commit **only the submodule path**, so unrelated work in
   progress in that project is never swept into the commit.
4. Leave pushing to you, unless ``--push`` is given.

Usage::

    python scripts/propagate_to_downstream.py --dry-run   # show the plan
    python scripts/propagate_to_downstream.py             # update + commit
    python scripts/propagate_to_downstream.py --push      # also push
    python scripts/propagate_to_downstream.py --root "D:/other/projects"

Exit code 0 if every project ends up pinned to this commit.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]


def git(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(cwd), check=check,
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def normalise_remote(url: str) -> str:
    """``owner/name`` in lower case, from any git remote spelling."""
    u = url.strip().rstrip("/")
    u = re.sub(r"\.git$", "", u)
    u = re.sub(r"^git@([^:]+):", r"https://\1/", u)     # SSH -> HTTPS shape
    parts = [p for p in u.split("/") if p]
    return "/".join(parts[-2:]).lower() if len(parts) >= 2 else u.lower()


class Project:
    def __init__(self, repo: Path, sub_path: str) -> None:
        self.repo = repo
        self.sub_path = sub_path
        self.status = "pending"
        self.detail = ""

    @property
    def sub_dir(self) -> Path:
        return self.repo / self.sub_path

    def pinned_sha(self) -> str | None:
        r = git("ls-tree", "HEAD", self.sub_path, cwd=self.repo, check=False)
        m = re.search(r"^160000 commit ([0-9a-f]{40})", r.stdout.strip())
        return m.group(1) if m else None


def discover(roots: list[Path], library_key: str, depth: int) -> list[Project]:
    found: list[Project] = []
    seen: set[Path] = set()
    for root in roots:
        if not root.is_dir():
            continue
        # every depth from 0 (the root itself) up to `depth`, not just `depth`
        patterns = ["/".join(["*"] * d + [".gitmodules"]) for d in range(depth + 1)]
        for gm in sorted({g for pat in patterns for g in root.glob(pat)}):
            repo = gm.parent
            if repo.resolve() == _ROOT.resolve() or repo in seen:
                continue
            text = gm.read_text(encoding="utf-8", errors="replace")
            blocks = re.findall(
                r'\[submodule "[^"]+"\][^\[]*', text, re.S)
            for b in blocks:
                url = re.search(r"url\s*=\s*(\S+)", b)
                path = re.search(r"path\s*=\s*(\S+)", b)
                if url and path and normalise_remote(url.group(1)) == library_key:
                    seen.add(repo)
                    found.append(Project(repo, path.group(1)))
    return found


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", action="append", default=None, metavar="DIR",
                    help="where to look for projects (repeatable; default: "
                         "the parent folder of this repository)")
    ap.add_argument("--depth", type=int, default=3, metavar="N",
                    help="how many directory levels below each root to scan "
                         "for .gitmodules (default: 3)")
    ap.add_argument("--dry-run", action="store_true",
                    help="report the plan, change nothing")
    ap.add_argument("--push", action="store_true",
                    help="also push each downstream project after committing")
    ap.add_argument("--allow-dirty", action="store_true",
                    help="propagate even if this repository is dirty or "
                         "unpushed (unsafe: the pin may not exist on origin)")
    ap.add_argument("--message", default=None, metavar="MSG",
                    help="commit message for the pin bump")
    args = ap.parse_args(argv)

    # ---- this repository: identity and readiness -------------------------
    try:
        origin = git("remote", "get-url", "origin", cwd=_ROOT).stdout.strip()
    except subprocess.CalledProcessError:
        print("ERROR: this repository has no 'origin' remote.", file=sys.stderr)
        return 2
    key = normalise_remote(origin)
    head = git("rev-parse", "HEAD", cwd=_ROOT).stdout.strip()
    short = head[:7]

    dirty = bool(git("status", "--porcelain", cwd=_ROOT).stdout.strip())
    unpushed = git("log", "--oneline", "@{u}..HEAD", cwd=_ROOT,
                   check=False).stdout.strip()

    bar = "=" * 78
    print(bar)
    print(f"  Propagating {key} @ {short}")
    print(f"  {git('log', '-1', '--pretty=%s', cwd=_ROOT).stdout.strip()}")
    print(bar)

    if (dirty or unpushed) and not args.allow_dirty:
        if dirty:
            print("  REFUSING: this repository has uncommitted changes.")
            print("  Commit them first — otherwise you would pin a commit that")
            print("  does not include your newest work.")
        if unpushed:
            print("  REFUSING: this repository has unpushed commits:")
            for line in unpushed.splitlines():
                print(f"    {line}")
            print("  Push first — a pin must exist on origin, or collaborators")
            print("  cannot fetch it.")
        print("  (override with --allow-dirty if you are sure)")
        return 2

    # ---- find the consumers ---------------------------------------------
    roots = [Path(r) for r in args.root] if args.root else [_ROOT.parent]
    projects = discover(roots, key, args.depth)
    if not projects:
        print(f"  No downstream projects found under: "
              f"{', '.join(str(r) for r in roots)}")
        return 0

    # ---- update each -----------------------------------------------------
    for p in projects:
        before = p.pinned_sha()
        label = f"{p.repo.name}/{p.sub_path}"
        if before == head:
            p.status, p.detail = "current", f"already at {short}"
            print(f"\n  [=] {label}: {p.detail}")
            continue
        if not p.sub_dir.is_dir():
            p.status, p.detail = "missing", "submodule folder not initialised"
            print(f"\n  [!] {label}: {p.detail} — run 'git submodule update --init'")
            continue

        print(f"\n  [>] {label}: {(before or 'unpinned')[:7]} -> {short}")
        if args.dry_run:
            p.status, p.detail = "would update", f"{(before or '?')[:7]} -> {short}"
            continue
        try:
            git("fetch", "origin", cwd=p.sub_dir)
            git("checkout", "--quiet", head, cwd=p.sub_dir)
            git("add", "--", p.sub_path, cwd=p.repo)
            staged = git("diff", "--cached", "--name-only", cwd=p.repo).stdout
            if p.sub_path.replace("\\", "/") in staged.replace("\\", "/"):
                msg = args.message or f"Bump {p.sub_path} pin to {short}"
                # path-limited commit: never sweeps up unrelated dirty files
                git("commit", "-m", msg, "--", p.sub_path, cwd=p.repo)
                p.status, p.detail = "updated", f"committed {short}"
            else:
                p.status, p.detail = "current", "nothing staged"
            if args.push and p.status == "updated":
                git("push", cwd=p.repo)
                p.detail += " + pushed"
        except subprocess.CalledProcessError as exc:
            p.status = "FAILED"
            p.detail = (exc.stderr or exc.stdout or str(exc)).strip().splitlines()[-1]
            print(f"      ERROR: {p.detail}")

    # ---- summary ---------------------------------------------------------
    print(f"\n{bar}")
    print("  SUMMARY")
    print(bar)
    width = max(len(f"{p.repo.name}/{p.sub_path}") for p in projects)
    for p in projects:
        tag = {"updated": "UPDATED", "current": "  OK   ",
               "would update": "  PLAN ", "missing": "MISSING",
               "FAILED": "FAILED "}.get(p.status, p.status)
        print(f"  [{tag}]  {f'{p.repo.name}/{p.sub_path}'.ljust(width)}   {p.detail}")
    print(bar)
    failed = [p for p in projects if p.status in ("FAILED", "missing")]
    if args.dry_run:
        print("  Dry run — nothing was changed.")
    elif not args.push:
        updated = [p for p in projects if p.status == "updated"]
        if updated:
            print("  Committed locally. Push each project when ready, or re-run "
                  "with --push.")
    print(bar)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
