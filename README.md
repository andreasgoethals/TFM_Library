# TFM Library

A personal, curated knowledge base on **tabular foundation models (TFMs)** —
the TabPFN family and everything around it. This repository keeps track of
two things, in one place, for every research project that needs them:

1. **All the interesting literature** — every collected paper as PDF with a
   full-text extraction, plus two levels of written digest: per-paper
   summaries and a cross-paper synthesis of the whole field.
2. **All the reference repositories** — flat-text snapshots of the upstream
   implementations (TabPFN, its extensions, finetuning codebases, …) so that
   "how does the official code actually do X?" is always answerable with a
   text search, offline, against the exact code the papers shipped.

It is designed to be mounted as a **git submodule** inside multiple research
projects (CreditPFN and future ones), so all of them share one consistently
maintained copy instead of each drifting on its own. If you are an AI agent:
read [`AGENTS.md`](AGENTS.md) before touching anything here.

## Contents

| Path | What you'll find |
|---|---|
| [`SYNTHESIS.md`](SYNTHESIS.md) | **Start here.** The cross-paper synthesis of the TFM paradigm: lineage timeline (PFNs → TabPFN v1/v2/2.5/3 → scaling / adaptation / extensions), the design axes on which the field varies, recurring weaknesses, open frontiers, and a one-card-per-paper appendix. |
| [`SUMMARIES.md`](SUMMARIES.md) | The per-paper tour, chronological: venue, where each paper fits, what it contains, strengths/limitations, and per-project relevance notes. |
| [`papers/`](papers/) | The PDFs, named `YYYY_Author_et_al._Title.pdf`, with full text extractions under [`papers/text/`](papers/text/) (same basename, `.txt`). |
| [`REPOSITORIES.md`](REPOSITORIES.md) | What each code dump is, why it's kept, and what to grep for when building on it. |
| [`repositories/`](repositories/) | The flat-text code snapshots themselves (made with `gitingest`). |
| [`CHANGELOG.md`](CHANGELOG.md) | Human-readable log of library updates — check it before bumping a project's submodule pin. |
| [`scripts/`](scripts/) | Maintenance tools: `refresh_repositories.py` (re-snapshot all dumps), `extract_paper_text.py` (PDF → `papers/text/`). |

## How to browse

- *"I want to understand the field"* → read `SYNTHESIS.md` top to bottom.
- *"What did paper X actually do?"* → `SUMMARIES.md`, or grep the full text
  in `papers/text/`.
- *"How does the official implementation handle Y?"* → `REPOSITORIES.md`
  to pick the right dump, then grep `repositories/*.txt` by symbol name.

## Using this library in a project

```bash
git submodule add <this-repo-url> tfm-library     # once, in the project root
git submodule update --init                        # after a fresh clone
git submodule update --remote tfm-library          # pull the latest library
```

Each project pins a specific commit of this library — reproducible by
construction. After improving the library, bump the pin in each consumer.

## Housekeeping notes

- `repositories/TabPFN Wide.txt` (~366 MB) exceeds GitHub's file limit and is
  gitignored; regenerate locally with `python scripts/refresh_repositories.py`.
- `repositories/VSC Documentation.txt` is KU Leuven VSC cluster documentation
  — not TFM literature, but shared here because every consuming project runs
  on that cluster.
- **Keep this repository private**: the PDFs are copyrighted publisher
  material, collected for private research use.

## Consuming projects

| Project | Mountpoint | Since |
|---|---|---|
| [CreditPFN](https://github.com/andreasgoethals/CreditPFN) | `tfm-library/` | 2026-07 |
