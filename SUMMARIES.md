# Literature on Tabular Foundation Models

A chronological tour of the papers in this folder. The arc:
PFNs (in-context Bayesian inference for arbitrary priors) → TabPFN
(PFNs with a tabular prior) → TabPFNv2 (the first production-grade
release) → a Cambrian explosion of variants (continued
pretraining, drift, fairness, causal inference, time series, many
classes, scalability) → TabPFN-2.5 (whose *default* checkpoint is
the real-data continued-pretrained variant) / 2.6 (back to a
synthetic-only default) →
TabPFN-3 (May 2026; new three-stage architecture, scales to 1M
rows, test-time-compute "Thinking" mode) → and, from June 2026, the
first big-tech entrant shipping the paradigm as a product (Google's
TabFM, wired into BigQuery).

For every paper:

* **Where it fits** in the picture above.
* **What it actually contains** — methods, datasets, headline result.
* **Strengths and limitations** — what the paper does and does not
  support.

**This document is project-neutral by contract** (see AGENTS.md). It
describes the literature for every consuming project; it contains no
project's pipeline details, hyperparameter choices, or relevance
rankings. Those belong in your project's own `PROJECT_SPECIFIC.md` —
copy [`PROJECT_SPECIFIC.template.md`](PROJECT_SPECIFIC.template.md)
inside your project's copy of this folder and write them there.

## Overview table

| Date | Authors | Title | One-line contribution | PDF |
|---------|---------|-------|-----------------------|-----|
| 2021-12 | Müller et al. | Transformers Can Do Bayesian Inference | Foundational PFN paper: a transformer trained on synthetic samples from a prior approximates the prior's posterior in-context. | [pdf](papers/2021/12_Muller_et_al._Transformers_Can_Do_Bayesian_Inference.pdf) |
| 2023-05 | Müller et al. | PFNs4BO — In-Context Learning for Bayesian Optimization | PFN as a drop-in surrogate for Gaussian-Process BO. | [pdf](papers/2023/05_Muller_et_al._PFNs4BO_In_Context_Learning_for_Bayesian_Optimization.pdf) |
| 2023-07 | Nagler | **Statistical Foundations of Prior-Data Fitted Networks** | The theory of *why* PFN in-context learning works — and its limit: a frequentist reading in which variance vanishes but bias only vanishes with proper localisation, which the transformer does not guarantee. | [pdf](papers/2023/07_Nagler_Statistical_Foundations_of_Prior_Data_Fitted_Networks.pdf) |
| 2023-09 | Hollmann et al. | TabPFN — A Transformer That Solves Small Tabular Classification Problems in a Second | First TabPFN: PFN trained on a tabular SCM prior, beats AutoML baselines on small datasets. | [pdf](papers/2023/09_Hollmann_et_al._TabPFN_A_Transformer_That_Solves_Small_Tabular_Classification_Problems_in_a_Second.pdf) |
| 2024-03 | Rundel et al. | Interpretable Machine Learning for TabPFN | Adapts SHAP / partial-dependence / interaction analysis to TabPFN's in-context inference path. | [pdf](papers/2024/03_Rundel_et_al._Interpretable_Machine_Learning_for_TabPFN.pdf) |
| 2024-06 | Breugel and Schaar | Why Tabular Foundation Models Should Be a Research Priority | Position paper: tabular FMs are an under-invested high-leverage area. | [pdf](papers/2024/06_Breugel_and_Schaar_Why_Tabular_Foundation_Models_Should_Be_a_Research_Priority.pdf) |
| 2024-10 | den Breejen et al. | **TabForestPFN** — Fine-tuned In-Context Learning Transformers are Excellent Tabular Data Classifiers | Swaps TabPFN's SCM prior for a *forest* generator producing unrealistic tables with complex decision boundaries; fine-tuning ICL transformers then beats GBDTs. The tree-prior ancestor of Mitra. | [pdf](papers/2024/10_Breejen_et_al._Fine_tuned_In_Context_Learning_Transformers_are_Excellent_Tabular_Data_Classifiers.pdf) |
| 2024-11 | Helli et al. | Drift-Resilient TabPFN | Trains TabPFN with a drift-injecting synthetic prior, generalises better under distribution shift. | [pdf](papers/2024/11_Helli_et_al._Drift_Resilient_TabPFN_In_Context_Learning_Temporal_Distribution_Shifts_on_Tabular_Data_1.pdf) |
| 2024-12 | Hoo et al. | The Tabular Foundation Model TabPFN Outperforms Specialized Time Series Forecasting Models | TabPFN-TS: forecasting framed as tabular regression on timestamp-derived features (no lags); an 11M-param frozen TabPFN beats Chronos-Mini and matches Chronos-Large. | [pdf](papers/2024/12_Hoo_et_al._The_Tabular_Foundation_Model_TabPFN_Outperforms_Specialized_Time_Series_Forecasting_Models_Based_on.pdf) |
| 2024-12 | Thomas et al. | **LoCalPFN** — Retrieval & Fine-Tuning for In-Context Tabular Models | Retrieves a k-NN neighbourhood as the context and fine-tunes end-to-end, breaking v1's size ceiling; SOTA on 95 TabZilla datasets. Ancestor of TabDPT's retrieval. | [pdf](papers/2024/12_Thomas_et_al._Retrieval_Fine_Tuning_for_In_Context_Tabular_Models.pdf) |
| 2024-12 | Feuer et al. | **TuneTables** — Context Optimization for Scalable Prior-Data Fitted Networks | Compresses a large dataset into a small *learned* context (prompt tuning for PFNs), lifting TabPFN v1's ~1000-row ceiling; best average rank over 19 algorithms on 98 datasets while tuning <5% of parameters. | [pdf](papers/2024/12_Feuer_et_al._TuneTables_Context_Optimization_for_Scalable_Prior_Data_Fitted_Networks.pdf) |
| 2025-01 | Hollmann et al. | Accurate predictions on small data with a tabular foundation model | The TabPFNv2 paper (Nature). Production-grade architecture with alternating-attention, NaN handling, ensemble preprocessing. | [pdf](papers/2025/01_Hollmann_et_al._Accurate_predictions_on_small_data_with_a_tabular_foundation_model.pdf) |
| 2025-02 | Liu and Ye | TabPFN Unleashed — A Scalable and Effective Solution to Tabular Classification Problems | Inference-time tricks (stratified context, bootstrap, query subsampling) that push v2 past its 10k-row limit. | [pdf](papers/2025/02_Liu_and_Ye_TabPFN_Unleashed_A_Scalable_and_Effective_Solution_to_Tabular_Classification_Problems.pdf) |
| 2025-05 | Müller et al. | Position — The Future of Bayesian Prediction Is Prior-Fitted | Position paper: PFNs as a unifying framework for approximate Bayesian inference. | [pdf](papers/2025/05_Muller_et_al._Position_The_Future_of_Bayesian_Prediction_Is_Prior_Fitted.pdf) |
| 2025-05 | Qu et al. | TabICL — A Tabular Foundation Model for In-Context Learning on Large Data | Hierarchical attention TabPFN-competitor scaling to 500 k-row tables. | [pdf](papers/2025/05_Qu_et_al._TabICL_A_Tabular_Foundation_Model_for_In_Context_Learning_on_Large_Data.pdf) |
| 2025-06 | Robertson et al. | FairPFN — A Tabular Foundation Model for Causal Fairness | PFN with explicit protected-attribute structure for counterfactual fairness audits. | [pdf](papers/2025/06_Robertson_et_al._FairPFN_A_Tabular_Foundation_Model_for_Causal_Fairness.pdf) |
| 2025-06 | Rubachev et al. | **On Finetuning Tabular Foundation Models** | Empirical study: fine-tuning TabPFN with full / LoRA / partial (last-layers, LN+embeddings+head) updates. Hyperparameter ranges that work. | [pdf](papers/2025/06_Rubachev_et_al._On_Finetuning_Tabular_Foundation_Models_1.pdf) |
| 2025-06 | Ye et al. | A Closer Look at TabPFN v2 — Understanding Its Strengths and Extending Its Capabilities | Empirical analysis identifying v2 weaknesses and proposing patches that became v2.5 specialist checkpoints. | [pdf](papers/2025/06_Ye_et_al._A_Closer_Look_at_TabPFN_v2_Understanding_Its_Strengths_and_Extending_Its_Capabilities.pdf) |
| 2025-07 | Garg et al. | **Real-TabPFN** — Improving Tabular Foundation Models via Continued Pre-training With Real-World Data | **The reference continued-pretraining recipe.** Continue-pretrains TabPFNv2 on 71 curated real datasets; +0.022 ROC-AUC on the OpenML AutoML benchmark. | [pdf](papers/2025/07_Garg_et_al._Real_TabPFN_Improving_Tabular_Foundation_Models_via_Continued_Pre_training_With_Real_World_Data.pdf) |
| 2025-10 | Zhang et al. | Mitra — Mixed Synthetic Priors for Enhancing Tabular Foundation Models | A "mixed" synthetic prior interpolating between TabPFN's and ForestPFN's priors. | [pdf](papers/2025/10_Zhang_et_al._Mitra_Mixed_Synthetic_Priors_for_Enhancing_Tabular_Foundation_Models.pdf) |
| 2025-11 | Robertson et al. | Do-PFN — In-Context Learning for Causal Effect Estimation | PFN trained to predict ``do``-interventions; in-context causal effect estimation. | [pdf](papers/2025/11_Robertson_et_al._Do_PFN_In_Context_Learning_for_Causal_Effect_Estimation.pdf) |
| 2025-11 | Zhang et al. | TabPFN — One Model to Rule Them All | Survey-style win aggregation across many domains. | [pdf](papers/2025/11_Zhang_et_al._TabPFN_One_Model_to_Rule_Them_All.pdf) |
| 2025-11 | Bouadi et al. | **Orion-MSP** — Multi-Scale Sparse Attention for Tabular In-Context Learning | Multi-scale features + block-sparse attention + Perceiver memory for bidirectional flow between stages; scales to wide tables. | [pdf](papers/2025/11_Bouadi_et_al._Orion_MSP_Multi_Scale_Sparse_Attention_for_Tabular_In_Context_Learning.pdf) |
| 2025-12 | Pfefferle et al. | nanoTabPFN — A Lightweight and Educational Reimplementation of TabPFN | TabPFN training loop in under 500 lines; the cleanest reference implementation publicly available. | [pdf](papers/2025/12_Pfefferle_et_al._nanoTabPFN_A_Lightweight_and_Educational_Reimplementation_of_TabPFN.pdf) |
| 2025-12 | Tanna et al. | TabTune — A Unified Library for Inference and Fine-Tuning Tabular Foundation Models | Common API across TabPFN, TabICL, TabDPT for fair head-to-head comparison. | [pdf](papers/2025/12_Tanna_et_al._TabTune_A_Unified_Library_for_Inference_and_Fine_Tuning_Tabular_Foundation_Models.pdf) |
| 2025-12 | Spinaci et al. | **ConTextTab** — A Semantics-Aware Tabular In-Context Learner | Table-native ICL with per-modality (text/date/number) embeddings trained on large-scale *real* tables; new standard on the semantically rich CARTE benchmark. | [pdf](papers/2025/12_Spinaci_et_al._ConTextTab_A_Semantics_Aware_Tabular_In_Context_Learner.pdf) |
| 2025-12 | Arazi et al. | **TabSTAR** — A Tabular Foundation Model for Tabular Data with Text Fields | Unfreezes a text encoder and conditions on *target tokens* for semantically target-aware representations; no dataset-specific parameters, and pretraining shows scaling laws in dataset count. | [pdf](papers/2025/12_Arazi_et_al._TabSTAR_A_Tabular_Foundation_Model_for_Tabular_Data_with_Text_Fields.pdf) |
| 2025-12 | Balazadeh Meresht et al. | **CausalPFN** — Amortized Causal Effect Estimation via In-Context Learning | One transformer trained on simulated ignorable DGPs returns calibrated CATE/ATE for new observational tables out of the box; best average rank over 310 tasks. | [pdf](papers/2025/12_Balazadeh_Meresht_et_al._CausalPFN_Amortized_Causal_Effect_Estimation_via_In_Context_Learning.pdf) |
| 2026-01 | Hoo et al. | From Tables to Time — Extending TabPFN-v2 to Time Series Forecasting | Native time-axis attention version of TabPFN. | [pdf](papers/2026/01_Hoo_et_al._From_Tables_to_Time_Extending_TabPFN_v2_to_Time_Series_Forecasting.pdf) |
| 2026-01 | Klein and Hoffart | Position — Foundation Models for Tabular Data within Systemic Contexts Need Grounding | Position paper from SAP: tabular FMs trained on isolated tables miss the operational context (business rules, code, data models) that gives data meaning. Proposes Semantically Linked Tables (SLT) and FMSLT as a new model class. | [pdf](papers/2026/01_Klein_and_Hoffart_Position_Foundation_Models_for_Tabular_Data_within_Systemic_Contexts_Need_Grounding.pdf) |
| 2026-01 | Ma et al. | TabDPT — Scaling Tabular Foundation Models on Real Data | Real-data-only TabPFN competitor; retrieval-based self-supervision on OpenML. | [pdf](papers/2026/01_Ma_et_al._TabDPT_Scaling_Tabular_Foundation_Models_on_Real_Data.pdf) |
| 2026-02 | Grinsztajn et al. | **TabPFN-2.5** — Advancing the State of the Art in Tabular Foundation Models | Successor architecture (18–24 layers, 50 k×2000 limit) and the family of v2.5 checkpoints. | [pdf](papers/2026/02_Grinsztajn_et_al._TabPFN_2.5_Advancing_the_State_of_the_Art_in_Tabular_Foundation_Models.pdf) |
| 2026-02 | Ma et al. | Foundation Models for Causal Inference via Prior-Data Fitted Networks | Unified causal-PFN framework; Do-PFN + FairPFN at scale. | [pdf](papers/2026/02_Ma_et_al._Foundation_Models_for_Causal_Inference_via_Prior_Data_Fitted_Networks.pdf) |
| 2026-02 | Qu et al. | TabICLv2 — A better, faster, scalable, and open tabular foundation model | Improved TabICL with bigger context limit and open weights. | [pdf](papers/2026/02_Qu_et_al._TabICLv2_A_better_faster_scalable_and_open_tabular_foundation_model.pdf) |
| 2026-03 | Kolberg et al. | **TabPFN-Wide** — Continued Pre-Training for Extreme Feature Counts | Continued-pretraining for >500-feature data via a feature-widening synthetic prior (argues *against* feature reduction). | [pdf](papers/2026/03_Kolberg_et_al._TabPFN_Wide_Continued_Pre_Training_for_Extreme_Feature_Counts.pdf) |
| 2026-04 | Tanna et al. | **Exploring Fine-Tuning for Tabular Foundation Models** | First large-scale study of *when* fine-tuning helps TFMs (zero-shot vs meta-learning vs SFT vs PEFT/LoRA across TALENT / OpenML-CC18 / TabZilla). Full SFT can hurt accuracy & calibration; gains are model- and data-dependent; TabPFN is comparatively robust. | [pdf](papers/2026/04_Tanna_et_al._Exploring_Fine_Tuning_for_Tabular_Foundation_Models.pdf) |
| 2026-04 | Bouadi et al. | **Orion-BiX** — Bi-Axial Attention for Tabular In-Context Learning | Bi-axial encoder (standard / grouped / hierarchical / relational attention fused by multi-CLS) plus a label-aware ICL head with hierarchical routing for large label spaces. | [pdf](papers/2026/04_Bouadi_et_al._Orion_Bix_Bi_Axial_Attention_for_Tabular_In_Context_Learning.pdf) |
| 2026-05 | Grinsztajn et al. | **TabPFN-3** — Technical Report | **The current frontier of the TabPFN line.** New three-stage architecture (column-wise → row-wise → ICL), scales to 1M rows on a single H100, many-class attention decoder, "Thinking" test-time-compute mode. Synthetic-prior only, +200 Elo over TabPFN-2.6 on TabArena-medium. | [pdf](papers/2026/05_Grinsztajn_et_al._TabPFN_3_Technical_Report.pdf) |
| 2026-05 | Tanna et al. | **Data Presentation Over Architecture** — Resampling Strategies for Credit Risk Prediction with TFMs | On Home Credit and Lending Club, **how the context window is built explains more AUC variance than which TFM you pick**: balanced/hybrid sampling adds 3–4 AUC points over uniform, exceeding the spread between TFM families. | [pdf](papers/2026/05_Tanna_et_al._Data_Presentation_Over_Architecture_Resampling_Strategies_for_Credit_Risk_Prediction_with_Tabular_Foundation_Models.pdf) |
| 2026-06 | Purucker et al. | **Beyond IID: How General Are Tabular Foundation Models, Really?** | BeyondArena (142 curated datasets, IID + temporal + grouped splits): TFM ICL wins tiny/small IID data but **loses to tuned RealMLP/GBDTs under temporal & grouped splits**, with the gap growing with sample size and high-cardinality categoricals. Fine-tuning explicitly untested. | [pdf](papers/2026/06_Purucker_et_al._Beyond_IID_How_General_Are_Tabular_Foundation_Models_Really.pdf) |
| 2026-06 | Kong and Das (Google) | **TabFM** — Introducing TabFM: A zero-shot foundation model for tabular data | *Blog post, not a paper.* Google's TabPFN+TabICL **hybrid** (alternating row/column attention → row compression → ICL over row embeddings), trained on hundreds of millions of synthetic SCM datasets; TabArena Elo vs tuned GBDTs; shipping into **BigQuery `AI.PREDICT`**. | [pdf](papers/2026/06_Kong_and_Das_Introducing_TabFM_A_zero_shot_foundation_model_for_tabular_data.pdf) |

---

## 2021-12 — Müller et al. — Transformers Can Do Bayesian Inference

**arXiv:** [2112.10510](https://arxiv.org/abs/2112.10510) ·
**PDF:** [open](papers/2021/12_Muller_et_al._Transformers_Can_Do_Bayesian_Inference.pdf)

**Where it fits.** The bedrock of the entire PFN / TabPFN line.
Müller and colleagues introduce *Prior-Fitted Networks* (PFNs):
transformers that, after a single training phase on synthetic
datasets sampled from a Bayesian prior, perform approximate
posterior inference *in context* on any new dataset drawn from
that prior — without any parameter update.

**What it contains.** The training recipe: at each step, sample a
prior dataset (an arbitrary stochastic process specified by the
researcher), give the transformer the labelled context plus an
unlabelled query point, and use cross-entropy loss to push the
network's prediction toward the true label sampled from the
prior. The authors prove (under capacity and prior-coverage
assumptions) that the trained network's predictive distribution
converges to the true Bayesian posterior of the underlying prior.
They demonstrate this on synthetic Gaussian-Process regression,
on Bayesian neural-network regression, and on small classification
problems sampled from a structured-causal-model prior — the
beginnings of what would become TabPFN.

The crucial conceptual contribution: there is no learning at
*inference* time. Once trained, the network is a fixed function;
calling it on a new dataset is one forward pass. This sidesteps
both the brittleness of MCMC sampling for non-conjugate priors
and the slowness of variational fitting for every new task.

---

## 2023-05 — Müller et al. — PFNs4BO

**arXiv:** [2305.17535](https://arxiv.org/abs/2305.17535) ·
**PDF:** [open](papers/2023/05_Muller_et_al._PFNs4BO_In_Context_Learning_for_Bayesian_Optimization.pdf)

**Where it fits.** Sister paper to TabPFN — applies PFNs to a
different domain (Bayesian-optimisation surrogate models).

**What it contains.** A PFN trained on synthetic
(configuration, value) pairs from a hyperparameter-search-style
prior. At inference time, given a few past evaluations of an
unknown objective, the PFN predicts the expected value at
unseen configurations. Used as a drop-in replacement for
Gaussian-Process surrogates inside an acquisition-function loop.
The advantages over GPs: no kernel choice, no quadratic-time
fitting, and the ability to encode arbitrary prior knowledge by
designing the prior generator.

---

<a id="nagler-theory"></a>

## 2023-07 — Nagler — Statistical Foundations of Prior-Data Fitted Networks

**Venue:** ICML 2023 (PMLR v202) · Thomas Nagler, LMU Munich / Munich
Center for Machine Learning ·
**PDF:** [open](papers/2023/07_Nagler_Statistical_Foundations_of_Prior_Data_Fitted_Networks.pdf)

**Where it fits.** The theory paper the rest of this corpus leans on
without always citing. Müller 2021 justified PFNs with a Bayesian
argument; Nagler asks what actually happens statistically, and arrives at
a *frequentist* reading that explains PFN behaviour more completely —
including the phenomenon nobody had accounted for, that accuracy keeps
improving when a PFN is fed datasets far larger than anything it saw in
pretraining.

**What it contains.** The central move is to stop treating the network as
an approximate posterior and treat it as a **pre-tuned but untrained
predictor**: a fixed function of the context set. Under that lens the
usual bias–variance decomposition applies, and two conditions emerge:

* **Variance vanishes** if the predictor's sensitivity to any *individual*
  training sample vanishes as the context grows. The transformer
  architecture, with attention averaging over context rows, delivers this
  — which is why PFNs behave stably and improve with more context.
* **Bias vanishes only if the predictor is appropriately *localised*
  around the test feature** — i.e. it must weight nearby context points
  more than distant ones. **Current PFN transformer implementations do
  not guarantee this.**

So PFNs get the variance half of consistency for free and the bias half
not at all. That asymmetry is the paper's real contribution and it is
predictive: it says a PFN will look excellent in-distribution and
plateau or mislead where localisation matters, and it tells architects
what to fix.

**Strengths and limitations.** This is the only rigorous account of *why*
the paradigm works, and it is constructive rather than merely critical —
"design for localisation" is actionable, and the later retrieval-based
models (LoCalPFN, TabDPT) can be read as exactly that fix arrived at
empirically. Its limitations are those of theory: the results are
asymptotic, they concern classification with a fixed pretraining
distribution, and they say nothing about how much bias a given
architecture actually carries on a given table. It also predates
TabPFN v2, so the analysis is of the v1-era architecture — though the
argument is about attention-based context aggregation in general and
transfers.

---

## 2023-09 — Hollmann et al. — TabPFN

**arXiv:** [2207.01848](https://arxiv.org/abs/2207.01848) ·
**PDF:** [open](papers/2023/09_Hollmann_et_al._TabPFN_A_Transformer_That_Solves_Small_Tabular_Classification_Problems_in_a_Second.pdf)

**Where it fits.** The first TabPFN. Applies the PFN recipe to
small tabular classification with a structured-causal-model
prior tailored for tabular data.

**What it contains.** A transformer takes
``(X_context, y_context, X_query) → ŷ_query`` in one forward
pass. The prior generator samples small structural causal models
that specify a joint distribution over features and a target;
millions of these are sampled and the transformer is trained to
predict held-out targets given context. At inference time, no
gradient updates: a held-out test set is just appended to the
training set in the input, the transformer marginalises over its
implicit prior, and predictions come out one forward pass later.

Empirical headline: on the OpenML-CC18 benchmark restricted to
small datasets (≤ 1k rows, ≤ 100 features, ≤ 10 classes),
TabPFN beats well-tuned XGBoost, Random Forest, and a tuned
AutoGluon stack — in a *second* of inference where AutoGluon
takes minutes. The paper also discusses calibration (TabPFN's
predictive probabilities are sharp and well-calibrated) and
robustness to small-sample noise.

---

## 2024-03 — Rundel et al. — Interpretable Machine Learning for TabPFN

**arXiv:** [2403.10923](https://arxiv.org/abs/2403.10923) ·
**PDF:** [open](papers/2024/03_Rundel_et_al._Interpretable_Machine_Learning_for_TabPFN.pdf)

**Where it fits.** Interpretability tooling for TabPFN.

**What it contains.** Adapts the standard interpretability
toolkit — SHAP values, partial-dependence plots, feature
interaction analysis — to TabPFN's in-context inference path.
Key challenge addressed: SHAP for TabPFN cannot use the standard
"model-as-black-box" approach because querying with a single row
plus the entire training set is the unit of inference, not just
the test row. The paper proposes adaptations that account for
the in-context structure and shows that the resulting
attributions are stable and consistent with expert intuition on
several benchmark datasets.

The headline argument is that TabPFN is *no harder* to
interpret than a GBDT once the right tooling is in place.

---

## 2024-06 — Breugel and Schaar — Why Tabular Foundation Models Should Be a Research Priority

**arXiv:** [2405.01147](https://arxiv.org/abs/2405.01147) ·
**PDF:** [open](papers/2024/06_Breugel_and_Schaar_Why_Tabular_Foundation_Models_Should_Be_a_Research_Priority.pdf)

**Where it fits.** Position / agenda paper. Pre-dates Real-TabPFN
and TabPFN-2.5; argues that tabular ML is an under-invested
research area despite tabular data being economically dominant.

**What it contains.** A diagnosis of why tabular ML lags behind
NLP and computer vision in foundation-model adoption. Five
proposed obstacles: (1) data heterogeneity (every tabular
dataset has its own schema), (2) the no-pretraining norm
(researchers train models from scratch per dataset), (3) the
absence of a TabArena-equivalent that the field treats as
canonical, (4) the absence of a public, large, high-quality
real-data corpus comparable to ImageNet or LAION, (5) the
absence of a commercial player whose interests align with
publishing such a corpus. The paper sketches research
directions for each.

---

## 2024-10 — den Breejen et al. — TabForestPFN

**Venue:** ICLR 2025 submission / OpenReview `pE0UM18TQh` (the copy held
here is the double-blind review version) ·
**PDF:** [open](papers/2024/10_Breejen_et_al._Fine_tuned_In_Context_Learning_Transformers_are_Excellent_Tabular_Data_Classifiers.pdf)

**Where it fits.** The origin of the **tree-based prior**, and therefore
the direct ancestor of Mitra's prior-mixing framework. It is also an
early, clean statement of the finding Rubachev 2025 later confirmed at
scale: fine-tuning a TFM is not a compromise but a large win.

**What it contains.** Two findings that interact.

* **Fine-tuning gives ICL transformers complex decision boundaries.**
  The paper extends TabPFN to the fine-tuning setting and reports a
  significant performance boost, then observes *why*: fine-tuned
  ICL-transformers can form decision boundaries that ordinary neural
  networks do not produce.
* **So pretrain on data that has complex boundaries, even if it is
  unrealistic.** They build a **forest dataset generator** — synthetic
  tables sampled from decision-tree/forest structures, explicitly
  described as unrealistic — and pretrain **TabForest** on it. It
  fine-tunes better the more complex the pretraining data, and beats
  TabPFN on some real datasets after fine-tuning *despite worse zero-shot
  performance*, precisely because the prior is unrealistic.
* **TabForestPFN** is the combination: pretrain on both the TabPFN
  generator and the forest generator, yielding good zero-shot *and*
  excellent fine-tuning performance.

**Strengths and limitations.** The zero-shot/fine-tuned trade-off is the
insight worth carrying: prior realism buys zero-shot quality, prior
*complexity* buys adaptability, and they are not the same axis. This
directly motivates Mitra's later claim that priors should be selected on
measured criteria rather than realism intuitions. Limitations: the copy
held here is an anonymous review version rather than a camera-ready, so
final numbers may differ; it is classification-only; and its gains are
demonstrated in the fine-tuning regime, which means they do not transfer
to a frozen-ICL deployment.

---

## 2024-11 — Helli et al. — Drift-Resilient TabPFN

**arXiv:** [2411.10634](https://arxiv.org/abs/2411.10634) ·
**PDF:** [open](papers/2024/11_Helli_et_al._Drift_Resilient_TabPFN_In_Context_Learning_Temporal_Distribution_Shifts_on_Tabular_Data_1.pdf)

**Where it fits.** TabPFN variant trained for distribution shift
— realistic temporal evolution of the data-generating process,
rather than i.i.d. test data.

**What it contains.** Modifies TabPFN's synthetic prior generator
to inject continuous distribution shifts between context rows
and query rows: covariate drift (input distribution moves over
time), prior drift (label-marginal moves), and concept drift
(conditional ``P(y|x)`` moves). A neural-network sub-component
parametrises the drift dynamics, and the sampler interleaves
"early" rows (context) with "late" rows (query) so the model
learns to extrapolate the drift function from the context.

The empirical message: a TabPFN trained with this drift-aware
prior generalises noticeably better when the test distribution
differs from training by a continuous shift. The vanilla TabPFN
prior is implicitly i.i.d.; under drift, it cannot recover.

---

## 2024-12 — Hoo et al. — TabPFN Outperforms Specialized Time Series Forecasting Models

**Venue:** NeurIPS 2024 Workshop on Time Series in the Age of Large
Models (the early version of what became
[arXiv:2501.02945](https://arxiv.org/abs/2501.02945), expanded into
the 2026 "From Tables to Time" paper below) ·
**PDF:** [open](papers/2024/12_Hoo_et_al._The_Tabular_Foundation_Model_TabPFN_Outperforms_Specialized_Time_Series_Forecasting_Models_Based_on.pdf)

**Where it fits.** Application paper rather than a method paper.
Shows that a frozen TabPFN matches state-of-the-art time-series
*foundation models* when forecasting is reframed as tabular
regression on timestamp-derived features.

**What it contains.** Pipeline (TabPFN-TS): take a univariate time
series, derive features **directly from the timestamps only** — a
running index plus sine/cosine-encoded calendar components; lagged
and rolling-window features are *deliberately excluded* (they
conflict with non-autoregressive multi-step prediction) — and feed
each (features → value) pair to the TabPFN regressor, predicting the
whole horizon in one pass. Evaluated on 24 of the 29 datasets of the
AutoGluon-TS benchmark: despite only 11M parameters and zero
time-series pretraining, TabPFN-TS outperforms Chronos-Mini and
matches or slightly beats Chronos-Large (65× more parameters).
Grouping by Chronos's own in-domain/zero-shot split shows Chronos
wins where test sets overlap its pretraining corpus, while TabPFN-TS
wins decisively on the 17 truly zero-shot datasets.

The narrative is that TabPFN's synthetic prior — free of any real
time-series pretraining, hence of contamination — transfers to
forecasting through feature engineering alone, where dedicated TS
foundation models rely on having seen similar series.

---

## 2024-12 — Feuer et al. — TuneTables

**Venue:** NeurIPS 2024 · NYU / U. Freiburg / U. Maryland / Abacus.AI ·
[DOI 10.52202/079017-2654](https://doi.org/10.52202/079017-2654) ·
arXiv [2402.11137](https://arxiv.org/abs/2402.11137) ·
**PDF:** [open](papers/2024/12_Feuer_et_al._TuneTables_Context_Optimization_for_Scalable_Prior_Data_Fitted_Networks.pdf)

**Where it fits.** The paper that defined the *context-optimisation*
branch of TFM adaptation, and the specific piece of prior art Rubachev
2025 later argued against. Where LoCalPFN localises the context by
retrieval and Real-TabPFN changes the weights, TuneTables changes what
the context *is* — making it the third distinct answer to "how do you
adapt a frozen PFN?".

**What it contains.** The problem is stated bluntly: TabPFN performs very
well on small tables but is not designed to predict for datasets larger
than ~1000 rows, and that ceiling blocks adoption. TuneTables lifts it by
**compressing a large dataset into a smaller learned context** — a
parameter-efficient fine-tuning strategy in which the context itself is
optimised rather than the network, the tabular analogue of prompt tuning.

The evaluation is unusually broad for the era: **nineteen algorithms
across 98 datasets**, where TuneTables achieves the **best average
performance**, outperforming boosted trees including CatBoost, while
**optimising fewer than 5% of TabPFN's parameters**. Two secondary
results widen its relevance: the learned context can be read as an
**interpretability tool**, and because the context is optimised against
an objective, it can be optimised against a **fairness objective** to
mitigate bias — a mechanism entirely different from FairPFN's
prior-level approach to the same goal. Code and raw results are open.

**Strengths and limitations.** The efficiency argument is strong (a
sub-5%-parameter method beating tuned CatBoost), the evaluation is wide,
and the fairness-by-context-optimisation idea is genuinely novel — it
makes the context a place where constraints can be imposed, which no
other paper here exploits. The limitations are what the later literature
seized on: it targets TabPFN **v1**, whose row ceiling v2 raised
architecturally, so part of the motivation evaporated; and Rubachev 2025
found that for v2 the "use parameter-efficient methods to avoid
destroying the prior" premise does not hold — full fine-tuning matches
PEFT variants while converging faster. Classification only.

---

## 2024-12 — Thomas et al. — LoCalPFN

**Venue:** NeurIPS 2024 · Layer 6 AI, Toronto ·
[DOI 10.52202/079017-3442](https://doi.org/10.52202/079017-3442) ·
**PDF:** [open](papers/2024/12_Thomas_et_al._Retrieval_Fine_Tuning_for_In_Context_Tabular_Models.pdf)

**Where it fits.** The retrieval branch of the adaptation literature, and
— read alongside [Nagler 2023](#nagler-theory)
— arguably the empirical answer to his localisation gap. Same lab as
TabDPT, whose FAISS-retrieved contexts are the successor idea.

**What it contains.** The diagnosis is that in-context learning had shown
promise on small tables but failed to scale to large, complex ones. The
fix combines two mechanisms that each address one half of the problem:

* **Retrieval** — instead of passing a global sample as context, collect
  the **k nearest neighbours of the query** and pass that local subset,
  so the model is conditioned on the region of feature space it is being
  asked about.
* **Fine-tuning on the retrieved context** — task-specific fine-tuning is
  then performed with those neighbours in context, jointly rather than as
  a post-hoc step.

Applied to TabPFN, this yields the **locally-calibrated PFN (LoCalPFN)**,
evaluated on the **95 TabZilla datasets** curated from OpenML, where it
sets a new state of the art — including against *tuned* tree-based
models — and shows a large gain over the base in-context model.

**Strengths and limitations.** The retrieve-then-fine-tune pairing is
theoretically well-motivated (it is localisation, which Nagler shows is
what the bias term needs) and is the largest single reported jump over
base TabPFN in the v1 era. The costs are real: retrieval makes inference
per-query rather than per-dataset, which complicates deployment and
assumes exchangeable rows; the method is classification-focused; and it
is built on TabPFN v1, so the scaling ceilings it lifts were partly
lifted by v2 architecturally instead.

---

<a id="tabpfn-v2-nature"></a>

## 2025-01 — Hollmann et al. — Accurate predictions on small data with a tabular foundation model

**Journal:** *Nature*, 2025 ·
**PDF:** [open](papers/2025/01_Hollmann_et_al._Accurate_predictions_on_small_data_with_a_tabular_foundation_model.pdf)

**Where it fits.** The TabPFNv2 paper. Production-grade release
that 100×s the scaling limits of v1 and ships in *Nature*.

**What it contains.** A re-architected v2 with alternating
sample-attention / feature-attention layers, scaling to
~10 000 rows × 500 features (orders of magnitude more than v1).
Headline ingredients:

* **Synthetic prior expansion.** Far broader and deeper than v1's
  prior; covers richer noise distributions, more diverse SCMs,
  and inputs with realistic categorical / numerical mixes.
* **Architecture.** Stacked transformer with two attention
  patterns interleaved per layer: "sample attention" treating
  each row as a token, and "feature attention" treating each
  column as a token. The interleaving lets the model reason
  about both row-level patterns (similarity, density) and
  column-level patterns (interactions, redundancy) in one pass.
* **NaN handling.** Built into the encoder via
  ``NanHandlingEncoderStep`` — explicit indicator features plus
  learned default replacements. Categorical handling via an
  internal ``OrdinalEncoder`` fitted at ``.fit(X, y)`` time.
* **Inference-time ensemble.** A pool of preprocessing
  configurations (``PowerTransformer``, ``QuantileTransformer``,
  ``RobustScaler``, ``SquashingScaler``, ``"none"``); each
  estimator in the ensemble cycles through one configuration,
  yielding diverse predictions that are averaged at inference.
* **Headline results.** Beats AutoGluon, CatBoost, XGBoost on
  the TabArena benchmark across the full ≤ 10k-row range.

---

## 2025-02 — Liu and Ye — TabPFN Unleashed

**arXiv:** [2502.02527](https://arxiv.org/abs/2502.02527) ·
**PDF:** [open](papers/2025/02_Liu_and_Ye_TabPFN_Unleashed_A_Scalable_and_Effective_Solution_to_Tabular_Classification_Problems.pdf)

**Where it fits.** Adaptation method for TabPFN. Re-frames TabPFN's
weaknesses through a formal **bias–variance decomposition** of its
generalisation error, then proposes a method (**BETA**: Bagging
and Encoder-based Fine-tuning for TabPFN Adaptation) that attacks
both sides simultaneously.

**What it contains.** The authors observe that previous TabPFN-
improvement papers each address either bias or variance, never
both — and the resulting methods leave performance on the table.
BETA combines two complementary mechanisms.

* **Bias reduction via a lightweight learned encoder.** A small
  parameter-efficient adapter sits between the raw features and
  TabPFN's internal embedding, mapping datasets of arbitrary
  dimensionality into multiple fixed-dimensional latent
  representations. This both addresses TabPFN's ~500-feature soft
  cap and lets the model adapt to the downstream task during
  fine-tuning.
* **Variance reduction via Batch Ensemble plus bootstrapped
  sampling.** Multiple lightweight encoders run in parallel with
  parameter sharing (à la Wen 2020 / Gorishniy 2025), each fed a
  bootstrap-sampled context. Their predictions are averaged,
  smoothing out idiosyncrasies of any single sampled context set.

The method also integrates with Error-Correcting Output Codes
(ECOC) to handle multiclass tasks with > 10 classes (which v2
struggles with). Evaluated on 186 TALENT classification
datasets where BETA either outperforms or matches state of the
art while remaining computationally lightweight.

---

## 2025-05 — Müller et al. — Position: The Future of Bayesian Prediction Is Prior-Fitted

**arXiv:** [2505.23947](https://arxiv.org/abs/2505.23947) ·
**PDF:** [open](papers/2025/05_Muller_et_al._Position_The_Future_of_Bayesian_Prediction_Is_Prior_Fitted.pdf)

**Where it fits.** Position paper / manifesto from the original
PFN authors.

**What it contains.** Argues that PFNs are the natural successor
to MCMC and variational Bayes for *predictive* Bayesian inference
(as opposed to posterior estimation per se). The argument:

* Inference algorithms for non-conjugate priors are slow and
  brittle.
* PFNs amortise inference into one forward pass, with arbitrary
  user-specified priors.
* The remaining bottlenecks are (a) prior design and (b) corpora
  of real data to validate against synthetic priors — *not*
  inference algorithms.

The paper sketches research directions: prior-design libraries,
PFN-as-baseline for new probabilistic methods, and a unified
benchmark across regression / classification / forecasting / BO.

---

## 2025-05 — Qu et al. — TabICL

**arXiv:** [2502.05564](https://arxiv.org/abs/2502.05564) ·
**PDF:** [open](papers/2025/05_Qu_et_al._TabICL_A_Tabular_Foundation_Model_for_In_Context_Learning_on_Large_Data.pdf)

**Where it fits.** Direct competitor to TabPFN. Different
architectural approach; scales to ~500 k-row tables natively.

**What it contains.** TabICL ("Tabular In-Context Learning")
adopts a **two-stage** architecture instead of TabPFNv2's flat
column-then-row alternation. First, each row is collapsed into a
single dense vector via a column-then-row attention block:
distribution-aware column-wise embedding (a Set-Transformer-style
operation that treats each column as a permutation-invariant set
of cell values, enabling cross-table transferability), then
within-row attention to model feature interactions, then a
[CLS]-token aggregation that produces a fixed-dimensional row
embedding. Second, ICL runs over these row embeddings — collapsing
the column dimension *before* in-context learning sidesteps
TabPFNv2's `O(n²m + nm²)` cost.

The pretraining adds a tree-based synthetic prior (decision-tree
ensembles) on top of the standard SCM prior to inject GBDT-flavoured
inductive biases, plus curriculum learning that scales the
pretraining dataset size from 1k → 60k rows. To handle > 10 classes
(the pretraining limit) the model uses hierarchical classification.
Empirically, on the TALENT benchmark's 53 large datasets above 10 k
rows TabICL
**surpasses both TabPFNv2 and CatBoost**, while on smaller datasets
it matches TabPFNv2 at up to 10× faster inference.

---

## 2025-06 — Robertson et al. — FairPFN

**arXiv:** [2506.07049](https://arxiv.org/abs/2506.07049) ·
**PDF:** [open](papers/2025/06_Robertson_et_al._FairPFN_A_Tabular_Foundation_Model_for_Causal_Fairness.pdf)

**Where it fits.** Causal-PFN sibling of Do-PFN, this time aimed
at the **causal-fairness** problem rather than treatment-effect
estimation. Addresses the limitation that current causal-fairness
frameworks require the user to specify the correct causal model —
a tall ask in practice and a source of "fairwashing" when the
specified graph is wrong.

**What it contains.** Pretraining recipe:

* **Synthetic causal-fairness data prior.** Sparse MLPs
  represent SCMs whose root nodes include exogenous protected
  attributes (binary: race / gender / age). For each SCM, the
  paper samples both a *biased* dataset (with the protected
  attribute's full causal influence) and a *fair* counterpart
  obtained by removing the outgoing edges of the protected
  attribute — i.e. by simulating the counterfactual world in
  which the protected attribute had no causal influence on the
  outcome.
* **Training objective.** The transformer sees the biased
  observational dataset as context and is trained to predict
  the *fair* outcomes from the counterfactual world. Loss is
  computed against the fair targets, so the network learns to
  internally identify and remove the causal effect of the
  protected attribute.
* **At inference time**, FairPFN takes only the biased
  observational data and produces fairer predictions, integrating
  over the simplest causal explanations consistent with the
  observed bias. **No user-specified causal graph is needed.**

The paper demonstrates strong performance on hand-crafted SCMs
and several real-world fairness benchmarks (Adult, COMPAS,
German Credit, Law School Admissions), beating robust baselines
across most settings.

---

<a id="on-finetuning"></a>

## 2025-06 — Rubachev et al. — On Finetuning Tabular Foundation Models

**arXiv:** [2506.08982](https://arxiv.org/abs/2506.08982) ·
**PDF:** [open](papers/2025/06_Rubachev_et_al._On_Finetuning_Tabular_Foundation_Models_1.pdf)

**Where it fits.** Empirical study of finetuning tabular FMs on
downstream datasets. The closest published reference for
single-dataset gradient-adaptation hyperparameters.

**What it contains.** A controlled study of **TabPFNv2** adaptation:
full gradient updates, LoRA, last-layer tuning, LayerNorm/head/embedding
tuning, and numerical-feature embeddings, across classification and
regression datasets. Headline findings:

* **Full finetuning is the practical default.** It performs similarly
  to the partial/PEFT alternatives while converging faster; the paper
  does not support a blanket claim that LoRA recovers a fixed percentage
  of the gain.
* **Learning rate is tuned per dataset** on ten log-spaced values from
  5e-6 to 5e-4. Each step scores 1 024 prediction objects while the
  remaining rows form the context.
* **Early stopping** evaluates the validation subset every ten gradient
  steps and stops after 16 non-improving evaluations.
* **Mechanism.** Finetuning sharpens the alignment between test-query
  and context-key representations, improving TabPFNv2's retrieval-like
  weighting of relevant in-context examples.

The paper also identifies pathological cases where finetuning
*hurts* (extremely small datasets, datasets with severe label
noise) and proposes early-stopping protocols to detect them.

The local ``repositories/On Finetuning Tabular Foundation Models.txt``
dump belongs to this Rubachev study. It is **not** a Real-TabPFN code
release. The studies answer complementary questions: Rubachev adapts one
target dataset at a time; Garg continues pretraining one model across a
71-table corpus.

---

## 2025-06 — Ye et al. — A Closer Look at TabPFN v2

**arXiv:** [2502.17361](https://arxiv.org/abs/2502.17361) ·
**PDF:** [open](papers/2025/06_Ye_et_al._A_Closer_Look_at_TabPFN_v2_Understanding_Its_Strengths_and_Extending_Its_Capabilities.pdf)

**Where it fits.** Mechanistic analysis of TabPFNv2 (rather than
a new architecture). Asks two questions: *how* does v2 cope so
well with heterogeneous tabular data, and *how* can its known
limits — 10 000 samples × 500 features × 10 classes — be lifted
without retraining? Three concrete findings.

**What it contains.**

1. **TabPFN v2 internalises attribute-token learning.** Unlike
   prior tabular methods that rely on word-vector–style attribute
   semantics or learn dataset-specific attribute tokens, v2 uses
   **randomly resampled attribute tokens at every inference call**.
   The paper's analysis shows that v2 still consistently infers
   attribute relationships *through ICL itself* — effectively
   integrating "what this column means" learning into the same
   forward pass that produces predictions. This is what lets v2
   transfer across datasets with different schemas and
   dimensionalities without per-dataset adaptation.
2. **TabPFN v2 can be repurposed as a feature extractor.** Using
   a leave-one-fold-out strategy that aligns training and test
   embeddings, the authors show v2 maps tabular instances into a
   *near-linearly-separable* embedding space. Training a plain
   linear model on those embeddings recovers most of v2's
   accuracy — meaning v2 is implicitly learning a strong general-
   purpose tabular representation, not just a classifier.
3. **Test-time divide-and-conquer mitigates the
   10 k × 500 × 10 limits.** Instead of retraining v2 on bigger
   data, the paper proposes post-hoc strategies analogous to LLM
   test-time scaling: hierarchical class decomposition for
   many-class tasks, feature-subset chunking for wide tables,
   bootstrap-context aggregation for large-N data. Empirical
   gains across all three limit regimes.

Several of these patches were rolled into the official Prior Labs
package as non-default v2.5 specialist checkpoints —
``_low-skew``, ``_quantiles``, ``_large-features-L``,
``_large-features-XL``, ``_large-samples`` — per the catalogue
in ``repositories/Huggingface TabPFN.txt``.

---

<a id="real-tabpfn"></a>

## 2025-07 — Garg et al. — Real-TabPFN

**arXiv:** [2507.03971](https://arxiv.org/abs/2507.03971) ·
**PDF:** [open](papers/2025/07_Garg_et_al._Real_TabPFN_Improving_Tabular_Foundation_Models_via_Continued_Pre_training_With_Real_World_Data.pdf)

**Where it fits.** The reference recipe for **corpus-level continued
pretraining**: take the released synthetic-only TabPFNv2 checkpoint and
continue pretraining it on a curated set of real-world tables from
OpenML and Kaggle. Any project that wants to specialise a TFM to a
domain by feeding it real in-domain tables is replicating this paper's
methodology with a different corpus.

**What it contains.**

* **Method.** Take the synthetic-only TabPFNv2 checkpoint and
  continue pretraining on a hand-curated corpus of 71 datasets
  (≥ 10 000 rows each, mixture of OpenML and Kaggle).
  *Minimal* preprocessing: ``OrdinalEncoder`` for categoricals
  (``num_policy`` noisy-quantile, ``cat_policy`` ordinal in their
  code), and if the target has more than 10 classes, retain the
  nine most common and merge the remainder into a tenth "other".
  No imputation, no scaling beyond what TabPFN does internally.
* **The actual Real-TabPFN recipe** (stated directly in Garg et al.):
  full-model continued pretraining with **AdamW, LR 3e-7, linear
  warmup followed by cosine annealing, and L2-SP λ=0.003** toward
  the synthetic checkpoint. It runs for **20 000 steps**, batch size
  one table, samples up to 20 000 rows / 400 000 cells, and splits
  each table 60% context / 40% query. The paper does not report
  AdamW's weight-decay value. At each step the table is drawn from a
  **71-dataset corpus**; batch size one does not make this a
  single-dataset finetuning study.
* **Do not conflate this with Rubachev et al.** Their separate paper,
  *On Finetuning Tabular Foundation Models*, contains the 342
  single-dataset runs, 5e-6…5e-4 tuned LR grid, patience-16 early
  stopping, constant LR, zero weight decay, and PEFT/LoRA ablations.
  That repository dump is useful as a second reference, but it is not
  the Real-TabPFN source release and its recipe is not Garg's recipe.
* **Data contamination protocol** (their §3) — a multi-tier
  filter: (1) only datasets > 10k samples (every evaluation
  dataset is smaller, so size alone separates pretrain from eval);
  (2) cross-reference IDs / names / shapes;
  (3) cross-reference column names;
  (4) row hashes;
  (5) column hashes;
  (6) manual metadata inspection.
  Any project reusing this protocol should reimplement all six tiers;
  natural extras are a rounded-row hash, subset detection, and fuzzy
  column-name matching.
* **Headline result.** On 29 datasets from the OpenML AutoML
  Benchmark, Real-TabPFN improves normalised ROC-AUC by +0.022
  vs. default TabPFNv2 (Wilcoxon signed-rank ``p = 0.0045``).
  The Wilcoxon test confirms this is a per-dataset improvement,
  not just an average bump driven by a few outliers.
* **Ablations.** OpenML alone: +0.019. Kaggle alone: +0.015.
  Union: +0.022 — heterogeneous sources are complementary.
  CommonCrawl as a continued-pretraining corpus *hurts*
  performance (the average dataset there is only ~100 rows ×
  7 features — too small to give TabPFN useful signal).
  GitTables (avg ~1000 rows × 9 features) helps, but less than
  OpenML+Kaggle (avg 10k–100k rows × 10s of features).
* **Context-size scaling.** Continued-pretraining gains grow with
  the context size used during continued pretraining: 2k → 20k
  context yields a monotonic improvement curve (Figure 4 in
  the paper).

**Attribution warning.** There is **no public Real-TabPFN code release**.
The local ``repositories/On Finetuning Tabular Foundation Models.txt``
dump belongs to **Rubachev et al.**, not to Garg et al. — do not read
that repository's hyperparameters as Garg's recipe. A second, genuinely
official reference point is the Prior Labs finetuning wrapper shipped in
the package (``FinetunedTabPFNClassifier``: 30 epochs, LR 2e-5,
``n_estimators_finetune`` 2; ``FinetunedTabPFNRegressor``: 30 epochs,
LR 1e-5, ``n_estimators_finetune`` 8,
``n_finetune_ctx_plus_query_samples`` 20 000), but that is
*single-dataset* finetuning, not corpus continued pretraining.

---

## 2025-10 — Zhang et al. — Mitra: Mixed Synthetic Priors

**arXiv:** [2510.21204](https://arxiv.org/abs/2510.21204) ·
**PDF:** [open](papers/2025/10_Zhang_et_al._Mitra_Mixed_Synthetic_Priors_for_Enhancing_Tabular_Foundation_Models.pdf)

**Where it fits.** Alternative pretraining recipe from Amazon /
AutoGluon team. Argues that the right way to improve TFMs is *not*
to add architectural complexity but to **design better synthetic
priors** — and proposes a principled framework for mixing them.
Pretrained model is open-source on HuggingFace as
``autogluon/mitra-classifier`` and ``autogluon/mitra-regressor``.

**What it contains.** The paper formalises three properties a good
synthetic prior should have, and operationalises each as a
measurable score:

1. **Standalone performance** — a TFM pretrained *only* on this
   prior should already do well on real data.
2. **Diversity** — a TFM pretrained on this prior should not
   easily overfit to its own distribution (i.e. the prior covers
   a wide range of generative mechanisms).
3. **Distinctiveness within a mixture** — data sampled from this
   prior should be hard for TFMs trained on *other* priors to
   predict, meaning it adds something the other priors miss.

The first is captured by a per-prior performance vector P; the
latter two by a "Generalisability Matrix" G with diagonal entries
measuring overfitting and off-diagonal entries measuring inter-
prior overlap. Using these criteria the authors select a final
mixture of **SCMs + tree-based priors** (gradient boosting,
random forest, decision tree, extra-tree). SCMs deliver
standalone performance and diversity; tree-based priors are
distinctive (TFMs pretrained on SCMs alone struggle on TBP-
generated data, so adding TBPs covers ground SCMs miss).

The mixture is model-agnostic: it improves both flat row-attention
architectures (à la TabPFN) and 2D cell-attention architectures.
**Mitra outperforms TabPFNv2 and TabICL on both classification and
regression benchmarks**, with better sample efficiency.

---

## 2025-11 — Robertson et al. — Do-PFN

**arXiv:** [2506.06039](https://arxiv.org/abs/2506.06039) ·
**PDF:** [open](papers/2025/11_Robertson_et_al._Do_PFN_In_Context_Learning_for_Causal_Effect_Estimation.pdf)

**Where it fits.** First PFN published for causal-effect
estimation. Predates the unified CausalFM framework (Ma 2026)
by ~6 months and focuses specifically on **conditional
interventional distributions** — the answer to "what would the
outcome distribution look like under an intervention that sets
treatment t?", given only observational data.

**What it contains.** Pretraining recipe:

* **Sample millions of SCMs.** Each SCM has explicit treatment
  variables, outcome variables, and confounders. Importantly,
  the prior covers a wide variety of causal structures including
  cases where unconfoundedness *fails*.
* **For each SCM, sample two datasets simultaneously**: one
  observational (no interventions) and one interventional (forced
  ``do(T = t)``). The transformer is given the *observational*
  dataset as context and is trained to predict the *interventional*
  outcomes — meta-learning the act of causal inference itself.
* **At inference time**, the model sees only an observational
  dataset and a query intervention; the network outputs an
  estimate of the causal effect with calibrated uncertainty.

The crucial property: Do-PFN does **not** require the user to
specify the causal graph, and does **not** rely on the
unconfoundedness assumption that classical methods (IPW, DR,
causal forests) need. The breadth of the SCM-prior means the
model has, in expectation, "seen" enough confounded cases during
training that it auto-corrects.

Beats classical IPW and Doubly Robust estimators on synthetic and
semi-synthetic causal-inference benchmarks.

---

## 2025-11 — Zhang et al. — TabPFN: One Model to Rule Them All

**arXiv:** [2505.20003](https://arxiv.org/abs/2505.20003) ·
**PDF:** [open](papers/2025/11_Zhang_et_al._TabPFN_One_Model_to_Rule_Them_All.pdf)

**Where it fits.** A statistician's appraisal of TabPFNv2,
written for a *Statistical Science*-flavoured audience rather
than an ICML one. Provides a careful re-derivation of how
TabPFN works as **approximate Bayesian inference**, and uses
that lens to identify several application domains in which
out-of-the-box TabPFN matches or beats domain-specific
state-of-the-art methods.

**What it contains.** Three concrete applications evaluated:

* **Semi-supervised parameter estimation** — using TabPFN with
  a small labelled set plus unlabelled rows as context. Beats
  specialised semi-supervised baselines on several benchmarks.
* **Prediction under covariate shift** — TabPFN automatically
  handles a moderate degree of distribution shift through its
  in-context calibration, with no covariate-shift-specific
  modifications. Competitive with importance-weighting and
  domain-adaptation baselines.
* **Heterogeneous treatment-effect estimation** — TabPFN
  predictions plug into S-learner / T-learner causal-inference
  frameworks and are competitive with Causal Forest, X-learner,
  and DR-learner.

A key theoretical observation: **TabPFN can adapt to both
nonparametric *and* parametric structure simultaneously**.
Sometimes outperforms LASSO even when the data is genuinely
sparse-linear (i.e. when LASSO's modelling assumptions are
correctly specified) — because TabPFN's implicit prior over
SCMs already covers sparse-linear data, plus everything else.
This blurs the classical bias-variance trade-off and makes
TabPFN attractive as a *default* tabular regressor / classifier
even in regimes where simple parametric models are usually
preferred.

---

## 2025-11 — Bouadi et al. — Orion-MSP

**arXiv:** [2511.02818](https://arxiv.org/abs/2511.02818) · Lexsi Labs
(India / France) ·
**PDF:** [open](papers/2025/11_Bouadi_et_al._Orion_MSP_Multi_Scale_Sparse_Attention_for_Tabular_In_Context_Learning.pdf)

**Where it fits.** One of the two Orion architectures from Lexsi Labs —
the models benchmarked by that lab's own TabTune library and
fine-tuning study, both of which this library already holds. Holding the
tooling papers without the model papers left an obvious gap.

**What it contains.** The paper names three limitations of TabPFN- and
TabICL-style architectures and addresses each:

1. **Single-scale feature processing** overlooks hierarchical
   dependencies → **multi-scale processing** to capture feature
   interactions at several granularities.
2. **Dense attention scales quadratically in table width** →
   **block-sparse attention** combining windowed, global and random
   patterns, keeping long-range connectivity at lower cost.
3. **Strictly sequential components** prevent iterative refinement →
   a **Perceiver-style memory** allowing safe bidirectional information
   flow between components, so the column and row stages can inform each
   other instead of running once in sequence.

The reported result is matching or surpassing state-of-the-art while
scaling to high-dimensional tables. Weights and code are public.

**Strengths and limitations.** The bidirectional-memory point is a
genuine architectural observation: the three-stage consensus design
(column → row → ICL) is strictly feed-forward, and there is no principled
reason it should be. The limitations are those of the whole Orion line:
evaluation is by the authors of the benchmark library used to evaluate
it — Lexsi Labs' own TabTune and fine-tuning study place Orion models at
or near the top of their leaderboards — so independent replication
matters more here than usual, and no calibration analysis is reported.

---

## 2025-12 — Pfefferle et al. — nanoTabPFN

**arXiv:** [2511.03634](https://arxiv.org/abs/2511.03634) ·
**PDF:** [open](papers/2025/12_Pfefferle_et_al._nanoTabPFN_A_Lightweight_and_Educational_Reimplementation_of_TabPFN.pdf)

**Where it fits.** Educational reference implementation —
TabPFN distilled to under 500 lines of clear PyTorch.

**What it contains.** A complete working PFN training loop
(synthetic prior dump, model, optimiser, training loop, eval),
designed to be readable end-to-end. Specifically:

* A synthetic-data HDF5 prior dump (300k×150×5 in the demo).
* The TabPFN-style model — alternating attention between samples
  and between features, plus a target-embedding head.
* A ``train()`` function that iterates over the prior dump,
  computes cross-entropy on held-out query labels, and applies
  AdamW with gradient-norm clipping.
* A small inference wrapper that exposes a sklearn-style
  ``fit`` / ``predict_proba`` interface.

The paper accompanies the code with an exposition of the PFN
recipe at a level appropriate for a graduate ML class.

---

## 2025-12 — Tanna et al. — TabTune

**arXiv:** [2511.02802](https://arxiv.org/abs/2511.02802) ·
**PDF:** [open](papers/2025/12_Tanna_et_al._TabTune_A_Unified_Library_for_Inference_and_Fine_Tuning_Tabular_Foundation_Models.pdf)

**Where it fits.** Software / benchmark paper from Lexsi Labs. A
unified, scikit-learn-compatible Python library that standardises
the entire workflow — inference, fine-tuning, evaluation — across
TabPFN, TabICL, ContextTab, OrionMSP, OrionBix, and other tabular
FMs.

**What it contains.** TabTune addresses four operational frictions
that have been slowing TFM adoption in practice:

* **Diverse preprocessing requirements** — each TFM expects its
  own data encoding (TabPFN wants numerically encoded categoricals
  consistent with its synthetic priors, TabICL wants set-transformer
  embeddings for categoricals, etc.). TabTune handles the per-model
  preprocessing internally.
* **Fragmented APIs and training protocols** — some models are
  zero-shot only, some support full SFT, some support PEFT
  (LoRA / prefix tuning). TabTune exposes a unified
  ``.fit()`` / ``.predict()`` / ``.evaluate()`` interface across
  all of them.
* **Evaluation gaps in deployment-relevant metrics** — beyond
  accuracy, the library ships built-in calibration (Expected
  Calibration Error, Maximum Calibration Error, Brier score) and
  fairness diagnostics (Statistical Parity Difference, Equalised
  Odds Difference, Equalised Opportunity Difference).
* **Model selection complexity** — a benchmarking module
  consistently ranks models on accuracy, calibration, fairness
  and resource efficiency on standard suites (TALENT, OpenML-CC18).

The library targets the "experimental bed" use-case: study how
zero-shot vs. PEFT vs. SFT trades off across calibration,
fairness, and compute, all under one harness.

---

## 2025-12 — Balazadeh Meresht et al. — CausalPFN

**Venue:** NeurIPS 2025 · University of Toronto / Vector Institute /
Layer 6 AI ·
**PDF:** [open](papers/2025/12_Balazadeh_Meresht_et_al._CausalPFN_Amortized_Causal_Effect_Estimation_via_In_Context_Learning.pdf)

**Where it fits.** The fourth member of the causal-PFN cluster in this
library, alongside Do-PFN, FairPFN and CausalFM — and the one the others
are measured against. CausalFM's own ablations report losing to
CausalPFN on ACIC2016, which makes holding it necessary to read that
comparison honestly.

**What it contains.** The problem framing is practical rather than
theoretical: dozens of specialised causal estimators exist, and
*choosing* one for a given dataset takes substantial manual effort and
domain expertise. CausalPFN amortises that choice. A single transformer
is trained once on a large library of **simulated data-generating
processes that satisfy ignorability**, and then infers causal effects for
new observational datasets out of the box — mapping raw observations
directly to effects with no task-specific adjustment, and supplying
**calibrated uncertainty** on Bayesian principles.

Evaluation covers heterogeneous and average treatment effect estimation
on **IHDP, Lalonde and ACIC** — 310 tasks in total — where it achieves
the best average rank by precision in estimating heterogeneous effects
while being much faster than EconML, deep-learning, BART and GRF
baselines. It is also competitive on real-world uplift-modelling tasks.

**Strengths and limitations.** The combination of best-average-rank,
order-of-magnitude speed, calibrated uncertainty, and released code makes
this the most deployable model in the causal-PFN group. The central
caveat is in its own construction: the prior assumes **ignorability**,
so unlike Do-PFN it does not target the unconfoundedness-violated regime,
and CausalFM's impossibility result argues that mixing identifiable and
non-identifiable settings in one prior is what degrades posteriors — a
theoretical objection CausalPFN's strong empirics do not settle. Its
benchmarks are also the standard semi-synthetic ones, which resemble the
simulated priors it trains on.

---

## 2025-12 — Arazi et al. — TabSTAR

**Venue:** NeurIPS 2025 · Technion — Israel Institute of Technology ·
**PDF:** [open](papers/2025/12_Arazi_et_al._TabSTAR_A_Tabular_Foundation_Model_for_Tabular_Data_with_Text_Fields.pdf)

**Where it fits.** The text-field branch of the TFM family, and now part
of the TabPFN lineage in a literal sense: its first author is a
co-author on the TabPFN-3 report, and TabPFN-3-Plus reports
state-of-the-art on the TabSTAR benchmark. Purucker's BeyondArena also
adopts that benchmark as one of its dataset sources.

**What it contains.** The critique of prior work is specific: methods
that bring language-model capability to tables mostly use **static,
target-agnostic** text representations — a column's text is embedded the
same way regardless of what is being predicted — which limits how useful
the embedding can be. TabSTAR instead:

* **unfreezes a pretrained text encoder**, so textual representations
  adapt during tabular pretraining rather than being fixed features; and
* **takes target tokens as input**, giving the model the context it needs
  to learn *task-specific* embeddings — the "semantically target-aware
  representations" of the name.

The architecture has **no dataset-specific parameters**, which is what
makes transfer across datasets possible at all. It reports
state-of-the-art on medium and large classification datasets with text
features, and — the forward-looking result — its **pretraining exhibits
scaling laws in the number of datasets**, implying the approach improves
with more pretraining corpora rather than saturating.

**Strengths and limitations.** The target-aware embedding idea is a real
advance over static text features, and dataset-count scaling laws are the
kind of evidence the field mostly lacks. Limitations: classification with
text features is a narrower setting than the general tabular problem, so
it is not a drop-in TabPFN competitor; unfreezing a text encoder makes it
far heavier than table-native models; and the reliance on natural-language
column content limits transfer to numeric-only domains.

---

## 2025-12 — Spinaci et al. — ConTextTab

**Venue:** NeurIPS 2025 (spotlight) · SAP France / SAP SE ·
**PDF:** [open](papers/2025/12_Spinaci_et_al._ConTextTab_A_Semantics_Aware_Tabular_In_Context_Learner.pdf)

**Where it fits.** The synthesis of the two halves of the tabular-ICL
field, and the empirical companion to SAP's own position paper on
grounding (Klein & Hoffart 2026, also held here). It sits exactly between
the table-native models and the LLM-based ones.

**What it contains.** The framing is a clean statement of a real
trade-off. Table-native ICL architectures (TabPFN, TabICL) are
architecturally efficient and well-adapted to table structure, but
training *exclusively on synthetic data* means they cannot exploit the
semantics and world knowledge that real tables carry — a column called
`country` is just a categorical to them. LLM-based tabular learners
(TabuLa-8B) have the semantics and world knowledge but can only ingest a
small context because of architectural limits.

ConTextTab keeps the table-native framework and adds semantics two ways:
**specialised embeddings per data modality** (text, dates, numbers rather
than one generic encoder) and **training on large-scale real-world
tabular data** instead of synthetic tables. It is competitive with SOTA
across a broad set of benchmarks and **sets a new standard on the
semantically rich CARTE benchmark**, particularly in the low-data regime.
Code and checkpoints are released.

**Strengths and limitations.** This is the strongest evidence that column
*semantics* are a real source of signal that the synthetic-prior line
discards by construction — a different argument from Real-TabPFN's, which
is about distributional realism rather than meaning. The obvious
limitation is the mirror of the synthetic camp's: training on real tables
raises contamination questions, and the gains concentrate where columns
carry natural-language meaning, which is exactly where a purely numeric
domain gains least.

---

## 2026-01 — Hoo et al. — From Tables to Time

**arXiv:** [2501.02945](https://arxiv.org/abs/2501.02945) ·
**PDF:** [open](papers/2026/01_Hoo_et_al._From_Tables_to_Time_Extending_TabPFN_v2_to_Time_Series_Forecasting.pdf)

**Where it fits.** A more thorough version of the 2024 forecasting
paper by the same authors. Reframes time-series forecasting as a
*tabular regression problem* and shows that the **unmodified**
pretrained TabPFN-v2 — paired with a lightweight temporal
featurisation — beats specialised time-series foundation models.
Released as **TabPFN-TS** at github.com/PriorLabs/tabpfn-time-series.

**What it contains.** The construction is simple but the result
is striking. Each time step becomes one row in a tabular
regression problem: features encode time progression
(running index), multi-scale seasonality (year, day-of-week,
hour-of-day, …), plus optional covariates (weather, economic
indicators, control inputs). The target is the observed value at
that time step. Forecasting then reduces to predicting future
rows whose temporal features are known in advance — and TabPFN-v2
predicts the entire forecast horizon **in one forward pass**.

Headline results:

* On the **fev-bench** benchmark (covariate-informed forecasting),
  TabPFN-TS achieves **state-of-the-art** at 11 M parameters.
* On **GIFT-Eval** (univariate forecasting), it is competitive
  with Chronos-Mini and **matches Chronos-Large** despite having
  ~65× fewer parameters.
* No time-series–specific pretraining. No fine-tuning. The
  pretrained TabPFN-v2 weights are used as-is.

The paper also includes mechanistic studies: how the model
exploits temporal structure (all features are timestamp-derived —
running index, calendar sin/cos encodings, FFT-selected seasonal
components; lagged/rolling features are deliberately excluded as
incompatible with non-autoregressive multi-step prediction), how
forecasting quality
varies across tabular backbones (TabPFN-v2 ≫ TabPFNv1 ≫ tree
ensembles given the same featurisation), and how the model
handles distribution shifts at long horizons.

---

## 2026-01 — Klein and Hoffart — Position: Foundation Models for Tabular Data within Systemic Contexts Need Grounding

**arXiv:** [2505.19825](https://arxiv.org/abs/2505.19825) ·
**PDF:** [open](papers/2026/01_Klein_and_Hoffart_Position_Foundation_Models_for_Tabular_Data_within_Systemic_Contexts_Need_Grounding.pdf)

**Where it fits.** A *contrarian* position paper from SAP that
challenges the entire "isolated tables" framing of current tabular
foundation models — TabPFN, TabICL, TabDPT, Mitra all included.
Argues these models trained on individual tables (or even on
schema-level multi-table relations via GNNs) fundamentally miss
the **operational context** — the procedural logic, declarative
rules, and domain knowledge — that gives tabular data its meaning
in real-world enterprise systems.

**What it contains.**

* **The diagnosis.** Current tabular FMs assume "information
  completeness within tables" — that the information needed to
  predict an outcome is in the rows themselves. In an enterprise
  setting that's almost never true. A row like
  `(amount=4999, ..., approved=True)` next to
  `(amount=5000, ..., approved=False)` is fully explained by a
  rule somewhere in the codebase: ``if amount >= 5000:
  require_manager_approval()``. A purely statistical model trained
  on historical decisions might learn an *approximate* threshold
  near $4 800 and misclassify edge cases — while the actual rule
  is a hard `>=` boundary, sitting in source code that the model
  never sees.
* **The proposal: SLT + FMSLT.** *Semantically Linked Tables* —
  the relational data plus three layers of explicitly-modelled
  context: declarative business knowledge (data models, business
  objects, business rules, process models), procedural knowledge
  (agent logic in natural language, application logic as code),
  and world knowledge (general business concepts, types,
  relationships, implicit assumptions). A *Foundation Model for
  SLT* (FMSLT) is then a new model class that ingests **code as
  logic**, not as text — distinguishing "branching paths
  define decision boundaries" from mere token co-occurrence.
* **Two-phase training recipe.** (i) Pre-train on open-source
  code-data pairs and synthetic systems to learn business-logic
  mechanics. (ii) Apply zero-shot to proprietary enterprise data
  via in-context retrieval of the relevant code/rules.
* **Operational Turing Test.** A new benchmark proposed in the
  paper: an FMSLT passes if, given an enterprise dataset, it can
  predict outcomes that depend on rules expressed only in code, at
  parity with a system that has access to the explicit rule
  engine. The paper reviews recent enterprise-agent benchmarks
  (WorkArena++, TheAgentCompany, CRMArena-Pro, AgentArch, MLGym,
  COMPASS) and shows current LLM-based agents top out at 30–35%
  on tasks requiring implicit business knowledge — motivating the
  need for explicit operational grounding.

---

## 2026-01 — Ma et al. — TabDPT

**arXiv:** [2410.18164](https://arxiv.org/abs/2410.18164) ·
**PDF:** [open](papers/2026/01_Ma_et_al._TabDPT_Scaling_Tabular_Foundation_Models_on_Real_Data.pdf)

**Where it fits.** From Layer 6 AI (Toronto). Pretrained at the
**opposite extreme of the synthetic-vs-real spectrum** from
TabPFN: a transformer pretrained on *real* OpenML data only, with
no synthetic prior. Open weights on
[HuggingFace](https://huggingface.co/Layer6/TabDPT) and
inference + training code on
[GitHub](https://github.com/layer6ai-labs/TabDPT-inference).

**What it contains.** Two methodological pillars:

* **ICL retrieval + self-supervised learning.** At each training
  step the model samples a real OpenML table, masks part of it,
  and is trained to fill the masked part — a column-masking SSL
  objective in the spirit of BERT's masked-language-model. Each
  forward pass also retrieves an in-context support set from the
  same table, so the model learns to use the retrieved context
  as evidence (like LLM RAG). Trained model handles both
  classification and regression.
* **Scaling laws on real data.** The paper's empirical contribution
  is showing that **scaling both model size and pre-training data
  size yields consistent gains following power-laws** (Figure 1
  of the paper). This is the first demonstration of LLM-style
  scaling behaviour for tabular foundation models — and crucially,
  it works on *real* data, not just synthetic.

Evaluated on **OpenML-CC18** (classification) and **OpenML-CTR23**
(regression). TabDPT consistently matches or surpasses specialised
per-dataset baselines that get hyperparameter-tuned, at a fraction
of the deployment cost. Particularly strong in the few-shot
regime: with minimal semi-supervised modifications, TabDPT
outperforms specialised baselines on **10-shot classification**.

**Contamination note.** The local code dump is
``repositories/TabDPT.txt``, and TabDPT publishes the exact list of
OpenML datasets it trained on
(`tabdpt_datasets/data_splits/{cls,reg}_datasets.csv`). Any evaluation
that uses TabDPT as a baseline must cross-check its held-out sets
against that list, or the comparison is contaminated in TabDPT's favour.

---

<a id="tabpfn-25"></a>

## 2026-02 — Grinsztajn et al. — TabPFN-2.5

**arXiv:** [2511.08667](https://arxiv.org/abs/2511.08667) ·
**PDF:** [open](papers/2026/02_Grinsztajn_et_al._TabPFN_2.5_Advancing_the_State_of_the_Art_in_Tabular_Foundation_Models.pdf)

**Where it fits.** Successor to
v2: deeper (18–24 layers), bigger context limit (50 000 samples
× 2000 features), and crucially **ships the real-data-finetuned
variant as a default option**.

**What it contains.**

* **Architecture.** Transformer with TabPFNv2-like alternating
  attention with 18–24 layers, varying across the family of
  checkpoints (the small-features specialist is shallower, the
  large-features specialist is deeper).
* **Training data.** Synthetic-only base + a Real-TabPFN-style
  real-data continued-pretraining variant. The Real-TabPFN-2.5
  checkpoint uses 43 curated datasets listed in the paper's
  Appendix C.1 (the same recipe as Garg 2025 above, refined and
  scaled).
* **Checkpoints.** Per the checkpoint catalogue in
  ``repositories/Huggingface TabPFN.txt``: ``_default`` is
  real-finetuned; ``_default-2`` is synthetic-only (the
  methodologically clean base for continued pretraining);
  multiple specialist variants (``_large-features-L``,
  ``_large-features-XL``, ``_large-samples``, ``_low-skew``,
  ``_quantiles``, ``_real``, …).
* **Evaluation.** New SOTA on a proprietary benchmark, on
  TabArena, and on RealCause (a causal-inference benchmark
  where the regression variant of the model is repurposed).

Note that v2.6 (the immediate successor described on the
HuggingFace card and the TabPFN docs) was released after v2.5
*without* a corresponding paper. v2.6 reverts the
"default-is-real-finetuned" naming convention: its single
``_default`` checkpoint is again *synthetic-only*. The primary sources
for checkpoint provenance are
`repositories/Huggingface TabPFN.txt` and `repositories/TabPFN .txt`.

---

## 2026-02 — Ma et al. — Foundation Models for Causal Inference via Prior-Data Fitted Networks

**arXiv:** [2506.10914](https://arxiv.org/abs/2506.10914) ·
**PDF:** [open](papers/2026/02_Ma_et_al._Foundation_Models_for_Causal_Inference_via_Prior_Data_Fitted_Networks.pdf)

**Where it fits.** Unified causal-PFN framework — published at
ICLR 2026, supersedes Do-PFN and FairPFN by generalising both.
Introduces **CausalFM**: a general recipe for training PFN-based
foundation models that perform Bayesian causal inference across
multiple identification strategies in a single forward pass.

**What it contains.** Three layers of contribution.

1. **Theory: necessary criteria for valid SCM-priors for causal
   inference.** The paper formalises how to construct prior
   distributions over structural causal models such that the
   resulting PFN's in-context predictions are valid estimates of
   the causal quantity of interest. Identifies what breaks if you
   naïvely take TabPFN's SCM-prior and ask it to estimate a
   treatment effect.
2. **Method: CausalFM priors.** A novel family of SCM-priors
   parameterised by Bayesian neural networks, structured to
   respect the underlying causal-inference setting. Concretely:
   different priors for **back-door adjustment** (the
   conditioning-on-confounders case), **front-door adjustment**
   (the mediator case), and **instrumental-variable adjustment**
   (the natural-experiment case).
3. **Empirics: trained PFN models for CATE estimation.**
   Conditional Average Treatment Effect estimation across diverse
   benchmarks. CausalFM **outperforms current state-of-the-art
   CATE estimators** that are specifically trained for the task,
   while requiring no per-dataset training itself.

Key advantages over classical causal inference: (i) no retraining
per new dataset (in-context inference), (ii) principled
uncertainty quantification, (iii) the model auto-selects the
identification formula based on the observed data structure,
(iv) identifiability guarantees baked into the prior design.

---

## 2026-02 — Qu et al. — TabICLv2

**arXiv:** [2602.11139](https://arxiv.org/abs/2602.11139) ·
**PDF:** [open](papers/2026/02_Qu_et_al._TabICLv2_A_better_faster_scalable_and_open_tabular_foundation_model.pdf)

**Where it fits.** Direct successor to TabICL — full state-of-the-
art tabular FM, **fully open** (inference code, model weights,
synthetic-data engine, and pretraining code), explicitly framed
as a "let's democratize the recipe so the field can build on top"
release. Beats RealTabPFN-2.5 on TabArena even after RealTabPFN-2.5
is hyperparameter-tuned, ensembled, and fine-tuned on real data.

**What it contains.** Three pillars of contributions, each with
substantial detail.

1. **A novel synthetic-data generation engine** focused on
   *diversity*. Builds on TabICL's distribution-aware feature
   embeddings and adds new SCM construction primitives,
   tree-ensemble priors (à la Mitra), and a controllable
   difficulty curriculum. The release of this generator is part
   of the paper's open-science contribution.
2. **Architectural innovations.** The most interesting one for
   the TabPFN line: a **scalable softmax** in the attention layers that
   solves the "attention fading" problem — as context length n
   grows, vanilla softmax's denominator grows too, flattening
   the attention distribution and preventing the model from
   focusing sharply. TabICLv2 scales attention logits by `s log n`
   (where s is a learnable per-head parameter), maintaining
   discriminative attention even at very large context sizes.
   This is what unlocks generalisation to **million-scale
   datasets in under 50 GB GPU memory**. Concurrent theoretical
   work (Chen 2025) confirms `log n` scaling is *necessary* to
   maintain attention sharpness as n grows.
3. **Optimisation protocol.** Replaces AdamW with the **Muon**
   optimizer (Jordan 2024), which converges faster on the
   transformer-style training loop. Combined with the new prior
   and architecture, this delivers TabICLv2's headline result:
   surpassing the strongest previously-published TFM
   (RealTabPFN-2.5) on TabArena and TALENT benchmarks **without
   any hyperparameter tuning**.

Comprehensive ablations quantify each contribution.

---

<a id="tabpfn-wide"></a>

## 2026-03 — Kolberg et al. — TabPFN-Wide

**arXiv:** [2510.06162](https://arxiv.org/abs/2510.06162) ·
**PDF:** [open](papers/2026/03_Kolberg_et_al._TabPFN_Wide_Continued_Pre_Training_for_Extreme_Feature_Counts.pdf)

**Where it fits.** Continued-pretraining sibling to Real-TabPFN,
focused on the extreme-feature-count regime.

**What it contains.** Modifies TabPFN's training recipe to
include synthetic datasets with hundreds-to-thousands of
features (matching multi-omics, wide bureau-data, etc.), then
fine-tunes on real wide-feature datasets. Specifically:

* **Synthetic prior augmentation (the actual method)** — the SCM
  generator is *widened* to produce datasets where the number of
  features vastly exceeds the number of rows, which v2's prior
  almost never sampled. The whole point is to handle wide data
  **without** reducing it.
* **FeatureAgglomeration is a baseline, not the method** — the
  paper evaluates agglomerative feature reduction only as a
  comparison point that its widened model beats (Fig. 3 /
  Appendix B). Its method is prior-widening, **not** feature reduction —
  a distinction routinely misread.
* **Released checkpoints** — TabPFN-Wide models continued-pretrained
  per maximum synthetic width (evaluated up to 60,000 features),
  **classifier-only** (the regressor is explicitly left as future
  work — so there is no wide *regressor*). Not to be confused with Prior
  Labs' own v2.5 ``_large-features-L`` (≤ 500) / ``_large-features-XL``
  (≤ 1000) specialist checkpoints from the TabPFN-2.5 release.

---

## 2026-04 — Tanna et al. — Exploring Fine-Tuning for Tabular Foundation Models

**Venue:** ACM Web Conference 2026 (WWW '26) ·
**DOI:** [10.1145/3774904.3792923](https://doi.org/10.1145/3774904.3792923) ·
**PDF:** [open](papers/2026/04_Tanna_et_al._Exploring_Fine_Tuning_for_Tabular_Foundation_Models.pdf)

**Where it fits.** A companion empirical study from the same lab as
the TabTune library — the broad "when does fine-tuning actually help a
tabular FM?" benchmark that Rubachev et al. 2025 began, now widened to
six TFMs and three large suites.

**What it contains.** Compares four adaptation strategies — zero-shot,
meta-learning (episodic, 48–512 support samples, 5 epochs), supervised
fine-tuning (full-parameter AdamW, LR 1e-5–5e-5, early stopping ≤ 10
epochs), and PEFT (LoRA r=8, α=16) — over TabPFN, TabICL, OrionMSP,
OrionBiX, TabDPT and Mitra on TALENT (155), OpenML-CC18 (63) and
TabZilla (27), plus a 9-dataset fairness suite (which includes
**German Credit** and **Default-of-Credit-Card-Clients (Taiwan)**).
Metrics span accuracy / weighted-F1 / mean-rank, **calibration**
(ECE, MCE, Brier), and **fairness** (SPD, EOD, EOpD). Headline
findings:

* **Zero-shot TFMs are already strong** — often competitive with tuned
  gradient boosting, so fine-tuning has a high bar to clear.
* **Gains are highly model- and data-dependent.** Meta-learning and
  PEFT give moderate, conditional gains; **full SFT frequently degrades
  accuracy and/or calibration** — catastrophically for some models
  (TabICL / OrionBiX collapse under SFT on the smaller suites) — while
  **TabPFN is comparatively robust** to fine-tuning.
* Dataset **imbalance, small size, and high dimensionality** are the
  factors that most often flip fine-tuning from helpful to harmful.
* Calibration can worsen even when accuracy holds, so accuracy alone is
  a misleading model-selection signal.

---

## 2026-04 — Bouadi et al. — Orion-BiX

**Venue:** ACM Web Conference 2026 (WWW '26), April 13–17 2026, Dubai ·
[DOI 10.1145/3774904.3792937](https://doi.org/10.1145/3774904.3792937) ·
Lexsi Labs (Paris / Mumbai / London) ·
**PDF:** [open](papers/2026/04_Bouadi_et_al._Orion_Bix_Bi_Axial_Attention_for_Tabular_In_Context_Learning.pdf)

**Where it fits.** The second Orion architecture, and the sibling of
Orion-MSP. Both are the models behind Lexsi Labs' TabTune library and
fine-tuning benchmark, which this library holds.

**What it contains.** A four-page conference paper, so the contribution
is stated compactly. Orion-BiX combines **bi-axial attention** with
**meta-learned in-context reasoning** for few-shot tabular learning:

* the encoder **alternates standard, grouped, hierarchical and relational
  attention**, fusing their outputs by **multi-CLS summarisation** to
  capture local and global dependencies in one pass — a richer mix than
  TabICL's flat row encoder;
* a **label-aware ICL head** adapts on the fly and scales to large label
  spaces through **hierarchical decision routing**, which is this line's
  answer to the many-class ceiling that TabPFN-3 solves with a retrieval
  decoder;
* it ships as a **scikit-learn-compatible** model, consistent with the
  Orion/TabTune emphasis on usability.

It reports outperforming gradient-boosting baselines and remaining
competitive with state-of-the-art TFMs on public benchmarks.

**Strengths and limitations.** The label-aware ICL head and hierarchical
routing are a reasonable alternative to attention-based many-class
decoding, and episodic meta-training is a defensible fit for the few-shot
regime. But at four pages this is a short paper: there is no room for
ablations separating the four attention types, no calibration analysis,
and the claim is "competitive with" rather than beating the frontier. As
with Orion-MSP, the evaluation is by the same lab that produces the
benchmark library, so treat the leaderboard position as self-reported.

---

## 2026-05 — Tanna et al. — Data Presentation Over Architecture

**arXiv:** [2605.18635](https://arxiv.org/abs/2605.18635) · Lexsi Labs ·
**PDF:** [open](papers/2026/05_Tanna_et_al._Data_Presentation_Over_Architecture_Resampling_Strategies_for_Credit_Risk_Prediction_with_Tabular_Foundation_Models.pdf)

**Where it fits.** The most directly applied paper in this library: TFMs
evaluated on real credit-default prediction, by the Lexsi Labs group
behind TabTune and the Orion models. It is the natural counterpart to
Purucker's BeyondArena — where that paper shows *split protocol* changes
TFM rankings, this one shows *context construction* does.

**What it contains.** The premise is that because TFMs predict by
in-context learning, their output is sensitive to **how the context
window is built** — which, under severe class imbalance, is a design
decision nobody had systematically varied. The study benchmarks **four
classical models and five TFMs** (TabPFN, TabICL, Orion-MSP, Orion-BiX
among them) on **Home Credit** and **Lending Club**, crossing **seven
context-construction strategies** with **context sizes from 1K to 50K**.

The headline finding is a genuine reordering of priorities:

* **The choice of context strategy explains more variance in AUC-ROC than
  the choice of TFM family.** Balanced and hybrid sampling add **3–4 AUC
  points** over uniform sampling, and that gap **exceeds the spread
  between TFMs**.
* With a **balanced context of 5K–10K examples**, the strongest TFMs reach
  the AUC of classical baselines trained on the *full* data — while also
  recovering meaningful **default-class recall** that default-threshold
  GBDTs do not. The paper notes that well-tuned GBDTs can collapse to
  majority-class prediction under severe imbalance, yielding near-zero
  minority recall at high aggregate accuracy.
* Conclusion: **context construction, not architecture choice, is the
  primary deployment lever** for TFMs in imbalanced settings.

**Strengths and limitations.** For anyone deploying a TFM on imbalanced
data this is the most actionable result in the corpus, and the recall
finding matters more than the AUC one: it identifies a failure mode of
the incumbent method rather than just a ranking. Limitations are scope —
two datasets, classification only, no LGD-style regression, and no
temporal splits, which is precisely the axis BeyondArena shows to be
decisive for credit data. Class imbalance and split protocol are
therefore two separate levers, and this paper isolates only the first.
Author-affiliation caveat as with the rest of the Orion line: the TFMs
being compared include the authors' own.

---

<a id="tabpfn-3"></a>

## 2026-05 — Grinsztajn et al. — TabPFN-3 (Technical Report)

**arXiv:** [2605.13986](https://arxiv.org/abs/2605.13986) ·
**PDF:** [open](papers/2026/05_Grinsztajn_et_al._TabPFN_3_Technical_Report.pdf) ·
**Date:** May 12, 2026

**Where it fits.** Prior Labs' next-generation tabular
foundation model after TabPFN-2.5 / 2.6. A clean architectural
reset rather than a continued-pretraining variant: a three-stage
transformer that scales in-context learning to **one million
training rows on a single H100**, adds native many-class
classification, and introduces test-time-compute ("Thinking
mode") for accuracy at the cost of latency. Released under the
TABPFN-3.0 license (permissive for research and internal
evaluation); enterprise / API tier ships TabPFN-3-Plus.

**What it contains — architecture.** TabPFN-3 abandons the
TabPFN-2.x alternating row/feature attention in favour of a
three-stage design borrowed from Qu et al.'s TabICL line:

1. **Feature distribution embedding (column-wise).** Each
   column independently embedded by a transformer with
   inducing-point attention — sidesteps the O(n²) cost of full
   cross-row attention.
2. **Feature aggregation (row-wise).** Learned `cls` tokens
   attend to all features within each row; concatenated
   `cls`-hidden states form a single fixed-dimensional row
   embedding decoupled from the input feature count.
3. **In-context learning.** A TabPFN-v1-style ICL transformer
   on the row embeddings — sequence length proportional to rows
   only, so scaling to 1M rows is feasible.

On top of this they layer (i) an **attention-based many-class
decoder** that frames class prediction as soft nearest-neighbour
retrieval over the in-context training rows (non-parametric in
class count); (ii) **row-chunking inference** that precomputes
the inducing-vector summary once and then streams rows through
the column-aggregator in fixed-size chunks, decoupling peak
activation memory from dataset size; (iii) **multi-query
attention** in the ICL stage — test rows share a single KV head,
shrinking the per-estimator KV cache to ~7 GB at 1M rows.
Pretrained purely on synthetic data from an improved SCM prior;
no real-data continued pretraining in the base release.

One integration consequence worth flagging for anyone writing
checkpoints: the **regressor criterion handling differs between v2.6 and
v3**. TabPFN regressors predict a *bar distribution* over a fixed grid
of borders. In v3, ``model.forward`` takes ``test_targets_MB`` and
the checkpoint loader **strips** any ``criterion.*`` keys and
rebuilds the bar distribution from the model's own
``regression_borders`` buffer; v2.6 has no ``test_targets_MB`` and
so the loader **requires** the ``criterion.*`` keys. Writing
``criterion.*`` unconditionally therefore round-trips for both bases —
required by v2.6, harmlessly stripped by v3. The checkpoint format itself is the
standard four-key ``torch.save`` dict (``state_dict``, ``config``,
``architecture_name``, ``inference_config``); valid
``architecture_name`` strings are ``tabpfn_v2``, ``tabpfn_v2_5``,
``tabpfn_v2_6``, ``tabpfn_v3``.

**What it contains — results.** On TabArena-medium
(10k–100k rows), a single forward pass of TabPFN-3 beats every
other model — including tuned-and-ensembled baselines — by a
significant Elo margin and pareto-dominates the speed/accuracy
frontier. TabPFN-3-Plus (Thinking) beats AutoGluon 1.5 extreme
(4 hours of tuning) in <1/10 the runtime, with no LLMs, no real
data, no internet search. Up to **20× faster than TabPFN-2.5
inference**. SOTA on many-class classification, on the RelBenchV1
relational benchmark via a relational checkpoint, on TabSTAR
(tabular-text) via Plus, and 2nd on the fev-bench time-series
benchmark via a TabPFN-TS-3 checkpoint.

---

## 2026-06 — Purucker et al. — Beyond IID: How General Are Tabular Foundation Models, Really?

**arXiv:** [2606.30410](https://arxiv.org/abs/2606.30410) ·
**Venue:** preprint (TabArena team: Prior Labs, U. Freiburg, INRIA, ELLIS) ·
**PDF:** [open](papers/2026/06_Purucker_et_al._Beyond_IID_How_General_Are_Tabular_Foundation_Models_Really.pdf)

**Where it fits.** The empirical counterpart to the position-paper
critiques: the most systematic test to date of whether TFM "generality"
survives outside the IID academic benchmark regime — co-authored by
TabPFN's own developers, which lends the negative result weight.

**What it contains.** Introduces **BeyondArena** — 142 datasets
hand-curated from 1,128 candidates (via the released DataFoundry
framework, now integrated into TabArena) spanning IID / **temporal** /
**grouped** splits, 100–1M rows, text and high-cardinality features —
and evaluates the *in-context learning* of three TFMs (TabPFN-2.6,
TabICLv2, TabDPT) against 8 default and tuned+ensembled baselines
(CatBoost, XGBoost, LightGBM, RealMLP, TabM, RF, ET, Linear; ~$50k
compute). Headline findings:

* **TFM ICL dominates tiny/small IID, low-dimensional data** — the
  regime the TabPFN line was built for.
* **On BOTH non-IID sub-benchmarks — temporal and grouped splits —
  tuned+ensembled RealMLP wins**, and tuned CatBoost takes
  high-cardinality data.
* The best-GBDT-over-best-TFM margin **grows with sample size
  (Spearman ρ=+0.60) and high-cardinality categoricals (ρ=+0.47)**.
* Split protocol matters enormously: scoring grouped tasks with IID
  splits distorts model rankings to Kendall τ=0.49–0.60.
* Calibration ablation: TabPFN-2.6 was one of only two models that
  post-hoc calibration made *worse* — native TFM calibration is
  already strong (GBDTs benefit most from recalibration).

**Limitations.** Tests in-context learning ONLY — TFM fine-tuning /
continued pretraining is explicitly listed as untested future work;
the non-IID sub-benchmarks are small (21 temporal / 18 grouped, noisy
grouped rankings); TabPFN-2.6/TabDPT results beyond 100k rows are
Random-Forest-imputed.

---

<a id="tabfm"></a>

## 2026-06 — Kong and Das (Google Research) — Introducing TabFM

**Venue:** **Google Research blog post, 30 June 2026** — *not* a paper:
no arXiv preprint, no technical report, no peer review. The GitHub
README states this outright ("A technical report is not included in
this repository at this time"). Authors Weihao Kong and Abhimanyu Das;
the acknowledgements credit Erez Louidor Ilan, Taman Narayan, Shuxin
Nie, Rajat Sen, Yichen Zhou, Joe Toth, Deqing Fu and Samet Oymak ·
**PDF:** [open](papers/2026/06_Kong_and_Das_Introducing_TabFM_A_zero_shot_foundation_model_for_tabular_data.pdf)
(print-to-PDF of the web page; the inline links and the results figure
do not survive text extraction) ·
**Weights:** [`google/tabfm-1.0.0-pytorch`](https://huggingface.co/google/tabfm-1.0.0-pytorch) ·
**Code:** [`google-research/tabfm`](https://github.com/google-research/tabfm) (JAX + PyTorch)

> **Citation trap.** The Hugging Face model card ships a BibTeX entry
> (`@article{tabfm2026, … author={Google Research} …}`) whose URL is the
> blog post. It is not a publication — do not cite it as one.

**Where it fits.** The first **big-tech entrant** into the TFM race,
and the clearest evidence that the paradigm has left the lab: Google
positions TabFM as "TimesFM for tables" — the same zero-shot pitch it
made for time series — and is wiring it into BigQuery. Scientifically
it is not a new idea but a **convergence artifact**: TabFM is
explicitly the TabPFN × TabICL hybrid that [TabPFN-3](#tabpfn-3) and
Qu et al.'s TabICLv2 arrived at independently, built by a third lab.
Treat it as *market* news with architectural confirmation value, not
as a methodological contribution.

**What it contains.** The post describes three mechanisms, and is
candid that each is borrowed:

* **Alternating row/column attention** over the raw table — "similar
  to TabPFN" — to learn feature interactions without manual feature
  engineering.
* **Row compression** — each cross-attended row is collapsed into a
  single dense vector.
* **ICL over compressed rows** — a dedicated Transformer attends over
  the row embeddings rather than the raw grid, "adopting the highly
  efficient approach of TabICL", which is what keeps inference cheap
  on larger tables.

**Training data is 100% synthetic**, and the post argues this is
forced rather than chosen: high-quality industrial tables are
proprietary, so "synthetic tables … are effectively the only viable
option for pre-training a foundation model at this scale." It reports
**hundreds of millions of synthetic datasets**, generated dynamically
from structural causal models with a wide variety of random functions.

**Evaluation** is on **TabArena** (Elo from head-to-head win rates):
38 classification and 13 regression datasets, 700–150,000 samples, in
two configurations —

| Configuration | What it is |
|---|---|
| **TabFM** | out-of-the-box, single forward pass, no tuning or cross-validation |
| **TabFM-Ensemble** | adds cross features and SVD features; 32-way ensemble whose weights come from a non-negative least-squares solver; **Platt scaling** as a calibration step for classification |

The headline claim is that TabFM "consistently outperforms heavily
tuned, industry-standard supervised algorithms". Deployment is the
real news: **BigQuery `AI.PREDICT`**, so a practitioner gets a TFM
from SQL with "no ML expertise required". Weights and code are
announced on Hugging Face and GitHub.

**What the released artifacts add (the blog is not the only source).**
The post itself has no architecture table, but `classification/config.json`
in the released checkpoints does — and it confirms the three-stage
reading: `col_num_blocks` 3 / `col_nhead` 4 with **`col_num_inds` 256**
(inducing-point column attention, the same trick TabPFN-3 uses),
`row_num_blocks` 3 / `row_nhead` 8, then `icl_num_blocks` **24** /
`icl_nhead` 8, all at `embed_dim` 256. **Hard limits, verified:**
`max_classes` **10** — described on the model card as a hard
architectural cap; `max_num_features` default **500** and
`max_num_rows` default **100 context rows**, which are estimator
defaults rather than ceilings (independent testing reached ~20k rows on
JAX/24 GB and ~40k on PyTorch with bf16 + chunking, and hit a genuine
failure on 1,777-feature data). **Parameter count is unpublished**;
do not infer it from the ~6.5 GB checkpoints, which are irreconcilable
with a 256-dim/24-block transformer and probably bundle replicas.
**Licensing is dual and consequential: code is Apache-2.0, but the
pretrained weights carry `tabfm-non-commercial-v1.0`, restricted to
non-commercial, non-production use** — and the quick-start loader
downloads those weights silently.

**Limitations — severe by this library's standards.** No specification
of the synthetic prior beyond "SCMs with random functions"; no
ablations separating the three mechanisms; no per-dataset results in
the post, no significance tests, and **no calibration metrics** (Platt
scaling appears as an ensemble ingredient, not as a measured outcome).
The Elo comparison exists **only as a figure**: the text states no
numbers and names only AdaBoost, XGBoost, random forests, and
unversioned "TabPFN"/"TabICL" — TabPFN-2.5, TabPFN-3, TabICLv2,
CatBoost, LightGBM, RealMLP and AutoGluon are never mentioned. So
**the post supports no quotable claim about how TabFM ranks against
the current TabPFN or TabICL frontier**; secondary reports place
TabFM-Ensemble 1st and TabFM 2nd in the figure's top-10, but the
specific Elo values circulating online trace to a single unreachable
aggregator and should not be recorded. Google's Elo is also computed
over *separate* classification and regression pools, so it is not
comparable with the public TabArena board's combined Elo, and TabFM was
not yet on that board (a pull request was reportedly pending). Note too
that **TabFM-Ensemble is not zero-shot** in the single-forward-pass
sense — it adds engineered cross/SVD features, a 32-way weighted
ensemble, and Platt scaling — yet it is the configuration that
reportedly ranks first. The one independent check available (a
13-dataset subset) found TabFM beat Optuna-tuned XGBoost zero-shot on
every fold-matched dataset, but was only "hair-thin" ahead of TabPFN.
Raw per-dataset metrics are in the repo under `results/*.parquet` if a
proper comparison is ever needed. Any claim from this source should be
attributed to Google's blog, not to the literature.
