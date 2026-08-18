# TFM Library

A curated knowledge base on **tabular foundation models (TFMs)** — the
TabPFN family and everything around it. It keeps two things in one place,
for every research project that needs them:

1. **All the interesting literature** — every collected paper as PDF with
   a full-text extraction, plus two levels of written digest: per-paper
   summaries and a cross-paper synthesis of the whole field.
2. **All the reference repositories** — flat-text snapshots of the
   upstream implementations (TabPFN, its extensions, finetuning
   codebases, …) so that "how does the official code actually do X?" is
   always answerable with a text search, offline, against the exact code
   the papers shipped.

Scope is **strictly tabular foundation models**: the PFN/TabPFN lineage,
direct TFM competitors, and TFM variants. Benchmarks, ordinary tabular
deep learning, and domain applications are deliberately out of scope.

The library is designed to be mounted as a **read-only folder inside
other projects**, so all of them share one consistently maintained copy.
It is edited *only* in its own checkout — never from inside a consuming
project. If you are an AI agent, read [`AGENTS.md`](AGENTS.md) before
touching anything.

---

<a id="update"></a>

## Using this library in a project

It is embedded as a **git submodule**, so a project always sees one exact,
pinned commit of the literature — which is what keeps a result reproducible
against the sources as they were when it was produced.

Run everything below **in the consuming project** (CreditPFN, CreditICL,
…), never inside the `tfm-library/` folder. One command per line:
**Windows PowerShell has no `&&`**, so chaining with `&&` is a parser
error.

### 1. Add it to a new project

```bash
git submodule add https://github.com/andreasgoethals/TFM_Library.git tfm-library
```

```bash
git commit -m "Add tfm-library as read-only submodule"
```

Then, optionally, create your project's notes file (the one file you are
allowed to add inside the folder — see [the read-only rule](#the-read-only-rule)):

```bash
Copy-Item tfm-library\PROJECT_SPECIFIC.template.md tfm-library\PROJECT_SPECIFIC.md
```

### 2. Update it to the latest version

Already in the project and you want the newest literature. Read
[`CHANGELOG.md`](CHANGELOG.md) first to see what changed, then run these
three, in order:

```bash
git submodule update --remote tfm-library
```

```bash
git add tfm-library
```

```bash
git commit -m "Bump tfm-library pin"
```

The first command only moves the working tree; **the new pin is not
recorded until you `git add` and commit.** Between the two,
`git submodule status` shows a leading `+` — that is normal, not an error.

<details>
<summary>Other things you may need</summary>

PowerShell one-liner for the update (uses `;` and `if ($?)`, not `&&`):

```bash
git submodule update --remote tfm-library; if ($?) { git add tfm-library; git commit -m "Bump tfm-library pin" }
```

After a fresh clone of a consuming project, the folder is empty until you
populate it:

```bash
git submodule update --init
```

Check which commit a project is pinned to:

```bash
git submodule status
```

</details>

<a id="the-read-only-rule"></a>

### The read-only rule

Inside a consuming project, `tfm-library/` is **read-only**. Never edit,
add, move, or delete anything in it — a change there is not tracked by
the consuming project's history and is lost the moment the pin moves.
Corrections go to this repository's own checkout and flow back down.

The single exception: a project may create **`PROJECT_SPECIFIC.md`**
inside the folder, by copying `PROJECT_SPECIFIC.template.md`. That
filename is gitignored by the library, so it never dirties the
submodule's status and can never be pushed upstream. All project-specific
notes about this literature belong there, following the rules in the
template.

### Where to look for what

- *"I want to understand the field"* → read `SYNTHESIS.md` top to bottom.
- *"What did paper X actually do?"* → `SUMMARIES.md`, or grep the full
  text in `papers/text/<year>/`.
- *"How does the official implementation handle Y?"* → `REPOSITORIES.md`
  to pick the right dump, then grep `repositories/*.txt` by symbol name.

---

## Zotero — the upstream of this library

The papers here are not collected ad hoc. They are the contents of **one
Zotero collection**, `09. Tabular Foundation Models`, mirrored onto disk.
Zotero decides *what* is in scope; this repository decides *how* it is
written up.

That means the answer to "should this paper be in the library?" is never
a judgement call made here — it is a question about whether the owner put
it in that collection.

### One-time setup

Turn on Zotero's local API: **Settings → Advanced → "Allow other
applications on this computer to communicate with Zotero"**. Everything
below then works while Zotero is running, with no key and no account:

```bash
curl http://localhost:23119/api/users/0/collections
```

Writing to Zotero additionally needs an API key from
[zotero.org/settings/keys](https://www.zotero.org/settings/keys), kept in
the `ZOTERO_API_KEY` environment variable. **Never put it in a file in
this repository — this repository is public.**

### Adding a paper, starting from Zotero

1. Add it to `09. Tabular Foundation Models` in Zotero, with the PDF
   attached and its metadata filled in (DOI or arXiv ID at minimum).
2. Copy the item key (right-click → *Export Item…*, or read it from the
   API) and run:

   ```bash
   python scripts/papers/new_paper.py --zotero VGNJPZAJ
   ```

   Title, authors, date and the PDF all come **from the Zotero item** —
   no retyping, and nothing re-derived from the PDF's first page, which
   is where wrong author lists come from. It refuses outright if the item
   is not in the mirrored collection, so the scope rule is enforced by
   the tool rather than by memory. Passing a plain PDF path still works
   and falls back to the arXiv API.
3. Write the prose. `check_docs.py` fails while a scaffold is unfinished.
4. `python scripts/checks/check_zotero_sync.py` — both sides should now
   report the same count and match one-for-one.

### Keeping the two in step

```bash
python scripts/checks/check_zotero_sync.py
```

It compares the collection against `papers/` and reports what diverged:
items on one side only, year/month/title/author mismatches, missing
identifiers, broken attachment links. It is **read-only on both sides**
and it never moves a file or edits a Zotero item.

Two things worth knowing about how it behaves:

- **It matches the collection by name substring**, not by number. The
  numeric prefixes are sort keys and get renumbered; `"Tabular Foundation
  Models"` is stable.
- **It ignores trashed items.** Zotero keeps collection membership until
  the trash is emptied, so without that filter a paper you deliberately
  deleted is reported forever as "missing from `papers/`".

A divergence is a **report, not a repair** — decide which side is wrong
and fix that side by hand. Nothing here deletes a paper to make two
numbers agree.

### Don't read `zotero.sqlite` while Zotero is running

It lags the running application by an unbounded amount: it has been seen
reporting 26 collections while the live API reported 16, because the
deletions were still inside an open transaction. Use the local API. The
SQLite path is a fallback for when Zotero is closed, nothing more.

---

# What is in here, folder by folder

## Root — the documents

Everything a reader consumes directly. The three shared documents are
**project-neutral by contract**: they describe the literature, never any
one project's pipeline. Project-specific notes live in that project's own
`PROJECT_SPECIFIC.md`.

| File | What it is |
|---|---|
| [`SYNTHESIS.md`](SYNTHESIS.md) | **Start here.** The cross-paper synthesis of the TFM paradigm: lineage timeline (PFNs → TabPFN v1/v2/2.5/3 → scaling / adaptation / extensions), the design axes on which the field varies, recurring weaknesses, open frontiers, and a one-card-per-paper appendix. |
| [`SUMMARIES.md`](SUMMARIES.md) | The per-paper tour, chronological: venue, where each paper fits, what it contains, strengths and limitations. Opens with an overview table of all papers. |
| [`REPOSITORIES.md`](REPOSITORIES.md) | The guide to the code dumps: what each one is, why it is kept, and what to grep for when building on it. |
| [`CHANGELOG.md`](CHANGELOG.md) | Human-readable log of library updates, newest first, one dated section per day. Read it before moving a project's pin. |
| [`AGENTS.md`](AGENTS.md) | The contract for AI agents. Which side of the read-only boundary you are on, and the rules for each side. |
| [`PROJECT_SPECIFIC.template.md`](PROJECT_SPECIFIC.template.md) | Template a consuming project copies to `PROJECT_SPECIFIC.md` for its own notes. Gitignored here under that name. |
| [`requirements.txt`](requirements.txt) | Dependencies of the maintenance scripts — and nothing else. There is deliberately no `pyproject.toml`: this is a knowledge base, not an installable package. |

## `papers/` — the literature

PDFs foldered by year and prefixed with the **release month**, so the
filesystem sorts chronologically and cannot disagree with the documents:

```
papers/<year>/<MM>_Author_et_al._Title.pdf
papers/text/<year>/<MM>_Author_et_al._Title.txt
```

`papers/text/` mirrors the PDF tree exactly, one UTF-8 extraction per
paper, so an agent can grep the full text of any paper without PDF
tooling. **Never hand-edit those** — they are generated, and a manual fix
is lost on the next extraction.

Naming: underscores, no spaces or commas; `Author_and_Author` for two
authors, `Author_et_al.` for three or more; names ASCII-folded
(`Müller` → `Muller`).

## `repositories/` — the code dumps

Flat-text snapshots of upstream implementations, one `.txt` per
repository, made with [`gitingest`](https://github.com/cyclotruc/gitingest).
This is what makes "what does the official code actually do" answerable
offline against the exact code a paper shipped.
[`REPOSITORIES.md`](REPOSITORIES.md) describes every one of them; two
deserve mention here because they are exceptions:

- **`TabPFN Wide.txt`** (~366 MB) exceeds GitHub's file limit and is
  **gitignored**. Regenerate it locally with
  `python scripts/dumps/refresh_repositories.py --only "TabPFN Wide.txt"`.
- **`VSC Documentation.txt`** is the one deliberate exception to the
  TFM-only scope, and a load-bearing one — **do not remove it**. It is the
  full KU Leuven / Flemish Supercomputer Centre user documentation. Every
  project consuming this library trains and evaluates on VSC, so SLURM
  scripting, partition and GPU choice, the Lustre/GPFS storage split, and
  credit accounting are shared questions across all of them; having the
  answers greppable offline is worth far more than the file costs. No
  further non-TFM files should be added.

Cite these dumps **by symbol name, never by line number** — a refresh
moves every line by thousands.

## `scripts/` — the maintenance tools

Run everything from the repository root. Set up once (Windows PowerShell;
one command per line, no `&&`):

```bash
python -m venv .venv
```

```bash
.venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
```

### The two you actually run

| File | What it does |
|---|---|
| `scripts/maintain.py` | **The one command.** Runs every stage and prints one consolidated report: fill in missing text extractions, check document consistency, check cited symbols, check against Zotero, check for newer arXiv versions, re-dump the repositories. |
| `scripts/propagate_to_downstream.py` | Pushes this commit out to every project on disk that embeds the library, moving each one's submodule pin. This folder is the ground truth. |

```bash
python scripts/maintain.py                     # full sweep
python scripts/maintain.py --check-only        # change nothing, just report
python scripts/maintain.py --skip repos        # skip the slow dump refresh
python scripts/maintain.py --only zotero       # a single stage
```

`propagate_to_downstream.py` refuses to run when this repository is dirty
or has unpushed commits, because a pin must exist on `origin` or a
collaborator's `git submodule update --init` cannot fetch it. It commits
**only** the submodule path, so unrelated work in a consuming project is
never swept into the bump, and it never pushes downstream unless asked.

```bash
python scripts/propagate_to_downstream.py --dry-run   # show the plan
python scripts/propagate_to_downstream.py             # update + commit locally
python scripts/propagate_to_downstream.py --push      # also push each project
```

### `scripts/papers/` — adding and extracting papers

| File | What it does |
|---|---|
| `new_paper.py` | Files a downloaded PDF under the house naming rule, extracts its text, and inserts **placeholders** for the summary entry, overview row, timeline row, appendix card and changelog line — each in the right chronological slot. It writes no prose: that is the actual work, and an auto-written summary nobody notices is worse than none. |
| `extract_paper_text.py` | PDF → `papers/text/<year>/<same-name>.txt`. Strips control bytes and the line-number gutters that ICLR/NeurIPS templates print, so the result stays greppable. |

```bash
python scripts/papers/new_paper.py ~/Downloads/2607.27546v1.pdf
python scripts/papers/new_paper.py paper.pdf --dry-run   # decide nothing
python scripts/papers/extract_paper_text.py --all        # fill in anything missing
python scripts/papers/extract_paper_text.py --check      # report gaps, write nothing
```

Placeholders read `TODO(new-paper)` and `check_docs.py` fails while any of
them survives, so a half-finished paper cannot be committed by accident.

### `scripts/checks/` — is everything still consistent?

All four are **read-only** and exit non-zero when something is wrong, so
they compose with `maintain.py` and with the pre-commit hook.

| File | What it verifies |
|---|---|
| `check_docs.py` | Every paper has a text extraction, a summary entry, an overview row, a timeline row and an appendix card, with counts agreeing; all four sequences are chronological; every relative link and `#anchor` resolves; the changelog is newest-first with no duplicate or future dates; the shared documents name no consuming project; no unfinished scaffolds remain. |
| `check_symbols.py` | Every code symbol cited in the documents still exists in the dump it is cited against — the check AGENTS.md rule 5 asks for after a refresh. Also flags any `` `dump.txt:1234` `` line-number citation. |
| `check_zotero_sync.py` | The Zotero collection mirroring this library against `papers/`: what is in one place and not the other, year/month/title/author mismatches, missing arXiv IDs or DOIs. Queries a copy of `zotero.sqlite`; never writes to Zotero or moves a file. |
| `check_paper_versions.py` | Asks arXiv whether a newer version exists than the PDF on disk. Never downloads anything — replacing a paper can change its year folder and month prefix, and the summaries may quote version-specific numbers, so it stays a manual decision. |

```bash
python scripts/checks/check_docs.py
python scripts/checks/check_symbols.py --verbose
python scripts/checks/check_zotero_sync.py --collection "Foundation Models"
python scripts/checks/check_paper_versions.py
```

### `scripts/dumps/` — refreshing the code snapshots

| File | What it does |
|---|---|
| `refresh_repositories.py` | Overwrites every `repositories/*.txt` with a fresh `gitingest` dump of its upstream source, under the same filename so existing greps keep resolving. Atomic (temp file + swap), with per-repository include/exclude filters and a shrink guard that refuses a new dump smaller than half the old one. |

```bash
python scripts/dumps/refresh_repositories.py
python scripts/dumps/refresh_repositories.py --only NanoTabPFN
```

Two warnings from this script are **permanent and expected**. The shrink
guard on `On Finetuning Tabular Foundation Models.txt` fails *correctly*:
upstream deleted its entire `exp/` directory including all 342
`report.json` reports, so this dump is now the only surviving copy —
never `--force-shrink` it. And `TabForestPFN.txt` reports SKIP because it
is too large for gitingest's clone timeout; refresh it with the
sparse-clone recipe in the script's docstring.

### `scripts/hooks/` — catching mistakes before they are committed

| File | What it does |
|---|---|
| `pre-commit` | Runs `check_docs.py` on every commit, and `check_symbols.py` when a document or a dump is staged. Offline only — nothing here touches the network. |
| `install.py` | Points git at this folder via `core.hooksPath`, so the hook itself stays under version control instead of hiding in `.git/hooks/`. |

```bash
python scripts/hooks/install.py
python scripts/hooks/install.py --status
python scripts/hooks/install.py --uninstall
```

Bypass a single commit with `git commit --no-verify`.

### `scripts/lib/` — shared internals

| File | What it is |
|---|---|
| `library.py` | Everything more than one script needs to know about the shape of this repository: where the papers and documents live, how to build the house filename from author/month/title, how to read the arXiv banner out of a paper, and how GitHub slugifies a heading. It exists so the scripts cannot drift apart in how they answer those questions — two of them once implemented the slug rule differently, and the wrong one reported twelve valid anchors as broken. |

Not run directly.

---

## Consuming projects

| Project | Mountpoint | Since | Angle |
|---|---|---|---|
| [CreditPFN](https://github.com/andreasgoethals/CreditPFN) | `tfm-library/` | 2026-07 | Real-data **continued pretraining** of TabPFN on a credit corpus (PD + LGD) |
| [CreditICL](https://github.com/andreasgoethals/CreditICL) | `tfm-library/` | 2026-08 | **Pretraining-prior design**: can domain knowledge be encoded in the synthetic prior? Built on TabICL, whose prior generator is open |

The two credit projects attack the same problem from opposite ends of design
axis (a) in [`SYNTHESIS.md`](SYNTHESIS.md): CreditPFN adapts a finished model
with real data, CreditICL changes what the model is pretrained on in the
first place.

This repository is **public**.

---

## Contents

| Path | What you'll find |
|---|---|
| [`SYNTHESIS.md`](SYNTHESIS.md) | The cross-paper synthesis of the field — start here. |
| [`SUMMARIES.md`](SUMMARIES.md) | Per-paper summaries, chronological, with an overview table. |
| [`REPOSITORIES.md`](REPOSITORIES.md) | Guide to the code dumps: what each is and what to grep for. |
| [`CHANGELOG.md`](CHANGELOG.md) | Update log, newest first — read before bumping a pin. |
| [`AGENTS.md`](AGENTS.md) | Rules for AI agents, on either side of the read-only boundary. |
| [`PROJECT_SPECIFIC.template.md`](PROJECT_SPECIFIC.template.md) | Template for a consuming project's own notes. |
| [`requirements.txt`](requirements.txt) | Dependencies of the maintenance scripts. |
| [`papers/`](papers/) | PDFs as `<year>/<MM>_Author_et_al._Title.pdf`. |
| [`papers/text/`](papers/text/) | Full-text extractions, mirroring the PDF tree. |
| [`repositories/`](repositories/) | Flat-text code snapshots of the upstream implementations. |
| [`scripts/maintain.py`](scripts/maintain.py) | Run every check and refresh; one report. |
| [`scripts/propagate_to_downstream.py`](scripts/propagate_to_downstream.py) | Move every downstream project's pin to this commit. |
| [`scripts/papers/`](scripts/papers/) | File a new paper; extract PDF text. |
| [`scripts/checks/`](scripts/checks/) | Document, symbol, Zotero and arXiv-version checks. |
| [`scripts/dumps/`](scripts/dumps/) | Re-snapshot the upstream repositories. |
| [`scripts/hooks/`](scripts/hooks/) | The pre-commit hook and its installer. |
| [`scripts/lib/`](scripts/lib/) | Shared helpers the scripts import. |
