# Literature on Tabular Foundation Models

A chronological tour of the **71 papers** in this folder (1 from 2021, 3 from 2023, 8 from
2024, 22 from 2025 and 37 from 2026, dated by the filed version), following the owner's
`Tabular Foundation Models` Zotero collection. The arc: PFNs (in-context Bayesian inference for
arbitrary priors) → TabPFN (PFNs with a tabular prior) → TabPFN v2 (the first production-grade
release) → a wave of variants and competitors (continued pretraining, drift, fairness, causal
inference, time series, many classes, scalability, real-data pretraining, text and relational
data) → TabPFN-2.5 / 2.6 → TabPFN-3 (May 2026: a TabICL-style three-stage architecture scaling
to 1M rows, with a test-time-compute "Thinking" mode) → a crowded second half of 2026 of
competing releases from industrial and academic labs (Google's TabFM, LG's EXAONE Tabular, the
open TabICLv2, TabPFN-3.5, Mitra-v2, Xiaomi-TabLDM, LimiX-2, Causilo). Alongside the model releases runs a
growing evaluation literature: theory of why PFNs work, benchmarks beyond IID splits and
beyond accuracy, fine-tuning and test-time-compute studies, self-consistency and depth
analyses, and domain studies (credit risk, insurance pricing, survival, relational and
multimodal data) that test how far generic benchmark wins transfer.

Every entry follows the same structure:

* An explicit anchor and a **Provenance** line — venue or status, arXiv identifier and the
  filed version, a non-arXiv DOI where one exists, notable affiliation, code and weights
  availability (with licence where it matters) and a link to the filed PDF.
* The **Citation key** — the Better BibTeX key of the Zotero record (omitted where none exists).
* **Where it fits** in the picture above — what it answers, extends or contradicts, with links to
  related entries.
* **What it contains** — the method, explained well enough to follow without the paper, and the
  data and evaluation protocol.
* **Key results** — headline numbers with table, section or figure pointers into the paper.
* **Strengths** — what the paper genuinely establishes.
* **Limitations** — what it does *not* support and where to be careful quoting it; author-stated
  limitations are distinguished from reviewer reading where the difference matters.

Material taken from code dumps or model cards rather than the paper is labelled as such.

**This document is project-neutral by contract** (see AGENTS.md). It describes the literature
for every consuming project; it contains no project's pipeline details, hyperparameter choices,
or relevance rankings. Those belong in your project's own `PROJECT_SPECIFIC.md` — copy
[`PROJECT_SPECIFIC.template.md`](PROJECT_SPECIFIC.template.md) inside your project's copy of
this folder and write them there.

## Overview table

| Date | Authors | Title | One-line contribution | PDF |
|---------|---------|-------|-----------------------|-----|
| 2021-12 | Müller et al. | Transformers Can Do Bayesian Inference | Foundational PFN paper: training a transformer on datasets sampled from a prior makes its loss the expected KL to the posterior predictive, so one forward pass approximates Bayesian inference; 1,000–8,000× faster than NUTS, and the BNN-prior PFN ranks first on 20 tiny (30-row) tabular tasks. | [pdf](papers/2021/12_Muller_et_al._Transformers_Can_Do_Bayesian_Inference.pdf) |
| 2023-05 | Müller et al. | PFNs4BO — In-Context Learning for Bayesian Optimization | PFN as a drop-in BO surrogate with GP, HEBO(+) and BNN priors plus prior-level spurious-feature and user-prior extensions; the HEBO+ prior beats all baselines on HPO-B and HEBO on PD1. | [pdf](papers/2023/05_Muller_et_al._PFNs4BO_In_Context_Learning_for_Bayesian_Optimization.pdf) |
| 2023-07 | Nagler | **Statistical Foundations of Prior-Data Fitted Networks** | The theory of *why* PFN in-context learning works — and its limit: read as a pre-tuned untrained predictor, variance vanishes but bias vanishes only with localisation, which transformers do not guarantee; TabPFN v1's bias plateaus near n ≈ 1,000 unless kNN-localised. | [pdf](papers/2023/07_Nagler_Statistical_Foundations_of_Prior_Data_Fitted_Networks.pdf) |
| 2023-09 | Hollmann et al. | TabPFN — A Transformer That Solves Small Tabular Classification Problems in a Second | First TabPFN: PFN trained on an SCM+BNN tabular prior; on 18 small numerical OpenML-CC18 tasks it matches one-hour AutoML (ROC-AUC 0.934 vs 0.930 AutoGluon) in 0.62 s on a GPU. | [pdf](papers/2023/09_Hollmann_et_al._TabPFN_A_Transformer_That_Solves_Small_Tabular_Classification_Problems_in_a_Second.pdf) |
| 2024-03 | Rundel et al. | Interpretable Machine Learning for TabPFN | Adapts IML methods (Kernel SHAP, SAGE, LOCO, PD/ICE/ALE, Data Shapley) to TabPFN, using in-context refits as exact, cheap retraining; lower Shapley error than imputation and +0.57–3.3% ROC-AUC from Data-Shapley context selection. | [pdf](papers/2024/03_Rundel_et_al._Interpretable_Machine_Learning_for_TabPFN.pdf) |
| 2024-06 | Breugel and Schaar | Why Tabular Foundation Models Should Be a Research Priority | Position paper (ICML 2024): "Large Tabular Models" are an under-invested priority; three hypothesised reasons for neglect and four design desiderata (D1–D4: mixed types, cross-dataset, textual context, column-order symmetry); no experiments. | [pdf](papers/2024/06_Breugel_and_Schaar_Why_Tabular_Foundation_Models_Should_Be_a_Research_Priority.pdf) |
| 2024-07 | Kim et al. | CARTE: Pretraining and Transfer for Tabular Learning | Rows as graphlets with language-model embeddings of column names and strings, contrastively pretrained on YAGO3 then fine-tuned; beats 42 baselines on 51 string-rich tables and transfers across unmatched schemas, at much higher compute. | [pdf](papers/2024/07_Kim_et_al._CARTE_Pretraining_and_Transfer_for_Tabular_Learning.pdf) |
| 2024-10 | den Breejen et al. | **TabForestPFN** — Fine-tuned In-Context Learning Transformers are Excellent Tabular Data Classifiers | Mixes TabPFN's prior with an unrealistic *forest* generator of complex decision boundaries and fine-tunes per dataset; fine-tuned TabForestPFN ties tuned GBDTs on TabZilla (0.840 vs CatBoost 0.842) and leads ICL variants on WhyTrees. Early tree-prior precursor cited by Mitra. | [pdf](papers/2024/10_Breejen_et_al._Fine_tuned_In_Context_Learning_Transformers_are_Excellent_Tabular_Data_Classifiers.pdf) |
| 2024-11 | Helli et al. | Drift-Resilient TabPFN | TabPFN v1 prior in which a 2nd-order SCM shifts causal edge weights over a temporal domain index, so ICL extrapolates drift; OOD accuracy 0.688→0.744 and ROC AUC 0.786→0.832 on 18 datasets, gains mostly on synthetic ones. | [pdf](papers/2024/11_Helli_et_al._Drift_Resilient_TabPFN_In_Context_Learning_Temporal_Distribution_Shifts_on_Tabular_Data_1.pdf) |
| 2024-12 | Hoo et al. | The Tabular Foundation Model TabPFN Outperforms Specialized Time Series Forecasting Models | TabPFN-TS (workshop): each series becomes a regression table of timestamp features (index + sin/cos calendar, no lags); frozen 11M-param TabPFN gets the best relative MASE on 24 AutoGluon-TS datasets (0.759), ahead of Chronos-Mini and Chronos-Large. | [pdf](papers/2024/12_Hoo_et_al._The_Tabular_Foundation_Model_TabPFN_Outperforms_Specialized_Time_Series_Forecasting_Models_Based_on.pdf) |
| 2024-12 | Thomas et al. | **LoCalPFN** — Retrieval & Fine-Tuning for In-Context Tabular Models | Uses each query's k nearest neighbours as TabPFN's context (TabPFN-kNN) and fine-tunes end-to-end with approximate shared local contexts; mean AUC 0.908 vs 0.892 tuned XGBoost and 0.867 TabPFN on 95 TabZilla datasets. Ancestor of TabDPT's retrieval. | [pdf](papers/2024/12_Thomas_et_al._Retrieval_Fine_Tuning_for_In_Context_Tabular_Models.pdf) |
| 2024-12 | Feuer et al. | **TuneTables** — Context Optimization for Scalable Prior-Data Fitted Networks | Prompt tuning for PFNs: distils a large dataset into a small learned context for frozen TabPFN v1 (<5% of parameters tuned); best mean accuracy/rank among 19 tuned algorithms on 98 TabZilla datasets, though not significantly ahead of CatBoost/XGBoost; also tunes for fairness. | [pdf](papers/2024/12_Feuer_et_al._TuneTables_Context_Optimization_for_Scalable_Prior_Data_Fitted_Networks.pdf) |
| 2025-01 | Hollmann et al. | Accurate predictions on small data with a tabular foundation model | The TabPFN v2 paper (Nature): new SCM prior, per-cell feature-then-sample attention, regression via bar distribution, up to 10K rows × 500 features; default model in 2.8 s beats baselines and AutoGluon tuned for 4 h (normalised ROC AUC 0.939 vs default CatBoost 0.752). | [pdf](papers/2025/01_Hollmann_et_al._Accurate_predictions_on_small_data_with_a_tabular_foundation_model.pdf) |
| 2025-02 | Liu and Ye | TabPFN Unleashed — A Scalable and Effective Solution to Tabular Classification Problems | BETA: frozen TabPFN v1 behind fine-tuned lightweight Batch-Ensemble encoders, bootstrapped 1,000-row contexts and ECOC, reducing bias and variance; untuned, best critical-difference rank on 186 TALENT datasets vs tuned baselines. | [pdf](papers/2025/02_Liu_and_Ye_TabPFN_Unleashed_A_Scalable_and_Effective_Solution_to_Tabular_Classification_Problems.pdf) |
| 2025-02 | McCarter | **What exactly has TabPFN learned to do?** | Black-box toy probes of v1 expose duplication oddities, no periodicity detection and reliance on ensembling (then ~1-NN behaviour); the v2 appendix finds bumpier toy surfaces but >99% accuracy on 10-bit parity from 127 rows. | [pdf](papers/2025/02_McCarter_What_exactly_has_TabPFN_learned_to_do.pdf) |
| 2025-05 | Müller et al. | Position — The Future of Bayesian Prediction Is Prior-Fitted | Position paper (ICML 2025): with real data scarce and compute cheap, prior-fitted networks should become the default route to Bayesian prediction; sets an agenda (extensions, understanding, scaling/speed/architecture fixes) and lists current PFN limitations. | [pdf](papers/2025/05_Muller_et_al._Position_The_Future_of_Bayesian_Prediction_Is_Prior_Fitted.pdf) |
| 2025-05 | Qu et al. | TabICL — A Tabular Foundation Model for In-Context Learning on Large Data | Set-Transformer column embedding and [CLS] row compression before ICL, tree-SCM prior and size curriculum; ties TabPFNv2 on 200 TALENT classification datasets at 1.5–10× speed and beats it and CatBoost above 10K rows. | [pdf](papers/2025/05_Qu_et_al._TabICL_A_Tabular_Foundation_Model_for_In_Context_Learning_on_Large_Data.pdf) |
| 2025-06 | Robertson et al. | FairPFN — A Tabular Foundation Model for Causal Fairness | PFN trained to map biased SCM data to fair targets (protected attribute's edges dropped), removing its causal effect without a graph; Pareto-optimal on 40% of 600 synthetic datasets, prediction ATE < 0.01 on Law School and Adult. | [pdf](papers/2025/06_Robertson_et_al._FairPFN_A_Tabular_Foundation_Model_for_Causal_Fairness.pdf) |
| 2025-06 | Rubachev et al. | **On Finetuning Tabular Foundation Models** | Single-dataset fine-tuning study of TabPFNv2: full FT matches PEFT, converges fastest and sharpens query–key retrieval; a 5-run FT ensemble ranks first among tuned DL baselines, but results are less stable on temporally shifted TabReD. | [pdf](papers/2025/06_Rubachev_et_al._On_Finetuning_Tabular_Foundation_Models_1.pdf) |
| 2025-06 | Ye et al. | A Closer Look at TabPFN v2 — Understanding Its Strengths and Extending Its Capabilities | Probes TabPFNv2's randomized attribute tokens and leave-one-fold-out embeddings on 273 TALENT datasets; retraining-free feature bagging, decimal label encoding and -SQ/-DF improve v2 on wide, many-class and large data but trail CatBoost/RealMLP at scale. | [pdf](papers/2025/06_Ye_et_al._A_Closer_Look_at_TabPFN_v2_Understanding_Its_Strengths_and_Extending_Its_Capabilities.pdf) |
| 2025-07 | Garg et al. | **Real-TabPFN** — Improving Tabular Foundation Models via Continued Pre-training With Real-World Data | **The reference continued-pretraining recipe.** Continue-pretrains TabPFNv2 on 71 curated real datasets with L2-SP; normalised ROC-AUC 0.954 → 0.976 on 29 AMLB datasets (Wilcoxon p = 0.0045). | [pdf](papers/2025/07_Garg_et_al._Real_TabPFN_Improving_Tabular_Foundation_Models_via_Continued_Pre_training_With_Real_World_Data.pdf) |
| 2025-10 | Zhang et al. | Mitra — Mixed Synthetic Priors for Enhancing Tabular Foundation Models | Selects a synthetic-prior mixture (SCM plus five tree-based priors) by performance, diversity and distinctiveness; with ensembling and fine-tuning it narrowly leads Attic and TabPFNv2 on 137 classification datasets, but trails v2 on larger regression. | [pdf](papers/2025/10_Zhang_et_al._Mitra_Mixed_Synthetic_Priors_for_Enhancing_Tabular_Foundation_Models.pdf) |
| 2025-10 | Wu and Bergman | **APT** — Zero-shot Meta-learning for Tabular Prediction Tasks with Adversarially Pre-trained Transformer | Makes the synthetic prior *adaptive*: adversarial data agents shift their generating distribution to challenge the model, and a mixture block removes the class-count cap; best mean rank (3.86) on 35 unfiltered small OpenML-CC18 datasets. | [pdf](papers/2025/10_Wu_and_Bergman_Zero_shot_Meta_learning_for_Tabular_Prediction_Tasks_with_Adversarially_Pre_trained_Transformer.pdf) |
| 2025-11 | Robertson et al. | Do-PFN — In-Context Learning for Causal Effect Estimation | PFN trained on paired observational/interventional SCM data predicts conditional interventional outcomes without a causal graph; beats CATE baselines when unconfoundedness fails, competitive on RealCause, and widens uncertainty when effects are unidentifiable. | [pdf](papers/2025/11_Robertson_et_al._Do_PFN_In_Context_Learning_for_Causal_Effect_Estimation.pdf) |
| 2025-11 | Zhang et al. | TabPFN — One Model to Rule Them All | Reads TabPFN v2 as approximate Bayesian inference for statisticians; untuned, it beats published specialists on their own designs for semi-supervised estimation, CATE (S-Learner) and covariate shift, and adapts to sparse-linear and label-noise settings. | [pdf](papers/2025/11_Zhang_et_al._TabPFN_One_Model_to_Rule_Them_All.pdf) |
| 2025-11 | Bouadi et al. | **Orion-MSP** — Multi-Scale Sparse Attention for Tabular In-Context Learning | TabICL-style classifier with multi-scale (1/4/16) row encoding, block-sparse feature attention and optional Perceiver memory; best zero-shot mean rank 3.58 (TabPFN 4.61) but 5.69 on wide tables, behind XGBoost/CatBoost. | [pdf](papers/2025/11_Bouadi_et_al._Orion_MSP_Multi_Scale_Sparse_Attention_for_Tabular_In_Context_Learning.pdf) |
| 2025-11 | Zheng et al. | **From Tables to Signals** — Revealing Spectral Adaptivity in TabPFN | Defines a context kernel (Jacobian w.r.t. context labels) and shows TabPFN's effective bandwidth widens with the *number of context rows*, unlike an MLP's; positional encoding tunes it, and training-free denoising reaches 31.70 dB vs WIRE's 29.48. | [pdf](papers/2025/11_Zheng_et_al._From_Tables_to_Signals_Revealing_Spectral_Adaptivity_in_TabPFN.pdf) |
| 2025-11 | Zhang et al. | LimiX: Unleashing Structured-Data Modeling Capability for Generalist Intelligence | Context-conditional masked modelling on hierarchical-SCM data unifies prediction, imputation and generation in LimiX-16M/2M; LimiX-16M has the best averaged reciprocal rank on classification (0.302) and regression (0.292) across 11 benchmarks. | [pdf](papers/2025/11_Zhang_et_al._LimiX_Unleashing_Structured_Data_Modeling_Capability_for_Generalist_Intelligence.pdf) |
| 2025-12 | Pfefferle et al. | nanoTabPFN — A Lightweight and Educational Reimplementation of TabPFN | Under-500-line educational reimplementation of v2's architecture and training loop on pre-generated TabICL-prior data; a one-minute pretrain beats sklearn baselines and TabPFN without ensembling/preprocessing on tiny binary tasks. | [pdf](papers/2025/12_Pfefferle_et_al._nanoTabPFN_A_Lightweight_and_Educational_Reimplementation_of_TabPFN.pdf) |
| 2025-12 | Tanna et al. | TabTune — A Unified Library for Inference and Fine-Tuning Tabular Foundation Models | Scikit-learn-style library running zero-shot, episodic meta-learning, full SFT and LoRA across seven TFMs with calibration/fairness metrics; adaptation is model-dependent (SFT: TabPFN best within-group rank 1.97, TabICL collapses 0.873→0.567 on TabZilla). | [pdf](papers/2025/12_Tanna_et_al._TabTune_A_Unified_Library_for_Inference_and_Fine_Tuning_Tabular_Foundation_Models.pdf) |
| 2025-12 | Spinaci et al. | **ConTextTab** — A Semantics-Aware Tabular In-Context Learner | TabPFN-style backbone with per-modality (text/date/number/column-name) embeddings, pretrained on 2.18M real T4 tables; best rank on the semantic CARTE benchmark (1.55), on par but not first on non-semantic benchmarks. | [pdf](papers/2025/12_Spinaci_et_al._ConTextTab_A_Semantics_Aware_Tabular_In_Context_Learner.pdf) |
| 2025-12 | Arazi et al. | **TabSTAR** — A Tabular Foundation Model for Tabular Data with Text Fields | Verbalised features plus target-value tokens through a partly unfrozen e5 encoder, then per-task LoRA fine-tuning; best text-tabular classification (0.83 vs TabM-Tuned 0.73, ≤10K rows), behind GBDTs on regression. | [pdf](papers/2025/12_Arazi_et_al._TabSTAR_A_Tabular_Foundation_Model_for_Tabular_Data_with_Text_Fields.pdf) |
| 2025-12 | Balazadeh Meresht et al. | **CausalPFN** — Amortized Causal Effect Estimation via In-Context Learning | ~20M-parameter PFN trained on ignorable DGPs built from real/synthetic base tables outputs CEPO posteriors; best average CATE rank (2.30) over 310 IHDP/ACIC/Lalonde tasks, ATE only competitive; OOD intervals need temperature scaling. | [pdf](papers/2025/12_Balazadeh_Meresht_et_al._CausalPFN_Amortized_Causal_Effect_Estimation_via_In_Context_Learning.pdf) |
| 2025-12 | Arbel et al. | **EquiTabPFN** — A Target-Permutation Equivariant Prior Fitted Network | Proves non-target-equivariant PFNs pay a non-negative "equivariance gap"; per-class target tokens, two-axis attention and an attention decoder make predictions class-order invariant and give the best median accuracy on 10 TabZilla tasks with >10 classes. | [pdf](papers/2025/12_Arbel_et_al._EquiTabPFN_A_Target_Permutation_Equivariant_Prior_Fitted_Network.pdf) |
| 2026-01 | Hoo et al. | From Tables to Time — Extending TabPFN-v2 to Time Series Forecasting | Recasts forecasting as tabular regression on timestamp-derived features (index, calendar, seasonal) fed to frozen TabPFN-v2; strongest overall on 28 fev-bench covariate tasks and close behind TiRex, Toto and Moirai-2 on GIFT-Eval, at ~30× Chronos-Bolt's inference time. | [pdf](papers/2026/01_Hoo_et_al._From_Tables_to_Time_Extending_TabPFN_v2_to_Time_Series_Forecasting.pdf) |
| 2026-01 | Klein and Hoffart | Position — Foundation Models for Tabular Data within Systemic Contexts Need Grounding | SAP position paper with no experiments: TFMs trained on isolated tables miss the operational context (business rules, code, data models) behind enterprise data; proposes Semantically Linked Tables, an FMSLT model class and an "Operational Turing Test". | [pdf](papers/2026/01_Klein_and_Hoffart_Position_Foundation_Models_for_Tabular_Data_within_Systemic_Contexts_Need_Grounding.pdf) |
| 2026-01 | Ma et al. | TabDPT — Scaling Tabular Foundation Models on Real Data | Row-based TFM pretrained only on 123 real OpenML tables with random-column self-supervised targets and kNN-retrieved contexts; matches TabPFN v2 on CC18/CTR23 (AUC 0.933 vs 0.932) and follows a joint power law in model and data size. | [pdf](papers/2026/01_Ma_et_al._TabDPT_Scaling_Tabular_Foundation_Models_on_Real_Data.pdf) |
| 2026-02 | Grinsztajn et al. | **TabPFN-2.5** — Advancing the State of the Art in Tabular Foundation Models | Deeper v2 architecture (18/24 layers) on an undisclosed synthetic prior for up to 50K×2K; default model beats AutoGluon 1.4 extreme on TabArena-Lite classification and the real-data Real-TabPFN-2.5 variant leads tuned ensembles; non-commercial weights. | [pdf](papers/2026/02_Grinsztajn_et_al._TabPFN_2.5_Advancing_the_State_of_the_Art_in_Tabular_Foundation_Models.pdf) |
| 2026-02 | Ma et al. | Foundation Models for Causal Inference via Prior-Data Fitted Networks | CausalFM: PFNs trained on identifiability-constrained SCM priors (one model per back-door, front-door or IV setting) to output CATEs in-context; best average PEHE on synthetic back-door, binary-IV and front-door tests but well behind CausalPFN on ACIC 2016. | [pdf](papers/2026/02_Ma_et_al._Foundation_Models_for_Causal_Inference_via_Prior_Data_Fitted_Networks.pdf) |
| 2026-03 | Kolberg et al. | **TabPFN-Wide** — Continued Pre-Training for Extreme Feature Counts | TabPFN v2 classifier continued-pretrained on a synthetic feature-widening of the TabICL prior; handles 30k+ features without reduction (BRCA AUROC 0.733 → 0.971, 92% HDLSS win rate) with no forgetting on TabArena (ρ = 0.9935). | [pdf](papers/2026/03_Kolberg_et_al._TabPFN_Wide_Continued_Pre_Training_for_Extreme_Feature_Counts.pdf) |
| 2026-03 | Regenwetter et al. | Engineering Regression Without Real-Data Training: Domain Adaptation for Tabular Foundation Models Using Multi-Dataset Embeddings | Real engineering dataset embeddings guide synthetic-task selection for continued pretraining of TabPFN 2.5; lower test error than the base on 29/35 engineering regression datasets. | [pdf](papers/2026/03_Regenwetter_et_al._Engineering_Regression_Without_Real_Data_Training_Domain_Adaptation_for_Tabular_Foundation_Models_Using_Multi_Dataset_Embeddings.pdf) |
| 2026-04 | Tanna et al. | **Exploring Fine-Tuning for Tabular Foundation Models** | Six TFMs × four adaptation strategies (zero-shot, episodic meta-learning, full SFT, LoRA) on TALENT, CC18 and TabZilla: zero-shot is hard to beat and best calibrated; SFT degrades most models (TabICL TabZilla accuracy 0.87 → 0.57) but not TabPFN; lightly tuned recipes, classification only. | [pdf](papers/2026/04_Tanna_et_al._Exploring_Fine_Tuning_for_Tabular_Foundation_Models.pdf) |
| 2026-04 | Bouadi et al. | **Orion-BiX** — Bi-Axial Attention for Tabular In-Context Learning | TabICL with a biaxial row encoder (standard, grouped, hierarchical and relational attention, multi-CLS pooling) and episodic meta-training; best mean rank on Medical and Finance subsets and +2–4 points at ≤32 shots; no ablations. | [pdf](papers/2026/04_Bouadi_et_al._Orion_Bix_Bi_Axial_Attention_for_Tabular_In_Context_Learning.pdf) |
| 2026-04 | Hudovernik et al. | **KumoRFM-2**: Scaling Foundation Models for Relational Learning | Closed relational foundation model: task-conditioned table attention plus foreign-key and cross-sample attention over temporal database subgraphs, ≤10k context examples; 79.60 AUROC on RelBenchV1 classification (RelGNN 78.06), 0.83 SALT MRR; rel-f1 regime disputed. | [pdf](papers/2026/04_Hudovernik_et_al._KumoRFM_2_Scaling_Foundation_Models_for_Relational_Learning.pdf) |
| 2026-05 | Grinsztajn et al. | **TabPFN-3** — Technical Report | **The May 2026 TabPFN generation.** TabICL-style column→row→ICL architecture with retrieval many-class decoder, row-chunking to 1M rows on one H100, synthetic-only prior and API-only "Thinking" mode; one forward pass beats tuned+ensembled models on TabArena (+72 Elo over Real-TabPFN-2.5), Thinking >200 Elo over non-TabPFN models. | [pdf](papers/2026/05_Grinsztajn_et_al._TabPFN_3_Technical_Report.pdf) |
| 2026-05 | Tanna et al. | **Data Presentation Over Architecture** — Resampling Strategies for Credit Risk Prediction with TFMs | Seven context-construction strategies × five TFMs on Home Credit and Lending Club: class-balanced contexts add ~3 AUC points on Home Credit (~1 on Lending Club) over uniform sampling, more than the inter-TFM gap, and restore default recall; baselines untuned and unweighted. | [pdf](papers/2026/05_Tanna_et_al._Data_Presentation_Over_Architecture_Resampling_Strategies_for_Credit_Risk_Prediction_with_Tabular_Foundation_Models.pdf) |
| 2026-05 | Hosseinzadeh et al. | **TabDPT-Turbo** — Efficient In-Context Learning for Tabular Prediction | Drops TabDPT's retrieval for **long-context pretraining**, stays row-based, scales the real corpus to 1,445 tables; fourth on TabArena-Lite Elo and ≈2.4× faster total time than TabPFN-3 (≈13× than TabICLv2) on shared hardware. Shipped as TabDPT v1.2. | [pdf](papers/2026/05_Hosseinzadeh_et_al._TabDPT_Turbo_Efficient_In_Context_Learning_for_Tabular_Prediction.pdf) |
| 2026-05 | Schambach et al. | **Benchmarking Attention for Tabular Foundation Models** | H100 microbenchmarks of five attention backends on tabular shapes: cuDNN SDPA wins feature-axis attention (2.5–3× efficient SDPA for 128–2,048 features), FlashAttention-3 wins sample-axis attention (up to 3.5×) by avoiding tensor copies. | [pdf](papers/2026/05_Schambach_et_al._Benchmarking_Attention_for_Tabular_Foundation_Models.pdf) |
| 2026-06 | Purucker et al. | **Beyond IID: How General Are Tabular Foundation Models, Really?** | BeyondArena (142 curated datasets; IID, temporal, grouped splits; 11 models): TFM in-context learning wins tiny/small IID data, but tuned+ensembled RealMLP leads temporal, grouped and large data and CatBoost high-cardinality data; the GBDT advantage grows with rows (ρ = 0.60). Fine-tuning untested. | [pdf](papers/2026/06_Purucker_et_al._Beyond_IID_How_General_Are_Tabular_Foundation_Models_Really.pdf) |
| 2026-07 | Luo et al. | **Memory Efficient Tabular Foundation Models** | Post-training INT4 quantization (GPTQ, AWQ, K-Means) of TabPFN v2.5/2.6 shrinks BZIP2-compressed checkpoints 6.06–7.65× with ≤0.005 accuracy loss on 30 OpenML datasets; inference memory (~4.7 GB) and runtime are unchanged. | [pdf](papers/2026/07_Luo_et_al._Memory_Efficient_Tabular_Foundation_Models.pdf) |
| 2026-08 | Shaheen et al. | **Understanding the Surprising Generalization Properties of Tabular Foundation Models** | Single-real-table pretraining (88 models, 107 held-out datasets) transfers broadly; feature and task count, not row count, drive transfer (meta-model R² 0.67); column cleaning helps, ≥30-feature filtering hurts; argues for **retrieval-and-aggregation** over prior-fitted Bayesian inference. | [pdf](papers/2026/08_Shaheen_et_al._Understanding_the_Surprising_Generalization_Properties_of_Tabular_Foundation_Models.pdf) |
| 2026-08 | Eo et al. | **EXAONE Tabular 1.0** — Technical Report | CAST interleaves feature- and item-axis attention via summary tokens, with no row compression; the 20.8M synthetic-only classifier ranks first on TabArena untuned, ties TabFM's 1.64B June checkpoint at ~1.3% of its size, leads BCCO/TALENT regression and ScoringBench; non-commercial weights, no ablations. | [pdf](papers/2026/08_Eo_et_al._EXAONE_Tabular_1.0_Technical_Report.pdf) |
| 2026-08 | Klötergens et al. | Do Tabular Foundation Models Agree with Themselves? | Label-free marginalization and factorization consistency tests (factorization implies marginalization): every evaluated TFM (TabPFN v2/v3, TabICL v1/v2, TabDPT, TabFM) violates both on all 17 target pairs, independently of accuracy. | [pdf](papers/2026/08_Klotergens_et_al._Do_Tabular_Foundation_Models_Agree_with_Themselves.pdf) |
| 2026-09 | Qu et al. | TabICLv2 — A better, faster, scalable, and open tabular foundation model | Fully open TabICL successor (ICML 2026): repeated feature grouping, early target embedding, QASSMax attention scaling, a new diverse prior and Muon; untuned it beats tuned+ensembled RealTabPFN-2.5 on TabArena and TALENT, runs ~10× faster than TabPFN-2.5 and handles 1M rows; the prior is the largest ablation effect. | [pdf](papers/2026/09_Qu_et_al._TabICLv2_A_better_faster_scalable_and_open_tabular_foundation_model.pdf) |
| 2026-09 | Jäger et al. | **TabPFN-3.5** — Technical Report | TabPFN-3 with Fourier and ECDF cell encodings, doubled width at constant KV cache (220M), one multitask checkpoint and a prior retuned for grouped/wide/high-cardinality data; the family (often API-only variants) ranks 1st on seven benchmarks, though tuned MLPs still lead BeyondArena's grouped/temporal/large slices. Restrictive weight licence. | [pdf](papers/2026/09_Jager_et_al._TabPFN_3.5_Technical_Report.pdf) |
| 2026-09 | Tao et al. | **Mitra-v2** — Technical Report | Unchanged 77M Tab2D backbone with ~10× larger pretraining tasks, an O'Prior-style Hybrid SCM and Muon; the finetuned, bagged system ties TabFM and EXAONE on TabArena (1,775 Elo) and TALENT and is first on >10-class tasks via a hierarchical wrapper; changes not ablated; Apache-2.0. | [pdf](papers/2026/09_Tao_et_al._Mitra_v2_Technical_Report.pdf) |
| 2026-09 | Xiaomi-TabLDM Team | **Xiaomi-TabLDM** — A Tabular Foundation Model | TabICLv2-style model with dual-stream feature grouping, attention residuals and the collection's first **sparse Mixture-of-Experts** ICL layers (~70M total, ~62M active); 1st on OpenML-CTR23 and 2nd to TabFM on TabArena, TALENT and BCCO regression; no ablations. | [pdf](papers/2026/09_Team_et_al._Xiaomi_TabLDM_A_Tabular_Foundation_Model_Technical_Report.pdf) |
| 2026-09 | Zhang et al. | **LimiX-2** — A Contextual Mechanism Network Towards General Structured-Data Intelligence | Cell-level dual-axis model pretrained on target prediction plus masked-feature reconstruction (CCMM); the 406M model ranks 1st on TabArena (Elo 1,935), TALENT and BCCO with log-linear capacity scaling; feature attention recovers causal skeletons (F1 0.80), not effects. | [pdf](papers/2026/09_Zhang_et_al._LimiX_2_A_Contextual_Mechanism_Network_Towards_General_Structured_Data_Intelligence.pdf) |
| 2026-09 | Cho et al. | **Causilo** — Technical Report | 36M-parameter model that refines cells across rows and features before row compression, with summary-token attention linear in feature count; 1,785 TabArena Elo at 0.10 s per 1K rows, beating TabPFN-3.5-Fast with 31.6% less inference time; weak on BeyondArena grouped splits. | [pdf](papers/2026/09_Cho_et_al._Causilo_Technical_Report.pdf) |
| 2026-09 | Arazi et al. | **MulTaBench**: Benchmarking Multimodal Tabular Learning with Text and Image | Benchmark of 40 text/image-tabular datasets curated so both modalities add signal and target-tuned (LoRA) encoders beat frozen embeddings; the gain generalises to new learners (significant on 37/40 when pooling all learners) and encoder sizes; 40 further candidates released. | [pdf](papers/2026/09_Arazi_et_al._MulTaBench_Benchmarking_Multimodal_Tabular_Learning_with_Text_and_Image.pdf) |
| 2026-09 | Wang et al. | LimiX-2M: Mitigating Low-Rank Collapse and Attention Bottlenecks in Tabular Foundation Models | Radial-basis cell embeddings (RaBEL) fix early low-rank collapse and sample→FFN→feature attention feeds the readout; the 1.92M model beats TabPFN v2 on 9 of 11 suites and TabICL v1 on all comparable ones, ~2× faster than v2 on GPU. ICML 2026. | [pdf](papers/2026/09_Wang_et_al._LimiX_2M_Mitigating_Low_Rank_Collapse_and_Attention_Bottlenecks_in_Tabular_Foundation_Models.pdf) |
| 2026-09 | Hayler et al. | Advancing Open and Reproducible Relational Learning: **RelArena-α**, **TabPFN-Rel** and RPI | Prior Labs' audit of non-comparable RelBench practice, a standardised relational benchmark (21 tasks) and a deep-feature-synthesis + TabPFN-3 harness: TabPFN-Rel tops the model board (Elo 1,821 with text), RT-PluRel tops with systems; reruns cut RelGNN by ~450 Elo. | [pdf](papers/2026/09_Hayler_et_al._Advancing_Open_and_Reproducible_Relational_Learning_RelArena_alpha_TabPFN_Rel_and_RPI.pdf) |
| 2026-09 | Kong et al. (Google) | **TabFM**: A Zero-Shot Foundation Model for Tabular Data | 408.7M row-compression TFM (learned Fourier cell embeddings, two column-ISAB/row-SAB stages, 24-layer ICL predictor) pretrained on SCM tables up to 16,384 × 100; zero-shot first among default TFMs in its TabArena pool (1,769 classification / 2,055 regression Elo), raised further by frozen-weight ensembling (TabFM+) and Gemini-driven program search (TabFM-Auto); no ablations, and the pool omits TabPFN-3.5, LimiX-2 and Causilo; non-commercial weights. | [pdf](papers/2026/09_Kong_et_al._TabFM_A_Zero_Shot_Foundation_Model_for_Tabular_Data.pdf) |
| 2026-10 | Ning et al. | **Test-Time Compute for Tabular Foundation Models: Mechanisms, Gains, and Limits** | Factorises test-time compute into adaptation, aggregation and context: DiagScale (0.003–0.03% of parameters) matches full finetuning on three backbones (+26/+82/+20 Elo); greedy selection over 96 configurations cuts TabPFN-3 error 2.4% where averaging hurts; retrieval helps or fails; combined +93 Elo costs 253 GPU-hours. | [pdf](papers/2026/10_Ning_et_al._Test_Time_Compute_for_Tabular_Foundation_Models_Mechanisms_Gains_and_Limits.pdf) |
| 2026-10 | Zhao et al. | **TabReliBench** — Evaluating Tabular Foundation Models Beyond Predictive Accuracy | Reliability benchmark (160 classification + 81 regression OpenML datasets, 11 TFMs vs BART/RealMLP/XGBoost): rankings shift across metrics; near-nominal marginal coverage but heterogeneous **worst-slab (subgroup) coverage**; ensembling and nine conformal methods do not reliably fix calibration or subgroup gaps. | [pdf](papers/2026/10_Zhao_et_al._TabReliBench_Evaluating_Tabular_Foundation_Models_Beyond_Predictive_Accuracy.pdf) |
| 2026-10 | Cannistraci and Vogt | **Tabular Foundation Models Are Effectively Shallow** | Closed-form, label-free affine maps replace contiguous transformer blocks: half-depth costs ≤0.002 median AUROC across 8 TFMs on 171 datasets and is near-lossless in regression; up to 96% of blocks removable for classification (one-block TabPFN-3 2.4× faster, 6× less memory), but single blocks hurt regression. | [pdf](papers/2026/10_Cannistraci_and_Vogt_Tabular_Foundation_Models_Are_Effectively_Shallow.pdf) |
| 2026-10 | Alberge et al. | **SurvICL**: a Foundation Model for in-context Survival Analysis | TabICLv2 backbone pretrained on a proportional-odds survival prior to output 999 latent event-time quantiles from censored contexts; 82.9% pairwise IBS win rate on 63 held-out datasets (Cox 71.3%), first to rank above Cox on small cohorts; boosting stays stronger above 1,000 samples. | [pdf](papers/2026/10_Alberge_et_al._SurvICL_a_Foundation_Model_for_in_context_Survival_Analysis.pdf) |
| 2026-10 | Deprez et al. | Is TabPFN the Silver Bullet for Insurance Pricing? | Default TabPFN v2.6/v3 vs GLM and fixed XGBoost on two motor-liability datasets: GLMs win claim frequency (Poisson deviance), TabPFN is competitive on scarcer severity data, inference is much slower, and missing offsets/weights handicap the actuarial set-up. | [pdf](papers/2026/10_Deprez_et_al._Is_TabPFN_the_Silver_Bullet_for_Insurance_Pricing.pdf) |
| 2026-10 | Lefebvre et al. | **TILE**: Bridging LLMs and Table Foundation Models for Tabular Learning with Strings | Frozen-LLM interface for string columns: row serialisation, middle-layer extraction, per-column pooling plus numeric/categorical by-passes feed any TFM; +333 Elo over the best of 30 baselines on 100 string tables and the top four places on STRABLE. | [pdf](papers/2026/10_Lefebvre_et_al._TILE_Bridging_LLMs_and_Table_Foundation_Models_for_Tabular_Learning_with_Strings.pdf) |
| 2026-10 | Baesens et al. | **Tabular Foundation Models for Credit Risk Prediction: A Dedicated Review and Empirical Comparison** (v1/v2 title: *Foundation Models for Credit Risk Prediction: A Game Changer?*) | PFN review plus a re-run benchmark of untuned TFMs against tuned baselines on 14 PD and 7 LGD credit datasets (33/27 methods, TFMs included): TabPFN-3 first on both tasks (AUC 0.764 vs CatBoost 0.750; R² 0.537 vs 0.487), gains largest at small samples and rare defaults, but mean PD underpredicted on all 14 datasets. | [pdf](papers/2026/10_Baesens_et_al._Tabular_Foundation_Models_for_Credit_Risk_Prediction_A_Dedicated_Review_and_Empirical_Comparison.pdf) |
| 2026-10 | Bouadi et al. | **O'Prior** — Shaping the Prior: How Synthetic Task Distributions Determine TFM Quality (v2; first released May) | **Controlled prior study** on nanoTabPFN: architecture, optimiser and budget fixed, only the synthetic task distribution varied. Mechanism diversity drives transfer most (Hybrid SCM alone: TabArena ROC-AUC 0.834 vs 0.791 for the TabICL-v2 prior); the full curriculum does not beat the best single components. | [pdf](papers/2026/10_Bouadi_et_al._Shaping_the_Prior_How_Synthetic_Task_Distributions_Determine_Tabular_Foundation_Model_Quality.pdf) |

---

<a id="pfns-2021"></a>

## 2021-12 — Müller et al. — Transformers Can Do Bayesian Inference

**Venue:** ICLR 2022 · **arXiv:** [2112.10510](https://arxiv.org/abs/2112.10510) (filed PDF: ICLR conference version, no arXiv banner) · **PDF:**
[open](papers/2021/12_Muller_et_al._Transformers_Can_Do_Bayesian_Inference.pdf)

**Citation key:** `2022.MULLER.transformerscanbayesianinference`

**Provenance.** First public release: 20 December 2021; publication: ICLR 2022. The filed conference PDF has no exact revision date. The historical path and chronology use the first release, not an inferred PDF month; its hash and evidence are recorded in `papers/filing_overrides.json`.

**Where it fits.** The bedrock of the entire PFN / TabPFN line. Müller and colleagues introduce
*Prior-Data Fitted Networks* (PFNs): transformers that, after a single training phase on synthetic
datasets sampled from a prior, approximate the posterior predictive distribution (PPD) *in
context* for any new dataset — without any parameter update. Every later model in this collection,
from [Hollmann 2023, *TabPFN*](#tabpfn-v1) onward, is an instance of this recipe;
[Nagler 2023, *Statistical Foundations of Prior-Data Fitted Networks*](#nagler-theory) supplies
the frequentist account of why it generalises.

**What it contains.** *Prior-fitting* (Algorithm 1): repeatedly sample a dataset D ∪ {(x, y)}
from the prior p(D) — any process the researcher can sample from, with no need for a likelihood
or posterior density — feed the labelled points D plus the held-out query x to the network, and
minimise the negative log-likelihood of y (the *Prior-Data NLL*). Insight 1 and Cor. 1.1 show this
loss equals the expected cross-entropy, hence (up to a constant) the expected KL divergence,
between the true PPD and the network's prediction; Cor. 1.2 says the optimum recovers the PPD if
the model family contains it. Architecture (§4): a transformer encoder **without positional
encodings**, so predictions are invariant to the order of the training points; each (x, y) pair is
a linearly embedded token, training tokens attend to each other and each query attends only to
the training tokens. For regression the head outputs a **Riemann distribution** — a piecewise
constant density over fixed buckets (Theorem 1: it can approximate any Riemann-integrable density).
Experiments: GP regression against the exact GP posterior; BNN priors (including priors over
architectures) against NUTS and SVI; small tabular classification (§6); and 5-way 5-shot Omniglot
with a 55-line "random strokes" prior plus fine-tuning (§7). For the tabular study, inputs are
zero-padded to a fixed maximum of 60 features (App. G).

**Key results.** Inference is more than 200× faster than MLE-II and 1,000–8,000× faster than
NUTS at comparable approximation quality (§5, Fig. 5). On 20 OpenML AutoML Benchmark datasets
simplified to balanced binary tasks with 30 labelled training points (Table 1), the BNN-prior PFN
has the best mean ROC-AUC rank (2.786 vs XGBoost 3.357 and PFN-GP 3.833), the lowest expected
calibration error (0.025 vs 0.066 for XGBoost), and needs 13 s of GPU time for all datasets
versus about 20 h for tuned XGBoost (>5,000×, §6). On Omniglot it reaches 0.865 accuracy, within
the confidence interval of PACOH-NN's 0.885 (Table 2).

**Strengths.** A clean theoretical justification (the training loss is a KL to the true PPD,
estimated on fresh prior draws at every step, so there is no fixed training set to overfit) and a
practical one: inference is a single forward pass, sidestepping MCMC for non-conjugate priors and
per-task variational fitting. It demonstrates priors that are hard to use in classical Bayesian
inference (distributions over BNN architectures, handwriting-like strokes).

**Limitations.** Author-stated (§8): the architecture is only a slight adaptation of a standard
transformer, and scaling to larger real-world problems is left open. Reviewer reading: the tabular
evidence is tiny-scale — 30 labelled rows, ≤60 (zero-padded) features, balanced binary targets,
datasets with missing values excluded — and the GP/BNN priors are simple; quadratic attention in
the number of points bounds the context.

---

<a id="pfns4bo"></a>

## 2023-05 — Müller et al. — PFNs4BO

**Venue:** ICML 2023 (PMLR 202) · **arXiv:** [2305.17535](https://arxiv.org/abs/2305.17535) (filed PDF: PMLR proceedings version) · **PDF:**
[open](papers/2023/05_Muller_et_al._PFNs4BO_In_Context_Learning_for_Bayesian_Optimization.pdf)

**Citation key:** `2023.MULLER.pfns4boincontextlearningbayesianoptimization`

**Where it fits.** Sister paper to [Hollmann 2023, *TabPFN*](#tabpfn-v1): the
[PFN recipe](#pfns-2021) applied to a different problem, the surrogate model in Bayesian
optimisation (BO). It shows that the "design the prior, amortise the posterior" idea is not
tabular-specific, and it introduces prior-side tricks (spurious features, user priors) that
later tabular priors reuse in spirit.

**What it contains.** A single PFN is prior-fitted on synthetic (configuration, value) datasets and
then used as a drop-in replacement for the GP surrogate in a BO loop: given the evaluations so far,
one forward pass returns a Riemann (bar) predictive distribution at candidate configurations, from
which EI, PI or UCB can be computed exactly (§3.4; simple EI worked most robustly). Gradients through
the network are used at suggestion time to optimise the acquisition function and to tune a
Kumaraswamy input warping per feature (§3.5). Three priors (§4): a fixed-hyperparameter **GP**
(RBF), a **HEBO-inspired** GP prior with sampled lengthscales, output scale and noise (Matérn-3/2),
and its tuned extension **HEBO+**, and a **BNN** prior with sampled architectures. Prior extensions
(§5) are things that are awkward for a GP: warping inside the prior, **spurious dimensions** (HEBO+
uses 30% irrelevant features), **user priors** — an interval believed to contain the optimum plus a
confidence ρ, fed as an extra input so one network serves any interval — and a learned
approximation of the non-myopic knowledge-gradient acquisition. Evaluation: GP samples and three
HPO testbeds — HPO-B (9 test search spaces, 51 tasks), Bayesmark (36 continuous tasks) and PD1
(neural-network HPO, 18 tasks).

**Key results.** Against an empirical-Bayes GP on GP-prior functions, most runs tie and the PFN
wins slightly more often than it loses (Table 1). On HPO-B the BNN prior performs similar to the
best baseline while the HEBO+ prior outperforms all baselines (§7.1, Fig. 4). On Bayesmark the
HEBO+ PFN is comparable to or slightly worse than HEBO with a Sobol initial design, and a
single-point initial design in the lower corner was clearly best (§7.2, Fig. 5). On PD1 the BNN-prior PFN
is clearly outperformed by HEBO while the HEBO+ PFN performs better, and a generic user prior
yields strong further gains (§7.3, Fig. 4).

**Strengths.** Encodes priors a GP cannot easily express (distributions over BNN architectures,
spurious features, beliefs about the optimum's location) by changing the sampler rather than the
inference code; inference stays a single forward pass, and code and trained models are published.

**Limitations.** Author-stated (§8): PFNs work worse on data that is very unlikely under the
prior; no setting was found that recovers mislabelled log dimensions while staying strong on
correctly specified spaces, so inference-time input warping is used only on HPO-B; no joint
samples over several points (blocking, e.g., noisy EI); results focus on accuracy-type objectives
and seem worse for others; PFNs had only been shown to work up to about 1,000 data points.
Reviewer reading: about 10% of HPO-B hyperparameters lack a needed log scale (§7.1), so HPO-B
results partly measure the warping fix rather than standard BO.

---

<a id="nagler-theory"></a>

## 2023-07 — Nagler — Statistical Foundations of Prior-Data Fitted Networks

**Venue:** ICML 2023 (PMLR 202) · Thomas Nagler, LMU Munich / Munich Center for Machine
Learning · **arXiv:** [2305.11097](https://arxiv.org/abs/2305.11097) (filed PDF: PMLR proceedings version) · **PDF:**
[open](papers/2023/07_Nagler_Statistical_Foundations_of_Prior_Data_Fitted_Networks.pdf)

**Citation key:** `2023.NAGLER.statisticalfoundationspriordatafittednetworks`

**Where it fits.** The theory paper the rest of this corpus leans on without always citing.
[Müller 2021, *Transformers Can Do Bayesian Inference*](#pfns-2021) justified PFNs with a
Bayesian argument; Nagler asks what actually happens statistically and arrives at a
*frequentist* reading that explains a puzzle the Bayesian argument does not: TabPFN was
pretrained on datasets of up to about 1,000 rows yet keeps improving when given larger training
sets at inference (§1.2).

**What it contains.** §2–4 define the PPD, its PFN approximation (characterised by a
Kullback–Leibler criterion) and when a PPD itself can learn (Theorem 3.1: enough prior support
and no concentration away from the truth). The central move (§5) is to stop treating the network
as an approximate posterior and treat it as a **pre-tuned but untrained predictor** — a fixed
function of the context set whose "hyperparameters" were tuned during pretraining for the tasks
the prior describes. The usual bias–variance decomposition then gives two conditions:

* **Variance vanishes** if the predictor's sensitivity to any *individual* training sample
vanishes as the context grows (Theorem 5.2). Attention averaging over context rows delivers this
for transformers regardless of the tuned weights (Theorems 6.2–6.3).
* **Bias vanishes only if the predictor is appropriately *localised* around the test feature**
(Theorem 5.4) — nearby context points must dominate, and distant ones must eventually stop
mattering. **Transformer PFNs do not guarantee this**: attention upweights similar samples but
never removes the influence of distant ones (§6.3).

§6 works through window smoothers, classification trees and transformers: multi-head attention
allows implicit selection or averaging over sub-models, which can make bias fall — but only for
sample sizes the weights were tuned to. A simple post-hoc fix (§6.4) is a **localised PFN** that
keeps only the k_n nearest neighbours of the query as context.

**Key results.** Numerical validation (§6.5, Fig. 1): 500 simulated binary datasets with
p₀(1 | X) = ½ + sin(1ᵀX)/2, X ~ N(0, I₅), run through the pip-released TabPFN v1 (0.1.8). The
variance decreases at rate 1/n; the squared bias decreases until n ≈ 1,000 and then stops
falling. With localisation (k_n = min{500, ⌈n^{4/(d+4)}⌉}) the bias keeps decreasing beyond
n = 1,000 at the cost of slightly larger variance. Beyond n ≈ 1,000, TabPFN therefore learns
mainly by reducing variance.

**Strengths.** A rigorous, constructive account: it explains in-context improvement beyond the
pretraining sizes, predicts a bias plateau, and names the fix (localisation, ideally built into
pretraining, §7). Reviewer reading: the later retrieval-based models —
[Thomas 2024, *LoCalPFN*](#localpfn) and [Ma 2026, *TabDPT*](#tabdpt) — can be read as that fix
arrived at empirically, although they do not derive it from this paper.

**Limitations.** Author-stated: posterior contraction under the nonparametric SCM prior is left
open (§7), and the empirical check is a single synthetic five-dimensional function. Reviewer
reading: the results are asymptotic, concern classification with a fixed pretraining
distribution, and do not quantify how much bias a given architecture carries on a given table.
The analysis targets the v1-era single-attention-axis architecture; the argument is about
attention-based context aggregation in general and plausibly transfers, but it is not re-tested
on v2 or later models here.

---

<a id="tabpfn-v1"></a>

## 2023-09 — Hollmann et al. — TabPFN

**Venue:** ICLR 2023 · **arXiv:** [2207.01848](https://arxiv.org/abs/2207.01848) (filed v6, 16 September 2023) · **PDF:**
[open](papers/2023/09_Hollmann_et_al._TabPFN_A_Transformer_That_Solves_Small_Tabular_Classification_Problems_in_a_Second.pdf)

**Citation key:** `2023.HOLLMANN.tabpfntransformerthatsolvessmalltabularclassificationproblemssecond`

**Where it fits.** The first TabPFN: the [PFN recipe](#pfns-2021) applied to small tabular
classification with a prior designed for tabular data. It established the paradigm every later
TFM here refines — synthetic-only pretraining, no per-dataset training, one forward pass — and
its stated limits (size, categoricals, missing values, regression) set the agenda for
[TabPFN v2](#tabpfn-v2-nature).

**What it contains.** The model is a 12-layer transformer that takes the labelled training rows
and the unlabelled test rows as one input set; each row (features plus label) is a token,
training tokens attend to each other and test tokens attend to the training tokens, and the
output is a class distribution for every test row (§2–3). Fewer features than the maximum are
zero-padded. The **prior** (§4) is a 50/50 mixture of **structural causal models** — a random DAG
whose nodes apply sampled mechanisms and noise, with some nodes selected as features and one as
the target, so the target may be a cause or an effect of features — and **BNNs** (random networks
with sampled architectures). Almost all prior hyperparameters are themselves sampled, so the
model integrates over them; simplicity (few nodes and parameters) is favoured; continuous targets
are discretised into classes; App. C adds correlated/categorical features, exponential scaling and
missing values. Prior-fitting ran for 18,000 batches of 512 synthetic datasets, about 20 h on
8 RTX 2080 Ti GPUs, once; the synthetic datasets had at most 1,024 rows. At inference TabPFN
ensembles 32 forward passes with power-transformed inputs (probability 0.5) and rotated feature
and class indices.

**Key results.** On the 18 OpenML-CC18 datasets with ≤1,000 training rows, ≤100 purely numerical
features, no missing values and ≤10 classes (Table 1, 60-minute budgets for baselines): mean
ROC-AUC (OVO) 0.934 for TabPFN versus 0.930 AutoGluon, 0.929 Auto-sklearn 2.0, 0.924 CatBoost and
XGBoost; mean rank 2.94 versus 4.0 AutoGluon. TabPFN takes 0.62 s on a GPU per dataset (1.30 s CPU /
0.05 s GPU without ensembling); matching the strongest baselines at five minutes amounts to 230×
(CPU) and 5,700× (GPU) speedups (§5). Averaging TabPFN with AutoGluon is best overall. On small
OpenML-AutoML Benchmark datasets it beats all baselines in mean cross-entropy, accuracy and the
OpenML metric in 4.4 s per dataset on CPU, and results are validated on 67 further small numerical
OpenML datasets. It also generalises to training sets of up to 5,000 rows, larger than any seen
in pretraining (App. B.1, Fig. 10).

**Strengths.** One pretrained network, no tuning, sub-second predictions competitive with
one-hour AutoML on small numerical tasks; its errors are weakly correlated with those of GBDTs,
which makes it a cheap ensemble member; qualitative analyses (App. B.3) show smooth, intuitive
decision boundaries biased towards simple causal explanations. Code, weights and an sklearn
interface were released.

**Limitations.** Author-stated (§6, App. A): quadratic attention limits it to small datasets;
evaluation covers only ≤1,000 training rows, ≤100 numerical features and ≤10 classes,
classification only; performance is generally worse with categorical features or missing values,
and robustness to uninformative features is weak. Reviewer reading: the headline benchmark is 18
datasets after filtering out the cases TabPFN handles worse (12 of the 30 small CC18 datasets,
reported only in App. B.1), and the margin over AutoML is within the reported standard deviations.

---

<a id="rundel-iml"></a>

## 2024-03 — Rundel et al. — Interpretable Machine Learning for TabPFN

**Venue:** xAI 2024 (Springer CCIS 2154, pp. 465–476) · **arXiv:** [2403.10923](https://arxiv.org/abs/2403.10923) (filed PDF: Springer chapter version) · **DOI:** [10.1007/978-3-031-63797-1_23](https://doi.org/10.1007/978-3-031-63797-1_23) · **PDF:**
[open](papers/2024/03_Rundel_et_al._Interpretable_Machine_Learning_for_TabPFN.pdf)

**Citation key:** `2024.RUNDEL.interpretablemachinelearningtabpfn`

**Where it fits.** The first interpretability toolkit built around a PFN's in-context inference,
for [TabPFN v1](#tabpfn-v1). Its core observation — that refitting an in-context model on a
subset is a forward pass, not a training run — applies to every later TFM in this collection.

**What it contains.** For a PFN, "training on" a feature subset or a row subset just means
running the forward pass with a different context. The paper exploits this to adapt standard
interpretable-ML methods (Table 1; binary classification throughout):
* **ICE, PD and ALE** computed in a single forward pass by stacking every grid-modified query
row into one inference batch, instead of one prediction call per grid point (§3.1).
* **LOCO** and **leave-one-out** become tractable because dropping a feature or a training row
needs no retraining (§3.2, §3.4).
* **Kernel SHAP** and **SAGE** use *exact retraining*: each coalition is evaluated by removing
the absent features from both context and queries, rather than imputing them with background
samples (§3.3).
* **Data Shapley** is implemented as Kernel SHAP over training rows and used for **context
optimisation** — choosing which rows to put in TabPFN's ~1,000-row context when the training
set is larger (§3.4).

Sensitivity analysis, decision-curve analysis, conformal prediction and MOC counterfactuals are
included unmodified. Everything ships as the `tabpfn_iml` package.

**Key results.** Single-pass ICE/PD is substantially faster than scikit-learn's
`partial_dependence` as grid or data size grows (§4.1, Fig. 1). On three OpenML-CC18 binary tasks
with six numerical features (n_train = 256, n_inf = 128, 25 repetitions), exact retraining almost
always gives lower Shapley approximation error at a fixed budget, converges to lower error and
has lower variance than approximate (imputation) retraining (§4.2, Fig. 2). Data-Shapley context
optimisation (n_train = 3,072, 512-row context, five repetitions) beats random contexts by 0.57%
(eeg-eye-state), 1.52% (albert) and 3.3% (higgs) ROC-AUC (§4.3, Fig. 3).

**Strengths.** Makes attributions faithful to the model actually deployed (no imputation
artefacts) while also making them cheaper; turns data valuation into a practical way to build
contexts; open implementation.

**Limitations.** Author-stated: the Data-Shapley procedure needs nearly 10,000 TabPFN forward
passes, far costlier than the other methods (§4.3); exact Shapley values scale exponentially with
features, so the comparison uses six-feature datasets. Reviewer reading: binary classification
only, TabPFN v1 only, three datasets per experiment, and no comparison of context optimisation
against the prompt-tuning alternative ([Feuer 2024, *TuneTables*](#tunetables)).

---

<a id="breugel-position"></a>

## 2024-06 — Breugel and Schaar — Why Tabular Foundation Models Should Be a Research Priority

**Venue:** ICML 2024 (PMLR 235, pp. 48976–48993; published as *Position: Why Tabular Foundation Models Should Be a Research Priority*), position paper · **arXiv:** [2405.01147](https://arxiv.org/abs/2405.01147) (filed v2, 2 June 2024) · **PDF:**
[open](papers/2024/06_Breugel_and_Schaar_Why_Tabular_Foundation_Models_Should_Be_a_Research_Priority.pdf)

**Citation key:** `2024.VANBREUGEL.whytabularfoundationmodelsshouldberesearchpriority`

**Where it fits.** Position / agenda paper written between [TabPFN v1](#tabpfn-v1) and
[TabPFN v2](#tabpfn-v2-nature). It argues that tabular foundation models are under-researched
relative to text and vision despite tabular data being the dominant modality in many fields, and
supplies a vocabulary and checklist later work implicitly answers.

**What it contains.** Coins **Large Tabular Model (LTM)** for a tabular foundation model, scoped
to single independent tables rather than relational databases (§2). Four desiderata (§2.1):
**D1** mixed-type columns (numerical, categorical, datetime, missing); **D2** cross-dataset
modelling over heterogeneous feature spaces; **D3** use of textual context (dataset description,
column and category names); **D4** invariance or equivariance to column order. **Three hypothesised
reasons** LTMs were overlooked (§1): data (few large tabular metadatasets, messy or unlabelled
tables, privacy/ownership gaps), the difficulty of tabular ML (strong baselines that new methods do
not consistently beat), and human perception (text and image outputs are easy to judge by eye,
tables are not). §3 reviews representation-learning, supervised (including TabPFN) and generative
approaches against D1–D4 and argues (Fig. 2) that autoregressive LLMs are an inefficient way to
sample continuous values. §4 distinguishes **direct** adaptation (fine-tuning or in-context
prediction) from **indirect** adaptation via synthetic data and discusses responsible-AI and
scientific uses; §5 lists challenges (generative LTMs, scale, data diversity and quality,
evaluation, bias); §6 compares LTM and LLM impact on five axes; App. B gives taxonomies of
evaluation tasks and settings (few-shot, zero-shot, in-distribution, …).

**Key results.** None quantitative beyond Fig. 1, a rough keyword count of accepted conference
papers by modality showing tabular foundation-model work heavily under-represented (App. A).

**Strengths.** A crisp, reusable design and evaluation checklist (D1–D4, adaptation and benchmark
taxonomies). D3 and D4 anticipate later semantic models ([Kim 2024, *CARTE*](#carte-pretraining-and),
[Spinaci 2025, *ConTextTab*](#contexttab)) and the symmetry concerns later formalised for targets
by [Arbel 2025, *EquiTabPFN*](#equitabpfn).

**Limitations.** Author-stated (§5): current models train on few datasets and are evaluated on
one task; whether web-scale table corpora are diverse enough, and whether proprietary or sensitive
domains (e.g. medicine) will be covered, is unknown; intrinsic evaluation of LTMs is hard.
Reviewer reading: purely argumentative, restricted to single tables, and written before the
synthetic-prior line had shown how far it could scale, so its emphasis on large real-table
corpora and generation reflects 2024 expectations rather than tested claims.

---

<a id="carte-pretraining-and"></a>

## 2024-07 — Kim et al. — CARTE: Pretraining and Transfer for Tabular Learning

**Venue:** ICML 2024 (PMLR 235, pp. 23843–23866) · **arXiv:** [2402.16785](https://arxiv.org/abs/2402.16785) (filed PDF: PMLR proceedings version; July 2024 follows the curated conference record, not an inferred arXiv revision) · [Primary record](https://proceedings.mlr.press/v235/kim24d.html) · **PDF:** [open](papers/2024/07_Kim_et_al._CARTE_Pretraining_and_Transfer_for_Tabular_Learning.pdf)

**Citation key:** `2024.KIM.cartepretrainingtransfertabularlearning`

**Where it fits.** A separate transfer branch alongside PFNs: CARTE pretrains *semantic*
representations on an external knowledge base and then fine-tunes them for each target table,
rather than approximating a synthetic-prior posterior through frozen in-context learning. It is
the earliest paper here that treats column names and string entries as signal, the line later
continued by [Arazi 2025, *TabSTAR*](#tabstar) and [Spinaci 2025, *ConTextTab*](#contexttab).

**What it contains.** *Representation* (§3.1): each row becomes a star-shaped **graphlet** — a
centre node linked to one leaf per non-missing cell, with the column name on the edge. Column
names and categorical/string values are embedded with a language model (FastText); a numerical
value is encoded as the value times its column-name embedding. Missing cells simply drop their
leaf, so no imputation is needed. *Architecture*: graph attention whose messages are conditioned
on the edge (column) embedding, followed by an aggregation-and-readout layer. *Pretraining*
(§3.2): self-supervised contrastive learning on graphlets extracted from **YAGO3** (over 18.1
million triplets of 6.3 million entities), with truncated graphlets as positives and other
graphlets in the batch as negatives. *Fine-tuning* (§3.3): only the initial node/edge layers and
the readout are kept (one attention layer, to avoid over-smoothing on simple star graphs), a linear
head is added, numerical inputs are Yeo–Johnson transformed, and predictions are bagged over
models with different early-stopping splits. For **transfer**, CARTE is fine-tuned jointly on a
target and a weakly related source table without column or entity matching, and the single-table
and pairwise learners are combined by a validation-weighted softmax.

**Key results.** On 51 string-rich tables (40 regression, 11 classification), CARTE has the best
normalised score and critical-difference rank across training sizes against 42 baselines,
including tuned XGBoost/CatBoost/RF, skrub's TableVectorizer and LLM row embeddings (§4.2, Fig. 4,
App. C.1). With 10–30% of cells randomly dropped it degrades less than CatBoost and TableVectorizer
pipelines (Table 1). It does not need manual entity matching (Fig. 5) or schema matching for
transfer, and adding up to three source tables improves median and worst-case gains (§4.3,
Figs. 7–8). On nine mostly numerical TabLLM datasets, TabPFN ranks first and CARTE is competitive
(Fig. 6).

**Strengths.** Makes names and string semantics transferable across mismatched schemas and
entity spellings, handles missing values natively, and is backed by component ablations and
broad baselines; [official code](https://github.com/soda-inria/carte) and the benchmark are public.

**Limitations.** Author-stated: much higher compute than the baselines — about 85 s (n = 64) and
315 s (n = 512) of learning time per dataset versus about 1 s for CatBoost (Table 2) — and the
edge is on string-rich tables, while TabPFN shines on heavily numerical ones. Reviewer reading:
external knowledge and pretrained string embeddings change the information budget relative to
anonymous-column PFNs; it requires supervised fine-tuning, not training-free ICL; and the
benchmark was selected for meaningful string columns, so gains need not carry to arbitrary
numerical tables.

---

<a id="tabforestpfn"></a>

## 2024-10 — den Breejen et al. — TabForestPFN

**Venue:** ICLR 2025 submission, OpenReview `pE0UM18TQh` · **arXiv:** [2405.13396](https://arxiv.org/abs/2405.13396) (filed PDF: anonymous double-blind review version, not an arXiv revision) · **PDF:**
[open](papers/2024/10_Breejen_et_al._Fine_tuned_In_Context_Learning_Transformers_are_Excellent_Tabular_Data_Classifiers.pdf)

**Citation key:** `2024.DENBREEJEN.finetunedincontextlearningtransformersareexcellenttabulardataclassifiers`

**Where it fits.** An early **tree-based synthetic prior** mixed with TabPFN's SCM prior — cited
by [Zhang 2025, *Mitra*](#mitra) alongside Attic and TabICL as a precursor that adopted tree
priors heuristically — and an early argument that fine-tuning ICL transformers is worthwhile
rather than a compromise.

**What it contains.** Model: a TabPFN-v1-style ICL transformer (support rows and query rows as
tokens; support attends to support, each query to the support set and itself), retrained by the
authors. Two findings interact:

* **Fine-tuning gives ICL transformers complex decision boundaries.** Fine-tuning on the target
dataset — each gradient step draws a random 80/20 support/query split of the training data, with
early stopping on validation loss that can stop at step 0 and fall back to zero-shot (§4.2) —
boosts performance and yields decision boundaries more complex than zero-shot ones (§5.3).
* **So pretrain on data with complex boundaries, even if unrealistic.** The **forest dataset
generator** (Algorithm 1) fits a decision tree of depth 1–25 to 1,024 random Gaussian points with
random targets, then labels 128–1,024 fresh Gaussian points with that tree (optionally making some
features categorical) and discretises the quantile-transformed outputs into 2–10 classes with
random boundaries (Table 1; 3–100 features). The data are deliberately unrealistic: axis-aligned
boundaries, no feature correlation. **TabForest** is pretrained on this generator alone;
**TabForestPFN** on a mix of the TabPFN and forest generators.

**Key results.** Benchmarks: 94 of the 176 TabZilla classification datasets and the 23 WhyTrees
(Grinsztajn et al.) datasets of 2,923–10,000 rows; ICL models use default settings, baselines get
random search. On WhyTrees (Table 2), fine-tuned TabForest is best among ICL variants (normalised
accuracy 0.853 mixed / 0.854 numerical) and TabForestPFN close behind (0.842 / 0.849), versus
0.775 / 0.817 for fine-tuned retrained TabPFN — although zero-shot TabForest is far weaker (0.388 /
0.536). On TabZilla (Table 3), fine-tuned TabForestPFN and fine-tuned retrained TabPFN share the
best mean rank (8.4), with mean normalised accuracy 0.840 and 0.843 versus CatBoost 0.842 and
XGBoost 0.836. Fine-tuning beats zero-shot on 57% of TabZilla datasets — 47% below 1,000 rows,
73% above — and clearly when there are more than 10,000 rows; a larger support set always helped,
so 8,192 is used despite pretraining at ≤1,024 (§5.6).

**Strengths.** The insight worth carrying: prior realism buys zero-shot quality while prior
*complexity* buys adaptability, and the two are different axes. Mixing the forest data in does
not appear to hurt zero-shot performance, so the combination costs little.

**Limitations.** Author-stated (§6): classification only; GPU memory still limits ICL context, and
fine-tuning is not compared with prompt tuning ([Feuer 2024, *TuneTables*](#tunetables)) or
retrieval ([Thomas 2024, *LoCalPFN*](#localpfn)); very wide tables and feature importance are
untested. Reviewer reading: the filed copy is an anonymous review version, so final numbers may
differ; on TabZilla the forest prior does not beat plain retrained TabPFN after fine-tuning; and
the gains are demonstrated in the fine-tuning regime, so they do not carry over to frozen-ICL
deployment.

---

<a id="drift-resilient-tabpfn"></a>

## 2024-11 — Helli et al. — Drift-Resilient TabPFN

**Venue:** NeurIPS 2024 · **arXiv:** [2411.10634](https://arxiv.org/abs/2411.10634) (filed v1, 15 November 2024) · **DOI:** [10.52202/079017-3134](https://doi.org/10.52202/079017-3134) · **PDF:** [open](papers/2024/11_Helli_et_al._Drift_Resilient_TabPFN_In_Context_Learning_Temporal_Distribution_Shifts_on_Tabular_Data_1.pdf)

**Citation key:** `2024.HELLI.driftresilienttabpfnincontextlearningtemporaldistributionshiftstabulardata`

**Where it fits.** The first TabPFN variant whose *prior* encodes distribution shift: instead of
assuming i.i.d. train and test data, it learns in context how a data-generating process drifts
over ordered temporal domains and extrapolates that drift. It is built on the TabPFN v1
architecture ([Hollmann et al. 2023, *TabPFN*](#tabpfn-v1)); the later temporal-shift evidence in
[Rubachev et al. 2025, *On Finetuning Tabular Foundation Models*](#on-finetuning) and
[Purucker et al. 2026, *Beyond IID*](#beyond-iid) addresses the same failure mode from the
evaluation side.

**What it contains.** Each pretraining dataset is an aggregation of per-domain datasets
`D_c1 … D_cn`, where every row carries a temporal domain index c. The base SCM of the TabPFN prior
is made time-dependent: a sparse subset of its causal edges is selected for shifting, and a
randomly generated **2nd-order SCM** — itself an SCM, run forward only — takes the domain index as
input and outputs the weight shifts of those edges (§3.2, Fig. 3). Because the 2nd-order SCM is
nonlinear and its nodes are correlated, the sampled shifts are smooth, correlated and
extrapolable, and shifting edges covers covariate shift, prior-probability shift, concept shift
and combinations. Domain indices are encoded with Time2Vec. Training domains precede test domains,
so the transformer is trained to predict *future* domains from past ones in a single forward pass.
Pretraining matches the base TabPFN budget (30 epochs on 8 GPUs, 30.72M synthetic datasets);
preprocessing settings were chosen once by random search over 300 configurations on 12 validation
datasets (§4). At inference, synthetic datasets have known domain indices; for real-world data they
are approximated by discretising time-encoding features, and large real datasets are subsampled.

**Key results.** On 18 test datasets (8 synthetic, 10 real-world), against GBDTs tuned for
1,200 s, unmodified TabPFN and Wild-Time methods, OOD accuracy rises from 0.688 to 0.744, OOD ROC
AUC from 0.786 to 0.832 and OOD ECE falls from 0.119 to 0.091, each vs the strongest baseline
(TabPFN given the domain index; Table 5). By subset (Table 1): synthetic accuracy 0.665→0.754 and
ROC 0.749→0.844; real-world accuracy 0.712→0.736 but ROC only 0.82→0.822, ECE 0.083→0.062.
Training plus prediction takes 10.9 s on average. A Time2Vec ablation shows at most slight gains:
the improvement comes from the prior (§4, App. A.4.1).

**Strengths.** A clean demonstration that a shift *type* can be put into the prior and learned
in context, with no deploy-time tuning, and that calibration improves out of distribution (the
model lowers its confidence as it extrapolates further, Fig. 5). Code and weights are released.

**Limitations.** Author-stated: quadratic attention in the number of samples limits it to small
data; the model is a black box with respect to the shifts it detects; sparse mechanism shifts in an
SCM may not describe real-world drift. Reviewer reading: the real-world gains are small (ROC +0.002)
and concentrated on synthetic data whose shifts resemble the prior; in-distribution accuracy is
slightly below base TabPFN (0.879 vs 0.885, Table 5); it requires a temporal domain index
(approximated on real data); classification only, on the v1 architecture.

---

<a id="tabpfn-ts-2024"></a>

## 2024-12 — Hoo et al. — TabPFN Outperforms Specialized Time Series Forecasting Models

**Venue:** NeurIPS 2024 Workshop on Time Series in the Age of Large Models (OpenReview
`ho8Yx5YfiM`); no separate arXiv record of this workshop version is confirmed — the expanded paper
is [arXiv:2501.02945](https://arxiv.org/abs/2501.02945), filed here as
[Hoo et al. 2026, *From Tables to Time*](#from-tables-to-time) · **PDF:** [open](papers/2024/12_Hoo_et_al._The_Tabular_Foundation_Model_TabPFN_Outperforms_Specialized_Time_Series_Forecasting_Models_Based_on.pdf) (filed PDF: workshop version)

**Citation key:** `2024.HOO.tabularfoundationmodeltabpfnoutperformsspecializedtimeseriesforecastingmodelsbasedsimplefeatures`

**Where it fits.** A short application paper, not a new model: it shows that a frozen tabular
foundation model, with no time-series pretraining, competes with dedicated time-series foundation
models once forecasting is reframed as tabular regression. It is the seed of the TabPFN-TS line
continued in *From Tables to Time*.

**What it contains.** **TabPFN-TS** treats each univariate series as its own table (§3). Rows are
time steps; features are derived **only from the timestamp**: a running index plus calendar
features (year raw; hour of day, day of week, day of month, day of year, week of year and month as
sine/cosine pairs with their natural periods). Lags and rolling statistics are deliberately excluded
because they would require unknown future values in non-autoregressive multi-step forecasting. The
history rows form the context, the future timestamps are the queries, and the TabPFN regressor
predicts the whole horizon in one pass; the median of TabPFN's predictive distribution is used
because the metric is MAE-based. The model is a then-unpublished TabPFN regression version
accessed through the hosted `tabpfn-client` endpoint (footnote 2, §4); it is local (no information
shared across series) and unbatched, so every series is processed separately.

**Key results.** On 24 of the 29 AutoGluon-TS benchmark datasets (5 excluded because TabPFN-TS
could not finish within the 4-hour limit), TabPFN-TS has the best geometric-mean relative MASE (0.759; Fig. 2),
which the authors report as 7.7% better than Chronos-Mini (20M) and 3.0% better than Chronos-Large
(710M), with 11M parameters; DeepAR, AutoETS and TFT trail further (§4.1). Splitting by
Chronos's in-domain/zero-shot partition (Fig. 5), Chronos-Large wins on its 7 in-domain datasets
(0.677 vs 0.728) and TabPFN-TS wins on the 17 zero-shot ones (0.772 vs 0.841). Ablations: index-only
features score 1.059, worse than Seasonal Naive (Fig. 3); swapping TabPFN for CatBoost on 16
datasets gives 1.100–1.119 vs 0.744 (Fig. 4).

**Strengths.** Very simple, reproducible recipe (Colab notebook) whose gain is shown to be
TabPFN-specific rather than a property of the features; synthetic-only pretraining removes the
benchmark-contamination question that affects real-data time-series models.

**Limitations.** Author-stated: point-forecast accuracy only (quantile accuracy left to future
work); each series processed individually, so latency is high (Table 3: average 2,210 s per dataset
vs Chronos-Large 148 s and Chronos-Mini 14 s). Reviewer reading: four-page workshop evidence on one
benchmark; local univariate modelling with no covariates or cross-series learning; reliance on an
unreleased, hosted checkpoint; no confidence intervals beyond Fig. 2's aggregate.

---

<a id="tunetables"></a>

## 2024-12 — Feuer et al. — TuneTables

**Venue:** NeurIPS 2024 · NYU / U. Freiburg / U. Maryland / Abacus.AI · **arXiv:** [2402.11137](https://arxiv.org/abs/2402.11137) (filed PDF: NeurIPS proceedings version) · **DOI:** [10.52202/079017-2654](https://doi.org/10.52202/079017-2654) · **PDF:** [open](papers/2024/12_Feuer_et_al._TuneTables_Context_Optimization_for_Scalable_Prior_Data_Fitted_Networks.pdf)

**Citation key:** `2024.FEUER.tunetablescontextoptimizationscalablepriordatafittednetworks`

**Where it fits.** The paper that defined the *context-optimisation* branch of TFM adaptation.
Where [Thomas et al. 2024, *LoCalPFN*](#localpfn) localises the context by retrieval and
[Garg et al. 2025, *Real-TabPFN*](#real-tabpfn) changes the weights, TuneTables changes what the
context *is* — a third answer to "how do you adapt a frozen PFN?". Its parameter-efficiency premise
was later questioned for TabPFN v2 by
[Rubachev et al. 2025, *On Finetuning Tabular Foundation Models*](#on-finetuning).

**What it contains.** TabPFN v1 is limited to about 1,000 training rows, 100 features and 10
classes; sketching (subsampling, as in the TabPFNs3000 baseline) and feature selection only partly
work around it (§2). TuneTables applies **soft prompt tuning** to a PFN (§3): a learned matrix of p
synthetic rows in TabPFN's embedding space, with labels initialised class-balanced, is optimised by
gradient descent on the *entire* labelled set while the transformer stays frozen. The large dataset
is thereby distilled into a small learned context. At test time the tuned prompt is either prepended
to real context rows (*C*) or used alone (*NC*); NC is often as good or better on larger datasets.
For more than 10 classes the decoder MLP is retrained together with the prompt; even then fewer than
5% of TabPFN's parameters are optimised. Over 100 features, a feature-selection method is chosen on
validation data. TuneTables-medium and -light cut runtime with adaptive sequence size, lower
patience, no ensembling above 150,000 rows and (light) one training epoch. Because the prompt is
fitted to an objective, it can also be fitted to accuracy plus **demographic parity** (§5), and a
small tuned prompt can be read as a condensed, interpretable summary of a dataset (Fig. 4).

**Key results.** On the 98 TabZilla datasets against 19 algorithms (each tuned with 30 Optuna
configurations), TuneTables has the best mean accuracy (0.860 vs CatBoost 0.856, XGBoost 0.854),
best mean rank (7.435 vs 7.514) and most wins (30), but CatBoost's mean Z-score is marginally higher
(0.496 vs 0.494) and the top three are not significantly different (Table 1, Fig. 2). On a new
LARGE SCALE TABLES suite (29 datasets up to 1.9M rows and 7,200 features) it has the highest average
accuracy (§4, App. Table 8); on 15 datasets with up to 100 classes its mean rank is 2.52, second to
XGBoost (2.0). TuneTables-medium cuts runtime 72% for <0.25% accuracy loss (Table 2). Optimising for
accuracy plus demographic parity lowers average DP from 0.183 (TabPFN) to 0.109 at accuracy 0.840 vs
0.842 (Table 3).

**Strengths.** A clean, parameter-efficient mechanism with a broad, statistically tested
evaluation and open code and raw results; it makes the context a place where constraints such as
fairness can be imposed, a route distinct from [Robertson et al. 2025, *FairPFN*](#fairpfn)'s
prior-level approach.

**Limitations.** Author-stated: end-to-end runtime is over 7× that of CatBoost and XGBoost and
slower than TabPFNs3000, because of prompt training (inference alone is ~9× faster than
TabPFNs3000); small datasets cannot always be fully captured by the prompt. Reviewer reading:
"beats CatBoost" is a rank/accuracy statement within noise, not a significant win; it targets
TabPFN v1, whose row ceiling v2 raised architecturally; for v2, Rubachev et al. found full
fine-tuning matches parameter-efficient variants; classification only.

---

<a id="localpfn"></a>

## 2024-12 — Thomas et al. — LoCalPFN

**Venue:** NeurIPS 2024 · Layer 6 AI, Toronto · **arXiv:** [2406.05207](https://arxiv.org/abs/2406.05207) (filed PDF: NeurIPS proceedings version) · **DOI:** [10.52202/079017-3442](https://doi.org/10.52202/079017-3442) · **PDF:** [open](papers/2024/12_Thomas_et_al._Retrieval_Fine_Tuning_for_In_Context_Tabular_Models.pdf)

**Citation key:** `2024.THOMAS.retrievalfinetuningincontexttabularmodels`

**Where it fits.** The retrieval branch of TFM adaptation and, read alongside
[Nagler 2023, *Statistical Foundations of Prior-Data Fitted Networks*](#nagler-theory), an
empirical answer to his localisation gap. The same lab carries kNN-retrieved contexts into
pretraining in [Ma et al. 2026, *TabDPT*](#tabdpt).

**What it contains.** The diagnosis (§2, Fig. 1): with a single global context, TabPFN v1
underfits as data grow more complex and cannot use more rows than its ~1,000-row context, so its
performance stops improving with dataset size. Two fixes are combined:

* **Retrieval (TabPFN-kNN).** For each query, the k nearest training rows (raw standardised
features, L2 distance, faiss search over the whole training set) form its context; k is the
minimum of 10·√N and a preset maximum. This needs no training and lets accuracy keep improving with
N even when k ≪ N (Fig. 2).
* **End-to-end fine-tuning with retrieved contexts (LoCalPFN).** Because exact per-query contexts
make the batch dimension equal to the number of queries, fine-tuning uses an approximation: sample B
training points, retrieve each one's neighbourhood, shuffle and split it into context and queries,
so many nearby queries share one local context (§2.4, Fig. 3). At inference each query still gets
its own exact kNN context.

**Key results.** On 95 TabZilla datasets (≤100 features, ≤10 classes, no NaNs; 10-fold CV;
baselines tuned with 30 rounds; Table 1), mean AUC is 0.908 for LoCalPFN vs 0.892 XGBoost, 0.891
CatBoost and TabPFN-kNN, and 0.867 TabPFN (IQM AUC 0.958 vs 0.943 for XGBoost and TabPFN-kNN). On the
47 small datasets (<2,000 rows) LoCalPFN leads (0.882 vs XGBoost 0.861); on the 48 medium/large ones
it is on par with GBDTs (0.934 vs 0.931 XGBoost and LightGBM), whereas TabPFN reaches 0.884.
Fine-tuning with random contexts and then retrieving does not match joint retrieval+fine-tuning
(Fig. 5); global-context alternatives (32-member ensembles, 3,000-row contexts) stay below
TabPFN-kNN (Table 11).

**Strengths.** A simple, well-motivated mechanism (localisation) with large, bootstrapped-CI
evidence; TabPFN-kNN alone is a training-free, few-hyperparameter improvement, and both are
insensitive to embedding and metric choice. Code is released.

**Limitations.** Author-stated: shown only for TabPFN (v1) as base model; regression untested;
inherited feature/class limits; inference 1–2 orders of magnitude slower than tree models (Fig. 7b:
0.38–0.72 s vs ≤0.04 s), and LoCalPFN training averages 20–43 s per dataset. Reviewer reading:
per-query contexts complicate batched deployment; the medium/large advantage over tuned GBDTs is
within a few thousandths of AUC; v2 later raised the context ceiling architecturally.

---

<a id="tabpfn-v2-nature"></a>

## 2025-01 — Hollmann et al. — Accurate predictions on small data with a tabular foundation model

**Venue:** *Nature* 637, 319–326 (9 January 2025) · **DOI:** [10.1038/s41586-024-08328-6](https://doi.org/10.1038/s41586-024-08328-6) · **PDF:** [open](papers/2025/01_Hollmann_et_al._Accurate_predictions_on_small_data_with_a_tabular_foundation_model.pdf) (filed PDF: journal version)

**Citation key:** `2025.HOLLMANN.accuratepredictionssmalldatatabularfoundationmodel`

**Where it fits.** The TabPFN v2 paper: the first production-grade TabPFN, raising
[Hollmann et al. 2023, *TabPFN*](#tabpfn-v1)'s limits about 10× in rows (1,000 → 10,000) and 5× in
features (100 → 500), adding regression, and serving as the base model for most later work in this
collection (fine-tuning, continued pretraining, analysis papers).

**What it contains.** Still a PFN: a transformer pretrained once to minimise cross-entropy on
held-out rows of synthetic datasets, then applied by in-context learning in one forward pass.
* **Prior.** A new SCM-based generator samples high-level hyperparameters, builds a random DAG,
and propagates noise through edges carrying small neural networks, discretisations for categorical
features and decision-tree mappings, plus Gaussian noise; post-processing adds Kumaraswamy warping,
quantisation and MCAR missingness (Fig. 2, Methods). Targets are a random continuous feature
(regression) or a categorical one with ≤10 classes. About 130M synthetic datasets (2M steps,
batch 64; up to 2,048 training rows, 1–160 features) per model, ~2 weeks on eight RTX 2080 Ti.
* **Architecture.** One representation per cell. Each layer applies attention across the
features of a row, then attention across samples within each column, then an MLP; test rows attend
only to training rows (Fig. 1b). Random feature embeddings let the model distinguish columns with
identical statistics; the default groups two features per token. Training-set keys/values can be
cached so fit and predict are separated. Compute is O(n² + m²), memory O(n·m). Regression uses a
piecewise-constant (bar) output distribution.
* **Inference.** A small ensemble whose members shuffle feature order, permute class labels and
use different preprocessing (quantile + identity, SVD features, Yeo–Johnson power transform, one-hot,
outlier removal), with softmax temperature 0.9. In the current `TabPFN .txt` code dump (not the
paper) this pool appears as `PowerTransformer`, `QuantileTransformer`, `RobustScaler`,
`SquashingScaler` and `"none"`, with categoricals encoded via `OrdinalEncoder`. The paper itself
handles missing values with a per-cell missingness indicator and the input set to 0; the
`PFNS.txt` dump's `NanHandlingEncoderStep` adds NaN/inf indicators and replaces NaNs with
training-set feature means.

**Key results.** Benchmarks: 29 AMLB classification and 28 regression datasets (AMLB plus
OpenML-CTR23) with ≤10,000 samples, ≤500 features, ≤10 classes. Normalised ROC AUC: default
TabPFN 0.939 vs default CatBoost 0.752; tuned 0.952 vs 0.822. Normalised negative RMSE: 0.923 vs
0.872 default, 0.968 vs 0.875 tuned (Fig. 4a). Default TabPFN (2.8 s classification, 4.8 s
regression) beats all baselines tuned for 4 h — 5,140× and 3,000× speedups — and beats AutoGluon 1.0
on classification even with its 4 h budget; TabPFN (PHE) reaches 0.971 vs AutoGluon 0.914 (Fig. 5c–d).
Default TabPFN beats default CatBoost on all five Kaggle Tabular Playground competitions (Extended
Data Table 6). Density estimation, data generation, embeddings and fine-tuning are shown as proofs
of concept (German Credit, mfeat-factors and synthetic sine-curve tasks; Fig. 6 and accompanying
text).

**Strengths.** Large, consistent margins on curated benchmarks with distributional regression
outputs, built-in handling of missing values and categoricals, robustness analyses (Fig. 5a,b) and a
clear user guide; code, weights and an API are released.

**Limitations.** Author-stated: inference can be slower than optimised GBDTs (0.2 s per sample on
10,000×10 vs 0.0002 s for CatBoost); memory grows linearly with table size; evaluation is confined to
≤10,000 samples and ≤500 features; for larger or highly non-smooth regression data CatBoost, XGBoost
or AutoGluon are likely better; native classification is limited to 10 classes. Reviewer reading:
the prior-generation code is not released, so the prior cannot be reproduced or audited; the
ensemble and preprocessing are part of the reported performance; foundation-model abilities are
demonstrated as proofs of concept, not benchmarked.

---

<a id="beta-tabpfn-unleashed"></a>

## 2025-02 — Liu and Ye — TabPFN Unleashed

**Venue:** ICML 2025 (PMLR 267) · **arXiv:** [2502.02527](https://arxiv.org/abs/2502.02527) (filed v1, 4 February 2025) · **PDF:** [open](papers/2025/02_Liu_and_Ye_TabPFN_Unleashed_A_Scalable_and_Effective_Solution_to_Tabular_Classification_Problems.pdf)

**Citation key:** `2025.LIU.tabpfnunleashedscalableeffectivesolutiontabularclassificationproblems`

**Where it fits.** A dataset-specific adaptation method for TabPFN v1 that organises earlier
variants — [Feuer et al. 2024, *TuneTables*](#tunetables),
[den Breejen et al. 2024, *TabForestPFN*](#tabforestpfn),
[Thomas et al. 2024, *LoCalPFN*](#localpfn) and MixturePFN — by whether they reduce the **bias**
or the **variance** of TabPFN's generalisation error (§2.3, Table 1), and proposes **BETA**
(Bagging and Encoder-based fine-tuning for TabPFN Adaptation) to reduce both. The authors treat
[Hollmann et al. 2025's TabPFN v2](#tabpfn-v2-nature) as concurrent work that only partially
removes the limits addressed here (§1).

**What it contains.** A bias–variance analysis on Adult and Bank (Fig. 2) finds that subsampling,
ensembling, bagging, kNN contexts and fine-tuning each move one term, rarely both. BETA (§3, Fig. 3):
* **Fine-tuning stage (bias).** TabPFN stays frozen; a lightweight encoder — a two-layer MLP with
hidden/output width 100, ReLU, dropout and periodic activations — maps raw features into the input
space TabPFN expects, and is trained end-to-end through TabPFN's predictive loss on support/query
splits. Mapping to a fixed width also removes the 100-feature input limit.
* **Multiple encoders (variance).** K encoders are trained jointly (sum of their losses), implemented
as a Batch Ensemble — shared weight matrices with member-specific scaling vectors — so the extra
members are cheap.
* **Inference.** Each encoder gets its own bootstrapped 1,000-row support set (16 bootstrap
iterations by default; App. B.3) and predictions are averaged.
* **More than 10 classes.** Error-correcting output codes, with distinct encoders handling the
binary sub-problems.

**Key results.** On the 186 TALENT classification datasets with fewer than 10 classes, untuned
BETA has the best rank in a Wilcoxon–Holm critical-difference analysis against 28 methods, whose
non-PFN members were tuned with 100 Optuna trials (Fig. 4); TabPFN variants including BETA use
defaults. Its improvement over TabPFN grows with dataset size across 173 datasets (Fig. 5); it has
the best average rank on 17 high-dimensional scikit-feature datasets (Fig. 6) and the best mean
accuracy on 12 TALENT datasets with more than 10 classes (Fig. 7). Efficiency (App. D.4, Table 3):
0.91 s mean inference vs 0.78 s TabPFN and 12.51 s LocalPFN, with a 0.60 MB checkpoint of learned
parameters; average rank 6.76 vs TabR 9.26 and TabPFN 15.63.

**Strengths.** The bias–variance framing is a useful lens for comparing TabPFN adaptations;
the method is cheap at inference, keeps PFN-style batched prediction, and beats tuned GBDTs and
tabular deep models with no per-dataset tuning of its own.

**Limitations.** Author-stated (App. C.2): classification only (regression left open); assumes
i.i.d. train and test data; on very small datasets fine-tuning the encoder can overfit and slightly
increase bias (App. D.2). Reviewer reading: built on TabPFN v1 with a fixed 1,000-row support set,
so its gains must be re-established against v2-era models; replacing raw features with learned
embeddings gives up the alignment between real feature distributions and the pretraining prior;
accuracy is the only metric (no calibration or log-loss).

---

<a id="mccarter-tabpfn"></a>

## 2025-02 — McCarter — What exactly has TabPFN learned to do?

**Venue:** ICLR 2024 Blogposts Track (initial version); filed as the expanded arXiv preprint
with a TabPFN-v2 appendix · **arXiv:** [2502.08978](https://arxiv.org/abs/2502.08978v1) (filed v1, 13 February 2025) · **PDF:** [open](papers/2025/02_McCarter_What_exactly_has_TabPFN_learned_to_do.pdf)

**Citation key:** `2025.MCCARTER.whatexactlyhastabpfnlearned`

**Where it fits.** A behavioural counterpart to
[Nagler 2023, *Statistical Foundations of Prior-Data Fitted Networks*](#nagler-theory):
inspect the predictor a context produces instead of inferring its behaviour from the pretraining
objective. It anticipates the symmetry concerns formalised by
[Arbel et al. 2025, *EquiTabPFN*](#equitabpfn) and the retrieval interpretation of
[Shaheen et al. 2026, *Understanding the Surprising Generalization Properties of Tabular Foundation
Models*](#shaheen-retrieval).

**What it contains.** TabPFN is treated as a black-box generator of function approximators and
probed with hand-built training sets, all with default settings and no tuning:
* **1-D binary probes** (§2): one red and one green point; then repeated features, duplicated rows
of both classes, duplicated rows of one class, and periodic label patterns.
* **2-D multiclass probes** (§3): one training point per class, randomly or grid-spaced, with
predictions compared to the Voronoi diagram, with and without ensembling.
* **Out-of-domain real data** (§4–5): BladderBatch gene expression (57 samples, 22,283 features,
5 microarray batches; random 75/25 splits and leave-one-batch-out) against logistic regression,
SVC and XGBoost; MNIST and CIFAR-10 flattened into tables with 30–1,000 training rows.
* **Appendix A (v2):** the same probes re-run on TabPFN v2, plus parity-function truth tables of
3–10 bits under four training-set regimes.

**Key results.** v1: predicted probabilities between two points are non-monotonic and biased
below 0.5 without ensembling (Fig. 1–2); repeating features pushes probabilities away from 0.5 with
diminishing effect (Fig. 3); duplicating both classes' rows has no visible effect, but duplicating
only the red row oddly also raises the green probability on the far side (Fig. 4–5); periodic
patterns are not detected and predictions drift toward 0.5 as cycles increase (Fig. 6). With 32
ensemble members, 2-D predictions resemble 1-nearest-neighbour Voronoi cells; without ensembling
they are erratic (Fig. 7). On BladderBatch TabPFN beats SVC and XGBoost and nearly matches logistic
regression (Fig. 8–9); on MNIST/CIFAR-10 it is competitive at the smaller training sizes but lags as rows
increase, ending last or second-last (Fig. 11, §6). v2: default hash-based fingerprint features let it distinguish duplicated
rows, but toy probability surfaces become "bumpy"; v2 ran out of memory on the high-dimensional
tasks except MNIST, where it moves to mid-pack at 300–1,000 rows. Ensembled v2 approximately learns
parity: at 10 bits with 127 training rows (about 12% of the truth table) it exceeds 99% accuracy
(App. A.2, Fig. 20).

**Strengths.** Transparent, cheap, reproducible stress tests expose inductive biases that average
benchmark ranks hide, and the expanded version tests both v1 and v2 with positive as well as
negative findings.

**Limitations.** Author-stated: preliminary, exploratory probes; whether the odd duplication
behaviour is optimal for the prior or an artefact is left open. Reviewer reading: small
hand-picked case studies, not a benchmark or a mechanistic proof; the nearest-neighbour analogy is
behavioural and holds only in the one-sample-per-class setting; v1's duplication results do not carry
over to v2, whose fingerprinting changes the setup; the parity result says nothing about calibration
or robustness, and later checkpoints are untested.

---

<a id="pfn-position-2025"></a>

## 2025-05 — Müller et al. — Position: The Future of Bayesian Prediction Is Prior-Fitted

**Venue:** ICML 2025 (PMLR 267), position track · **arXiv:** [2505.23947](https://arxiv.org/abs/2505.23947) (filed v1, 29 May 2025; carries the ICML proceedings header) · **PDF:** [open](papers/2025/05_Muller_et_al._Position_The_Future_of_Bayesian_Prediction_Is_Prior_Fitted.pdf)

**Citation key:** `2025.MULLER.positionfuturebayesianpredictionpriorfitted`

**Where it fits.** The PFN authors' manifesto and research agenda, written after TabPFN v2
([Hollmann et al. 2025](#tabpfn-v2-nature)). It restates the case made in
[Müller et al. 2021, *Transformers Can Do Bayesian Inference*](#pfns-2021) for the whole field
and lists the open problems that later papers in this collection take up (scaling, inference
speed, duplicated rows, interpretability, harder priors).

**What it contains.** The position (§1): PFNs "will dominate most applications of Bayesian
prediction". Background (§2) recaps PFN training — sample a dataset from a prior, train a
transformer to predict held-out targets, so a forward pass approximates the posterior predictive —
and contrasts it with MCMC, VI and GPs and with other amortised methods. §3 states what PFNs offer:
priors defined *declaratively* by a sampler (no tractable likelihood needed), use of growing compute
when real data are scarce, and no train/test leakage because pretraining data are synthetic. It also
lists five current limitations (below). The agenda: **extensions** (§4 — extra inputs such as
user knowledge, an in-context interpreter, Bayesian optimisation via reinforcement learning, latent
prediction); **understanding** (§5 — martingale property, limit behaviour, impact of prior density,
interpretability); **improvements** (§6 — scaling to more samples, focusing pretraining on hard
datasets, fast inference, adaptive compute, architectural limitations). §7 answers three
alternative views (traditional Bayesian methods are superior; PFNs do not scale; PFNs lack
interpretability).

**Key results.** Position paper, so evidence is mostly cited: PFNs >200× faster than earlier
methods at small-scale Bayesian prediction and >10,000× for learning-curve extrapolation (§1);
TabPFN v2 pretraining cost 2,700 GPU hours (§6.1). Two small new illustrations: a martingale check
in which predictive standard deviation shrinks slightly over the first sequential self-sampling
steps and then stabilises (§5.1, Fig. 2), and a coin-flip prior on which the original PFN
architecture fails to count repeated examples (§6.5, Fig. 3).

**Strengths.** A clear, citable statement of the paradigm's premises with an organised agenda;
it endorses post-pretraining ensembling and fine-tuning where many related datasets exist (§6.1)
and is candid about current weaknesses.

**Limitations.** Author-stated (§3, §6.5): PFNs hide the latent and are less interpretable; the
support of the prior is ill-defined, so it is unclear which data they work on; they work best on
small data and lose on large data; inference is slower than traditional tabular methods; encoder-only
transformers struggle to count identical examples (v2 works around this with noise features), and
mixed heavy-tailed/centred features hurt. Reviewer reading: an advocacy piece by the field's main
proponents (several with Prior Labs affiliations), with no systematic new evidence; the scaling
optimism (§6.1, §7) is argued, not demonstrated.

---

<a id="tabicl-2025"></a>

## 2025-05 — Qu et al. — TabICL

**Venue:** ICML 2025 (PMLR 267) · **arXiv:** [2502.05564](https://arxiv.org/abs/2502.05564) (filed v2, 24 May 2025) · **PDF:**
[open](papers/2025/05_Qu_et_al._TabICL_A_Tabular_Foundation_Model_for_In_Context_Learning_on_Large_Data.pdf)

**Citation key:** `2025.QU.tabicltabularfoundationmodelincontextlearninglargedata`

**Where it fits.** The first open, synthetic-prior competitor to TabPFNv2 built for *large*
tables (INRIA SODA). It introduces the row-compression design — embed each row first, then do
ICL over rows — that later models adopt, including Orion-MSP, [TabICLv2](#tabiclv2) and
[TabPFN-3](#tabpfn-3). Classification only.

**What it contains.** A **two-stage** architecture instead of
[Hollmann 2025, *Accurate predictions on small data with a tabular foundation model*](#tabpfn-v2-nature)'s
alternating column/row attention over every cell (§3):

* **Distribution-aware column embedding (TF_col).** Each column is treated as a
permutation-invariant *set* of cell values and passed through a Set Transformer with induced
self-attention (3 ISAB blocks, k = 128 inducing vectors fitted on training rows only), which
outputs per-cell weights and biases. One shared module therefore embeds columns of any
distribution or type, rather than per-feature embedding layers.
* **Row-wise interaction (TF_row).** A transformer over the cells of each row (with rotary
positional encoding to stop identically distributed features collapsing to the same
representation) and four learnable [CLS] tokens whose concatenation is a 512-dim row embedding.
* **Dataset-wise ICL (TF_icl).** Label embeddings are added to training-row embeddings and a
transformer does ICL from test rows to training rows.

Complexity drops from O(m²n + n²m) for TabPFNv2 to O(m²n + n²) (n rows, m columns; §3.5).
The prior is TabPFN-v1-style MLP SCMs with 15 extra activation functions (70%) plus new
**tree-based SCMs** whose node functions are XGBoost regressors fitted to noise targets (30%)
(§4.1). A three-stage **curriculum** raises pretraining table size from 1,024 rows to 1K–40K and
finally 40K–60K, the last stage training only TF_icl (§4.2, App. E); pretraining took ~20 days
on three A100s over ≈82M synthetic datasets. More than 10 classes are handled by hierarchical
classification; memory is managed by batch-size prediction and CPU/disk offloading (§4.4).

**Key results.** On TALENT's 200 classification datasets, TabICL has the best median relative
accuracy over a tuned MLP and is statistically tied with TabPFNv2, both ahead of all tuned
baselines (Fig. 5, App. I); on log loss the two are again tied and better than the
accuracy-tuned competitors. On the 53 datasets above 10K rows it surpasses TabPFNv2 and CatBoost
(Fig. 7). It is 1.5× faster than TabPFNv2 on small and 3–10× faster on large datasets (Fig. 6;
e.g. ~20 s vs 1 min 40 s at 10K×100). On the 12 datasets with > 10 classes it ranks second
(after RealMLP) in normalised accuracy (Fig. 8). Tree-based SCMs improve accuracy, AUC and log
loss (Fig. 9); the curriculum lifts its large-data average rank 11.4 → 7.46 → 6.95 (§5.3).
Memory: 100K × 500 needs ~5 GB GPU and 32 GB RAM; the introduction quotes "around 20GB" GPU for
500K × 500, while App. E.4 measures < 14 GB GPU with ~120 GB CPU RAM (reducible via disk
offloading).

**Strengths.** Moves frozen ICL an order of magnitude beyond TabPFNv2's tested row range on
modest hardware; reports probability quality (log loss), not only accuracy; open pretraining
code, inference code and weights; ablations isolate the tree prior and the curriculum.

**Limitations.** Author-stated (§6): classification only; slow inference relative to cached
predictors; RoPE breaks column-permutation invariance, restored only approximately by ensembling
over column permutations; evaluation inherits TALENT's protocol (single holdout-tuned baselines,
mean imputation of missing values). Reviewer reading: the curriculum causes slight drops on some
small datasets (Fig. 10); the > 10-class result rests on 12 datasets; the large-data claim is
measured up to 150K training rows, with 500K shown only as a memory demonstration.

---

<a id="fairpfn"></a>

## 2025-06 — Robertson et al. — FairPFN

**Venue:** ICML 2025 (PMLR 267) · **arXiv:** [2506.07049](https://arxiv.org/abs/2506.07049) (filed v1, 8 June 2025) · **PDF:**
[open](papers/2025/06_Robertson_et_al._FairPFN_A_Tabular_Foundation_Model_for_Causal_Fairness.pdf)

**Citation key:** `2025.ROBERTSON.fairpfntabularfoundationmodelcausalfairness`

**Where it fits.** The causal-fairness member of the Freiburg/Prior Labs causal-PFN cluster,
alongside [Robertson 2025, *Do-PFN*](#do-pfn) and [Balazadeh Meresht 2025, *CausalPFN*](#causalpfn).
Counterfactual-fairness methods (Kusner et al. 2017) need the correct causal model; a wrong
user-specified graph invalidates the fairness guarantee ("fairwashing"). FairPFN replaces the
graph with a pretrained prior over causal explanations.

**What it contains.** A PFN for binary classification whose task is redefined by the prior (§4):

* **Prior.** Sparse random MLPs act as SCMs; a binary exogenous protected attribute A sits at the
input layer, m features are drawn from the second hidden layer onwards and the target from the
output layer (binarised at a random threshold). A first forward pass gives a *biased* dataset; a
second pass with dropout on A's outgoing edges (A's causal weight masked to zero) gives the
*fair* counterpart.
* **Objective.** The transformer receives the biased data (X_bias, A, Y_bias) as context and is
trained with cross-entropy against the *fair* targets, i.e. it learns X_bias → Y_fair. A
dedicated encoder step tells it which column is the protected attribute.
* **Training.** ~3 days on one RTX 2080 over ~1.5M sampled data-generating mechanisms.
* **Inference.** Only observational data; the model integrates over causal explanations
consistent with it. No causal graph is supplied.

Baselines (§5.1) are Unfair, Unaware (averaging predictions over both values of A),
counterfactual-average, CFP (Kusner's three levels, given true fair causes/noise), EGR
(Exponentiated Gradient Reduction with XGBoost), Constant and Random; graph-dependent baselines
use FairPFN with a noise column as "UnfairPFN".

**Key results.** Six synthetic case studies × 100 datasets (Fig. 2): FairPFN is on the
fairness–accuracy Pareto front on 40% of the 600 datasets, competitive with CFP and
counterfactual averaging that see true causal quantities (Fig. 3), and has average rank 1.88/4
in causal-effect removal among graph-free methods, with prediction ATE within about ±0.2 and
outliers from datasets under 250 rows (Fig. 4, §5.2). On Law School Admissions and Adult Census
Income (§5.3), prediction ATE is below 0.01 at accuracy comparable to Unfair (Fig. 6), and
maximum counterfactual absolute error is under 0.05 and 0.2 respectively (Fig. 7).

**Strengths.** Shows that a prior can encode a *task transformation* (biased → fair outcome),
not just a data distribution. Synthetic studies have exact ground-truth counterfactuals, and
ablations show it reverts to an ordinary classifier when its assumptions (e.g. exogeneity) fail
(App. Fig. 13, 17).

**Limitations.** Author-stated (§6): one binary, exogenous protected attribute; binary
classification only; it does not remove effects of other protected attributes (in Law School it
*increases* the correlation with Sex while removing Race; Fig. 8, App. Fig. 12); spurious-effect
and business-necessity distinctions are left to future work. Reviewer reading: the real-data
"ground truth" ATE and counterfactuals come from `dowhy.gcm` models fitted on assumed graphs
(App. A), so real-data evaluation is only as good as those graphs; only two real datasets; no
calibration analysis.

---

<a id="on-finetuning"></a>

## 2025-06 — Rubachev et al. — On Finetuning Tabular Foundation Models

**Venue:** preprint (Yandex / HSE University; "under review") · **arXiv:** [2506.08982](https://arxiv.org/abs/2506.08982) (filed v2, 11 June 2025) · **PDF:**
[open](papers/2025/06_Rubachev_et_al._On_Finetuning_Tabular_Foundation_Models_1.pdf)

**Citation key:** `2025.RUBACHEV.finetuningtabularfoundationmodels`

**Where it fits.** The systematic study of *single-dataset* gradient adaptation of TabPFNv2, and
a mechanistic counterpart to [Hollmann 2025, *Accurate predictions on small data with a tabular
foundation model*](#tabpfn-v2-nature). It disputes the premise of
[Feuer 2024, *TuneTables*](#tunetables) and earlier v1 work that partial or parameter-efficient
tuning is needed to avoid overfitting, and it complements corpus-level continued pretraining in
[Garg 2025, *Real-TabPFN*](#real-tabpfn).

**What it contains.** Three parts.

* **Finetuning strategies (§3).** On datasets from the Grinsztajn et al. and Gorishniy et al.
benchmarks small enough to finetune with the whole training set as prompt on one 80 GB GPU
(average ≈15K rows vs ≈3K in the TabPFNv2 paper), it compares full finetuning, LoRA, last-layer
tuning, LayerNorm+head+embedding tuning and added numerical-feature embeddings. Protocol: learning
rate tuned per dataset over ten log-spaced values from 5e-6 to 5e-4; 1,024 objects per gradient
step form the prediction batch while the remaining rows are the context; validation every ten
steps with early stopping after 16 non-improving evaluations; RMSE or accuracy reported, plus
relative improvement over a tuned MLP.
* **Mechanism (§4).** Treating TabPFNv2 as an implicit retriever, it uses last-layer attention
weights as similarity scores for a weighted-kNN predictor and measures attention entropy before
and after finetuning.
* **Context (§5).** In-context, 8-member ensemble, finetuned and 5-run finetuned-ensemble
TabPFNv2 against tuned MLP-PLR, ModernNCA, TabM†mini and XGBoost, then on subsampled TabReD
datasets with temporal shift.

**Key results.** Full finetuning matches the PEFT variants (Fig. 1) and converges fastest
(Table 1); larger prediction batches help (Table 2). Finetuning gains grow with dataset size and
are often insignificant on small subsamples (Fig. 2). Attention-weighted kNN improves after
finetuning (e.g. California RMSE 0.473 → 0.407; Table 3), and most of the gain comes from test
points whose attention entropy drops (Figs. 3–4); TabPFNv2's gains over MLP correlate 0.89 with
ModernNCA's vs 0.53 with MLP-PLR's. In Fig. 5, in-context TabPFNv2 is close to MLP-PLR (+1.15%
over MLP, mean rank 3.24), finetuned +3.17% (rank 1.81) and the 5-run finetuned ensemble +3.90%
(rank 1.05), ahead of TabM†mini×5 (+2.92%, rank 2.38). On TabReD subsamples TabPFNv2 is less
stable than TabM; finetuning improves almost all datasets but often degrades Sberbank Housing
(Fig. 6, §5.2).

The local ``repositories/On Finetuning Tabular Foundation Models.txt`` dump belongs to this
Rubachev study. It is **not** a Real-TabPFN code release. The studies answer complementary
questions: Rubachev adapts one target dataset at a time; Garg continues pretraining one model
across a 71-table corpus.

**Strengths.** A controlled, reproducible finetuning protocol (LR grid, 1,024-object batch,
patience-16 early stopping, ×5 ensembling) compared against strong modern tabular DL baselines,
not only GBDTs; a testable mechanistic account (query–key similarity sharpening) linking
finetuning to retrieval; honest negative results under temporal shift.

**Limitations.** Author-stated (§6): only datasets that fit on a single 80 GB GPU (≤ ≈1M cells,
up to 50K objects), so chunked large-scale finetuning is untested; preprocessing is not
standardised across methods. Reviewer reading: evaluation is accuracy/RMSE only — no AUC, log loss
or calibration — so whether attention sharpening harms probability quality is open; the
retrieval analysis uses one seed (Table 3); TabReD is subsampled; only TabPFNv2 is studied.

---

<a id="closer-look-tabpfn-v2"></a>

## 2025-06 — Ye et al. — A Closer Look at TabPFN v2

**Venue:** NeurIPS 2025 · **arXiv:** [2502.17361](https://arxiv.org/abs/2502.17361) (filed v2, 11 June 2025, a pre-camera-ready "under review" version) · **DOI:** [10.52202/085713-4527](https://doi.org/10.52202/085713-4527) · **PDF:**
[open](papers/2025/06_Ye_et_al._A_Closer_Look_at_TabPFN_v2_Understanding_Its_Strengths_and_Extending_Its_Capabilities.pdf)

**Citation key:** `2025.YE.closerlooktabpfnv2understandingitsstrengthsextendingitscapabilities`

**Where it fits.** An external (Nanjing / Ohio State) analysis of TabPFNv2 rather than a new
model: *how* does [Hollmann 2025, *Accurate predictions on small data with a tabular foundation
model*](#tabpfn-v2-nature) cope with heterogeneous schemas, and can its suggested regime
(≤ 10,000 samples, ≤ 500 features, ≤ 10 classes) be extended *without retraining*? Same group as
[Liu 2025, *TabPFN Unleashed*](#beta-tabpfn-unleashed), which attacks v1's limits by fine-tuning
instead.

**What it contains.**

1. **Broad evaluation (§4).** TabPFNv2 against 26 tuned methods on the TALENT benchmark's 300
datasets minus the 27 used for v2's checkpoint selection (273 left; 64/16/20 splits, 15 seeds,
Optuna-tuned baselines), plus 18 high-dimensional (d ≥ 2,000), 18 large-scale (N × d > 10⁶) and
12 > 10-class datasets.
2. **Randomised attribute tokens (§5).** Each cell value x_j is embedded as x_j·u + W p_j with a
shared u and a *random* vector p_j drawn at inference (a detail the authors took from v2's
supplement and code). Probing layers 3–12 on churn and bank, token embeddings of different
attributes start scattered and become structured, so v2 infers attribute relationships through
ICL instead of needing semantic or dataset-specific attribute tokens.
3. **Feature extraction (§6).** Naively taking the output tokens of training rows fails because
their label embeddings are real while test rows get dummy labels. A **leave-one-fold-out**
scheme (10 folds; each fold embedded with dummy labels while the rest is context) yields
comparable train/test embeddings that are close to linearly separable.
4. **Test-time divide-and-conquer (§7).** High-dimensional: bag m = ⌈d/500⌉ random 500-feature
subsets. > 10 classes: encode labels as decimal digits, one v2 per digit, with √C random
class-to-digit permutations ensembled. Large N: **-SQ** (10,000-row support set, embeddings for
everything else, logistic-regression head, repeated four times) and **-DF** (32 shallow decision
trees on 60% subsamples, v2 applied per leaf).

**Key results.** On the 273 datasets v2 beats all tuned baselines in the critical-difference
analysis and is best on 26.02% of datasets (PAMA), vs ModernNCA 11.79% and TabM 9.78% (Figs. 1–2).
Without extensions its average rank is 3.36 on high-dimensional (behind logistic regression,
2.27), 3.97 on large-scale (CatBoost 1.89) and 3.33 on > 10-class datasets (Table 1). A logistic
regression on combined-layer embeddings ranks 1.94 vs in-context v2's 2.69 on 29 classification
datasets (Table 2). Extensions (Fig. 5): feature bagging gives the best mean accuracy on the
high-dimensional set (0.8973 vs 0.8525 for plain v2); decimal encoding is second (0.7093) behind
RealMLP (0.7251) on > 10 classes; on large data -DF (rank 4.35) and -SQ (7.00) improve on plain
v2 (9.64) but stay behind CatBoost (3.06), RealMLP (3.72) and ModernNCA (3.80).

**Strengths.** Large, leakage-aware benchmark (checkpoint-selection datasets excluded), a reusable
leave-one-fold-out embedding diagnostic, and cheap retraining-free extensions with per-dataset
results in the appendix.

**Limitations.** Reviewer reading: the explanations are observational (PCA/attention probes on two
datasets; the pretraining-mismatch cause of the large-data failure is hypothesised, not tested);
extensions multiply inference cost yet still trail tuned CatBoost/RealMLP at scale; evaluation is
accuracy/RMSE only, with no calibration or log loss; large-scale baselines use default
hyperparameters.

---

<a id="real-tabpfn"></a>

## 2025-07 — Garg et al. — Real-TabPFN

**Venue:** 1st ICML Workshop on Foundation Models for Structured Data (2025) · **arXiv:**
[2507.03971](https://arxiv.org/abs/2507.03971) (filed v1, 5 July 2025) · **PDF:**
[open](papers/2025/07_Garg_et_al._Real_TabPFN_Improving_Tabular_Foundation_Models_via_Continued_Pre_training_With_Real_World_Data.pdf)

**Citation key:** `2025.GARG.realtabpfnimprovingtabularfoundationmodelscontinuedpretrainingrealworlddata`

**Where it fits.** The reference recipe for **corpus-level continued pretraining**: take the
released synthetic-only TabPFNv2 checkpoint and continue pretraining it on curated real tables.
It sits between purely synthetic pretraining ([Hollmann 2025, *Accurate predictions on small
data with a tabular foundation model*](#tabpfn-v2-nature)) and purely real-data pretraining
([Ma 2026, *TabDPT*](#tabdpt)), and the Real-TabPFN variant later became the default checkpoint
of [Grinsztajn 2026, *TabPFN-2.5*](#tabpfn-25).

**What it contains.**

* **Data (§3).** 71 hand-curated OpenML and Kaggle classification datasets, each > 10,000 rows
(App. A). Minimal preprocessing: scikit-learn ``OrdinalEncoder`` for categoricals; targets with
more than ten classes keep the nine most common and merge the rest into a tenth class. A
five-tier contamination filter: (1) size > 10K rows (every evaluation dataset is smaller);
(2) IDs, names and shapes; (3) feature names; (4) row and column hashes; (5) manual metadata
inspection for shared or subsampled sources.
* **Recipe (§4).** Two-stage: start from the synthetic TabPFNv2 checkpoint, then continue
pretraining the unchanged architecture on real tables only (not mixed with synthetic data).
AdamW at LR 3e-7 with linear warm-up and cosine annealing; cross-entropy plus an **L2-SP**
penalty (α/2)‖w − w₀‖² with α = 0.003 toward the starting weights to limit forgetting;
**20,000 steps**, batch size one table, up to 20,000 rows and 400,000 cells per table, split
60% context / 40% query; one RTX 2080 Ti. The paper does not report AdamW's weight decay.
Batch size one does not make this single-dataset finetuning: each step draws a table from the
71-dataset corpus.
* **Evaluation (§5).** The 29 OpenML AutoML Benchmark classification datasets used for
TabPFNv2 (≤ 10,000 rows, ≤ 500 features), 10-fold CV, untuned TabPFN models, baseline results
reused from Hollmann 2025 (tuned 4 h for ROC-AUC).

**Key results.** Mean normalised ROC-AUC rises from 0.954 to 0.976 (+0.022) and Real-TabPFN beats
default TabPFNv2 per dataset (two-sided Wilcoxon signed-rank p = 0.0045; Figs. 1, 3). Raw mean
ROC-AUC moves 0.929 → 0.932 and mean ECE 0.042 → 0.040 (App. C). Source ablation: OpenML alone
+0.019, Kaggle alone +0.015, both +0.022 (Fig. 5); filtered CommonCrawl (~97,000 tables, ~100
rows × 7 features on average) gives −0.003 and GitTables (658 tables, ~1,000 × 9) +0.010
(Fig. 6). Gains grow with continued-pretraining context: +0.010 at 2,048 and 4,096 rows,
+0.016 at 8,192 and 16,384, +0.022 at 20,000 (Fig. 4).

**Attribution warning.** The paper releases weights on Hugging Face but there is **no public
Real-TabPFN training-code release**. The local
``repositories/On Finetuning Tabular Foundation Models.txt`` dump belongs to **Rubachev et
al.**, not to Garg et al. — do not read that repository's hyperparameters as Garg's recipe. A
second reference point, from the `TabPFN .txt` package dump rather than the paper, is the Prior
Labs single-dataset finetuning wrapper: in the current dump both ``FinetunedTabPFNClassifier`` and
``FinetunedTabPFNRegressor`` default to 30 epochs, ``learning_rate`` 1e-5, ``weight_decay`` 0.01,
``n_estimators_finetune`` 2 and ``n_finetune_ctx_plus_query_samples`` 50,000. These defaults
change between package versions, and they describe *single-dataset* finetuning, not corpus
continued pretraining.

**Strengths.** Cheap (one consumer GPU), simple and reproducible in outline; a statistically
significant per-dataset gain; careful contamination filtering; clean source and context-size
ablations that point to table size and quality, not corpus volume, as the driver.

**Limitations.** Reviewer reading: workshop-length; classification only (no regression); 29
small evaluation datasets; the absolute raw ROC-AUC gain is small (+0.003) and the calibration
change marginal; no sensitivity analysis on α, LR or steps and no parameter-efficient variant;
baselines are reused rather than rerun; the 71-dataset corpus is listed but no training code is
released.

---

<a id="mitra"></a>

## 2025-10 — Zhang et al. — Mitra: Mixed Synthetic Priors

**Venue:** NeurIPS 2025 (stated on the filed PDF; Zotero lists the arXiv preprint) · **arXiv:** [2510.21204](https://arxiv.org/abs/2510.21204) (filed v1, 24 October 2025) · **PDF:**
[open](papers/2025/10_Zhang_et_al._Mitra_Mixed_Synthetic_Priors_for_Enhancing_Tabular_Foundation_Models.pdf)

**Citation key:** `2025.ZHANG.mitramixedsyntheticpriorsenhancingtabularfoundationmodels`

**Where it fits.** The Amazon/AutoGluon prior-design paper: improve a TFM by choosing *which
synthetic priors to mix*, not by new architecture. It generalises the tree prior of
[den Breejen 2024, *TabForestPFN*](#tabforestpfn) into a measured selection framework, is
contemporary with the adaptive prior of [Wu 2025, *APT*](#apt), and is extended by
[Tao 2026, *Mitra-v2*](#mitra-v2) and compared in the controlled study of
[Bouadi 2026, *O'Prior*](#oprior). The paper reports releasing weights on Hugging Face as
``autogluon/mitra-classifier`` and ``autogluon/mitra-regressor`` (footnote 1).

**What it contains.** Three criteria for a prior G_i, each measured (§3, Table 1):

1. **Standalone performance** — a TFM pretrained only on G_i should do well on real data (the
performance vector P).
2. **Diversity** — a model pretrained on G_i should not easily fit G_i's own held-out data
(a low diagonal entry of the *generalizability matrix* G, whose entry G_ij is the performance
of a model trained on G_i when tested on data from G_j).
3. **Distinctiveness** — data from G_i should be hard for models trained on the other priors
(low off-diagonal entries).

Candidates are the SCM prior and tree-based priors (TBPs): decision tree (DT), random forest
(RF), extra trees (ET), gradient boosting (GB) and a new "directly sampled" random forest (DSRF).
A greedy prior-importance ablation (§4.7, Table 6) adds the best prior at each step; SCM matters
most and adding ET to SCM gives +63 Elo. The final mixture is 50% SCM and 50% TBPs equally
weighted (SCM + ET + GB + DT + RF + DSRF). The model (App. B.3) is a 12-layer, 512-dim
transformer alternating row and column attention (72M parameters; a 37M row-only "Mitra1D"
tests model-agnosticism), pretrained on 45M synthetic datasets of at most 16 features and 640
rows, ~60 h on eight A100s. Inference adds ICL ensembling (+e), fine-tuning (+f), and an 8-fold
cross-validation bagging of fine-tuned models.

**Key results.** On 137 merged classification datasets (TabRepo, TabZilla, AMLB; Table 2),
Mitra (+ef) ranks first (Elo 1136, AUC 0.905) just ahead of Attic (+ef) (1128, 0.903) and
TabPFNv2 (+e) (1107, 0.901); plain ICL Mitra (1015) roughly matches TabICL (1015) and trails
TabPFNv2 (1043). On 10 small TabRepo regression datasets Mitra (+ef) leads (Elo 1140 vs
TabPFNv2 (+e) 1090; Table 4), but on the larger AMLB + OpenML-CTR23 regression benchmark
TabPFNv2 (+e) is best (App. C.5, Table 18). The prior mixture also lifts the 1D model above
TabPFN and TabForestPFN (Table 3); Mitra edges TabPFNv2 and TabICL at every subsampling level
(Table 5); bagged Mitra beats TabPFNv2 post-hoc ensembling and AutoGluon best-quality for
300–3600 s budgets (Fig. 3). Gains saturate beyond 12 layers and around 37M datasets (Fig. 5).

**Strengths.** A transferable, measurable methodology for building prior mixtures; broad
evaluation with rank, Elo and aggregate metrics and confidence intervals; an explicit
model-agnosticism test; released classification and regression checkpoints.

**Limitations.** Author-stated (App. C.5, D): does not consistently beat TabPFNv2 on
large-feature regression, attributed to pretraining on ≤ 16 features and ≤ 640 rows; mixture
weights not tuned. Reviewer reading: the headline margin over Attic is 8 Elo with overlapping
95% CIs, and plain ICL Mitra is below TabPFNv2 — the lead comes from ensembling and fine-tuning;
greedy prior selection evaluated on the same TabRepo benchmark risks meta-overfitting; cross-
entropy is reported but no calibration analysis.

---

<a id="apt"></a>

## 2025-10 — Wu and Bergman — APT (Adversarially Pre-trained Transformer)

**Venue:** ICML 2025 (PMLR 267) · UC Berkeley + Capital One · **arXiv:** [2502.04573](https://arxiv.org/abs/2502.04573) (filed PDF: PMLR proceedings version) · **PDF:**
[open](papers/2025/10_Wu_and_Bergman_Zero_shot_Meta_learning_for_Tabular_Prediction_Tasks_with_Adversarially_Pre_trained_Transformer.pdf)

**Citation key:** `2025.WU.zeroshotmetalearningtabularpredictiontasksadversariallypretrainedtransformer`

**Where it fits.** A prior-design paper that makes the synthetic task distribution *adaptive*:
part of the generator reacts to the model being trained. It contrasts with fixed-prior mixing in
[Zhang 2025, *Mitra*](#mitra) and the later controlled comparison of fixed generators in
[Bouadi 2026, *O'Prior*](#oprior). Its class-count fix parallels, by a different mechanism,
the target-equivariant decoder of [Arbel 2025, *EquiTabPFN*](#equitabpfn).

**What it contains.** Built on TabPFN v1 (same MLP-SCM generator and shared hyperparameters):

* **Adversarial data agents (§2.1).** Each pretraining batch draws datasets from m generators; a
fraction are sparse MLPs whose weights are updated by *gradient ascent* on the model's
prediction loss, so they keep shifting towards datasets the model handles badly. Because the
loss of the agent is the negated model loss, model and agents update in one step (GAN-like, but
with no real-vs-fake discrimination). Soft discretisation keeps categorical features
differentiable, and agents are periodically reset to avoid collapse. Settings (§3): 12.5% of
generators adversarial, LR 1e-1, weight decay 1e-5, soft-discretisation temperature 1e-2, reset
every 2,000 gradient steps.
* **Mixture block (§2.2).** Replaces the fixed-width classification head: each test embedding
attends over training embeddings with softmax weights, sparsified by Concrete-distribution gates
(a point-specific "leaf" of relevant training rows), and class probabilities are a scatter-sum
of weights by training label — so any number of classes works without retraining.

**Key results.** On all 35 OpenML-CC18 datasets with ≤ 2,000 rows — no filtering on classes,
features, categoricals or missing values (TabPFN v1's main result used 18 filtered datasets),
80/20 splits, one-hour budget per tuned baseline (Table 1):

| | mean rank ↓ | ROC-AUC ↑ | wins | time (s) |
|---|---|---|---|---|
| **APT** | **3.86** | **0.921** | **13** | **0.90** |
| CatBoost | 4.03 | 0.918 | 6 | 3,542 |
| TabPFN | 4.57 | 0.913 | 4 | 0.86 |
| XGBoost | 5.37 | 0.914 | 4 | 3,608 |

Ablations (Table 3): the gain comes from adversarial pretraining (APT without mixture block 0.917
vs TabPFN 0.913); the mixture block alone leaves accuracy unchanged. On OpenML-CTR23 regression
adversarial pretraining lowers mean MSE 0.412 → 0.344 on 12 small datasets and 0.340 → 0.306 on
all 35 (Table 4). Agents' data diverge more from ordinary generators (KL 0.813 vs 0.134 between
two ordinary sets; §3.2). The mixture block reaches AUC 0.80 within 591 steps (Fig. 5); trained
on ≤ 10 classes it matches a 26-class head on 3 of 4 > 10-class datasets but is worse on isolet
(0.939 vs 0.970; Table 2).

**Strengths.** A genuinely different lever on the prior (the generator chases the model's
weaknesses); unfiltered evaluation; tuned-CatBoost-level rank at about 4,000× lower runtime; a
class-agnostic head; the final checkpoint is used without cherry-picking.

**Limitations.** Author-stated (§5, App. A.2): does not beat GBDTs on large datasets; keeps
TabPFN's quadratic attention cost; dense input embedding still caps features (subsampled to 100).
Reviewer reading: the baseline is TabPFN **v1** (class cap raised from 10 to 26), not v2; gains
over TabPFN are small (0.921 vs 0.913 AUC); regression uses classification-tuned
hyperparameters and no GBDT comparison; no calibration analysis.

---

<a id="do-pfn"></a>

## 2025-11 — Robertson et al. — Do-PFN

**Venue:** NeurIPS 2025 (stated on the filed PDF; Zotero lists the arXiv preprint) · **arXiv:** [2506.06039](https://arxiv.org/abs/2506.06039) (filed v3, 20 November 2025) · **PDF:**
[open](papers/2025/11_Robertson_et_al._Do_PFN_In_Context_Learning_for_Causal_Effect_Estimation.pdf)

**Citation key:** `2025.ROBERTSON.dopfnincontextlearningcausaleffectestimation`

**Where it fits.** A PFN that predicts **conditional interventional distributions (CIDs)**
p(y | do(t), x) from observational data alone, without a causal graph. It belongs to the
causal-PFN cluster with [Robertson 2025, *FairPFN*](#fairpfn) (same first author),
[Balazadeh Meresht 2025, *CausalPFN*](#causalpfn) (which assumes ignorability) and Ma et al.
2026 (*Foundation Models for Causal Inference via Prior-Data Fitted Networks*, CausalFM); all
three first appeared on arXiv in June 2025. Do-PFN is the one that deliberately trains on
priors where unconfoundedness can fail.

**What it contains.**

* **Prior and objective (§3, Alg. 1).** Sample an SCM with a binary treatment; draw an
*observational* dataset as context and, from the same SCM with incoming edges to t removed, an
*interventional* query set (do(t)). The transformer is trained to predict interventional
outcomes given observational context, so it approximates the posterior-predictive CID
integrated over SCMs consistent with the data (Prop. 1).
* **Uncertainty decomposition.** The PPD separates aleatoric noise, uncertainty over
observationally equivalent SCMs (unidentifiability) and epistemic uncertainty about the
equivalence class; with infinite data it concentrates only up to the Markov equivalence class
(Eq. 5, App. B). Where effects are unidentifiable it widens rather than "correcting" confounding.
* **Model.** TabPFN-v2-like architecture with a treatment-column indicator, 7.3M parameters, a
bar-distribution output; v1 (graphs up to 10 nodes, 48 h) and v1.1 (up to 60 nodes, 96 h), each
trained on one RTX 2080. CATE is the difference of predicted means under do(1) and do(0).

**Key results.** Six synthetic case studies (observed confounder, mediator, confounder +
mediator, unobserved confounder, front-door, back-door; 100 datasets each): Do-PFN beats Random
Forest, TabPFN v2 and an observational-outcome PFN ("Dont-PFN") on CID MSE and is competitive
with DoWhy given the true graph (Fig. 3, §4.2); on CATE and ATE it significantly outperforms
meta-learners, causal-forest DML, DragonNet and TARNet (§4.3). PICP curves show good overall
calibration and wider intervals in the unidentifiable case (§4.4). v1 degrades on out-of-prior
graphs with 21–50 nodes; v1.1 recovers (Fig. 4). On RealCause (unconfounded semi-synthetic)
v1.1 is strong on three of four datasets and competitive overall (Fig. 5); on Law School and
Amazon Sales with known graphs v1 is best on Law School and not significantly worse than the
best on Amazon Sales (Fig. 6, §4.5).

**Strengths.** Graph-free causal effect estimation with a formal account of what the PPD
targets and why uncertainty grows under unidentifiability; robustness to violated
unconfoundedness; OOD analysis (noise, nonlinearities, graph size); released model, prior code
and case-study data.

**Limitations.** Author-stated (§5): results hinge on the SCM prior matching reality, and
validation is mostly synthetic or semi-synthetic; theory for amortised estimators is immature;
binary interventions only, no counterfactuals or non-i.i.d. data. §4.4 also reports slight
under-confidence in identifiable cases (bar-distribution discretisation, imperfect loss
minimisation) and a large drop with doubled Gaussian noise variance. Reviewer reading: v1 only
covers graphs up to 10 nodes, so real tables with many covariates need the larger v1.1; real-
data evidence is two known-graph datasets plus RealCause.

---

<a id="one-model-to-rule"></a>

## 2025-11 — Zhang et al. — TabPFN: One Model to Rule Them All

**Venue:** preprint (statistics-journal format; footnote 1 says it was revised after TabPFN-2.5's release) · **arXiv:** [2505.20003](https://arxiv.org/abs/2505.20003) (filed v2, 27 November 2025) · **PDF:** [open](papers/2025/11_Zhang_et_al._TabPFN_One_Model_to_Rule_Them_All.pdf)

**Citation key:** `2025.ZHANG.tabpfnonemodelrulethemall`

**Where it fits.** A statisticians' appraisal of TabPFN v2
([Hollmann 2025, *Accurate predictions on small data with a tabular foundation model*](#tabpfn-v2-nature)):
not another benchmark, but a test of whether an untuned TFM can replace specialised estimators
from recent statistics-journal papers on those papers' own simulation designs. All experiments
use v2, not 2.5.

**What it contains.** §2 explains TabPFN for a statistics audience as in-context
**approximate Bayesian inference**: the network approximates the posterior predictive
distribution under its synthetic prior. §3 then runs three case studies, each reproducing a
published comparator's simulations and adding real data:

* **Semi-supervised parameter estimation** (§3.1). TabPFN fitted on the labelled rows imputes
  labels for all rows; the working-model parameter (linear, logistic or quantile regression) is
  estimated by ERM on the imputed data, without (TabPFN-I) or with (TabPFN-D) the
  Angelopoulos-style debiasing correction. Comparator: Song, Lin and Zhou (SLZ).
* **Heterogeneous treatment effects** (§3.2). TabPFN as base learner in S-, T-, X- and
  DR-learners on Foster and Syrgkanis's designs (vs an AutoML base learner); it cannot be used
  in the R-learner or the oracle because TabPFN does not support weighted loss minimisation.
  Real-data check on the ACIC 2017 benchmark against 16 methods incl. BCF, GRF and BART.
* **Covariate shift** (§3.3). Plain TabPFN on the source data, with no shift correction, against
  Wang's pseudo-labelling (PL) KRR, an oracle variant, importance-weighted and naive boosting.

§4 studies **adaptivity**: on 120 sparse-linear settings (Hastie–Tibshirani–Tibshirani design,
p = 100) TabPFN is compared with LASSO, SCAD and MCP, and an OLS fit to TabPFN's fitted values
recovers coefficients; under homogeneous label noise it is compared with kNN, LDA and the Bayes
classifier.

**Key results.** SSL: TabPFN-I/-D significantly beat SLZ in simulation MSE (SLZ wins only at
p = 4; Fig. 1); on real data mean-imputation TabPFN is best for logistic regression (Tables 2–3).
HTE: S-Learner (TabPFN) is best in most settings and top-two in almost all (Fig. 2); on ACIC 2017
TabPFN learners match or beat baselines under weak selection but degrade under strong selection;
adding a TabPFN propensity score as a covariate (best for the X-Learner) restores
competitiveness with the state of the art (Fig. 3, §3.2.5). Covariate shift: TabPFN beats PL
and matches or exceeds the oracle for n ≥ 800 in all settings except (iii) (Fig. 4), and is best
on Airfoil and Concrete (Table 4). Adaptivity: better than LASSO for s ≤ 10 and than SCAD/MCP for
s ≥ 5 (Fig. 5); with label noise it nearly reaches the Bayes risk at ρ = 0.3 given ≥ 5K samples
and stays robust at ρ = 0.4 (Figs. 6–7). App. D.4: ~95% nominal coverage in the interpolation
region, and much higher coverage than a GP when extrapolating.

**Strengths.** Each comparison uses the comparator's own published design, which makes the
"out-of-the-box beats specialist" claims harder to dismiss. The label-noise and sparse-linear
studies give unusual evidence that one prior-fitted model can behave parametrically when that
suits the data and nonparametrically when it does not. Code is public.

**Limitations.** Author-stated (§5): TabPFN struggles with dense regression, cannot handle
≥ 500 features, its MSE curves seem to plateau for n ≥ 10K, and it lacks weighted-loss support.
Reviewer reading: the adaptivity account is empirical, not derived; most designs are
low-dimensional simulations; coverage evidence is 1D and against a GP only; under strong
confounding plain TabPFN learners need the BCF-style propensity fix; and conclusions are tied to
the v2 checkpoint.

---

<a id="orion-msp"></a>

## 2025-11 — Bouadi et al. — Orion-MSP

**Venue:** preprint · Lexsi Labs (India / France) · **arXiv:** [2511.02818](https://arxiv.org/abs/2511.02818) (filed v3, 7 November 2025) · **PDF:** [open](papers/2025/11_Bouadi_et_al._Orion_MSP_Multi_Scale_Sparse_Attention_for_Tabular_In_Context_Learning.pdf)

**Citation key:** `2025.BOUADI.orionmspmultiscalesparseattentiontabularincontextlearning`

**Where it fits.** A classification TFM in the
[TabICL](#tabicl-2025) (Qu 2025, *TabICL: A Tabular Foundation Model for In-Context Learning on
Large Data*) three-stage family, and one of two Orion models from Lexsi Labs (the other is
Orion-BiX, *Bi-Axial Attention for Tabular In-Context Learning*, 2026). The same lab's
[Tanna 2025, *TabTune*](#tabtune) library and its 2026 study *Exploring Fine-Tuning for Tabular
Foundation Models* benchmark both Orion models.

**What it contains.** Orion-MSP keeps TabICL's pipeline — Set-Transformer column embedding →
row-wise interaction producing one embedding per row → split-masked ICL transformer over rows —
and changes the middle and last stages to address three stated limitations (§1, §3):

1. **Multi-scale row encoding.** Features are processed at scales 1, 4 and 16 (coarser scales
   group features into ⌈m/s⌉ tokens); each scale has its own transformer, and the [CLS] outputs
   are averaged across scales into the row embedding (Alg. 1).
2. **Block-sparse feature attention.** CLS and global tokens with full connectivity, a sliding
   window (w = 8) and optional random links replace dense attention, reducing cost in table
   width from O(m²) to O(m·(w+g+r)).
3. **Optional Perceiver-style memory** inside the ICL stage (Alg. 2): learnable latents attend
   to training rows only (write), then all rows attend to the latents (read), so test rows
   cannot leak into the context.

Labels are one-hot embedded into training rows only; >10 classes use TabICL-style hierarchical
grouping. Pretraining follows TabICL: synthetic SCM plus tree-based SCM priors, in three
curriculum stages (25K steps at 1,024 rows; 2K steps at 1K–40K rows; 50 steps at 40K–60K rows
training only the ICL transformer; App. A).

**Key results.** Zero-shot mean accuracy rank over the intersection of 154 TALENT, 63
OpenML-CC18 and 27 TabZilla datasets: Orion-MSP 3.58 overall vs TabPFN 4.61, TabICL 4.96 and
TabDPT 5.42 (Table 1); TabPFN has the higher TALENT accuracy (0.8514 vs 0.8461). By width
(Table 3) it leads on narrow tables (< 10 features, rank 3.76), but on wide tables (> 100
features) ranks 5.69, behind XGBoost (4.79) and CatBoost (5.50). It ranks first on imbalanced
datasets (3.38, Table 4) and on the finance subset (4.60, Table 5). Code and weights are public.

**Strengths.** The write-train/read-all memory is a clean way to add feedback between stages
without breaking ICL's train/test separation, and the paper reports results by size, width,
imbalance and domain rather than only an aggregate.

**Limitations.** Author-stated: the extra complexity gives little benefit on simple,
low-dimensional data (§5). Reviewer reading: the text claims strong wide-table performance that
its own Table 3 does not show; no component ablation (scales, sparsity, memory) is reported
despite an ablation switch in App. A; efficiency is argued by complexity, with no runtime or
memory measurements; Mitra's sub-0.40 accuracy and ContextTab's weak TALENT result suggest
pipeline problems in the baselines; evaluation is classification-only, accuracy/F1 only (no
calibration), and run by the model's authors.

---

<a id="spectral-adaptivity"></a>

## 2025-11 — Zheng et al. — From Tables to Signals: Revealing Spectral Adaptivity in TabPFN

**Venue:** preprint · Australian Institute for Machine Learning, University of Adelaide · **arXiv:** [2511.18278](https://arxiv.org/abs/2511.18278) (filed v1, 23 November 2025) · **PDF:** [open](papers/2025/11_Zheng_et_al._From_Tables_to_Signals_Revealing_Spectral_Adaptivity_in_TabPFN.pdf)

**Citation key:** `2025.ZHENG.tablessignalsrevealingspectraladaptivitytabpfn`

**Where it fits.** One of the few papers in the collection that tries to explain *why* TabPFN
works rather than to make it work better, and the third distinct mechanism offered.
[Nagler 2023, *Statistical Foundations of Prior-Data Fitted Networks*](#nagler-theory) argued
analytically that a PFN's variance vanishes for free but its bias vanishes only under
**localisation**;
[Shaheen et al. 2026, *Understanding the Surprising Generalization Properties of Tabular
Foundation Models*](#shaheen-retrieval) argued empirically that the learned procedure is
**retrieval-and-aggregation**. Zheng et al. add a **frequency** account — and the three converge
rather than compete, because the paper's own attention maps sharpen into local neighbourhoods as
context grows. That is localisation, measured spectrally.

**What it contains.** A 1D signal is recast as a table — each sampled point (x, y) is a row,
x the single feature and y the regression target — so TabPFN v2's regressor performs signal
reconstruction in one forward pass (Fig. 2). The paper then makes a definition, a claim and
three experiments.

The **context kernel** (Definition 1) is the paper's portable contribution. The Neural Tangent
Kernel is meaningless for an in-context model, since there are no gradient updates to
differentiate through, so the authors define the analogous object for ICL: the Jacobian of
predicted query outputs with respect to *context labels*,

> `K_context := ∂g(X_q; X_c, y_c) / ∂y_c  ∈ R^{M×N}`

For a single attention block this collapses to the softmax attention matrix itself (Eq. 5),
which is what makes it interpretable rather than merely formal. Proposition 2 states that as the
context size N grows the kernel's spectrum flattens towards the identity.

**Spectral adaptivity** (Remark 2) is what the kernel reveals. A ReLU-MLP's spectral bias
evolves over *training epochs* and is otherwise fixed once the architecture is chosen; TabPFN's
effective bandwidth instead expands with the *number of in-context samples*. Positional encoding
(random Fourier features) is examined as a third lever (§6).

**Key results.** Context-kernel eigenvalues decay more slowly and effective rank grows from
N = 64 to 4,096 context points, whereas ReLU-MLP NTK spectra are nearly sample-invariant
(Figs. 3–4). On sinusoid probes (k from 0.5 to 20) untuned TabPFN's spectral response matches a
well-trained deep MLP (Fig. 5) and keeps gaining high frequencies from 256 to 8,192 samples while
MLPs' responses do not change (Fig. 6). Self-attention maps become sharper and more local with
more context, and an SVD of layer-8 attention shows progressively higher rank (App. A).
**Positional encoding acts as a frequency dial**: larger RFF scales recover higher frequencies
from fewer samples; v2 and v2.5 differ in level but both adapt with sample count (Figs. 8–10).
The paper reads this as explaining why time-series uses of TabPFN needed calendar/positional
features, as in [Hoo 2024, *The Tabular Foundation Model TabPFN Outperforms Specialized Time
Series Forecasting Models*](#tabpfn-ts-2024). **Training-free image denoising** by patching
(Alg. 1) reaches 31.70 dB PSNR on the WIRE test image vs WIRE 29.48, MFN 28.38, ReLU+PE 27.05,
Gauss 25.16 and ReLU 22.60 (Fig. 7); across patch sizes it attains the highest maximum PSNR and,
per the authors, beats all INR baselines (incl. SIREN) on runtime too, and a single regressor nearly matches the default
8-member ensemble (App. Figs. 3–4).

**Strengths.** The context kernel is a reusable definition — an NTK-shaped tool for models
without gradient updates — and cheap to compute. The paper offers a mechanism for an existing
empirical practice (positional/calendar features) rather than another trick. The denoising
result shows that the pretrained model behaves as a training-free implicit signal model, and is
cheap to reproduce.

**Limitations.** Author-stated (§7): the kernel interpretation relies on a local linearisation
of a nonlinear transformer, leaving open how spectral adaptivity emerges from full attention
dynamics and from the pretraining distribution; experiments are bounded by TabPFN's context
window and input dimensionality; patching introduces blending artefacts that a globally trained
INR does not have. Reviewer reading: evidence is limited to the TabPFN v2/v2.5 line, so
row-compression architectures ([TabICL](#tabicl-2025), [TabPFN-3](#tabpfn-3)) are untested; the
denoising comparison uses one image; and 1D/2D signals with one or two coordinates are far from
real multi-feature tables, so the link to tabular performance is suggestive, not shown.

---

<a id="limix-unleashing-structured"></a>

## 2025-11 — Zhang et al. — LimiX: Unleashing Structured-Data Modeling Capability for Generalist Intelligence

**Venue:** technical report (Stable AI & Tsinghua University) · **arXiv:** [2509.03505](https://arxiv.org/abs/2509.03505) (filed v2, 7 November 2025) · **PDF:** [open](papers/2025/11_Zhang_et_al._LimiX_Unleashing_Structured_Data_Modeling_Capability_for_Generalist_Intelligence.pdf)

**Citation key:** `2025.ZHANG.limixunleashingstructureddatamodelingcapabilitygeneralistintelligence`

**Provenance.** First released 3 September 2025 (Zotero date). The filed PDF's internal header
reads 2025-11-10, which differs from the arXiv v2 banner (7 November 2025); filing uses the
banner month.

**Where it fits.** Extends PFN-style prediction from "predict the label column" to queries over
any variables and missingness patterns, so one model serves classification, regression,
imputation and generation. This original report precedes the separate
[LimiX-2](#limix-2) generation; "LimiX-2M" denotes the 2M-parameter size (see also the later
[LimiX-2M architecture paper](#limix-2m-mitigating)) and must not be confused with LimiX-2.

**What it contains.** Two models, LimiX-16M and LimiX-2M (§2). Each cell is embedded by a
two-layer MLP; a learnable low-rank **discriminative feature encoding** (rank p/4) is added so
attention can tell columns apart. LimiX-16M has 12 blocks, each with two feature-axis attention
passes and one sample-axis pass. **Context-conditional masked modelling** (§3): rows are split
into context and query; cell-wise, column-wise and block masks (ratio 0.1–0.4) hide query
entries, and the model recovers them from visible query cells plus the context. A learned mask
embedding doubles as the missing-value token, and a mask-density token reduces the mismatch
between heavy pretraining masks and single-target inference. Pretraining data (§4) come from
**hierarchical SCMs** built from local causal structures with MLP, convolutional or fixed
decision-tree edge functions, graph-aware and solvability-aware subsampling, then discretisation
for classification. Inference (§5) ensembles 4 (classification) or 8 (regression) pipelines with
feature permutations and simple transforms, and optionally **retrieves** per-test-sample context
rows using the model's own last-layer feature- and sample-attention scores. §6 argues that
learning many random-mask conditionals constrains the joint distribution.

**Key results.** Evaluation spans 11 benchmarks, including TALENT-CLS, OpenML-CC18, PFN-CLS,
TabZilla, TabArena and the authors' own BCCO-CLS (106 datasets) / BCCO-REG, filtered to
≤ 50,000 training rows, ≤ 10,000 features and ≤ 10 classes (§7.1). Averaged reciprocal rank
across all classification benchmarks: LimiX-16M 0.302, LimiX-2M 0.194, AutoGluon 0.149, TabPFN-v2
0.138, TabICL 0.136 (Fig. 1); across regression: LimiX-16M 0.292, AutoGluon 0.217, LimiX-2M 0.186,
TabPFN-v2 0.158 (Fig. 2). §7.3–7.8 add imputation, robustness, embedding, fine-tuning, generation
and OOD results. §8 fits power laws for models of 1.05M–16.53M parameters on BCCO, without
retrieval (R² > 0.99 for loss vs data size), and extrapolates fits to ~1.6B parameters.

**Strengths.** One conditional interface supports several tasks, and the masked objective gives
a principled route to imputation and generation that label-only PFNs lack. Broad regimes,
public BCCO benchmarks and scaling experiments complement predictive ranks. Models are released
under Apache 2.0; the paper links model releases and
[official inference/configuration code](https://github.com/limix-ldm-ai/LimiX) (the paper's
limix-ldm URL redirects there).

**Limitations.** Author-stated: scaling returns diminish (§8.2). Reviewer reading: the
"generalist intelligence" framing is not tested by the experiments; the headline is a
reciprocal-rank aggregate over benchmark collections including the authors' own BCCO; scaling
fits use small models (≤ 16.53M) and the billion-scale statements are extrapolations, with
inconsistent token ranges in §8 (1.7 × 10¹² vs 10¹³); and a joint-modelling objective does not
prove that the finite learned conditionals are mutually compatible — compare
[Klötergens 2026, *Do Tabular Foundation Models Agree with Themselves?*](#do-tabular-foundation),
which tests other TFMs. The evolving repository contains multiple generations, so code and
checkpoint identities must be pinned.

---

<a id="nanotabpfn"></a>

## 2025-12 — Pfefferle et al. — nanoTabPFN

**Venue:** AI for Tabular Data workshop at EurIPS 2025 · **arXiv:** [2511.03634](https://arxiv.org/abs/2511.03634) (filed v2, 18 December 2025) · **PDF:** [open](papers/2025/12_Pfefferle_et_al._nanoTabPFN_A_Lightweight_and_Educational_Reimplementation_of_TabPFN.pdf)

**Citation key:** `2025.PFEFFERLE.nanotabpfnlightweighteducationalreimplementationtabpfn`

**Where it fits.** The minGPT/nanoGPT analogue for the PFN line: an educational
reimplementation of the [TabPFN v2](#tabpfn-v2-nature) architecture and a training loop in under
500 lines of code, versus over 10,000 lines in the official TabPFN repository. It is a teaching
and prototyping tool, not a new model.

**What it contains.** Four modules (§3.1, Figs. 1–2):

* **FeatureEncoder** — normalises each feature with training-set mean/std, clips outliers, and
  linearly embeds every cell; no positional embedding, so the model stays permutation-invariant
  over rows and features.
* **TargetEncoder** — pads `y_train` with its mean for the test rows and embeds the target
  column.
* **Transformer layers** — attention across features, then across datapoints (training rows
  attend only to training rows; test rows only to training rows), each with a skip connection and
  LayerNorm, followed by a cell-wise two-layer MLP.
* **Decoder** — a two-layer MLP on the test-target cells producing class logits.

Training (§3.2) uses schedule-free AdamW without weight decay and reads **pre-generated prior
data from an HDF5 dump**; the repository has no prior implementation (the paper's data were
generated with TabICL's prior, App. A). Omitted relative to v2 (§3.4): feature-pair grouping,
the row-hash fingerprint column, native categorical and missing-value handling, regression and
preprocessing ensembles.

**Key results.** The demo trains a 3-layer, 96-dimensional, 4-head model on **80,000 synthetic
datasets of 150 rows × 5 features × 2 classes** (2,500 steps × batch 32), converging in about one
minute on one RTX 2080 Ti — reported as over 160,000× less compute than v2's pretraining (eight
GPUs for two weeks). On binary TabArena datasets with ≤ 10 features and no missing values,
subsampled to 200 rows, it beats default scikit-learn kNN, decision tree and random forest in
ROC AUC within 60 s, and shortly after beats TabPFN with ensembling and preprocessing disabled —
not default TabPFN (§4, Fig. 4; App. A). Hyperparameters came from a 200-configuration random
search (App. A, Table 1).

**Strengths.** Exposes in readable form the core mechanisms of a TabPFN-style model (cell
encoders, two-axis attention with train/test masking, training loop), with a pretraining run
cheap enough for teaching and fast architecture or training-loop experiments. Code is public.

**Limitations.** Author-stated (§5): no regression, missing-value handling or preprocessing
ensembles, no simplified prior implementation, and a deliberate small-data focus. Reviewer
reading: the comparison favours nanoTabPFN, which was pretrained at almost exactly the
evaluation scale, against a general-purpose model; the evaluation covers only a handful of tiny
binary datasets; and the HPO table's best weight decay (10⁻⁷) sits awkwardly with the stated
no-weight-decay optimiser, so the exact recipe should be read from the code.

---

<a id="tabtune"></a>

## 2025-12 — Tanna et al. — TabTune

**Venue:** preprint, Lexsi Labs · **arXiv:** [2511.02802](https://arxiv.org/abs/2511.02802) (filed v3, 2 December 2025) · **PDF:**
[open](papers/2025/12_Tanna_et_al._TabTune_A_Unified_Library_for_Inference_and_Fine_Tuning_Tabular_Foundation_Models.pdf)

**Citation key:** `2025.TANNA.tabtuneunifiedlibraryinferencefinetuningtabularfoundationmodels`

**Where it fits.** Software and benchmark paper from the lab that builds the Orion models
([Bouadi et al. 2025, *Orion-MSP*](#orion-msp); Orion-BiX). It is the harness behind that
lab's later adaptation studies (Tanna et al. 2026, *Exploring Fine-Tuning for Tabular
Foundation Models*), and it complements single-model fine-tuning studies such as
[Rubachev et al. 2025, *On Finetuning Tabular Foundation Models*](#on-finetuning) by comparing
the same adaptation recipes across architectures.

**What it contains.** A scikit-learn-compatible Python library (`TabularPipeline` front end,
`DataProcessor`, `TuningManager`, `TabularLeaderboard`; §3–4) wrapping seven TFMs: TabPFN,
TabICL, TabDPT, Mitra, ContextTab, OrionMSP and OrionBiX (Table 1).

* **Model-aware preprocessing** (§4.1): integer/numeric encoding for TabPFN, semantic vectors
  for ContextTab, normalisation for TabICL and Mitra, Set-Transformer column embeddings and
  sparse masks for the Orion models.
* **Four adaptation regimes** (§4.2): zero-shot inference; full supervised fine-tuning (for ICL
  models, each batch is split into pseudo-support and pseudo-query halves); episodic
  meta-learning on disjoint support/query samples with labels remapped per episode; and LoRA
  (r = 8, α = 16 on attention projections) for either SFT or meta-learning, silently falling back
  to full fine-tuning when adapters cannot be injected. Support is uneven: ContextTab has no
  meta-learning, TabPFN's PEFT is experimental (Table 2).
* **Evaluation modules**: accuracy, weighted F1 and AUC; ECE, MCE and Brier score; statistical
  parity, equalised-odds and equalised-opportunity differences on Adult, German Credit and COMPAS
  (§6.4).

Experiments use 155/181 TALENT, 63/72 OpenML-CC18 and 27/36 TabZilla classification datasets
(the common subset all models could run; OOM or CUDA failures excluded the rest, §6.1), with
AutoGluon-run XGBoost, LightGBM, CatBoost and random forest as baselines.

**Key results.** Ranks in Table 3 are mean accuracy ranks *within each strategy group*, not a
single leaderboard. Zero-shot: TabPFN-2.5 has the best aggregate rank (4.13), OrionMSP next
(4.61); TFMs exceed the GBDT baselines by roughly 2–4 accuracy points. Meta-learning: OrionMSP
2.26, TabPFN 2.42. Full SFT: TabPFN 1.97, TabDPT 2.79, OrionMSP 2.88, while TabICL collapses
(TabZilla accuracy 0.873 → 0.567, F1 0.870 → 0.473) and OrionBiX also degrades (§6.2). TabPFN
stays best calibrated across regimes (ECE 0.027–0.047, Brier 0.12–0.16; §7.3), whereas SFT
raises TabICL's ECE 3–4×. PEFT is reported to retain ≈95% of SFT accuracy (§7.2).

**Strengths.** One harness, one dataset subset and one metric set across seven models and four
regimes, which makes architecture × adaptation interactions visible: the same full fine-tuning
that helps TabPFN destroys TabICL. Calibration and fairness are reported next to accuracy, and
the code is public (github.com/Lexsi-Labs/TabTune).

**Limitations.** *Author-stated* (§7.7): classification only (binary and multiclass);
TabPFN's latency and memory beyond ~10K rows; degradation above ~1,000 features; partial PEFT
for TabPFN and ContextTab; ContextTab evaluated only on smaller subsets; manually specified
sensitive attributes. *Reviewer reading:* each strategy uses fixed default hyperparameters
(e.g. 3–5 epochs in the examples) with no per-dataset tuning or significance tests; within-group
ranks are not comparable across groups; Mitra's accuracies of roughly 0.31–0.55 in every regime
(Table 3) look like an integration failure rather than a model property; Table 1 misdescribes
TabDPT as diffusion-based; and the authors evaluate their own Orion models, so independent
replication matters.

---

<a id="causalpfn"></a>

## 2025-12 — Balazadeh Meresht et al. — CausalPFN

**Venue:** NeurIPS 2025 · University of Toronto / Vector Institute / Layer 6 AI ·
**arXiv:** [2506.07918](https://arxiv.org/abs/2506.07918) (filed PDF: NeurIPS 2025 proceedings version) ·
**DOI:** [10.52202/085713-5184](https://doi.org/10.52202/085713-5184) · **PDF:**
[open](papers/2025/12_Balazadeh_Meresht_et_al._CausalPFN_Amortized_Causal_Effect_Estimation_via_In_Context_Learning.pdf)

**Citation key:** `2025.BALAZADEHMERESHT.causalpfnamortizedcausaleffectestimationincontextlearning`

**Where it fits.** One of four causal PFNs here, alongside
[Robertson et al. 2025, *Do-PFN*](#do-pfn), [Robertson et al. 2025, *FairPFN*](#fairpfn) and
[Ma et al. 2026, *Foundation Models for Causal Inference via Prior-Data Fitted Networks*](#causalfm)
(CausalFM). It is the identifiable, back-door-only design: where Do-PFN trains on SCMs that may
violate unconfoundedness, CausalPFN builds ignorability into every prior DGP. It comes from the
Layer 6 group behind [TabDPT](#tabdpt), whose predictive pretraining it reuses.

**What it contains.** The target is the conditional expected potential outcome (CEPO)
µ_t(x) = E[Y_t | X = x]; CATE and ATE follow from µ_1 − µ_0. Section 3 shows that minimising a
"causal data-prior loss" makes the network approximate the posterior predictive of the CEPO,
and that this is asymptotically consistent when the prior is identifiable and contains the true DGP.

*Prior* (§4, Fig. 4): take a base table — one of 337 leakage-checked OpenML tables or a
synthetic one — pick some columns as covariates X and two others as µ_0(X), µ_1(X), optionally
add noise to get Y_0, Y_1, draw treatment T ~ Bernoulli(sigmoid(f(X))) from a random function f,
and observe Y = Y_T. Because T depends only on X, ignorability holds by construction; the
sigmoid ensures positivity. Treatments are binary in the implementation.

*Model:* a ~20M-parameter PFN-style encoder (20 layers) with (t, x, y) context tokens and (t, x)
query tokens attending only to the context. Each query outputs a 1,024-bin histogram over the
CEPO, trained with a Gaussian-smoothed histogram loss. Training is two-stage: TabDPT-style
predictive pretraining (context up to 16K), then the causal loss (context 2,048) (App. D.2).
Inference returns the posterior mean and credible intervals from 10,000 samples; the default
context is 4,096 rows.

**Key results.** Over 310 realisations (100 IHDP, 10 ACIC 2016, Lalonde CPS and PSID), it has
the best average CATE rank (PEHE rank 2.30 vs T-Learner 3.57 and DA-Learner 3.60); on ATE it is
competitive, not best (4.45 vs T-Learner 4.31 and IPW 4.41) (Table 1). Most baselines are
cross-validated and grid-searched. On five marketing RCTs subsampled to 50K rows it has the best
average normalised Qini score (0.952 vs X-Learner 0.944; Table 2), but on full tables (up to
2.5M rows, via retrieval) it falls to fifth of five (0.924; App. Table 7). Credible intervals are
calibrated in distribution but severely overconfident on out-of-distribution DGPs. Temperature
scaling, tuned so that observable-outcome coverage is nominal, makes CATE intervals calibrated or
conservative (Fig. 7). TabPFN v2 used as a CEPO regressor is competitive, but CausalPFN beats it
everywhere except ACIC 2016; fine-tuning TabPFN on the causal prior narrows the gap (Table 3).

**Strengths.** A strong out-of-the-box CATE estimator with no per-dataset tuning; uncertainty
that can be recalibrated from observational data; ablations against TabPFN that separate the
effect of an identifiable causal prior; and released weights and code. Independent evidence:
CausalFM's appendix ACIC 2016 table puts CausalPFN's PEHE (0.239) ahead of CausalFM (0.638) and
Do-PFN (0.857).

**Limitations.** *Author-stated* (§7): strong ignorability is untestable and is assumed
throughout; guarantees are asymptotic and assume a well-specified prior; performance drops on
the largest tables; only binary treatments are implemented; no instrumental-variable or other
non-back-door settings. *Reviewer reading:* App. D.4 clarifies that the speed advantage in
Fig. 1 is wall-clock time including baseline tuning, not a faster estimator. The benchmarks are
standard semi-synthetic suites that satisfy ignorability by design. CausalFM's argument against
priors that mix identifiable and non-identifiable settings targets Do-PFN's design, not this
one; for CausalPFN, the open risk is unmeasured confounding, which the model cannot detect.

---

<a id="tabstar"></a>

## 2025-12 — Arazi et al. — TabSTAR

**Venue:** NeurIPS 2025 · Technion — Israel Institute of Technology ·
**arXiv:** [2505.18125](https://arxiv.org/abs/2505.18125) (filed PDF: NeurIPS 2025 proceedings version) ·
**DOI:** [10.52202/085713-5726](https://doi.org/10.52202/085713-5726) · **PDF:**
[open](papers/2025/12_Arazi_et_al._TabSTAR_A_Tabular_Foundation_Model_for_Tabular_Data_with_Text_Fields.pdf)

**Citation key:** `2025.ARAZI.tabstartabularfoundationmodeltabulardatatextfields`

**Where it fits.** The text-field branch of the TFM family. Unlike PFN-style models, it is a
pretrain-then-fine-tune model, closer in spirit to
[Kim et al. 2024, *CARTE*](#carte-pretraining-and) than to frozen ICL. Its links to the PFN
line are concrete: the first author is listed among the TabPFN-3 report's contributors, and that
report evaluates TabPFN-3-Plus on the TabSTAR text-tabular collection
([Grinsztajn et al. 2026, *TabPFN-3*](#tabpfn-3)).
[Purucker et al. 2026, *Beyond IID*](#beyond-iid) draws datasets from the TabSTAR benchmark, and
the same group's [MulTaBench](#multabench-benchmarking-multimodal) extends the
target-aware-encoder argument to images. Compare
[Spinaci et al. 2025, *ConTextTab*](#contexttab), which adds semantics to a frozen ICL model instead.

**What it contains.** The critique: earlier language-model-based tabular methods use static,
target-agnostic text embeddings. TabSTAR (§3) has five modules and **no dataset-specific
parameters**:

1. *Verbalisation* — every feature becomes a "name: value" string. Numerical features are also
   binned into 10 quantile bins (e.g. "Age: 45–51 (Quantile 60–70%)") and keep their
   standardised value. Each possible target value (classification) or the target name
   (regression) becomes an extra **target token**.
2. *Encoding* — an e5-small-v2 text encoder with its upper half unfrozen; numbers pass through a
   small MLP.
3. *Fusion* — one transformer layer merges each feature's semantic and numeric embeddings.
4. *Interaction* — a 6-layer encoder without positional encoding, where features and target
   tokens attend to each other.
5. *Prediction* — a shared classification head scores each target token (softmax over classes,
   so any class count works); a shared regression head reads the single target token.

Pretraining uses 350 curated datasets (253 classification, 97 regression) plus 40 of the 50
benchmark datasets, in five variants so that each benchmark dataset is held out of one variant.
Each task is then **fine-tuned with LoRA** on the layers unfrozen in pretraining (§4). It is not
a training-free ICL model.

**Key results.** The benchmark has 50 text-feature datasets: 14 classification, 36 regression,
29 of the regression sets from CARTE. Evaluation uses 10 random splits per dataset. In
classification with ≤10K training rows, TabSTAR's normalised score is 0.83 vs TabM-Tuned 0.73,
CatBoost-Tuned 0.69 and TabPFN-v2 0.67 (via its API); without the row cap it scores 0.84 vs
TabM-Tuned-Unlimited 0.79 (Fig. 2). In regression it is competitive but not best; GBDTs lead,
TabPFN-v2 is better than TabSTAR, and the gap to GBDTs persists without the row cap (Fig. 3).
Median training time is 493 s vs 39–86 s for GBDTs, while inference is GBDT-like (3.0 s) and far
cheaper than TabICL or TabDPT (Table 3). Ablations: unfreezing even one encoder layer beats static
embeddings and six layers is best (Fig. 4); more pretraining datasets (16 → 64 → 256) improve
both AUROC and R² (Fig. 5); quantile-bin verbalisation beats name-only or name-plus-bin (Table 4).

**Strengths.** Target-aware, fine-tunable text representations are a clear advance over frozen
embeddings, and the paper isolates that effect directly. Shared target-token heads remove the
class-count cap without dataset-specific layers. The held-out-variant protocol gives every
benchmark dataset an uncontaminated model, and code and variants are released.

**Limitations.** *Author-stated* (§7): regression lags GBDTs; memory limits with hundreds of
features; training slower than GBDTs and ICL TFMs; little evaluation in few-shot or purely
numerical settings. *Reviewer reading:* the benchmark has only 14 classification datasets (11 in
the TabPFN-v2 head-to-head), so the classification headline rests on a small sample. The
"scaling law" is three pretraining sizes plus a no-pretraining point on a 20-dataset analysis
subset, not a fitted law. Per-task LoRA fine-tuning makes deployment heavier than frozen ICL, and
the method only pays off when columns carry natural-language content.

---

<a id="contexttab"></a>

## 2025-12 — Spinaci et al. — ConTextTab

**Venue:** NeurIPS 2025 · SAP France / SAP SE ·
**arXiv:** [2506.10707](https://arxiv.org/abs/2506.10707) (filed PDF: NeurIPS 2025 proceedings version) ·
**DOI:** [10.52202/085713-4918](https://doi.org/10.52202/085713-4918) · **PDF:**
[open](papers/2025/12_Spinaci_et_al._ConTextTab_A_Semantics_Aware_Tabular_In_Context_Learner.pdf)

**Citation key:** `2025.SPINACI.contexttabsemanticsawaretabularincontextlearner`

**Where it fits.** A bridge between table-native ICL models and LLM-based tabular learners. It
is the empirical companion to SAP's position paper,
[Klein and Hoffart 2026, *Position: Foundation Models for Tabular Data within Systemic Contexts
Need Grounding*](#klein-grounding). It keeps frozen in-context inference but, unlike
[TabSTAR](#tabstar), does not fine-tune per task. Where
[Garg et al. 2025, *Real-TabPFN*](#real-tabpfn) uses real data for distributional realism,
ConTextTab uses it for semantics.

**What it contains.** The diagnosis (§1): synthetic-prior ICL models (TabPFN, TabICL) are
efficient but cannot use the meaning of column names or categories, while LLM-based learners
such as TabuLa-8B have that knowledge but short contexts and no row/column permutation
invariance. ConTextTab's changes (§3):

* *Modality-specific encoding.* Text and categorical cells, and column headers, are embedded
  with a small sentence model (all-MiniLM-L6-v2) plus learned projections; header embeddings
  replace positional encodings. Dates sum learned day, month and year embeddings. Numbers are
  clipped to the 2–98% quantiles, standardised and multiplied by a learned vector; the bias acts
  as a NaN flag. All of this is equivariant to row and column permutations.
* *Backbone.* An essentially unchanged TabPFN v2-style stack alternating cross-column and
  cross-row attention, with weights shared across blocks. The "base" model has 12 blocks of
  width 768: 172M parameters in total, 16M trainable thanks to sharing.
* *Decoding.* A cross-entropy MLP head for classification (with a target-column encoding that
  breaks full label equivariance) and an L2 head for regression; soft-binning and a
  supervised-clustering head are alternatives.
* *Pretraining* (§4.1). The T4 web-table corpus filtered to tables of at least 150 rows: 2.18M
  tables, median 750 rows × 9 columns. Each step samples 1,000 rows (50–900 as queries) and a
  random target column, for 4–10M steps on one H100 (4–12 days).
* *Inference.* 8-fold bagging with context c = 8,192, although training contexts never exceed
  950 rows.

**Key results.** 203 tasks (112 classification, 91 regression) over CARTE, OpenML-CC18,
OpenML-CTR23, TALENT-Tiny (45 datasets) and TabReD, each evaluated on one fixed split (Table 1).
ConTextTab ranks first on CARTE (rank 1.55, accuracy 76.9, R² 72.4), significantly better than
every model except CatBoost and AutoGluon (Fig. 2), and leads at every subsample size from 128
rows, beating AutoGluon up to 2,048 rows (Fig. 3). Overall rank is 2.96 vs RealMLP-HPO-CV 2.50
and CatBoost-HPO-CV 2.71; on the non-semantic suites the gap is mostly not significant (§5).
Ablations (Table 2) on CARTE: replacing semantic features with ordinal encoding costs 2.7
accuracy and 4.8 R² points; anonymising column names costs about 1 and 2 points. A larger model
gives no gain; training data below about 100K tables hurts.

**Strengths.** The clearest controlled evidence here that cell and column-name *semantics* carry
signal that anonymous-feature synthetic priors discard by construction. The design keeps the
efficiency and permutation symmetry of table-native ICL, ablations are paired with significance
tests, and code and checkpoints are public.

**Limitations.** *Author-stated* (§6): real-data training raises contamination risk. Their
embedding-similarity check found no CARTE tables in T4, but OpenML overlap is deferred to the
T4 authors' study. All table-native ICL models, including this one, fail to scale to very large
datasets, and gains saturate with more T4 data. *Reviewer reading:* tuned, cross-validated GBDTs
and RealMLP still rank higher outside semantic data. Single fixed splits limit precision.
Context lengths at inference extrapolate far beyond training. The benefit concentrates where
columns carry natural-language meaning and shrinks on anonymised numeric tables.

---

<a id="equitabpfn"></a>

## 2025-12 — Arbel et al. — EquiTabPFN

**Venue:** NeurIPS 2025 · INRIA, University of Freiburg, ELLIS Institute Tübingen, Prior Labs ·
**arXiv:** [2502.06684](https://arxiv.org/abs/2502.06684) (filed PDF: NeurIPS 2025 proceedings version) ·
**DOI:** [10.52202/085713-2097](https://doi.org/10.52202/085713-2097) · **PDF:**
[open](papers/2025/12_Arbel_et_al._EquiTabPFN_A_Target_Permutation_Equivariant_Prior_Fitted_Network.pdf)

**Citation key:** `2025.ARBEL.equitabpfntargetpermutationequivariantpriorfittednetwork`

**Where it fits.** A symmetry argument from authors that include Frank Hutter and a Prior Labs
affiliation. TabPFN is equivariant to row order, and bi-attention models such as TabPFN v2 are
also equivariant to column order. EquiTabPFN adds the missing third symmetry, the order of the
*target* (class) dimensions. It removes the class-count cap by construction; ECOC, hierarchical
classification ([Qu et al. 2025, *TabICL*](#tabicl-2025)) and
[Wu and Bergman 2025, *APT*](#apt)'s mixture-block output are the alternatives.

**What it contains.** *Theory* (§5). A one-hot classification target has no canonical order, so
permuting classes should permute predictions. TabPFN's linear target encoder and fixed-width
MLP decoder break this. The **target-equivariance gap** is
E_equi(f) = L(f) − L(f_equi), where f_equi averages f over all class permutations. Under a
strictly convex, permutation-invariant loss and a permutation-invariant data prior, the gap is
non-negative (Prop. 5.3). The pretraining objective therefore splits into this gap plus an
optimality error, so a non-equivariant model carries an extra error term that an equivariant
one avoids. Empirically, TabPFN's equivariance violations decline only slowly during training
(Fig. 3). Hollmann et al.'s class-permutation ensembling is a mitigation, but exact averaging
needs O(q!) calls.

*Architecture* (§4, Fig. 1):
* *Encoder.* Each covariate vector becomes one token. Each target component becomes its own
  token via a shared 1×1 convolution, and unknown test targets are replaced by a learned
  prediction token.
* *Attention.* Layers alternate between attention across components within a row (target tokens
  attend only to the covariate token) and attention across rows (all tokens attend only to
  training rows).
* *Decoder.* A non-parametric attention decoder averages the training targets with
  attention weights, then a point-wise MLP adds a residual correction, preserving equivariance.

The ~25M-parameter model is trained for about 4 days on one A100, on TabPFN v1's public prior
and code, with fewer than 10 classes (§6.1).

**Key results.** Evaluation uses TabZilla classification: 76 tasks with ≤10 classes and 10 tasks
with >10 classes, accuracy relative to kNN, and no ensembling for EquiTabPFN. On the >10-class
tasks, EquiTabPFN has the best median relative accuracy; TabPFN v2 with ECOC falls below a linear
model and random forest in median, and runs slower (Fig. 4, right). The pattern holds for AUC and
F1 (App. C). On ≤10 classes it is comparable to TabPFN v2 and consistently beats **TabPFNv2\***,
v2's architecture retrained on the same public prior. Extra ensembling helps TabPFN v2 only
marginally relative to its cost (Fig. 5).

**Strengths.** Formalises a real architectural defect and explains an existing workaround
(permutation ensembling) instead of adding one. The TabPFNv2\* control separates architecture
from the closed v2 prior, and arbitrary class counts come by construction rather than through
costly post-processing. Code is released.

**Limitations.** *Author-stated* (§7): attention across target components adds a cost quadratic
in the number of target dimensions. Some targets are not exchangeable — ordinal labels, 5 of
86 surveyed datasets — and would need a non-equivariant prior or positional embeddings.
*Reviewer reading:* the model is classification-only and trained on the older v1 prior, so it is
not compared at equal prior quality with current TabPFN checkpoints. The >10-class evidence
rests on 10 datasets, and the main results are medians of accuracy relative to kNN shown in
figures; critical-difference diagrams appear only in the appendix (Figs. 7–8).

---

<a id="from-tables-to-time"></a>

## 2026-01 — Hoo et al. — From Tables to Time

**Provenance.** TMLR (journal version per Zotero) · arXiv
[2501.02945v4](https://arxiv.org/abs/2501.02945v4) (filed version, 26 January 2026) · University
of Freiburg / Prior Labs / ELLIS Tübingen · code:
[PriorLabs/tabpfn-time-series](https://github.com/PriorLabs/tabpfn-time-series) · **PDF:**
[open](papers/2026/01_Hoo_et_al._From_Tables_to_Time_Extending_TabPFN_v2_to_Time_Series_Forecasting.pdf)

**Citation key:** `2026.HOO.tablestimeextendingtabpfnv2timeseriesforecasting`.

**Where it fits.** The full version of the same authors' workshop paper, [Hoo 2024, *TabPFN
Outperforms Specialized Time Series Forecasting Models*](#2024-12--hoo-et-al--tabpfn-outperforms-specialized-time-series-forecasting-models).
It recasts forecasting as *tabular regression* and uses the **unmodified** pretrained TabPFN-v2
([Hollmann 2025, *Accurate predictions on small data with a tabular foundation
model*](#tabpfn-v2-nature)) as the forecaster, released as **TabPFN-TS**. It is the main evidence
in this collection that a synthetic tabular prior transfers to another modality without
modality-specific pretraining.

**What it contains.** Each time step of a series becomes one table row (§3.1, Fig. 3.1). The
features are all derived from the timestamp, so they are known for the forecast horizon:

* a **running index** (time progression);
* **calendar features**: sin/cos encodings of eight cyclic components (second of minute up to
  month of year) plus the calendar year;
* **automatic seasonal features**: the top-*k* periods found by an FFT of the linearly detrended,
  Hann-windowed, zero-padded series (Algorithm 1), encoded as sin/cos pairs;
* optional **known-in-advance covariates** (e.g. holidays, control inputs).

Lagged and rolling features are deliberately excluded, since they would require recursive
multi-step prediction. The historical rows form the context and the horizon rows the query set;
TabPFN-v2's binned predictive distribution gives the mean, median and arbitrary quantiles
(§3.2). Each series needs its own forward pass; there is no fine-tuning.

**Key results.**

* **Covariate-informed forecasting (fev-bench, §4.2, Fig. 4.2).** On the 28 tasks with
  covariates known over both history and horizon (30 eligible; two excluded for exceeding the
  6-hour limit), TabPFN-TS (11M parameters) has the strongest overall MASE and WQL against
  TiRex, Chronos-Bolt, Toto-1.0, Moirai-2.0 and Sundial.
* **Univariate forecasting (GIFT-Eval, 97 tasks, §4.1, Fig. 4.1).** It ranks closely behind
  TiRex, Toto-1.0 and Moirai-2 and on par with TimesFM-2.0 and Chronos-Bolt, models the authors
  describe as over two orders of magnitude larger.
* **Backbone swap (§5.4, Fig. 5.5).** TabDPT as backbone (point forecasts only, 78 of 97 tasks)
  gives usable forecasts at roughly Chronos-Bolt-Tiny level, well below TabPFN-TS; see [Ma 2026,
  *TabDPT*](#tabdpt).
* **Featurisation ablation (§5.5, Fig. 5.6, 81 smallest tasks).** Index, calendar and automatic
  seasonal features are complementary; index-only or seasonal-only is much worse.
* **Cost (§6.2, Fig. 6.1).** About 30× the single-GPU-equivalent inference time of
  Chronos-Bolt-Base and TimesFM-2.0.

**Strengths.** A simple, fully specified construction with public code; tested on two
standard benchmarks against current TSFMs; quantile forecasts come for free; the qualitative
analyses (§5.1–5.3) and the backbone swap explain *why* it works rather than only reporting a
rank.

**Limitations.** Author-stated (§6): trends cannot be extrapolated beyond the range of observed
targets, a structural consequence of the interpolation-oriented pretraining objective, and
inference is ~30× slower because of one forward pass per series and quadratic attention.
Reviewer reading: the univariate result is "competitive", not a win; fev-bench admits only tasks
whose covariates are known over the horizon, which is the setting the tabular formulation is
built for, and drops two tasks that timed out.

---

<a id="klein-grounding"></a>

## 2026-01 — Klein and Hoffart — Position: Foundation Models for Tabular Data within Systemic Contexts Need Grounding

**Provenance.** Position paper, arXiv preprint · arXiv
[2505.19825v2](https://arxiv.org/abs/2505.19825v2) (filed version, 17 January 2026) · SAP SE ·
no code (conceptual paper) · **PDF:**
[open](papers/2026/01_Klein_and_Hoffart_Position_Foundation_Models_for_Tabular_Data_within_Systemic_Contexts_Need_Grounding.pdf)

**Citation key:** `2026.KLEIN.positionfoundationmodelstabulardatasystemiccontextsneedgrounding`.

**Where it fits.** A contrarian counterpart to [Breugel 2024, *Why Tabular Foundation Models
Should Be a Research Priority*](#2024-06--breugel-and-schaar--why-tabular-foundation-models-should-be-a-research-priority),
whose "isolated tables" scope it accepts only for narrow, static tasks (§5). It argues that
single-table TFMs (TabPFN, TabICL, ConTextTab) and relational models over foreign-key graphs
(RelBench GNNs, CARTE, KumoRFM; compare [Hudovernik 2026, *KumoRFM-2*](#kumorfm-2-scaling))
both miss the **operational context** — business rules, application code and process
knowledge — that determines how enterprise data is generated.

**What it contains.**

* **Diagnosis (§1–2).** Current models assume the information needed for prediction is
  contained in the tables. The running example is an expense rule `if amount >= 5000:
  require_manager_approval()`: a statistical model may learn a fuzzy threshold near $4,800, and
  retrieval-augmented generation may retrieve the code as text without treating `>=` as a hard
  boundary, whereas a model that reads **code as logic** would be exact without examples.
* **Semantically Linked Tables (SLT, Fig. 1).** Relational data plus declarative knowledge
  (data models, business objects, rules, process models), procedural knowledge (application
  code, agent logic in natural language) and operational world knowledge. A **Foundation Model
  for SLT (FMSLT)** is proposed as a new model class over this bundle.
* **Data challenges (§3).** Silos, privacy and the scarcity of public multi-table data with
  attached logic.
* **Training sketch (§4, Fig. 4).** "Retrieval-augmented in-context learning": phase 1 learns
  to predict row outcomes from arbitrary rules on procedurally generated synthetic systems and
  open-source code–database pairs (with injected noise and "simulated technical debt"); phase 2
  retrieves an organisation's rules, code and tables at inference and predicts zero-shot. This
  transposes the PFN idea — learn inference from synthetic tasks — from functions to business
  logic.
* **Call to action (§6).** (1) An **Operational Turing Test** (Def. 6.1): join an unseen
  simulated organisation, predict a transaction's outcome from its rules, code, relational
  data and a few examples, and justify the decision by citing the relevant artefacts; (2)
  privacy-preserving data sandboxes; (3) privacy-preserving multi-table synthetic data; (4)
  architectures that natively process relations, code and rules while keeping ICL.

**Key results.** None empirical. The motivation cites external enterprise-agent benchmarks,
e.g. agents completing about 30% of tasks needing implicit business knowledge in
TheAgentCompany and 35.3% success on complex enterprise tasks in AgentArch (§1).

**Strengths.** Names a real gap in how TFMs are framed for enterprise data, with a concrete
example, a layered definition of the missing context and a falsifiable benchmark proposal.
The synthetic-training sketch is a coherent extension of the prior-fitting philosophy.

**Limitations.** No architecture, loss, dataset, benchmark instance or numbers. The authors
acknowledge that realistic synthetic generators, retrievers over large organisational systems
and the "provenance gap" (mapping rows to the code that produced them) are open problems
(§4). Reviewer reading: the "Alternative Views" section mainly restates the position rather
than engaging counter-arguments, and the claim that no existing TFM can pass the test is
asserted, not tested.

---

<a id="tabdpt"></a>

## 2026-01 — Ma et al. — TabDPT

**Provenance.** NeurIPS 2025 (the filed PDF is the camera-ready revision posted to arXiv) ·
arXiv [2410.18164v3](https://arxiv.org/abs/2410.18164v3) (filed version, 17 January 2026) · DOI
[10.52202/085713-5748](https://doi.org/10.52202/085713-5748) · Layer 6 AI (Toronto) · open
weights on [Hugging Face](https://huggingface.co/Layer6/TabDPT), inference and training code on
[GitHub](https://github.com/layer6ai-labs/TabDPT-inference), training-dataset list released ·
**PDF:** [open](papers/2026/01_Ma_et_al._TabDPT_Scaling_Tabular_Foundation_Models_on_Real_Data.pdf)

**Citation key:** `2025.MA.tabdptscalingtabularfoundationmodelsrealdata` (Zotero files the
NeurIPS 2025 version).

**Where it fits.** The real-data pole of the synthetic-versus-real spectrum: a TFM pretrained
only on real OpenML tables, with no synthetic prior, set against the TabPFN line ([Hollmann
2025, *Accurate predictions on small data with a tabular foundation model*](#tabpfn-v2-nature)).
Its successor drops retrieval for long-context pretraining ([Hosseinzadeh 2026,
*TabDPT-Turbo*](#tabdpt-turbo)); [Hoo 2026, *From Tables to Time*](#from-tables-to-time) uses it
as an alternative forecasting backbone.

**What it contains.** Three components (§3):

* **Row-based transformer** (§3.1). Each row is one token after padding or PCA-reducing the
  features to F_max = 100; a shared backbone has a classification head (C_max = 10 classes) and
  a regression head (Table C.1). Column permutation at training time gives approximate
  feature-order invariance. More classes are handled by encoding labels in base C_max
  (⌈log_Cmax C⌉ forward passes), more features by PCA (§3.4).
* **Self-supervised targets on real tables** (§3.2). Each training step picks a random column
  with enough unique values as the target (standardised for regression, binned for
  classification) and predicts it from the other columns, which are shuffled and randomly
  dropped. The number of tasks grows combinatorially with the feature count, which counters the
  overfitting that supervised training on ~one target per table causes.
* **Retrieval in training and inference** (§3.3–3.4). Contexts are formed from rows close to
  each other in feature space, matching the kNN (faiss) context retrieval used for every test
  query at inference.

Pretraining data: 123 OpenML datasets, 32M rows, 2B cells (§4.1), screened against the
evaluation sets with a metadata-based contamination analysis (Appendix B.1). The main model
has 78M parameters and 16 layers.

**Key results.**

* **CC18 (72 classification) and CTR23 (35 regression), Table 1.** TabDPT: AUC 0.933, accuracy
  0.884, correlation 0.837, R² 0.742; TabPFN v2: 0.932, 0.872, 0.835, 0.740. Only the accuracy
  gap is outside the bootstrap CIs. Tuned TabM/TabR/MLP-PLR and GBDTs trail; TabDPT without the
  validation split ("no val.") is beaten only by TabM on CC18 accuracy.
* **Ablations (§4.4, Fig. 4).** Removing self-supervised targets causes overfitting after ~50
  epochs and the largest drop; removing training-time or inference-time retrieval also hurts.
  Training on the TabPFN v1 synthetic generator gives higher test loss than real data with SSL
  under the same compute (Fig. 4b).
* **Scaling (§4.5, Fig. 1).** Models from 33K to 78M parameters on 52M to 2B cells follow a joint
  power law with exponents α = 0.42 (parameters) and β = 0.39 (data), which the authors call
  the first domain-general TFM scaling-law analysis.
* **Few-shot (§4.6, Table 2).** A pseudo-labelling variant, TabDPT (semi), beats STUNT on 5 of
  7 CC18 datasets in the 10-shot setting (average 77.6% vs 76.8%).
* **Speed (§4.7, Fig. 3b).** At least an order of magnitude faster than tuned per-dataset
  baselines once their search is counted, comparable to TabPFN v2; tree pipelines remain
  faster for inference alone.

**Code-dump note.** In `TabDPT.txt` the released training-set list sits under
`tabdpt_datasets/data_splits/` (`cls_datasets.csv`, `reg_datasets.csv`). An evaluation that uses
TabDPT as a baseline should check its held-out datasets against that list.

**Strengths.** Fully open (weights, training code, dataset list) with an explicit contamination
audit and a "Bitter Lessons" appendix of failed variants (Appendix A). The self-supervised
target trick is a simple, reusable answer to the scarcity of labelled real tables, and the
scaling study is a systematic model-by-data grid rather than a single curve.

**Limitations.** Hard caps of 100 features and 10 classes need lossy PCA and base-C
decomposition. Margins over TabPFN v2 are small (CI-overlapping except CC18 accuracy). The
real-versus-synthetic comparison uses the old TabPFN v1 generator, not a current prior. No
calibration metrics are reported. Author-stated (§5): feature-name embeddings overfitted, and
the model assumes i.i.d. rows, with no temporal, shift or hierarchical structure. Per-query
retrieval adds deployment complexity; its successor removes it.

---

<a id="tabpfn-25"></a>

## 2026-02 — Grinsztajn et al. — TabPFN-2.5

**Provenance.** Technical report (Prior Labs Team), arXiv preprint · arXiv
[2511.08667v2](https://arxiv.org/abs/2511.08667v2) (filed version, 5 February 2026; report
dated 6 November 2025) · Prior Labs · weights on Hugging Face under the non-commercial
TABPFN-2.5 License v1.0, `tabpfn` package and cloud API; prior and distillation engine not
released · **PDF:**
[open](papers/2026/02_Grinsztajn_et_al._TabPFN_2.5_Advancing_the_State_of_the_Art_in_Tabular_Foundation_Models.pdf)

**Citation key:** `2026.GRINSZTAJN.tabpfn25advancingstatearttabularfoundationmodels`.

**Where it fits.** The successor to TabPFN v2 ([Hollmann 2025, *Accurate predictions on small
data with a tabular foundation model*](#tabpfn-v2-nature)) and the predecessor of the
architectural reset in [Grinsztajn 2026, *TabPFN-3*](#tabpfn-3). It keeps v2's design and scales
it to 50,000 rows × 2,000 features (a 20× increase in cells), and ships a real-data
continued-pretrained sibling following [Garg 2025, *Real-TabPFN*](#real-tabpfn).

**What it contains.** Changes relative to v2 (§3):

* **Architecture.** Same alternating row/feature attention; depth raised from 12 to 18 layers
  (regression) and 24 (classification); feature-group size 3 instead of 2; a 2-layer MLP target
  encoder for regression; 64 learned "thinking" rows that add compute and act as attention
  sinks.
* **Prior.** An improved, broader synthetic prior (undisclosed); the base model is
  synthetic-only. Prior and architecture hyperparameters (~50) were tuned by training ~100 models
  and using TabPFN v2 as a surrogate over 10,000 configurations.
* **Real-TabPFN-2.5.** Continued pretraining on 43 curated OpenML/Kaggle datasets, deduplicated
  against internal benchmarks and all of TabArena by identifiers, schemas and row/column hashes
  (Appendix C).
* **Post-processing and deployment.** Optional decision-threshold tuning and multiclass
  temperature scaling (off in all reported results); a proprietary **distillation engine** that
  turns the model into a dataset-specific MLP or tree ensemble (§4.4); 1–2.3× faster than v2
  despite the larger network (Appendix I).

**Key results.**

* **TabArena-Lite (51 datasets, one fold), ≤10K rows and 500 features (Fig. 3).** Default
  TabPFN-2.5 outperforms every other model in a forward pass; on classification it beats
  AutoGluon 1.4 extreme (4-hour tuned ensemble including v2); regression needs tuning (60
  configurations) to pass AutoGluon. Real-TabPFN-2.5 widens the classification lead.
* **All TabArena datasets, up to 100K rows and 2K features (Fig. 4).** Best default model;
  tuned, it outperforms (regression) or approaches (classification) AutoGluon 1.4. Default
  Real-TabPFN-2.5 beats every tuned-and-ensembled model on classification.
* **Versus v2 (Fig. 2).** Better on almost all datasets of the v2-compatible subset and "never
  much worse" (Wilcoxon p < 0.0001).
* **Versus default XGBoost (abstract).** 100% win rate on classification with ≤10K rows and 500
  features; 87% on larger classification datasets and 85% on regression.
* **Internal benchmark (§4.2, Figs. 5–6).** Over 100 proprietary use cases up to 50K rows: default
  TabPFN-2.5 beats 1-hour-tuned GBDTs.
* **Causal inference (§4.5, Fig. 9).** On RealCause, PFN-based CATE methods take the first seven
  places; TabPFN-2.5 as a T-learner ranks first by PEHE.

**Model-card note (not the paper).** `Huggingface TabPFN.txt` (a Hugging Face model-card
snapshot) lists `_default` as the real-data checkpoint and `_default-2` as the synthetic-only one,
plus specialist variants such as `_large-features-XL`, `_low-skew` and `_quantiles`. TabPFN v2.6,
released later without a paper, makes its single `_default` checkpoint synthetic-only again.

**Strengths.** A clear, statistically tested improvement over v2 on public TabArena, with the
real-data variant deduplicated against the evaluation suite. Explicit about license terms and
about reporting uncalibrated default scores. The distillation route addresses a real deployment
need (low latency, conventional model classes).

**Limitations.** A vendor report, not peer reviewed. The new prior and the distillation engine
are undisclosed, so the gains cannot be attributed or reproduced. TabArena-Lite uses one test
fold, and TabPFN-2.5 is tuned with 60 configurations versus 200 for baselines. The internal
benchmark is proprietary. No calibration metrics (ECE, Brier) are reported. Weights may not be
used commercially or in production, including for internal commercial decisions (§6).

---

<a id="causalfm"></a>

## 2026-02 — Ma et al. — Foundation Models for Causal Inference via Prior-Data Fitted Networks

**Provenance.** ICLR 2026 (conference paper) · arXiv
[2506.10914v3](https://arxiv.org/abs/2506.10914v3) (filed version, 24 February 2026) · LMU
Munich & MCML · code: [CausalFM](https://github.com/yccm/CausalFM) and the
[CausalFM Toolkit](https://github.com/yccm/CausalFM-toolkit) · **PDF:**
[open](papers/2026/02_Ma_et_al._Foundation_Models_for_Causal_Inference_via_Prior_Data_Fitted_Networks.pdf)

**Citation key:** `2026.MA.foundationmodelscausalinferencepriordatafittednetworks`.

**Where it fits.** The causal-inference branch of the PFN line. The two concurrent causal PFNs
cover less: [Balazadeh Meresht 2025, *CausalPFN*](#2025-12--balazadeh-meresht-et-al--causalpfn)
assumes back-door adjustment (unconfoundedness) throughout, and [Robertson 2025,
*Do-PFN*](#2025-11--robertson-et-al--do-pfn) trains one PFN on a mixture of causal graphs
without identifiability constraints (Table 1, Appendix A.1). **CausalFM** is a recipe for
training a PFN per identified causal setting and is the first in the corpus to cover
**front-door** and **instrumental-variable (IV)** adjustment as well as back-door. It inherits
the Bayesian reading of PFNs from [Nagler 2023, *Statistical Foundations of Prior-Data Fitted
Networks*](#nagler-theory).

**What it contains.**

* **Priors over observational–interventional pairs (§4.1).** Instead of a prior over the
  observational distribution only (which would require plugging the PFN into a hand-derived
  identification formula, e.g. an integral equation for IV), the prior is placed on structural
  causal models (SCMs). An SCM simulates both the observational data and the interventional
  outcome under do(A=a), so the PFN can be trained to output the interventional posterior
  predictive directly.
* **Theory (§4.2, Theorem 4.3).** A prior is *well-specified* if the causal query evaluated on
  the posterior-predictive interventional distribution is consistent. Under mild conditions, a
  well-specified prior must put **zero mass** on SCMs that violate the setting's identifiability
  assumptions. This is the paper's argument against Do-PFN-style mixture priors, whose
  posteriors may never concentrate on the true effect.
* **Prior construction (§4.3).** The practitioner supplies a cluster-DAG (C-DAG) for the
  setting plus constraints (positivity; for IV, additive separability of the confounder in the
  outcome equation). Latent clusters are standard normal; mixed observed/latent clusters get a
  TabPFN-style clustered Bayesian-neural-network prior; purely observed clusters get an
  observational BNN prior. Running examples: back-door (X, A, Y), front-door with a mediator M
  and an unobserved A–Y confounder, and IV with instrument Z.
* **Training (§5).** The loss pairs a context sampled from the *observational* distribution with
  query targets sampled from the *interventional* one (for CATE, y(1) − y(0) after do(A=1) and
  do(A=0)). The backbone is the TabPFN architecture with a Gaussian-mixture output head; about
  24 hours on one A100 per model. Prior and generation details are in Appendix D.1.
* **Identification is chosen, not learned.** The introduction says the model "automatically
  learns to select" an identification formula, but only in the sense that it learns the
  estimator implied by its prior: the setting (back-door, front-door or IV) is chosen by the
  practitioner before estimation, and each setting has its own trained model (Appendix A.1).

**Key results.** All metrics are PEHE (root-mean-squared CATE error; lower is better).

* **Back-door (Table 2).** Average over 10 synthetic datasets: CausalFM 0.515 vs CausalPFN 0.557,
  Do-PFN 0.586 and X-learner 0.563 (best classical). Semi-synthetic Jobs: 0.478 vs Do-PFN 0.482
  and CausalPFN 0.528. Per dataset (Table 5) it is best on five of the ten; Do-PFN is best on
  the other five.
* **ACIC 2016 (Appendix H.3, Table 6).** CausalFM 0.638 vs **CausalPFN 0.239** and X-learner
  0.519, i.e. it loses clearly on this semi-synthetic benchmark outside its own prior.
* **IV (Table 3).** Binary instrument: 0.422, best, narrowly ahead of DeepIV 0.427 and KIV 0.454.
  Continuous instrument: 0.579, behind DeepIV 0.516 and level with KIV 0.577.
* **Front-door (Table 4).** 0.847 vs 0.889 for the neural plug-in front-door learner and 1.274 for
  Do-PFN.
* **Wrong identification hurts (Table 9).** Using a back-door model on IV data raises PEHE from
  0.422 to 0.489; on front-door data from 0.847 to 0.876.
* **Speed (Tables 10–11).** About 0.5 s inference per dataset, versus seconds to tens of seconds
  for per-dataset learners (KIV, at 0.32 s, is the exception).

**Strengths.** A principled separation of identification (domain knowledge, chosen by the
analyst) from estimation (amortised by the PFN), backed by a formal result that explains why
identifiability must be encoded in the prior. One recipe covers three settings, with the first
PFNs for front-door and IV. Code and toolkit are public, and the misspecification experiment
directly tests the paper's central design choice.

**Limitations.** Author-stated (§6.4): evaluation is limited to synthetic and semi-synthetic data
because counterfactuals are unobserved; real A/B-test validation is future work. Reviewer
reading: the synthetic benchmarks are generated by mechanisms close to the training prior,
and on the one external semi-synthetic benchmark (ACIC 2016) CausalFM is far behind CausalPFN.
Margins elsewhere are small relative to the reported standard deviations. One model per
setting must be trained, and the IV prior assumes an additive confounder. Bayesian uncertainty
quantification is claimed as an advantage, but no calibration or interval-coverage results are
reported.

---

<a id="tabpfn-wide"></a>

## 2026-03 — Kolberg et al. — TabPFN-Wide

**Provenance.** arXiv preprint (journal-template manuscript, venue not stated) · arXiv
[2510.06162v2](https://arxiv.org/abs/2510.06162v2) (filed version, 29 March 2026) · University
of Tübingen (Institute for Bioinformatics and Medical Informatics; AutoML for Science) · training
code, package and weights on [GitHub](https://github.com/not-a-feature/TabPFN-Wide) · **PDF:**
[open](papers/2026/03_Kolberg_et_al._TabPFN_Wide_Continued_Pre_Training_for_Extreme_Feature_Counts.pdf)

**Citation key:** `2026.KOLBERG.tabpfnwidecontinuedpretrainingextremefeaturecounts`.

**Where it fits.** A continued-pretraining extension of TabPFN v2 ([Hollmann 2025, *Accurate
predictions on small data with a tabular foundation model*](#tabpfn-v2-nature)) for
high-dimensional, low-sample-size (HDLSS) data such as multi-omics, where v2's ~500-feature
pretraining range is far exceeded. It is a sibling of [Garg 2025, *Real-TabPFN*](#real-tabpfn)
in method (continue pretraining a released checkpoint) but not in data: TabPFN-Wide continues on
**synthetic** data only. It also shows that the open TabICL prior ([Qu 2025,
*TabICL*](#tabicl-2025)) can drive continued pretraining of a model trained on a different,
closed prior.

**What it contains.**

* **Feature-widening prior (Algorithms 1–2).** Because the TabPFN v2 prior is not public,
  each training dataset is first drawn from the open TabICL prior (40–400 rows, 50–350
  features, up to 10 classes) and then widened to a target width d. New continuous features
  are sparse random linear combinations of the existing ones plus feature-dependent Gaussian
  noise; new categorical features copy values from sparsely chosen existing categoricals, with
  cardinality capped by a sampled target. The sparsity p ∈ [0, 0.05] and noise σ ∈ [0, 1] are
  set to mimic the correlated, noisy structure of omics data (Appendix L); with probability 0.5
  the original features are appended, then all columns are shuffled.
* **Continued pretraining.** All parameters of the TabPFN v2 *classifier* are updated for
  10,000 AdamW steps (learning rate 1e-5) on 4 H100 GPUs. Separate models are trained for maximum
  widths of 1,500, 5,000 and 8,000 features ("TabPFN-Wide-1.5k/5k/8k"). Training is
  **synthetic-only**: a set of real omics and synthetic SNP datasets was used only to observe
  convergence, not for fine-tuning or checkpoint selection (Appendix J).
* **Attention as feature importance.** With v2's feature grouping and added features
  disabled so that each token is one feature, the feature-wise attention to the label column,
  averaged over samples, heads and layers, is read as an importance score.
* **Feature reduction is a baseline, not the method.** Agglomerative feature clustering is used
  only to compare models at reduced feature counts (Fig. 3, Appendix B). The method keeps every
  feature.

**Key results.**

* **Five TCGA multi-omics cancer-subtype datasets (14k–19k features; Fig. 2, Appendix D
  Table 3).** AUROC rises sharply over TabPFN v2, e.g. BRCA 0.733 → 0.971 and COAD 0.710 → 0.954
  for the 5k model. The margin over tuned classical baselines is small (BRCA: Random Forest and
  XGBoost 0.967, RealMLP 0.966). Training width beyond 1.5k matters little.
* **Feature-reduction sweep (Fig. 3).** TabPFN-Wide stays stable as features are added, whereas
  TabPFN v2 degrades.
* **No catastrophic forgetting (Fig. 4a).** On 21 TabArena classification tasks (≤10,000 rows,
  ≤500 features) TabPFN-Wide-5k tracks v2 closely (Spearman ρ = 0.9935).
* **HDLSS benchmark (15 datasets from Li et al.; Fig. 4c).** 92.0% pairwise AUROC win rate,
  versus 68.0% for Random Forest and 5.3% for TabICL; paired Wilcoxon p < 0.005 (Appendix H).
* **Synthetic SNP needle-in-a-haystack (Fig. 4b; up to 70,000 categorical features).**
  TabPFN-Wide and XGBoost degrade least as non-causal SNPs are added; TabICL falls towards
  chance.
* **Interpretability (subsection 3.4, Appendix F).** On synthetic signal-recovery tasks, attention-based
  Recall@k matches Random Forest impurity importance; the top-10 attended BRCA genes include
  nine with direct breast-cancer associations in the literature.

**Strengths.** A cheap, reusable recipe — widen an open prior and continue pretraining — that
extends a TFM's operating range without retraining from scratch or changing the architecture,
with an explicit forgetting check. Real omics, standard HDLSS and controlled synthetic
benchmarks are all used, ensembling is disabled for every neural model to show raw behaviour,
and code and weights are released.

**Limitations.** Author-stated ("Limitations and Outlook"): only the TabPFN v2 classifier was continued (no wide
regressor); the same recipe failed to train TabICL (Appendix I); the unchanged v2 attention
limits how far rows and features can grow; and attention-as-importance is reliable on
synthetic tasks but should be read with caution on real biomedical data. Reviewer reading: on
the omics datasets the gain is mainly over TabPFN v2 rather than over Random Forest, XGBoost or
RealMLP; no calibration analysis is reported; and the prior is tailored to omics-like
correlation structure, so transfer to other wide-data domains is untested. Not to be confused
with the `_large-features-*` checkpoints released with TabPFN-2.5 (Hugging Face model-card
material, see [Grinsztajn 2026, *TabPFN-2.5*](#tabpfn-25)).

---

<a id="engineering-regression-without"></a>

## 2026-03 — Regenwetter et al. — Engineering Regression Without Real-Data Training: Domain Adaptation for Tabular Foundation Models Using Multi-Dataset Embeddings

**Provenance.** arXiv preprint · [2603.04692v1](https://arxiv.org/abs/2603.04692v1),
filed version 5 March 2026 · MIT · DOI: 10.48550/arXiv.2603.04692 ·
**PDF:** [open](papers/2026/03_Regenwetter_et_al._Engineering_Regression_Without_Real_Data_Training_Domain_Adaptation_for_Tabular_Foundation_Models_Using_Multi_Dataset_Embeddings.pdf).
The paper does not identify released code or adapted weights.

**Citation key:** `2026.REGENWETTER.engineeringregressionrealdatatrainingdomainadaptationtabularfoundationmodelsusingmultidatasetembeddings`

**Where it fits.** A domain-targeted synthetic continued-pretraining study for
[TabPFN-2.5](#tabpfn-25). It contrasts with [Real-TabPFN](#real-tabpfn), which updates
weights using real tables, and complements [O'Prior](#oprior), which compares synthetic
prior families under controlled conditions. Unlike TabPFN-Wide's classification focus,
this study targets engineering regression.

**What it contains.** TREDBench collects 83 regression datasets, 35 labelled engineering
and 48 non-engineering. TabPFN 2.5 row representations are averaged into 192-dimensional
dataset embeddings. An XGBoost classifier trained on embeddings from real engineering
datasets and synthetic tasks scores candidate tasks; the 200 most engineering-like of
9,750 candidates are selected from 10,000 generated tasks. TabPFN 2.5 is then continued
pretrained for five epochs on the selected synthetic tasks. **Real engineering data guide
selection**, even though real samples do not directly update the model weights (§§3–4).
The paper describes held-out engineering datasets excluded from selection and evaluates
across 35 engineering datasets with context-size sweeps and cross-validation (§4.2).

**Key results.** An embedding-space classifier distinguishes engineering from non-engineering
datasets with 65.8% accuracy and synthetic from engineering datasets with 96.8%; the latter
falls to 88.9% for the selected synthetic tasks (§3.5, Fig. 4). On the paper's 70/30
train/test comparison, the adapted model has lower test error on 29/35 datasets than base
TabPFN 2.5 and 27/35 than AutoGluon (Table 1). The reported mean multiplicative
data-efficiency gains are 1.75× and 4.44× respectively (§4.3); these are estimated from
learning curves and may involve extrapolation when a target is not reached (§4.2).

**Strengths.** Uses a direct base-model comparator and separates synthetic weight updates
from the real-data signal used for task selection. Dataset-level embeddings offer a concrete
way to investigate and target a synthetic-to-real gap in regression.

**Limitations.** The authors report losses on 6/35 datasets against the base and 8/35
against AutoGluon, sometimes substantial (§4.3); improvements are not universal. Reviewer
reading: the preprint studies one backbone, one domain and a limited baseline set, with no
explicit equal-budget random-synthetic continued-pretraining control in the reported
comparisons, so the added value of the selection step versus continued training alone is
not isolated. The paper's description of dataset-level and row-level splitting is terse;
verify its implementation and overlap controls before treating the reported gains as a
general estimate. No calibration or predictive-distribution comparison is reported.

---

<a id="tanna-finetuning"></a>

## 2026-04 — Tanna et al. — Exploring Fine-Tuning for Tabular Foundation Models

**Provenance.** ACM Web Conference 2026 (WWW '26, Dubai), four-page short paper; the filed PDF
is the ACM proceedings version (no arXiv stamp) · DOI
[10.1145/3774904.3792923](https://doi.org/10.1145/3774904.3792923) · Lexsi Labs (Mumbai, Paris,
London) · experiment code announced for the TabTune repository ("will be available") ·
**PDF:** [open](papers/2026/04_Tanna_et_al._Exploring_Fine_Tuning_for_Tabular_Foundation_Models.pdf)

**Citation key:** `2026.TANNA.exploringfinetuningtabularfoundationmodels`.

**Where it fits.** An empirical study of when post-pretraining adaptation pays, by the Lexsi Labs
group that maintains the harness it runs on ([Tanna 2025,
*TabTune*](#2025-12--tanna-et-al--tabtune)). It widens [Rubachev 2025, *On Finetuning Tabular
Foundation Models*](#on-finetuning) to six TFMs, four strategies and three suites, and adds
calibration and fairness. Its companion [Tanna 2026, *Data Presentation Over
Architecture*](#tanna-resampling) varies the context instead of the weights; [Ning 2026,
*Test-Time Compute for Tabular Foundation Models*](#test-time-compute) later separates the
adaptation mechanisms under control.

**What it contains.** Six TFMs — TabPFN, TabICL, OrionMSP, OrionBiX, TabDPT and Mitra — run
through TabTune, against XGBoost, LightGBM, CatBoost and Random Forest run through AutoGluon
(their tuning budget is not described) (§2). Four adaptation strategies:

* **Zero-shot**: frozen weights, plain in-context learning.
* **Meta-learning**: episodic fine-tuning with 48–512 support samples for 5 epochs.
* **Supervised fine-tuning (SFT)**: full-parameter AdamW, learning rate 1e-5 to 5e-5, early
  stopping within 10 epochs.
* **PEFT**: LoRA (r = 8, α = 16) on top of both meta-learning and SFT. It is "not supported for
  some models"; TabPFN has no PEFT rows.

Results are reported on the common subset every model could run: TALENT (155 of 181 datasets),
OpenML-CC18 (63 of 72) and TabZilla (27 of 36), plus nine datasets with demographic attributes
for fairness (Adult, COMPAS, German Credit, Taiwan credit default, HMDA and others). Metrics are
accuracy, weighted F1 and mean rank; ECE, MCE and Brier score; and SPD, EOD and EOpD. Table 2
breaks accuracy down by size (<1K, 1K–10K, >10K rows), class balance and width (<10, 10–100,
>100 features). Classification only.

**Key results.**

* **Zero-shot is hard to beat (Table 1).** OrionMSP has the best aggregate rank (3.76), then
  TabPFN (4.44) and TabICL (4.78); the four tree baselines rank 6.16–7.06. TALENT accuracy:
  TabPFN 0.851, TabICL 0.847, XGBoost 0.840.
* **Full SFT hurts most models (Table 1).** TabPFN is the exception (TALENT 0.846 vs 0.851
  zero-shot; best SFT rank 1.97). TabICL falls to 0.767 on TALENT and from 0.873 to 0.567 on
  TabZilla; OrionBiX falls to 0.770 and 0.648.
* **Meta-learning gives small, model-specific gains.** TabPFN reaches 0.884 on OpenML-CC18
  (zero-shot 0.871); TabICL drops to 0.696 on TabZilla.
* **Regimes (Table 2).** Small datasets favour zero-shot. On medium datasets TabPFN gains with
  meta-learning (0.856 → 0.864); on wide datasets TabPFN SFT reaches 0.935 vs 0.913 zero-shot.
* **Calibration (Table 3).** Zero-shot is best calibrated. SFT raises TALENT ECE for TabICL from
  0.022 to 0.077, while TabPFN barely moves (0.0276 → 0.0287).
* **Fairness (Table 4).** Mitra has the lowest disparities at much lower accuracy. SFT's large
  fairness swings for TabICL and OrionBiX coincide with accuracy collapse (TabICL 0.874 → 0.458
  on the fairness suite).

**Strengths.** A joint accuracy, calibration and fairness view of adaptation, which shows that an
accuracy-neutral update can still degrade calibration. The per-regime breakdown turns the
results into usable guidance (zero-shot below 1K rows; SFT only for update-tolerant models such
as TabPFN), and restricting every table to a common dataset subset keeps comparisons paired.

**Limitations.** *Author-stated:* classification only; PEFT unavailable for some models;
sensitive attributes chosen by hand per dataset. *Reviewer reading:* the recipes are barely tuned
(one LoRA configuration, at most 10 epochs, no learning-rate search), so "SFT hurts" may describe
the recipe rather than the method. Mitra's zero-shot accuracy (0.39 on TALENT, 0.36 on CC18) is
far below every baseline, which points to an integration failure the paper does not discuss.
Table 3's PEFT blocks repeat the non-PEFT meta-learning and SFT values exactly, and Table 4's
TabPFN SFT row equals its meta-learning row. Some narrative claims are not visible in Table 2:
on imbalanced datasets meta-learning *lowers* accuracy for TabPFN (0.881 → 0.878), TabICL,
OrionMSP, OrionBiX and TabDPT, and OrionMSP's claimed medium-size gain is a drop (0.849 →
0.841). No seeds or variances are reported. The authors' own OrionMSP tops the zero-shot
ranking, and continued pretraining is not compared.

---

<a id="orion-bix"></a>

## 2026-04 — Bouadi et al. — Orion-BiX

**Provenance.** ACM Web Conference 2026 (WWW '26, Dubai), four-page short paper; the filed PDF
is the ACM proceedings version (no arXiv stamp) · DOI
[10.1145/3774904.3792937](https://doi.org/10.1145/3774904.3792937) · Lexsi Labs (Paris, Mumbai,
London) · code and checkpoint at [Lexsi-Labs/Orion-BiX](https://github.com/Lexsi-Labs/Orion-BiX)
(scikit-learn interface) · **PDF:**
[open](papers/2026/04_Bouadi_et_al._Orion_Bix_Bi_Axial_Attention_for_Tabular_In_Context_Learning.pdf)

**Citation key:** `2026.BOUADI.orionbixbiaxialattentiontabularincontextlearning`.

**Where it fits.** The second Lexsi Labs architecture after [Bouadi 2025,
*Orion-MSP*](#2025-11--bouadi-et-al--orion-msp). Both modify [Qu 2025, *TabICL*](#tabicl-2025)
and are evaluated in the same group's adaptation study ([Tanna 2026, *Exploring Fine-Tuning for
Tabular Foundation Models*](#tanna-finetuning)). Where Orion-MSP changes the row encoder for
scale, Orion-BiX changes it for multi-scale feature structure and adds episodic training aimed at
few-shot use.

**What it contains.** TabICL's SetTransformer column embedder and its label-aware in-context
learner (split attention mask; hierarchical classification for more than C_max classes) are kept
unchanged. Two things change (§2):

* **Biaxial row encoder** (§2.3). TabICL's single row transformer is replaced by stacked
  blocks, each applying four attentions over the feature axis in sequence: standard full
  self-attention; grouped attention within G local feature groups; hierarchical cross-attention
  between two halves of the feature set; and a second full ("relational") self-attention.
  N_CLS learnable CLS tokens attend to the result, and their concatenation is the row
  representation ("multi-CLS"), avoiding a single-vector bottleneck.
* **Episodic meta-training** (§2.5). Synthetic tables from a TabICL-like prior are cut into
  many support/query episodes, with random or kNN-based support selection, so pretraining
  matches the few-shot inference objective.

Inference adds automatic preprocessing (type detection, imputation, optional power, quantile or
robust scaling, outlier clipping) and an ensemble over normalisation × feature-permutation
views (§2.6). Parameter count, prior settings and training budget are not reported.

**Key results.**

* **Domain suites (Table 1).** On Medical and Finance subsets drawn from TALENT and OpenML-CC18
  (dataset counts not reported; the caption also names an Energy domain that is not shown),
  Orion-BiX has the best mean rank: Medical 4.10 (TabPFN 5.04, LightGBM 5.32, TabICL 5.54) and
  Finance 5.39 (CatBoost 5.82, TabICL 6.60). TabPFN has higher Medical accuracy (0.798 vs
  0.789); on Finance Orion-BiX leads (0.821 vs TabICL 0.813).
* **Few-shot (§3.3, Fig. 1).** With k = 5–128 support rows, it beats TabICL, TabPFN and TabDPT
  by 2–4 points for k ≤ 32. On OpenML-CC18 TabPFN overtakes it at k = 128.
* **Support selection (§3.4, Fig. 2).** At k = 32, uniform sampling beats kNN-based "diverse"
  selection by 3–5 points; Orion-BiX beats TabICL under both.

**Strengths.** A cleanly scoped change to an open model, released with code and weights. The
few-shot experiment tests the regime the episodic training targets, and the support-selection
result is reported even though it cuts against the kNN option the method offers.

**Limitations.** No ablation separates the four attention types, multi-CLS pooling and episodic
training, so the gains the authors attribute to biaxial attention are not isolated. The domain
results rest on hand-grouped subsets of unreported size, and the few-shot results are only
plotted. No regression, calibration or runtime results. Mitra scores 0.39 Medical accuracy in
Table 1, the same anomaly seen in the group's adaptation study, which questions the shared
harness. In that study's broader zero-shot ranking ([Tanna 2026](#tanna-finetuning), Table 1)
Orion-BiX (5.27) ranks behind OrionMSP, TabPFN and TabICL. Evaluated by its own authors.

---

<a id="kumorfm-2-scaling"></a>

## 2026-04 — Hudovernik et al. — KumoRFM-2: Scaling Foundation Models for Relational Learning

**Provenance.** Vendor technical report, arXiv preprint (not peer reviewed) · arXiv
[2604.12596v1](https://arxiv.org/abs/2604.12596v1) (filed version, 14 April 2026) · Kumo.ai
(Leskovec, Fey and colleagues) · closed model: no weights, size or pretraining corpus released;
access through the `kumoai` SDK and a hosted endpoint, fine-tuning only in enterprise
deployments; the linked benchmark-script repository was not found on 2026-10-26 ·
**PDF:** [open](papers/2026/04_Hudovernik_et_al._KumoRFM_2_Scaling_Foundation_Models_for_Relational_Learning.pdf)

**Citation key:** `2026.HUDOVERNIK.kumorfm2scalingfoundationmodelsrelationallearning`.

**Where it fits.** The first *relational* foundation model (RFM) in this collection by date: it
carries in-context learning over labelled examples from single tables to whole databases of
tables linked by primary–foreign keys, as a commercial system rather than an open model. It
answers [Klein and Hoffart 2026, *Position: Foundation Models for Tabular Data within Systemic
Contexts Need Grounding*](#klein-grounding) on the relational-data layer only — multi-table
structure and time, not the code, rules and world knowledge that paper also asks for. Its
central argument targets the flattening route that Prior Labs later takes: propositionalising a
database into one wide table for a TFM such as [Grinsztajn 2026, *TabPFN-2.5*](#tabpfn-25) or
[Qu 2026, *TabICLv2*](#tabiclv2). Its rel-f1 evaluation regime and undocumented per-task
configurations are disputed by [Hayler 2026, *Advancing Open and Reproducible Relational
Learning*](#advancing-open-and).

**What it contains.** A relational database is treated as a temporal heterogeneous graph
(rows are nodes, key links are edges, every node carries a timestamp). A prediction task
is a set of (entity, anchor time, label) context examples and the model predicts from
time-consistent subgraphs around each entity (§2). Tasks are declared in Kumo's Predictive
Query Language (PQL); context labels are generated automatically by "replaying" earlier
database states, which is how the system avoids hand-built task tables while preventing
temporal leakage. Versus KumoRFM-1, the architecture (§3, Fig. 3) is **hierarchical**: a
lightweight network builds **task-conditioned** row embeddings with alternating column
and row attention (context targets are injected into the input tables early), and a
larger network then applies **foreign-key graph attention and cross-sample attention**
over the context. Pretraining mixes SCM-generated synthetic tables/graphs with public
relational databases, staged from single tables to multi-table structures; context
selection mixes the entity's own lagged targets with recent global context; ensembling
shuffles columns, classes and hop counts. A constructed example (Fig. 4) — label positive
iff two child-table features co-occur *in the same related row* — gives AUROC 0.5 for any
model on column-wise deep-feature-synthesis encoders and 1.0 for KumoRFM-2; this is the
paper's **expressivity argument against flattening**.

**Key results.** Evaluation (§4) covers **41 tasks on 15 databases** (RelBenchV1, RelBenchV2,
SAP SALT, 4DBInfer), none used in pretraining, with at most **10k context examples** — as little
as 0.2% of the available training rows — and two-hop subgraphs. The abstract summarises this
as outperforming supervised and foundation-model approaches by up to 8%.

* **RelBenchV1 classification (12 tasks, Table 3).** **79.60 AUROC** (rank 3.08) against RelGNN
  78.06, KumoRFM-1 76.71, RDBLearn 75.97 and data-scientist features + LightGBM 75.62;
  TabPFN-2.5 on entity-table features alone scores 61.63. The largest wins are on
  small-training-set databases (rel-f1, avito, event, trial); supervised relational models keep
  an edge on amazon, stack and hm.
* **Other suites.** RelBenchV2 classification 79.96 (Table 4); 4DBInfer 79.96 against HGT 79.94
  (Table 5); SALT multi-class tasks (up to 589 classes) **0.83 MRR** against KumoRFM-1 0.80,
  DS+CARTE 0.79, DS+AutoGluon 0.77 and DS+TabICLv2 0.71 (Table 6); RelBenchV1 regression
  normalised MAE 0.822 against RelGNN 0.861 (Table 7).
* **Robustness (§4.4, Figs. 6–7).** Accuracy saturates at about four hops on SALT; the best
  neighbourhood size is task-dependent; degradation under injected missingness is slower than
  for XGBoost and TabICLv2; accuracy stays nearly flat with up to 160 added noise columns, where
  KumoRFM-1 declines.
* **Fine-tuning (§4.5, Table 9).** SALT MRR rises from 0.83 to **0.89**, in under two minutes per
  task.

**Strengths.** Takes relational and temporal structure seriously instead of flattening it
away, and gives a concrete, checkable expressivity counterexample to column-wise
aggregation. The evaluation is broad (four suites, binary, multi-class and regression),
includes both data-scientist feature pipelines and TFM-on-flattened-table baselines, and
reports robustness to scarce links, missing features and noise — the cold-start and dirty-
data regimes in which single-table TFMs are weakest. The automatic, leakage-aware context
generation from historical database states is the operationally important idea.

**Limitations.** A vendor report: model, weights, parameter count, pretraining corpus and
synthetic generator are undisclosed, and the linked benchmark-script repository
(`kumo-ai/kumo-rfm`) was not found on 2026-10-26, so no official code snapshot is kept here.
Many baselines are copied from publications rather than re-run, so tuning budgets and data
states differ across rows. Hayler 2026 notes that the per-task configurations released with
the benchmark scripts span a 384-combination grid with no account of how they were chosen, and
that KumoRFM-2's rel-f1 evaluation exposes database state beyond RelBench's fixed test cut-off
— a valid but non-comparable regime worth over ten AUROC points on that database's two
classification tasks, where KumoRFM-2 has some of its largest margins. *Reviewer inference, not a re-run:* removing a gain
of that size from the two rel-f1 tasks would cost the 12-task average about 1.7 AUROC points,
more than the 1.54-point lead over RelGNN. The fine-tuning gain is shown on SALT only.

---

<a id="tanna-resampling"></a>

## 2026-05 — Tanna et al. — Data Presentation Over Architecture

**Provenance.** arXiv preprint · arXiv [2605.18635v1](https://arxiv.org/abs/2605.18635v1)
(filed version, 18 May 2026) · Lexsi Labs · no code link in the paper (experiments run through
the group's TabTune library) · **PDF:**
[open](papers/2026/05_Tanna_et_al._Data_Presentation_Over_Architecture_Resampling_Strategies_for_Credit_Risk_Prediction_with_Tabular_Foundation_Models.pdf)

**Citation key:**
`2026.TANNA.datapresentationarchitectureresamplingstrategiescreditriskpredictiontabularfoundationmodels`.

**Where it fits.** A credit-default study by the Lexsi Labs group behind TabTune and the Orion
models. It complements their weight-adaptation study ([Tanna 2026, *Exploring Fine-Tuning for
Tabular Foundation Models*](#tanna-finetuning)) by varying what goes into the context instead,
and parallels [Purucker 2026, *Beyond IID*](#beyond-iid): there the split protocol reorders
rankings, here context construction does. [Baesens 2026, *Foundation Models for Credit Risk
Prediction*](#credit-risk-benchmark) is the broader credit benchmark.

**What it contains.** Because a TFM conditions on a bounded context rather than the full training
set, the context's class composition is a free design choice; under an ~8% default rate a
uniformly sampled context is mostly non-defaults. The study crosses (§4):

* **Data.** Home Credit (~307K applications, 120+ features from a seven-table schema, ~8%
  defaults, random split; ~246K training rows) and Lending Club (~533K loans, 70+ features,
  12–22% defaults, temporal split: train to June 2019, test H2 2019). Both pass through a
  three-stage pipeline: sentinel imputation for informative missingness, 50+ engineered
  features, and correlation → mutual-information → VIF → SHAP feature selection.
* **Models.** Five TFMs via TabTune (TabPFN v2.5, TabICL, OrionMSP v1.0 and v1.5, OrionBiX)
  and four classical models (Random Forest, XGBoost, LightGBM, CatBoost) trained on the full
  data with default hyperparameters, no class weighting and no threshold tuning.
* **Seven context strategies** in three families: baseline (Uniform, Stratified), class-balance
  (Balanced, Oversample+, SMOTE) and informed (Diversity-KM via MiniBatch k-means; Hybrid =
  Balanced plus Diversity-KM), at six context sizes from 1,024 to 50,000 rows.
* **Metrics.** ROC-AUC (primary), default-class recall, MCC, default-class F1 and balanced
  accuracy.

**Key results.**

* **Strategy versus model (§5.2, Table 2).** Averaged over TFMs and context sizes, the best
  class-aware strategy beats Uniform by ~3 AUC points on Home Credit (Balanced 0.734 vs 0.703)
  but ~1 point on Lending Club (Hybrid 0.686 vs 0.673) — less than the abstract's "3 to 4
  points" on both. The authors report that the best–worst strategy gap (~0.03–0.05) exceeds the
  inter-TFM gap within a strategy. Diversity-KM is worst on both datasets.
* **Crossover (§5.3).** On Home Credit, TabPFN and TabICL pass the best classical model (Random
  Forest, 0.739) with 5K–10K context rows; at 50K Balanced, TabPFN reaches 0.786 (Table 3). On
  Lending Club most TFMs never reach XGBoost (0.718); the best at 50K is TabPFN at 0.703.
* **Recall (§5.4, Tables 1 and 3).** At the 0.5 threshold three of four classical models predict
  no defaults on Home Credit. At 50K Balanced context all five TFMs reach MCC 0.19–0.26 and
  default-class F1 0.24–0.31; under Uniform sampling the TFMs are also at MCC ≈ 0.

**Strengths.** Isolates a cheap deployment lever that model comparisons ignore, with the
direction confirmed on two structurally different datasets. The authors state the key caveat
themselves: the recall gap is an operating-point effect that `scale_pos_weight` would remove for
GBDTs, and the Uniform-context TFMs fail the same way.

**Limitations.** *Author-stated (§6.3):* preprocessing is not competition-grade (top Home
Credit solutions reach ~0.80 AUC using all seven tables); strategies are heuristic; two consumer
credit datasets only. *Reviewer reading:* the classical models are untuned and unweighted, so
the recall comparison shows a threshold choice rather than a GBDT failure. "Explains more
variance" is asserted from averages, with no variance decomposition or per-model table across
strategies, and the Lending Club effect is small. A balanced context shifts the model's implied
base rate, so predicted probabilities are no longer calibrated to the true default rate — a
material issue for probability-of-default use that the paper does not measure. No seeds or
intervals, and the compared TFMs include the authors' own.

---

<a id="tabdpt-turbo"></a>

## 2026-05 — Hosseinzadeh et al. — TabDPT-Turbo

**Provenance.** Workshop paper, 2nd ICML Workshop on Foundation Models for Structured Data
(Seoul, 2026), [OpenReview](https://openreview.net/forum?id=Y00pwFyrHR); Zotero also records
arXiv DOI [10.48550/arXiv.2608.01400](https://doi.org/10.48550/arXiv.2608.01400), but the filed
PDF is the workshop version (no arXiv stamp) · Layer 6 AI, Toronto (one author now at Cohere) ·
open weights and code released as TabDPT v1.2 in
[layer6ai-labs/TabDPT-inference](https://github.com/layer6ai-labs/TabDPT-inference) · **PDF:**
[open](papers/2026/05_Hosseinzadeh_et_al._TabDPT_Turbo_Efficient_In_Context_Learning_for_Tabular_Prediction.pdf)

**Citation key:** `2026.HOSSEINZADEH.tabdptturboefficientincontextlearningtabularprediction`.

**Where it fits.** The retrieval line revising itself. The same lab introduced retrieval-based
contexts ([Thomas 2024, *LoCalPFN*](#localpfn)) and shipped kNN retrieval in [Ma 2026,
*TabDPT*](#tabdpt); here it removes retrieval in favour of **long-context pretraining**, citing
[Shaheen 2026, *Understanding the Surprising Generalization Properties of Tabular Foundation
Models*](#shaheen-retrieval) for the view that attention already behaves like
nearest-neighbour retrieval. It also declines the column-embed → row-compress design of
[Grinsztajn 2026, *TabPFN-3*](#tabpfn-3) and [Qu 2026, *TabICLv2*](#tabiclv2) and stays
**row-based** (one token per row), on the grounds that row tokens make long contexts cheaper and
easier to batch.

**What it contains.** TabDPT's real-data self-supervised objective (a random column becomes the
target) is kept, with four groups of changes (§3):

* **Corpus.** All active OpenML datasets, filtered (10–200 columns, ≤300 MB, categorical
  cardinality ≤100) and deduplicated against CC18, CTR23 and — new in this version — TabArena,
  plus an order-invariant duplicate check: **1,445 datasets**, 309.9M rows, 5.6B cells, against
  112 datasets and 0.87B cells for TabDPT v1.1 (Appendix Table 2; the 2.86×–12.90× ratios there
  are corpus-size ratios, not speedups).
* **Architecture.** Rows zero-padded to 128 features and linearly encoded; a 32-layer pre-norm
  transformer (width 512, 8 heads, SwiGLU); 64 learned "thinking rows"; context targets routed
  through a per-layer MLP into the attention *values* rather than added to row embeddings;
  QK-normalisation, a sigmoid attention gate and attention-temperature scaling with context
  length. Up to 16 classes natively, more by TabDPT's digit decomposition.
* **Losses.** Regression as a 2,048-bin distribution over [−10, 10] standardised units trained
  with CRPS (a proper scoring rule), plus a z-loss and an auxiliary context-row prediction loss.
* **Retrieval-free long context.** Training contexts up to 32k rows; inference uses one shared
  sequence of all context rows followed by all queries, tested up to 100k context rows.

**Key results.**

* **Speed (Table 1).** Same-hardware TabArena-Lite rerun (1×H100, 96 vCPUs, 8 ensemble members):
  fit + predict ≈0.63 s per 1K rows versus ≈1.51 s for TabPFN-3 (≈2.4×) and ≈8.2 s for
  TabICLv2 (≈13×); TabICLv2 fits marginally faster (0.41 vs 0.44 s) but predicts far slower
  (7.75 vs 0.19 s).
* **Quality (Fig. 4).** Fourth on TabArena-Lite default Elo, behind TabPFN-2.6, TabICLv2 and
  RealTabPFN-2.5 and ahead of CatBoost, Mitra, TabDPT v1.1, TabICL and TabPFN v2. Against
  TabDPT v1.1 on CC18 and CTR23 (Fig. 1) it is reported as comparable (abstract) or better
  (introduction) in AUC and R², at a fraction of the wall time.
* **Retrieval ablation (§4.2, Fig. 2).** Full context beats retrieval at every neighbour count
  except K = 8,192, where the difference is small; retrieval is at least 100× slower, and
  K = 8,192 nearly 1,000×.
* **Scaling (Appendix A.4).** Training on 16,384-row rather than 1,024-row contexts, and doubling
  depth, both improve validation loss.

**Code-dump note (not the paper).** The README in `TabDPT.txt` announces v1.2 ("TabDPT-Turbo")
on 17 June 2026 with "~120x" average speed-up on TabArena, and a later v1.3 with further
training-recipe changes, so the snapshot no longer corresponds exactly to the paper's model.

**Strengths.** An honest efficiency paper: it claims near-peak quality at much lower cost, not
state of the art. The timing comparison is rerun on shared hardware, the retrieval ablation
tests the lab's own earlier design, the corpus is deduplicated against TabArena, and weights and
code are open.

**Limitations.** A four-page workshop paper: quality results are mostly figures without
per-benchmark tables or intervals, and the TabArena-Lite Elo mixes the authors' runs with
repository scores from other hardware (TabPFN-3 is absent from the Elo plot). No calibration
metrics despite the CRPS head. None of the changes (corpus scale, value routing, thinking rows,
CRPS head) is ablated individually, so the gains cannot be attributed. The row encoder is not
column-order invariant, wider tables need PCA or column subsampling beyond 128 features, and the
corpus is OpenML-derived, so contamination control rests on the deduplication heuristics.
TabDPT v1.1's 112-dataset corpus differs from the 123 datasets in the original TabDPT paper, a
version difference rather than an inconsistency.

---

<a id="tabpfn-3"></a>

## 2026-05 — Grinsztajn et al. — TabPFN-3 (Technical Report)

**Provenance.** Vendor technical report (Prior Labs Team), arXiv preprint · arXiv
[2605.13986v2](https://arxiv.org/abs/2605.13986v2) (filed version, 28 May 2026; report dated
12 May 2026) · Prior Labs · open weights under the TABPFN-3.0 License v1.0 (research and
internal evaluation only; no commercial or production use); TabPFN-3-Plus and its Thinking mode
only via API/enterprise licence · **PDF:**
[open](papers/2026/05_Grinsztajn_et_al._TabPFN_3_Technical_Report.pdf)

**Citation key:** `2026.GRINSZTAJN.tabpfn3technicalreport`.

**Where it fits.** Prior Labs' generation after [Grinsztajn 2026, *TabPFN-2.5*](#tabpfn-25) and
the undocumented v2.6, and an architectural reset rather than another continued-pretraining
variant. It abandons the TabPFN-2.x alternating row/feature attention for the row-compression
design of [Qu 2026, *TabICLv2*](#tabiclv2), scales in-context learning to **one million training
rows on a single H100**, adds a many-class decoder and introduces a test-time-compute "Thinking"
mode. Its successor is [Jäger 2026, *TabPFN-3.5*](#tabpfn-3-5); the relational extension is
documented in [Hayler 2026, *Advancing Open and Reproducible Relational
Learning*](#advancing-open-and).

**What it contains.** Architecture (§2.1, Fig. 5):

* **Input.** Features are grouped into triplets with each feature's two cyclically shifted
  neighbours (TabICLv2's assignment), linearly embedded, with target-aware embeddings added for
  training rows and a NaN/Inf indicator concatenated to each cell (native missing values).
* **Stage 1, column-wise.** Each feature column is embedded by a transformer with
  inducing-point attention, capturing column statistics without quadratic cross-row cost.
* **Stage 2, row-wise.** Learned `cls` tokens attend over a row's feature embeddings; their
  concatenation is one fixed-size row vector, decoupling later stages from the feature count.
* **Stage 3, in-context learning.** A TabPFN-v1-style transformer over row vectors: training
  rows attend to each other, test rows to training rows. Stages 1 and 3 use TabICLv2's
  query-aware scalable softmax (QASSMax) for length generalisation; normalisation is RMSNorm.
* **Many-class decoder (§2.2).** The MLP head is replaced by attention-based retrieval: class
  probabilities are an attention-weighted average of in-context one-hot labels, so the decoder is
  class-permutation-equivariant and non-parametric in the class count. The revision credits
  earlier target-equivariant and localisation work (Arbel et al., Koshil et al.). The trained
  checkpoint still fixes a ceiling of 160 classes.
* **Inference engineering (§2.4).** Row-chunking precomputes the inducing-vector summary once and
  streams rows in chunks, with outputs equivalent to unchunked computation; multi-query attention
  for test rows cuts the KV cache to about 7 GiB per estimator at 1M rows; cached prediction is
  one to three orders of magnitude faster than fit+predict; optional distillation to MLPs/trees,
  `torch.compile` and FlashAttention-3.
* **Prior (§2.5).** Synthetic SCM prior only, extended with new graph samplers and combiner
  mechanisms, richer categoricals, high-frequency and spatial activations, a many-class prior, a
  temporal (dynamic SCM) prior and out-of-distribution/extrapolation tasks; more than 8 trillion
  training tokens. Not released.
* **TabPFN-3-Plus (§2.6).** API-only variant with native text columns; "Thinking" adds
  undisclosed inference-time computation using only TabPFN (no LLMs, real data or retrieval).

**Key results.**

* **TabArena, 51 datasets (§3.1.1, Fig. 10).** One forward pass of TabPFN-3 beats every other
  model including tuned-and-ensembled ones, +72 Elo over tuned+ensembled Real-TabPFN-2.5;
  significantly better than Real-TabPFN-2.5 per dataset (Wilcoxon p < 0.0001, Fig. 4b). Plus
  (Thinking) beats every non-TabPFN model by over 200 Elo and AutoGluon 1.5 extreme (4 h) by over
  100 Elo at about a tenth of its runtime. The TabPFN-3 family dominates the time/accuracy Pareto
  front (Fig. 11).
* **15 largest TabArena datasets, 10k–100k rows (Fig. 1).** TabPFN-3 leads by 100 Elo; Plus
  (Thinking) by over 420 Elo against non-TabPFN models and 220 over AutoGluon 1.5 extreme.
* **TALENT, 274 datasets (Fig. 13).** First in mean rank overall and per task type.
* **Large data (§3.2.1, Figs. 15–16).** On an internal benchmark of 13 datasets with
  100k–1M rows and up to 200 features (regression with temporal splits), TabPFN-3 beats default
  and 8-hour-tuned GBDTs and TabICLv2 in one forward pass and scales smoothly to 1M rows.
* **Many classes (§3.2.2, Fig. 17).** On a synthetic benchmark of up to 100 classes built by
  binning TabArena regression targets: normalised ROC-AUC 1.00 versus 0.89 for TabICLv2 and 0.83
  for TabPFN-2.5 with their wrappers.
* **Many features (§3.2.3, Fig. 18).** Six datasets with 102–322 rows and 1,117–22,215 features:
  best with 32 estimators; at equal estimator budget Real-TabPFN-2.5 can slightly win.
* **Other domains.** Quantile regression first by pinball loss (§3.2.4); TabPFN-TS-3 second to
  Chronos-2 on fev-bench (43.1 SQL skill; §3.3, Table 1); on RelBenchV1 the TabPFN-REL
  pipeline is the best *foundation* model while supervised RelGNN stays best overall, using early
  checkpoints (§3.4, Fig. 21); TabSTAR text tables led by Plus (§3.1.3).
* **Speed.** Up to 20× faster than TabPFN-2.5 (abstract); SHAP via `shapiq` over 120× faster
  with KV caching (§2.4.5).

**Code-dump note (not the paper).** In `TabPFN .txt` the regressor's bar-distribution borders
are stored differently by generation: up to v2.6 as `criterion.*` state beside the model, from
v3 as a `regression_borders` buffer on the model. The loader keeps `criterion.*` out of the
model state and `_resolve_regression_borders` prefers saved borders, falling back to the buffer,
so writing `criterion.*` round-trips for both. Checkpoints are the standard `torch.save` dict
(`state_dict`, `config`, `architecture_name`, `inference_config`), with `architecture_name` one
of `tabpfn_v2`, `tabpfn_v2_5`, `tabpfn_v2_6`, `tabpfn_v3`.

**Strengths.** A real scaling advance with an exact (not approximate) chunked inference path,
full predictive distributions from one head, and evaluation on public benchmarks (TabArena,
TALENT) beyond the vendor's internal suites. The synthetic-only prior removes real-data
contamination as an explanation of the public results. Honest about the cell-budget trade-off
of early feature compression.

**Limitations.** A vendor report without peer review and without ablations isolating the
architecture, prior and training changes. The prior and Thinking mode are undisclosed, and the
headline Thinking numbers come from an API-only model. Large-data, many-feature and quantile
results use internal or constructed benchmarks; the many-class benchmark is synthetic.
Author-stated: when rows and features are both large, early feature compression becomes a
bottleneck, and each estimator sees at most 200 features by default. The open licence bars
commercial and production use, including using outputs for internal commercial decisions (§5).

---

<a id="attention-benchmark"></a>

## 2026-05 — Schambach et al. — Benchmarking Attention for Tabular Foundation Models

**Provenance.** Workshop paper, Proceedings of the 2nd ICML Workshop on Foundation Models for
Structured Data (Seoul, 2026) · no arXiv version; [OpenReview](https://openreview.net/forum?id=rwtcugrpDq)
· SAP SE · benchmark code at
[SAP-samples/tabular-attention-benchmark](https://github.com/SAP-samples/tabular-attention-benchmark)
· **PDF:** [open](papers/2026/05_Schambach_et_al._Benchmarking_Attention_for_Tabular_Foundation_Models.pdf)

**Citation key:** `2026.SCHAMBACH.benchmarkingattentiontabularfoundationmodels`.

**Where it fits.** Measures the implementation cost beneath the architectural scaling arguments
of alternating-attention TFMs such as [Hollmann 2025, *Accurate predictions on small data with a
tabular foundation model*](#tabpfn-v2-nature). It complements [Hosseinzadeh 2026,
*TabDPT-Turbo*](#tabdpt-turbo) and [Grinsztajn 2026, *TabPFN-3*](#tabpfn-3): a model can become
faster through the attention backend and memory layout as well as through a different
architecture. The authors note that the pattern studied applies to TabPFNv2-like models but not
directly to TabICL's staged design.

**What it contains.** In the paper's terminology, **column attention** attends across features
(sequence length C, contiguous in the usual row-first `(B, R, C, H, D)` layout) and **row
attention** across samples (sequence length R, needing a transposed view). PyTorch SDPA expects
`(…, H, L, D)`, so row attention needs a copy for each of queries, keys and values;
FlashAttention-3 accepts `(…, L, H, D)` strided views and avoids them (§2). The study times
forward and backward passes of five backends — SDPA efficient, SDPA cuDNN, FlashAttention-2, -3
and -4 — on one H100 NVL in bfloat16, non-causal, batch size 1, 12 heads of dimension 64. Column
attention varies C from 16 to 2,048 at R = 1,024; row attention varies R from 32 to 16,384 at
C = 64. Each point is 50 repetitions after warm-up, with wrappers validated against PyTorch's
math attention (§3). Other head counts and dimensions are in the appendix.

**Key results (§4, Fig. 1).**

* **Column attention.** Efficient SDPA wins the shortest sequences (over 2× FA3 for C = 16–64,
  small in absolute terms); from C = 128 to 2,048 cuDNN dominates at 2.5–3× the efficient-SDPA
  baseline and about 1.5× FA3. FA2 underperforms on Hopper.
* **Row attention.** FA3 dominates above R = 128, up to 3.5× the efficient-SDPA baseline and
  about 1.5× cuDNN, mainly by avoiding the copies; the relative advantage shrinks with longer
  sequences because copying is O(N) and attention O(N²).
* **FA4** cannot run head dimension 64 on Hopper (it needs 128).
* **Recommendation (H100, H = 12, D = 64).** cuDNN SDPA for column attention with C > 64,
  efficient SDPA for C ≤ 64; FA3 for row attention, with efficient SDPA as a fallback for
  R ≤ 128. The best–worst backend gap can exceed 3× for a given shape (§5).

**Strengths.** Separates kernel throughput from tensor-layout overhead, measures backward as well
as forward passes, and releases code with additional shape sweeps. Explains concretely why a
backend tuned for long causal language-model sequences need not win on tabular shapes.

**Limitations.** Hardware- and version-specific microbenchmarks, not whole-model training or
serving measurements. Author-stated: the batch-size-1 SDPA wrapper deliberately keeps copies that
are not strictly needed at B = 1, so speedups compare complete wrappers rather than kernels alone.
The crossover points depend on batch size and hidden dimension, and nothing here establishes the
same ranking on A100/B200, with causal masks, or for staged architectures.

---

<a id="beyond-iid"></a>

## 2026-06 — Purucker et al. — Beyond IID: How General Are Tabular Foundation Models, Really?

**Provenance.** arXiv preprint · arXiv [2606.30410v1](https://arxiv.org/abs/2606.30410v1) (filed
version, 29 June 2026) · TabArena team (Prior Labs, University of Freiburg, University of
Mannheim, INRIA Saclay, Technion, ELLIS Tübingen, Probabl) · benchmark integrated into TabArena
([code](https://tabarena.ai/code)); curation framework and data at
[TabArena/data-foundry](https://github.com/TabArena/data-foundry) · **PDF:**
[open](papers/2026/06_Purucker_et_al._Beyond_IID_How_General_Are_Tabular_Foundation_Models_Really.pdf)

**Citation key:** `2026.PURUCKER.iidhowgeneralaretabularfoundationmodelsreally`.

**Where it fits.** The most systematic test so far of whether TFM "generality" survives outside
the IID benchmark regime in which TFMs were developed. Co-authored by TabPFN developers, which
gives the negative findings weight. It is the evaluation axis later targeted by [Jäger 2026,
*TabPFN-3.5*](#tabpfn-3-5), whose prior was retuned for grouped, wide and high-cardinality data,
and it complements the temporal-shift concerns of [Helli 2024, *Drift-Resilient
TabPFN*](#drift-resilient-tabpfn).

**What it contains.** **BeyondArena**: 142 datasets hand-curated from 1,128 candidates with the
released **DataFoundry** framework and metadata schema (§4). Datasets span IID (103), temporal
(21) and grouped (18) tasks, 100 to 1M training rows, low/high dimensionality and text or
high-cardinality features, organised into 12 sub-benchmarks. Eleven models are compared (§5):
three TFMs evaluated **only by in-context learning** (TabPFN-2.6, TabICLv2, TabDPT) against
default, tuned (25 random configurations) and tuned+post-hoc-ensembled CatBoost, LightGBM,
XGBoost, RealMLP, TabM, random forest, extra trees and linear models. Outer splits respect the
task (group-based CV; application-specific rolling temporal splits) and so do inner validation
splits. TabPFN-2.6 and TabDPT are run only up to 100k training rows; their larger-data results
are imputed with a default random forest. Text is embedded with Qwen3-Embedding-8B (32 dims);
metrics are ROC AUC, log-loss and RMSE, aggregated by Elo and Improvability. Cost about $50k.

**Key results.**

* **Where TFMs win (§6, Figs. 1, 4–5).** TFM in-context learning is best on tiny, small, IID and
  low-dimensional data, and best on average by Improvability and among default models.
* **Where they lose.** Tuned+ensembled RealMLP leads the temporal, grouped, medium, large,
  high-dimensional and text sub-benchmarks; tuned CatBoost leads high-cardinality data (Appendix
  E.5, Table E.4). The grouped ranking is uncertain: only 5.1% of pairwise comparisons survive
  Holm correction there.
* **Drivers (Table E.3).** The best-GBDT-over-best-TFM advantage grows with row count
  (Spearman ρ = +0.60) and number of high-cardinality categoricals (ρ = +0.47).
* **Peak performance (Fig. 6).** TFMs significantly beat all other models on 49% of datasets and
  tie the best non-TFM on a further 21% (70% in total); TabICLv2 ranks first on 19%, TabPFN-2.6
  on 10.5%. TFMs are clearly outperformed on 42 datasets.
* **Ablations (Table 1, Appendix F).** IID outer splits on two grouped datasets distort rankings
  (Kendall τ = 0.49 and 0.60); 5×5 inner CV beats 8-fold CV on small data; TabPFN-2.6 improves
  when the grouped-data preprocessing is disabled, so its grouped results are negatively biased;
  post-hoc calibration helps most models but worsens TabPFN-2.6 and RealMLP.
* **Cost.** TFM training cost stays far below tuned competitors, but inference cost is large.

**Strengths.** Application-appropriate outer and inner splits, Friedman/Holm-corrected Wilcoxon
testing, a released curation framework, explicit ablations of its own protocol choices, and
per-regime recommendations. BeyondArena-Core offers a cheaper split subset with more stable
per-dataset rankings than TabArena-Lite.

**Limitations.** Author-stated (§7): TFM fine-tuning and continued pretraining are not tested;
only 25 tuning configurations; only three open TFMs; unbalanced sub-benchmarks; validation and
preprocessing best practices for non-IID and text data remain open. Reviewer reading: the
temporal and grouped sub-benchmarks are small (21 and 18 datasets), sub-benchmarks overlap (a
large dataset may also be temporal), and imputing TabPFN-2.6/TabDPT beyond 100k rows with a
random forest affects the large-data comparison.

---

<a id="memory-efficient-tfms"></a>

## 2026-07 — Luo et al. — Memory Efficient Tabular Foundation Models

**Provenance.** Workshop paper, 2nd Foundation Models for Structured Data (FMSD) Workshop at
ICML 2026 · arXiv [2607.27546v1](https://arxiv.org/abs/2607.27546v1) (filed version, 30 July
2026) · Commonwealth Bank of Australia and Australian Institute for Machine Learning (University
of Adelaide) · no code release found in the paper · **PDF:**
[open](papers/2026/07_Luo_et_al._Memory_Efficient_Tabular_Foundation_Models.pdf)

**Citation key:** `2026.LUO.memoryefficienttabularfoundationmodels`.

**Where it fits.** The deployment-cost counterpart to [Hosseinzadeh 2026,
*TabDPT-Turbo*](#tabdpt-turbo), from an industry-practitioner perspective. Turbo redesigns the
model to cut inference cost; this paper compresses an existing model's weights after training
to cut storage and distribution cost. It is an open alternative to the proprietary distillation
engine of [Grinsztajn 2026, *TabPFN-2.5*](#tabpfn-25), but it addresses a different cost.

**What it contains.** Three post-training **INT4 weight-quantization** methods applied to
**TabPFN v2.5 and v2.6** (§3.1): **GPTQ** and **AWQ**, whose calibration procedures are adapted
by feeding the in-context `(x_train, y_train; x_test)` tuple as calibration input, and
**K-Means** codebook quantization with INT4 bit-packing. Evaluation uses 30 OpenML datasets
within TabPFN's limits, against default and tuned XGBoost, CatBoost, LightGBM, kNN and random
forest (§3.2). "Memory" in the headline is the size of the **BZIP2-compressed checkpoint file**,
mimicking a deployment pipeline. TabICL is discussed but not quantized.

**Key results.**

* **Compression versus accuracy (Table 1).** All three methods reach 6.06–7.65× smaller
  compressed checkpoints with an accuracy drop of at most 0.005. K-Means is best on both:
  TabPFN v2.5 goes from 40.95 MB to 5.36 MB (7.65×) at accuracy 0.871 versus 0.872; v2.6 reaches
  7.56×. Every quantized variant stays above the best classical baseline (tuned LightGBM, 0.864).
  The abstract's "up to 7.6×" and "nearly 87%" refer to this file-size reduction.
* **Bit width (Table 2, Fig. 3).** INT4 retains over 99% of baseline accuracy; 2-bit gives
  14–15× compression at about 90% accuracy recovery; 1-bit collapses.
* **Rankings (Fig. 2).** Quantized models lose little Elo relative to FP32 and still beat all
  classical baselines pairwise; per-dataset variance is unchanged (Appendix Table 3).
* **Inference cost (Appendix Table 4).** Inference memory stays at about 4.7 GB (<2% change) and
  runtime within ±10%, because weights are dequantized before inference and attention
  activations dominate.

**Strengths.** A practical, clearly scoped measurement that the literature lacked: known
compression methods applied to this model class, with the accuracy–size curve and the
inference-memory caveat reported explicitly.

**Limitations.** Author-stated (§5): post-training quantization only (no quantization-aware
training), a subset of methods, dequantization means no run-time memory saving, no kernel- or
hardware-level optimisation, and TabPFN's context limits remain. Reviewer reading: a short
workshop study on 30 accuracy-scored datasets; the headline ratio is a compressed-file ratio,
not a reduction in GPU memory; no calibration or log-loss analysis, although quantization may
perturb probabilities more than accuracy.

---

<a id="shaheen-retrieval"></a>

## 2026-08 — Shaheen et al. — Understanding the Surprising Generalization Properties of Tabular Foundation Models

**Provenance.** arXiv preprint · arXiv [2608.17957v1](https://arxiv.org/abs/2608.17957v1)
(filed version, 18 August 2026) · Polytechnique Montréal / Mila / Chandar Lab, University of
Toronto, **Layer 6 AI**, **Prior Labs** / ELLIS Institute Tübingen / University of Freiburg,
Cohere · no official code found in the PDF ·
**PDF:** [open](papers/2026/08_Shaheen_et_al._Understanding_the_Surprising_Generalization_Properties_of_Tabular_Foundation_Models.pdf)

**Citation key:** `2026.SHAHEEN.understandingsurprisinggeneralizationpropertiestabularfoundationmodels`.

**Where it fits.** The most direct challenge in this collection to the Bayesian reading the
paradigm was built on. [Müller 2021, *Transformers Can Do Bayesian Inference*](#pfns-2021)
argues that a PFN approximates the posterior predictive *under its prior*, which presupposes
that downstream tasks lie in the prior's support. This paper shows a model pretrained on **one
real table** transferring to unrelated ones and proposes a **retrieval-and-aggregation**
account instead, in line with the localisation analysis of [Nagler 2023, *Statistical
Foundations of Prior-Data Fitted Networks*](#nagler-theory). It is a cross-lab paper: the Layer
6 AI team behind [Ma 2026, *TabDPT*](#tabdpt) with Frank Hutter (Prior Labs). It cites
[Klötergens 2026, *Do Tabular Foundation Models Agree with Themselves?*](#do-tabular-foundation)
as concurrent evidence against the prior-fitting account (§4).

**What it contains.**

* **Single-table pretraining (§2).** Architecture and procedure are fixed: the row-based
  backbone shared by TabPFN v1 and TabDPT, TabDPT's self-supervised task construction (random
  target column, random feature subset), retrieval off during pretraining and on at inference.
  Eighty-eight models are each pretrained on one TabDPT pretraining table and evaluated on 107
  held-out datasets (72 CC-18 classification, 35 CTR-23 regression; no overlap).
* **Meta-analysis (§2.2–2.3).** An XGBoost regressor predicts each table's average downstream
  score from simple meta-features; row/column-dropping and task-count experiments then separate
  feature count from the number of unique tasks a table yields (O(k·2^k) for k columns).
* **Corpus design at scale (§3).** A 1,732-dataset OpenML corpus (excluding CC-18, CTR-23 and
  TabArena) is used to test dataset-level selection (exact deduplication, ≥30-feature
  filtering) against column-level cleaning: drop columns >50% missing, greedy correlation
  deduplication at |ρ| > 0.90 (Pearson or Spearman), and skip tables with <5 surviving features.
* **Mechanism probes (§4).** (i) A retrieve-and-copy test (query rows identical to context rows)
  scored as "retrieval AUC"; (ii) tying the query and key projections (W_Q = W_K), which under
  qk-normalisation makes each attention score a negative squared distance, i.e. closer to a
  Gaussian kNN; (iii) attention-map similarity across 52 single-table checkpoints.

**Key results.**

* **Single-table transfer (Fig. 1).** A model trained only on vectorized MNIST performs well on
  California Housing; one trained only on COLLEGES closely matches a random forest on CC-18 and
  CTR-23.
* **Universality (Fig. 2).** Pretraining-table rankings are highly correlated across evaluation
  sets, with no within-domain advantage; some domains are simply better (other-science good,
  deterministic-simulated poor).
* **Width over height (Fig. 3, Fig. 4).** The meta-regressor reaches R² = 0.67; feature count
  has importance 0.771 versus 0.012 for instance count. Dropping ~70% of COLLEGES' features
  falls to linear-model level, dropping >70% of rows stays near random forest. Raising the number
  of tasks from 5 to tens of thousands moves CC-18 AUC from ~0.5 to good. Pairing a strong with
  a weak table does not hurt (COLLEGES 0.918 + ANALCATDATA_SUPREME 0.814 → 0.919).
* **Corpus curation (Table 1).** Exact deduplication (1,732 → 1,535 datasets) is statistically
  indistinguishable from the full corpus; ≥30-feature filtering (607 datasets) lowers every
  metric (average 0.9039 → 0.8927). Every column-level variant improves regression (IQM R² +0.002
  to +0.014) and accuracy. On TabArena (§3.3, Fig. 5) the cleaned model beats its baseline on
  67/61/63% of tasks at 4k/2k/1k training context.
* **Retrieval evidence (§4).** Retrieval AUC correlates with base AUC at Pearson 0.89 across the
  88 models (Fig. 6). W_Q = W_K gains +0.1088 AUC on three weak pretraining tables, −0.0027 on
  three strong ones and +0.0001 on the full corpus (Figs. 7–8). Attention similarity correlates
  with mean AUC (Spearman 0.537); strong–strong pairs are more similar than strong–weak
  (+0.163, Table 2).

**Strengths.** The design is the argument: holding architecture and procedure fixed while
varying only the pretraining table is the controlled discipline that [Bouadi 2026,
*O'Prior*](#oprior) applies to synthetic priors. The width-over-height and column-versus-dataset
results are directly actionable for anyone assembling a real-data corpus, including what *not*
to bother doing (exact deduplication, feature-count filtering). The retrieval account connects
several loose ends: why retrieval-based models such as LoCalPFN ([Thomas 2024, *Retrieval & Fine-Tuning for
In-Context Tabular Models*](#localpfn)) and
TabDPT gained most, and why Nagler's localisation gap matters.

**Limitations.** Author-stated (§6): other mechanisms besides learned retrieval cannot be
excluded; pretraining is **real-data only**, so the findings may not extend to the synthetic-prior
models whose Bayesian justification is questioned; and only **row-based attention** is tested,
not the cell-based attention of TabPFN v2 or the row-compression designs of TabICL and TabPFN-3.
Reviewer reading: the probes show retrieval is *sufficient* and correlated with quality, not that
it is the mechanism; models are small and the authors concede approximate Bayesian inference may
occur under broader priors. No calibration is reported, although calibrated posteriors are what
the Bayesian framing explains. Unreviewed preprint.

---

<a id="exaone-tabular-1"></a>

## 2026-08 — Eo et al. — EXAONE Tabular 1.0: Technical Report

**Provenance.** Technical report, arXiv preprint · arXiv
[2608.25774v1](https://arxiv.org/abs/2608.25774v1) (filed version, 26 August 2026) · LG AI
Research · inference code on [GitHub](https://github.com/LGAI-Research/EXAONE-Tabular)
(BSD-3-Clause-LG, commercial use allowed) and weights on
[Hugging Face](https://huggingface.co/LG-AI-Research/EXAONE-Tabular) under the non-commercial
EXAONE AI Model License 1.2 - NC (§6); prior and training code not released ·
**PDF:** [open](papers/2026/08_Eo_et_al._EXAONE_Tabular_1.0_Technical_Report.pdf)

**Citation key:** `2026.EO.exaonetabular10technicalreport`.

**Where it fits.** An intervention in the field's main architectural question: *where, if
anywhere, should a model collapse a row into a single vector?* [Hollmann 2025, *Accurate
predictions on small data with a tabular foundation model*](#tabpfn-v2-nature) (TabPFN v2) keeps
a representation per **cell** and alternates feature- and sample-axis attention. [Qu 2025,
*TabICL*](#tabicl-2025), [Qu 2026, *TabICLv2*](#tabiclv2) and [Grinsztajn 2026,
*TabPFN-3*](#tabpfn-3) compress each row into one embedding *before* a dataset-level ICL stage,
which buys row-count scaling. EXAONE Tabular argues the compression boundary is the defect and
removes it. It is the fourth industrial lab in the field after Prior Labs, Amazon ([Zhang 2025,
*Mitra*](#mitra)) and Google ([Kong 2026, *TabFM*](#tabfm), released in June and documented
in a September paper).

**What it contains.**

* **CAST (Cross-Axis Summary Transformer, §2.1, Table 2).** Twelve layers, width 192, six heads.
  Each layer applies feature-axis attention twice within every item (with three item-summary
  tokens appended to the item's cells), then support-conditioned item-axis attention within
  every feature (with 32 feature-summary tokens appended to the feature's support cells). Cells
  read the other axis's summary tokens by cross-attention before each step, so cell-level state
  survives the whole depth and support context formed at one layer can reshape feature
  representations at the next. Query cells only cross-attend to support and summary states, so
  each query prediction is conditionally independent of the other queries and can be chunked.
  Attention uses Scalable Softmax (SSMax) for context-length generalisation.
* **Heads (§2.2).** Classification: an MLP over at most 10 classes; more classes use an
  error-correcting output-code (ECOC) decomposition at inference. Regression: **999 conditional
  quantiles** (τ = k/1000); the point estimate is a trapezoidal average over the central 99.8% of
  the sorted quantile function.
* **Prior and training (§2.3, §3).** Synthetic only: an SCM prior whose edges are neural,
  tree-based or identity mechanisms, with categorical discretisation, feature warping,
  quantisation, missingness injection and an optional quality filter. Classification and
  regression are separate checkpoints (20.81M and 21.11M parameters) trained on ~30M and ~10M
  synthetic tables with Muon plus AdamW, WSD schedules and EMA weights. Missing values are
  consumed natively, with missingness indicators in the feature encoding.
* **Inference (§2.4–2.5).** Eight test-time estimators by default (preprocessing, category,
  feature-order and label permutations); support-side key/value caching across query chunks;
  support sets beyond the configured limit are subsampled.

**Key results.**

* **TabArena (51 tasks; numbers from the official leaderboard, §4.3).** Classification: highest
  Elo on the whole leaderboard with the single default configuration, ≈125 Elo above TabPFN-3 at
  comparable latency (0.605 s per 1K samples, Fig. 3). Regression: second to TabFM within
  overlapping 95% CIs at ≈1/11 of its inference time (TabFM ≈7.0 s per 1K), ≈140 Elo above Nori
  (Fig. 4). Split-level win rates of 65–92% against the other TFMs and ≥89% against every
  tuned-and-ensembled GBDT and neural baseline (Fig. 5). Combined, statistically tied with
  TabFM at ≈1.3% of its stored parameters (Fig. 1), measured against the 1.64B June 1.0.0
  checkpoint; the paper's 1.1.0 checkpoint has 408.7M.
* **BCCO (§4.4, Fig. 6; re-run against six TFMs from official checkpoints, support capped at
  50K).** Classification accuracy 0.792 versus TabFM 0.799 (2nd; TabFM uses 32 ensemble members,
  the others 8); regression R² 0.799, first ahead of TabPFN-3 (0.795).
* **TALENT (§4.5, Fig. 7).** Accuracy 0.857 versus TabFM 0.863 on 188 classification datasets
  (12 with >10 classes excluded); regression R² 0.736, first ahead of TabFM (0.733) on 100
  datasets.
* **ScoringBench (§4.6, Fig. 8; live leaderboard, 102 datasets).** Best mean rank on R², RMSE
  and CRPS, i.e. on the full predictive distribution as well as the point estimate.

**Strengths.** The compression-boundary claim is a falsifiable architectural argument, and the
efficiency results (≈21M parameters on the TabArena Pareto front) are the strongest evidence
for it. Ranking first with one untuned default configuration against tuned-and-ensembled
baselines is the comparison that [Purucker 2026, *Beyond IID*](#beyond-iid) argues the field
should make. Native missing-value handling and a CRPS-leading quantile head are useful on real
tables. The licences, ensemble budgets and confidence-interval overlaps are stated plainly.

**Limitations.** A vendor report, not peer reviewed. **No ablation isolates CAST** from the
prior and training recipe, so the architectural claim rests on end-to-end wins; the prior and
training code are not released. TabArena and ScoringBench numbers are leaderboard-reported, while
BCCO/TALENT use a 50K support cap and drop many-class datasets. Author-stated (§5): the 10-class
head needs ECOC, whose cost grows with the label space (a ceiling that [Wu 2025,
*APT*](#apt) and [Arbel 2025, *EquiTabPFN*](#equitabpfn) attack differently), and large
supports are subsampled rather than compressed. Weights are non-commercial. Being synthetic-only,
it does not speak to the real-data question raised by [Garg 2025, *Real-TabPFN*](#real-tabpfn)
and [Shaheen 2026, *Understanding the Surprising Generalization Properties of Tabular Foundation
Models*](#shaheen-retrieval).

---

<a id="do-tabular-foundation"></a>

## 2026-08 — Klötergens et al. — Do Tabular Foundation Models Agree with Themselves?

**Provenance.** arXiv preprint (no peer-reviewed venue recorded) · arXiv
[2608.06004v1](https://arxiv.org/abs/2608.06004v1) (filed version, 6 August 2026) · University
of Hildesheim (ISMLL / VWFS DARC) · no code repository linked in the PDF ·
**PDF:** [open](papers/2026/08_Klotergens_et_al._Do_Tabular_Foundation_Models_Agree_with_Themselves.pdf)

**Citation key:** `2026.KLOTERGENS.tabularfoundationmodelsagreethemselves`.

**Where it fits.** A label-free test of a *necessary* consequence of the Bayesian reading in
[Müller 2021, *Transformers Can Do Bayesian Inference*](#pfns-2021): if a TFM's predictions are
posterior predictives under some prior, they must at least be conditionals of *one* joint
distribution. The posterior itself cannot be checked on real data, but coherence can. The
question matters whenever univariate TFMs are chained into multivariate predictors (append a
predicted target as a feature, predict the next), e.g. for generation or imputation. It is
cited as concurrent evidence by [Shaheen 2026, *Understanding the Surprising Generalization
Properties of Tabular Foundation Models*](#shaheen-retrieval), which argues for a retrieval
rather than Bayesian account.

**What it contains.**

* **Two consistency requirements (§3)**, stated for a pair of targets A and B with the remaining
  columns as features. *Marginalization consistency* (C1): the marginal of A predicted directly
  without B must equal the mixture of the conditionals p̂(a | b, x) weighted by the model's own
  p̂(b | x) (the law of total probability; the finite analogue of the martingale property of
  coherent predictive systems). *Factorization consistency* (C2): the two chain-rule orders,
  p̂(a | b, x) p̂(b | x) and p̂(b | a, x) p̂(a | x), must give the same joint.
* **Theory.** Proposition 1: C2 implies C1 for normalised predictive densities, so any C1
  failure already certifies order dependence. Proposition 2: C1 does not imply C2 (counterexample
  in Appendix A).
* **Measurement (§4.1).** Total-variation distance between the two sides of each check, averaged
  over test points under 5-fold cross-testing. Classification checks are exact finite sums.
  Regression uses the quantile head: 1,000 equal-mass atoms for the marginalising integral,
  compared on a deliberately coarse 20-cell grid (so TV is a lower bound), and a 128 × 128 grid
  for the two joints.
* **Models and data.** TabPFN v2 and v3, TabICL v1 and v2, TabDPT v1.2, and (classification only)
  TabFM, whose regression head gives points only. Ten classification and seven regression
  OpenML tables with a natural pair of mutually dependent target columns (Appendix B).

**Key results.**

* **Every model violates both conditions on every dataset** (Tables 1–2), for classification and
  regression; classification gaps are exact, so not sampling noise. Factorization gaps are larger
  than marginalization gaps, and the two are strongly associated across model–dataset pairs
  (Pearson r = 0.89, Spearman ρ = 0.90; Fig. 3).
* **Classification.** TabFM has the lowest factorization TV on 8 of 10 datasets and is second on
  the rest; for marginalization no model is uniformly best (TabFM lowest on five datasets, TabDPT
  on four, TabPFN v3 on one). TabICL v1 is the most inconsistent classifier. Average TV ranges
  from 0.001 to 0.17, and the worst single test instance per cell often exceeds 0.4 (up to 0.76).
* **Regression.** No model is near zero on any dataset. TabDPT is the most marginalization-
  consistent (lowest on six of seven datasets) but among the least factorization-consistent;
  TabPFN v3 is the most factorization-consistent on most datasets.
* **Consistency is a separate axis (§4.4, Appendix D).** Consistency gaps show no strong
  correlation with accuracy or RMSE. TabDPT, trained on real data with swapped target columns,
  is no more consistent on OpenML tables it may have seen in pretraining.

**Strengths.** The diagnostics need neither labels nor knowledge of the pretraining prior, are
cheap (C1 compares univariate heads only) and are formally ordered, so one test certifies both
failures. The classification results are exact, and the regression discretisation is chosen to
under- rather than over-state violations. It adds an evaluation axis that accuracy benchmarks
such as TabArena do not capture, and the authors argue it should sit next to accuracy and
calibration for any TFM used as a joint density estimator (§6).

**Limitations.** Seventeen hand-picked target pairs and specific model releases; mixed
categorical–continuous pairs are left out because current models use separate classification
and regression weights (§6). The findings show finite trained models are incoherent; they do not
refute the asymptotic PFN loss argument, nor show that single-target predictions are poor.
Consistency is neither calibration nor correctness. No remedy is tested: training penalties,
shared latent joints and post-hoc reconciliation are only proposed.

---

<a id="tabiclv2"></a>

## 2026-09 — Qu et al. — TabICLv2

**Provenance.** ICML 2026 (PMLR 306), first posted 11 February 2026 · arXiv
[2602.11139v2](https://arxiv.org/abs/2602.11139v2) (filed version, 16 September 2026) · Inria
SODA team with Probabl · fully open: inference, pretraining and prior code at
[soda-inria/tabicl](https://github.com/soda-inria/tabicl), plus a minimal educational
re-implementation ([nanotabicl](https://github.com/soda-inria/nanotabicl)) ·
**PDF:** [open](papers/2026/09_Qu_et_al._TabICLv2_A_better_faster_scalable_and_open_tabular_foundation_model.pdf)

**Citation key:** `2026.QU.tabiclv2betterfasterscalableopentabularfoundationmodel`.

**Where it fits.** The successor to [Qu 2025, *TabICL*](#tabicl-2025) and the open-source
counterweight to the closed TabPFN-2.5 prior ([Grinsztajn 2026, *TabPFN-2.5*](#tabpfn-25)):
weights, synthetic-data engine and pretraining code are all released. Its row-compression
design and prior became reference points for later reports, which borrow from it or benchmark
against it: [Grinsztajn 2026, *TabPFN-3*](#tabpfn-3), [Jäger 2026, *TabPFN-3.5*](#tabpfn-3-5),
[Eo 2026, *EXAONE Tabular 1.0*](#exaone-tabular-1), and SurvICL ([Alberge 2026, *SurvICL: a
Foundation Model for in-context Survival Analysis*](#survicl-a-foundation)), which builds on it.

**What it contains.**

* **Architecture (§3, ~28M parameters).** TabICL's three stages are kept, at O(n² + nm²) cost:
  a set transformer embeds each column, a row transformer with [CLS] tokens compresses each row
  to one vector, and an ICL transformer lets test rows attend to training rows. New: *repeated
  feature grouping* (each feature enters three groups via circular shifts (0, 1, 3), which
  breaks feature symmetry without reducing the feature count); *target-aware embedding* (the
  label embedding is added to every training cell before compression, so feature relevance can
  be judged early); and **QASSMax**, a query-aware scalable softmax. QASSMax rescales queries by
  an MLP of log n times a bounded query-dependent gate, countering "attention fading" (the
  softmax denominator grows with context length n, flattening attention) in the column and ICL
  transformers.
* **Outputs.** Regression predicts 999 quantiles trained with pinball loss (mean of quantiles for
  point predictions; full distribution with exponential tails, Appendix I). More than 10 classes
  use *mixed-radix ensembling* (one column-embedding pass per digit of a balanced mixed-radix
  label code) combined with hierarchical classification in the ICL stage.
* **Prior (§5, Appendix E).** Fully synthetic and developed mostly by design principles rather
  than validation feedback: random "Cauchy" graphs, eight random function types (MLP,
  CatBoost-style symmetric tree ensembles, discretisation, GP, linear, quadratic, EM-style
  plateaus, products), no node-level Gaussian noise, correlated hyperparameter sampling, and
  rejection of datasets where ExtraTrees cannot beat a constant baseline (~35% of classification
  and ~25% of regression datasets filtered in stage 1).
* **Pretraining (§4).** Muon instead of AdamW; three stages (500K steps at 1,024 rows, 40K steps up
  to 10,240 rows, 10K steps up to 60K rows), ~35M synthetic datasets, ~24.5 H100 GPU-days per
  model. Disk offloading handles 1M rows × 500 features in ~450 s within 50 GB GPU and 24 GB CPU
  memory.

**Key results.**

* **TabArena and TALENT (§6, Figs. 1, 5).** Untuned, TabICLv2 dominates the improvability–runtime
  Pareto front and surpasses RealTabPFN-2.5 even when the latter is tuned and ensembled. A
  binomial test on TALENT gives a win rate above 50% against RealTabPFN-2.5 (accuracy p = 0.0018,
  R² p = 0.0028; Table L.2), although critical-difference diagrams show no significant gap.
* **Speed (Fig. 6).** Faster than TabPFN-2.5 on every tested hardware: 10.6× on an H100 at 50K rows
  and 11.8× on CPU at 10K rows (100 features, 8 estimators).
* **Scale and many classes (Figs. 7–9).** Beats RealTabPFN-2.5 on TALENT datasets above 20K rows,
  performs strongly on ~600K-row datasets where TabPFN-2.5 runs out of memory, and outperforms all
  baselines on the 12 TALENT datasets with >10 classes (the ECOC wrapper is slightly better but
  3× slower than mixed-radix ensembling).
* **Ablations (§7, Fig. 10).** The prior has the largest effect, with a strong architecture × prior
  interaction: TabICLv2 trained on the TabICL prior degrades, and TabICL trained on the new prior
  only matches TabICL. Early target inclusion, Muon and QASSMax each give ≈100 Elo (≈64% win
  rate); feature grouping and filtering give smaller gains.
* **Appendix L (added in v2).** Most ensembling gain is reached by 8 members (Table L.1); with 16
  training samples TabICLv2 ranks second to RealTabPFN-2.5 (Table L.3); it beats Claude Opus 4.6
  and Qwen3.5 from 16 shots on nine small classification datasets (Table L.4); the TabPFN random
  forest extension lowers memory but hurts accuracy and runtime (Table L.6); label noise degrades
  it less than tree models.

**Strengths.** The most complete open release among frontier TFMs, with a minimal reference
implementation and a modest, disclosed pretraining budget. Single-component ablations isolate
each architectural and optimisation change, and the architecture × prior result shows why
prior and architecture cannot be judged separately. Strong untuned results at substantially
lower runtime than its closest competitor.

**Limitations.** Author-stated (§8): no use of column names or text; missing values are
mean-imputed; distributional regression is evaluated only on toy data; million-row tables remain
challenging; no multi-output or shift handling; tuning and finetuning are not explored. Reviewer
reading: the prior itself is not ablated component by component (by design), so which prior
elements matter is unknown; ablations run at 280K steps with fewer heads than the release; no
calibration metric beyond log-loss is reported; the Appendix L comparisons (nine LLM datasets,
six noise datasets) are small.

---

<a id="tabpfn-3-5"></a>

## 2026-09 — Jäger et al. — TabPFN-3.5: Technical Report

**Provenance.** Technical report (Prior Labs Team, contributors in Appendix A), arXiv preprint ·
arXiv [2609.17895v2](https://arxiv.org/abs/2609.17895v2) (filed version, 22 September 2026;
report dated 14 September 2026) · Prior Labs · code ([`tabpfn`](https://github.com/PriorLabs/TabPFN),
client SDK) under Apache 2.0; TabPFN-3.5 and -Fast weights downloadable under the restrictive
TABPFN-3.5 License v1.0; -Plus and -Thinking API/enterprise only ·
**PDF:** [open](papers/2026/09_Jager_et_al._TabPFN_3.5_Technical_Report.pdf)

**Citation key:** `2026.JAGER.tabpfn35technicalreport`.

**Where it fits.** The successor to [Grinsztajn 2026, *TabPFN-3*](#tabpfn-3), four months on,
and a response to [Purucker 2026, *Beyond IID: How General Are Tabular Foundation Models,
Really?*](#beyond-iid) (which has Prior Labs co-authors): that benchmark found TFMs behind tuned
models on grouped and temporal splits, large or wide tables, and text or high-cardinality
features. TabPFN-3.5 retunes its prior towards those slices and reports on that benchmark. It
borrows Fourier value encodings from [Kong 2026, *TabFM*](#tabfm) and prior ideas from [Qu 2026,
*TabICLv2*](#tabiclv2), and its relational results come through the harness of [Hayler 2026,
*RelArena-α, TabPFN-Rel and RPI*](#advancing-open-and).

**What it contains.** TabPFN-3's three-stage design is kept; the changes are (§3):

* **Per-cell encodings (Fig. 8).** On top of TabPFN-3's missing/infinite indicators, feature
  grouping (G = 3 columns at circular offsets) and standardised values, each value gets learned
  **Fourier features** (32 frequencies, sine and cosine) and an **in-context ECDF feature**: the
  cell's midrank among the training rows of its column, expanded into low-frequency sines and
  cosines, so monotone transformations of a column (e.g. a log) give identical encodings.
  Quantile/robust-scaling and SVD preprocessing are dropped (§3.2).
* **One multitask checkpoint.** Classification and regression are trained jointly with the task
  type as input; only the label encoder and output head are task-specific. QK-norm and extra
  normalisation layers stabilise training.
* **Doubled width, same cache.** The ICL transformer goes from 512 to 1,024 dimensions (eight
  instead of four CLS tokens per row, 16 heads), roughly quadrupling parameters to 220M (Fast:
  84M). Test rows attend through a single 64-dimensional key/value head, so the KV cache, and
  hence cached single-row prediction time, stays about the same as TabPFN-3's. Recommended
  limits rise to 1M rows × 6,000 features (Fig. 1a).
* **Prior (§3.3).** Close to TabPFN-3's, with more diversity, TabICLv2-inspired elements and
  emphasis on high-cardinality categoricals, many features and grouped data whose test group is
  unseen in training. Not disclosed in detail.
* **Family.** TabPFN-3.5 (8 estimators) and TabPFN-3.5-Fast (4 estimators; up to 6× faster than
  3.5, 3× faster than TabPFN-3) are open checkpoints. -Plus adds text/date handling and FP8
  attention; -Thinking adds inference-time compute (12× faster than TabPFN-3-Thinking). Their
  implementation is proprietary and "intentionally not described" (§3.4).

**Key results.**

* **Seven benchmarks (Table 1).** The best family member ranks first on TabArena, BeyondArena,
  STRABLE, MulTaBench, RelArena-α, TALENT and ScoringBench. That member is -Thinking on the first
  four, TabPFN-Rel built on -Plus on RelArena-α, and the open TabPFN-3.5 only on TALENT and
  ScoringBench. Split win rates against the best other TFM: 57% (TabFM), 83% (TabICLv2), 98%,
  90%, 57% (RT-PluRel), 80%, 78% (EXAONE); means 78% against the best other TFM and 89% against
  the best non-foundation model.
* **TabArena (§2.1, Fig. 2).** The open TabPFN-3.5 beats TabFM by 84 Elo at one tenth of its total
  time per sample and AutoGluon 1.6 extreme by 130 Elo at a fifth of the time; clearly better than
  TabPFN-3 per dataset (Wilcoxon p < 0.0001, Fig. 1b).
* **BeyondArena (§2.2, Figs. 3–4).** First overall and better than TabPFN-3 in every slice, but
  **tuned-and-ensembled MLPs still lead on grouped, temporal and large datasets**; restricted to
  tables under 100K rows, TabPFN-3.5 matches the best baselines on grouped and temporal data.
  The group identifier is exposed to the TabPFN models on some grouped datasets, which differs
  from the official BeyondArena procedure (Appendix C.2.3). -Thinking adds 20 Elo; -Fast loses 40.
* **STRABLE and MulTaBench (§2.3–2.4).** Compared against the published leaderboards, not re-run;
  open checkpoints use the benchmarks' TF-IDF or frozen-embedding preprocessing, while -Plus and
  -Thinking read raw text.
* **Speed (§2.6, Fig. 7).** Up to 2× slower than TabPFN-3 on large training sets (1.25× behind
  -Plus); cached prediction of a single row matches TabPFN-3.
* **Other.** The general checkpoint beats the time-series-specific TabPFN-TS-3 on fev-bench
  (Appendix C.6); swapping TabPFN-3-Plus for 3.5-Plus adds nearly 90 Elo in TabPFN-Rel.

**Strengths.** The broadest evaluation in this collection, much of it on benchmarks built to
expose TFM weaknesses, including the lab's own critique. Doubling width while holding the cache
fixed is a deployment-minded choice, and the ECDF encoding is a simple, clearly motivated fix for
skewed and heavy-tailed columns. The report states where tuned MLPs still win and that the
temporal slice is confounded with dataset size.

**Limitations.** No ablation separates encodings, width, joint training and prior, so the
BeyondArena gains cannot be attributed (the problem [Bouadi 2026, *O'Prior*](#oprior) names). The
"first on all seven" headline mixes family members, and four of the seven wins belong to
API-only variants whose methods are undisclosed. Several comparisons reuse published leaderboard
numbers, so newer models are absent; grouped-data evaluation exposes the group identifier. The
prior is undisclosed. Weights may not be used for commercial or production purposes, including
outputs feeding internal commercial decisions (§4). A vendor report, not peer reviewed.

---

<a id="mitra-v2"></a>

## 2026-09 — Tao et al. — Mitra-v2 Technical Report

**Provenance.** Technical report, arXiv preprint · arXiv
[2609.04540v1](https://arxiv.org/abs/2609.04540v1) (filed version, 3 September 2026) · Amazon ·
weights (`autogluon/mitra-classifier-2`, `autogluon/mitra-regressor-2` on Hugging Face),
inference and finetuning code (`autogluon/mitra-finetune`) and evaluation results under
Apache-2.0 · **PDF:** [open](papers/2026/09_Tao_et_al._Mitra_v2_Technical_Report.pdf)

**Citation key:** `2026.TAO.mitrav2technicalreport`.

**Where it fits.** The successor to [Zhang 2025, *Mitra: Mixed Synthetic Priors*](#mitra). Mitra-v1
argued for *mixing* priors; Mitra-v2 asks how far a fixed, small backbone can be pushed by
*widening the synthetic task distribution* and changing the optimiser. Its new Hybrid SCM is a
variant of the generator in [Bouadi 2026, *O'Prior*](#oprior), but unlike that study it is **not**
a controlled comparison: the authors state that several training changes were made at once
(§5). It competes directly with [Kong 2026, *TabFM*](#tabfm), [Eo 2026, *EXAONE Tabular
1.0*](#exaone-tabular-1) and [Grinsztajn 2026, *TabPFN-3*](#tabpfn-3), and is the only one of the
four with permissively licensed weights.

**What it contains.**

* **Backbone (§2.1).** The Tab2D model of Mitra-v1, unchanged: 12 layers of cell-wise 2D
  attention (across rows, then across columns), width 512, four heads, no positional encoding.
  75.7M parameters for classification; 76.7M for regression, whose MSE head is replaced by a
  1,000-bin distributional head (the only architectural change).
* **Wider pretraining (Table 1).** Support tables of 160–5,120 rows (v1: up to 512), 1,280 query
  rows (v1: 128), 1–50 features (v1: 16), still at most 10 classes; ~28.7M nominal classification
  tasks on 4 × 8 H200s.
* **Prior (§2.2–2.3).** A hand-set outer mixture: base TabPFN-style SCM 0.35, **Hybrid SCM** 0.35,
  five tree-based generators 0.06 each. The Hybrid SCM places different mechanism families (MLPs,
  decision trees, ExtraTrees, random forests, 1D convolutions, random-Fourier-feature GPs, vector
  autoregression) at different nodes of one 3–7-node DAG; Mitra-v2's variant uses vector-valued
  nodes and residual-like parent projections.
* **Optimisation (§2.5).** Muon on 2D weight matrices, AdamW elsewhere, ~14,000 updates at 2,048
  tasks per update (regression finetuned 3,000 more).
* **Deployment wrappers (§2.6, §3.1).** Tables wider than 50 features are reduced to 256 by
  train-only SelectKBest (classification) or truncated SVD (regression). More than 10 classes use
  a balanced hierarchical tree of ≤10-class Mitra nodes, with a different class grouping per
  bagged member. The **evaluated system** is AutoGluon's bagged Mitra: ~50 finetuning steps per
  child, eight-fold bagging, support up to 16,384–32,768 rows at prediction.

**Key results.**

* **TabArena, 51 datasets, one-hour budget (Table 3).** Elo 1,774.6 versus TabFM 1,773.5, EXAONE
  1,749.4 and TabPFN-3 1,637.5, with overlapping intervals; only a four-hour AutoGluon 1.6
  portfolio rates higher. Mitra-v2 is first outright on about 9 of 51 datasets, but TabFM has the
  smaller mean gap to the best method (5.3% versus 7.1%). Classification is a three-way tie
  (~128 Elo over TabPFN-3; lower error than TabPFN-3 on 31 of 38 datasets); on regression Mitra-v2
  has the smallest gap to best of any single model (1.5%).
* **TALENT, 274 datasets without the TabPFN/TabICLv2 development sets (§4, Tables 7–8).** Under
  matched train-only context TabFM leads (1,503.2) ahead of Mitra-v2 (1,479.7) and EXAONE
  (1,451.8), all within intervals; Mitra-v2 leads TabPFN-3 by 65–85 Elo. With validation rows in
  context, EXAONE gains 67 Elo and moves above Mitra-v2. Mitra-v2 is first on the 12 datasets with
  >10 classes (2,070 Elo, +220 over TabPFN-3; TabFM cannot run them) and has the best train-only
  regression point estimate; its weakest slice is ≤10-class classification, ~75 Elo behind TabFM.
* **Negative results (Appendix C).** HL-Gauss, CRPS and quantile heads, longer or continued
  pretraining, real-data-like correlation priors, reweighting the mixture and larger prediction
  contexts did not help.

**Strengths.** Shows that data and optimiser scaling on a fixed 77M backbone reaches the level
of a model about 21× larger (the 1.6B June TabFM checkpoint; the paper's 1.1.0 checkpoint has
408.7M parameters). The many-class wrapper reaches first place without any many-class
pretraining. The report is unusually careful about comparison conditions: matched context
policies on TALENT, removal of competitors' development datasets, a disclosed TabFM time-budget
asymmetry, uncertainty intervals and an appendix of negative results. Fully open under
Apache-2.0, including finetuning code.

**Limitations.** Author-stated (§5): the top of every board is a statistical tie; the regression
board has only 13 datasets; the headline system is finetuned and bagged, so it "should not be
described as zero-shot or Pareto-dominant", and is much slower than forward-pass models; context
length, feature range, prior mixture, optimiser, distributed recipe and checkpoint changed at
once with no ablation, and accelerator hours and realised mixture frequencies are unrecorded;
prediction time is not instrumented separately. Reviewer reading: comparing a finetuned, bagged
system against zero-shot defaults favours Mitra-v2, which matters most for the TabPFN-3 margin;
the Hybrid SCM's contribution is therefore unknown.

---

<a id="xiaomi-tabldm"></a>

## 2026-09 — Team et al. — Xiaomi-TabLDM: A Tabular Foundation Model Technical Report

**Provenance.** Technical report, arXiv preprint · arXiv
[2609.03880v2](https://arxiv.org/abs/2609.03880v2) (filed version, 4 September 2026) · Xiaomi
(authored as "Xiaomi-TabLDM Team") · classifier and regressor checkpoints on
[Hugging Face](https://huggingface.co/occams/Xiaomi-TabLDM), code on
[GitHub](https://github.com/xiaomi-research/xiaomi-tabldm) · **PDF:**
[open](papers/2026/09_Team_et_al._Xiaomi_TabLDM_A_Tabular_Foundation_Model_Technical_Report.pdf)

**Citation key:** `2026.XIAOMI-TABLDMTEAM.xiaomitabldmtabularfoundationmodeltechnicalreport`.

**Where it fits.** Another industrial entrant after Prior Labs, Amazon ([Zhang 2025,
*Mitra*](#mitra)), Google ([Kong 2026, *TabFM*](#tabfm)) and LG ([Eo 2026, *EXAONE
Tabular 1.0*](#exaone-tabular-1)). Architecturally it is a close descendant of [Qu 2026,
*TabICLv2*](#tabiclv2): the same column-embed → row-aggregate → ICL pipeline, QASSMax attention,
Muon optimiser, Cauchy-graph SCM prior and mixed-radix many-class wrapper. Its new lever is
**conditional capacity**: it is the first model in this collection with a **sparse
Mixture-of-Experts** inside the ICL transformer. Its strongest results are on **regression**.

**What it contains.** Three stages plus test-time scaling (§2–3, Fig. 4):

* **Column-wise embedding with dual-stream feature grouping.** Each column is embedded together
  with two others chosen by circular shifts, via a shared linear map ℝ³ → ℝ^d. One stream uses
  TabICLv2's fixed offsets (1, 2, 4); a second uses width-adaptive offsets (1, ⌊√s⌋, s) with
  s = min(32, m − 1), so it spans the table's width. The two embeddings are summed, then each
  grouped column is encoded by a Set Transformer with 128 inducing points.
* **Row-wise aggregation.** Four learnable CLS tokens per row and a stack of self-attention
  layers (with RoPE). The plain residual is replaced by a lightweight **Attention Residual**: at
  a fixed stride, a learned pseudo-query softmax-weights earlier block outputs, so a layer can
  retrieve shallow or deep representations. The authors report that without it Stage-1 training
  collapses on datasets beyond roughly 1,200 rows (§2.2).
* **ICL predictor with sparse MoE.** Training rows attend to each other, test rows only to
  training rows. In selected layers the feed-forward block becomes a router that activates the
  top-K of M_R routed experts plus M_S always-on shared experts, with load-balance and router
  z-losses (Table 9). The released checkpoints have ~70–71M total and ~62–63M active
  parameters (Table 10).
* **Pretraining (§2.2–2.3).** Separate classifier (cross-entropy) and regressor (pinball loss
  over 999 quantiles), synthetic SCM data only, three stages over dataset size (1,024 rows →
  400–10,240 → 400–60,000), MoE enabled from Stage 2. Tasks where ExtraTrees cannot beat a
  constant predictor are rejected. About 11–14 days on 8 A100s.
* **Test-time scaling (§3).** Ensembles over feature shuffles/subsets and preprocessing views
  (normalisations, quantile transforms, SVD features, feature interactions, heavy-tail target
  transforms), combined with non-negative least squares on holdout or out-of-fold predictions
  (an idea the authors credit to TabFM), optionally followed by probability calibration.

**Key results** (§4; all self-reported):

* **OpenML-CTR23 (33 regression datasets, Fig. 2).** Best average rank, 3.03, ahead of TabFM
  (3.06), EXAONE (3.29), TabPFN-3 (3.71) and TabICLv2 (4.55).
* **TabArena regression (13 datasets, Table 2).** Elo 1,900, second to TabFM (2,019), ahead of
  EXAONE (1,885), TabPFN-3 (1,800) and AutoGluon 1.5 extreme (1,776). Improvability 1.7% vs
  TabFM's 1.6%, with 82% less training time (6.99 vs 38.85 s per 1K rows) and 68% less
  prediction time (3.12 vs 9.67 s). TabPFN-3 is still ~7× faster at prediction (0.42 s).
* **TabArena overall (51 datasets).** Elo 1,659, fourth, essentially tied with AutoGluon 1.5
  extreme (1,662) and above TabPFN-3 (1,650).
* **TALENT (300 datasets, Fig. 3 and 6).** Second on regression (rank 4.03 vs TabFM 3.72) and
  overall (4.82 vs 4.23); tied with TabFM for best on binary classification (5.72).
* **BCCO (156 datasets, Table 3).** Second on regression and multiclass accuracy/log-loss,
  third overall (behind TabFM and EXAONE).

**Strengths.** Regression is the less-studied half of this literature, and the model is
consistently near the top across four regression suites rather than one. The MoE gives a TFM a
different scaling lever (more parameters at fixed per-token compute). Weights, code and full
architectural and MoE hyperparameters (Appendix A) are released, and the efficiency numbers are
reported alongside accuracy.

**Limitations.** No ablation separates the changes (MoE, dual-stream grouping, Attention
Residual, curriculum, enlarged prior, test-time scaling), so none can be credited with the
gains. The abstract says test-time scaling "consistently improves" over the base model, but no
with/without comparison is reported. The report has no limitations section. Classification is
competitive rather than leading (fourth overall on TabArena). Many ingredients are inherited
from TabICLv2 and TabFM. A self-reported technical report on public leaderboards, not peer
reviewed.

---

<a id="limix-2"></a>

## 2026-09 — Zhang et al. — LimiX-2: A Contextual Mechanism Network Towards General Structured-Data Intelligence

**Provenance.** Technical report, arXiv preprint · arXiv
[2609.17488v1](https://arxiv.org/abs/2609.17488v1) (filed version, 15 September 2026) · LimiX
Team, Stable AI and Tsinghua University · links the LimiX
[GitHub](https://github.com/limix-ldm/LimiX/) and the Stable AI Hugging Face organisation; the
report does not state the licence or release status of the LimiX-2 weights · **PDF:**
[open](papers/2026/09_Zhang_et_al._LimiX_2_A_Contextual_Mechanism_Network_Towards_General_Structured_Data_Intelligence.pdf)

**Citation key:** `2026.ZHANG.limix2contextualmechanismnetworkgeneralstructureddataintelligence`.

**Where it fits.** The scaled successor of [LimiX Team 2025, *LimiX: Unleashing
Structured-Data Modeling Capability for Generalist Intelligence*](#limix-unleashing-structured)
and sibling of the small [Wang 2026, *LimiX-2M*](#limix-2m-mitigating). Like [Eo 2026, *EXAONE
Tabular 1.0*](#exaone-tabular-1) it keeps one representation per cell instead of compressing
rows, against the row-compression camp of [Qu 2026, *TabICLv2*](#tabiclv2) and [Grinsztajn
2026, *TabPFN-3*](#tabpfn-3). Its framing, **Contextual Mechanism Networks (CMNs)**, targets
the joint p(x, y | context) through masked reconstruction instead of only the label posterior
p(y | x, context). Its causal claim is about graph-skeleton recovery, not treatment-effect
estimation as in Ma 2026 (*Foundation Models for Causal Inference via Prior-Data Fitted
Networks*).

**What it contains.** (§2–4)

* **Cell embeddings.** Each cell gets a d = 256 vector from a shared two-layer MLP; missing
  cells share one learnable vector. Column identity comes from a low-rank (d/4) learned code,
  so columns are distinguishable without positional order. Targets are encoded into K = 4
  task-embedding slots.
* **Backbone (24 dual-axis blocks, Fig. 2).** Sample-axis attention (context rows see each
  other; queries see only context, so predictions do not depend on the query batch), separate
  SwiGLU FFNs for feature and target streams, then *asymmetric* feature-axis attention:
  features attend to features and target, the target attends only to features. Q/K
  normalisation and a learned length-dependent query scaling stabilise long contexts.
* **Heads.** Classification and a 5,000-bin regression head read the final task embeddings;
  the masked-feature reconstruction head reads a shallower layer.
* **Context-Conditional Masked Modeling (CCMM, §3).** Each episode combines target prediction
  with reconstruction of masked query entries, using entry, column and block masks.
* **Prior (§4).** Synthetic SCM data only, from an expanded generator (more graph structures,
  mechanisms and observation transforms than LimiX).
* **Scaling study (§6).** Six sizes from 12.5M to 406.2M parameters under a fixed data,
  optimisation and inference recipe.

**Key results** (§5–6; TabArena against leaderboard scores accessed 15 September 2026;
TALENT/BCCO with 15 seeds, competitor TFMs run untuned from their official repositories):

* **TabArena (51 datasets, Table 2).** Default LimiX-2 (406.2M) Elo 1,935, 117 above the
  runner-up TabFM+ (1,818) and ahead of Causilo (1,790), AutoGluon 1.6 non-commercial 4h
  (1,789), TabFM (1,774), Mitra-v2 (1,769), EXAONE (1,749) and TabPFN-3 (1,632). First on both
  classification (1,917) and regression (2,206).
* **TALENT (288 datasets; 12 with >10 classes excluded; Table 5).** Elo 1,506 vs TabFM 1,471
  and AutoGluon 1.6 extreme 1,438; first in all five categories.
* **BCCO (156 datasets, Table 6).** Elo 1,432, 56–63 above AutoGluon 1.6 and TabFM and 202 above
  LimiX-16M.
* **Causal skeletons (§5.5, Table 7).** Thresholded feature-attention scores give mean skeleton
  F1 0.7972 over six datasets (Sachs, UF, CausalChamber, PATHFINDER, DIABETES, PIGS), vs 0.6591
  for EXAONE; best F1 on all six, lower SHD than PC, GES, NOTEARS-MLP and others on five.
* **Scaling (Table 8, Fig. 12).** Elo is log-linear in parameters (R² 0.96–0.98); on TabArena
  +169 Elo from 12.5M to 406.2M (34.7 per doubling), with no saturation observed.

**Strengths.** Makes feature reconstruction an explicit pretraining task, so one model serves
prediction, imputation and structure probing. The scaling sweep holds the recipe fixed, which
is stronger evidence for capacity scaling than comparing unrelated models. Protocols,
baselines and per-dataset causal results are reported in detail, and the authors themselves
caution that cross-model gaps cannot be attributed to design alone (§6.2).

**Limitations.** Unreviewed technical report from the model's authors. No CCMM-versus-target-only
ablation isolates the objective's contribution from architecture and prior changes. The 2B
extrapolation is a forecast (author-stated). Conditional predictions under many masks do not
by themselves guarantee a coherent joint distribution or identify interventions. The skeleton
probe neither orients edges nor estimates effects, and spreading group-level attention
uniformly over features (author-stated protocol) structurally handicaps row-compressing models
such as TabPFN-3, TabICLv2, TabFM and Xiaomi-TabLDM. Elo values are specific to this report's
comparison pool, not interchangeable with other reports. No temporal/grouped-split robustness or
calibration evaluation.

---

<a id="causilo"></a>

## 2026-09 — Cho et al. — Causilo Technical Report

**Provenance.** Technical report, arXiv preprint · arXiv
[2609.22866v1](https://arxiv.org/abs/2609.22866v1) (filed version, 19 September 2026; report
dated 18 September 2026) · Nums AI · code on [GitHub](https://github.com/nums-ai/causilo)
under Apache-2.0; weights on [Hugging Face](https://huggingface.co/nums-ai/causilo) under the
Causilo License v1.0 (non-commercial research and evaluation only; commercial, production and
hosted use need a separate licence, §4) · **PDF:**
[open](papers/2026/09_Cho_et_al._Causilo_Technical_Report.pdf)

**Citation key:** `2026.CHO.causilotechnicalreport`.

**Where it fits.** A compromise between the row-compression design of [Qu 2026,
*TabICLv2*](#tabiclv2) and the persistent-cell route of [Eo 2026, *EXAONE Tabular
1.0*](#exaone-tabular-1) and [Zhang 2026, *LimiX-2*](#limix-2). It keeps an efficient ICL
transformer over row embeddings, but first gives cells one more exchange across features and
context rows, and makes feature-side attention linear. Despite the name, it is a predictive
model; it does not estimate causal effects.

**What it contains.** Five stages, "refine first, compress later" (§2, Fig. 2):

1. **Column encoding.** Features are grouped in threes; each scalar gets sine/cosine features at
   16 learned frequencies (an idea taken from TabFM) and a linear map to d = 128. Per column, a
   Set-Transformer layer lets inducing tokens gather from context cells and broadcast to all
   cells; query cells never feed the summaries.
2. **Row refinement.** Within each row, K = 4 summary tokens repeatedly gather from and
   broadcast to the cell tokens, so cells exchange information at O(K·G) rather than O(G²) cost
   for G feature groups (Table 1).
3. **Column refinement.** A second, independently parameterised column stage lets the enriched
   cells revisit the context.
4. **Row compression.** A separate set of four summaries reads the cells (cells stay fixed) and
   is concatenated into a 512-dimensional row embedding.
5. **ICL transformer** (12 layers): context rows attend to each other, queries only to context.

Two further ingredients: **bounded QASSMax**, which keeps TabICLv2's length- and query-dependent
attention scaling but squashes each factor into a positive bounded range (overall 1/32 to 32,
§2.3); and inference-time ensembles over four normalisation schemes, feature orders (which
change the groupings) and cyclic class shifts (§2.4). Classification and regression models
have 36.08M and 37.08M parameters, pretrained on about 36M synthetic tables; the prior is not
described.

**Key results** (§3; self-reported):

* **TabArena (leaderboard as of 18 September 2026, Fig. 1).** Combined Elo 1,785 at a median
  0.1043 s per 1K test rows, on the Pareto frontier. It exceeds TabFM's Elo with 63.8× faster
  inference and beats TabPFN-3.5-Fast with 31.6% less inference time. Higher frontier points:
  TabPFN-3.5 (1,861 at 0.47 s) and LimiX-2 (1,943 at 9.03 s). Classification 1,766 (ties TabFM,
  62× faster; does not dominate TabPFN-3.5-Fast); regression 2,019 (dominates
  TabPFN-3.5-Fast by 106 Elo).
* **Feature scaling (§2.2, Fig. 3).** In a microbenchmark of each model's feature-mixing module,
  run time grows as F^1.23 for Causilo vs F^1.90–1.99 for TabICLv2, EXAONE, Mitra-v2, TabFM and
  TabPFN-3.5.
* **BeyondArena (142 datasets, Table 2, Figs. 6–8).** Combined Elo 1,359, ahead of RealMLP
  (1,274) and TabPFN-3 (1,270). It does **not** lead on grouped splits: fourth on grouped
  classification (behind TabM, RealMLP, LightGBM) and fifth on grouped regression.
* **ScoringBench (Fig. 9).** On the Pareto frontier for RMSE, R², MAE and CRPS at ~0.3 s per
  fold; beats TabPFN-3.5-Fast, below full TabPFN-3.5; fine-tuned Mitra-v2 is slightly better on
  CRPS but takes ~242 s per fold.

**Strengths.** A concrete architectural middle ground with a clear cost argument (Table 1)
backed by a timing probe. Reports latency alongside accuracy throughout and evaluates beyond
IID splits and beyond point prediction. Unusually explicit about the licence split between code
and weights.

**Limitations.** No ablation isolates refinement, bounded QASSMax, prior or ensembling, and the
prior is undisclosed. Linear feature-side cost does not mean linear cost in rows: the ICL stage
is still quadratic in context size, and the microbenchmark times single modules, not whole
models. BeyondArena adds Causilo locally to a published board that stops at TabPFN-3, so it is
not compared there with TabPFN-3.5 or LimiX-2; its grouped-split weakness echoes [Purucker 2026,
*Beyond IID*](#beyond-iid). Elo depends on the leaderboard snapshot and comparator pool. CRPS
is a proper scoring rule, not a calibration guarantee. Unreviewed vendor report; weights are not
licensed for commercial use.

---

<a id="multabench-benchmarking-multimodal"></a>

## 2026-09 — Arazi et al. — MulTaBench: Benchmarking Multimodal Tabular Learning with Text and Image

**Provenance.** NeurIPS 2026, Evaluations and Datasets track (stated on the filed PDF; Zotero
records the arXiv preprint) · arXiv [2605.10616v2](https://arxiv.org/abs/2605.10616v2) (filed
version, 27 September 2026) · Technion with Prior Labs, NVIDIA, Inria SODA, Freiburg, Probabl
and ELLIS Tübingen · code on [GitHub](https://github.com/alanarazi7/MulTaBench), datasets on
Kaggle · **PDF:**
[open](papers/2026/09_Arazi_et_al._MulTaBench_Benchmarking_Multimodal_Tabular_Learning_with_Text_and_Image.pdf)

**Citation key:** `2026.ARAZI.multabenchbenchmarkingmultimodaltabularlearningtextimage`.

**Where it fits.** An evaluation paper in the mirrored collection, not a new TFM. It turns the
representation argument of [Arazi 2025, *TabSTAR: A Tabular Foundation Model for Tabular Data
with Text Fields*](#2025-12--arazi-et-al--tabstar) into a benchmark for both text and images,
and asks where the frozen embeddings that [Spinaci 2025, *ConTextTab: A Semantics-Aware Tabular
In-Context Learner*](#2025-12--spinaci-et-al--contexttab) relies on lose target-relevant
information. Like [Purucker 2026, *Beyond IID*](#beyond-iid), it qualifies what a benchmark win
implies, here through modality and representation rather than split design. [Lefebvre 2026,
*TILE*](#tile-bridging-llms) answers the same gap from the opposite side, with a frozen,
label-free LLM interface.

**What it contains.** A curation pipeline and the benchmark it produces (§3–4, Appendix A):

* **Four conditions per dataset**: structured-only, unstructured-only, joint frozen, and joint
  **target-aware representations (TAR)**. Embeddings come from e5-small-v2 (text) and
  DINOv3-small (images), reduced to 30 PCA components. TAR fine-tunes the encoder's top three
  layers with LoRA on the target, on the training split only (90/10 checkpoint selection),
  **without the structured features**, as a preprocessing step shared by all learners.
  Regression targets are binned into 20 equal-frequency classes for this step.
* **Acceptance rule**: a dataset enters if, for at least three of five curation learners
  (LightGBM, CatBoost, TabM, TabPFNv2, TabPFN-2.5), joint frozen beats both unimodal conditions
  (**Joint Signal**) *and* TAR beats joint frozen (**Task-awareness**), each by at least 0.001
  in rounded mean AUC/R². Five seeds, training capped at 10,000 rows, default hyperparameters.
* **Benchmark**: **40 datasets, 20 text-tabular and 20 image-tabular**, 400–114,000 rows and
  1–245 structured features, plus **40 further candidates** that pass Joint Signal only (80
  released in total). Of 56 existing text-tabular datasets, about 41% pass both criteria; of 16
  existing image-tabular datasets, 5 do, so most image tasks were newly collected from Kaggle.

**Key results.**

* **TAR generalises beyond the curation panel (§5, Fig. 4).** XGBoost, RandomForest, RealMLP,
  TabDPT and TabICLv2 also gain from TAR; GBDTs gain most. A paired, Benjamini–Hochberg-corrected
  test finds significant TAR gains on **37/40 datasets** (Appendix G.1), but it pools all
  learners with both conditions, *including* the five curation models.
* **Not an artefact of size or compression.** TAR-small beats frozen-large encoders (Fig. 5);
  the gain holds at 15, 30 and 60 PCA components and without PCA in a reduced run (Fig. 6,
  Appendix G.5). Re-curating with other 5-learner panels leaves the accepted set largely
  unchanged (Appendix G.6).
* **ConTextTab**, state of the art on CARTE, scores below every TAR variant on the text subset
  and is significantly outperformed by AutoGluon-Multimodal and TabSTAR.
* **Trimodality is rare**: of nine image-tabular datasets that also contain text, only two pass
  the strict trimodal criterion (PetFinder: TAR on both modalities gives the best AUC for every
  learner, Table 2).

**Strengths.** Makes complementary modality signal and representation adaptation separately
testable, with unimodal controls, extra learners, encoder-size and dimension checks, and
sensitivity analyses for the learner panel and thresholds. The authors state the selection
bias openly (§7) and release the broader candidate set so methods can also be checked where
frozen embeddings suffice. Attention maps (Fig. 7) show what TAR changes in the image encoder.

**Limitations.** Selection deliberately keeps tasks where this TAR recipe helps (author-stated),
so neither the model ranking nor the prevalence of TAR gains estimates general multimodal
performance, and the curation models cannot be ranked fairly. No per-dataset tuning of
learners or TAR; fine-tuning cost can dominate (Appendix G.3). TAR must be redone inside each
evaluation fold, since a globally target-tuned embedding cache would leak labels. Adaptation is
supervised and ignores the structured features, so the results motivate, but do not
demonstrate, a jointly conditioned or ICL-only multimodal TFM; none is proposed.

---

<a id="limix-2m-mitigating"></a>

## 2026-09 — Wang et al. — LimiX-2M: Mitigating Low-Rank Collapse and Attention Bottlenecks in Tabular Foundation Models

**Provenance.** ICML 2026, PMLR 306, pp. 132541–132570 ([proceedings
record](https://proceedings.mlr.press/v306/wang26kw.html)); the filed PDF is the proceedings
version, with no arXiv stamp, and Zotero also records an earlier arXiv identifier, 2606.04485 ·
Tsinghua University and Stable AI (authors disclose a conflict of interest: Stable AI develops
the LimiX family, including the LimiX-16M baseline) · checkpoints and inference code via the
LimiX [GitHub](https://github.com/limix-ldm-ai/LimiX) · **PDF:**
[open](papers/2026/09_Wang_et_al._LimiX_2M_Mitigating_Low_Rank_Collapse_and_Attention_Bottlenecks_in_Tabular_Foundation_Models.pdf)

**Citation key:** `2026.WANG.limix2mmitigatinglowrankcollapseattentionbottleneckstabularfoundationmodels`.

**Where it fits.** The small, efficiency-oriented member of the LimiX family ([Zhang 2025,
*LimiX: Unleashing Structured-Data Modeling Capability for Generalist
Intelligence*](#limix-unleashing-structured)); "2M" is the parameter count, not a generation,
and it is distinct from [Zhang 2026, *LimiX-2*](#limix-2). It targets two components that most
alternating-attention TFMs inherit from TabPFN v2 ([Hollmann 2025, *Accurate predictions on
small data with a tabular foundation model*](#tabpfn-v2-nature)): the linear scalar embedding
and the feature→sample attention order. It belongs with other cell-encoding work such as the
Fourier encodings of [Jäger 2026, *TabPFN-3.5*](#tabpfn-3-5).

**What it contains.**

* **Diagnosis (§3).** With a linear per-cell embedding and no positional signal, the embedded
  input has rank at most 2 and a single attention head's output at most 2 (H + 1 for H heads;
  Proposition 3.1, Appendix A). Adding feature IDs separates columns but does not add
  within-feature value degrees of freedom (Appendix B). Empirically, TabPFN v2's early hidden
  states have low effective rank on OpenML-CC18 (Fig. 1), and truncating every module input to
  rank 50 of 192 leaves AUC unchanged (0.9177 → 0.9143), with 0.8985 still at rank 20 (Table 1).
* **RaBEL, a radial-basis embedding layer (§4.2).** Each standardised scalar is expanded into
  M Gaussian bumps with learnable, quantile-initialised centres and widths, then linearly
  projected (shared across columns) and LayerNorm-ed. An optional **exponent gate** soft-bins
  log₂|x| and the sign, and an MLP rescales all centres and widths per cell, making the bank
  adapt across orders of magnitude.
* **Reordered bidirectional attention (§4.3).** Blocks run sample attention → FFN → feature
  attention (S→N→F) instead of feature → sample → FFN, so columns gather cross-sample statistics
  before feature mixing, and the prediction pools attention over all feature tokens rather than
  reading only the target token, so every attention computation reaches the readout.
* **Model (§5.4).** 12 blocks, d = 96, 6 heads, 1.92M parameters, pretrained on LimiX-style
  hierarchical SCM data.

**Key results.**

* **Embedding comparisons.** Inside an MLP, RaBEL is best on 7 of 13 datasets on the first
  metric against no-embedding, MLP, PLE and periodic embeddings (Table 2). Inside a 2M transformer it is best on BCCO
  classification (AUC 85.04 vs 83.52–84.66) and regression (R² 0.779; Tables 3–4). Against an identical 2M S→N→F baseline with a linear embedding, it raises
  shallow-layer numerical rank by 35% and Rank@95% by 83% (Table 5).
* **Against other models (Table 6).** Average ranks over 11 suites (TALENT, CC18, PFN, TabZilla,
  TabArena, BCCO, CTR23; ≤50K rows, ≤10K features, ≤10 classes). LimiX-2M beats TabPFN v2
  (7.24M) on 9 of 11 suites (ties TALENT-REG, loses BCCO-REG), and TabICL v1 (27.1M) and Mitra
  (75.7M) on every comparable suite. LimiX-16M is best almost everywhere.
* **Speed (Appendix C.6, Table 26).** On one synthetic 900×60 task: 171 ms on an RTX 4090 vs
  353 ms for TabPFN v2 and 1,750 ms for TabICL; 17 s vs 52 s on CPU.
* **Ablations (§5.5, Fig. 3; Appendix C.3).** On TabArena and TabZilla, adding RaBEL and the
  reordering each increase AUC; sample-attention-first orderings win. A toy DAG shows S→N→F
  attention concentrating on the target's direct causes (Fig. 2).

**Strengths.** Connects a formal statement, measured ranks, a concrete fix and a matched
2M baseline, so the embedding effect is isolated rather than asserted. The reordering costs no
parameters and is argued from what the readout actually uses. A very small model that is
competitive with much larger TFMs is useful where CPU or latency budgets are tight. The
conflict of interest is disclosed.

**Limitations.** The rank bound concerns the input and a single attention layer under a linear
embedding; later nonlinear layers can and do enrich representations, so the low-rank argument
is motivation rather than proof of a capacity limit. The text's claim of consistently
second-best performance (§5.4.3) holds among foundation models, but on regression suites TabM, RealMLP or
AutoGluon often rank better (e.g. BCCO-REG, CTR23, TALENT-REG). Baselines are earlier
generations (TabPFN v2, TabICL v1, Mitra), not TabPFN-2.5/3, TabICLv2 or LimiX-2. Reduced
training cost is claimed but not measured, and the timing uses one small synthetic task. The
shared LimiX repository evolves, so exact checkpoint configuration needs separate checking.

---

<a id="advancing-open-and"></a>

## 2026-09 — Hayler et al. — Advancing Open and Reproducible Relational Learning: RelArena-α, TabPFN-Rel and RPI

**Provenance.** α-release report, arXiv preprint (not peer reviewed) · arXiv
[2608.16319v2](https://arxiv.org/abs/2608.16319v2) (filed version, 7 September 2026; first
posted in August) · Prior Labs, with Stanford University and NVIDIA co-authors · official code
in [PriorLabs/relarena](https://github.com/PriorLabs/relarena) and the split-out
[PriorLabs/tabpfn-rel](https://github.com/PriorLabs/tabpfn-rel) (local snapshots: [repository
guide](REPOSITORIES.md#relarena-code)) · **PDF:**
[open](papers/2026/09_Hayler_et_al._Advancing_Open_and_Reproducible_Relational_Learning_RelArena_alpha_TabPFN_Rel_and_RPI.pdf)

**Citation key:** `2026.HAYLER.advancingopenreproduciblerelationallearningrelarenaatabpfnrelrpi`.

**Where it fits.** Prior Labs' entry into relational learning and the flattening counterpart to
[Hudovernik 2026, *KumoRFM-2: Scaling Foundation Models for Relational
Learning*](#kumorfm-2-scaling): where KumoRFM-2 argues for a database-native model, this report
packages the opposite bet (deep feature synthesis into one flat table, then a single-table TFM)
as **TabPFN-Rel**, a harness around [Grinsztajn 2026, *TabPFN-3*](#tabpfn-3). The benchmark
half, **RelArena-α**, brings TabArena's model/system distinction, standardised tuning and Elo
aggregation (the machinery behind [Purucker 2026, *Beyond IID*](#beyond-iid)) to relational
learning; [Jäger 2026, *TabPFN-3.5*](#tabpfn-3-5) later reports on it. Its text-column finding
connects to [Arazi 2026, *MulTaBench*](#multabench-benchmarking-multimodal).

**What it contains.**

* **An audit of RelBench v1 practice (§1, Table 1).** Missing training code; undocumented
  per-task configurations (KumoRFM-2's released configurations imply a grid of 384, RelGNN's
  checkpoints one of over 25,000); baselines copied rather than rerun; results not recomputed
  after a RelBench leakage fix (rel-event/user-ignore scores fall 2–6 AUROC points); and
  incompatible regression aggregates. Above all, **two evaluation regimes**: RelBench freezes
  the database at the test cut-off, while some methods (KumoRFM-2 and relational-transformer
  derivatives, by the authors' reading) let each rel-f1 test entity see data up to its own
  timestamp, years of extra signal. Under RelBench's regime the same model loses over ten
  AUROC points on the two rel-f1 classification tasks and its MAE rises by over 40% (§1.2).
* **RelArena-α (§2.1).** A harness for the 21 entity-level RelBench v1 tasks with one enforced
  data state. *Model* submissions declare a search space and are tuned by the framework under
  approximately compute-matched budgets (Appendix B); *system* submissions bring their own
  tuning. Elo is anchored at a global constant predictor (1,000) via TabArena's library.
* **TabPFN-Rel (§2.2).** Extends RDBLearn's deep-feature-synthesis + TFM recipe: tunes only
  aggregation depth (2, 3 or 4), gives TabPFN-3 an order of magnitude more context rows,
  fixes tuning-time data drift, uses recency/diversity-aware context selection, reuses
  validation rows as test-time context, and (API variant only, via TabPFN-3-Plus) re-attaches
  entity-table text.
* **RPI (§2.3).** A YAML-declared, model-agnostic interface for defining entity-level
  forecasting tasks on one's own database.

**Key results** (§3, single seed):

* TabPFN-Rel ranks first on the model leaderboard, ahead of GraphSAGE, RelGT, RDBLearn and
  RelGNN: Elo 1,821 for the API variant and 1,706 for the open-source, text-free variant
  (Fig. 2). Including systems, the fine-tuned relational transformer **RT-PluRel ranks first
  overall**, at about 5× the run time of TabPFN-Rel (API) and 30× that of the open-source
  variant, excluding TabPFN-Rel's CPU feature-synthesis pass.
* **Text matters locally**: the 115-point drop without text comes mainly from two tasks
  (rel-event/user-ignore, rel-avito/user-clicks).
* **Constant predictors are not trivially beaten**: a per-entity constant beats RelGNN and RelGT
  on four tasks each; only TabPFN-Rel and RT-PluRel beat it on all 21.
* **Self-reported vs rerun (Appendix C, Table 3)**: RelGNN drops by nearly 450 Elo and RelGT by
  about 200. Tuning clearly helps RelGNN but gives no reliable gain for most methods (§3.3,
  Fig. 3); TabPFN-Rel's default depth 2 is already competitive.

**Strengths.** The most careful account in this collection of why relational-learning numbers
are not comparable, with specific, checkable causes. Code, search spaces, cache-generation
scripts and per-task raw scores are public, and the report names its own conflict of interest
(a benchmark released together with a competing model). The constant-predictor and
self-reported-versus-rerun comparisons are unusually useful baselines.

**Limitations.** Vendor report, single seed, RelBench v1 entity forecasting only. The authors
list open problems (§4): compute budgets only approximately matched, preprocessing time not
tracked, flattening methods possibly disadvantaged by timestamp-boundary handling, RDBLearn run
without its LimiX backbone. KumoRFM-2, RT-J and automated-feature-engineering + GBDT baselines
are absent. The best TabPFN-Rel variant depends on the hosted API. RelGNN was re-implemented,
so part of its Elo drop may be implementation rather than tuning (author-stated). The code has
since moved on (separate TabPFN-Rel package, TabPFN-3.5 variants), so the numbers describe the
release state, not the live leaderboard.

---

<a id="tabfm"></a>

## 2026-09 — Kong et al. — TabFM: A Zero-Shot Foundation Model for Tabular Data

**Provenance.** Technical report, arXiv preprint (not peer reviewed) · arXiv
[2609.37959v1](https://arxiv.org/abs/2609.37959v1) (filed version, 29 September 2026; the only
version on arXiv as of 27 October 2026) · Google Research · first announced in the Google
Research blog post *Introducing TabFM: A zero-shot foundation model for tabular data* (Kong and
Das, 30 June 2026), which also announced a BigQuery `AI.PREDICT` interface that the paper does
not mention; the library filed that post until 2026-10-27 · the paper links the weights
[`google/tabfm-1.1.0-pytorch`](https://huggingface.co/google/tabfm-1.1.0-pytorch) (separate
classification and regression checkpoints; the June release was
[`google/tabfm-1.0.0-pytorch`](https://huggingface.co/google/tabfm-1.0.0-pytorch)) under the
non-commercial `tabfm-non-commercial-v1.0` licence; code
[`google-research/tabfm`](https://github.com/google-research/tabfm) under Apache-2.0 (licences
from the model card and repository, not the paper) · **PDF:**
[open](papers/2026/09_Kong_et_al._TabFM_A_Zero_Shot_Foundation_Model_for_Tabular_Data.pdf)

**Citation key:** `2026.KONG.tabfmzeroshotfoundationmodeltabulardata`.

**Where it fits.** Google's tabular foundation model, and the paper behind the June release
that third-party reports had been benchmarking against. It belongs to the row-compression line:
feature grouping follows [Grinsztajn 2026, *TabPFN-3*](#tabpfn-3) and [Qu 2026,
*TabICLv2*](#tabiclv2), induced column attention and CLS row pooling follow [Qu 2025,
*TabICL*](#tabicl-2025), and the SCM prior follows TabICLv2's. Its distinctive choices are
learned Fourier cell embeddings (credited by [Jäger 2026, *TabPFN-3.5*](#tabpfn-3-5) and
[Cho 2026, *Causilo*](#causilo)) and a wide 24-layer ICL predictor holding 402.7M of the
408.7M parameters. [Eo 2026, *EXAONE Tabular 1.0*](#exaone-tabular-1), [Tao 2026,
*Mitra-v2*](#mitra-v2), [Ning 2026, *Test-Time Compute*](#test-time-compute), [Zhao 2026,
*TabReliBench*](#tabrelibench) and [Cannistraci 2026, *Effectively Shallow*](#effectively-shallow)
evaluate the June 1.0.0 checkpoint, which they describe as a 1.6B-parameter model; the paper
describes the smaller 1.1.0 checkpoint (see Limitations).

**What it contains.**

* **Architecture (§3.1, Fig. 2, Table 1).** Each column is grouped with the columns at dyadic
  offsets 1 and 3; each slot maps its scalar through 32 learned Fourier frequencies, with
  separate banks and projections for numerical and categorical columns, summed into E = 128.
  Two untied stages each run three column-wise induced-attention blocks (256 inducing points,
  whose summaries read only labelled rows) and three row-wise self-attention blocks with RoPE
  over features. Eight CLS tokens pool each row into a 1,024-d vector. Labelled rows receive a
  target embedding at the input and again before a 24-layer ICL predictor (width 1,024, 8 heads)
  in which queries attend only to labelled rows, so test predictions are conditionally
  independent given the context. A two-layer head outputs class logits or a scalar regression
  value. Total 408.7M parameters.
* **Pretraining (§3.2, Fig. 3).** Synthetic SCM tables only: random DAGs with randomised
  functions, four root distributions, sum/product/logsumexp/max aggregation, randomised shape,
  categorical share and cardinality, missingness, label noise and class balance, at most 100
  columns. Each table carries a classification and a regression target, and the loss is taken on
  query rows. A four-stage curriculum grows context from 2,048 to 16,384 rows at a constant 2^22
  rows per step. Dataset count, steps, optimiser and compute are not reported.
* **TabFM+ (§4).** 32 views through the frozen checkpoint: half on the original columns (up to
  500 features), half with added random pairwise products and truncated-SVD features (up to
  ⌊√H⌋ each); each view varies scaling (optionally Yeo–Johnson, clipping at z = 4), column order,
  categorical codes and class-label order. Members are stacked by non-negative least squares on
  internal validation folds, shrunk 25% toward uniform, with Platt scaling for classification.
  This is the ensemble configuration of the June announcement.
* **TabFM-Auto (§5).** Gemini 3.8 Flash iteratively writes a Python program around the frozen
  model (preprocessing, feature engineering, context-row selection, post-processing, inference
  settings; auxiliary models may be blended). Candidates are scored by three-fold CV inside the
  first outer fold's training split; the search stops after 96 evaluations or six hours, and one
  of the top three programs is refitted and scored on every fold. Full details are deferred to a
  companion paper (Fu et al. 2026, *TabFM-Auto*, not held here).

**Key results** (TabArena, 51 datasets: 38 classification / 594 tasks, 13 regression / 222
tasks; repeated 10-fold CV; Bradley–Terry Elo with Random Forest at 1,000 over a pool of 67
configurations; self-reported):

* **Zero-shot TabFM (Table 2, Fig. 4).** Classification 1,768.6 Elo, level with EXAONE-Tabular
  (1,768.0) and ahead of AutoGluon 1.5 extreme (1,669.7), TabPFN-3 (1,641.9) and TabICLv2
  (1,586.4), with the lowest geometric-mean error (0.0957) and improvability (6.10%) of the
  single-pass models. Regression 2,055.2 against EXAONE 1,973.1, TabPFN-3 1,866.6 and AutoGluon
  1.5 extreme 1,851.2.
* **Pooled (Figs. 1 and 5).** 1,785 Elo, first among default foundation models in the pool;
  fold-level win rates of 65.7% against EXAONE, 72.1% against AutoGluon 1.5 extreme, 75.9%
  against TabPFN-3 and 79.8% against TabICLv2.
* **TabFM+ (Table 2).** +69.4 Elo on classification (1,838.0) and +134.0 on regression (2,189.2).
* **TabFM-Auto (Table 2, Fig. 6).** First on both tracks (1,940.7 and 2,392.4 Elo; +172.1 and
  +337.2 over TabFM). It improves 41 of 51 datasets, including all 13 regression datasets; on
  the ten classification datasets it does not improve, error rises by at most 1.8%. Median error
  reduction is 2.14% when the chosen program changed the table and 0.27% when it did not.

**Strengths.** Turns a blog-level release into a specified model: architecture with a parameter
table, masks, curriculum and tabulated leaderboards with several summary metrics and pairwise
win rates. The context mask gives batch-order-invariant, leakage-free query predictions by
construction. Three deployment tiers (zero-shot, test-time ensemble, LLM program search) are
reported against one pool, so the gain from each kind of extra effort is visible. Weights and
code are public.

**Limitations.** Author-stated (§6): pretraining covers at most 16,384 rows and 100 columns, so
larger tables rely on length generalisation or subsampling; free text is not semantically
encoded; only single flat tables are handled. Reviewer reading:

* **No ablations.** Fourier embeddings, dyadic grouping, untied stages, the curriculum and the
  predictor's depth are motivated but not isolated, and the prior is described only
  qualitatively.
* **Comparison pool.** It includes TabPFN-3 and EXAONE but not TabPFN-3.5, LimiX-2 or Causilo,
  public earlier in September and each reporting a higher TabArena Elo than TabFM ([Jäger 2026,
  *TabPFN-3.5*](#tabpfn-3-5), [Zhang 2026, *LimiX-2*](#limix-2), Cho 2026), nor Mitra-v2, which
  reports a tie. "First among default foundation models" holds for this pool only.
* **Two checkpoints.** The paper's 1.1.0 checkpoint has E = 128 and 408.7M parameters; the June
  1.0.0 configuration has E = 256 and is cited by other reports at 1.64B. The paper does not
  mention 1.0.0 or the change, and its pooled 1,785 Elo differs from the 1,773.5–1,774 that
  Mitra-v2 and LimiX-2 report for "TabFM". Size and latency comparisons in other reports refer to
  the June checkpoint.
* **Outputs.** The abstract says "calibrated", but no calibration metric is reported, and Platt
  scaling appears only in TabFM+. Regression returns a point estimate only, as Klötergens 2026
  and TabReliBench also note. The model card and configuration cap classification at 10 classes;
  the paper does not state the cap.
* **TabFM-Auto protocol.** It needs a proprietary LLM and up to six hours per dataset. Its
  program is selected with labels from the first fold's training split, which contains most of
  the other folds' test rows, so its Elo is not a strictly held-out estimate. Neither TabFM+ nor
  TabFM-Auto is single-pass zero-shot, and the paper reports no inference cost for any tier.
* Unreviewed vendor report; weights are not licensed for commercial use.

---

<a id="test-time-compute"></a>

## 2026-10 — Ning et al. — Test-Time Compute for Tabular Foundation Models: Mechanisms, Gains, and Limits

**Provenance.** arXiv preprint (no venue recorded in Zotero) · arXiv
[2610.12005v1](https://arxiv.org/abs/2610.12005v1) (filed version, 8 October 2026) ·
University of Connecticut / Morgan Stanley · code:
[GitHub](https://github.com/kanghui-learning/test-time-compute-for-tabular-foundation-models),
mirrored in `Test-Time Compute for Tabular Foundation Models.txt` (the
[repository guide](REPOSITORIES.md#test-time-compute-code) maps adaptation, aggregation,
retrieval and evaluation to source files) · **PDF:**
[open](papers/2026/10_Ning_et_al._Test_Time_Compute_for_Tabular_Foundation_Models_Mechanisms_Gains_and_Limits.pdf)

**Citation key:** `2026.NING.testtimecomputetabularfoundationmodelsmechanismsgainslimits`.

**Where it fits.** Revisits [Rubachev 2025, *On Finetuning Tabular Foundation Models*](#on-finetuning) on newer backbones and separates mechanisms that [Thomas 2024, *Retrieval & Fine-Tuning for In-Context Tabular Models*](#localpfn)
combines. It tests how much [Grinsztajn 2026, *TabPFN-3*](#tabpfn-3) gains
beyond its already ensembled default. Here **test-time compute includes supervised
task-specific fitting after pretraining**, not access to unseen query labels.

**What it contains.** The prediction pipeline is factorised into three modifiable
components (§3): **parameters** (adaptation), **member predictions and their reducer**
(aggregation), and **conditioning data** (context construction). Adaptation is studied
on three independently pretrained backbones (TabPFN-3, TabICLv2, and TabFM's June 1.0.0
checkpoint at 1.64–1.65B parameters); aggregation
and context construction in depth on TabPFN-3. The benchmark is the **51 TabArena
datasets** (classification and regression), supplemented by wide and large OpenML
tables (§4).

* **Adaptation (§5).** A 25-setting sweep over which parameters to update motivates
  **DiagScale**: freeze all pretrained weights and learn a zero-initialised diagonal
  multiplier on query–key similarity in every attention module, i.e. logits
  `qᵀ(I + diag(δ))k`, equivalent at the logit level to IA³ key scaling. Only
  **0.003–0.03%** of parameters train; checkpoint selection can fall back to the
  pretrained model.
* **Aggregation (§6).** Compares enlarging TabPFN-3's native ensemble of preprocessing
  views with a broader pool of **96 configurations** reduced either by uniform averaging
  or by greedy (Caruana-style) selection on training-side out-of-fold predictions.
* **Context construction (§7).** *Curation*: attention-guided row retrieval (scored
  within blocks, so pools can exceed the memory limit) and column selection, each
  against matched random controls. *Expansion*: synthetic or optimised rows,
  pseudo-labelled rows and derived features.
* **Composition and cost (§8).** Combines interventions and reports total fitting plus
  prediction GPU-hours over the 51-dataset workload.

**Key results.**

* **DiagScale ≈ full finetuning (Table 2).** Trainable parameters on the regression
  checkpoints: 12.7K (TabPFN-3), 7.3K (TabICLv2), 53.8K (TabFM). Elo gains over each
  frozen backbone: **+26 / +82 / +20**, versus **+25 / +77 / +28** for full finetuning.
* **Native views saturate (§6, Fig. 3A).** Going from 8 to 32 views reduces error by
  only **0.60%** (+21 Elo), with little more at 64.
* **Selection beats averaging (§6).** On the 96-configuration pool, greedy selection
  reduces error by **2.44%** (95% CI −4.75% to −0.80%; **+67 Elo**; better on 42/51
  datasets), whereas uniform averaging *increases* it by **3.68%**. Giving the selector
  only one eighth of the training-side labels erases the gain (error 0.4% above default).
* **Combination and cost (§8, Fig. 5).** DiagScale + greedy aggregation reaches **+93
  Elo** at **253.1 GPU-hours**, versus 6.61 for DiagScale alone, 247.5 for aggregation
  and 1.66 for 32 native views. DiagScale's fitting time is close to full finetuning's
  despite far fewer trainable parameters. **Frozen TabFM** achieves a higher Elo than
  the fully adapted-and-aggregated TabPFN-3 at 19.3 GPU-hours.
* **Retrieval helps or fails (§7).** Retrieval extends usable pools to **10M rows**,
  beyond the 4.0–4.5M full-context limit on one 80 GB GPU (e.g. −3.5% log loss on Higgs
  versus 4M-row full context). On **COMET_MC** it raises log loss from **0.0151 to
  0.2302**: a 1.7% rare class makes up a median 40.3% of retrieved contexts, and
  correcting proportions only partly repairs it (0.1270). Context-expansion methods
  give no consistent gain.
* **Gains are concentrated and unpredictable (§8).** The five largest per-dataset
  reductions account for 46–70% of the positive total; 21 dataset predictors reach at
  best cross-validated R² 0.012 for forecasting the gain.

**Strengths.** Separates parameter, ensemble-reducer and context effects with matched
controls; reports uncertainty, negative results, validation-label sensitivity and total
fitting/prediction costs. Tests a compact adaptation mechanism across three independently
pretrained backbones and both task types rather than treating v2 conclusions as universal.
Code is linked from the paper, and the appendix specifies splits and reference predictions.

**Limitations.** Unreviewed, benchmark-bound evidence: aggregation/retrieval results are
not established for every backbone or for temporal/grouped evaluation. Learning-rate
defaults are selected across the benchmark; three diagnostic datasets motivate the
similarity mechanism. Elo depends on the reference field, and reported error reductions
combine different task metrics, not a common absolute accuracy gain. Benefits concentrate
on a few datasets and cannot yet be predicted per dataset (authors' own conclusion).
The frozen-TabFM comparison shows that extra compute on a fixed backbone is not always
the best purchase. The retrieval failure and context-expansion null
results constrain the tested recipes; they do not prove all retrieval or learned-context
methods ineffective, nor do these experiments establish probability calibration.

---

<a id="tabrelibench"></a>

## 2026-10 — Zhao et al. — TabReliBench: Evaluating Tabular Foundation Models Beyond Predictive Accuracy

**Provenance.** arXiv preprint · arXiv [2610.13654v1](https://arxiv.org/abs/2610.13654v1)
(filed version, 9 October 2026) · Renmin University of China, Cerebras Systems, National
University of Singapore, MBZUAI · code stated as available via a link in the abstract (URL
not recoverable from the text extraction) · **PDF:**
[open](papers/2026/10_Zhao_et_al._TabReliBench_Evaluating_Tabular_Foundation_Models_Beyond_Predictive_Accuracy.pdf)

**Citation key:** `2026.ZHAO.tabrelibenchevaluatingtabularfoundationmodelspredictiveaccuracy`.

**Where it fits.** The synthesis has long listed calibration as the paradigm's most glaring
evaluation gap — claimed everywhere because a PFN approximates a posterior predictive, measured
almost nowhere. Scattered evidence existed: Brier score, log loss and a portfolio-level mean-bias check in
[Baesens et al. 2026, *Tabular Foundation Models for Credit Risk Prediction: A Dedicated Review and Empirical Comparison*](#credit-risk-benchmark),
CRPS in [Cho et al. 2026, *Causilo*](#causilo), ScoringBench results in the
[EXAONE](#exaone-tabular-1) and [TabPFN-3.5](#tabpfn-3-5) reports. TabReliBench is the first paper
here built *for* the question, across eleven TFMs at once, and it separates what a single proper
score blends together: accuracy, calibration, marginal coverage, subgroup coverage and interval
width. It also tests the founding promise of
[Müller et al. 2021, *Transformers Can Do Bayesian Inference*](#pfns-2021) — that calibration
falls out of the objective — and finds it true on average and false locally.

**What it contains.** A benchmark of **160 classification and 81 regression** OpenML datasets
(§2), each with five train–test repetitions of at most 10,000 sampled rows split roughly
half/half, so every model stays in its operating regime. **Eleven TFMs** — TabPFN v2, 2.5, 3
and 3.5; TabICL v1 and v2; TabDPT 1.1 and 1.3; Causilo; LimiX-2; TabFM 1.0.0 — are compared with BART
and with fixed and tuned RealMLP and XGBoost. All 11 TFMs enter classification; TabICLv1 and
TabDPT 1.1 are classification-only, leaving **9 regression TFMs**, and LimiX-2 and TabFM give no
regression predictive distribution, leaving **7 distributional TFMs**. Each dataset–model pair
gets a profile over five properties (Table 1): point prediction (accuracy, R²), proper score
(Brier, CRPS), marginal calibration (confidence ECE; PIT–KS and 90% marginal coverage),
classwise/subgroup calibration (classwise ECE; **worst-slab coverage**, i.e. coverage on the
worst-covered covariate slab) and interval width. The main runs fix each TFM's inference
ensemble at **E = 8**; an ensemble study varies E ∈ {1, 4, 8, 16, 32}, and a post-processing
study applies **nine conformal methods** (four global split-conformal, five covariate-adaptive)
to the E = 8 predictions. Treating the dataset as the unit of analysis, a variance
decomposition and meta-feature regressions ask *where* reliability varies.

**Key results.**

* **Rankings move (§3.1, Fig. 1).** Orderings differ between TabArena and TabReliBench and
  across metrics: LimiX-2 has the best mean rank for accuracy and R², TabPFN-3.5 for Brier,
  classwise ECE and CRPS, Causilo for confidence ECE and the regression calibration metrics.
  TFMs still dominate the baselines: all 11 rank ahead of every baseline on accuracy and
  Brier (all but TabDPT 1.1 on both ECEs), all 9 on R², and all 7 on CRPS and the four
  regression calibration diagnostics.
* **Marginal coverage masks local gaps (§3.2).** Regression TFMs usually reach near-nominal
  90% marginal coverage with narrow intervals, but worst-slab coverage stays heterogeneous
  and often poor.
* **Dataset-level structure (§3.3–4).** Most score variation lies between datasets rather than
  between TFMs. Local class overlap is a warning sign for both accuracy (ρ = −0.78 with
  neighbourhood disagreement) and confidence ECE (ρ = 0.64); in regression, predictive
  performance is not a reliable indicator of calibration.
* **Ensembling (§5.1).** From E = 1 to 32, median accuracy and Brier improve for all 11
  classification TFMs and CRPS for all 7 distributional TFMs, mostly by E = 4–8; but
  classwise ECE improves for only 5 of 11 and PIT–KS for 3 of 7, and median R² falls for
  TabPFN-3.5, 3 and 2.5.
* **Conformal post-processing (§5.2, Fig. 8).** Marginal correction helps BART (which starts
  over-covered) far more than TFMs, and no global or covariate-adaptive method consistently
  removes worst-slab undercoverage.

**Strengths.** Exactly the study the paradigm's selling point required and had not received.
Separating marginal from worst-slab coverage is the methodological contribution that matters
most: a model can be perfectly calibrated on average while systematically under-covering a
subgroup, which is what subgroup-sensitive applications and fairness analyses care about.
Using the dataset as the unit of analysis, with enough datasets to make
that meaningful, is a real advance over leaderboard averaging. Comparing eleven current TFMs in
one harness also makes it the broadest independent cross-model comparison in this collection.

**Limitations.** The authors note that worst-slab coverage does not guarantee pointwise
conditional coverage, and that conclusions are bounded by the chosen datasets, configurations
and criteria. The 10,000-row cap leaves the large-data regime — where TabPFN-3.5 and TabICLv2
make their strongest claims — untested. The distributional comparison covers only seven TFMs
(two of the eleven are classification-only and two more emit no regression distribution). The
data are i.i.d. OpenML splits, so how reliability — especially subgroup coverage — behaves under
the temporal and grouped shifts of [Beyond IID](#beyond-iid) is an open question. It is a
preprint.

---

<a id="effectively-shallow"></a>

## 2026-10 — Cannistraci and Vogt — Tabular Foundation Models Are Effectively Shallow

**Provenance.** arXiv preprint · arXiv [2610.13253v1](https://arxiv.org/abs/2610.13253v1)
(filed version, 9 October 2026) · ETH Zurich · code on
[GitHub](https://github.com/icannistraci/shallow-tfm) · **PDF:**
[open](papers/2026/10_Cannistraci_and_Vogt_Tabular_Foundation_Models_Are_Effectively_Shallow.pdf)

**Citation key:** `2026.CANNISTRACI.tabularfoundationmodelsareeffectivelyshallow`.

**Where it fits.** A compression paper with a theoretical edge. On the deployment side it joins
[Luo et al. 2026, *Memory Efficient Tabular Foundation Models*](#memory-efficient-tfms), which
shrinks the *bits* per parameter: this paper removes the *parameters*, and the two compose. On
the conceptual side it supplies the cleanest evidence yet for what three other papers argued
from different directions —
[Nagler 2023, *Statistical Foundations of Prior-Data Fitted Networks*](#nagler-theory) (bias
vanishes only under localisation),
[Zheng et al. 2025, *From Tables to Signals*](#spectral-adaptivity) (attention sharpens into
local neighbourhoods) and
[Shaheen et al. 2026, *Understanding the Surprising Generalization Properties of Tabular
Foundation Models*](#shaheen-retrieval) (the learned procedure is retrieval-and-aggregation).
A retrieve-and-pool procedure does not need twenty-four layers of nonlinear composition, and
this paper measures that it does not use them.

**What it contains.** The tool is a **closed-form, label-free affine translator** (§3). For a
contiguous window of transformer blocks, a ridge regression fitted on hidden states from one
forward pass over the support set plus unlabelled calibration queries (at most 500 positions)
maps the state *entering* the window to the state *leaving* it; at inference the window is
skipped and the remaining blocks and original head run unchanged. The window is chosen
label-free by minimising forward KL between the full and compressed models' output
distributions on the calibration split; with a KL tolerance the same rule also chooses *how
many* blocks to replace. Single-axis models (TabPFN-3, TabICL, TabDPT, TabFM, Orion) get one
shared map; dual-axis models (TabPFN v2, LimiX) get one map per feature index. At a network
boundary the map folds into the adjacent linear layer, leaving a plain k-block model. If outputs
survive, the bypassed blocks did work a linear map can absorb. The study covers **8 TFMs from 6
families on 171 classification datasets** (163 from OpenML-CC18, TabZilla, TabArena and
Grinsztajn plus eight clinical sets), a 41-dataset regression study, and a controlled
nanoTabPFN experiment (Pfefferle et al. 2025, *nanoTabPFN*, not held here).

**Key results.**

* **Half depth is near-lossless (§5.1).** Replacing half the blocks costs at most **0.002 median
  AUROC** for every architecture, with up to 97% of datasets within one point; half-depth TabFM
  still beats every other *full-depth* TFM and tuned GBDTs (abstract).
* **One block often suffices for classification.** TabPFN-3, Orion-BiX and TabICL stay within a
  median 0.007 AUROC with one block kept. Overall the translator replaces **up to 96% of
  blocks**, removing up to **1.5B parameters** (TabFM's 1.64B June checkpoint), with up to **6×** faster end-to-end GPU
  inference at a median cost of 0.03 AUROC; a one-block TabPFN-3 serves cached queries **2.4×
  faster with 6.1× less memory** (§6, Table 1: MIMIC-III on one RTX 5090).
* **Where depth lives differs by family (§4).** TabPFN-3 leans on its encoders and survives
  whichever single block is kept; other single-axis models need only their first block;
  dual-axis models concentrate work in one critical block. Representation-similarity and
  attention signals correspond only inconsistently with actual replaceability.
* **The map does real work.** Dropping blocks without it collapses the model; a supervised
  early-exit head loses ≈0.02 AUROC and is matched or beaten by the label-free translator in
  81% of 2,664 configurations (Table 16).
* **Regression (§5.2, 41 datasets, Fig. 6).** Half depth costs only 0.001–0.026 median R², but
  with one block kept most regressors degrade sharply (TabPFN-3 −0.132 R²; TabFM the exception at
  −0.022): predictions shrink toward the mean and rankings worsen (Spearman 0.91 → 0.57 for
  TabDPT), so late blocks refine output ordering.
* **Compression ≈ shallow training (§7, Fig. 7).** On a 1.4M-parameter nanoTabPFN, a 12-block
  model compressed to k blocks matches one trained at depth k within 0.011 AUROC, but only when
  the map is fitted on the target's rows (fitting on prior tasks drops AUROC to 0.43–0.83); a
  natively trained 6-block model matches the 12-block one.

**Strengths.** Intervention rather than observation: instead of inferring redundancy from
representation similarity or attention maps — which the paper shows correspond inconsistently
with actual replaceability — it removes the blocks and measures. The translator is closed-form
and label-free, so it costs almost nothing and needs no downstream labels, which is what makes
it usable in the privacy-constrained settings the paper motivates. Breadth (eight models, six
families) turns a curiosity into a property of the paradigm. And the per-family diagnosis of
*where* depth lives is new information about architectures that the model papers themselves
never report.

**Limitations.** The main 171-dataset study is classification scored by AUROC — a ranking
metric that is blind to calibration, which [Zhao 2026, *TabReliBench*](#tabrelibench) shows
can vary independently of ranking metrics (reviewer reading; calibration of compressed models is
not reported). Author-stated: single-block compression fails to preserve continuous target
rankings in regression; for dual-axis models whose map cannot be absorbed (LimiX-16M) the
per-feature map outweighs the removed blocks on very wide tables; and the compression-equals-
shallow-training result is shown only on a 1.4M-parameter nanoTabPFN, with production scale
explicitly open. The translator needs unlabelled target rows at deployment. It is a preprint,
and a closely related ICML 2026 study (Balef et al., *Is one layer enough?*, not in this
collection) reached a neighbouring conclusion.

---

<a id="survicl-a-foundation"></a>

## 2026-10 — Alberge et al. — SurvICL: a Foundation Model for in-context Survival Analysis

**Provenance.** arXiv preprint (no venue recorded in Zotero) · arXiv
[2610.22242v1](https://arxiv.org/abs/2610.22242v1) (filed version, 15 October 2026) · Inria
Saclay, with EPFL and Probabl affiliations · code and models stated as released (§7), no
URL in the PDF text · **PDF:**
[open](papers/2026/10_Alberge_et_al._SurvICL_a_Foundation_Model_for_in_context_Survival_Analysis.pdf)

**Citation key:** `2026.ALBERGE.surviclfoundationmodelincontextsurvivalanalysis`.

**Where it fits.** Extends [Qu 2026, *TabICLv2: A better, faster, scalable, and open tabular foundation model*](#tabiclv2) to **right-censored time-to-event
prediction**. Like Robertson 2025 (*Do-PFN*), it uses simulator-accessible outcomes
that real observations do not reveal: the context remains censored, while synthetic
query targets are uncensored event times. Its controlled prior ablations complement
[Bouadi 2026, *O'Prior*](#oprior). It also broadens the distributional evidence
alongside [Zhao 2026, *TabReliBench*](#tabrelibench), while evaluating a
different form of calibration.

**What it contains.** A TabICLv2-style backbone is pretrained specifically for survival
analysis. Context outcomes encode **observed duration plus event/censoring indicator**
at both the cell-embedding and row-ICL stages. A softplus head predicts **999 positive
event-time quantiles** using plain pinball loss against latent event times; sorting
and interpolation produce a monotone survival function. Thus the simple loss depends
on synthetic supervision, rather than treating censored durations as observed events.
The architecture retains TabICLv2's repeated feature grouping, row compression and
`O(n² + nm²)` attention cost; inference averages eight preprocessing/permutation views.

The synthetic prior combines SCM covariates with a **proportional-odds survival model**:
a flexible random baseline hazard and covariate-dependent risk generate event times,
with a separately drawn censoring mechanism plus administrative study-end censoring.
The generator filters out tables with over 95% censoring and tables without exploitable
predictive signal. Pretraining uses **200,000 steps**, 1,024-row tables with at most
100 features, and about **72 hours on two H100s**. It omits TabICLv2's later scaling
stages.

The benchmark has **103 datasets: 40 for development and 63 held out from design
decisions**, compared against **20 baselines** including four earlier survival TFMs
(SurvPFN, SurvivalPFN, Survival-IC, TFM4Survival; Table 1). Each held-out dataset
receives ten event-stratified 80/20 train/test splits. SurvICL uses at most **4,096
context rows** without per-dataset tuning; test sets are also capped at 4,096. Tunable
baselines receive up to 50 random-search trials, with their seed-0 choice reused across
splits.

**Key results.**

* **Overall (§6, Figs. 1 and 4).** On the 63 held-out datasets SurvICL's pairwise **IBS
  win rate is 82.9%**, versus 71.3% for the runner-up Cox model (difference statistically
  significant); for the median-horizon IPCW C-index it is **77.7%**, versus 71.6% for random
  survival forests. These rates aggregate comparisons over datasets and all competitors,
  not head-to-head rates against the runner-up. All earlier survival TFMs trail classical
  methods.
* **By dataset size.** On datasets under 1,000 samples (69.8% of the held-out set) SurvICL
  is the first model to rank above Cox in IBS (84.9% vs 77.2%), not statistically
  significant (Figs. 22–26). Above 1,000 samples SurvivalBoost is clearly best in IBS (86.9%
  win rate); SurvICL ranks second in average IBS and first in C-index.
* **Calibration and time error.** Average **KM-calibration** rank (mean predicted survival
  curve versus the test Kaplan–Meier curve) is 6.0, behind KM itself (4.3), Cox (5.0),
  DeepSurv (5.6) and sksurv GBS-Cox (5.9); KM and Cox's Breslow baseline enforce this
  calibration by construction. MAE is close to Survival-IC and slightly behind SurvivalPFN,
  not significantly.
* **Runtime.** On the Pareto front for C-index and IBS in all size regimes; reported
  baseline runtime excludes hyperparameter search.
* **Prior ablation (Fig. 4c; development set, shallower model trained 10K steps).** With the
  architecture fixed, the PO prior beats Cox (77.6), mixed (84.0), SurvPFN (79.0),
  SurvivalPFN (82.7) and Survival-IC (83.7) priors; a censoring-time head hurts (81.0). The
  final model keeps 999 quantiles despite a small ablation edge for 99 (88.5 vs 87.2).

**Strengths.** Preserves censored information in context while exploiting simulator
ground truth for training; separates survival targets, prior design and backbone
reuse. The 40/63 development/evaluation split reduces dataset-level design leakage,
and the benchmark reports probability error, ranking, time error, calibration and
runtime separately. Reports the large-dataset reversal, statistical qualifications
and failed-baseline handling rather than relying on a single overall leaderboard.

**Limitations.** Unreviewed evidence restricted to right-censored, single-event,
static-covariate data; competing risks and time-varying covariates remain future work.
Random event-stratified splits do not establish temporal or grouped transfer. Reusing
seed-0 baseline tuning overlaps later splits' test observations, a limitation the
authors acknowledge as favouring baselines. Failed baseline fits are assigned IBS 1
or C-index 0.5 on affected datasets, so aggregate ranks partly reflect robustness of
the implementations. The 4,096-row context cap and 1,024-row pretraining regime limit
claims about large cohorts; prior rankings from shallow, short ablations need not hold
unchanged at full scale. IBS assesses probability quality and KM-calibration assesses
an average curve: neither establishes individual or subgroup calibration. Finally,
latent event times are unavailable for censored real observations, so plain pinball
training here does not by itself supply a valid real-data finetuning or continued-
pretraining objective.

---

<a id="is-tabpfn-the"></a>

## 2026-10 — Deprez et al. — Is TabPFN the Silver Bullet for Insurance Pricing?

**Provenance.** arXiv preprint (q-fin.RM) · arXiv
[2605.22892v3](https://arxiv.org/abs/2605.22892v3) (filed version, 9 October 2026; first
posted May 2026 per Zotero) · KU Leuven and University of Antwerp-imec · evaluation code on
[GitHub](https://github.com/B-Deprez/tabpfn_insurance) · **PDF:**
[open](papers/2026/10_Deprez_et_al._Is_TabPFN_the_Silver_Bullet_for_Insurance_Pricing.pdf)

**Citation key:** `2026.DEPREZ.tabpfnsilverbulletinsurancepricing`.

**Where it fits.** A short domain evaluation: whether default TabPFN can replace the
generalised linear models (GLMs) and gradient boosting that dominate non-life insurance
pricing. It complements broad leaderboards such as [Purucker 2026, *Beyond IID*](#beyond-iid)
and the credit-risk benchmark of [Baesens 2026, *Foundation Models for Credit Risk
Prediction*](#credit-risk-benchmark) by asking whether a generic regression win carries over
to a problem with actuarial structure — exposure offsets, sparse claim counts,
heteroskedastic severities and distribution-specific losses — and to latency-bound quoting.

**What it contains.** The technical price is decomposed into claim **frequency** (claims per
unit exposure) and **severity** (average claim amount) (§1). TabPFN v2.6 (alternating
row/feature attention, up to 100,000 context rows) and TabPFN v3 (row compression, up to 1M
rows below 200 features) are used with defaults on raw inputs, against a Poisson/gamma GLM and
XGBoost with fixed hyperparameters from earlier actuarial work (depth 3, 500 trees), no
dataset-specific tuning (§2–3). Data: French **freMTPL2** (~678,000 policies) and Belgian
**beMTPL97** (~163,000) motor third-party-liability sets, 5-fold cross-validation.

Because TabPFN supports neither offsets nor observation weights, exposure enters as an
**input feature** with the claim count as target, predictions being evaluated at a full year
of exposure; GLM and XGBoost use log-exposure as an offset. For severity, the baselines are
weighted by claim count while TabPFN is unweighted and fitted on ln(1 + y) with its built-in
target transform. Metrics: exposure-weighted RMSE, Poisson deviance (frequency), claim-
weighted gamma deviance (severity) and per-fold time. Frequency contexts are subsampled to
2,000–100,000 policies (plus the full ~542,000-row fold for v3); severity folds (~20,000 and
~14,600 claims) are used in full.

**Key results.**

* **Frequency (Table 1, Fig. 1).** The GLM is best on both metrics and both datasets
  (Poisson deviance 0.296 French, 0.551 Belgian). TabPFN's RMSE is close to the baselines
  and barely moves with context size, but its deviance is worse and context-sensitive:
  v3 on French data improves steadily from 0.363 (2,000 rows) to 0.343 (full fold), roughly
  matching XGBoost (0.344); v2.6 is non-monotonic (0.356 → 0.383 → 0.379). On Belgian data
  v2.6 beats XGBoost (≈0.563–0.568 vs 0.583) while v3 is worst (≈0.63).
* **Severity (Table 2, Fig. 2).** Competitive: on French data XGBoost has the best gamma
  deviance (1.598), then v2.6 (1.654), with the GLM worst (1.755) and large fold variance
  driven by one outlier fold; on Belgian data v3 is best (2.041 vs GLM 2.046).
* **Runtime (Fig. 3).** TabPFN's inference time grows steeply with context and exceeds the
  GLM's and XGBoost's combined training-plus-inference time even at small contexts, reaching
  minutes per fold at capacity; v3 is much faster than v2.6.
* **Conclusion (§5).** TabPFN is not yet a replacement for actuarial frequency models, but is
  competitive where data are scarce (severity).

**Strengths.** Uses the actuarially relevant losses (Poisson and gamma deviance) rather than
RMSE alone, and shows they can disagree; separates frequency from severity and maps
performance and runtime against context size. Documents concretely why a generic TFM
interface (no offsets, no weights, mean of a discretised predictive distribution) is a
modelling handicap, not just a missing feature. Public datasets and linked code make it
reproducible.

**Limitations.** Author-stated (§5): two datasets, two TabPFN versions, no fine-tuning, no
downstream premium or profitability analysis, and no comparison of learned risk drivers.
Reviewer reading: TabPFN v2.6 sees at most 100,000 of ~542,000 French training policies while
the baselines see all of them; XGBoost is untuned, so the baselines are not strong
machine-learning references; exposure as a feature is not equivalent to an offset, so part
of the frequency gap reflects the interface rather than the model; and only predictive means
are scored, not TabPFN's distributional output. The licence point (non-commercial weights for
v2.6 and v3 at the time of writing) describes those releases, not every future version.

---

<a id="tile-bridging-llms"></a>

## 2026-10 — Lefebvre et al. — TILE: Bridging LLMs and Table Foundation Models for Tabular Learning with Strings

**Provenance.** arXiv preprint · arXiv [2610.17065v1](https://arxiv.org/abs/2610.17065v1)
(filed version, 12 October 2026) · SODA team, Inria Saclay (with SAP SE and Probabl
affiliations) · no official code repository found · **PDF:**
[open](papers/2026/10_Lefebvre_et_al._TILE_Bridging_LLMs_and_Table_Foundation_Models_for_Tabular_Learning_with_Strings.pdf)

**Citation key:** `2026.LEFEBVRE.tilebridgingllmstablefoundationmodelstabularlearningstrings`.

**Where it fits.** The semantics strand of this collection has so far built *string-aware
TFMs*. [Arazi 2025, *TabSTAR: A Tabular Foundation Model for Tabular Data with Text Fields*](#2025-12--arazi-et-al--tabstar) and [Spinaci 2025, *ConTextTab: A Semantics-Aware Tabular In-Context Learner*](#2025-12--spinaci-et-al--contexttab)
do this end to end with small text encoders. [Kim 2024, *CARTE: Pretraining and Transfer for Tabular Learning*](#carte-pretraining-and) does it through knowledge-pretrained
graphlets. TILE leaves the TFM untouched and instead redesigns the **interface** through
which a frozen decoder LLM supplies features to it. It complements [Arazi 2026, *MulTaBench*](#multabench-benchmarking-multimodal), which shows that
task-tuned rather than frozen encoders win on its selected tasks: TILE gets large gains
from a *frozen*, label-free LLM by changing what the LLM sees and which layer is read. It
benefits directly from each new TFM generation, including [Jäger 2026, *TabPFN-3.5*](#tabpfn-3-5), [Eo 2026, *EXAONE Tabular 1.0*](#exaone-tabular-1) and
[Cho 2026, *Causilo*](#causilo).

**What it contains.** Four design choices (§3, Fig. 2):

- **Row serialisation** ("The ⟨column⟩ is ⟨value⟩." for every column) lets each string
  attend to its header and the rest of the row. An ambiguous cell such as "E.T." becomes
  identifiable next to "Spielberg".
- **Intermediate-layer extraction** reads one fixed middle layer (layer 14 of 32 for
  Llama-3.1-8B). Only the layers up to that point are loaded.
- **Columnar pooling** averages token embeddings within each string column's span instead
  of over the whole sentence, removing the length bias of global mean pooling. Each column
  is then standardised and gets its own PCA, sized to the TFM's preferred feature-count
  window.
- **By-pass features** pass numerical columns, low-cardinality categoricals and
  out-of-fold target encodings directly to the TFM alongside the embeddings.

The TFM then predicts in one forward pass.

Evaluation uses **100 string-carrying tables** (65 regression, 35 classification) from
TextTabBench, CARTE and WikiDBs (five seeds; training sizes 1,024 / 10k / 50k) against
**30 baselines**, including cell-wise LLM encoders, TF-IDF, tuned GBDTs and end-to-end
string-aware models (ConTextTab, TabSTAR, TabLLM, CASE).

**Key results.**

At 1,024 training rows, TILE with Causilo scores 91.6 (regression) and
90.4 (classification) normalised points against 77.8 and 81.0 for the best Table 1
baseline, the same LLM applied cell-wise + Causilo. In Elo it leads the strongest
baseline (cell-wise LLM + EXAONE-Tabular) by **+333** and wins 88.6% of the 500 shared
splits (Appendix B). The regression gap narrows with more data (13.8 → 9.1 → 7.3 points).
TF-IDF features fed to a TFM roughly match the cell-wise 8B LLM and beat end-to-end
ConTextTab, TabSTAR and TabLLM.

On the separately assembled **STRABLE** benchmark (108 tables, 51 baselines; Blayer 2026,
*STRABLE: Benchmarking tabular machine learning with strings*, not held here), the four
TILE variants take the top four places. TILE + Causilo scores 1.024, i.e. above choosing
the best baseline per dataset (§4.3, Fig. 3). With row context, larger LLMs help. TILE's
lead over the cell-wise encoder grows from 4.2 points with Qwen3-0.6B to 16.7 with
Qwen3-8B, whereas cell-wise Qwen3-0.6B beats Qwen3-8B (§5.1, Fig. 4).

Ablations (§5.4, Table 2) attribute most of the gain to the numerical by-pass (removing it
costs 11–15 points) and inter-column attention (3–9 points). Reading the last rather than
the middle layer costs up to 3.6 points; adding the target name to the prompt, repeating
the row, uninformative column names and mirrored column order all hurt. TILE runs at a
median 26–45 s per dataset and peaks at 8.7 GB GPU memory against 16.0 GB for the
cell-wise encoder (Appendix G).

**Strengths.** Turns a vague practice ("use an LLM to embed strings") into a controlled
design space with ablations for each choice, two LLM families across two orders of
magnitude, ten downstream learners and an external benchmark assembled by different
authors. Its gains survive across TFM generations rather than being tied to one backbone.
The cell-wise LLM baseline shares the same backbone, isolating the interface. The
TF-IDF result is an honest, useful baseline for anyone adding semantics to a TFM.

**Limitations.** No official code repository is linked from the paper or its arXiv
record, and none was found under the authors' GitHub organisation on 2026-10-26. Results
therefore rest on the paper's description of a pipeline built from public components
(Appendix I). The extraction layer, feature-count window and cardinality threshold were
chosen on the main benchmark. STRABLE provides partial independent confirmation, but 15
of its tables share sources with the main benchmark. Possible LLM memorisation of
Wikidata- or web-derived entities is not audited, which matters for a method whose gains
come from world knowledge. The decoder's causal mask makes features depend on column
order. A GPU is required for the LLM stage, and very wide or text-heavy rows need
chunking beyond the context window. End-to-end baselines run with package defaults.
CASE uses a fallback backbone because its tuned checkpoint is unreleased. Gains are
largest at small training sizes.

---

<a id="credit-risk-benchmark"></a>

## 2026-10 — Baesens et al. — Tabular Foundation Models for Credit Risk Prediction: A Dedicated Review and Empirical Comparison

**Provenance.** arXiv preprint; no publication venue recorded in Zotero · arXiv
[2605.18147v3](https://arxiv.org/abs/2605.18147v3) (filed version, 23 October 2026; first
released May 2026) · **v3 retitled the paper** (v1/v2: *Foundation Models for Credit Risk Prediction: A Game Changer?*) and is a major revision: the 25-page v2 (15 July
2026) becomes a 66-page invited review with a re-run benchmark, and the author order changes
(Baesens, Goethals, De Vos, Bravo, Lessmann, Martens, Medina-Olivares, Mues, Óskarsdóttir, vanden
Broucke, Van Gestel, Verdonck, Verbeke). Zotero, heading, filename and citation key follow the v3 title · KU Leuven-led collaboration with seven further universities and
Dexia · benchmark built on the TALENT framework; evaluation, statistics and figure code at
[andreasgoethals/TabPFNCredit](https://github.com/andreasgoethals/TabPFNCredit) (v2 named no
code release); the proprietary datasets are not released · **PDF:**
[open](papers/2026/10_Baesens_et_al._Tabular_Foundation_Models_for_Credit_Risk_Prediction_A_Dedicated_Review_and_Empirical_Comparison.pdf)

**Citation key:** `2026.BAESENS.tabularfoundationmodelscreditriskpredictiondedicatedreviewempiricalcomparison`.

**Where it fits.** A domain benchmark in the tradition of large credit-scoring comparisons, now
framed by a review of the PFN line (Bayesian foundations, architecture lineage, prior design)
written for a credit-risk audience. It asks whether untuned TFMs transfer to probability of
default (PD, classification) and loss given default (LGD, bounded regression), and — new in v3 —
how their advantage changes with sample size and with the rarity of defaults. It evaluates
[Grinsztajn 2026, *TabPFN-3*](#tabpfn-3) and [Qu 2026, *TabICLv2*](#tabiclv2) on domain data
from outside their developer teams. It complements [Tanna 2026, *Data Presentation Over
Architecture*](#tanna-resampling) on context construction for imbalanced credit data and
[Deprez 2026, *Is TabPFN the Silver Bullet for Insurance Pricing?*](#is-tabpfn-the) as another
domain stress test. It also qualifies any broad reading of [Purucker 2026, *Beyond
IID*](#beyond-iid): strong cross-validated results here do not address temporal or grouped
generalisation.

**What it contains.**

* **Review (§2–3, Table 1).** Credit-risk modelling and deep tabular learning; PFN theory,
  TabPFN, later architectures and pretraining-data design; Table 1 compares nine PFNs by task
  support, prior, ICL architecture and reported row/feature limits.
* **Data (§4.2, Table 2).** **14 PD and 7 LGD datasets**, public and proprietary (two PD, five
  LGD), retail and small-business. PD default rates range from 6.7% to 40.0% (mean ≈22.1%); LGD
  sets range from 594 to 58,862 observations and show the bimodal, zero-one-inflated target
  (Fig. 1).
* **Methods and protocol (§4.3–4.4, Table 3).** **33 PD and 27 LGD methods**, counts that include
  the TFMs: nine for PD (TabPFN v1, TabPFNv2, TabPFN-2.5, TabPFN-3, Real-TabPFN, TabICL,
  TabICLv2, TabDPT, Mitra) and six for LGD (TabPFNv2, TabPFN-2.5, TabPFN-3, TabICLv2, TabDPT,
  Mitra). TFMs run in their default in-context configuration; tunable learners get 20 Optuna
  trials per fold on a 20% validation split. Five-fold cross-validation with fold-wise TALENT
  preprocessing; tables with more than 99 retained features are reduced to at most 99 principal
  components fitted on the training fold; TFMs receive the processed inputs without external
  standardisation, and method-specific caps apply only to the training context. LGD targets and
  predictions are clipped to [0, 1].
* **Metrics and statistics (§4.4, App. A–B).** Primary metrics are AUC (PD) and R² (LGD);
  Appendix B adds Gini, KS, adjusted AP, Brier score, log loss and F1-thresholded measures for
  PD, and MSE, RMSE, MAE, MedAE, maximum error and correlations for LGD. A new portfolio-level
  **mean-bias check** compares observed and mean predicted PD/LGD per dataset (§5.1.1). v2's
  Holm-corrected Wilcoxon tests are replaced by Friedman (Iman–Davenport) tests, Nemenyi critical
  differences and Shaffer-adjusted pairwise p-values, a Bayesian signed-rank test with a ±0.01
  region of practical equivalence, win/loss matrices and an exploratory panel of family
  champions.
* **Auxiliary experiments (§4.5, App. F.2).** Nested, fixed-seed subsampling with HPO disabled,
  comparing TabPFN-3 and TabICLv2 with CatBoost and logistic/linear regression: (i) learning
  curves from 30,000 to 100 PD rows (nine datasets) and from 4,600 to 100 LGD rows (four
  datasets); (ii) a PD class-imbalance sweep lowering the default rate from 0.15 to 0.0025 on six
  datasets. Both subsample natively large portfolios.
* **Pretraining-overlap audit (App. F.3, Table F.2).** Real-TabPFN's corpus contains Vehicle
  Loan; TabDPT's contains reduced versions of GMSC and Taiwan Credit Card; no LGD dataset
  overlaps. Descriptive checks show no advantage on the overlapping datasets.
* **Management implications and research directions (§6).** Governance, validation and
  ecosystem consequences, plus an agenda on mechanisms, negative transfer, context design,
  calibration, and survival, fairness and causal extensions.

**Key results.**

* **PD (Fig. 2, Table B.1).** TabPFN-3 has the highest mean AUC (**0.7644**), followed by
  TabICLv2 (0.7597), TabPFN-2.5 (0.7572) and TabICL (0.7526); the best conventional learner is
  CatBoost (0.7496). Mitra (0.7232) and TabPFN v1 (0.7031) rank among the weakest. TabPFN-3 is
  also best on every discrimination measure and on Brier score/log loss (0.1251/0.3886).
* **LGD (Fig. 3, Table B.2).** TabPFN-3 leads on R² (**0.5366**), followed by TabPFN-2.5 (0.5305)
  and TabICLv2 (0.5298); CatBoost is fourth (0.4872) and TabDPT fifth (0.4809). Mitra is the
  weakest method (0.1656). TabPFN-2.5 has the lowest MAE, ModernNCA the lowest MedAE.
* **Fold wins (PAMA; Figs. 4–5).** TabPFN-3 wins 35.7% of PD folds (25/70) and TabICLv2 30.0%
  (21/70); CatBoost 5.7%. TFMs as a group win 81.4% of PD folds and 74.3% of LGD folds, where
  TabPFN-3 wins 34.3% (12/35) and ModernNCA is the best conventional learner (14.3%).
* **Significance (App. A).** Friedman tests reject equal performance (PD F_F = 10.32, LGD 8.64),
  but full-panel Shaffer corrections flag only 61 of 528 PD and 24 of 351 LGD pairs, almost all
  strong-versus-weak contrasts. The Bayesian test gives TabPFN-3 a 0.57 probability of beating
  CatBoost on PD (0.43 practical equivalence) and 0.75 on LGD; against TabICLv2, practical
  equivalence dominates (0.76 PD, 0.59 LGD). The champion comparison is exploratory because the
  champions are selected on the same benchmark.
* **Per dataset (App. C).** TabPFN-3 beats CatBoost on 13 of 14 PD datasets (not Home Credit) and
  6 of 7 LGD datasets (not PropLGD1), and beats the linear baselines on every dataset. Its
  relative gain over CatBoost shrinks with dataset size; the authors treat this as descriptive,
  and the LGD slope depends on its smallest dataset.
* **Mean bias (§5.1.1, Figs. 6–7).** TabPFN-3 underpredicts the mean default rate on **all 14 PD
  datasets** (mean +1.42 percentage points) and TabICLv2 on 13 (+0.68), against +0.08 for logistic
  regression and −1.27 for CatBoost. LGD mean biases are small (+0.35 for TabPFN-3).
* **Sample size (§5.2.1, Figs. 8–9).** At 750 PD rows TabPFN-3/TabICLv2 reach AUC 0.700/0.693
  versus 0.677 for CatBoost; at 30,000 rows 0.763/0.760 versus 0.754. At 130 LGD rows they reach
  R² 0.449/0.407 versus 0.325 (CatBoost) and 0.169 (linear); at 4,600 rows 0.576/0.577 versus
  0.550. The gap narrows with data but does not reverse within the sweep.
* **Class imbalance (§5.2.2, Fig. 10).** At a 15% default rate TabPFN-3/TabICLv2 reach AUC
  0.783/0.778 versus 0.770 for CatBoost; at 0.25% they remain at 0.718/0.715 while CatBoost falls
  to 0.683, below logistic regression (0.689).
* **Changes from v2.** v2 found TabICL best on mean PD AUC (0.7517), TabPFNv2 best on LGD R² and
  PD Brier score/log loss, and none of 231 LGD pairs significant after Holm correction. v3 adds
  TabPFN-2.5, TabPFN-3, TabICLv2 and TabDPT, reruns all methods (CatBoost's mean LGD R² moves
  from 0.4401 to 0.4872), replaces the statistics, and replaces v2's 500–15,000-row learning
  curves, including its finding that XGBoost overtakes TabPFNv2 beyond about 8,000 LGD rows.

**Strengths.** Evaluates six TFMs on bounded, bimodal LGD regression rather than treating credit
risk as classification only. Pairs proper scoring rules with an explicit portfolio-level bias
check, which exposes a weakness that discrimination metrics hide. Separates average performance,
fold wins, practical equivalence and pairwise significance, and states the selection caveat on
its champion panel. Nested fixed-seed subsampling varies sample size and default rate within
datasets, and the pretraining-overlap audit checks the two real-data models against their
published corpora. Code is released.

**Limitations.** *Author-stated:* the auxiliary experiments subsample natively large portfolios,
so they do not test intrinsically small ones, and the imbalance sweep removes defaults
artificially rather than reproducing low-default portfolios; the dataset-size association is
descriptive, with few heterogeneous datasets; the champion analysis is exploratory; with seven
LGD datasets, nonsignificant pairwise tests are inconclusive. *Reviewer reading:* random
cross-validation folds give no out-of-time or cross-institution holdout. Much of the PD margin
over CatBoost lies within the equivalence region. The auxiliary experiments compare only two
TFMs with default-setting baselines. The paper recommends post-hoc recalibration for the PD bias
but does not test it. LGD is scored on clipped point predictions, so no predictive distribution
is assessed. Fine-tuning and continued pretraining are not tested. Proprietary datasets limit
reproducibility.

---

<a id="oprior"></a>

## 2026-10 — Bouadi et al. — O'Prior (Shaping the Prior)

**Provenance.** arXiv preprint · arXiv [2605.18971v2](https://arxiv.org/abs/2605.18971v2)
(filed version, 23 October 2026; v1 18 May 2026) · Lexsi Labs · v1's abstract linked code at
[o-prior/O-prior](https://github.com/o-prior/O-prior); v2 deletes that sentence and gives no
other code link, so the filed version does not confirm a release. Apart from that sentence and
the arXiv banner, the v2 text is identical to v1: methods, tables and numbers are unchanged ·
**PDF:** [open](papers/2026/10_Bouadi_et_al._Shaping_the_Prior_How_Synthetic_Task_Distributions_Determine_Tabular_Foundation_Model_Quality.pdf)

**Citation key:**
`2026.BOUADI.shapingpriorhowsynthetictaskdistributionsdeterminetabularfoundationmodelquality`.

**Where it fits.** The first study in this collection to make **prior design the controlled
variable**. Its premise is a criticism of how the line has advanced: TabPFN v2 changed prior and
architecture together, "making attribution impossible". Where [Zhang 2025, *Mitra: Mixed
Synthetic Priors*](#mitra) proposed criteria for *selecting* prior components, O'Prior builds a
prior and measures which of its parts pay. [Shaheen 2026, *Understanding the Surprising
Generalization Properties of Tabular Foundation Models*](#shaheen-retrieval) attacks the same
question from the real-data side.

**What it contains.** O'Prior is a "compositional realism prior" with four coupled components
(§2):

1. a **hierarchical SCM meta-generator**: basic SCM families plus a "Hybrid SCM" that composes
   five mechanism families (MLPs, decision trees, 1-D convolutions, RBF Gaussian processes,
   time-lagged VARs) within one random DAG;
2. a **modular realism engine**: marginal morphing, feature augmentation, MCAR / MAR / MNAR
   missingness, label noise and target reshaping, at moderate or strong intensity;
3. a **stress module** injecting latent confounding, spurious support predictors, covariate
   shift and temporal drift between support and query; and
4. a **curriculum-governed, leakage-safe generation protocol** (linear mild-to-hard schedule).

The protocol is the transferable part (§3.1). Architecture, optimiser, budget and evaluation are
fixed and only the task distribution varies. The model is **nanoTabPFN**, a small open
reimplementation of the TabPFN v2 architecture, trained with the **TFM-Playground** protocol:
**40,000 synthetic datasets per prior** (512–1,024 rows, 3–50 features), 4 tables per step,
1,000 steps per epoch, 10 epochs, no per-condition tuning. Nine O'Prior variants in four groups
(Table 1: SCM diversity G1a–c, realism G2a–c, shift stress G3a–b, full curriculum G4) are
compared with three generators trained under the same budget: the **TabPFN v1**, **TabICL-v1**
and **TabICL-v2** priors. Evaluation is classification only: 21 TabArena v0.1 datasets and 31
OpenML-CC18 datasets with ≤50 features and <10,000 rows, scored by ROC-AUC, accuracy and macro
F1.

**Key results** (Table 2, ROC-AUC on TabArena / OpenML-CC18).

* **Baselines.** The TabPFN v1 prior reaches **0.576 / 0.519** (macro F1 below 0.37 on both);
  TabICL-v1 improves modestly (0.636 / 0.575); TabICL-v2 reaches **0.791 / 0.724**.
* **Mechanism diversity dominates.** The basic SCM prior (G1a, 0.788 / 0.741) already matches
  TabICL-v2. The Hybrid SCM alone (G1b) gives the largest single gain and the **best TabArena
  ROC-AUC of any condition (0.834)**, with 0.823 on CC18; basic + Hybrid (G1c) has the best
  CC18 ROC-AUC (0.831).
* **Realism and stress add smaller, distinct gains.** Strong realism beats moderate realism on
  all six metric–benchmark pairs (G2b 0.832 / 0.813 vs G2a 0.810 / 0.797); adding the shift
  module to the basic SCM prior also helps (G3a 0.801 / 0.781). Combining Hybrid SCM with strong
  realism (G2c) is worse than G2b on CC18, which the authors attribute to the fixed budget.
* **The full curriculum does not win.** G4 beats TabICL-v2 by 2.8 / 10.1 ROC-AUC points (F1 by
  5.9 / 12.5), but G1b, G1c and G2b outperform it on several metric–benchmark pairs; the authors
  argue the warm-up spends budget on easy tasks.
* **Supporting analyses.** A schema-agnostic adaptation of TabStruct (§3.2.2, Table 3, four
  reference datasets) gives O'Prior higher correlation-spectrum alignment and composite score
  than TabICL-v2 everywhere, while TabICL-v2 matches the marginals slightly better. Linear
  probes of each layer (Table 4) show O'Prior representations becoming more class-separable with
  depth on Vehicle, Ionosphere and Segment, where TabICL-v2 stays flat or weak; Breast Cancer and
  Credit-g do not discriminate between priors.

**Strengths.** The controlled protocol is the contribution: cheap enough to rerun at nano scale
and reusable for any prior component (code was linked from v1 only). The result that a single well-chosen
mechanism family beats the full curriculum is reported rather than hidden, and the probing study
includes a random-initialisation control.

**Limitations.** *Scale:* everything runs at nano scale with low absolute numbers, and only the
*qualitative* ordering is claimed to transfer; whether it holds for TabICL- or TabPFN-sized
models is untested. *Evaluation:* classification only, so the regression and target-reshaping
parts of the realism engine are never exercised; a single training run per prior with no seeds
or intervals, although several gaps are under one point. The stress module is meant to help
under shift, but the benchmarks are i.i.d.; the authors acknowledge that its benefit is
untested. Baseline generators were designed for other architectures and budgets. *Authorship:*
the winning prior is the authors' own (Lexsi Labs), so independent replication matters.

---
