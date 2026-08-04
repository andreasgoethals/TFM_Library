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

Line counts are as of the 2026-07-17 snapshots; they drift on every
refresh, so treat them as rough sizes only.

| File | Lines | GitHub | Paper | What it gives us |
|------|-------|--------|-------|------------------|
| `Huggingface TabPFN.txt` | 551 | [tabpfn_2_5](https://huggingface.co/Prior-Labs/tabpfn_2_5), [tabpfn_2_6](https://huggingface.co/Prior-Labs/tabpfn_2_6) | [Hollmann 2025](papers/2025/01_Hollmann_et_al._Accurate_predictions_on_small_data_with_a_tabular_foundation_model.pdf), [Grinsztajn 2026](papers/2026/02_Grinsztajn_et_al._TabPFN_2.5_Advancing_the_State_of_the_Art_in_Tabular_Foundation_Models.pdf) | Primary citation source for checkpoint provenance (synthetic vs. real-finetuned, layer counts, intended limits, licence). |
| `NanoTabPFN.txt` | 1,103 | [automl/nanoTabPFN](https://github.com/automl/nanoTabPFN) | [Pfefferle 2025](papers/2025/12_Pfefferle_et_al._nanoTabPFN_A_Lightweight_and_Educational_Reimplementation_of_TabPFN.pdf) | Cleanest end-to-end reference of a PFN training loop. Cleanest structural template for a PFN training loop. |
| `On Finetuning Tabular Foundation Models.txt` | 77,581 | [yandex-research/tabpfn-finetuning](https://github.com/yandex-research/tabpfn-finetuning) | [Rubachev 2025](papers/2025/06_Rubachev_et_al._On_Finetuning_Tabular_Foundation_Models_1.pdf) | Yandex research repo for TabPFNv2 full/PEFT finetuning: experiment configs, reports, LoRA utilities, vendored TabPFN changes, and practical LR/early-stopping recipes. |
| `PFNS.txt` | 29,093 | [SamuelGabriel/PFNs](https://github.com/SamuelGabriel/PFNs) | [Müller 2021](papers/2021/12_Muller_et_al._Transformers_Can_Do_Bayesian_Inference.pdf) | Implementations of every encoder step that runs *inside* every TabPFN forward pass (NaN handling, normalisation, …). Delimits what an upstream preprocessing step should *not* duplicate. |
| `PFNs4BO.txt` | 7,455 | [automl/PFNs4BO](https://github.com/automl/PFNs4BO) | [Müller 2023](papers/2023/05_Muller_et_al._PFNs4BO_In_Context_Learning_for_Bayesian_Optimization.pdf) | PFN-as-Bayesian-optimisation surrogate. Tangential to tabular prediction; relevant only for PFN-as-BO-surrogate work. |
| `TabDPT.txt` | 3,168 | [layer6ai-labs/TabDPT-inference](https://github.com/layer6ai-labs/TabDPT-inference) | [Ma 2026](papers/2026/01_Ma_et_al._TabDPT_Scaling_Tabular_Foundation_Models_on_Real_Data.pdf) | Inference code for the real-data-only competitor to TabPFN. Comparison baseline. |
| `TabPFN .txt` | 77,938 | [PriorLabs/tabPFN](https://github.com/PriorLabs/tabPFN) | [Hollmann 2023](papers/2023/09_Hollmann_et_al._TabPFN_A_Transformer_That_Solves_Small_Tabular_Classification_Problems_in_a_Second.pdf), [Hollmann 2025](papers/2025/01_Hollmann_et_al._Accurate_predictions_on_small_data_with_a_tabular_foundation_model.pdf), [Grinsztajn 2026](papers/2026/02_Grinsztajn_et_al._TabPFN_2.5_Advancing_the_State_of_the_Art_in_Tabular_Foundation_Models.pdf) | Canonical sklearn-style API, all checkpoint metadata, the multi-table finetuning machinery (`get_preprocessed_dataset_chunks`, `DatasetCollectionWithPreprocessing`, `FinetunedTabPFN*`). Primary code reference for training/finetuning work. |
| `TabPFN Client.txt` | 12,672 | [PriorLabs/tabpfn-client](https://github.com/PriorLabs/tabpfn-client) | — | Hosted-API HTTP client. Irrelevant to self-hosted training; only for benchmarking the hosted API. |
| `TabPFN Docs.txt` | 7,797 | _GitHub source removed_ — refresh manually from [docs.priorlabs.ai/overview](https://docs.priorlabs.ai/overview) | — | The docs.priorlabs.ai source. Documents *intent* of every config knob; faster to grep than the implementation in `TabPFN .txt`. |
| `TabPFN Drift-Resilient.txt` | 138,551 | [automl/Drift-Resilient_TabPFN](https://github.com/automl/Drift-Resilient_TabPFN) | [Helli 2024](papers/2024/11_Helli_et_al._Drift_Resilient_TabPFN_In_Context_Learning_Temporal_Distribution_Shifts_on_Tabular_Data_1.pdf) | Drift-aware training augmentation. The reference for drift-aware training-time augmentation. |
| `TabPFN Extensions.txt` | 21,784 | [PriorLabs/tabpfn-extensions](https://github.com/PriorLabs/tabpfn-extensions) | — | `AutoTabPFN` post-hoc ensembling, RF-PFN, embeddings, HPO. Source of evaluation baselines. |
| `TabPFN V2 Finetuning.txt` | 4,331 | [PriorLabs/TabPFN/examples](https://github.com/PriorLabs/TabPFN/tree/main/examples) | [Rubachev 2025](papers/2025/06_Rubachev_et_al._On_Finetuning_Tabular_Foundation_Models_1.pdf) | The `finetune_classifier.py` and `finetune_regressor.py` reference scripts built on the official `FinetunedTabPFN*` wrappers. |
| `TabPFN Wide.txt` | 2,279,103 | [not-a-feature/TabPFN-Wide](https://github.com/not-a-feature/TabPFN-Wide) | [Kolberg 2026](papers/2026/03_Kolberg_et_al._TabPFN_Wide_Continued_Pre_Training_for_Extreme_Feature_Counts.pdf) | Continued-pretraining for extreme-feature-count regimes via a feature-widening prior (it argues *against* feature reduction; not the source of our agglomeration). Gitignored (~366 MB); regenerate locally. |
| `TabTune.txt` | 162,653 | [Lexsi-Labs/TabTune](https://github.com/Lexsi-Labs/TabTune) | [Tanna 2025](papers/2025/12_Tanna_et_al._TabTune_A_Unified_Library_for_Inference_and_Fine_Tuning_Tabular_Foundation_Models.pdf) | Unified sklearn-style wrapper around the **non-TabPFN** tabular foundation models (TabICL, OrionMSP/Bix, Mitra, ContextTab, TabDPT, LimiX) plus TabPFNv2.6 native FT, ensembling, distillation, and a `TabularLeaderboard`. A convenient source of non-TabPFN eval baselines; it does **not** natively support Real-TabPFN-style multi-dataset continued pretraining. |
| `TransformersCanDoBayesianInference.txt` | 12,325 | [automl/TransformersCanDoBayesianInference](https://github.com/automl/TransformersCanDoBayesianInference) | [Müller 2021](papers/2021/12_Muller_et_al._Transformers_Can_Do_Bayesian_Inference.pdf) | The original (unmaintained) code release of the 2021 PFN paper. Historical; useful for explaining what a PFN is. |
| `VSC Documentation.txt` | 38,120 | [hpcleuven/VscDocumentation](https://github.com/hpcleuven/VscDocumentation) | — | Full Sphinx source of the VSC supercomputer documentation. SLURM job scripting, **Mindwell B200 / wICE H100+A100** partitions, Lustre/GPFS + project-staging storage tiers, account / credit management. The reference when writing SLURM scripts. |

## Layout

This file lives at the repo root; the dumps live in
[`repositories/`](repositories/) — sixteen flat `.txt` files, one per
upstream source, named exactly as in the table above (`TabPFN .txt`
keeps its intentional trailing space). Line counts are in the table;
the only file not tracked by git is `TabPFN Wide.txt` (~366 MB,
gitignored — regenerate with `python scripts/refresh_repositories.py`).

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
* `tests/cls_example.py`, `reg_example.py` — minimum working
  example.

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

**v2.6-vs-v3 criterion handling (regressors).** v3's
`model.forward` takes `test_targets_MB`, so the loader STRIPS the
`criterion.*` keys and rebuilds the bar-distribution from the model's
`regression_borders` buffer; v2.6 has no `test_targets_MB`, so the
loader REQUIRES the `criterion.*` keys. Writing `criterion.*` for regressors
unconditionally — required by v2.6, harmlessly stripped by v3 — makes a
saved regressor checkpoint round-trip for both architectures.

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
cannot be refreshed by ``scripts/refresh_repositories.py``. It's
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

## `VSC Documentation.txt`

**Upstream:** [github.com/hpcleuven/VscDocumentation](https://github.com/hpcleuven/VscDocumentation)
(the source of the [VSC documentation site](https://docs.vscentrum.be)).

**Related paper:** none — this is supercomputer infrastructure
documentation, not a research artefact.

**What it is.** Flat dump of the entire Sphinx-generated VSC
(Vlaams Supercomputer Centrum / Flemish Supercomputer Centre)
user documentation. ~39,000 lines of `.rst` source covering
account management, SSH/MFA setup, **Genius / wICE / Mindwell**
cluster hardware, SLURM job scripting, storage tiers, scientific
software modules, and the various ways to acknowledge the VSC.

**Why it matters here.** GPU training runs on the **Mindwell B200** partition; CPU data prep and
eval run on **wICE**. When writing SLURM scripts —
partitions, GPU allocation,
walltimes, the Lustre/GPFS storage split — this dump is the canonical
reference. Verified facts (as of the 2026-06-23 dump; grep the bolded
keywords):

* **Mindwell** (grep `gpu_b200`): partition `gpu_b200`, 3 nodes × 8
  = **24 B200 GPUs**, **192 GiB** VRAM each, AMD EPYC Turin hosts; max
  **24 cores + ~190 GiB CPU mem per GPU**. Account `lp_mindwell_pilot`
  (free pilot). `--clusters=mindwell`. GPFS scratch.
* **wICE** (grep `gpu_h100`): `gpu_h100` (5×4 = 20 H100, 80 GiB,
  16 cores/GPU) and `gpu_a100` (4×4 = 16 A100, 80 GiB, 18 cores/GPU).
  Lustre scratch. CPU `batch` partition for data prep.
* **Storage** (grep `VSC_SCRATCH`): `$VSC_HOME` 3 GiB / `$VSC_DATA`
  75 GiB (both NFS, backed up, all-cluster) / `$VSC_SCRATCH` 500 GiB
  (Lustre on wICE+Genius, GPFS on Mindwell; **purged after 30 days** —
  and `mv`/`rsync -a` don't refresh atime, so stage with `cp`).
  **Project ("staging") storage** lives under `$VSC_PROJECT_LUSTRE1`
  (`stg_XXXXX`, Lustre) and `$VSC_PROJECT_GPFS1` (Mindwell, GPFS) —
  single-copy, not guaranteed backed up. **Hard rule:** Mindwell jobs
  must use GPFS, wICE/Genius jobs must use Lustre for *sustained* I/O.
* **Scheduling** (grep `sam-balance`): `--clusters=` is
  mandatory; GPU walltime caps at **72 h** (no `gpu_*_long`); shorter
  walltime ⇒ better backfill priority; `sam-balance -A <acct>` checks
  credits (B200 437.5 / H100 569.4 / A100 141.7 per GPU-min).
* **Cross-cluster:** `--dependency` (afterok) across `-M` clusters is
  **undocumented/unverified** — safest to treat it as unsupported and
  submit per-cluster stages independently, sequenced through the shared
  staging tier.

**When to grep this file:** writing/updating a SLURM script, debugging
a job-submission error, choosing a partition or GPU type, or sizing
storage.

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
  `python scripts/refresh_repositories.py` (see its module docstring
  for `--only` / `--force-shrink` / `--timeout`). It re-dumps every
  mapped file via gitingest and **overwrites the existing file under
  the same filename** — atomically, with a shrink guard — so existing
  greps keep resolving. After a refresh, spot-check that the symbol
  names cited in this file and in `SUMMARIES.md` still exist, and log
  the refresh in `CHANGELOG.md` (AGENTS.md rule 5).
- `TabPFN Docs.txt` and `Huggingface TabPFN.txt` have no git
  upstream (`SKIP_NON_GIT` in the script): refresh them manually
  from docs.priorlabs.ai and the Hugging Face model cards.
