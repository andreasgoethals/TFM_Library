"""Refresh the flat-text snapshots under ``repositories/`` via gitingest.

This module is the canonical way to bring every ``repositories/*.txt``
file back in sync with its upstream GitHub source. Each entry in the
:data:`REPOSITORIES` mapping below pairs a **filename that already
exists in** ``repositories/`` with the GitHub URL it was originally
dumped from. Running this script overwrites every listed file with a
fresh `gitingest <https://github.com/coderamp-labs/gitingest>`_ dump
**of the exact same filename** — so existing grep paths in the rest of
the codebase keep resolving.

Why not auto-derive the URLs from the existing files?
    The pretty filenames (``NanoTabPFN.txt``) don't encode the
    upstream slug, and the flattened directory tree at the top of each
    file (``automl-nanotabpfn/``) is case-lossy. An explicit mapping is
    the only correct option — and ``REPOSITORIES.md`` (repo root) is
    where the canonical URLs are documented anyway.

Skipped on purpose
    :data:`SKIP_NON_GIT` lists files whose upstream is not a Git repo
    (Hugging Face model card, public docs site without a GitHub mirror,
    …). :data:`SKIP_MANUAL` lists Git repos too large for gitingest's
    clone timeout, refreshed by hand with the recipe below. Both print as
    ``SKIP`` in the summary so it's clear they were intentionally not
    touched — neither is an error.

Safety guards
    * **Atomic swap.** Each refresh writes to a sibling temp file and
      only ``os.replace``-swaps it in on success. If
      ``gitingest.ingest()`` raises (network flake, rate limit, deleted
      repo, …), the existing ``.txt`` is left untouched.
    * **Shrink guard.** If the new file is < 50 % of the size of the
      existing snapshot, the swap is refused and the old file is kept.
      This catches the case where a repo has been gutted, replaced
      with a stub, or moved private. Pass ``--force-shrink`` to
      override (rare; use only when a legitimate slim-down is
      expected).

Running it
    Press *play* in your IDE on this file → refreshes every entry.
    Equivalent CLI calls::

        python scripts/dumps/refresh_repositories.py
        python scripts/dumps/refresh_repositories.py --only "NanoTabPFN.txt"
        python scripts/dumps/refresh_repositories.py --only NanoTabPFN     # .txt added for you
        python scripts/dumps/refresh_repositories.py --only "TabPFN .txt" --only "PFNS.txt"
        python scripts/dumps/refresh_repositories.py --force-shrink

Very large repositories
    gitingest clones before it filters, and the installed release
    hardcodes a 60 s clone timeout that ``--timeout`` cannot raise. A
    repository whose *history* is large therefore fails even when the
    files you want are tiny (``TabForestPFN`` is 1.36 GB of experiment
    artifacts around 1.2 MB of Python). Workaround — sparse-clone the
    source files yourself, then point ``ingest`` at the local directory,
    which has no timeout::

        git clone --depth=1 --filter=blob:none --no-checkout <url> /tmp/x
        cd /tmp/x && git sparse-checkout init --no-cone
        git sparse-checkout set '/*.py' '/*.md' '<pkg>/**/*.py' && git checkout
        python -c "from gitingest import ingest; ingest(source='/tmp/x', \\
            output='repositories/<Name>.txt', include_patterns={'*.py','*.md'})"

    Then fix the first tree line to the upstream slug
    (``felixdenbreejen-tabforestpfn/``) so the dump looks like the others.

Dependencies
    ``pip install -r requirements.txt``  (gitingest, pypdf).
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
import warnings
from pathlib import Path

LOGGER = logging.getLogger(__name__)

# Refuse to swap if the new dump is below this fraction of the existing one.
_SHRINK_GUARD_RATIO = 0.5

# Default per-repository ingest timeout (seconds). Some repos
# (VscDocumentation in particular) are slow to clone — bump from
# gitingest's stock 60s default. Can be overridden with `--timeout`.
_DEFAULT_TIMEOUT_SECONDS = 180


# --------------------------------------------------------------------------- #
# Windows / asyncio teardown noise
# --------------------------------------------------------------------------- #
#
# gitingest runs `git clone` through an asyncio subprocess transport. On
# Windows + Python 3.12, the ProactorEventLoop transports occasionally
# raise during interpreter shutdown — `RuntimeError: Event loop is closed`
# and `ValueError: I/O operation on closed pipe`. These are cosmetic,
# the actual subprocess already completed, and the cleanup happens AFTER
# `_print_summary` has written the user-visible result. Swallow them so
# the summary stays clean.


_NOISY_SHUTDOWN_MARKERS = (
    "Event loop is closed",
    "I/O operation on closed pipe",
    "unclosed transport",
)


def _install_quiet_async_shutdown() -> None:
    """Install a ``sys.unraisablehook`` that swallows asyncio teardown noise.

    Only suppresses messages that match the well-known set of cosmetic
    shutdown traces; any other unraisable exception still surfaces via
    the default hook.
    """
    orig_hook = sys.unraisablehook

    def _hook(unraisable):
        err = unraisable.exc_value
        msg = str(err) if err is not None else ""
        if any(marker in msg for marker in _NOISY_SHUTDOWN_MARKERS):
            return  # silently drop
        orig_hook(unraisable)

    sys.unraisablehook = _hook
    # Same warnings, different surface — ResourceWarning sometimes fires
    # before the transport raises. Filter only the ones we know about.
    warnings.filterwarnings(
        "ignore",
        category=ResourceWarning,
        message=".*unclosed.*transport.*",
    )


# --------------------------------------------------------------------------- #
# Mapping: filename in repositories/  →  upstream GitHub URL
# --------------------------------------------------------------------------- #
#
# Edit this dict to fix a wrong URL or to add a new repo. Filenames are
# matched exactly (case + spaces + trailing dot extension all matter),
# and **the script never renames the output** — so dropping a new entry
# in here is enough to make `git pull && python refresh_repositories.py`
# bring in a new snapshot under its existing name.
#
# Sources cross-checked against REPOSITORIES.md (repo root).
#
# A value is either a bare URL string, or a dict for repositories that need
# file filtering:
#
#     "Name.txt": {"url": "https://github.com/o/r",
#                  "include": {"*.py", "*.md"},     # only these
#                  "exclude": {"outputs/*"},        # drop these
#                  "note": "why the filter exists"}
#
# Filtering matters more than it sounds: several TFM repositories commit
# gigabytes of experiment artifacts, model checkpoints, or per-dataset
# metadata stubs next to a few hundred KB of actual source. An unfiltered
# dump of those is useless to grep and dwarfs the rest of this folder.

_PY_DOCS = {"*.py", "*.md", "*.toml", "*.txt", "*.yaml", "*.yml", "*.cfg", "*.ipynb"}

REPOSITORIES: dict[str, str | dict] = {
    "CausalPFN.txt": {
        # Inference + estimation only (no prior generator / pretraining).
        # ~175 MB of the repo is benchmark data: 201 realcause CSVs and
        # IHDP .npz archives. Code alone is well under 1 MB.
        "url": "https://github.com/vdblm/CausalPFN",
        "include": _PY_DOCS,
        "note": "code only; excludes ~175 MB of benchmark CSV/npz data",
    },
    "LoCalPFN.txt":
        # Tiny and entirely unique: retrieval + fine-tuning logic in ~8
        # Python files. The repo's bulk is one committed TabPFN v1
        # checkpoint (~103 MB), which the include-filter drops.
        {"url": "https://github.com/layer6ai-labs/LoCalPFN",
         "include": _PY_DOCS,
         "note": "code only; excludes the committed 103 MB v1 checkpoint"},
    "NanoTabPFN.txt":
        "https://github.com/automl/nanoTabPFN",
    "NanoTabICL.txt": {
        # TabICLv2's own release (the paper points here): the open
        # synthetic-data engine and pretraining code, not just inference.
        "url": "https://github.com/soda-inria/nanotabicl",
        "note": "TabICLv2 release — prior generator + pretraining code",
    },
    "On Finetuning Tabular Foundation Models.txt":
        "https://github.com/yandex-research/tabpfn-finetuning",
    "PFNS.txt":
        # automl/PFNs was moved to SamuelGabriel/PFNs; use the new canonical
        # URL directly rather than relying on the GitHub redirect.
        "https://github.com/SamuelGabriel/PFNs",
    "PFNs4BO.txt":
        "https://github.com/automl/PFNs4BO",
    "TabDPT.txt":
        "https://github.com/layer6ai-labs/TabDPT-inference",
    "TabICL.txt": {
        # Fully open TFM: inference, weights, synthetic-data engine and
        # pretraining code. High grep value precisely because the
        # pretraining path is public, unlike the TabPFN line.
        "url": "https://github.com/soda-inria/tabicl",
        "note": "fully open — includes the prior generator and pretraining",
    },
    "TabPFN .txt":                              # the trailing space is intentional
        "https://github.com/PriorLabs/tabPFN",
    "TabPFN Client.txt":
        "https://github.com/PriorLabs/tabpfn-client",
    "TabPFN Drift-Resilient.txt":
        "https://github.com/automl/Drift-Resilient_TabPFN",
    "TabPFN Extensions.txt":
        "https://github.com/PriorLabs/tabpfn-extensions",
    "TabPFN V2 Finetuning.txt":
        # Sub-path of the main TabPFN repo (the examples/ folder).
        # gitingest's parse_remote_repo understands /tree/<branch>/<path>.
        "https://github.com/PriorLabs/TabPFN/tree/main/examples",
    "TabPFN Wide.txt":
        # Canonical upstream for the TabPFN-Wide paper (Kolberg et al. 2026).
        "https://github.com/not-a-feature/TabPFN-Wide",
    "TabSTAR.txt": {
        # Complete text-aware stack: pretraining, LoRA finetuning, and
        # baseline adapters. NOTE the default branch is `master`, not
        # `main` — a /tree/main/ URL 404s here.
        # 401 of its 536 .py files are per-dataset metadata stubs under
        # tabstar_paper/datasets/annotated/ (~8.6 MB of noise).
        "url": "https://github.com/alanarazi7/TabSTAR",
        "include": _PY_DOCS,
        "exclude": {"tabstar_paper/datasets/annotated/*"},
        "note": "excludes 401 per-dataset metadata stubs; branch is master",
    },
    "TabTune.txt":
        # Vendors complete copies of ~13 other TFMs under tabtune/models/ —
        # see the note in REPOSITORIES.md before adding any new TFM dump.
        "https://github.com/Lexsi-Labs/TabTune",
    "TransformersCanDoBayesianInference.txt":
        # The ORIGINAL (unmaintained) code release of the 2021 PFN paper —
        # NOT the maintained successor (SamuelGabriel/PFNs, see PFNS.txt).
        # Mapping it to the successor (as before 2026-07-17) silently
        # turned this file into a byte-duplicate of PFNS.txt and lost the
        # paper-era snapshot it exists to preserve.
        "https://github.com/automl/TransformersCanDoBayesianInference",
    "VSC Documentation.txt":
        "https://github.com/hpcleuven/VscDocumentation",
}

# Files whose upstream is a Git repo but is too large for gitingest's
# hardcoded 60 s clone timeout (which --timeout cannot raise). They are
# refreshed by hand with the sparse-clone recipe in the module docstring, so
# they are reported as SKIP rather than failing every maintenance run.
SKIP_MANUAL: dict[str, str] = {
    "TabForestPFN.txt":
        "upstream is ~1.36 GB (19.5k files of experiment artifacts around "
        "~1.2 MB of Python), so gitingest's 60 s clone timeout always trips. "
        "Refresh with the sparse-clone recipe in this module's docstring: "
        "git clone --depth=1 --filter=blob:none --no-checkout + "
        "git sparse-checkout set '/*.py' '/*.md' 'tabularbench/**/*.py', then "
        "ingest the local directory. Upstream is dead since 2024-05, so this "
        "rarely needs doing.",
}

# Files that exist in repositories/ but cannot be refreshed by gitingest.
# Each entry maps the filename to a short human-readable reason; the
# summary prints both. The existing on-disk file is never touched.
SKIP_NON_GIT: dict[str, str] = {
    "Huggingface TabPFN.txt":
        "Hugging Face model card; not a git repo. "
        "Refresh manually from https://huggingface.co/Prior-Labs/tabpfn_2_5 "
        "and https://huggingface.co/Prior-Labs/tabpfn_2_6.",
    "TabPFN Docs.txt":
        "Prior Labs no longer publishes the docs GitHub source. "
        "Refresh manually from https://docs.priorlabs.ai/overview.",
}


def _default_repositories_dir() -> Path:
    """Resolve ``<repo-root>/repositories`` from this file's location.

    Layout assumed:  ``<repo-root>/scripts/dumps/refresh_repositories.py``.
    """
    return Path(__file__).resolve().parents[2] / "repositories"


def _silence_gitingest_logging() -> None:
    """Mute gitingest's verbose loguru output.

    gitingest streams ~15 INFO lines per repo via loguru. For interactive
    use we only care about the final outcome, so suppress those entirely.
    """
    # Stdlib bridge — covers gitingest's own logger and the noisy HTTP
    # request logs that show up as `logging:callHandlers:1762`.
    logging.getLogger("gitingest").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    # Native loguru sink — gitingest also logs through loguru directly.
    try:
        from loguru import logger as _loguru_logger
        _loguru_logger.disable("gitingest")
    except ImportError:                                            # pragma: no cover
        pass


# --------------------------------------------------------------------------- #
# Result records
# --------------------------------------------------------------------------- #


class _Result:
    """One row of the final summary table."""

    __slots__ = ("filename", "url", "status", "size_kb", "elapsed", "reason")

    def __init__(
        self,
        filename: str,
        url: str | None,
        status: str,                     # "OK" | "FAIL" | "SKIP"
        *,
        size_kb: float | None = None,
        elapsed: float | None = None,
        reason: str | None = None,
    ) -> None:
        self.filename = filename
        self.url      = url
        self.status   = status
        self.size_kb  = size_kb
        self.elapsed  = elapsed
        self.reason   = reason


# --------------------------------------------------------------------------- #
# One-file refresh (atomic + shrink-guard)
# --------------------------------------------------------------------------- #


def entry_url(entry: str | dict) -> str:
    """URL of a REPOSITORIES value, which may be a bare string or a dict."""
    return entry if isinstance(entry, str) else entry["url"]


def entry_patterns(entry: str | dict) -> dict[str, set[str]]:
    """gitingest include/exclude kwargs for a REPOSITORIES value."""
    if isinstance(entry, str):
        return {}
    kw: dict[str, set[str]] = {}
    if entry.get("include"):
        kw["include_patterns"] = set(entry["include"])
    if entry.get("exclude"):
        kw["exclude_patterns"] = set(entry["exclude"])
    return kw


def refresh_one(
    filename: str,
    url: str,
    *,
    repositories_dir: Path,
    force_shrink: bool = False,
    timeout: int | None = None,
    patterns: dict[str, set[str]] | None = None,
) -> _Result:
    """Refresh a single ``repositories/<filename>`` from ``url`` atomically.

    Strategy
    --------
    1. ``gitingest.ingest(source=url, output=<filename>.refresh.tmp)`` —
       writes the new content next to the target.
    2. Sanity-check the temp file: must exist with non-zero size.
    3. Shrink guard: if a previous snapshot exists and the new dump is
       smaller than ``_SHRINK_GUARD_RATIO`` of it, refuse the swap.
       Override with ``force_shrink=True``.
    4. ``os.replace`` swaps the temp file in.
    5. On any failure, the temp file is removed and the original file
       (if any) is left untouched.

    Parameters
    ----------
    timeout
        Forwarded to gitingest as a ``timeout=`` kwarg if the installed
        version accepts it (newer releases do). On older releases that
        don't accept it the call is retried without the kwarg — the
        bump is then a no-op rather than a crash. ``None`` falls back to
        whatever default gitingest applies.
    """
    target = repositories_dir / filename
    tmp    = repositories_dir / f"{filename}.refresh.tmp"

    # Lazy import: surface a clean error if gitingest isn't installed.
    try:
        from gitingest import ingest
    except ImportError:                                            # pragma: no cover
        return _Result(filename, url, "FAIL",
                       reason="gitingest is not installed. "
                              "Install with: pip install gitingest")

    # Clean up any leftover temp from a previous interrupted run.
    if tmp.exists():
        try:
            tmp.unlink()
        except OSError:                                            # pragma: no cover
            pass

    t0 = time.monotonic()
    try:
        _ingest_with_optional_timeout(ingest, url, tmp, timeout=timeout,
                                      patterns=patterns or {})
    except Exception as exc:                                       # noqa: BLE001
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:                                        # pragma: no cover
                pass
        return _Result(filename, url, "FAIL",
                       reason=_summarise_exception(exc))

    # gitingest finished without raising. Sanity-check the temp file.
    if not tmp.exists() or tmp.stat().st_size == 0:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:                                        # pragma: no cover
                pass
        return _Result(filename, url, "FAIL",
                       reason="ingest produced an empty/missing file")

    new_size = tmp.stat().st_size
    old_size = target.stat().st_size if target.exists() else 0

    # Shrink guard: refuse to overwrite a substantially larger snapshot.
    # Suggests the upstream got gutted / went private / was replaced
    # with a stub. The existing file stays untouched.
    if (old_size > 0
            and not force_shrink
            and new_size < _SHRINK_GUARD_RATIO * old_size):
        try:
            tmp.unlink()
        except OSError:                                            # pragma: no cover
            pass
        return _Result(
            filename, url, "FAIL",
            reason=(f"shrink guard: new dump is {new_size/1024:.1f} KB, "
                    f"existing is {old_size/1024:.1f} KB "
                    f"(< {int(_SHRINK_GUARD_RATIO*100)}%). "
                    f"Existing file kept. If the slim-down is legitimate, "
                    f"override with: "
                    f"--force-shrink --only {filename!r}."),
        )

    os.replace(tmp, target)
    return _Result(filename, url, "OK",
                   size_kb=new_size / 1024,
                   elapsed=time.monotonic() - t0)


def _ingest_with_optional_timeout(ingest_fn, url: str, tmp: Path,
                                  *, timeout: int | None,
                                  patterns: dict[str, set[str]] | None = None) -> None:
    """Call ``gitingest.ingest`` with an optional timeout kwarg.

    Newer gitingest releases accept ``timeout=``; older ones don't. We
    try the modern signature first and gracefully fall back. A
    ``TypeError`` for an unexpected ``timeout`` arg is the signal; any
    other exception propagates so the caller's error handler sees it.
    """
    kwargs = {"source": url, "output": str(tmp), **(patterns or {})}
    if timeout is not None:
        try:
            return ingest_fn(**kwargs, timeout=timeout)
        except TypeError as exc:
            if "timeout" not in str(exc):
                raise
            # Older gitingest — fall through to the no-timeout call.
    return ingest_fn(**kwargs)


def _summarise_exception(exc: BaseException) -> str:
    """One-line, user-readable rendering of an exception.

    Strips git's multi-line CLI output down to the most informative bit,
    keeping the summary table tidy.
    """
    msg = str(exc).strip()
    # Common: "Command failed: git ls-remote ...\nError: remote: Repository not found.\nfatal: ..."
    # Pull out the first "Error:" / "fatal:" line — it's the diagnostic.
    for marker in ("Error:", "fatal:", "Repository not found"):
        if marker in msg:
            for line in msg.splitlines():
                if marker in line:
                    return line.strip()
    # Fallback: first non-empty line.
    for line in msg.splitlines():
        if line.strip():
            return line.strip()
    return f"{type(exc).__name__}: <no message>"


# --------------------------------------------------------------------------- #
# Whole-folder refresh
# --------------------------------------------------------------------------- #


def refresh_all(
    *,
    only: list[str] | None = None,
    repositories_dir: Path | None = None,
    force_shrink: bool = False,
    timeout: int | None = _DEFAULT_TIMEOUT_SECONDS,
) -> list[_Result]:
    """Refresh every entry in :data:`REPOSITORIES`.

    Parameters
    ----------
    only
        Optional list of filenames to restrict the run to. Each entry
        is normalised: ``"NanoTabPFN"`` and ``"NanoTabPFN.txt"`` both
        work. Unknown names raise :class:`ValueError`.
    repositories_dir
        Where the ``.txt`` files live. Defaults to ``<repo-root>/repositories``.
    force_shrink
        Bypass the shrink guard. Use only when a legitimate slim-down
        of the upstream is expected.

    Returns
    -------
    list of :class:`_Result` — one row per attempted file, in the order
    they were processed (REPOSITORIES order, then SKIP_NON_GIT order).
    """
    repositories_dir = repositories_dir or _default_repositories_dir()
    if not repositories_dir.exists():
        raise FileNotFoundError(
            f"repositories/ directory not found at: {repositories_dir}"
        )

    targets = _resolve_targets(only)

    print(f"Refreshing {len(targets)} repository file(s) from "
          f"{repositories_dir}...", file=sys.stderr, flush=True)

    results: list[_Result] = []
    for i, filename in enumerate(targets, start=1):
        entry = REPOSITORIES[filename]
        url = entry_url(entry)
        # Minimal in-flight signal — one line per file, no scrollback noise.
        print(f"  [{i:>2}/{len(targets)}] {filename!s}",
              file=sys.stderr, flush=True)
        results.append(
            refresh_one(filename, url,
                        repositories_dir=repositories_dir,
                        force_shrink=force_shrink,
                        timeout=timeout,
                        patterns=entry_patterns(entry))
        )

    # Skipped files — only on a full run; --only callers know what they're doing.
    if only is None:
        for source in (SKIP_NON_GIT, SKIP_MANUAL):
            for filename in sorted(source):
                results.append(
                    _Result(filename, None, "SKIP", reason=source[filename])
                )

    return results


def _resolve_targets(only: list[str] | None) -> list[str]:
    """Normalise the ``--only`` list against :data:`REPOSITORIES` keys."""
    if not only:
        return list(REPOSITORIES.keys())

    valid = set(REPOSITORIES.keys())
    resolved: list[str] = []
    bad: list[str] = []
    for name in only:
        candidate = name.strip()
        if candidate not in valid:
            candidate_with_ext = f"{candidate}.txt"
            if candidate_with_ext in valid:
                candidate = candidate_with_ext
            else:
                bad.append(name)
                continue
        resolved.append(candidate)

    if bad:
        valid_sorted = "\n  ".join(sorted(valid))
        raise ValueError(
            f"--only matched no known repositories: {bad!r}\n"
            f"Valid filenames are:\n  {valid_sorted}"
        )
    # Preserve order, drop duplicates while keeping first occurrence.
    seen: set[str] = set()
    return [x for x in resolved if not (x in seen or seen.add(x))]


# --------------------------------------------------------------------------- #
# Summary rendering
# --------------------------------------------------------------------------- #


def _print_summary(results: list[_Result]) -> None:
    """Print the final overview table.

    Layout
    ------
    * One short row per file: status badge + filename + size/time or reason.
    * A counts line at the bottom (OK / FAIL / SKIP).
    * If any FAIL or SKIP rows have reasons, repeat them as a block below
      so the user doesn't have to scan back through the table.
    """
    n_ok   = sum(1 for r in results if r.status == "OK")
    n_fail = sum(1 for r in results if r.status == "FAIL")
    n_skip = sum(1 for r in results if r.status == "SKIP")

    bar = "-" * 78
    print()
    print(bar)
    print(f"  Repository refresh - summary    "
          f"(OK: {n_ok}   FAIL: {n_fail}   SKIP: {n_skip})")
    print(bar)

    max_name = max((len(r.filename) for r in results), default=20)
    name_w = min(max_name, 50)

    for r in results:
        name = r.filename.ljust(name_w)
        if r.status == "OK":
            detail = f"{r.size_kb:>7.1f} KB   {r.elapsed:>5.1f}s"
            print(f"  [OK  ]  {name}   {detail}")
        elif r.status == "FAIL":
            print(f"  [FAIL]  {name}   -- see reasons below")
        else:
            print(f"  [SKIP]  {name}   -- see reasons below")

    print(bar)

    # Detailed reasons for non-OK rows, in the same order as the table.
    bad = [r for r in results if r.status in ("FAIL", "SKIP")]
    if bad:
        print("Reasons:")
        for r in bad:
            print(f"  * {r.status} {r.filename}")
            if r.url:
                print(f"      url:    {r.url}")
            print(f"      reason: {r.reason}")
        print(bar)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=("Refresh repositories/*.txt files via gitingest. "
                     "With no arguments, every entry in REPOSITORIES is "
                     "refreshed (non-Git sources skipped)."),
    )
    parser.add_argument(
        "--only", action="append", default=None, metavar="FILENAME",
        help=("Refresh only this filename (repeatable). Accepts either "
              "'NanoTabPFN' or 'NanoTabPFN.txt'."),
    )
    parser.add_argument(
        "--force-shrink", action="store_true",
        help=("Disable the shrink guard. Allows overwriting an existing "
              "snapshot with a new dump that is smaller than 50%% of it. "
              "Use only when a legitimate slim-down of the upstream is "
              "expected."),
    )
    parser.add_argument(
        "--timeout", type=int, default=_DEFAULT_TIMEOUT_SECONDS,
        metavar="SECS",
        help=(f"Per-repository gitingest timeout in seconds "
              f"(default: {_DEFAULT_TIMEOUT_SECONDS}). Increase if "
              f"large repos like VscDocumentation time out. Ignored "
              f"silently on gitingest versions that don't accept "
              f"a 'timeout' kwarg."),
    )
    args = parser.parse_args(argv)

    # Quiet, table-style output. The streaming gitingest INFO logs are
    # muted so the user only sees per-file progress + the final summary.
    logging.basicConfig(level=logging.WARNING, format="%(message)s", force=True)
    _silence_gitingest_logging()
    # Swallow cosmetic asyncio shutdown noise on Windows + Python 3.12.
    _install_quiet_async_shutdown()

    try:
        results = refresh_all(
            only=args.only,
            force_shrink=args.force_shrink,
            timeout=args.timeout,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    _print_summary(results)
    n_fail = sum(1 for r in results if r.status == "FAIL")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
