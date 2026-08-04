# Changelog

Human-readable log of library updates, newest first. Consuming projects pin
a commit of this repo — read this to decide whether to bump your pin.
One line per change; date every entry.

## 2026-08-04 (e) — six new code dumps; all dumps refreshed

- **Six new snapshots** (16 → 22 dumps), all requested by the owner:
  - **`TabICL.txt`** (32,794 lines) — the most valuable addition. The only
    *fully open* competitive TFM: complete synthetic prior generator
    (`prior/`, `prior/graph_lib/`), pretraining loop with the **Muon
    optimiser** (`train/_muon.py`), the 3-stage curriculum scripts for v1
    **and** v2, plus finetuning, forecasting and SHAP extensions. Nothing
    else here exposes how a frontier TFM is actually *trained*.
  - **`NanoTabICL.txt`** — TabICLv2's minimal release: `model.py` +
    `prior.py`, the shortest readable path to a whole TFM.
  - **`LoCalPFN.txt`** — the only k-NN-retrieval context implementation
    here (~58 KB). No upstream LICENSE: read, don't redistribute.
  - **`TabSTAR.txt`** — text-aware pretraining, LoRA, checkpoint
    averaging, `verbalize.py`. Default branch is `master`, not `main`.
  - **`CausalPFN.txt`** — amortised CATE/ATE estimation (inference only;
    the simulated-DGP prior is unreleased).
  - **`TabForestPFN.txt`** — the forest-prior generators; historical
    (upstream dead since 2024-05).
- **`refresh_repositories.py` now supports per-repository file filters.**
  Values in `REPOSITORIES` may be `{"url", "include", "exclude", "note"}`
  instead of a bare URL. Needed because several TFM repos commit gigabytes
  of experiment artifacts, checkpoints or metadata stubs around a few
  hundred KB of source — CausalPFN (~175 MB of benchmark data), LoCalPFN
  (a 103 MB committed checkpoint), TabSTAR (401 per-dataset stubs).
- **New `SKIP_MANUAL` category.** `TabForestPFN.txt` cannot be refreshed by
  gitingest at all: upstream is 1.36 GB and gitingest hardcodes a 60 s
  clone timeout that `--timeout` cannot raise. It is now reported as SKIP
  with the sparse-clone recipe rather than failing every run, and the
  recipe is in the module docstring.
- **All 19 refreshable dumps re-dumped** (18 OK). Several grew
  substantially since the last snapshot — `TabPFN .txt` 77,938 → 84,092
  lines, `TabTune.txt` 162,653 → 168,086, `TabPFN V2 Finetuning.txt`
  4,331 → 4,835. Overview-table line counts refreshed accordingly.
- **`On Finetuning Tabular Foundation Models.txt` is now an archive — do
  not `--force-shrink` it.** Upstream has **deleted its entire `exp/`
  directory**: 636 files, including all **342 `report.json` experiment
  reports**, with `lib/` code unchanged and nothing added. A fresh dump
  would be 37 % of the size and would destroy the hyperparameter evidence
  the "Verified config facts" table is built from — data that no longer
  exists upstream. The shrink guard blocks this and reports a FAIL on every
  run; that FAIL is correct and should be left alone. Warning added to
  REPOSITORIES.md.
- **`VSC Documentation.txt` is now documented as the one deliberate
  exception to the TFM-only scope**, in README.md, AGENTS.md and
  REPOSITORIES.md, with an explicit "never remove this" note: every
  consuming project runs on VSC, so it is shared infrastructure knowledge.

## 2026-08-04 (d) — text extractions repaired; TabTune coverage documented

- **All 41 text extractions regenerated.** 27 of the 31 pre-existing files
  were **Latin-1 encoded with CRLF endings** — so they were never produced
  by `scripts/extract_paper_text.py` (which writes UTF-8/LF) but carried
  over from the original import. Every non-ASCII author name was mangled
  (`Samuel Mu¨ller`, `M\xfcller`) and any tool decoding them as UTF-8
  crashed outright. All are now uniform UTF-8 with LF, and diacritics
  render correctly.
- **New extraction filter: submission line-number gutters.** ICLR/NeurIPS
  templates print a line number beside every line, which pypdf emitted as
  long runs of bare integers — 1,491 of 3,135 lines (48%) in the den
  Breejen extraction. Runs of ≥8 are now stripped; shorter numeric columns
  inside real tables survive.
- **`extract_paper_text.py --check` now validates quality, not just
  presence**: flags non-UTF-8 files, CRLF endings, control bytes, and
  line-number gutters, and exits non-zero. `maintain.py` therefore catches
  this class of corruption automatically from now on.
- **REPOSITORIES.md: documented what `TabTune.txt` actually contains.**
  That dump silently vendors complete copies of 13 model implementations
  (`tabpfnv3/` 117 files, `tabpfnv26/` 101, `orion_msp/` 30,
  `orion_bix/` 33, `contexttab/` 14, `limix/`, `mitra/`, `tabicl/`,
  `tabiclv2/`, `tabdpt/`, …), verified by file count. Consequence:
  **separate dumps of Orion-MSP, Orion-BiX or ConTextTab would be
  redundant** — spot-checked byte-identical, and the vendored
  `orionmsp_v15/` is newer than the standalone repo. Also noted that
  ConTextTab's upstream was renamed to `SAP-samples/sap-rpt-1-oss`, so the
  URL printed in the paper is dead.

## 2026-08-04 (c) — ten papers added

Added on the owner's request, imported from the Zotero "Foundation Models"
collection. Corpus goes 31 → 41 papers. Each got the full five-step
treatment (file + text extraction + SUMMARIES entry and overview row +
SYNTHESIS timeline row, thematic integration and appendix card).

- **Nagler 2023 — Statistical Foundations of Prior-Data Fitted Networks**
  (ICML 2023). The theory of *why* PFN in-context learning works: a
  frequentist reading in which variance vanishes for free but bias
  vanishes only under localisation, which PFN transformers do not
  guarantee. Integrated into the Foundations section, since it predicts
  the later success of retrieval-based localisation.
- **den Breejen 2024 — TabForestPFN.** Origin of the tree/forest prior
  and of the finding that prior *realism* and prior *adaptability* are
  different axes — the observation Mitra later formalised.
- **Thomas 2024 — LoCalPFN** (NeurIPS 2024). Retrieval + fine-tuning;
  SOTA on 95 TabZilla datasets. The empirical answer to Nagler's bias
  analysis and the ancestor of TabDPT's retrieval.
- **Bouadi 2025 — Orion-MSP** and **Bouadi 2026 — Orion-BiX** (WWW '26).
  The two Lexsi Labs architectures behind TabTune and the Tanna
  fine-tuning study, both already held — closing an obvious gap.
- **Spinaci 2025 — ConTextTab** (NeurIPS 2025) and **Arazi 2025 —
  TabSTAR** (NeurIPS 2025). The semantics axis: per-modality embeddings
  on real tables, and target-aware text representations with scaling laws
  in dataset *count*. Prompted a new paragraph in the scaling section,
  since semantics is signal a synthetic SCM prior cannot contain even in
  principle.
- **Balazadeh Meresht 2025 — CausalPFN** (NeurIPS 2025). Fourth member of
  the causal-PFN cluster, and the model CausalFM loses to on ACIC2016 —
  needed to read that comparison honestly.
- **Tanna 2026 — Data Presentation Over Architecture.** On imbalanced
  credit data, **context construction explains more AUC variance than the
  choice of TFM**: balanced/hybrid sampling adds 3–4 points, exceeding the
  between-model spread. Added as its own weakness in SYNTHESIS (§3b),
  because every other comparison in the corpus holds context construction
  fixed while varying the model.
- **Feuer 2024 — TuneTables** (NeurIPS 2024). Context optimisation —
  compress a large dataset into a small *learned* context — as the third
  distinct answer to adapting a frozen PFN, alongside retrieval
  (LoCalPFN) and weight updates (Real-TabPFN). Notable as the only method
  in the corpus where a constraint (a fairness objective) can be imposed
  on the context itself. Its "prefer PEFT to protect the prior" premise
  is what Rubachev 2025 later overturned for v2, so the two are now
  filed together deliberately.

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
