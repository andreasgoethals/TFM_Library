# Changelog

Human-readable log of library updates, **newest first**. Consuming projects
pin a commit of this repo — read this to decide whether to update your pin.
One line per change; one dated section per day.

## 2026-08-07

- Added **Bouadi 2026-05 — O'Prior, "Shaping the Prior"** (arXiv 2605.18971,
  Lexsi Labs, code public), 42 → 43 papers, full five-step treatment. The
  first study to isolate synthetic prior design as the sole variable:
  architecture, optimizer, compute budget and evaluation pipeline fixed,
  only the task distribution varied — nanoTabPFN, 40,000 synthetic datasets
  per prior, nine variants against the TabPFN-v1/TabICL-v1/TabICL-v2
  generators. Finding: **mechanism diversity is the strongest driver of
  transfer**, with observational realism (incl. MCAR/MAR/MNAR missingness
  and target reshaping) and shift-stress complementary but not
  interchangeable.
- **Two standing claims corrected as a result.** Weakness §2 said "no paper
  runs the controlled comparison (same compute, same base)" — half of it now
  exists, so the text now scopes the remaining gap to the real-CPT arm.
  "Open frontiers → Resolving the prior question empirically" said the
  experiment had not been run at all; it now credits O'Prior and enumerates
  the three arms still open, including the untouched question of whether
  prior design can be **domain-targeted** rather than generically realistic.
- Two limits worth carrying forward: O'Prior is **nano-scale**, so its
  component ranking is unverified at frontier scale, and it is
  **classification-only**, so target reshaping is never exercised on a
  regression target and bounded/bimodal targets are outside its scope.

## 2026-08-06

- Added **Hosseinzadeh 2026-05 — TabDPT-Turbo** (ICML FMSD workshop,
  OpenReview `Y00pwFyrHR`), 41 → 42 papers, full five-step treatment.
  Notable because it is the **retrieval branch recanting**: the lab that
  introduced retrieved contexts (LoCalPFN) and shipped FAISS retrieval in
  TabDPT removes it in favour of long-context pretraining, reporting
  retrieval-style inference as 100×–1000× slower. It also stays
  **row-based**, declining the column-compress convergence that TabPFN-3,
  TabICLv2 and TabFM all adopted — so that consensus is narrower than it
  looked. Integrated into the scaling section (as a partial answer to
  Nagler's localisation argument: exposure can substitute for engineered
  retrieval), weakness §5 on inference cost, and design axes (b) and (c).
- Recorded a source conflict: TabDPT-Turbo states TabDPT was trained on
  112 datasets; **TabDPT's own paper says 123** (32M rows, 2B cells, 93
  classification + 29 regression). The library keeps 123 and flags the
  discrepancy in the Turbo entry.
- Turbo ships as **TabDPT v1.2** in `layer6ai-labs/TabDPT-inference`, which
  is already snapshot here as `TabDPT.txt` — the code arrives on the next
  `refresh_repositories.py` run, no new dump needed.
- `README.md`: added **CreditICL** to the consuming-projects list (a new
  downstream project on pretraining-prior design, built on TabICL), and
  gave the table an *Angle* column so the two credit projects are
  distinguishable.

## 2026-08-05

- **Papers now carry their release month everywhere, and sort by it.**
  `SUMMARIES.md` entry headings and overview rows are `YYYY-MM` (column
  renamed Year → Date) and all 41 entries are ordered by year *and* month;
  `SYNTHESIS.md`'s timeline table and appendix cards likewise. The thematic
  sections keep their argument order, which is not chronological by design.
  Months are derived from the `papers/<year>/<MM>_` filenames, so the
  documents and the filesystem cannot disagree.
- Normalised `SUMMARIES.md` entry separators (41 entries had only 31), and
  converted the one auto-generated heading anchor to an explicit
  `<a id="nagler-theory">` so it survives heading changes.
- Condensed this changelog (2,170 → ~690 words) and merged the five
  same-day 2026-08-04 sections into one; the `(a)`–`(e)` suffixes ran
  opposite to the newest-first order and read as broken sorting.

## 2026-08-04

**⚠ Breaking for consumers: every paper path changed.** Papers are now
foldered by year and prefixed with their release month —
`papers/<year>/<MM>_Author_et_al._Title.pdf`, with extractions mirrored at
`papers/text/<year>/`. Update any reference to the old
`papers/YYYY_Author_Title.pdf` form.

- **Shared docs are now project-neutral by contract.** All CreditPFN
  content removed from `SUMMARIES.md` (31 blocks), `SYNTHESIS.md` (a whole
  section) and `REPOSITORIES.md`; mentions 90 → 0. Project notes now live
  in a downstream-only `PROJECT_SPECIFIC.md` (template shipped, filename
  gitignored so it can never dirty or be pushed to this repo).
- **`AGENTS.md` rewritten around the read-only boundary**: separate rules
  for working *inside* this repo (edit) versus *in a downstream project*
  (read only, `PROJECT_SPECIFIC.md` the sole exception). Scope stated as
  strictly tabular foundation models. Removed the stale "not public" claim.
- **`README.md` rewritten**: every script documented, submodule embedding
  and the two-step update explained, read-only rule stated.
- **Papers 31 → 41.** Added Nagler 2023 (PFN theory), den Breejen 2024
  (TabForestPFN), Thomas 2024 (LoCalPFN), Feuer 2024 (TuneTables), Bouadi
  2025/2026 (Orion-MSP, Orion-BiX), Spinaci 2025 (ConTextTab), Arazi 2025
  (TabSTAR), Balazadeh 2025 (CausalPFN), Tanna 2026 (credit-risk
  resampling), Kong & Das 2026 (Google TabFM, blog only — not a paper).
- **Dumps 16 → 22.** Added `TabICL.txt` (the standout: the only fully open
  TFM — prior generator, pretraining loop, Muon optimiser, 3-stage
  curriculum for v1 and v2), `NanoTabICL.txt`, `LoCalPFN.txt`,
  `TabSTAR.txt`, `CausalPFN.txt`, `TabForestPFN.txt`. All 19 refreshable
  dumps re-dumped; line counts refreshed.
- **All 41 text extractions regenerated.** 27 were Latin-1 with CRLF, so
  every non-ASCII author name was mangled (`Samuel Mu¨ller`) and UTF-8
  readers crashed. Now uniform UTF-8/LF. Also strips ICLR/NeurIPS
  line-number gutters (48% of one file).
- **New scripts:** `maintain.py` (runs everything, one summary),
  `check_zotero_sync.py` (read-only Zotero ↔ library consistency),
  `check_paper_versions.py` (newer arXiv versions). `extract_paper_text.py`
  gained `--check` with encoding/CRLF/gutter validation.
  `requirements.txt` added (no `pyproject.toml` — this is not a package).
- **`refresh_repositories.py`:** per-repository include/exclude filters
  (several TFM repos commit GBs of artifacts around a little source), and a
  new `SKIP_MANUAL` category for repos too large for gitingest's 60 s
  clone timeout.
- **`VSC Documentation.txt` documented as the one deliberate exception to
  the TFM-only scope — never remove it.** Every consuming project runs on
  VSC, so it is shared infrastructure knowledge.
- **Two permanent, expected warnings from `maintain.py`.** (1) The
  `On Finetuning…txt` shrink-guard FAIL is *correct*: upstream deleted its
  entire `exp/` directory including all 342 `report.json` reports, so this
  dump is now the only surviving copy — never `--force-shrink` it.
  (2) `TabForestPFN.txt` reports SKIP; refresh it with the sparse-clone
  recipe in the script docstring.
## 2026-07-17

Full consistency audit: docs cross-checked against the paper texts and code
dumps.

- **`TransformersCanDoBayesianInference.txt` re-dumped from its true
  upstream.** The refresh script had pointed it at the maintained successor
  (`SamuelGabriel/PFNs`), silently making it a byte-duplicate of `PFNS.txt`
  and losing the 2021 paper-era snapshot.
- **Factual corrections in `SUMMARIES.md`:** five wrong arXiv IDs (one
  pointed at an unrelated paper); the Hoo 2024 entry described the wrong
  experiment (features are timestamp-derived and lags *excluded*; eval is
  AutoGluon-TS vs Chronos, not M4/M5 vs ARIMA); nanoTabPFN is <500 lines;
  BETA used 186 TALENT datasets; TabICL's >10k-row win is on TALENT;
  Rubachev tested partial FT, not prefix-tuning.
- **`SYNTHESIS.md`:** 7 broken table-of-contents anchors; v2's prior is
  ~100M synthetic tables, not ~130M; "full FT beats PEFT" softened to
  "matches while converging fastest".
- **`REPOSITORIES.md`:** all stale line counts refreshed (15 of 16 wrong);
  line-number dump citations converted to symbol names per AGENTS.md rule 3;
  `TabPFN V2 Finetuning.txt` section rewritten for the current upstream.
- **`extract_paper_text.py`:** strips control bytes, which had made two
  extractions grep as binary.

## 2026-07-11

- Restructured for multi-project use: `LITERATURE.md` → `SUMMARIES.md`,
  `SUMMARY.md` → `SYNTHESIS.md`; human `README.md` + agent contract
  `AGENTS.md`; added `CHANGELOG.md` and `scripts/extract_paper_text.py`.
- Policy: papers are added only on the owner's explicit request (no
  proactive collecting; the earlier `WATCHLIST.md` was removed for this
  reason).
- Initial import from CreditPFN: 30 papers (PDF + text), 15 repository
  dumps, per-paper summaries, field synthesis, repository guide,
  standalone dump-refresh script.
