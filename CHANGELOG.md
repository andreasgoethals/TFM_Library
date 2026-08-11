# Changelog

Human-readable log of library updates, **newest first**. Consuming projects
pin a commit of this repo — read this to decide whether to update your pin.
One line per change; one dated section per day.

## 2026-08-06

- Added **Luo 2026-07 — Memory Efficient Tabular Foundation Models**
  (arXiv 2607.27546, FMSD @ ICML 2026), 43 → 44 papers, full five-step
  treatment. Post-hoc **INT4 quantization** cuts TFM memory **7.6×**
  (≈87% lower deployment requirement) with negligible accuracy loss,
  leaving the quantized model above the strongest tuned baseline. Studied
  on TabPFN v2.5/v2.6 and TabICL.
- Notable for two reasons, both recorded in the synthesis. It is the
  **first paper in this collection written from inside a deploying
  institution** (Commonwealth Bank of Australia), and it supplies an
  **open** answer to the inference-cost problem where the frontier's own
  answer — the v2.5/v3 distillation engines — is proprietary. Integrated
  into weakness §5 and design axis (d) as complementary to, not competing
  with, TabDPT-Turbo: quantization shrinks weights, row-compression and
  retrieval-free designs shrink in-context activations.
- Replaced the last two auto-generated heading anchors in `SUMMARIES.md`
  with explicit `<a id=…>` ones (`#mitra`, `#tabdpt-turbo`). All 13
  internal links are now anchor-backed and survive heading edits.

## 2026-08-05

Papers 41 → 43. Months added throughout and everything ordered by them;
`README.md` reorganised around the downstream-update commands.

- **Papers now carry their release month everywhere, and sort by it.**
  `SUMMARIES.md` headings and overview rows are `YYYY-MM` (column renamed
  Year → Date); `SYNTHESIS.md`'s timeline and appendix cards likewise. The
  thematic sections keep their argument order, which is not chronological by
  design. Months derive from the `papers/<year>/<MM>_` filenames, so the
  documents and the filesystem cannot disagree.
- Added **Hosseinzadeh 2026-05 — TabDPT-Turbo** (ICML FMSD workshop). The
  retrieval branch recanting: the lab that introduced retrieved contexts
  (LoCalPFN) and shipped FAISS retrieval in TabDPT removes it for
  long-context pretraining, reporting retrieval as 100×–1000× slower. It
  also stays **row-based**, declining the column-compress convergence —
  so that consensus is narrower than it looked. Ships as TabDPT v1.2 in
  `layer6ai-labs/TabDPT-inference`, already snapshot here, so no new dump.
  Recorded a source conflict: it says TabDPT used 112 datasets; TabDPT's own
  paper says **123** — the library keeps 123.
- Added **Bouadi 2026-05 — O'Prior, "Shaping the Prior"** (arXiv 2605.18971,
  code public). The first study to isolate prior design as the sole
  variable: architecture, optimizer, budget and evaluation fixed, only the
  synthetic task distribution varied — nanoTabPFN, 40,000 datasets per
  prior, nine variants against the TabPFN-v1/TabICL-v1/TabICL-v2
  generators. **Mechanism diversity is the strongest driver of transfer**;
  realism (incl. MCAR/MAR/MNAR missingness and target reshaping) and
  shift-stress are complementary but not interchangeable. Limits worth
  carrying: nano-scale only, and **classification-only**, so target
  reshaping is never tested on a regression target.
- **Two standing claims corrected because of O'Prior.** Weakness §2 said no
  paper runs the controlled comparison — half of it now exists, so the text
  scopes the gap to the real-CPT arm. "Open frontiers → Resolving the prior
  question" now credits O'Prior and lists the three arms still open,
  including whether prior design can be **domain-targeted** rather than
  generically realistic.
- **`README.md` reorganised around the two things a consumer needs.** The
  general introduction stays first; immediately after it, one "Using this
  library in a project" section gives the exact command chains for (1)
  adding the submodule to a new project and (2) updating an existing one to
  the latest version, one command per block, with the rarer operations
  (`--init` after clone, `submodule status`) collapsed. The duplicate
  section further down was removed so the two cannot drift.
- **Removed every `&&` from documented commands.** Windows PowerShell 5.1
  has no `&&`, so `git add tfm-library && git commit …` and
  `python -m venv .venv && .venv\Scripts\activate` were parser errors on
  the platform this repo is maintained from.
- **Fixed a wrong submodule URL** — the setup snippet said
  `andreasgoethals/tfm-library`; the real remote, and what both consuming
  projects use, is `andreasgoethals/TFM_Library.git`. Following the README
  verbatim would have failed.
- Added **CreditICL** to the consuming-projects list (pretraining-prior
  design on TabICL) and gave the table an *Angle* column so the two credit
  projects are distinguishable.
- Housekeeping: normalised `SUMMARIES.md` entry separators (41 entries had
  only 31); replaced auto-generated heading anchors with explicit
  `<a id=…>` ones where a heading change would silently break them;
  condensed this changelog and merged the five same-day 2026-08-04 sections
  into one, since the `(a)`–`(e)` suffixes ran opposite to the newest-first
  order.

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
