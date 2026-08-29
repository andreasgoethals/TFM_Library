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
tools, grouped by job (`papers/`, `checks/`, `dumps/`, `hooks/`,
`lib/`); `README.md` documents every one of them.

It is a **read-only knowledge base**, not a code library. Nothing here is
imported or installed. Downstream agents *read* the literature and grep
the scraped implementations.

## Zotero is upstream of this repository

The owner's reference manager is **Zotero**, and it holds *all* of their
sources — causal inference, credit risk, statistics, deep learning,
regulation, fairness, and more — not only tabular foundation models. It
is the upstream of this repository and it is **queryable by an agent
working here**, so use it rather than guessing.

| | How | Can it write? |
|---|---|---|
| **Local API** | `http://localhost:23119/api/users/0/…` — mirrors the Zotero Web API, no key, requires Zotero running with Settings → Advanced → *Allow other applications on this computer to communicate with Zotero* | **No.** `501 Method not implemented` |
| **Web API** | `https://api.zotero.org/users/<id>/…` with header `Zotero-API-Key` | Yes |
| **`zotero.sqlite`** | direct file read | **Never write.** And reads are unreliable — see below |

The API key lives in the **`ZOTERO_API_KEY` user environment variable**.
Read it from the environment; never write it into a file in this
repository, which is public.

**Do not read `zotero.sqlite` when Zotero is running.** The file lags the
application by an unbounded amount — it has been observed reporting 26
collections while the live API reported 16, because the deletions were
still sitting in an open transaction. Use the Local API and treat the
SQLite path as a fallback for when Zotero is closed.

### Which collection this repository mirrors

**`08. Tabular Foundation Models`.** That collection *is* the definition
of what belongs in `papers/` — one PDF here per item there, and nothing
else. Three rules follow:

- **Seeing a source in Zotero is not a reason to add it here.** If the
  owner keeps a paper in `10. Causal ML — Foundations` or `16. Credit Risk Modelling`
  and not in the TFM collection, that is a deliberate judgement that it
  is out of scope. Do not "helpfully" pull it in.
- **A divergence is a report, not a repair.** Run the check, say what
  differs, let the owner decide which side is wrong. Never add or delete
  a paper to make the numbers agree.
- **Match the collection by name substring, never by number.** The
  numeric prefixes are sort keys and get renumbered — they have been
  renumbered twice already — so `"Tabular Foundation Models"` is the
  stable handle. `check_zotero_sync.py` already does this, which is why
  neither renumbering broke it.

### Use Zotero as the metadata source

When you need a paper's venue, DOI, authors, year, abstract or citation
key, **query Zotero first**. It is curated, it is the same record the
owner will cite from, and it is more reliable than re-deriving the
information from a PDF's first page or recalling it. In order of
preference:

1. The Zotero item (Local API) — `creators`, `date`, `DOI`,
   `publicationTitle`/`proceedingsTitle`, `abstractNote`, `citationKey`.
2. CrossRef by DOI, or OpenAlex — authoritative and free.
3. The PDF itself.

Never invent bibliographic detail. If none of the three can confirm a
field, say it is unconfirmed and leave it empty.

**Better BibTeX** is installed and maintains a `citationKey` on every
item, reachable at `http://localhost:23119/better-bibtex/json-rpc`
(read-only). Cite by that key when writing anything the owner will paste
into a manuscript.

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
   the corpus cites them heavily — and even when you can see them in the
   owner's Zotero, which holds their whole reading list. The operational
   test is membership of the `08. Tabular Foundation Models` collection;
   see [above](#which-collection-this-repository-mirrors).

   **There is exactly one deliberate exception, and it is important:**
   `repositories/VSC Documentation.txt`, the KU Leuven / Flemish
   Supercomputer Centre user documentation. **Never remove or deprioritise
   it.** Every consuming project runs on VSC, so SLURM scripting, partition
   and GPU selection, the Lustre/GPFS storage split, and credit accounting
   are recurring questions for all of them, and having the answers greppable
   offline is worth more than the file costs. Do not add further non-TFM
   files without the owner's explicit request.
3. **Papers are added ONLY when the owner explicitly says so** (or adds
   one themselves). Never collect papers proactively — the trigger is
   always the owner, and the source of truth for *what* is in scope is
   the `08. Tabular Foundation Models` collection in Zotero. When the
   owner does ask, follow all five steps:
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
   4. Integrate into `SYNTHESIS.md`: a timeline row, and — the part that
      matters — a place in the argument. `SYNTHESIS.md` carries no
      per-paper appendix: it compares and contrasts, so a new paper earns
      its place by what it confirms, extends or contradicts. If it
      disputes an existing result, say so in *Where the papers disagree*.
   5. Log it in `CHANGELOG.md`.

   `python scripts/papers/new_paper.py --zotero <item-key>` does steps
   1–2 and puts `TODO(new-paper)` placeholders in the right chronological
   slot for 3–5. **Prefer the `--zotero` form**: it takes the title,
   authors, date and PDF from the curated Zotero item instead of
   re-deriving them, and refuses any item outside the mirrored
   collection. A plain PDF path still works as a fallback.
   It writes **no prose** — steps 3 and 4 are the actual work and are
   yours. `check_docs.py` fails while any placeholder survives.
4. **Cite code dumps by symbol name, never by line number.** The dumps
   are periodically refreshed and line numbers drift by thousands.
   `` `TabPFN .txt`, `save_tabpfn_model` `` — yes.
   `` `TabPFN .txt:12211` `` — never.
5. **Name the paper, not just the author, when citing one document from
   another.** In `SUMMARIES.md` and `SYNTHESIS.md`, a reference to another
   paper carries its **title** alongside the author-year — `Nagler 2023
   (*Statistical Foundations of Prior-Data Fitted Networks*)`, not `Nagler
   2023`. Author-only is the ordinary scholarly convention and it is what
   these documents used until 2026-08-29; the owner asked for titles because
   a passage should be readable without stopping to look the citation up,
   and several authors here have two or three papers in the corpus.

   Apply it on the **first mention within each section**, then the short form
   afterwards — repeating a full title every time destroys the prose. A
   citation that already names the paper (`Qu 2025 (TabICL)`, `Zhang 2025's
   Mitra`) already satisfies this. Cross-document links point at the anchor
   in the other file: `[…](SUMMARIES.md#nagler-theory)` from `SYNTHESIS.md`,
   since `check_docs.py` resolves bare `#anchor` links **within the same
   document only**.
6. **Refreshing a dump:** run
   `python scripts/dumps/refresh_repositories.py`, then run
   `python scripts/checks/check_symbols.py` — it verifies exhaustively
   that every symbol cited in `REPOSITORIES.md`, `SUMMARIES.md` and
   `SYNTHESIS.md` still exists, which is what "spot-check" used to mean
   by hand. Note the refresh in `CHANGELOG.md`.
7. **Every substantive change gets a `CHANGELOG.md` entry** (date, what,
   why, one line each). Consumers pin commits; the changelog is how a
   human decides whether to update.
   Before committing, run `python scripts/checks/check_docs.py`; it
   catches coverage gaps, broken links and anchors, chronology errors,
   duplicate or future changelog dates, and project-specific material
   that has leaked into a shared document. `python scripts/maintain.py`
   runs it along with everything else.
8. **Do not push.** Commit locally when asked; pushing this repository —
   and updating the pin in any consuming project — is the owner's action.
9. **Large files:** anything >95 MB must be gitignored (see
   `repositories/TabPFN Wide.txt`) and documented as locally
   regenerable.
10. **Never hand-edit `papers/text/**`** — those files are generated by
   `scripts/papers/extract_paper_text.py`, so manual fixes are lost on
   the next extraction. Fix the script instead.

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
