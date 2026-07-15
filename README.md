# tfm-library — shared tabular-foundation-model knowledge base

> **⚠️ FOR AGENTS AND HUMANS: this directory is a SHARED GIT SUBMODULE,
> mounted into multiple independent research projects.** It is NOT owned by
> the project you found it in. Everything here — the paper collection, the
> literature summaries, the upstream code dumps — is the single canonical
> copy shared by every consuming project, so that all of them work from the
> same, consistently maintained understanding of the tabular-foundation-model
> (TFM) literature and reference implementations.

## What's inside

| Path | What it is |
|---|---|
| [`papers/`](papers/) | Every collected TFM paper as PDF, named `YYYY_Author_et_al._Title.pdf`, plus full text extractions in [`papers/text/`](papers/text/) (same basename, `.txt`) so agents can grep/read without PDF tooling. |
| [`LITERATURE.md`](LITERATURE.md) | Chronological per-paper tour: venue, where it fits, what it contains, strengths/weaknesses, and per-project relevance notes. |
| [`SUMMARY.md`](SUMMARY.md) | The cross-paper synthesis of the whole TFM paradigm — lineage timeline (PFNs → TabPFN v1/v2/2.5/3 → scaling/adaptation/extensions), design-axis comparison, recurring weaknesses, open frontiers, one-card-per-paper appendix. **Read this first to understand the field.** |
| [`repositories/`](repositories/) | Flat-text dumps (via `gitingest`) of the upstream reference implementations (TabPFN, TabPFN extensions, finetuning repos, nanoTabPFN, TabDPT, …) — greppable ground truth for "how does the official code actually do X". |
| [`REPOSITORIES.md`](REPOSITORIES.md) | What each dump is, why it's kept, and what to grep for when designing pipeline stages. |
| [`scripts/refresh_repositories.py`](scripts/refresh_repositories.py) | Standalone refresher: re-snapshots every `repositories/*.txt` from its GitHub source (`pip install gitingest`, then `python scripts/refresh_repositories.py`). |

Note: `repositories/TabPFN Wide.txt` (~366 MB) exceeds GitHub's file limit and
is **gitignored** — regenerate it locally with the refresh script when needed.
`repositories/VSC Documentation.txt` is cluster (KU Leuven VSC) documentation
rather than TFM literature; it lives here because every consuming project runs
on that cluster.

## Rules of the road (agents: follow these)

1. **Edits here propagate to every project.** Improve summaries, add papers,
   refresh dumps — that benefits everyone. But never delete or rewrite
   another project's relevance notes (the "For <project>" sections in
   `LITERATURE.md` / `SUMMARY.md`); add your project's own section beside them.
2. **Adding a paper**: drop the PDF in `papers/` using the naming convention,
   extract its text to `papers/text/<same-name>.txt` (e.g. via `pypdf`), add a
   `LITERATURE.md` entry (house style: venue → where it fits → contents →
   limitations → per-project relevance) and integrate it into `SUMMARY.md`
   (timeline row + thematic section + appendix card).
3. **Citing the code dumps**: cite by **symbol name** (`TabPFN .txt`,
   `save_tabpfn_model`), never by line number — the dumps are periodically
   refreshed and line numbers drift by thousands.
4. **This submodule is pinned per-project.** A consuming project sees the
   commit it has pinned, not necessarily the latest. After changing this repo:
   commit + push HERE, then in each consuming project run
   `git submodule update --remote <mountpoint>` and commit the bumped pointer.
5. **Copyright**: the PDFs are for private research use. Keep this repository
   **private**; do not fork it public.

## Using it in a new project

```bash
# in the consuming project's repo root:
git submodule add <this-repo's-github-url> tfm-library
git commit -m "add tfm-library knowledge base as submodule"
# fresh clones of the project then need:
git clone --recursive <project-url>          # or, after a plain clone:
git submodule update --init
# pull the latest library state into a project:
git submodule update --remote tfm-library
```

## Consuming projects

| Project | Mountpoint | Since |
|---|---|---|
| [CreditPFN](https://github.com/andreasgoethals/CreditPFN) | `tfm-library/` | 2026-07 |

(Add a row when you wire this into a new project.)
