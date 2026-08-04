# Changelog

Human-readable log of library updates, newest first. Consuming projects pin
a commit of this repo — read this to decide whether to bump your pin.
One line per change; date every entry.

## 2026-08-04 (b) — restructure: project-neutral, chronological, self-maintaining

**Breaking for consumers: every paper path changed.** Papers are now
foldered by year and prefixed with their release month, so they sort
chronologically: `papers/<year>/<MM>_Author_et_al._Title.pdf`, with text
extractions mirrored at `papers/text/<year>/<same-name>.txt`. All 62 files
were moved with `git mv` (history preserved) and all 92 path references in
the docs were rewritten. Update any downstream reference to the old
`papers/YYYY_Author_Title.pdf` form.

- **The shared documents are now project-neutral by contract.** All 31
  "For CreditPFN" blocks were removed from `SUMMARIES.md`, the "Where
  CreditPFN sits" section from `SYNTHESIS.md`, and the CreditPFN
  comparison tables and `our src/…` phrasing from `REPOSITORIES.md`.
  CreditPFN mentions across the three documents: 57 + 22 + 11 → 0. The
  extracted material was handed to CreditPFN verbatim; three
  consumer-neutral facts inside those blocks were deliberately kept
  upstream (the Real-TabPFN attribution warning, TabDPT's contamination
  list, and the v2.6-vs-v3 `criterion.*` asymmetry).
- **`PROJECT_SPECIFIC.template.md` added**, and `PROJECT_SPECIFIC.md` is
  now gitignored. A downstream project copies the template inside its own
  copy of this folder and writes its notes there: the file sits next to
  the literature, survives updates, and can never dirty or be pushed to
  this repository. The template carries the six-rule contract so every
  consumer's notes have the same shape.
- **`AGENTS.md` rewritten around the read-only boundary.** It now opens
  with a table telling an agent which side it is on, states that edits
  happen in this repository's own checkout *only*, and gives separate rule
  sets for "inside this repository" and "in a downstream project" (where
  the folder is strictly read-only, with `PROJECT_SPECIFIC.md` the single
  exception). Scope is stated explicitly as *strictly tabular foundation
  models*. The stale claim that the repository is private was removed —
  it is public.
- **`README.md` rewritten**: documents every script with runnable
  examples, explains the submodule embedding and the two-step update, and
  states the read-only rule and the `PROJECT_SPECIFIC.md` exception.
- **`requirements.txt` added** (no `pyproject.toml` on purpose — this is a
  knowledge base, not an installable package).
- **New `scripts/check_zotero_sync.py`** — read-only consistency check
  between `papers/` and the mirroring Zotero collection. Auto-detects the
  Zotero data dir and linked-attachment base path from `prefs.js`, queries
  a *copy* of `zotero.sqlite` (never the live locked file), and reports
  presence gaps, year mismatches, missing DOI/URL, authorless items,
  broken attachment links, and missing extractions. First run: 31/31
  matched, 5 real issues found.
- **New `scripts/check_paper_versions.py`** — asks arXiv whether a newer
  version exists than the PDF on disk. First run found TabPFN-3 v2
  (2026-05-28) available against the v1 held here. Never downloads.
- **New `scripts/maintain.py`** — one command running all of the above
  (`text` → `zotero` → `versions` → `repos`) with a consolidated summary;
  `--check-only`, `--skip`, `--only`.
- `scripts/extract_paper_text.py` reworked for the year-foldered layout,
  plus a `--check` mode reporting missing and orphaned extractions.

## 2026-08-04 (a)

- Added **Kong & Das 2026 — "Introducing TabFM: A zero-shot foundation
  model for tabular data"** (Google Research blog post, 30 June 2026) at
  the owner's request: PDF renamed to house convention
  (`2026_Kong_and_Das_Introducing_TabFM_A_zero_shot_foundation_model_for_tabular_data.pdf`),
  text extracted, SUMMARIES.md entry + overview row, SYNTHESIS.md
  timeline row / scaling-section paragraph / design-axes rows (a)+(b) /
  vendor-science tension / appendix card.
- Note for consumers: TabFM is a **blog post, not a paper** — no arXiv,
  no peer review, no prior spec or ablations, and its TabArena Elo
  results exist only as a figure (the text names no numbers and no
  versioned TabPFN/TabICL baseline). It is recorded for its
  architectural significance (a third independent lab converging on
  column-embed → row-compress → ICL) and its productization (BigQuery
  `AI.PREDICT`), not as a citable results source. The HF model card's
  BibTeX entry looks like a paper citation but is not one.
- Two facts worth flagging before anyone plans to use TabFM: the weights
  are **non-commercial / non-production licensed** (code is Apache-2.0),
  and `max_classes` is a **hard cap of 10**. Verified architecture
  details and limits come from the released `config.json` / README, not
  the blog.

## 2026-07-17

- Full consistency audit of the library (docs cross-checked against the
  paper texts and code dumps); fixes below.
- `repositories/TransformersCanDoBayesianInference.txt` re-dumped from its
  true upstream (`automl/TransformersCanDoBayesianInference`, the 2021
  paper's own repo): the refresh script had mapped it to the successor
  `SamuelGabriel/PFNs`, which had silently turned it into a byte-duplicate
  of `PFNS.txt`; script mapping and REPOSITORIES.md description corrected.
- SUMMARIES.md: corrected four arXiv IDs (Müller Position → 2505.23947,
  nanoTabPFN → 2511.03634, TabPFN-Wide → 2510.06162, Hoo 2024 →
  NeurIPS'24 TS workshop / arXiv 2501.02945v1 — 2407.05393 was an
  unrelated paper) and added Purucker's (2606.30410).
- SUMMARIES.md: rewrote the Hoo 2024 entry (features are
  timestamp-derived, lags explicitly excluded; eval is 24 of 29
  AutoGluon-TS datasets vs Chronos — not M4/M5 vs ARIMA/N-BEATS); same
  lag-feature correction in the From-Tables-to-Time entry.
- SUMMARIES.md: nanoTabPFN is <500 lines (was "~900"); BETA evaluated on
  186 TALENT datasets (was "200+"); TabICL's >10k-row win is on TALENT
  (was "TabArena"); Rubachev tested partial FT variants, not
  prefix-tuning; TabPFN-Wide's checkpoints are its own per-width
  classifiers (the `_large-features-*` names belong to TabPFN-2.5);
  intro no longer claims v2.6 ships a real-data default.
- SYNTHESIS.md: repaired 7 broken table-of-contents anchors; v2 prior is
  ~100M synthetic tables (was ~130M in two places); TabICL SFT collapse
  is 0.873→0.567 (one spot said 0.847); "full FT beats PEFT" softened to
  "matches while converging fastest" (matching Rubachev and SUMMARIES).
- REPOSITORIES.md: refreshed all stale line counts (15 of 16 were wrong,
  e.g. `TabPFN Wide.txt` is now 2.28M lines); converted line-number dump
  citations to symbol/grep citations per AGENTS.md rule 3; rewrote the
  `TabPFN V2 Finetuning.txt` section for the current upstream examples
  (old hand-rolled scripts are gone; wrapper defaults re-verified);
  fixed the Yandex-dump README bullet (README is charmap-lost in the
  dump); "Refreshing this folder" now points at the refresh script;
  de-linked consuming-project paths (`docs/CHECKPOINTS.md`,
  `docs/VSC_GUIDE.md`) here and in SUMMARIES.md; TabTune row/section now
  link the local Tanna 2025 PDF.
- scripts/refresh_repositories.py: fixed stale `docs/REPOSITORIES.md` and
  `src/utils/` path references in docstrings.
- scripts/extract_paper_text.py: strips control bytes from extractions
  (pypdf glyph artifacts made grep treat two texts as binary);
  re-extracted TabPFN-3 and Beyond-IID texts.

## 2026-07-11

- Restructured for multi-project use: `LITERATURE.md` → `SUMMARIES.md`,
  `SUMMARY.md` → `SYNTHESIS.md`; human `README.md` + agent contract
  `AGENTS.md`; added `CHANGELOG.md` and `scripts/extract_paper_text.py`.
- Policy: papers are added only on the owner's explicit request (no
  proactive collecting; the earlier WATCHLIST.md was removed for this
  reason).
- Initial import from CreditPFN: 30 papers (PDF + text), 15 repository
  dumps, per-paper summaries, field synthesis, repository guide,
  standalone dump-refresh script.
