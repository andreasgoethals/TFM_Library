# Repositories — context corpus

This folder is a **read-only** reference corpus. Every `.txt` file
here is a flat dump of an upstream repository or webpage, kept
locally so downstream code can be grepped against canonical
implementations without round-tripping to the internet. **Never edit
these files.** If a snapshot is stale, replace the whole file with a
fresh dump using the same filename, so existing greps in the
codebase keep working.

Listed alphabetically below. Where a repo corresponds to a paper in
[`papers/`](papers/), the paper is linked. Where the file is a
fresh dump of a public GitHub repo, the upstream URL is linked.

## Overview table

Line counts are as of the 2026-08-04 refresh, except VSC Documentation,
recounted on 2026-10-12. They drift on every refresh; treat them as rough sizes.

| File | Lines | GitHub | Paper | What it gives us |
|------|-------|--------|-------|------------------|
| `CausalPFN.txt` | 6,636 | [vdblm/CausalPFN](https://github.com/vdblm/CausalPFN) | [Balazadeh Meresht 2025](papers/2025/12_Balazadeh_Meresht_et_al._CausalPFN_Amortized_Causal_Effect_Estimation_via_In_Context_Learning.pdf) | Amortised causal-effect ICL: the `CausalEstimator` API and the transformer head. Inference/estimation only — no prior generator. Filtered to code (upstream carries ~175 MB of benchmark data). |
| `Huggingface TabPFN.txt` | 552 | [tabpfn_2_5](https://huggingface.co/Prior-Labs/tabpfn_2_5), [tabpfn_2_6](https://huggingface.co/Prior-Labs/tabpfn_2_6) | [Hollmann 2025](papers/2025/01_Hollmann_et_al._Accurate_predictions_on_small_data_with_a_tabular_foundation_model.pdf), [Grinsztajn 2026](papers/2026/02_Grinsztajn_et_al._TabPFN_2.5_Advancing_the_State_of_the_Art_in_Tabular_Foundation_Models.pdf) | Primary citation source for checkpoint provenance (synthetic vs. real-finetuned, layer counts, intended limits, licence). |
| `LoCalPFN.txt` | 1,714 | [layer6ai-labs/LoCalPFN](https://github.com/layer6ai-labs/LoCalPFN) | [Thomas 2024](papers/2024/12_Thomas_et_al._Retrieval_Fine_Tuning_for_In_Context_Tabular_Models.pdf) | The retrieval + fine-tuning recipe in ~8 files: `methods/ftknn.py` (LoCalPFN) and `methods/pfknn.py` (TabPFN-kNN). The only k-NN-context implementation in this folder. **No LICENSE upstream** — read, don't redistribute. |
| `NanoTabICL.txt` | 665 | [soda-inria/nanotabicl](https://github.com/soda-inria/nanotabicl) | [Qu 2026](papers/2026/02_Qu_et_al._TabICLv2_A_better_faster_scalable_and_open_tabular_foundation_model.pdf) | TabICLv2's minimal release: `model.py` + `prior.py` only. The shortest readable path to a complete TFM — architecture and prior in two files. |
| `NanoTabPFN.txt` | 1,103 | [automl/nanoTabPFN](https://github.com/automl/nanoTabPFN) | [Pfefferle 2025](papers/2025/12_Pfefferle_et_al._nanoTabPFN_A_Lightweight_and_Educational_Reimplementation_of_TabPFN.pdf) | Cleanest end-to-end reference of a PFN training loop; the structural template to copy. |
| `On Finetuning Tabular Foundation Models.txt` | 90,496 | [yandex-research/tabpfn-finetuning](https://github.com/yandex-research/tabpfn-finetuning) | [Rubachev 2025](papers/2025/06_Rubachev_et_al._On_Finetuning_Tabular_Foundation_Models_1.pdf) | Yandex research repo for TabPFNv2 full/PEFT finetuning: experiment configs, reports, LoRA utilities, vendored TabPFN changes, and practical LR/early-stopping recipes. |
| `PFNS.txt` | 29,093 | [SamuelGabriel/PFNs](https://github.com/SamuelGabriel/PFNs) | [Müller 2021](papers/2021/12_Muller_et_al._Transformers_Can_Do_Bayesian_Inference.pdf) | Implementations of every encoder step that runs *inside* every TabPFN forward pass (NaN handling, normalisation, …). Delimits what an upstream preprocessing step should *not* duplicate. |
| `PFNs4BO.txt` | 7,455 | [automl/PFNs4BO](https://github.com/automl/PFNs4BO) | [Müller 2023](papers/2023/05_Muller_et_al._PFNs4BO_In_Context_Learning_for_Bayesian_Optimization.pdf) | PFN-as-Bayesian-optimisation surrogate. Tangential to tabular prediction; relevant only for PFN-as-BO-surrogate work. |
| `TabForestPFN.txt` | 27,827 | [FelixdenBreejen/TabForestPFN](https://github.com/FelixdenBreejen/TabForestPFN) | [den Breejen 2024](papers/2024/10_Breejen_et_al._Fine_tuned_In_Context_Learning_Transformers_are_Excellent_Tabular_Data_Classifiers.pdf) | The **forest/tree prior generators** (`synthetic_generator_forest.py`, `_tabpfn.py`, `_cuts.py`, `_mix.py`) plus pretrain/finetune trainers. Dead upstream since 2024-05; filtered to code from a 1.36 GB repo. |
| `TabICL.txt` | 32,794 | [soda-inria/tabicl](https://github.com/soda-inria/tabicl) | [Qu 2025](papers/2025/05_Qu_et_al._TabICL_A_Tabular_Foundation_Model_for_In_Context_Learning_on_Large_Data.pdf), [Qu 2026](papers/2026/02_Qu_et_al._TabICLv2_A_better_faster_scalable_and_open_tabular_foundation_model.pdf) | **The most valuable dump here after `TabPFN .txt`.** The only *fully open* competitive TFM: complete synthetic prior generator (`prior/`, `prior/graph_lib/`), pretraining loop with the **Muon optimiser** (`train/_muon.py`), the 3-stage curriculum scripts for v1 **and** v2, finetuning, forecasting and SHAP extensions. |
| `TabDPT.txt` | 3,174 | [layer6ai-labs/TabDPT-inference](https://github.com/layer6ai-labs/TabDPT-inference) | [Ma 2026](papers/2026/01_Ma_et_al._TabDPT_Scaling_Tabular_Foundation_Models_on_Real_Data.pdf) | Inference code for the real-data-only competitor to TabPFN. Comparison baseline. |
| `TabPFN .txt` | 84,092 | [PriorLabs/tabPFN](https://github.com/PriorLabs/tabPFN) | [Hollmann 2023](papers/2023/09_Hollmann_et_al._TabPFN_A_Transformer_That_Solves_Small_Tabular_Classification_Problems_in_a_Second.pdf), [Hollmann 2025](papers/2025/01_Hollmann_et_al._Accurate_predictions_on_small_data_with_a_tabular_foundation_model.pdf), [Grinsztajn 2026](papers/2026/02_Grinsztajn_et_al._TabPFN_2.5_Advancing_the_State_of_the_Art_in_Tabular_Foundation_Models.pdf) | Canonical sklearn-style API, all checkpoint metadata, the multi-table finetuning machinery (`get_preprocessed_dataset_chunks`, `DatasetCollectionWithPreprocessing`, `FinetunedTabPFN*`). Primary code reference for training/finetuning work. |
| `TabPFN Client.txt` | 13,282 | [PriorLabs/tabpfn-client](https://github.com/PriorLabs/tabpfn-client) | — | Hosted-API HTTP client. Irrelevant to self-hosted training; only for benchmarking the hosted API. |
| `TabPFN Docs.txt` | 7,797 | _GitHub source removed_ — refresh manually from [docs.priorlabs.ai/overview](https://docs.priorlabs.ai/overview) | — | The docs.priorlabs.ai source. Documents *intent* of every config knob; faster to grep than the implementation in `TabPFN .txt`. |
| `TabPFN Drift-Resilient.txt` | 138,551 | [automl/Drift-Resilient_TabPFN](https://github.com/automl/Drift-Resilient_TabPFN) | [Helli 2024](papers/2024/11_Helli_et_al._Drift_Resilient_TabPFN_In_Context_Learning_Temporal_Distribution_Shifts_on_Tabular_Data_1.pdf) | The reference implementation for drift-aware training-time augmentation. |
| `TabPFN Extensions.txt` | 21,845 | [PriorLabs/tabpfn-extensions](https://github.com/PriorLabs/tabpfn-extensions) | — | `AutoTabPFN` post-hoc ensembling, RF-PFN, embeddings, HPO. Source of evaluation baselines. |
| `TabPFN V2 Finetuning.txt` | 4,835 | [PriorLabs/TabPFN/examples](https://github.com/PriorLabs/TabPFN/tree/main/examples) | [Rubachev 2025](papers/2025/06_Rubachev_et_al._On_Finetuning_Tabular_Foundation_Models_1.pdf) | The `finetune_classifier.py` and `finetune_regressor.py` reference scripts built on the official `FinetunedTabPFN*` wrappers. |
| `TabSTAR.txt` | 8,743 | [alanarazi7/TabSTAR](https://github.com/alanarazi7/TabSTAR) | [Arazi 2025](papers/2025/12_Arazi_et_al._TabSTAR_A_Tabular_Foundation_Model_for_Tabular_Data_with_Text_Fields.pdf) | Text-aware TFM, end to end: `pretraining/` (`pretrainer.py`, `unfreezing.py`), `training/` (`lora.py`, `checkpoint_averaging.py`), `preprocessing/verbalize.py`, and baseline adapters for tabpfnv2/tabicl/tabdpt/carte. Default branch is `master`; 401 metadata stubs excluded. |
| `TabPFN Wide.txt` | 2,279,103 | [not-a-feature/TabPFN-Wide](https://github.com/not-a-feature/TabPFN-Wide) | [Kolberg 2026](papers/2026/03_Kolberg_et_al._TabPFN_Wide_Continued_Pre_Training_for_Extreme_Feature_Counts.pdf) | Continued-pretraining for extreme-feature-count regimes via a feature-widening prior (it argues *against* feature reduction, and uses FeatureAgglomeration only as a baseline). Gitignored (~366 MB); regenerate locally. |
| `TabTune.txt` | 168,086 | [Lexsi-Labs/TabTune](https://github.com/Lexsi-Labs/TabTune) | [Tanna 2025](papers/2025/12_Tanna_et_al._TabTune_A_Unified_Library_for_Inference_and_Fine_Tuning_Tabular_Foundation_Models.pdf) | Unified sklearn-style wrapper around the **non-TabPFN** tabular foundation models (TabICL, OrionMSP/Bix, Mitra, ContextTab, TabDPT, LimiX) plus TabPFNv2.6 native FT, ensembling, distillation, and a `TabularLeaderboard`. A convenient source of non-TabPFN eval baselines; it does **not** natively support Real-TabPFN-style multi-dataset continued pretraining. |
| `TransformersCanDoBayesianInference.txt` | 12,325 | [automl/TransformersCanDoBayesianInference](https://github.com/automl/TransformersCanDoBayesianInference) | [Müller 2021](papers/2021/12_Muller_et_al._Transformers_Can_Do_Bayesian_Inference.pdf) | The original (unmaintained) code release of the 2021 PFN paper. Historical; useful for explaining what a PFN is. |
| `VSC Documentation.txt` | 39,613 | [hpcleuven/VscDocumentation](https://github.com/hpcleuven/VscDocumentation) | — | VSC user documentation: **wICE P100/V100/A100/H100 and Mindwell B200**, Slurm selection and limits, Lustre/GPFS storage, software modules, credits and OnDemand. See the [current usage guide](#vsc-usage). |

## Check `TabTune.txt` before adding any new TFM dump

`TabTune.txt` does far more coverage work than its one-line index entry
suggests: TabTune **vendors complete copies** of most other tabular
foundation models, so their implementations are already greppable here.
Verified file counts under `tabtune/models/` in the current dump:

| Vendored model | Files | | Vendored model | Files |
|---|---|---|---|---|
| `tabpfnv3/` | 117 | | `orion_msp/` | 30 |
| `tabpfnv26/` | 101 | | `orionmsp_v15/` | 29 |
| `tabpfn/` | 40 | | `regression/` | 16 |
| `tabiclv2/` | 36 | | `contexttab/` | 14 |
| `orion_bix/` | 33 | | `tabdpt/` | 7 |
| `tabicl/` | 30 | | `limix/` | 6 |
| | | | `mitra/` | 5 |

Two consequences. First, **a separate dump of Orion-MSP, Orion-BiX or
ConTextTab would be redundant** — spot-checking `orion_msp/attention.py`
against upstream showed byte-identical content after line-ending
normalisation, and the vendored `orionmsp_v15/` is *newer* than the
standalone repository. Adding them would only create duplicate grep hits
with no way to tell which copy you are reading. Second, when you *do* need
one of these implementations, grep `TabTune.txt` for
`FILE: tabtune/models/<model>/` rather than assuming it is absent.

The exception is provenance: TabTune is a third-party wrapper, so if you
need to cite or diff a *canonical* upstream implementation, go to that
project's own repository. Note that ConTextTab's has been renamed —
`SAP-samples/contexttab` now redirects to
[`SAP-samples/sap-rpt-1-oss`](https://github.com/SAP-samples/sap-rpt-1-oss)
(same checkpoint, rebranded `sap-rpt-1-oss`), so the URL printed in the
paper is dead as a literal string.

## Layout

This file lives at the repo root; the dumps live in
[`repositories/`](repositories/) — 22 flat `.txt` files, one per
upstream source, named exactly as in the table above (`TabPFN .txt`
keeps its intentional trailing space). Line counts are in the table;
the only file not tracked by git is `TabPFN Wide.txt` (~366 MB,
gitignored — regenerate with `python scripts/dumps/refresh_repositories.py`).

### The one deliberate exception to the TFM-only scope

`VSC Documentation.txt` is **not** tabular-foundation-model literature —
it is the full KU Leuven / Flemish Supercomputer Centre user
documentation. It is here on purpose and **must not be removed**: every
project that consumes this library runs its training and evaluation on
VSC, so the same SLURM, storage-tier and credit questions come up in all
of them, and answering them offline from a grep is worth far more than
the file costs. Treat it as shared infrastructure knowledge that happens
to live beside the literature. It is the *only* non-TFM file in this
folder, and no further exceptions should be added without the owner
saying so.

---

## `Huggingface TabPFN.txt`

**Upstream:** HuggingFace model cards for
[`Prior-Labs/tabpfn_2_5`](https://huggingface.co/Prior-Labs/tabpfn_2_5)
and
[`Prior-Labs/tabpfn_2_6`](https://huggingface.co/Prior-Labs/tabpfn_2_6).

**Related papers:**
[2025 — Hollmann et al. — Accurate predictions on small data with a tabular foundation model](papers/2025/01_Hollmann_et_al._Accurate_predictions_on_small_data_with_a_tabular_foundation_model.pdf),
[2026 — Grinsztajn et al. — TabPFN-2.5](papers/2026/02_Grinsztajn_et_al._TabPFN_2.5_Advancing_the_State_of_the_Art_in_Tabular_Foundation_Models.pdf).

**What it is.** Concatenation of the public HuggingFace model-card
READMEs for `Prior-Labs/tabpfn_2_5` and `Prior-Labs/tabpfn_2_6` (the
source URLs are written out as comments inside the file). Each card
is included twice in the dump (with and without `# Source:` headers);
the content is identical and any grep against the file will still
hit.

**Why it matters here.** The model cards are the *primary published
source* for which checkpoint is real-finetuned vs. synthetic-only,
the layer counts (v2.5 = 18–24, v2.6 = 24), the licence terms, and
the citation. Consuming projects that maintain a checkpoint
inventory should cross-check every fact against this file.

**Contents in detail.**

- **YAML front matter** — licence (`tabpfn-2.5-license-v1.1` /
  `tabpfn-2.6-license-v1.0`), pipeline tag, gated-access fields,
  thematic tags including `finance`.
- **Model overview** — TabPFN-2.x = transformer-based foundation
  model, in-context learning, single forward pass.
- **Architecture** — v2.5: "TabPFNv2-like alternating attention with
  18-24 layers"; v2.6: "TabPFNv2-like alternating attention with 24
  layers".
- **Training data and priors** —
  - v2.5: "TabPFN-2.5: trained purely on synthetic tabular tasks /
    Real-TabPFN-2.5: continued pre-training on real-world datasets
    (for details please see Appendix C.1 of the model tech report)."
  - v2.6: "TabPFN-2.6 is trained purely on synthetic tabular tasks."
    (No real-finetuned variant. Decisive evidence that v2.6 default
    *is* the synthetic-only base.)
- **The complete v2.5 checkpoint catalogue** with one-line
  descriptions per checkpoint, identical to the catalogue inside
  `TabPFN .txt` (grep `tabpfn-v2.5-classifier-v2.5_large-features-L`).
  The 🌍 emoji marks the real-finetuned variants. v2.6 has only the
  `_default` checkpoints listed.
- **Intended use / limitations** — ≤ 50,000 samples and ≤ 2,000
  features; not for unstructured data.
- **Licensing** — research-only with an enterprise option for
  commercial use.

**When to grep this file:** when you need a primary citation for any
checkpoint provenance claim (v2.5/v2.6, real vs synthetic, intended
sample/feature limits). For pipeline implementation, prefer
`TabPFN .txt` (more detailed) or `TabPFN Docs.txt` (more recent
prose).

---

## `NanoTabPFN.txt`

**Upstream:** [github.com/automl/nanoTabPFN](https://github.com/automl/nanoTabPFN).

**Related paper:**
[2025 — Pfefferle et al. — nanoTabPFN: A Lightweight and Educational Reimplementation of TabPFN](papers/2025/12_Pfefferle_et_al._nanoTabPFN_A_Lightweight_and_Educational_Reimplementation_of_TabPFN.pdf).

**What it is.** A minimal reference implementation of TabPFN — the
"how-it-works-in-under-1000-lines" educational version, trimmed of
the production package's ergonomics (sklearn API surface, ensembles,
distributed training, autocast handling, multiple checkpoints) so
that the *core training and inference loop* is visible at a glance.

**Why it is the highest-signal file in this folder:** Real-TabPFN's
source is not public, so the closest available thing to a
continued-pretraining loop readable end-to-end in a few hundred lines
lives here.

**Contents in detail:**

- **Data loading and preprocessing.** Defines
  `get_feature_preprocessor(X)` which fits a `ColumnTransformer` that
  separates numerical from categorical columns by checking, for each
  column, whether `pd.to_numeric(errors='coerce').notna().sum()`
  equals the non-NaN count. Numerical columns get coerced to numeric
  arrays; categoricals get an `OrdinalEncoder(handle_unknown=
  'use_encoded_value', unknown_value=np.nan)`. Constant columns (≤ 1
  unique non-NaN value) are dropped. This is the *minimum* feature
  preprocessing TabPFN inputs need, and it defines the
  minimum any downstream preprocessing step must match.
- **`get_openml_datasets(...)`** — illustrates the OpenML download
  path for evaluation (TabArena task IDs hardcoded), with stratified
  subsampling via `train_test_split(stratify=y)`.
- **Model definition (`NanoTabPFNModel`).** The full TabPFN-style
  alternating-attention transformer in pure PyTorch: alternating
  attention "between samples" and "between features" within the same
  layer, plus a target embedding head.
  `forward(src, train_test_split_index)` shows exactly how the
  context-vs-query split is consumed: the model sees one tensor of
  shape `(B, N, F)` and an integer index that says "rows
  [0:split_idx) are context with labels, rows [split_idx:] are query
  with masked labels".
- **Training loop (grep `AdamWScheduleFree`).** The pretraining loop
  in 70 lines: `schedulefree.AdamWScheduleFree`, learning rate `4e-3`,
  cross-entropy loss reshaped to `(B*N_query, n_classes)`,
  gradient-norm clip at `1.0`, periodic eval. This is the structural
  reference for a from-scratch PFN training loop.
- **`PriorDumpDataLoader`.** Loads pre-baked
  synthetic prior datasets from an HDF5 file. Fields:
  `X (B, N_max, F_max)`, `y (B, N_max)`, `num_features`,
  `num_datapoints`, `single_eval_pos` (= train/test split index),
  `max_num_classes`. Padding-aware: each batch slices to the
  per-batch max feature count and max sequence length. **Reference
  format only** — a pipeline that reads real tables directly can
  assemble the same `(X_context, y_context, X_query, y_query)` quadruple
  on the fly instead of pre-baking a prior dump.

**When to grep this file:** any time you need the "what does the
training loop actually look like" answer — model `forward`
semantics, loss shape, gradient handling, optimizer setup, batch
layout.

---

## `On Finetuning Tabular Foundation Models.txt`

**Upstream:** [github.com/yandex-research/tabpfn-finetuning](https://github.com/yandex-research/tabpfn-finetuning).

**Related paper:**
[2025 - Rubachev et al. - On Finetuning Tabular Foundation Models](papers/2025/06_Rubachev_et_al._On_Finetuning_Tabular_Foundation_Models_1.pdf).

> **This dump is now an archive — do not `--force-shrink` it.** As of the
> 2026-08-04 refresh, upstream has **deleted its entire `exp/` directory**:
> 636 files, including all **342 `report.json` experiment reports**. The
> `lib/` code (29 files) is unchanged and nothing new was added. A fresh
> dump would therefore be 37 % of the size and would silently destroy the
> hyperparameter evidence the "Verified config facts" table below is built
> from — data that no longer exists anywhere upstream. The shrink guard in
> `scripts/dumps/refresh_repositories.py` currently blocks this, reporting it as
> a FAIL on every run; that FAIL is **correct and should be left alone**.

**What it is.** A Yandex Research code dump for the Rubachev et al.
TabPFNv2 finetuning study. It is much larger than the Prior Labs
example scripts because it includes experiment grids, tuned configs,
result reports, RTDL-style data/model utilities, LoRA utilities, and
a vendored/modified TabPFN implementation.

**Why it matters here.** The paper's main practical conclusion is
that full finetuning is the strongest and simplest TabPFNv2
adaptation baseline: it converges quickly, tends to beat PEFT
variants, and can be run on datasets up to roughly 50K rows on an
80GB GPU. The mechanism result: finetuning improves the alignment between test-row query
representations and in-context training-row key representations, so
attention weights better track target similarity. This repo is the best public source for the LR grid, patience,
prediction length, and A100 memory assumptions behind single-dataset
gradient adaptation.

**Two facts that frame comparisons against it:** (1) the 342 archived
``report.json`` grid runs inspected below are full-FT runs, but the
**paper also reports LoRA and other partial/PEFT ablations**. Do not turn
the contents of that one result directory into a claim that the paper did
not evaluate LoRA. (2) each run adapts to one target table. Multi-dataset
corpus continued pretraining is Garg et al.'s Real-TabPFN setting, not
Rubachev's experimental design.

**Contents in detail:**

- **`FILE: README.md`** - unreadable in the current dump: gitingest
  hit a `charmap` codec error, so only the error line remains. Read
  project-overview / setup claims from the paper PDF
  (arXiv `2506.08982`), not from this dump.
- **`FILE: pyproject.toml`** - Python pinned to
  `==3.11.11`, with CUDA 12.4 extras and dependencies including
  PyTorch, CatBoost, XGBoost, Optuna, RTDL utilities, and `loralib`.
- **`exp/full-finetune/*/*.toml`** - reproducible experiment grids.
  The adult config calls
  `bin.tabpfnv2_finetune.main`, uses `n_trials = 10`, brute-force
  learning rates from about `5e-6` to `5e-4`, `batch_size = 1`,
  `epoch_size = 10`, `seq_len_pred = 1024`, and
  `finetune_mode = "full"`.
- **`report.json` / `summary.json` blocks** - practical run reports:
  A100-SXM4-80GB hardware, roughly 7.2M or 11.1M trainable
  parameters depending on the config, early-stopped best steps, and
  zero-shot vs. finetuned metrics.
- **`lib/data.py`** - expects arrays such as `X_num.npy`,
  `X_bin.npy`, `X_cat.npy`, `Y.npy`, and
  `split-default/{train,val,test}_idx.npy`. Useful when designing
  adapters between a custom cache format and RTDL-style loaders.
- **`lib/deep.py`** - RTDL numerical embedding utilities such as
  piecewise-linear embeddings, one-hot helpers, optimization helpers,
  and parameter-count utilities.
- **`FILE: lib/tabpfn/lora_utils.py`** - LoRA injection
  helpers for TabPFN internals, including replacements for MHA,
  linear layers, and embeddings. The local reference for benchmarking LoRA against full continued
  pretraining.
- **`FILE: lib/tabpfn/preprocessing.py`** - vendored
  TabPFN preprocessing configs (`none`, `numeric`, `onehot`,
  `ordinal`, `ordinal_shuffled`, etc.) and the package-level feature
  preprocessing choices.

**Verified config facts (aggregated across all 342 `report.json` runs,
2026-06-23).** These are the *reference* values a downstream project
should calibrate against, not adopt blindly:

| Knob | Reference value (all 342 runs) |
|------|--------------------------------|
| optimizer | AdamW |
| **weight_decay** | **0.0** |
| LR | tuned 5e-6…5e-4, median ~3.9e-5 |
| LR schedule | **none (constant)** |
| **L2-SP / anchor** | **not used** |
| batch_size | 1 |
| epoch policy | `n_epochs=-1` + early stop (patience 16) |
| ensemble/step | clf 2 / **reg 8** (official wrappers) |
| loss | CE (clf) / bar-dist NLL (reg) |
The main optimization lesson from this repository is that Rubachev uses
`weight_decay=0.0`; stacking decay-to-origin on an L2-SP anchor would be a
separate, untested regularization choice. **This says nothing about Garg's
AdamW weight decay, which the Real-TabPFN paper does not report.** Garg
does explicitly use L2-SP λ=0.003, warmup→cosine, and LR 3e-7. Keep the
two papers separate. (The README body is unrecoverable from this dump — a
`charmap` codec error replaced it — so prose claims must be read from the
PDF, not this `.txt`.)

**Important caveat.** The dump references
`bin.tabpfnv2_finetune.main`, but this `.txt` snapshot contains no
`FILE: bin/...` sections. Use it as a high-signal reference for
configs, results, LoRA/vendored TabPFN changes, and paper-grounded
hyperparameters; do not assume the local dump is a complete runnable
clone.

**When to grep this file:** when choosing single-dataset finetuning
hyperparameters, comparing full finetuning vs. LoRA/prefix variants,
or checking how Rubachev et al. structure their data arrays, tuning
reports, and TabPFNv2 internals.

---

## `PFNS.txt`

**Upstream:** [github.com/SamuelGabriel/PFNs](https://github.com/SamuelGabriel/PFNs)
(formerly `automl/PFNs`; the old slug no longer resolves directly).

**Related papers:**
[2021 — Müller et al. — Transformers Can Do Bayesian Inference](papers/2021/12_Muller_et_al._Transformers_Can_Do_Bayesian_Inference.pdf)
(the foundational PFN framework that this code implements).

**What it is.** The full Prior-Labs `PFNs` repo — the underlying
"Prior-fitted Network" framework that TabPFN is built on top of.
Contains the canonical implementations of the *internal* encoder
steps that run inside every TabPFN forward pass.

**Why it matters here:** it delimits what an upstream preprocessing step
should *not* duplicate. The model already handles a lot of preprocessing
internally; a pipeline that does it a second time either wastes work
or (worse) double-transforms features in ways that drift the
distribution off the model's training prior.

**Contents in detail:**

- **Encoder-step composition.** Shows how the
  standard TabPFN-2.x model assembles its input encoder as a
  sequence:
  - `NanHandlingEncoderStep` — handles missing values (emits an
    explicit indicator and replaces NaN with a learned default).
  - `LinearInputEncoderStep` — linear projection of features into
    embedding space.
  - `VariableNumFeaturesEncoderStep` — pads/shuffles the feature
    dimension so a model trained on F-max features can ingest any
    F ≤ F-max.
  - `ConstantNormalizationInputEncoderStep` and
    `InputNormalizationEncoderStep` — per-column normalisation
    fitted on the *context* rows only and applied to query rows.
- **Each encoder step's full implementation** (grep the class
  names):
  - `LinearInputEncoderStep`.
  - `ConstantNormalizationInputEncoderStep`.
  - `NanHandlingEncoderStep`: replaces `NaN` with
    `nan_indicator`, `+inf` with `inf_indicator`, `-inf` with
    `neg_inf_indicator`, then concatenates a binary "was-this-NaN"
    flag along the feature dimension. Confirms that replacing ±inf with NaN
    upstream is consistent with the model's own handling.
  - `VariableNumFeaturesEncoderStep`.
  - `InputNormalizationEncoderStep` — per-column mean/std
    computed on the context split only.
- **Standalone preprocessing transforms** (grep `PowerTransformer`) that
  run *before* the model, as ensemble members at inference time:
  `PowerTransformer(method='yeo-johnson')` /
  `PowerTransformer(method='box-cox')` /
  `QuantileTransformer(output_distribution='normal')` /
  `RobustScaler(unit_variance=True)`. **These are inference-time
  ensemble preprocessing, not training-time preprocessing.**

**When to grep this file:** to confirm whether something is the
model's internal job or the pipeline's job; to look up what the
encoder steps actually do to NaNs / infs / constants; to see the
canonical ensemble of preprocessing options at inference.

---

## `PFNs4BO.txt`

**Upstream:** Same repo as PFNs (BO branch /
[github.com/automl/PFNs4BO](https://github.com/automl/PFNs4BO)).

**Related paper:**
[2023 — Müller et al. — PFNs4BO: In-Context Learning for Bayesian Optimization](papers/2023/05_Muller_et_al._PFNs4BO_In_Context_Learning_for_Bayesian_Optimization.pdf).

**What it is.** PFNs adapted to Bayesian optimisation. Implements an
acquisition function on top of a PFN posterior — useful for
hyperparameter search but unrelated to credit-risk pretraining.

**When to grep this file:** only if you later want to use a PFN as
a surrogate model for tuning your own continued-pretraining
hyperparameters. No relevant preprocessing or training-loop
machinery beyond what's already in `PFNS.txt`.

---

## `TabDPT.txt`

**Upstream:** [github.com/layer6ai-labs/TabDPT-inference](https://github.com/layer6ai-labs/TabDPT-inference)
(inference code; full training code is in the sibling repo
[`layer6ai-labs/TabDPT-training`](https://github.com/layer6ai-labs/TabDPT-training)).

**Related paper:**
[2026 — Ma et al. — TabDPT: Scaling Tabular Foundation Models on Real Data](papers/2026/01_Ma_et_al._TabDPT_Scaling_Tabular_Foundation_Models_on_Real_Data.pdf).

**What it is.** TabDPT is the *real-data-only* counterpart to
TabPFN: a transformer trained on real tables sampled from OpenML
via retrieval-augmented self-supervision, with no synthetic
prior. The dump in this folder is the *inference* repo — load
weights from HuggingFace and predict on a new dataset via a
sklearn-style API.

**Why it matters.** TabDPT and TabPFN bracket the
synthetic-vs-real spectrum from opposite ends. Real-TabPFN (and
and any domain specialisation after it) sits in the middle. Having
TabDPT locally makes it usable as an *inference baseline* alongside
TabPFN-2.6, TabICL and the published Real-TabPFN-2.5 weights.

**Contents in detail.**

* `src/tabdpt/classifier.py`, `regressor.py`, `estimator.py`,
  `model.py`, `utils.py` — the inference path.
* `tabdpt_datasets/openml.py` — OpenML dataset loaders that they
  used at training time and ship for reproducibility.
* `tabdpt_datasets/data_splits/{cls,reg}_datasets.csv` — the
  exact CSV manifest of which OpenML datasets they trained on.
  Useful for *contamination checking* — any dataset on this list
  must NOT appear in a held-out evaluation set, or the comparison is
  unfair to TabDPT's competitors.
* `examples/cls_example.py`, `reg_example.py` — minimum working
  example. They sat in `tests/` until upstream put a real pytest
  suite there (`test_cls.py`, `test_reg.py`, `test_estimator.py`,
  `test_inference.py`), so older notes point at the wrong path.

**When to grep this file:** when implementing the TabDPT
TabDPT baseline, or when checking that your held-out
splits don't overlap with TabDPT's training corpus.

---

## `TabPFN .txt`

**Upstream:** [github.com/PriorLabs/tabPFN](https://github.com/PriorLabs/tabPFN)
(the main `tabpfn` Python package).

**Related papers:**
[2023 — Hollmann et al. — TabPFN](papers/2023/09_Hollmann_et_al._TabPFN_A_Transformer_That_Solves_Small_Tabular_Classification_Problems_in_a_Second.pdf),
[2025 — Hollmann et al. — Accurate predictions on small data](papers/2025/01_Hollmann_et_al._Accurate_predictions_on_small_data_with_a_tabular_foundation_model.pdf),
[2026 — Grinsztajn et al. — TabPFN-2.5](papers/2026/02_Grinsztajn_et_al._TabPFN_2.5_Advancing_the_State_of_the_Art_in_Tabular_Foundation_Models.pdf).

**What it is.** The user-facing sklearn-style API
(`TabPFNClassifier`, `TabPFNRegressor`), the checkpoint-loading
infrastructure, the inference-time ensembling, and the documented
list of every released `.ckpt` and what it's good for. Plus the
finetuning wrappers (`FinetunedTabPFNClassifier` /
`FinetunedTabPFNRegressor`) and the multi-table machinery
(`get_preprocessed_dataset_chunks`,
`DatasetCollectionWithPreprocessing`, `fit_from_preprocessed`) that a
multi-dataset training loop composes on.

**Why it matters:** this is the single source of truth for
checkpoint provenance (which files are synthetic-only, which are
real-finetuned), the public configuration knobs
(`PreprocessorConfig`, `ModelInterfaceConfig`), and the supported
input shapes / dtypes / NaN handling at the API boundary.

**Contents in detail:**

- **README block** listing the *default* v2.5
  classifier and regressor checkpoint URLs.
- **The complete TabPFN-2.5 checkpoint catalogue with one-line
  descriptions** (grep `tabpfn-v2.5-classifier-v2.5_large-features-L`):
  which is real-finetuned (🌍 emoji),
  which is synthetic, which specialises for "large features"
  (`large-features-L` up to 500 features, `large-features-XL` up
  to 1000), which for "large samples" (>30K), which for low-skew
  regression targets, etc. **This is what a consuming project's
  checkpoint inventory is
  built from — when in doubt, this section of `TabPFN .txt` is
  ground truth.**
- **Programmatic checkpoint name registry** used
  inside the package to validate `model_path` arguments.
- **`tabpfn-v2-` (v2.0) checkpoint registry** for
  the older v2.0 model family.
- **`DatasetCollectionWithPreprocessing`**, the
  `torch.utils.data.Dataset` subclass that lazily preprocesses each
  dataset on `__getitem__`, returning a `ClassifierBatch` or
  `RegressorBatch`.
- **`shuffle_and_chunk_data`**, TabPFN's own
  per-dataset row sub-sampler. Stratified for multiclass,
  non-stratified for regression. Reference behaviour for any
  per-epoch subsample → context/query split → ordinal-encode step.
- **`get_preprocessed_dataset_chunks`**, the
  helper that accepts a *list* of datasets and produces a
  `DatasetCollectionWithPreprocessing` ready for a multi-table
  training loop.
- **`FinetunedTabPFNBase`,
  `FinetunedTabPFNClassifier`, `FinetunedTabPFNRegressor`** — the
  official sklearn-compatible finetuning wrappers.
- **`PreprocessorConfig` definitions** — exposes
  `name='none' | 'safepower' | 'quantile_uni_coarse' | 'quantile_uni'
  | 'robust_scaler' | …`. These are inference-time ensemble names.
- **`save_tabpfn_model` utility** — the reverse
  direction: how to dump a model object back to a `.ckpt`. PR #930
  (see the package CHANGELOG inside the dump) fixed it to set
  `architecture_name="tabpfn_v3"` for v3 configs and to persist
  `inference_config_` — the exact gap any custom checkpoint writer has
  to close (see the checkpoint-format note below).
- **Architecture registry** (`architectures/tabpfn_v2_6.py`,
  `tabpfn_v3.py`; `inference_config.py`) — the `architecture_name`
  strings the loader recognises and the `InferenceConfig` schema
  (pydantic, `extra="forbid"`).

**The 4-key checkpoint contract.**
A TabPFN checkpoint is a single `torch.save` dict with exactly four
keys: `state_dict`, `config` (asdict of the pydantic
`ArchitectureConfig`), `architecture_name`, and `inference_config`
(asdict of `InferenceConfig`). Valid `architecture_name` values are
`tabpfn_v2`, `tabpfn_v2_5`, `tabpfn_v2_6`, `tabpfn_v3` (a missing key
defaults to `tabpfn_v2`; the legacy `"base"` string remaps to
`tabpfn_v2_5`). Any writer must emit all four keys. Two traps: deriving
`architecture_name` via the *private* upstream symbol
`_resolve_architecture_name` is brittle (better to raise than to
mislabel an unknown architecture as `"base"`), and loading such a
checkpoint needs `weights_only=False`, because PyTorch ≥ 2.6 rejects the
embedded pydantic config objects by default.

**v2.6-vs-v3 criterion handling (regressors).** The two generations
store the bar-distribution borders in different places — up to v2.6 as
`criterion.*` state saved beside the model, from v3 as a
`regression_borders` buffer on the model itself. The loader no longer
branches on the architecture at all: it always separates `criterion.*`
out of the model state, then `_resolve_regression_borders` takes the
checkpoint's saved borders if they are there, falls back to the buffer,
and raises if neither is. Writing `criterion.*` for regressors
unconditionally therefore round-trips for both architectures — and is
what `save_tabpfn_model` itself does.

Older releases decided the same thing by sniffing `model.forward` for a
`test_targets_MB` parameter. Upstream has removed it, but **`TabTune.txt`
still vendors a TabPFN copy that carries both the `test_targets_MB`
sniff and the vestigial parameter it tests for** — so a checkpoint
written for current upstream and a checkpoint written for TabTune's
bundled loader are not interchangeable on this point.

**When to grep this file:** checkpoint names, the 4-key checkpoint
schema, public API surface, inference-time preprocessing names,
validation / error messages the package raises, the multi-table
finetuning machinery.

---

## `TabPFN Client.txt`

**Upstream:** [github.com/PriorLabs/tabpfn-client](https://github.com/PriorLabs/tabpfn-client).

**Related paper:** none.

**What it is.** The HTTP client for Prior Labs' hosted inference
API.

**When to grep this file:** only if you're benchmarking against the
hosted API. Not relevant to a self-hosted training workflow.

---

## `TabPFN Docs.txt`

**Upstream:** [docs.priorlabs.ai/overview](https://docs.priorlabs.ai/overview).
Prior Labs **no longer publishes** the docs GitHub source, so this file
cannot be refreshed by ``scripts/dumps/refresh_repositories.py``. It's
listed in ``SKIP_NON_GIT`` and must be refreshed by hand (copy the
relevant pages from the live docs site) when the on-disk snapshot
goes stale.

**Related papers:** indirectly all of the TabPFN papers — the docs
sit on top of the package described above.

**What it is.** Flat dump of the TabPFN documentation repository —
the Markdown sources that the docs.priorlabs.ai site is built from.
~7,800 lines covering every documented capability, hyperparameter,
integration, and fine-tuning recipe.

**Why it's the highest-signal recent addition:** it contains the
*official* documentation of TabPFN's preprocessing knobs, the
fine-tuning wrappers shipped inside the package, and the design
intent behind every configurable parameter. For Stage 1–4 design,
this is the most authoritative non-code reference.

**Contents in detail (grep the `.mdx` filenames):**

- **`overview.mdx`** — what TabPFN is and what
  its capabilities are.
- **`models.mdx`** — version comparison
  table.
- **`improving-performance/preprocessing.mdx`** —
  **the most important section for designing an
  upstream preprocessing step.** Documents:
  - `PREPROCESS_TRANSFORMS`: ensemble preprocessing names
    (`"quantile_uni"`, `"squashing_scaler_default"`, `"safepower"`,
    `"quantile_uni_coarse"`, `"kdi"`, `"robust"`, `"none"`).
  - `categorical_name`: encoding options.
  - `max_features_per_estimator`: default `500`.
  - `REGRESSION_Y_PREPROCESS_TRANSFORMS`: target transforms for
    regression (`"none"`, `"safepower"`, `"quantile_norm"`,
    `"quantile_uni"`, `"1_plus_log"`).
  - `OUTLIER_REMOVAL_STD`: **default `"auto"` which resolves to
    `12.0` for classification and `None` for regression** — see the
    "Outlier handling" section below.
  - `POLYNOMIAL_FEATURES`, `FINGERPRINT_FEATURE`,
    `SUBSAMPLE_SAMPLES`. None of these belong in a
    training-time data config — they are inference-time levers.
- **`capabilities/fine-tuning.mdx`** —
  documentation of the official `FinetunedTabPFNClassifier` and
  `FinetunedTabPFNRegressor` wrappers. Important caveat: "The
  fine-tuning process decouples the preprocessing
  pipeline to generate transformed tensors that mirror the
  preprocessing configurations used during inference, ensuring the
  model optimizes on the exact same data variations it encounters
  when making predictions."
- **`improving-performance/feature-engineering.mdx`,
  `feature-selection.mdx`, `model-parameters.mdx`** — softmax
  temperature, balanced-probability handling, imbalance handling.
- **`extensions/*.mdx`** — `hpo`, `many-class`, `post-hoc-ensembles`,
  `rf-pfn`. Reference for the evaluation protocol later.
- **`api-reference/*.mdx`** — hosted-API only.
- **`integrations/*.mdx`** — Databricks, Azure Foundry, SageMaker,
  MLflow, n8n.
- **`use-cases/*.mdx`** — including `finance.mdx`.

**When to grep this file:** for the *intent* and *contract* of any
documented TabPFN configuration option. Faster than grepping
`TabPFN .txt` (which is the implementation) when you just need
"what does this parameter do".

---

## `TabPFN Drift-Resilient.txt`

**Upstream:** [github.com/automl/Drift-Resilient_TabPFN](https://github.com/automl/Drift-Resilient_TabPFN).

**Related paper:**
[2024 — Helli et al. — Drift-Resilient TabPFN](papers/2024/11_Helli_et_al._Drift_Resilient_TabPFN_In_Context_Learning_Temporal_Distribution_Shifts_on_Tabular_Data_1.pdf).

**What it is.** A research repo that fine-tunes / specialises TabPFN
for distribution-shift robustness — explicitly modelling "training
distribution drifts at inference time" rather than assuming i.i.d.

**Why it matters.** Any domain whose data is defined by regime shift
(finance, epidemiology, demand) may benefit from the drift-aware
training-time augmentations implemented here rather than assuming
i.i.d. context and query rows.

**Contents in detail:** drift-aware loss formulations,
distribution-shift simulation as a training-time augmentation,
extra evaluation protocols (eval on artificially shifted test
sets).

**When to grep this file:** when designing training-time
augmentations or evaluation under regime shift.

---

## `TabPFN Extensions.txt`

**Upstream:** [github.com/PriorLabs/tabpfn-extensions](https://github.com/PriorLabs/tabpfn-extensions).

**Related paper:** none directly; references the `AutoTabPFN`
ensemble idea documented across multiple TabPFN papers.

**What it is.** `tabpfn-extensions` — official add-on package
(post-hoc ensembling, RF-PFN hybrids, embeddings, hyperparameter
search via OpenAutoML, a "many-class classifier" wrapper for >10
target classes, a fingerprint-feature tool, etc.).

**Why it's relevant:** the standard reporting package compares plain
TabPFN vs. `AutoTabPFN` (post-hoc ensemble).
A fair comparison usually reports against both, so the ensemble
mechanics matter.

**Contents in detail:** post-hoc ensemble definition (uses
AutoGluon under the hood), RF-PFN tree-based hybrid (`rf_pfn`
extension — good baseline since classical PD/LGD modelling
traditionally uses gradient-boosted trees and random forests).

**When to grep this file:** when designing the evaluation protocol
or building strong baselines.

---

## `TabPFN V2 Finetuning.txt`

**Upstream:** [github.com/PriorLabs/TabPFN/tree/main/examples](https://github.com/PriorLabs/TabPFN/tree/main/examples)
(the `finetune_classifier.py` and `finetune_regressor.py`
example scripts).

**Related paper:**
[2025 — Rubachev et al. — On Finetuning Tabular Foundation Models](papers/2025/06_Rubachev_et_al._On_Finetuning_Tabular_Foundation_Models_1.pdf).

**What it is.** The official `examples/` folder of the main TabPFN
package. Its two finetuning scripts are the closest public analog of
Real-TabPFN's continued pretraining, but with one key difference:
this is dataset-specific finetuning ("finetune TabPFN-v2 to *one*
downstream dataset") rather than continued pretraining on a whole
corpus.

*(History note: earlier snapshots of this file carried hand-rolled
training-loop examples — `preprocess_dummy_data`,
`save_path_to_fine_tuned_model`, manual `loss.backward()` — that
upstream has since deleted. Since the 2026 refresh the examples
drive the official `FinetunedTabPFN*` wrappers instead, and the
actual forward/backward loop lives inside the package: grep
`tabpfn.finetuning` in `TabPFN .txt`.)*

**Why it's a critical reference:** it shows the supported way to
load a v2 checkpoint, run gradient adaptation over it, and evaluate
the result — the unit-of-work that corpus-level continued
pretraining sweeps over many datasets.

**Official wrapper defaults (verified against the constants at the
top of `finetune_classifier.py` / `finetune_regressor.py` in the
dump).** These are the upstream `FinetunedTabPFN*` settings a
finetuning grid should be calibrated against:

| Wrapper | epochs | lr | `n_estimators_finetune` | ctx+query samples |
|---|---|---|---|---|
| `FinetunedTabPFNClassifier` | 30 | `2e-5` | 2 | — |
| `FinetunedTabPFNRegressor` | 30 | `1e-5` | 8 | `n_finetune_ctx_plus_query_samples = 20_000` |

Note the asymmetry: the official regressor uses **8** estimators during
finetuning against the classifier's 2. A project that copies the
classifier setting onto a regression track is silently departing from
the reference.

**Contents in detail (grep the `FILE: examples/...` headers):**

- **`finetune_classifier.py`** — `FinetunedTabPFNClassifier` on the
  Higgs OpenML dataset (100k-sample subset): constants
  (`NUM_EPOCHS = 30`, `LEARNING_RATE = 2e-5`,
  `NUM_ESTIMATORS_FINETUNE = 2`), base-vs-finetuned ROC/log-loss
  comparison, multi-GPU via `torchrun`, and
  `ignore_pretraining_limits=True` with
  `inference_config={"SUBSAMPLE_SAMPLES": 50_000}`.
- **`finetune_regressor.py`** — the regression twin
  (`LEARNING_RATE = 1e-5`, `NUM_ESTIMATORS_FINETUNE = 8`,
  `N_FINETUNE_CTX_PLUS_QUERY_SAMPLES = 20_000`).
- **`save_and_load_model.py`** — the supported persistence path for
  fitted estimators. Note the package loader's *inference*
  checkpoint is the 4-key `torch.save` dict (`state_dict`, `config`,
  `architecture_name`, `inference_config`) — see the
  `TabPFN .txt` section for that contract.
- **`notebooks/TabPFN_Demo_Local.ipynb`** —
  `OrdinalEncoder(handle_unknown='use_encoded_value',
  unknown_value=-1)`: the categorical encoding contract.
- Plus benchmarking (`benchmarking_tabpfn.py`, vs XGBoost on German
  Credit Data), KV-cache fast prediction, tuning, SageMaker /
  Databricks-MLflow integration examples.

**When to grep this file:** for the canonical, supported
"load checkpoint → finetune → evaluate → save" sequence for *real*
TabPFN-2 weights, not the toy model. For the loop internals
themselves, grep `tabpfn/finetuning/` inside `TabPFN .txt`.

---

## `TabPFN Wide.txt`

**Upstream:** [github.com/not-a-feature/TabPFN-Wide](https://github.com/not-a-feature/TabPFN-Wide)
(the canonical repo for the TabPFN-Wide paper, Kolberg et al. 2026).

**Related paper:**
[2026 — Kolberg et al. — TabPFN-Wide](papers/2026/03_Kolberg_et_al._TabPFN_Wide_Continued_Pre_Training_for_Extreme_Feature_Counts.pdf).

**What it is.** TabPFN-Wide — modifications for high-dimensional
inputs, e.g. multi-omics or wide credit-bureau datasets with
hundreds to thousands of columns.

**Why it matters:** any corpus with >100-column tables needs a story for
wide data. TabPFN-Wide's answer is to *widen the synthetic prior* so the
model natively handles hundreds-to-thousands of columns, rather than
reducing features; it uses `FeatureAgglomeration` only as a **baseline
it compares against**,
not as its method. Unsupervised feature *selection* (keeping real
columns) is an independent, pragmatic alternative; read this repo for
how the widening approach works, **not** as a source for feature
reduction.

**Contents in detail:**

- **Multiple `load_state_dict` patterns** for
  loading both the standard TabPFN checkpoint and Wide-modified
  checkpoints.
- **The `load_checkpoint(self)` method** showing how
  the Wide trainer loads a *training-state* checkpoint
  (state_dict + optimizer state + scheduler state). Template for
  resumable training in cluster jobs.
- **`FeatureAgglomeration` usage** (as a *baseline*). Two
  variants: `FeatureAgglomeration(n_clusters=n_features)` (default
  Euclidean+Ward) and `FeatureAgglomeration(
  n_clusters=n_features, metric='precomputed', linkage='complete')`.

**When to grep this file:** dimensionality-reduction strategies,
checkpoint resumption, anything wide/high-feature.

---

## `TabTune.txt`

**Upstream:** [github.com/Lexsi-Labs/TabTune](https://github.com/Lexsi-Labs/TabTune).

**Related paper:**
[2025 — Tanna et al. — TabTune: A Unified Library for Inference and
Fine-Tuning Tabular Foundation Models](papers/2025/12_Tanna_et_al._TabTune_A_Unified_Library_for_Inference_and_Fine_Tuning_Tabular_Foundation_Models.pdf)
([arXiv:2511.02802](https://arxiv.org/abs/2511.02802)).

**What it is.** A unified, sklearn-style wrapper that exposes ~10
recent tabular foundation models — TabPFN-v2 / -v2.6, TabICL,
TabICLv2, OrionMSP v1.0 / v1.5, OrionBix, Mitra, ContextTab, TabDPT,
LimiX — under a single `TabularPipeline.fit() / .predict() /
.evaluate() / .save() / .load()` API. Built on three components:
`DataProcessor` (model-aware preprocessing), `TuningManager`
(per-model training strategy), `TabularPipeline` (end-to-end driver),
plus a `TabularLeaderboard` for head-to-head comparison. Each model
gets four tuning strategies: zero-shot inference, episodic
meta-learning FT (the *standard* way to finetune ICL models),
supervised FT, and PEFT/LoRA. Recent additions: 6-strategy ensembling
(`TabularEnsemble`), distillation (`TabDistiller` — TFM → MLP /
LightGBM / XGBoost / CatBoost), and TabPFNv2.6 native FT (the
official Prior Labs `FinetunedTabPFN*` API, surfaced through TabTune's
unified pipeline).

**Scope note.** TabTune's pipelines are *per-dataset*: one
`TabularPipeline.fit()` call corresponds to one dataset. It therefore
does not natively express Real-TabPFN-style continued pretraining,
which iterates one model over a *corpus* of tables. Its natural use is
the evaluation side — a single library giving TabICL, OrionMSP, Mitra,
ContextTab, TabDPT and LimiX baselines — at the cost of pulling in
every model's runtime as a dependency.

**When to grep this file:** when designing a new eval baseline that
would otherwise need its own model-specific wrapper. The
`TuningManager` and `DataProcessor` source code in particular shows
how each non-TabPFN model expects its inputs preprocessed
(integer-encoded categoricals for TabPFN vs. text-tokenised columns
for ContextTab vs. column-attention masks for TabICL, …).

---

## `TransformersCanDoBayesianInference.txt`

**Upstream:** [github.com/automl/TransformersCanDoBayesianInference](https://github.com/automl/TransformersCanDoBayesianInference)
— the original, explicitly unmaintained code release of the 2021 PFN
paper (its README points to `SamuelGabriel/PFNs`, i.e. `PFNS.txt`,
as the maintained successor).

**Related paper:**
[2021 — Müller et al. — Transformers Can Do Bayesian Inference](papers/2021/12_Muller_et_al._Transformers_Can_Do_Bayesian_Inference.pdf).

**What it is.** Code accompanying Müller et al. 2021 — the original
PFN paper, as the authors shipped it: `train.py`, `transformer.py`,
`bar_distribution.py`, `encoders.py`, the prior implementations
under `priors/`, and the paper's experiment notebooks. Mostly
historical context for understanding what a
"Prior-fitted Network" *is*: a transformer trained to perform
posterior inference for a particular Bayesian prior, by sampling
synthetic datasets from that prior and training the model to map
context → query predictions.

*(History note: before 2026-07-17 the refresh script pointed this
file at the maintained `SamuelGabriel/PFNs` repo, which made it a
byte-identical duplicate of `PFNS.txt` and silently lost the
paper-era snapshot. It now tracks the original repo again.)*

**When to grep this file:** when you need to write a paragraph
explaining PFNs in your thesis / a defence / a report. Not relevant
for pipeline implementation.

---

<a id="vsc-usage"></a>

## `VSC Documentation.txt`

**Upstream:** [hpcleuven/VscDocumentation](https://github.com/hpcleuven/VscDocumentation),
the source of the [VSC documentation site](https://docs.vscentrum.be).
**Related paper:** none; this is the library's deliberate infrastructure exception.

**What it is.** The supplied snapshot contains **39,613 lines**, including the current
wICE/Mindwell guides and archived Genius hardware pages. It covers account access,
SSH/MFA, Slurm, storage, software, credits, OnDemand and publication acknowledgments.
The guidance below was reconciled with that snapshot and the live KU Leuven guides on
**2026-10-12**. Source paths below are searchable `FILE:` headings in the dump; cite those
paths or symbols rather than dump line numbers. Other VSC sites and Tier-1 systems have
their own rules: do not transfer their driver versions, quotas or partitions to Leuven.

**Cluster selection after the October maintenance.** P100 and V100 partitions now belong
to **wICE**, and Genius is archived. A downstream launcher targeting those GPUs should
use `--clusters=wice`, retaining the appropriate `gpu_p100` or `gpu_v100` partition.
Mindwell B200 jobs still use `--clusters=mindwell --partition=gpu_b200`.
The default for Slurm commands on login nodes is now wICE; on Mindwell compute nodes
it is Mindwell. **Explicit `-M/--clusters` remains mandatory for job submission**, even
though a default exists for commands such as `squeue`. Always select the cluster when
monitoring or cancelling a specific job; `squeue -M all` and `sacct -M all` can span both.
Source: `source/leuven/slurm_specifics.rst`, `leuven_cluster_choice`, and the
[live Slurm guide](https://docs.vscentrum.be/leuven/slurm_specifics.html).

These read-only commands illustrate the distinction from a login shell:

```bash
squeue -M wice -u "$USER"
squeue -M mindwell -u "$USER"
squeue -M all -u "$USER"
sinfo -M wice
sinfo -M mindwell
```

**GPU resources and time limits.** The following describes configured capacity, not
current availability. Source: `source/leuven/wice_quick_start.rst`,
`source/leuven/mindwell_quick_start.rst`, their `tier2_hardware/` pages, and
`cpu_resource_limits_in_gpu_jobs` in `source/leuven/slurm_specifics.rst`.

| Slurm cluster | GPU partition | Regular nodes × GPUs | VRAM per GPU | CPU cores / CPU memory per GPU (maximum) | Maximum walltime |
|---|---|---|---|---|---|
| `wice` | `gpu_p100` | 13 × 4 | 16 GiB | 9 / 45,000 MiB | 72 h; `gpu_p100_long`: 168 h |
| `wice` | `gpu_v100` | 2 × 8 | 32 GiB | 4 / 84,000 MiB | 72 h; `gpu_v100_long`: 168 h |
| `wice` | `gpu_a100` (alias `gpu`) | 4 × 4 | 80 GiB | 18 / 126,000 MiB | 72 h |
| `wice` | `gpu_h100` | 5 × 4 | 80 GiB | 16 / 187,200 MiB | 72 h |
| `mindwell` | `gpu_b200` | 3 × 8 | 192 GiB | 24 / 194,400 MiB | 72 h |

The wICE hardware page counts **14 P100 nodes in total**, including debug capacity;
the quick-start table lists 13 for the regular partitions. `gpu_p100_debug` and
`gpu_a100_debug` allow up to **1 hour**. Do not infer A100, H100 or B200 `*_long`
partitions from the P100/V100 exceptions. Request actual GPU resources (for example,
`--gpus-per-node=1`) as well as a GPU partition, with proportionate CPU/memory requests.
GPU nodes can host other jobs, but allocated cores and GPUs are exclusive to each job.
For multi-node scaling, check interconnects: the wICE H100 nodes have Ethernet rather
than the high-performance interconnect available to most other wICE nodes; Mindwell
nodes use InfiniBand NDR.

CPU work can run on either cluster. wICE `batch`/`batch_icelake` uses 72-core nodes;
`batch_sapphirerapids` uses 96 cores. Mindwell defaults to `batch_graniterapids` with
192 cores. Their documented `*_long` variants allow 168 h. The free `interactive`
partitions allow up to 16 h and eight cores; wICE offers one **1/7 A100 instance**,
whereas Mindwell offers one **RTX 5000 Ada GPU**. An interactive A100 instance is not
a full 80 GiB device. See the quick-start guides for memory and resource requests.

**Software and job environment.** Use `#!/bin/bash -l` and load application modules in
the jobscript so the compute node selects its own architecture stack. Submission-shell
variables are not propagated by default; use Slurm's documented `--export` behaviour
when a workflow needs extra variables. P100/Skylake, V100/Cascadelake, A100/IceLake,
and H100/Zen4 remain different hardware targets after migration. Check
`VSC_ARCH_LOCAL`, `VSC_ARCH_SUFFIX` and `MODULEPATH` for native builds. Mindwell's
central modules start with toolchains **2024a for CPUs / 2025a for GPUs**. Pure Python
code need not have a separate environment for every CPU, but compiled extensions and
GPU kernels must support the target hardware. Sources: `source/leuven/wice_advanced_guide.rst`,
`source/leuven/tier2_hardware/mindwell_hardware.rst`, and
`source/compute/software/using_software/cluster_modules.rst`.

The announcement reports an updated **system GPU driver**, not an automatic replacement
of a project's Python packages or CUDA runtime. Newer NVIDIA drivers generally support
older CUDA runtimes, subject to supported hardware and compatible application libraries
([NVIDIA compatibility guide](https://docs.nvidia.com/deploy/cuda-compatibility/why-cuda-compatibility.html)).
After maintenance, a downstream project should check `nvidia-smi` and run a small GPU
smoke test **inside an allocated GPU job** using its existing environment. Record the
driver, GPU and framework/runtime versions before a larger run. No exact Leuven driver
version is established by the announcement; the Tier-1 driver number elsewhere in this
dump is not evidence for it.

**Storage and transfers.** Source: `source/leuven/tier2_hardware/kuleuven_storage.rst`
and `source/leuven/tier2_hardware/parallel_filesystems.rst`.

- `$VSC_HOME` (default **3 GiB**) and `$VSC_DATA` (**75 GiB**) are backed-up NFS with
  snapshots, accessible across VSC. They are intended for persistent files with modest
  I/O; home-institute policy can change quotas.
- `$VSC_SCRATCH` (default **500 GiB**, no backup) resolves to **Lustre on wICE** and
  **GPFS on Mindwell**. Intensive compute I/O must use the filesystem associated with
  the executing cluster; violations can cause cancellation by administrators.
- Group storage follows the same split: staging directories beneath
  `$VSC_PROJECT_LUSTRE1` for wICE, project1 directories beneath `$VSC_PROJECT_GPFS1`
  for Mindwell. Do not assume access from another cluster means equivalent throughput
  or that a project directory provides a backup; confirm the allocation's storage policy.
- Explicit `$VSC_SCRATCH_LUSTRE1` / `$VSC_SCRATCH_GPFS1` paths support transfers.
  **GPFS is not reachable from the wICE P100/V100 nodes.** Stage required GPFS inputs
  through a wICE login node or an appropriate transfer job before using these GPUs.
  The recommended transfer jobs can use either cluster's `interactive` partition;
  keep login-node copies to a few minutes. The guide recommends transfer jobs rather
  than Globus for volumes above 1 TB.
- Scratch files not accessed for **30 days** are removed. When initially staging old
  files, use `cp` without `-a`: moves and timestamp-preserving transfers can leave them
  eligible for early deletion. The parallel-filesystem guide also illustrates `rsync -a`
  for stage-in/out; that is not an exemption from the cleanup policy.
- `$VSC_SCRATCH_NODE` is local temporary storage, removed when the job ends: default
  200 GiB on P100/V100 nodes and 600 GiB on other wICE/Mindwell nodes. Copy required
  outputs to durable storage before exit. Avoid millions of small files on shared
  parallel filesystems, and plan either one cluster per work package or explicit
  stage-in/stage-out and verified transfers between stages.

**Credits and scheduling.** Source: `source/leuven/credits.rst` and
`source/leuven/slurm_accounting.rst`. Mindwell now accepts regular credit accounts;
the `lp_mindwell_pilot` name still present in some examples is not a guarantee of free
production access. Choose an account you can charge with `--account`, inspect its
balance with `sam-balance`, and estimate a submission with `sam-quote sbatch ...`.
The documented GPU weights in credits per GPU-minute are **P100 41.667, V100 59.583,
A100 141.667, H100 569.444, B200 437.500**. These are only the GPU component:
**(CPU weight × effective allocated cores + GPU weight × GPU count) × runtime minutes**
determines GPU-job cost. A large memory request can allocate and bill more CPU cores
than requested explicitly. Read live `TRESBillingWeights` with
`scontrol show partitions --clusters=wice` (or `mindwell`) before budgeting; the
quoted maximum cost assumes the job uses its entire time limit.

The site-specific Slurm guide distinguishes submission limits from running-resource
limits through partition QoS (`normal`, `long`, `interactive`, `debug`). Inspect live
limits with `sacctmgr show qos debug,interactive,long,normal`; a pending resource-limit
reason is not evidence that the submitted job was lost. Cross-cluster `afterok`
dependencies remain **unverified by this library**: coordinate dependent stages only
after confirming upstream completion and the required data transfer, or first validate
the intended cross-cluster dependency behaviour with VSC support.

**OnDemand release and operational status.** The owner's **1 October 2026** notice from
[KU Leuven OnDemand](https://ondemand.hpc.kuleuven.be/) reports that Genius has been
removed, the dashboard displays available credits, Help can submit support tickets,
and the Module Browser searches centrally installed modules. R/Python/Julia/Perl/Rust
extensions are not indexed there yet. An absent extension search result therefore does
not establish that a package is unavailable. Use `module spider <name>` / module help
and inspect the selected runtime or environment; a browser entry also does not install
or activate software in a job. Public portal coverage is documented in
`source/compute/portal/index.rst` and the [web portal guide](https://docs.vscentrum.be/compute/portal/index.html).

**Dated status, checked 2026-10-12:** the [Leuven incident page](https://status.vscentrum.be/tier2_leuven.html#incident_0013)
(last updated 2026-10-11) still lists the **two V100 nodes as unavailable**, with no end
time. Its updates returned A100/interactive nodes on 2 October, H100/B200/Mindwell
interactive nodes later that day, and P100 nodes on 6 October. Recheck that page and
Slurm before choosing hardware; this dated observation is not a permanent partition rule.

**When to grep this file:** writing or reviewing job scripts, selecting hardware,
checking environment compatibility, accounting for compute or storage, and looking up
access, transfer and acknowledgment procedures. Cluster usage is a downstream project's
choice; this shared guide does not prescribe a specific project's CPU/GPU split.

---

## `TabPFN V2 Finetuning.txt` ↔ `On Finetuning Tabular Foundation Models.txt` ↔ `NanoTabPFN.txt` ↔ `TabPFN Wide.txt` — how they relate

| | NanoTabPFN | Wide | V2 Finetuning | On Finetuning |
|---|---|---|---|---|
| Model definition | toy reimpl | full + wide modifications | uses real package | vendored/modified package |
| Loads real `.ckpt`? | no (trains from scratch) | yes | yes | yes |
| Has training loop? | yes (synthetic prior) | yes (sweep over real datasets) | yes (single-dataset finetune) | configs/results for single-dataset finetune |
| Closest to corpus-CPT | training-loop structure | dataset-sweep structure | checkpoint mechanics | hyperparameters + PEFT/full-finetune evidence |

A corpus continued-pretraining implementation typically needs all four:
V2-Finetuning's checkpoint loading, On-Finetuning's hyperparameter
evidence, Wide's resumable training-state pattern, and NanoTabPFN's
training-loop scaffolding.

---

### Outlier handling: what TabPFN actually does (verified)

This is important enough to factor out into its own subsection,
because it determines how an upstream preprocessing step should treat
extreme values. The implementation lives in `TabPFN .txt` — grep the
function `remove_outliers` and the public knob `OUTLIER_REMOVAL_STD`.

```python
# TabPFN .txt, grep _REGRESSION_DEFAULT_OUTLIER_REMOVAL_STD
_REGRESSION_DEFAULT_OUTLIER_REMOVAL_STD: float | None = None
_CLASSIFICATION_DEFAULT_OUTLIER_REMOVAL_STD: float = 12.0
```

```python
# TabPFN .txt, grep remove_outliers (paraphrased)
def remove_outliers(X, n_sigma=4, normalize_positions=-1, ...):
    # 1. Compute per-column mean/std using ONLY the context split.
    # 2. Mark cells outside [mean ± n_sigma·std] as NaN.
    # 3. Re-compute mean/std from the now-cleaned data.
    # 4. Re-derive the [lower, upper] bounds from those robust stats.
    # 5. Apply a SOFT log-squash (not hard clip):
    X = max(-log(1+|X|) + lower, X)
    X = min( log(1+|X|) + upper, X)
```

**Three takeaways for an upstream pipeline:**

1. **TabPFN's z-score normalization is *not* a substitute for
   outlier handling.** Z-scoring is sensitive to the very outliers
   it's trying to normalise — a single `1e9` value pins the mean
   and std to `~1e9` and crushes everything else to ~0. That's why
   the package itself ships an outlier removal step *before* /
   *alongside* the normalization step.
2. **The default threshold is `12σ` for classification, and outlier
   removal is *disabled* by default for regression.** A `[0.5%,
   99.5%]` quantile cut would be ~ `±2.6σ` for Gaussians, which is
   far more aggressive than what TabPFN does at inference and would
   create a train-vs-inference distribution mismatch.
3. **`OUTLIER_REMOVAL_STD` is an *inference-time* parameter** — when
   training feeds tensors directly to the underlying torch model, this
   step is not applied automatically. An upstream step should therefore
   normalise only `±inf → NaN` and delegate true outlier handling to the
   package's own machinery at inference time.

### Fine-tuning wrappers: official package machinery

Independent of the data pipeline, `TabPFN Docs.txt`
(`capabilities/fine-tuning.mdx`) and `TabPFN .txt` (grep
`FinetunedTabPFNClassifier`) document `FinetunedTabPFNClassifier` /
`FinetunedTabPFNRegressor`. These are the supported entry points
for gradient-based adaptation of TabPFN. Corpus-level continued
pretraining has to go one level lower than these wrappers, calling the
underlying `PerFeatureTransformer.forward(x, y, ...)` directly with
batches assembled on the fly, so the loop can iterate over a *corpus*
of datasets rather than fine-tune one dataset at a time. Per-epoch
subsample size then has to be capped per architecture, in the same
spirit as the upstream `FinetunedTabPFNClassifier` per-fit row cap.

---

## Refreshing this folder

- For the upstream code repos (`TabPFN .txt`, `PFNS.txt`, etc.), run
  `python scripts/dumps/refresh_repositories.py` (see its module docstring
  for `--only` / `--force-shrink` / `--timeout`). It re-dumps every
  mapped file via gitingest and **overwrites the existing file under
  the same filename** — atomically, with a shrink guard — so existing
  greps keep resolving. After a refresh, spot-check that the symbol
  names cited in this file and in `SUMMARIES.md` still exist, and log
  the refresh in `CHANGELOG.md` (AGENTS.md rule 5).
- `TabPFN Docs.txt` and `Huggingface TabPFN.txt` have no git
  upstream (`SKIP_NON_GIT` in the script): refresh them manually
  from docs.priorlabs.ai and the Hugging Face model cards.

---

## `TabICL.txt`

**Upstream:** [github.com/soda-inria/tabicl](https://github.com/soda-inria/tabicl).

**Related papers:**
[2025 — Qu et al. — TabICL](papers/2025/05_Qu_et_al._TabICL_A_Tabular_Foundation_Model_for_In_Context_Learning_on_Large_Data.pdf),
[2026 — Qu et al. — TabICLv2](papers/2026/02_Qu_et_al._TabICLv2_A_better_faster_scalable_and_open_tabular_foundation_model.pdf).

**What it is — and why it is the highest-value non-TabPFN dump here.**
Every other frontier TFM in this collection is closed where it matters
most: Prior Labs has never released v2's prior-generation code, and the
v2.5/v3 priors are undisclosed. TabICL is the exception. This repository
ships the **entire pipeline** for a model that beats Real-TabPFN-2.5 on
TabArena: the synthetic data engine, the pretraining loop, the curriculum,
the optimiser, and the inference path. If you need to know how a
competitive tabular foundation model is actually *built* rather than
merely used, this is the only complete answer in the folder.

**Contents in detail (127 files; grep the `FILE:` headers).**

- **`src/tabicl/prior/` — the synthetic prior generator.** The part no
  TabPFN release includes. `_mlp_scm.py` and `_tree_scm.py` are the two
  SCM families (the MLP/tree mixture the papers describe), `_graph_scm.py`
  the graph-structured variant, `_hp_sampling.py` the hyperparameter
  sampler that decides each synthetic dataset's shape, `_activations.py`
  the function library, `_reg2cls.py` the regression→classification
  discretisation, and `_dataset.py` / `_genload.py` the generation and
  loading path. `__main__.py` means the generator is runnable standalone.
- **`src/tabicl/prior/graph_lib/` — a sub-library for random DAGs.**
  `_graph.py`, `_node_function.py`, `_multi_function.py`, `_weights.py`,
  `_matrix.py`, `_points.py`, `_properties.py`, plus an `eval/` folder of
  plotting scripts (`plot_random_dag.py`, `plot_random_dataset.py`,
  `plot_random_function.py`) that visualise what the prior actually
  samples. Read these to see a prior rather than infer it from a paper.
- **`src/tabicl/train/` — pretraining.** `_run.py` is the loop,
  `_train_config.py` the configuration surface, `_optim.py` the optimiser
  setup, and **`_muon.py` is the Muon implementation** — the optimiser
  TabICLv2 credits for part of its gain, and which the papers reference
  but no other dump here contains.
- **`scripts/train_stage{1,2,3}.sh`** and
  **`scripts/train_v2_{clf,reg}_stage{1,2,3}.sh`** — the three-stage size
  curriculum as actually invoked, for v1 and for v2's classifier and
  regressor. These are the closest thing available to a reproducible
  recipe for pretraining a TFM from scratch.
- **`src/tabicl/_finetune/`** — `base.py`, `classifier.py`, `regressor.py`,
  `data.py`: gradient adaptation on top of the released weights.
- **`src/tabicl/forecast/`** — a time-series extension (`_engine.py`,
  `_forecaster.py`, `transforms/_calendar.py`, `_seasonality.py`), the
  TabICL analogue of TabPFN-TS.
- **`src/tabicl/shap/`** — `_shap.py`, `_shapiq.py`: interpretability
  hooks, comparable to what Rundel 2024 built for TabPFN.
- **`src/tabicl/_unsupervised/`** and `docs/` (Sphinx API reference).

**When to grep this file:** any question of the form "how is a TFM
actually trained?" — prior sampling, curriculum staging, optimiser choice,
loss construction — and any comparison of TabICL's design against the
TabPFN line. Also the reference for Muon.

---

## `NanoTabICL.txt`

**Upstream:** [github.com/soda-inria/nanotabicl](https://github.com/soda-inria/nanotabicl)
— the release the TabICLv2 paper points to.

**Related paper:**
[2026 — Qu et al. — TabICLv2](papers/2026/02_Qu_et_al._TabICLv2_A_better_faster_scalable_and_open_tabular_foundation_model.pdf).

**What it is.** Four files: `README.md`, `LICENSE`, **`model.py`** and
**`prior.py`**. A deliberately minimal TabICL — the `nanoTabPFN` idea
applied to the TabICL line, and the shortest readable path from "what is
a TFM" to working code, since architecture and data generation are one
file each.

**Why keep it along`TabICL.txt`:** the full repository is 127 files, and
the prior alone spans two packages. When the question is *pedagogical*
("what is the minimum that makes this work?") this is the better file;
when it is *operational* ("what does the real thing do?") use `TabICL.txt`.
Pairs naturally with `NanoTabPFN.txt` for a TabPFN-vs-TabICL comparison at
comparable, readable scale.

---

## `TabForestPFN.txt`

**Upstream:** [github.com/FelixdenBreejen/TabForestPFN](https://github.com/FelixdenBreejen/TabForestPFN)
(MIT; **dead since 2024-05**). Note the README still carries the arXiv v1
title, "Why In-Context Learning Transformers are Tabular Data
Classifiers" — the paper was retitled at v2.

**Related paper:**
[2024 — den Breejen et al. — TabForestPFN](papers/2024/10_Breejen_et_al._Fine_tuned_In_Context_Learning_Transformers_are_Excellent_Tabular_Data_Classifiers.pdf).

**What it is.** The origin of the tree-based prior. The dump is filtered
to source: upstream is ~1.36 GB across ~19,500 files, almost all of it
`outputs_done/` experiment artifacts, around ~1.2 MB of actual Python.

**Contents worth grepping.**

- **The synthetic generators** — `synthetic_generator_forest.py` (the
  paper's contribution: tables sampled from decision-tree/forest
  structures, deliberately unrealistic but with complex decision
  boundaries), `synthetic_generator_tabpfn.py` (their reimplementation of
  the TabPFN-style prior), `_cuts.py`, and `_mix.py` (the combination that
  produces TabForestPFN).
- **`pretrain.py`, `trainer_pretrain.py`, `trainer_finetune.py`** — both
  training stages, which is what lets you check the paper's claim that
  fine-tuning quality tracks pretraining-data complexity.

**When to grep this file:** designing or critiquing a tree-flavoured
prior, or tracing where Mitra's prior-mixing framework came from. Treat it
as historical — it targets TabPFN v1 and has not been touched since 2024.

---

## `LoCalPFN.txt`

**Upstream:** [github.com/layer6ai-labs/LoCalPFN](https://github.com/layer6ai-labs/LoCalPFN).
**No LICENSE file upstream** — treat as all-rights-reserved: read and
learn from it, do not vendor it.

**Related paper:**
[2024 — Thomas et al. — LoCalPFN](papers/2024/12_Thomas_et_al._Retrieval_Fine_Tuning_for_In_Context_Tabular_Models.pdf).

**What it is.** Unusually compact — eight Python files, ~58 KB — and
entirely unique in this folder: the only implementation of
**retrieval-based context construction**. `methods/ftknn.py` is LoCalPFN
itself (k-NN retrieval plus end-to-end fine-tuning), `methods/pfknn.py`
the simpler TabPFN-kNN baseline, with `pfn.py`, `dataset.py`, `config.py`,
`utils.py` and `main.py` around them. Fine-tuning is present; there is no
prior or pretraining.

**When to grep this file:** implementing or evaluating retrieved contexts,
and as the concrete counterpart to Nagler's localisation argument — this
is what "localise the predictor around the query" looks like in code.
Compare against `TabDPT.txt`, whose FAISS retrieval is the same lab's
later take.

---

## `TabSTAR.txt`

**Upstream:** [github.com/alanarazi7/TabSTAR](https://github.com/alanarazi7/TabSTAR)
(MIT; actively maintained). **The default branch is `master`, not `main`**
— a `/tree/main/` URL 404s.

**Related paper:**
[2025 — Arazi et al. — TabSTAR](papers/2025/12_Arazi_et_al._TabSTAR_A_Tabular_Foundation_Model_for_Tabular_Data_with_Text_Fields.pdf).

**What it is.** A complete text-aware TFM stack, and the only dump here
that shows a **pretrained language encoder being unfrozen and trained
jointly with tabular data**. Filtered to exclude the 401 per-dataset
metadata stubs under `tabstar_paper/datasets/annotated/`.

**Contents in detail.**

- **`tabstar_paper/pretraining/`** — `pretrainer.py`, `dataloaders.py`,
  `unfreezing.py` (the text-encoder unfreezing schedule), `hdf5.py`; with
  `do_pretrain.py` / `do_finetune.py` as entry points.
- **`src/tabstar/training/`** — `trainer.py`, **`lora.py`**,
  `checkpoint_averaging.py`. The LoRA implementation is directly
  comparable to the one in `On Finetuning Tabular Foundation Models.txt`.
- **`src/tabstar/preprocessing/verbalize.py`** — how columns and target
  tokens are turned into text for the encoder. The mechanical answer to
  "what does target-aware representation mean".
- **`src/tabstar/arch/`** — the architecture, and **baseline adapters** for
  tabpfnv2, tabicl, tabdpt and carte, useful as a worked example of
  wrapping several TFMs behind one interface.

**When to grep this file:** anything involving free-text columns, column
semantics, LoRA on a TFM, or checkpoint averaging.

---

## `CausalPFN.txt`

**Upstream:** [github.com/vdblm/CausalPFN](https://github.com/vdblm/CausalPFN)
(Apache-2.0; actively maintained; `pip install causalpfn`).

**Related paper:**
[2025 — Balazadeh Meresht et al. — CausalPFN](papers/2025/12_Balazadeh_Meresht_et_al._CausalPFN_Amortized_Causal_Effect_Estimation_via_In_Context_Learning.pdf).

**What it is.** The inference and estimation path of the causal-PFN
cluster's most deployable model. `src/causalpfn/causal_estimator.py` is
the user-facing estimator, `models/icl_model.py` and `transformer_layer.py`
the architecture, `evaluation.py` the metrics. **There is no prior
generator and no pretraining code** — the simulated-DGP library that makes
CausalPFN work is not released, so this dump answers "how do I *use* an
amortised causal estimator", not "how do I train one".

It also ships a benchmark harness with econml / CATENets / GRF / BART /
IPW baselines, which is a useful reference for how causal methods are
compared. Filtered to code: upstream carries ~175 MB of benchmark data
(201 realcause CSVs, IHDP `.npz`).

**When to grep this file:** wiring a CATE/ATE estimator into an evaluation
pipeline, or comparing the causal-PFN head against classical estimators.

