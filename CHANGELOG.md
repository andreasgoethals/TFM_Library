# Changelog

Human-readable log of library updates, **newest first**. Consuming projects
pin a commit of this repo — read this to decide whether to update your pin.
One line per change; one dated section per day.

## 2026-08-29

- Added **Eo et al. 2026-08 — EXAONE Tabular 1.0** (arXiv 2608.25774), LG AI Research. Attacks
the row-compression boundary that TabICL/TabICLv2/TabPFN-3 all rely on: its CAST architecture
interleaves feature-axis and item-axis attention at every layer instead. A 20.8M-parameter model
ranks **first on TabArena classification** with no tuning and ties Google's 1.64B TabFM at ~1.3%
of the parameters. Leads CRPS on ScoringBench — the most credit-risk-relevant result here, since
it measures the whole predictive distribution rather than the conditional mean.
- Added **Zheng et al. 2025-11 — From Tables to Signals** (arXiv 2511.18278). The first
frequency-domain account of why TabPFN works: it defines a **context kernel** (the ICL analogue
of the NTK) and shows TabPFN's effective bandwidth grows with the number of **context rows**,
where an MLP's is fixed by its architecture. Converges with Nagler's localisation argument and
Shaheen's retrieval account, and explains why positional encoding was needed to make TabPFN work
on time series.
- **New citation convention in `SUMMARIES.md` and `SYNTHESIS.md`:** a reference to another paper
now carries its **title** alongside the author-year, on first mention in each section, so a
passage can be read without looking the citation up. Recorded in `AGENTS.md`.
## 2026-08-27

Dumps refreshed, and the two code citations the refresh invalidated corrected.
No papers added; no claim about the literature changed.

- **`repositories/` refreshed** (TabPFN, TabDPT, TabICL, TabTune, NanoTabICL,
TabPFN Client / Extensions / V2 Finetuning, VSC Documentation).
- **TabDPT moved its worked examples out of `tests/`.** `cls_example.py` and
`reg_example.py` now live in `examples/`; `tests/` holds a real pytest suite
(`test_cls.py`, `test_reg.py`, `test_estimator.py`, `test_inference.py`).
`REPOSITORIES.md` pointed at the old path.
- **TabPFN dropped the `test_targets_MB` signature sniff.** The loader used to
decide v2.6-vs-v3 regressor criterion handling by inspecting `model.forward`
for that parameter. It now branches on the data instead: `criterion.*` is
always separated out of the model state, and `_resolve_regression_borders`
prefers the checkpoint's saved borders, falls back to the model's
`regression_borders` buffer, and raises if neither is present. Corrected in
`REPOSITORIES.md` and `SUMMARIES.md`. **The practical advice is unchanged** —
write `criterion.*` for regressors unconditionally and the checkpoint
round-trips on both architectures.
- **Worth knowing if you use TabTune:** its vendored TabPFN copy *still* carries
the `test_targets_MB` sniff and the vestigial parameter it tests for, so on this
point TabTune's bundled loader and current upstream are not interchangeable.
Recorded in `REPOSITORIES.md`.

## 2026-08-26

Zotero-side only — no papers added, no documents changed in substance.

- **`08. TabPFN Originals` retired in favour of a saved search.** The collection held
six hand-picked papers; the intent was "anything the TabPFN originators wrote", which is
a rule, not a list. `★ TabPFN Originals (auto)` matches any item with **Müller,
Hollmann, Grinsztajn or Hutter** among the creators and returns **22** items — a strict
superset that misses none of the six. All six were already in other collections, so
deleting the collection stranded nothing.
- **Collections renumbered `00`–`18`** to close the gap the deletion left. `Tabular
Foundation Models` is now **`08`**, and every reference in `AGENTS.md`, `README.md` and
the assignment rules moved with it. This is the second renumbering; nothing broke either
time, because every tool matches the collection by **name substring** rather than by
number — which is now stated as the reason in `AGENTS.md`.
- **`★ My publications` removed** — Zotero has My Publications built in.
- **`★ Added in the last 30 days` was genuinely broken**, not merely empty: 51 items
qualified while the search returned none. The value `30 d` is not parseable — Zotero
reads `isInTheLast` as `<number> <unit>` with a spelled-out unit — so it is now `30
days`.
- Useful discovery for future work: the local API endpoint **`/searches/<key>/items`
executes a saved search and returns its results**, so a saved search can be verified
programmatically instead of by eye.

## 2026-08-20

- Added **Shaheen et al. 2026-08 — Understanding the Surprising Generalization
Properties of Tabular Foundation Models** (arXiv 2608.17957), 46 → 47 papers, filed
from Zotero with `new_paper.py --zotero`.
- **This is the first paper in the collection to attack the paradigm's founding
claim.** Every model here descends from Müller 2021's argument that a PFN approximates
the Bayesian posterior predictive *under its prior*, which requires downstream tasks to
lie in that prior's support. Shaheen trains 88 models, each on a **single real table**,
and evaluates them on 107 held-out datasets: one trained only on vectorized MNIST
transfers to California Housing. A prior induced by one table cannot cover that task, so
the authors propose TFMs are learned **retrieval-and-aggregation** procedures — closer
to kNN than to a fitted predictor — and back it with a retrieve-and-copy probe and a
`W_Q = W_K` intervention that makes attention an explicit negative squared distance.
- Recorded in **Where the papers disagree** as two rows, because it disputes two
separate consensus positions: the Bayesian account of *why* TFMs work, and the scaling
line's premise that only a massive, diverse corpus enables out-of-domain transfer.
- **It also completes Nagler 2023.** His localisation gap said bias vanishes only if the
predictor localises around the query, which nothing in the architecture guarantees; if
retrieval is what the models learn regardless, that 2023 analysis becomes the most
predictive piece of theory in this collection. Noted in the Foundations section.
- Two corpus-design findings worth carrying: **feature count predicts transfer and row
count does not** (R² = 0.67 from simple meta-features, width dominating), because
pretraining manufactures tasks from target-column and feature-subset choices, so wide
tables yield combinatorially many tasks; and **column-level cleaning helps while
dataset-level filtering, deduplication included, does not**.
- Discounts recorded: real-data pretraining only, so it does not directly speak to the
synthetic-prior frontier it questions; row-based attention only, so v2's cell-based
bi-attention and the column-compress designs are untested; preprint; no calibration
reported — pointed given that calibrated posteriors are what the Bayesian framing was
invoked to explain.

## 2026-08-19

- Added **Wu and Bergman 2025-10 — APT** (ICML 2025) and **Arbel et al.
  2025-12 — EquiTabPFN** (NeurIPS 2025), 44 → 46 papers, both filed
  straight from Zotero with `new_paper.py --zotero`.
- **APT makes the prior adaptive.** A minority (12.5%) of pretraining
  generators are adversarial agents that shift their own data-generating
  distribution toward whatever the model currently handles badly. That is
  a third distinct lever on prior design alongside Mitra's *mixing* and
  O'Prior's *comparison*, and the one most directly relevant to designing
  a domain-targeted prior. Its evaluation also drops the class/feature/
  categorical/missing-value filters that earlier PFN headlines relied on.
- **EquiTabPFN names an architectural defect from inside Prior Labs.**
  Tabular targets have no canonical ordering, yet permuting them changes
  TabPFN's predictions; the paper formalises the irreducible
  *target-equivariance gap* and closes it by construction. Two
  consequences worth carrying: it explains why permutation ensembling was
  needed at all, and its **TabPFNv2\*** baseline — v2's architecture
  retrained on the *public* prior — is the control this library has
  repeatedly noted is missing whenever a closed prior is compared.
- Both papers independently remove the **class-count cap**, by unrelated
  mechanisms (APT's mixture block, EquiTabPFN's target equivariance),
  which is decent evidence it was a real limitation rather than a
  cosmetic one. Recorded against weakness §5 and design axis (d).
- **`SUMMARIES.md` is now the complete per-paper reference, and the only
  one.** Every entry carries all four house sections — where it fits, what
  it contains, strengths, limitations — where previously only 2 of 46 did.
  The strengths and limitations were folded in from the `SYNTHESIS.md`
  appendix cards, which said the same things about the same papers in a
  second place. Entries are rewrapped from a ~55-character hard wrap to
  ~96, roughly doubling the readable line length.
- **`SYNTHESIS.md` is now a synthesis and nothing else — the 46-card
  per-paper appendix is gone.** Two documents were each half a per-paper
  reference; they are now one reference and one argument. The synthesis
  opens by stating its own shape, each section inherits the previous one
  instead of restarting, and a new **Where the papers disagree** section
  makes the contested claims explicit: what was asserted, who overturned
  it, and whether it is settled — TuneTables' PEFT premise overturned by
  Rubachev, retrieval withdrawn by the lab that introduced it, the
  real-vs-synthetic prior question still open, CausalFM's theorem losing
  to CausalPFN's empirics, and the architectural "consensus" that one
  strong open model declines.
- **APT and EquiTabPFN entered the argument, not just the timeline.** Both
  had been filed with a timeline row and a card but were absent from the
  prose. APT now sits in the prior discussion as the third lever
  (adaptive, next to Mitra's mixing and O'Prior's comparison), and
  EquiTabPFN anchors a new thread on symmetry running through the whole
  model line — rows, then columns, then targets, each discovered late and
  each explaining a workaround the field had been paying for.
- `check_docs.py` follows: it no longer counts appendix cards, and instead
  **verifies every summary carries all four sections**, so an incomplete
  entry now fails the build rather than passing unnoticed.
- Caveat recorded for the credit projects: EquiTabPFN finds 5 of 86
  benchmark datasets have **ordinal** targets, which are genuinely *not*
  permutation-equivariant — relevant to rating-grade targets.

## 2026-08-18

Zotero documented as the upstream of this library, in `AGENTS.md` (the
rules) and `README.md` (the workflow).

- **`new_paper.py` can start from a Zotero item: `--zotero <key>`.** It
  takes the title, authors, date and the attached PDF straight from the
  record the owner already curated, instead of re-deriving them from the
  PDF — which is exactly how a wrong author list got introduced during
  this work. It **refuses an item that is not in the mirrored
  collection**, so the scope rule is enforced by the tool rather than by
  memory, and it warns when Zotero's date disagrees with the arXiv
  banner, since that disagreement decides the filename.
- **`09. Tabular Foundation Models` in Zotero is now the stated
  definition of what belongs in `papers/`.** The owner's Zotero holds
  their whole reading list — causal inference, credit risk, statistics,
  regulation — and an agent working here can query all of it. That makes
  an explicit rule necessary: seeing a source in Zotero is *not* a reason
  to add it here, because a paper kept in `11. Causal ML` and not in the
  TFM collection is a deliberate scope judgement. Divergence between the
  two is a **report, not a repair**.
- **Documented the three ways into Zotero and what each can do.** The
  Local API (`localhost:23119`) is read-only — it answers `501 Method not
  implemented` to a write — the Web API can write with a key held in the
  `ZOTERO_API_KEY` environment variable, and `zotero.sqlite` must never
  be written at all.
- **Recorded the trap that cost the most time: `zotero.sqlite` lags the
  running application by an unbounded amount.** It reported 26
  collections while the live API reported 16, because the deletions were
  still inside an open transaction. Any tool here reads the Local API and
  treats the file as a fallback for when Zotero is closed.
- **Agents must now source bibliographic metadata from Zotero first**,
  then CrossRef/OpenAlex, then the PDF — and never invent a field. Better
  BibTeX maintains a `citationKey` on every item, which is what to cite
  by when writing anything destined for a manuscript.
- The collection is matched **by name substring, never by number**, so
  the mirror survives renumbering — which it has already had to.

## 2026-08-12

`scripts/` reorganised by job, three new tools, and a `README.md` rebuilt
around "what is in each folder".

- **`scripts/` now has subfolders**, one per job: `papers/` (add and
  extract), `checks/` (four read-only consistency checks), `dumps/` (the
  gitingest refresh), `hooks/`, and `lib/` for shared code. `maintain.py`
  and `propagate_to_downstream.py` stay at the top because they are the
  two you actually run. Every documented path was updated; nothing else
  changed about how the scripts behave.
- **New `scripts/lib/library.py`.** The shape of this repository —
  where papers live, how a filename decomposes into date/author/title,
  how to read an arXiv stamp out of an extraction, how GitHub slugifies a
  heading — was being re-derived in each script, slightly differently
  each time. One of those re-derivations was already wrong. It now has a
  single implementation.
- **New `scripts/papers/new_paper.py`.** Does the mechanical half of the
  five-step add-a-paper procedure: files the PDF under the house naming
  rule (metadata from the arXiv API, falling back to the PDF's own arXiv
  banner rather than to today's date), extracts the text, and inserts
  `TODO(new-paper)` placeholders in the correct chronological slot in all
  four documents. It writes no prose on purpose — a plausible
  auto-summary is worse than a missing one, because nobody would notice
  it was never written.
- **New `scripts/checks/check_symbols.py`**, wired into `maintain.py` as
  the `symbols` stage. AGENTS.md rule 5 asks for a spot-check that cited
  symbols survive a dump refresh; this does all 175 of them. Attribution
  is the whole difficulty: subsections inherit their parent's dump,
  headings naming several dumps are satisfied by any one, a sentence that
  names a dump adds it, and `SUMMARIES.md`/`SYNTHESIS.md` are checked
  against the whole corpus rather than a dump guessed from context. A
  naive version reported 33 failures, all false. Four genuine absences
  are listed with their reason — names upstream deleted, a path the
  refresh filters out — because the documents describe them *as* absent.
- **New pre-commit hook** (`scripts/hooks/`, installed with
  `python scripts/hooks/install.py`). Runs `check_docs.py` on every commit
  and `check_symbols.py` when a document or dump is staged. Offline only.
  Installed via `core.hooksPath` so the hook stays under version control
  instead of hiding in `.git/hooks/`.
- **`check_zotero_sync.py`: two fixes, and the Zotero check is now
  clean for the first time.** It counted **trashed** items as collection
  members, because Zotero keeps collection membership until the trash is
  emptied — so a paper deliberately deleted in Zotero was reported
  forever as "in Zotero but missing from `papers/`". The standing "1
  issue to resolve by hand" (*From Tables to Time*, allegedly missing a
  PDF attachment) was that phantom; both sides now report 44/44 and
  agree. Collection lookup also accepts an unambiguous substring, so the
  numbered collection names used here (`1.14. Tabular Foundation
  Models`) keep resolving when the numbering changes.
- **`check_docs.py` now fails on unfinished scaffolds.** Without it a
  `TODO(new-paper)` placeholder would satisfy every coverage count while
  saying nothing, which is worse than a missing entry.
- **`README.md` restructured.** Introduction and the submodule commands
  first, then one section per folder describing every file in it, then
  the contents table at the end.
- **Considered and rejected: tracking citation counts per paper.** Built
  and tested, then removed, so nobody rebuilds it without knowing why.
  Google Scholar — the number people actually quote — has no API, and
  scraping it violates Google's terms and CAPTCHA-blocks the IP; the only
  fast route is a paid third-party scraper. The free alternatives are not
  a substitute: OpenAlex indexes the arXiv preprint record separately from
  the published one and returned **0** for most of this collection, while
  Semantic Scholar returned 68 for the same paper. Semantic Scholar's
  anonymous pool also rate-limited a single 44-paper sweep **173 times**.
  If this is ever revisited, use the batch endpoints — Semantic Scholar
  takes 500 ids in one POST, OpenAlex 50 per filtered page — so the whole
  library is two requests, not 88.

## 2026-08-07

- **New `scripts/propagate_to_downstream.py`.** Finds every repository on
  disk that embeds this library as a submodule and moves its pin to the
  commit checked out here — this folder is the ground truth. It refuses to
  run when this repository is dirty or has unpushed commits, because a pin
  must exist on `origin` or a collaborator's `submodule update --init`
  cannot fetch it; it commits only the submodule path, so unrelated work in
  a consuming project is never swept into the bump; and it never pushes
  downstream unless asked. `--dry-run` shows the plan.
- **New `scripts/check_docs.py`**, wired into `maintain.py` as the `docs`
  stage. Checks coverage (every paper has an extraction, a summary entry, an
  overview row, a timeline row and an appendix card, with counts agreeing),
  chronological order across all four sequences, link and anchor
  resolution, changelog ordering/duplicates/future dates, and
  project-neutrality of the shared documents.
- The anchor check implements **GitHub's** slug rule, which deletes
  punctuation but preserves the surrounding spaces — so `Timeline & lineage`
  becomes `timeline--lineage` with two hyphens. Naive implementations
  collapse whitespace and report a false failure on every heading
  containing punctuation, which is what a throwaway check did before this
  script existed.

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
