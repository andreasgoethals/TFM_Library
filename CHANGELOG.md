# Changelog

Human-readable log of library updates, newest first. Consuming projects pin
a commit of this repo — read this to decide whether to bump your pin.
One line per change; date every entry.

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
