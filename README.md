# TFM Library

<a id="update"></a>

## ⚡ Update this library inside a downstream project

Run these **in the consuming project** (CreditPFN, CreditICL, …), never
inside the `tfm-library/` folder. One command per line — **Windows
PowerShell has no `&&`**, so chaining them with `&&` is a parser error:

```bash
git submodule update --remote tfm-library
```

```bash
git add tfm-library
```

```bash
git commit -m "Bump tfm-library pin"
```

<details>
<summary>One-liner, and the other things you might need</summary>

PowerShell one-liner (uses `;` and `if ($?)`, not `&&`):

```bash
git submodule update --remote tfm-library; if ($?) { git add tfm-library; git commit -m "Bump tfm-library pin" }
```

First time in a new project — add the submodule:

```bash
git submodule add https://github.com/andreasgoethals/TFM_Library.git tfm-library
```

After a fresh clone of a consuming project — populate it:

```bash
git submodule update --init
```

Check which commit a project is pinned to (a leading `+` means the working
tree moved but the pin is not committed yet — that is the normal state
between the `update` and the `commit` above):

```bash
git submodule status
```

</details>

**Before you bump:** read [`CHANGELOG.md`](CHANGELOG.md) to see what
changed. **After you bump:** the new pin is only recorded once you commit
it, so don't skip the `git add` + `git commit`. Because the pin is a
commit, an old result stays reproducible against the literature exactly as
it was when that result was produced.

---

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

## Contents

| Path | What you'll find |
|---|---|
| [`SYNTHESIS.md`](SYNTHESIS.md) | **Start here.** The cross-paper synthesis of the TFM paradigm: lineage timeline (PFNs → TabPFN v1/v2/2.5/3 → scaling / adaptation / extensions), the design axes on which the field varies, recurring weaknesses, open frontiers, and a one-card-per-paper appendix. |
| [`SUMMARIES.md`](SUMMARIES.md) | The per-paper tour, chronological: venue, where each paper fits, what it contains, strengths and limitations. |
| [`papers/`](papers/) | The PDFs, foldered by year and prefixed with the release month — `papers/<year>/<MM>_Author_et_al._Title.pdf` — with full-text extractions mirrored under [`papers/text/`](papers/text/) as `papers/text/<year>/<same-name>.txt`. |
| [`REPOSITORIES.md`](REPOSITORIES.md) | What each code dump is, why it's kept, and what to grep for when building on it. |
| [`repositories/`](repositories/) | The flat-text code snapshots themselves (made with `gitingest`). |
| [`PROJECT_SPECIFIC.template.md`](PROJECT_SPECIFIC.template.md) | Template a consuming project copies to `PROJECT_SPECIFIC.md` for its own notes. |
| [`CHANGELOG.md`](CHANGELOG.md) | Human-readable log of library updates — check it before updating a project's pin. |
| [`scripts/`](scripts/) | Maintenance tools — see below. |

The shared documents are **project-neutral by contract**: they describe
the literature, never any one project's pipeline. Project-specific notes
live in that project's own `PROJECT_SPECIFIC.md`.

## How to browse

- *"I want to understand the field"* → read `SYNTHESIS.md` top to bottom.
- *"What did paper X actually do?"* → `SUMMARIES.md`, or grep the full
  text in `papers/text/<year>/`.
- *"How does the official implementation handle Y?"* → `REPOSITORIES.md`
  to pick the right dump, then grep `repositories/*.txt` by symbol name.

## Scripts

Windows PowerShell (one command per line — no `&&`):

```bash
python -m venv .venv
```

```bash
.venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
```

Everything is run from the repository root.

### `scripts/maintain.py` — the one command to run

Runs the whole maintenance sweep and prints a single consolidated report:
re-dumps the upstream repositories, checks every paper has an up-to-date
text extraction, checks whether newer arXiv versions of the papers exist,
and checks this library against Zotero.

```bash
python scripts/maintain.py                  # full sweep
python scripts/maintain.py --check-only     # change nothing, just report
python scripts/maintain.py --skip repos     # skip the slow dump refresh
```

### `scripts/refresh_repositories.py` — re-snapshot the code dumps

Overwrites every `repositories/*.txt` with a fresh `gitingest` dump of
its upstream GitHub source, under the same filename so existing greps
keep resolving. Atomic (temp file + swap) with a shrink guard that
refuses a new dump smaller than 50 % of the old one.

```bash
python scripts/refresh_repositories.py
python scripts/refresh_repositories.py --only NanoTabPFN
python scripts/refresh_repositories.py --force-shrink --only "PFNS.txt"
```

### `scripts/extract_paper_text.py` — PDF → text

Writes `papers/<year>/X.pdf` to `papers/text/<year>/X.txt`, stripping
control bytes so the result stays greppable. Step 2 of adding a paper.

```bash
python scripts/extract_paper_text.py papers/2026/06_Kong_and_Das_Introducing_TabFM.pdf
python scripts/extract_paper_text.py --all      # fill in anything missing
python scripts/extract_paper_text.py --check    # report gaps, write nothing
```

### `scripts/check_zotero_sync.py` — Zotero ↔ library consistency

Compares the Zotero collection that mirrors this library against
`papers/` and reports what diverged: papers in one place but not the
other, year/month/title/author mismatches, and missing arXiv IDs or DOIs.
Read-only on both sides — it queries a copy of `zotero.sqlite` and never
writes to Zotero or moves a file.

```bash
python scripts/check_zotero_sync.py
python scripts/check_zotero_sync.py --collection "Foundation Models"
python scripts/check_zotero_sync.py --json      # machine-readable
```

### `scripts/check_paper_versions.py` — are the PDFs current?

For every paper with an arXiv ID, asks arXiv whether a newer version
exists than the one on disk, and reports the ones worth re-downloading.
Never downloads anything itself.

```bash
python scripts/check_paper_versions.py
```

## Using this library in another project

The library is embedded as a **git submodule** — a pinned commit, so a
project always sees an exact, reproducible snapshot of the literature.
Pinning is the point: a result stays reproducible against the literature
exactly as it was when the result was produced.

**All the commands live in [one place, at the top of this file](#update)**
— adding the submodule, populating it after a clone, bumping the pin, and
checking which commit a project is on. They are deliberately not repeated
here, so they cannot drift apart.

Two things that are easy to get wrong:

- `git submodule update --remote tfm-library` only moves the *working
  tree*. The pin is not recorded until you `git add tfm-library` and
  commit — until then `git submodule status` shows a leading `+`.
- Always run these **in the consuming project**, never inside
  `tfm-library/` itself.

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

## Housekeeping notes

- `repositories/TabPFN Wide.txt` (~366 MB) exceeds GitHub's file limit
  and is gitignored; regenerate locally with
  `python scripts/refresh_repositories.py --only "TabPFN Wide.txt"`.
- **`repositories/VSC Documentation.txt` is the one deliberate exception
  to the TFM-only scope, and it is a load-bearing one — do not remove
  it.** It is the full KU Leuven / Flemish Supercomputer Centre user
  documentation. Every project consuming this library trains and evaluates
  on VSC, so SLURM scripting, partition and GPU choice, the Lustre/GPFS
  storage split, and credit accounting are shared questions across all of
  them; having the answers greppable offline is worth far more than the
  file costs. No further non-TFM files should be added.
- This repository is **public**.

## Consuming projects

| Project | Mountpoint | Since | Angle |
|---|---|---|---|
| [CreditPFN](https://github.com/andreasgoethals/CreditPFN) | `tfm-library/` | 2026-07 | Real-data **continued pretraining** of TabPFN on a credit corpus (PD + LGD) |
| [CreditICL](https://github.com/andreasgoethals/CreditICL) | `tfm-library/` | 2026-08 | **Pretraining-prior design**: can domain knowledge be encoded in the synthetic prior? Built on TabICL, whose prior generator is open |

The two credit projects attack the same problem from opposite ends of design
axis (a) in [`SYNTHESIS.md`](SYNTHESIS.md): CreditPFN adapts a finished model
with real data, CreditICL changes what the model is pretrained on in the
first place.
