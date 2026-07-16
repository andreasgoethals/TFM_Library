# Watchlist — to acquire next

Papers and repositories that should be added to the library. When you add
one, follow the five-step procedure in `AGENTS.md` §4 and remove it here.

## Papers

- **TabArena** (Erickson et al.) — the living-benchmark paper behind the
  leaderboard every recent TFM reports on; referenced constantly in
  SYNTHESIS.md but not yet collected.
- **TabReD** (Rubachev et al. 2024) — the temporally-shifted industrial
  benchmark that Beyond-IID builds on; central to the temporal-evaluation
  question.
- **Falck et al. 2024, "are LLMs Bayesian?"** — the Martingale-property
  critique cited in SYNTHESIS.md's foundations section (PFN-Bayesianity
  caveat); collect for completeness.
- Any TabPFN-3 / TabICLv2 follow-ups appearing on arXiv (watch quarterly).

## Repositories (dumps to add or refresh)

- **TabArena benchmark code** (github.com/autogluon/tabarena or equivalent)
  — needed if any project evaluates on it.
- **TabICLv2** official release (weights/code announced open; dump when the
  training/prior code lands).
- Periodic refresh of `TabPFN .txt` (tracks Prior Labs main; last refreshed
  2026-06-23).

## Ideas parked

- `references.bib` — BibTeX entries for all collected papers (thesis-ready
  citing). Generate once, maintain per added paper.
- `CATALOG.csv` — machine-readable index (bibkey, year, authors, title,
  venue, arXiv id, PDF path, tags) for scripting.
- `BENCHMARKS.md` — one page tracking the evaluation landscape (TabArena,
  TabReD, OpenML suites, BeyondArena): what each measures, where to get it.
