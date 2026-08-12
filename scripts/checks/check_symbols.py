#!/usr/bin/env python
"""Do the code symbols cited in the documents still exist in the dumps?

AGENTS.md rule 4 says to cite the code dumps **by symbol name, never by
line number**, because a refresh moves every line. That rule buys
stability, but it does not make a citation permanent: upstream renames
things, and a refresh silently turns `` `save_tabpfn_model` `` into a
promise the dump no longer keeps. Rule 5 therefore says to spot-check the
cited symbols after every refresh. This is that check, done exhaustively
instead of by spot.

How it decides what to check
----------------------------
A backticked token counts as a symbol worth verifying only if it looks
like code rather than prose: it contains an underscore, a slash, a dot-py,
a call suffix, or internal capitals. Everything else — ordinary words,
document names, prose in backticks for emphasis — is ignored, because a
check that cries wolf is a check nobody runs.

A symbol is attributed to a dump by the section it sits in
(``## `TabICL.txt` ``), by its row in the overview table, or — in
`SUMMARIES.md` and `SYNTHESIS.md` — by a dump filename mentioned in the
same paragraph. Two details matter and both cost false alarms if they are
skipped. Headings that name **several** dumps ("how they relate") are
satisfied if the symbol is in *any* of them. Headings that name **no**
dump end the attribution unless they are nested inside one, so the
symbols in "Refreshing this folder" are not blamed on whichever dump
happened to be discussed above it.

It also enforces rule 4 itself: any `` `Something.txt:1234` `` citation is
reported, since line numbers drift by thousands on every refresh.

Usage::

    python scripts/checks/check_symbols.py
    python scripts/checks/check_symbols.py --verbose     # list every hit too
    python scripts/checks/check_symbols.py --doc REPOSITORIES.md

Exit code 0 when every cited symbol is still present.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.library import REPOSITORIES, ROOT  # noqa: E402

DOCS = ["REPOSITORIES.md", "SUMMARIES.md", "SYNTHESIS.md"]

# Only REPOSITORIES.md is organised dump-by-dump, so only there can a
# symbol be pinned to a particular file. Elsewhere the honest claim is
# "this exists somewhere in the corpus", and checking it against a dump
# guessed from the surrounding paragraph invents failures.
SECTIONED = {"REPOSITORIES.md"}
ANY_DUMP = ("*",)

# Symbols the documents deliberately mention as *not* being in a dump:
# names upstream deleted, paths the refresh filters out, code checked
# against upstream rather than against the snapshot. Each is a real
# sentence in the docs, so silently "fixing" them would be wrong — they
# are listed here with the reason instead, and reported as notes.
ALLOW_MISSING = {
    "preprocess_dummy_data":
        "history note: upstream deleted the hand-rolled training examples",
    "save_path_to_fine_tuned_model":
        "history note: upstream deleted the hand-rolled training examples",
    "tabstar_paper/datasets/annotated/":
        "excluded by the dump's filter (401 per-dataset metadata stubs)",
    "orion_msp/attention.py":
        "compared against upstream, not against the vendored copy",
}

_DUMP = re.compile(r"`([^`]+\.txt)`")
_TICK = re.compile(r"`([^`\n]+)`")
_LINE_CITE = re.compile(r"`([^`\n]+\.txt):(\d+)`")

# A token is code-like if it has any of these shapes.
_CODE_SHAPES = (
    re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\(\)$"),         # foo()
    re.compile(r"^[A-Za-z_][A-Za-z0-9_]*_[A-Za-z0-9_]+$"),  # snake_case
    re.compile(r"^[a-z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*$"),    # camelCase
    re.compile(r"^[A-Z][a-z0-9]+[A-Z][A-Za-z0-9]*$"),       # PascalCase
    re.compile(r"^[\w./-]+\.py$"),                          # a file
    re.compile(r"^[\w.-]+(?:/[\w.-]+)+/?$"),                # a path
)

# Tokens that pass the shape test but are not symbols in any dump: prose
# conventions, external references, and this repository's own furniture.
_IGNORE = {
    "FILE:", "TabPFN", "TabICL", "TabDPT", "TabSTAR", "CausalPFN",
    "PROJECT_SPECIFIC.md", "requirements.txt", "gitingest",
}
_IGNORE_PREFIX = ("papers/", "scripts/", "repositories/", "data/",
                  "https://", "http://", "arXiv:")


def _own_code_symbols() -> set[str]:
    """Identifiers defined by *this* repository's own scripts.

    The documents discuss the maintenance scripts too (``SKIP_NON_GIT``,
    ``--force-shrink``). Those are ours, not upstream's, and looking for
    them inside a code dump is a category error.
    """
    out: set[str] = set()
    for py in (ROOT / "scripts").rglob("*.py"):
        out.update(re.findall(r"^\s*(?:def|class)\s+(\w+)", py.read_text(
            encoding="utf-8", errors="replace"), re.M))
        out.update(re.findall(r"^([A-Z][A-Z0-9_]{3,})\s*[:=]", py.read_text(
            encoding="utf-8", errors="replace"), re.M))
    return out


_OWN = _own_code_symbols()


# `owner/repo` — a GitHub reference, not a path inside a dump. Real
# in-dump paths in these documents always end in a slash or a filename.
_GITHUB_REF = re.compile(r"^[\w.-]+/[\w.-]+$")


def is_symbol(tok: str) -> bool:
    tok = tok.strip()
    if tok in _IGNORE or tok in _OWN or tok.startswith(_IGNORE_PREFIX):
        return False
    if tok.endswith((".txt", ".md", ".pdf", ".ipynb")) or " " in tok:
        return False
    if "XXX" in tok:                       # `stg_XXXXX` — a prose placeholder
        return False
    if _GITHUB_REF.match(tok) and "." not in tok.split("/")[-1]:
        return False
    return any(p.match(tok) for p in _CODE_SHAPES)


def dump_names(s: str) -> list[str]:
    """Dump filenames in a string, without any `repositories/` prefix."""
    return [n.split("/")[-1] for n in _DUMP.findall(s)]


def dump_sections(text: str) -> list[tuple[list[str], str]]:
    """Split a document into ``(dump filenames, body)`` blocks.

    Headings nest: a subsection that names no dump belongs to the dump
    section that encloses it, while a heading at the same or a shallower
    level ends the attribution entirely. Without that rule the symbols
    under "Refreshing this folder" get blamed on whichever dump was
    discussed just above it, which is where most of the false alarms in a
    naive version come from.
    """
    heads = list(re.finditer(r"^(#{2,6})\s+(.*)$", text, re.M))
    out: list[tuple[list[str], str]] = []
    stack: list[tuple[int, list[str]]] = []
    for i, m in enumerate(heads):
        level, names = len(m.group(1)), dump_names(m.group(2))
        while stack and stack[-1][0] >= level:
            stack.pop()
        if names:
            stack.append((level, names))
        current = names or (stack[-1][1] if stack else [])
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        if current:
            out.append((current, text[m.end():end]))
    return out


def paragraph_sections(text: str) -> list[tuple[list[str], str]]:
    """Fallback attribution: any paragraph that names a dump."""
    out = []
    for para in re.split(r"\n\s*\n", text):
        names = dump_names(para)
        if names:
            out.append((names, para))
    return out


def collect(doc: str) -> dict[str, set[str]]:
    """``{symbol: candidate dumps}`` cited in one document.

    The candidates are a *union*, not a conjunction: a symbol documented
    in several places is live if any one of those dumps still contains
    it. Requiring every attribution to hold instead turns one citation
    written loosely — a sentence that names a neighbouring dump — into a
    failure about a symbol that is demonstrably still there.
    """
    text = (ROOT / doc).read_text(encoding="utf-8")
    sections = (dump_sections(text) if doc in SECTIONED
                else [(list(ANY_DUMP), p) for _, p in paragraph_sections(text)])

    cited: dict[str, set[str]] = {}
    for names, body in sections:
        for line in body.split("\n"):
            # A sentence that names a dump ("grep `x/` inside `Y.txt`") is
            # the most specific attribution there is, and it routinely
            # points somewhere other than the enclosing section. Add it to
            # the section's dumps rather than replacing them: candidates
            # are a union, so a wider set can only reduce false alarms.
            here = set(names) | set(dump_names(line))
            for tok in _TICK.findall(line):
                if is_symbol(tok):
                    cited.setdefault(tok.strip().rstrip("()"), set()).update(here)
    return cited


def line_citations() -> list[tuple[str, int, str]]:
    """Every `dump.txt:1234` citation — banned by AGENTS.md rule 4.

    Scanned only in the documents that actually cite code, and only for
    filenames that are real dumps. `README.md` and `AGENTS.md` state the
    rule by quoting a counter-example, so scanning them would report the
    rule itself forever.
    """
    real = {p.name for p in REPOSITORIES.glob("*.txt")}
    out = []
    for doc in DOCS:
        path = ROOT / doc
        if not path.is_file():
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            for m in _LINE_CITE.finditer(line):
                if m.group(1).split("/")[-1] in real:
                    out.append((doc, i, m.group(0)))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--doc", action="append", default=[], choices=DOCS,
                    metavar="DOC", help="check one document (repeatable)")
    ap.add_argument("--verbose", action="store_true",
                    help="also list the symbols that were found")
    args = ap.parse_args(argv)

    cited: dict[str, set[str]] = {}
    for doc in (args.doc or DOCS):
        for sym, names in collect(doc).items():
            cited.setdefault(sym, set()).update(names)

    # read each dump once: several are hundreds of MB
    bodies: dict[str, str | None] = {}

    def body_of(name: str) -> str | None:
        if name not in bodies:
            p = REPOSITORIES / name
            # `TabPFN Wide.txt` is gitignored (>95 MB) and regenerated
            # locally, so its absence is expected, not a failure.
            bodies[name] = (p.read_text(encoding="utf-8", errors="replace")
                            if p.is_file() else None)
        return bodies[name]

    on_disk = sorted(p.name for p in REPOSITORIES.glob("*.txt"))
    per_dump: dict[str, list[str]] = {}
    skipped: set[str] = set()
    missing: list[tuple[str, str]] = []
    notes: list[tuple[str, str]] = []
    for sym in sorted(cited):
        names = on_disk if ANY_DUMP[0] in cited[sym] else sorted(cited[sym])
        skipped.update(n for n in names if body_of(n) is None)
        avail = [n for n in names if body_of(n) is not None]
        if not avail:
            continue
        where = next((n for n in avail if sym in body_of(n)), None)
        if where:
            per_dump.setdefault(where, []).append(sym)
        elif sym in ALLOW_MISSING:
            notes.append((sym, ALLOW_MISSING[sym]))
        else:
            missing.append((", ".join(avail[:3]), sym))

    bar = "-" * 78
    print(bar)
    print(f"  Symbol check   ({len(cited)} distinct symbols cited, "
          f"{len(per_dump)} dump(s) matched)")
    print(bar)
    for name in sorted(per_dump):
        syms = sorted(per_dump[name])
        print(f"  [ ok ] {name:<56} {len(syms)}")
        if args.verbose:
            for s in syms:
                print(f"           found: {s}")
    for where, sym in missing:
        print(f"  [MISS] {sym:<56} not in {where}")

    if skipped:
        print(bar)
        for n in sorted(skipped):
            print(f"  [SKIP] {n:<48} not on disk (gitignored / not dumped)")

    if notes:
        print(bar)
        for sym, why in sorted(set(notes)):
            print(f"  [note] absent on purpose: {sym}")
            print(f"         {why}")

    bad_cites = line_citations()
    if bad_cites:
        print(bar)
        print("  LINE-NUMBER CITATIONS (AGENTS.md rule 4 — they drift on")
        print("  every refresh; cite the symbol instead):")
        for doc, i, cite in bad_cites:
            print(f"    {doc}:{i}  {cite}")

    print(bar)
    if missing:
        print(f"  {len(missing)} cited symbol(s) exist in no dump that names them.")
        print("  Either upstream renamed them — update the document — or the")
        print("  refresh filtered out the file that held them.")
    else:
        print("  Every cited symbol is still present.")
    print(bar)
    return 1 if (missing or bad_cites) else 0


if __name__ == "__main__":
    raise SystemExit(main())
