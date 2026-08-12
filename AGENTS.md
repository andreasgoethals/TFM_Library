# AGENTS.md — how AI agents must treat this repository

**First, establish which side of the boundary you are on.** Everything
below depends on it.

| Where you are | What you may do |
|---|---|
| **In this repository's own checkout** — you were launched *in* the TFM Library, and this file sits at your working-directory root | Read **and** edit. This is the only place the library is ever edited. |
| **In a downstream project** that contains this library as a folder (e.g. `creditpfn/tfm-library/`) | **READ ONLY. Never create, edit, move, or delete anything inside this folder.** |

## What this is

The single canonical collection of tabular-foundation-model (TFM)
knowledge: paper PDFs + text extractions (`papers/<year>/`), per-paper
summaries (`SUMMARIES.md`), the cross-paper field synthesis
(`SYNTHESIS.md`), flat-text dumps of upstream reference implementations
(`repositories/`, guide in `REPOSITORIES.md`), and a `CHANGELOG.md` for
consumers deciding when to update. `scripts/` holds the maintenance
tools, grouped by job (`papers/`, `checks/`, `citations/`, `dumps/`,
`hooks/`, `lib/`); `README.md` documents every one of them.

It is a **read-only knowledge base**, not a code library. Nothing here is
imported or installed. Downstream agents *read* the literature and grep
the scraped implementations.

## The flow is one-directional

```
   THIS REPOSITORY  ──edited directly──▶  commit  ──▶  push to origin
                                                          │
                       ┌──────────────────────────────────┴──────────────┐
                       ▼                                                 ▼
           creditpfn/tfm-library/                        other-project/tfm-library/
           (pinned, read-only folder)                    (pinned, read-only folder)
```

Edits happen **here and only here**. Downstream projects receive updates
by bumping their pinned commit. They never push changes back, and no
downstream edit can ever reach this repository.

## Rules for an agent working INSIDE this repository

1. **Everything shared must be project-neutral.** `SUMMARIES.md`,
   `SYNTHESIS.md` and `REPOSITORIES.md` describe the literature for
   *every* consumer. No project's pipeline paths, config values,
   hyperparameter choices, dataset registry, cluster details, or
   relevance rankings belong in them. Write "a downstream project
   should…", never "our `src/train/` does…". Project-specific material
   belongs in that project's own `PROJECT_SPECIFIC.md` — see
   [`PROJECT_SPECIFIC.template.md`](PROJECT_SPECIFIC.template.md), which
   lives in the project's copy of this folder and is gitignored here.
2. **Scope is strictly tabular foundation models**: the PFN/TabPFN
   lineage, direct TFM competitors, and TFM variants/derivatives.
   Benchmarks, non-foundation-model tabular deep learning, general ML
   methods, and domain application papers are **out of scope** even when
   the corpus cites them heavily.

   **There is exactly one deliberate exception, and it is important:**
   `repositories/VSC Documentation.txt`, the KU Leuven / Flemish
   Supercomputer Centre user documentation. **Never remove or deprioritise
   it.** Every consuming project runs on VSC, so SLURM scripting, partition
   and GPU selection, the Lustre/GPFS storage split, and credit accounting
   are recurring questions for all of them, and having the answers greppable
   offline is worth more than the file costs. Do not add further non-TFM
   files without the owner's explicit request.
3. **Papers are added ONLY when the owner explicitly says so** (or adds
   one themselves). Never collect papers proactively. When the owner does
   ask, follow all five steps:
   1. PDF into `papers/<year>/` as `MM_Author_et_al._Title.pdf`, where
      `<year>` and `MM` are the year and **month** of the version being
      filed, so papers sort chronologically. Underscores, no spaces or
      commas; `Author_and_Author` for two authors, `Author_et_al.` for
      three or more; ASCII-fold names (`Müller` → `Muller`).
   2. Extract text:
      `python scripts/papers/extract_paper_text.py papers/<year>/<file>.pdf`
      (writes the mirror `papers/text/<year>/<same-name>.txt`).
   3. Add a `SUMMARIES.md` entry in the house style (venue → where it
      fits → what it contains → strengths/limitations), plus a row in the
      overview table.
   4. Integrate into `SYNTHESIS.md`: timeline row, the fitting thematic
      section, and an appendix card.
   5. Log it in `CHANGELOG.md`.

   `python scripts/papers/new_paper.py <pdf>` does steps 1–2 and puts
   `TODO(new-paper)` placeholders in the right chronological slot for 3–5.
   It writes **no prose** — steps 3 and 4 are the actual work and are
   yours. `check_docs.py` fails while any placeholder survives.
4. **Cite code dumps by symbol name, never by line number.** The dumps
   are periodically refreshed and line numbers drift by thousands.
   `` `TabPFN .txt`, `save_tabpfn_model` `` — yes.
   `` `TabPFN .txt:12211` `` — never.
5. **Refreshing a dump:** run
   `python scripts/dumps/refresh_repositories.py`, then run
   `python scripts/checks/check_symbols.py` — it verifies exhaustively
   that every symbol cited in `REPOSITORIES.md`, `SUMMARIES.md` and
   `SYNTHESIS.md` still exists, which is what "spot-check" used to mean
   by hand. Note the refresh in `CHANGELOG.md`.
6. **Every substantive change gets a `CHANGELOG.md` entry** (date, what,
   why, one line each). Consumers pin commits; the changelog is how a
   human decides whether to update.
   Before committing, run `python scripts/checks/check_docs.py`; it
   catches coverage gaps, broken links and anchors, chronology errors,
   duplicate or future changelog dates, and project-specific material
   that has leaked into a shared document. `python scripts/maintain.py`
   runs it along with everything else.
7. **Do not push.** Commit locally when asked; pushing this repository —
   and updating the pin in any consuming project — is the owner's action.
8. **Large files:** anything >95 MB must be gitignored (see
   `repositories/TabPFN Wide.txt`) and documented as locally
   regenerable.
9. **Never hand-edit `papers/text/**`** — those files are generated by
   `scripts/papers/extract_paper_text.py`, so manual fixes are lost on
   the next extraction. Fix the script instead. The same goes for
   `data/citations.csv`: it is append-only history written by
   `scripts/citations/citations.py`, and editing a past row rewrites a
   measurement.

## Rules for an agent working in a DOWNSTREAM project

You are reading this file inside someone else's repository. The folder
containing it is a pinned, read-only snapshot of a shared library.

1. **Never write inside this folder.** No edits, no new files, no
   renames, no deletions — not even to fix an obvious typo, and not to
   add your project's notes. Your project's history does not track this
   folder's contents, so anything you write here is either lost on the
   next update or silently corrupts a shared resource.
2. **Read freely.** That is the entire point. Grep `SUMMARIES.md` and
   `SYNTHESIS.md` for the literature, `REPOSITORIES.md` +
   `repositories/*.txt` for how upstream code actually works, and
   `papers/text/<year>/*.txt` for full paper text.
3. **The one exception is `PROJECT_SPECIFIC.md`** — the only file a
   downstream project may create inside this folder, by copying
   `PROJECT_SPECIFIC.template.md`. It is gitignored by the library, so it
   never dirties the library's status and can never be pushed upstream.
   Every project-specific note about this literature goes there,
   following the rules in the template.
4. **If a shared document is wrong**, do not patch it here. Report it to
   the owner so it can be fixed in the library's own checkout and flow
   down to every consumer.
5. **Cite by path, and record the pin.** Reference papers as
   `<mountpoint>/papers/<year>/<file>.pdf`. When a result depends on the
   literature, record which library commit was pinned — that is what
   makes the claim reproducible.

## Notes

- This repository is **public**.
- Consuming projects see the **commit they have pinned**, not this
  repository's latest state. An edit made here is invisible downstream
  until that project updates its pin.
