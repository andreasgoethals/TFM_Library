# Project-specific notes — TEMPLATE (do not fill in here)

**This file is the template. Do not write project notes into it.**

Copy it to `PROJECT_SPECIFIC.md` **in your own project's copy of this
folder** and write there:

```bash
# from inside your project, e.g. creditpfn/tfm-library/
cp PROJECT_SPECIFIC.template.md PROJECT_SPECIFIC.md
```

`PROJECT_SPECIFIC.md` is gitignored by this library, so it stays inside
your project's copy, never dirties this repository's git status, and
survives `git submodule update`. It is never committed to the TFM
Library — that is the whole point.

## Why this file exists

The shared documents in this library (`SUMMARIES.md`, `SYNTHESIS.md`,
`REPOSITORIES.md`) are **project-neutral**: they describe the tabular
foundation model literature for every consuming project. Anything that is
true only for *your* project — how a paper's recipe maps onto your
pipeline, which checkpoint you chose, your hyperparameter deviations,
your dataset registry — belongs here instead, next to the literature it
annotates but outside the shared corpus.

## The rule for adding entries

So that every downstream project's notes read the same way:

1. **One `##` section per paper or repository dump**, headed exactly as the
   shared docs head it — `## <Year> — <Author> — <Short title>` for papers,
   `` ## `<Filename>.txt` `` for dumps. This makes entries greppable by the
   same key as `SUMMARIES.md`.
2. **Cite the shared library, never restate it.** Link the paper by its
   path (`papers/<year>/<MM>_<Author>_<Title>.pdf`) and summarise only what
   your project adds. Do not copy the neutral summary in.
3. **Cite code dumps by symbol name, never by line number** — the dumps are
   refreshed periodically and line numbers drift by thousands.
4. **State deviations as deviations**, with the reference value first and
   yours second, plus the reason: *"Garg uses LR 3e-7; we use 1e-5 because
   …"*. Never present a project choice as the paper's recipe.
5. **Date every claim that could go stale** (`— verified 2026-08-04`), since
   this file is not reviewed when the library is refreshed.
6. **Keep it additive.** Never contradict the shared docs silently: if you
   believe a shared document is wrong, fix it upstream in the library
   itself (directly, in its own checkout) rather than overriding it here.

## Skeleton

```markdown
# Project-specific notes — <PROJECT NAME>

Project: <one line on what this project is>
Library pin: <commit SHA this was written against>
Maintainer: <name>

## <Year> — <Author> — <Short title>

**Relevance.** Why this paper matters to this project specifically.

**How we use it.** The concrete mapping onto this project's code/config.

**Where we deviate.** Reference value → our value → why.

**Open questions.** What we still need to check.
```

---

*Template version 1 — part of the TFM Library. If you change the rules
above, change them here so every downstream project inherits the update.*
