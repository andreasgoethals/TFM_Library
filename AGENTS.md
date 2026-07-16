# AGENTS.md — how AI agents must treat this repository

**You are inside a SHARED knowledge base, not the project you were launched
from.** This repository is mounted as a git submodule into multiple
independent research projects (CreditPFN and others). Whatever you change
here propagates — by design — to every one of those projects the next time
they bump their submodule pin. Act accordingly.

## What this is

The single canonical collection of tabular-foundation-model (TFM) knowledge
shared across the owner's projects: paper PDFs + text extractions
(`papers/`), per-paper summaries (`SUMMARIES.md`), the cross-paper field
synthesis (`SYNTHESIS.md`), flat-text dumps of upstream reference
implementations (`repositories/`, guide in `REPOSITORIES.md`), and a
`CHANGELOG.md` for consumers deciding when to update their pin.

## Rules

1. **Never delete or rewrite another project's material.** The relevance
   notes ("For CreditPFN…", "For <project>…") in `SUMMARIES.md` and
   `SYNTHESIS.md` belong to their projects. Add your project's own notes
   beside them; do not "clean up" someone else's.
2. **Shared content must stay project-neutral.** When editing the common
   parts (paper descriptions, the synthesis narrative, `REPOSITORIES.md`),
   write for every consumer, not just the project you came from. Project-
   specific reasoning goes in the per-project notes or in your own project's
   repo — not here.
3. **Cite code dumps by symbol name, never by line number.** The dumps are
   periodically refreshed (`scripts/refresh_repositories.py`) and line
   numbers drift by thousands. `` `TabPFN .txt`, `save_tabpfn_model` `` —
   yes. `` `TabPFN .txt:12211` `` — never.
4. **Papers are added ONLY when the owner explicitly says so** (or adds
   one themselves). Never collect papers proactively. When the owner does
   ask, follow the full procedure — all five steps:
   1. PDF into `papers/` as `YYYY_Author_et_al._Title.pdf` (underscores, no
      spaces or commas).
   2. Extract text: `python scripts/extract_paper_text.py papers/<file>.pdf`.
   3. Add a `SUMMARIES.md` entry in the house style (venue → where it fits →
      what it contains → limitations → per-project relevance).
   4. Integrate into `SYNTHESIS.md`: timeline row, the fitting thematic
      section, and an appendix card.
   5. Log it in `CHANGELOG.md`.
5. **Refreshing a dump**: run the refresh script, then spot-check that
   symbol names cited in `SUMMARIES.md`/`REPOSITORIES.md`/consumer code
   still exist; note the refresh in `CHANGELOG.md`.
6. **Every substantive change gets a `CHANGELOG.md` entry** (date, what,
   why, one line each). Consumers pin commits; the changelog is how a human
   decides whether to bump.
7. **Do not push.** Commit locally when asked; publishing this repository
   (and bumping submodule pointers in consuming projects) is strictly the
   owner's action.
8. **Do not make this repository public, and do not copy the PDFs
   elsewhere** — copyrighted material for private research use.
9. **Large files:** anything >95 MB must be gitignored (see
   `repositories/TabPFN Wide.txt`) and documented as locally-regenerable.

## Relationship to consuming projects

- A consuming project sees the COMMIT it has pinned, not this repo's latest.
  If you edit the library from inside a project checkout, remember the edit
  is invisible to the project until its pin is bumped
  (`git submodule update --remote <mountpoint>` + commit, by the owner).
- Paths inside consumers: reference this library through the mountpoint
  (e.g. `tfm-library/papers/…`), never with `../` escapes from the
  submodule back into a specific project.
