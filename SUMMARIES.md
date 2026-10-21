# Literature on Tabular Foundation Models

A chronological tour of the papers in this folder. The arc: PFNs (in-context Bayesian inference
for arbitrary priors) → TabPFN (PFNs with a tabular prior) → TabPFNv2 (the first
production-grade release) → a Cambrian explosion of variants (continued pretraining, drift,
fairness, causal inference, time series, many classes, scalability) → TabPFN-2.5 (whose
*default* checkpoint is the real-data continued-pretrained variant) / 2.6 (back to a
synthetic-only default) → TabPFN-3 (May 2026; new three-stage architecture, scales to 1M rows,
test-time-compute "Thinking" mode) → and, from June 2026, the first big-tech entrant shipping
the paradigm as a product (Google's TabFM, wired into BigQuery). The September releases
extend the comparison to TabPFN-3.5, Mitra-v2, Xiaomi-TabLDM, LimiX-2's masked conditional
modelling, and Causilo's refinement-before-compression design. MulTaBench tests the
multimodal representation gap; the October test-time-compute study separates the gains
from adapting weights, selecting ensemble members, and constructing the context.

For every paper:

* **Where it fits** in the picture above — what it answers, extends or contradicts.
* **What it contains** — method, datasets, headline numbers.
* **Strengths** — what the paper genuinely establishes.
* **Limitations** — what it does *not* support, and where to be careful quoting it.

**This document is project-neutral by contract** (see AGENTS.md). It describes the literature
for every consuming project; it contains no project's pipeline details, hyperparameter choices,
or relevance rankings. Those belong in your project's own `PROJECT_SPECIFIC.md` — copy
[`PROJECT_SPECIFIC.template.md`](PROJECT_SPECIFIC.template.md) inside your project's copy of
this folder and write them there.

## Overview table

| Date | Authors | Title | One-line contribution | PDF |
|---------|---------|-------|-----------------------|-----|
| 2021-12 | Müller et al. | Transformers Can Do Bayesian Inference | Foundational PFN paper: training a transformer on datasets sampled from a prior makes its cross-entropy loss equal the expected KL to the posterior predictive, so one forward pass approximates Bayesian inference (GP/BNN priors; Riemann output head). | [pdf](papers/2021/12_Muller_et_al._Transformers_Can_Do_Bayesian_Inference.pdf) |
| 2023-05 | Müller et al. | PFNs4BO — In-Context Learning for Bayesian Optimization | PFN surrogate for Bayesian optimisation with GP, HEBO(+) and BNN priors; outputs a full predictive distribution; the HEBO+ prior beats baselines on HPO-B. | [pdf](papers/2023/05_Muller_et_al._PFNs4BO_In_Context_Learning_for_Bayesian_Optimization.pdf) |
| 2023-07 | Nagler | **Statistical Foundations of Prior-Data Fitted Networks** | The theory of *why* PFN in-context learning works — and its limit: a frequentist reading in which variance vanishes but bias only vanishes with proper localisation, which the transformer does not guarantee. | [pdf](papers/2023/07_Nagler_Statistical_Foundations_of_Prior_Data_Fitted_Networks.pdf) |
| 2023-09 | Hollmann et al. | TabPFN — A Transformer That Solves Small Tabular Classification Problems in a Second | First TabPFN: PFN trained on an SCM+BNN tabular prior; on par with tuned AutoML on small numerical classification tasks in about a second. | [pdf](papers/2023/09_Hollmann_et_al._TabPFN_A_Transformer_That_Solves_Small_Tabular_Classification_Problems_in_a_Second.pdf) |
| 2024-03 | Rundel et al. | Interpretable Machine Learning for TabPFN | Adapts IML methods (SHAP, LOCO, PD/ICE/ALE, Data Shapley) to TabPFN, using in-context refits as exact, cheap retraining. | [pdf](papers/2024/03_Rundel_et_al._Interpretable_Machine_Learning_for_TabPFN.pdf) |
| 2024-06 | Breugel and Schaar | Why Tabular Foundation Models Should Be a Research Priority | Position paper (ICML 2024): "Large Tabular Models" are an under-invested priority, with three reasons and four desiderata (D1–D4). | [pdf](papers/2024/06_Breugel_and_Schaar_Why_Tabular_Foundation_Models_Should_Be_a_Research_Priority.pdf) |
| 2024-10 | den Breejen et al. | **TabForestPFN** — Fine-tuned In-Context Learning Transformers are Excellent Tabular Data Classifiers | Swaps TabPFN's SCM prior for a *forest* generator producing complex decision boundaries; after fine-tuning, TabForestPFN ties tuned GBDTs on TabZilla (0.840 vs 0.842). Tree-prior ancestor of Mitra. | [pdf](papers/2024/10_Breejen_et_al._Fine_tuned_In_Context_Learning_Transformers_are_Excellent_Tabular_Data_Classifiers.pdf) |
| 2024-11 | Helli et al. | Drift-Resilient TabPFN | Adds a secondary SCM that shifts the base SCM over a domain index, so ICL extrapolates temporal drift; accuracy 0.688→0.744 on 18 shifted datasets. | [pdf](papers/2024/11_Helli_et_al._Drift_Resilient_TabPFN_In_Context_Learning_Temporal_Distribution_Shifts_on_Tabular_Data_1.pdf) |
| 2024-12 | Hoo et al. | The Tabular Foundation Model TabPFN Outperforms Specialized Time Series Forecasting Models | TabPFN-TS: forecasting framed as tabular regression on timestamp-derived features (no lags); an 11M-param frozen TabPFN beats Chronos-Mini and matches Chronos-Large. | [pdf](papers/2024/12_Hoo_et_al._The_Tabular_Foundation_Model_TabPFN_Outperforms_Specialized_Time_Series_Forecasting_Models_Based_on.pdf) |
| 2024-12 | Thomas et al. | **LoCalPFN** — Retrieval & Fine-Tuning for In-Context Tabular Models | Retrieves a k-NN neighbourhood as the context and fine-tunes end-to-end, breaking v1's size ceiling; SOTA on 95 TabZilla datasets. Ancestor of TabDPT's retrieval. | [pdf](papers/2024/12_Thomas_et_al._Retrieval_Fine_Tuning_for_In_Context_Tabular_Models.pdf) |
| 2024-12 | Feuer et al. | **TuneTables** — Context Optimization for Scalable Prior-Data Fitted Networks | Compresses a large dataset into a small *learned* context (prompt tuning for PFNs), lifting TabPFN v1's ~1000-row ceiling; best average rank over 19 algorithms on 98 datasets while tuning <5% of parameters. | [pdf](papers/2024/12_Feuer_et_al._TuneTables_Context_Optimization_for_Scalable_Prior_Data_Fitted_Networks.pdf) |
| 2025-01 | Hollmann et al. | Accurate predictions on small data with a tabular foundation model | The TabPFNv2 paper (Nature): cell-level alternating attention, ~10× rows and 5× features over v1, regression head; beats a 4-hour tuned ensemble in 2.8 s on small data. | [pdf](papers/2025/01_Hollmann_et_al._Accurate_predictions_on_small_data_with_a_tabular_foundation_model.pdf) |
| 2025-02 | Liu and Ye | TabPFN Unleashed — A Scalable and Effective Solution to Tabular Classification Problems | BETA: a fine-tuned lightweight encoder with Batch-Ensemble paths, bootstrapped contexts and ECOC lifts TabPFN v1's feature/class/size limits while reducing bias and variance. | [pdf](papers/2025/02_Liu_and_Ye_TabPFN_Unleashed_A_Scalable_and_Effective_Solution_to_Tabular_Classification_Problems.pdf) |
| 2025-02 | McCarter | **What exactly has TabPFN learned to do?** | Black-box probes expose duplication, periodicity and ensembling failures in v1; the v2 appendix combines rougher toy decision surfaces with strong parity learning. | [pdf](papers/2025/02_McCarter_What_exactly_has_TabPFN_learned_to_do.pdf) |
| 2025-05 | Müller et al. | Position — The Future of Bayesian Prediction Is Prior-Fitted | Position paper (ICML 2025): with real data scarce and compute cheap, prior-fitted networks should become the default route to Bayesian prediction. | [pdf](papers/2025/05_Muller_et_al._Position_The_Future_of_Bayesian_Prediction_Is_Prior_Fitted.pdf) |
| 2025-05 | Qu et al. | TabICL — A Tabular Foundation Model for In-Context Learning on Large Data | Column-collapsing row embeddings before ICL; up to 500K rows (with CPU/disk offloading) and up to 10× faster than TabPFNv2 at comparable accuracy. | [pdf](papers/2025/05_Qu_et_al._TabICL_A_Tabular_Foundation_Model_for_In_Context_Learning_on_Large_Data.pdf) |
| 2025-06 | Robertson et al. | FairPFN — A Tabular Foundation Model for Causal Fairness | Fair predictor pretrained on biased/fair SCM pairs that removes causal effects of a protected attribute in-context; real-data validation on Law School and Adult. | [pdf](papers/2025/06_Robertson_et_al._FairPFN_A_Tabular_Foundation_Model_for_Causal_Fairness.pdf) |
| 2025-06 | Rubachev et al. | **On Finetuning Tabular Foundation Models** | Empirical study of fine-tuning TabPFNv2: full FT matches PEFT and converges fastest by sharpening query–key retrieval, but is less stable under temporal shift (TabReD). | [pdf](papers/2025/06_Rubachev_et_al._On_Finetuning_Tabular_Foundation_Models_1.pdf) |
| 2025-06 | Ye et al. | A Closer Look at TabPFN v2 — Understanding Its Strengths and Extending Its Capabilities | Explains TabPFNv2's randomized feature tokens; test-time extensions (decimal-digit encoding for many classes, feature bagging, -SQ/-DF for large data) extend it without retraining. | [pdf](papers/2025/06_Ye_et_al._A_Closer_Look_at_TabPFN_v2_Understanding_Its_Strengths_and_Extending_Its_Capabilities.pdf) |
| 2025-07 | Garg et al. | **Real-TabPFN** — Improving Tabular Foundation Models via Continued Pre-training With Real-World Data | **The reference continued-pretraining recipe.** Continue-pretrains TabPFNv2 on 71 curated real datasets with L2-SP; +0.022 normalised ROC-AUC on the OpenML AutoML benchmark. | [pdf](papers/2025/07_Garg_et_al._Real_TabPFN_Improving_Tabular_Foundation_Models_via_Continued_Pre_training_With_Real_World_Data.pdf) |
| 2025-10 | Zhang et al. | Mitra — Mixed Synthetic Priors for Enhancing Tabular Foundation Models | Selects a mixture of synthetic priors (SCM plus four tree-based) by performance, diversity and distinctiveness; the resulting model edges TabPFNv2 on ≤10k-row benchmarks. | [pdf](papers/2025/10_Zhang_et_al._Mitra_Mixed_Synthetic_Priors_for_Enhancing_Tabular_Foundation_Models.pdf) |
| 2025-10 | Wu and Bergman | **APT** — Zero-shot Meta-learning for Tabular Prediction Tasks with Adversarially Pre-trained Transformer | Makes the synthetic prior *adaptive*: adversarial data agents shift their own generating distribution to keep challenging the model. A mixture block removes the class-count cap. | [pdf](papers/2025/10_Wu_and_Bergman_Zero_shot_Meta_learning_for_Tabular_Prediction_Tasks_with_Adversarially_Pre_trained_Transformer.pdf) |
| 2025-11 | Robertson et al. | Do-PFN — In-Context Learning for Causal Effect Estimation | PFN trained on paired observational/interventional SCM data predicts conditional interventional outcomes without a causal graph; uncertainty grows when effects are unidentifiable. | [pdf](papers/2025/11_Robertson_et_al._Do_PFN_In_Context_Learning_for_Causal_Effect_Estimation.pdf) |
| 2025-11 | Zhang et al. | TabPFN — One Model to Rule Them All | Explains TabPFNv2 as approximate Bayesian inference for statisticians, then shows strong out-of-the-box results in semi-supervised estimation, treatment effects and covariate shift. | [pdf](papers/2025/11_Zhang_et_al._TabPFN_One_Model_to_Rule_Them_All.pdf) |
| 2025-11 | Bouadi et al. | **Orion-MSP** — Multi-Scale Sparse Attention for Tabular In-Context Learning | Extends TabICL with multi-scale features, block-sparse attention and optional Perceiver memory; overall rank 3.58, but weaker on wide tables (5.69). | [pdf](papers/2025/11_Bouadi_et_al._Orion_MSP_Multi_Scale_Sparse_Attention_for_Tabular_In_Context_Learning.pdf) |
| 2025-11 | Zheng et al. | **From Tables to Signals** — Revealing Spectral Adaptivity in TabPFN | First frequency-domain account of TFM inductive bias. TabPFN's effective bandwidth widens with the *number of context rows*, where an MLP's is fixed once the architecture is. | [pdf](papers/2025/11_Zheng_et_al._From_Tables_to_Signals_Revealing_Spectral_Adaptivity_in_TabPFN.pdf) |
| 2025-12 | Pfefferle et al. | nanoTabPFN — A Lightweight and Educational Reimplementation of TabPFN | Under-500-line educational reimplementation of v2's architecture and training loop, trained on TabICL prior data; beats TabPFN without ensembling in its small regime. | [pdf](papers/2025/12_Pfefferle_et_al._nanoTabPFN_A_Lightweight_and_Educational_Reimplementation_of_TabPFN.pdf) |
| 2025-12 | Tanna et al. | TabTune — A Unified Library for Inference and Fine-Tuning Tabular Foundation Models | Unified library for zero-shot, meta-learning, SFT and LoRA across seven TFMs; adaptation outcomes are strongly model-dependent. | [pdf](papers/2025/12_Tanna_et_al._TabTune_A_Unified_Library_for_Inference_and_Fine_Tuning_Tabular_Foundation_Models.pdf) |
| 2025-12 | Spinaci et al. | **ConTextTab** — A Semantics-Aware Tabular In-Context Learner | Table-native ICL with per-modality (text/date/number) embeddings trained on large-scale *real* tables; new standard on the semantically rich CARTE benchmark. | [pdf](papers/2025/12_Spinaci_et_al._ConTextTab_A_Semantics_Aware_Tabular_In_Context_Learner.pdf) |
| 2025-12 | Arazi et al. | **TabSTAR** — A Tabular Foundation Model for Tabular Data with Text Fields | Unfrozen text encoder conditioned on *target tokens* for target-aware representations, with per-task LoRA fine-tuning; scaling in pretraining dataset count; weaker on regression than GBDTs. | [pdf](papers/2025/12_Arazi_et_al._TabSTAR_A_Tabular_Foundation_Model_for_Tabular_Data_with_Text_Fields.pdf) |
| 2025-12 | Balazadeh Meresht et al. | **CausalPFN** — Amortized Causal Effect Estimation via In-Context Learning | One transformer trained on simulated ignorable DGPs estimates CATE/ATE in-context; best average CATE rank over 310 tasks, but needs temperature scaling for calibrated intervals out of distribution. | [pdf](papers/2025/12_Balazadeh_Meresht_et_al._CausalPFN_Amortized_Causal_Effect_Estimation_via_In_Context_Learning.pdf) |
| 2025-12 | Arbel et al. | **EquiTabPFN** — A Target-Permutation Equivariant Prior Fitted Network | Names a real architectural defect: TabPFN is not equivariant to the *ordering of target dimensions*, leaving an irreducible "equivariance gap". | [pdf](papers/2025/12_Arbel_et_al._EquiTabPFN_A_Target_Permutation_Equivariant_Prior_Fitted_Network.pdf) |
| 2026-01 | Hoo et al. | From Tables to Time — Extending TabPFN-v2 to Time Series Forecasting | Frozen TabPFN-v2 plus temporal features forecasts time series; best on fev-bench covariate tasks and competitive on GIFT-Eval behind TiRex, Toto and Moirai-2. | [pdf](papers/2026/01_Hoo_et_al._From_Tables_to_Time_Extending_TabPFN_v2_to_Time_Series_Forecasting.pdf) |
| 2026-01 | Klein and Hoffart | Position — Foundation Models for Tabular Data within Systemic Contexts Need Grounding | Position paper from SAP: tabular FMs trained on isolated tables miss the operational context (business rules, code, data models) that gives data meaning. Proposes Semantically Linked Tables (SLT) and FMSLT as a new model class. | [pdf](papers/2026/01_Klein_and_Hoffart_Position_Foundation_Models_for_Tabular_Data_within_Systemic_Contexts_Need_Grounding.pdf) |
| 2026-01 | Ma et al. | TabDPT — Scaling Tabular Foundation Models on Real Data | Row-based TFM pretrained on real OpenML tables with a random-column-target objective and kNN-retrieved contexts; power-law scaling in model and data size. | [pdf](papers/2026/01_Ma_et_al._TabDPT_Scaling_Tabular_Foundation_Models_on_Real_Data.pdf) |
| 2026-02 | Grinsztajn et al. | **TabPFN-2.5** — Advancing the State of the Art in Tabular Foundation Models | Deeper TabPFN (18 regression / 24 classification layers) for up to 50K×2K; matches AutoGluon 1.4 on TabArena; separate Real-TabPFN-2.5 variant. | [pdf](papers/2026/02_Grinsztajn_et_al._TabPFN_2.5_Advancing_the_State_of_the_Art_in_Tabular_Foundation_Models.pdf) |
| 2026-02 | Ma et al. | Foundation Models for Causal Inference via Prior-Data Fitted Networks | CausalFM: PFNs on identifiability-constrained SCM priors for back-door, front-door and IV CATE estimation; one model per identification setting; competitive with task-specific estimators. | [pdf](papers/2026/02_Ma_et_al._Foundation_Models_for_Causal_Inference_via_Prior_Data_Fitted_Networks.pdf) |
| 2026-03 | Kolberg et al. | **TabPFN-Wide** — Continued Pre-Training for Extreme Feature Counts | TabPFNv2 classifier continued-pretrained on a synthetic feature-widening prior (TabICL prior plus sparse projections) to handle 30k+ features without forgetting. | [pdf](papers/2026/03_Kolberg_et_al._TabPFN_Wide_Continued_Pre_Training_for_Extreme_Feature_Counts.pdf) |
| 2026-04 | Tanna et al. | **Exploring Fine-Tuning for Tabular Foundation Models** | Six TFMs × four adaptation strategies: zero-shot is strong; SFT often hurts accuracy and calibration; meta-learning helps on imbalanced data; small datasets favour zero-shot. | [pdf](papers/2026/04_Tanna_et_al._Exploring_Fine_Tuning_for_Tabular_Foundation_Models.pdf) |
| 2026-04 | Bouadi et al. | **Orion-BiX** — Bi-Axial Attention for Tabular In-Context Learning | TabICL-based model with a bi-axial multi-attention row encoder and episodic kNN meta-training; strongest in few-shot and domain-specific ranks. | [pdf](papers/2026/04_Bouadi_et_al._Orion_Bix_Bi_Axial_Attention_for_Tabular_In_Context_Learning.pdf) |
| 2026-05 | Grinsztajn et al. | **TabPFN-3** — Technical Report | **The May 2026 TabPFN generation.** TabICL-style three-stage architecture scaling to 1M rows on one H100, many-class decoder and "Thinking" mode; synthetic-prior only; tops TabArena by >200 Elo over non-TabPFN models. | [pdf](papers/2026/05_Grinsztajn_et_al._TabPFN_3_Technical_Report.pdf) |
| 2026-05 | Tanna et al. | **Data Presentation Over Architecture** — Resampling Strategies for Credit Risk Prediction with TFMs | On imbalanced credit data, context construction outweighs TFM choice: balanced/hybrid sampling adds ~3 AUC points on Home Credit (~1 on Lending Club); untuned, unweighted baselines. | [pdf](papers/2026/05_Tanna_et_al._Data_Presentation_Over_Architecture_Resampling_Strategies_for_Credit_Risk_Prediction_with_Tabular_Foundation_Models.pdf) |
| 2026-05 | Hosseinzadeh et al. | **TabDPT-Turbo** — Efficient In-Context Learning for Tabular Prediction | Drops TabDPT's retrieval for **long-context pretraining**, stays row-based, scales the real corpus to 1,445 tables; ≈2.4× faster total time than TabPFN-3 and ≈13× than TabICLv2. Shipped as TabDPT v1.2. | [pdf](papers/2026/05_Hosseinzadeh_et_al._TabDPT_Turbo_Efficient_In_Context_Learning_for_Tabular_Prediction.pdf) |
| 2026-05 | Bouadi et al. | **O'Prior** — Shaping the Prior: How Synthetic Task Distributions Determine TFM Quality | **Controlled prior study**: architecture, optimizer and compute fixed, only the synthetic task distribution varied. Mechanism diversity drives transfer most; the full curriculum does not beat the best single components. | [pdf](papers/2026/05_Bouadi_et_al._Shaping_the_Prior_How_Synthetic_Task_Distributions_Determine_Tabular_Foundation_Model_Quality.pdf) |
| 2026-05 | Schambach et al. | **Benchmarking Attention for Tabular Foundation Models** | H100 microbenchmarks show that attention across features and across samples need different backends; tensor-copy overhead makes FlashAttention-3 especially effective across samples. | [pdf](papers/2026/05_Schambach_et_al._Benchmarking_Attention_for_Tabular_Foundation_Models.pdf) |
| 2026-06 | Purucker et al. | **Beyond IID: How General Are Tabular Foundation Models, Really?** | BeyondArena (142 curated datasets, IID + temporal + grouped splits): TFM ICL wins tiny/small IID data but **loses to tuned RealMLP/GBDTs under temporal & grouped splits**, with the gap growing with sample size and high-cardinality categoricals. Fine-tuning explicitly untested. | [pdf](papers/2026/06_Purucker_et_al._Beyond_IID_How_General_Are_Tabular_Foundation_Models_Really.pdf) |
| 2026-06 | Kong and Das (Google) | **TabFM** — Introducing TabFM: A zero-shot foundation model for tabular data | *Blog post, not a paper.* Google's TabPFN+TabICL **hybrid** trained on hundreds of millions of synthetic SCM tables; TabArena Elo shown only as a figure; BigQuery `AI.PREDICT` announced; non-commercial weights. | [pdf](papers/2026/06_Kong_and_Das_Introducing_TabFM_A_zero_shot_foundation_model_for_tabular_data.pdf) |
| 2026-07 | Luo et al. | **Memory Efficient Tabular Foundation Models** | Post-hoc INT4 quantization (GPTQ, AWQ, K-Means) of TabPFN v2.5/2.6 shrinks compressed checkpoints up to **7.6×** with negligible accuracy loss; inference memory is largely unchanged. | [pdf](papers/2026/07_Luo_et_al._Memory_Efficient_Tabular_Foundation_Models.pdf) |
| 2026-07 | Baesens et al. | **Foundation Models for Credit Risk Prediction: A Game Changer?** | Untuned TFMs compete strongly on 14 PD and 7 LGD datasets against 29/22 methods (TFMs included), especially with little data; discrimination and probability quality select different winners. | [pdf](papers/2026/07_Baesens_et_al._Foundation_Models_for_Credit_Risk_Prediction_A_Game_Changer.pdf) |
| 2026-08 | Shaheen et al. | **Understanding the Surprising Generalization Properties of Tabular Foundation Models** | Pretraining on a *single* real table transfers broadly; feature count drives transfer and ≥30-feature filtering hurts; argues TFMs learn **retrieval-and-aggregation** rather than prior-fitted Bayesian inference. | [pdf](papers/2026/08_Shaheen_et_al._Understanding_the_Surprising_Generalization_Properties_of_Tabular_Foundation_Models.pdf) |
| 2026-08 | Eo et al. | **EXAONE Tabular 1.0** — Technical Report | CAST interleaves feature- and item-axis attention at every layer without row compression; a 20.8M model ranks first on TabArena classification untuned; 999-quantile regression head. | [pdf](papers/2026/08_Eo_et_al._EXAONE_Tabular_1.0_Technical_Report.pdf) |
| 2026-09 | Qu et al. | TabICLv2 — A better, faster, scalable, and open tabular foundation model | Open TabICL successor: new SCM prior, QASSMax attention scaling and Muon pretraining; beats RealTabPFN-2.5 untuned on TabArena and TALENT, scales to million-row tables. | [pdf](papers/2026/09_Qu_et_al._TabICLv2_A_better_faster_scalable_and_open_tabular_foundation_model.pdf) |
| 2026-09 | Jäger et al. | **TabPFN-3.5** — Technical Report | TabPFN-3 with Fourier cell encodings, doubled width and a prior retuned for grouped/wide/high-cardinality data; the family ranks 1st on seven benchmarks incl. BeyondArena. Weights downloadable under a restrictive licence. | [pdf](papers/2026/09_Jager_et_al._TabPFN_3.5_Technical_Report.pdf) |
| 2026-09 | Tao et al. | **Mitra-v2** — Technical Report | Same Tab2D backbone with ~10× wider pretraining tasks and a Hybrid SCM; 77M parameters tie the 1.64B TabFM on TabArena; >10 classes via a hierarchical wrapper; all changes made at once. | [pdf](papers/2026/09_Tao_et_al._Mitra_v2_Technical_Report.pdf) |
| 2026-09 | Xiaomi-TabLDM Team | **Xiaomi-TabLDM** — A Tabular Foundation Model | First **sparse Mixture-of-Experts** in a TFM, extending TabICLv2's grouping; 1st on OpenML-CTR23 regression, 2nd on TALENT overall; no ablations. | [pdf](papers/2026/09_Team_et_al._Xiaomi_TabLDM_A_Tabular_Foundation_Model_Technical_Report.pdf) |
| 2026-09 | Zhang et al. | **LimiX-2** — A Contextual Mechanism Network Towards General Structured-Data Intelligence | Retains cells and jointly trains target prediction and masked-feature reconstruction; the 406M model ranks 1st on TabArena, TALENT and BCCO; attention probes recover causal skeletons, not effects. | [pdf](papers/2026/09_Zhang_et_al._LimiX_2_A_Contextual_Mechanism_Network_Towards_General_Structured_Data_Intelligence.pdf) |
| 2026-09 | Cho et al. | **Causilo** — Technical Report | Refines cells across both axes before row compression with linear feature-side attention; 1785 TabArena Elo at 0.10 s per 1K queries; beats TabPFN-3.5-Fast with 31.6% less inference time. | [pdf](papers/2026/09_Cho_et_al._Causilo_Technical_Report.pdf) |
| 2026-09 | Arazi et al. | **MulTaBench**: Benchmarking Multimodal Tabular Learning with Text and Image | 40 text/image-tabular datasets where both modalities add signal and target-aware encoders beat frozen embeddings (37/40 when pooling all learners); 40 further candidates test the selection boundary. | [pdf](papers/2026/09_Arazi_et_al._MulTaBench_Benchmarking_Multimodal_Tabular_Learning_with_Text_and_Image.pdf) |
| 2026-10 | Ning et al. | **Test-Time Compute for Tabular Foundation Models: Mechanisms, Gains, and Limits** | DiagScale matches much of full finetuning's gain; selective aggregation helps at substantial cost, while retrieval can help or fail and context expansion gives no consistent gain. | [pdf](papers/2026/10_Ning_et_al._Test_Time_Compute_for_Tabular_Foundation_Models_Mechanisms_Gains_and_Limits.pdf) |
| 2026-10 | Zhao et al. | **TabReliBench** — Evaluating Tabular Foundation Models Beyond Predictive Accuracy | Reliability benchmark (241 datasets, 11 TFMs): near-nominal marginal coverage but heterogeneous **subgroup coverage**; ensembling and conformal post-processing do not reliably fix it. | [pdf](papers/2026/10_Zhao_et_al._TabReliBench_Evaluating_Tabular_Foundation_Models_Beyond_Predictive_Accuracy.pdf) |
| 2026-10 | Cannistraci and Vogt | **Tabular Foundation Models Are Effectively Shallow** | Label-free affine translators replace up to 96% of TFM blocks; half-depth is near-lossless for classification and regression; one-block TabPFN-3 is 2.4× faster in 6× less memory, but single blocks hurt regression. | [pdf](papers/2026/10_Cannistraci_and_Vogt_Tabular_Foundation_Models_Are_Effectively_Shallow.pdf) |
| 2026-10 | Alberge et al. | **SurvICL**: a Foundation Model for in-context Survival Analysis | TabICLv2-based survival ICL trained on latent event-time quantiles from a proportional-odds prior; best held-out IBS on 63 datasets, with size-dependent limits. | [pdf](papers/2026/10_Alberge_et_al._SurvICL_a_Foundation_Model_for_in_context_Survival_Analysis.pdf) |

---

<a id="pfns-2021"></a>

## 2021-12 — Müller et al. — Transformers Can Do Bayesian Inference

**arXiv:** [2112.10510](https://arxiv.org/abs/2112.10510) · **PDF:**
[open](papers/2021/12_Muller_et_al._Transformers_Can_Do_Bayesian_Inference.pdf)

**Provenance.** First public release: 20 December 2021; publication: ICLR 2022. The filed conference PDF has no exact revision date. The historical path and chronology use the first release, not an inferred PDF month; its hash and evidence are recorded in `papers/filing_overrides.json`.

**Where it fits.** The bedrock of the entire PFN / TabPFN line. Müller and colleagues introduce
*Prior-Fitted Networks* (PFNs): transformers that, after a single training phase on synthetic
datasets sampled from a Bayesian prior, perform approximate posterior inference *in context* on
any new dataset drawn from that prior — without any parameter update.

**What it contains.** The training recipe: at each step, sample a prior dataset (an arbitrary
stochastic process specified by the researcher), give the transformer the labelled context plus
an unlabelled query point, and use cross-entropy loss to push the network's prediction toward
the true label sampled from the prior. The authors show that this loss equals the expected KL
divergence between the true posterior predictive distribution (PPD) and the network's
prediction, up to a constant (Cor. 1.1), so its optimum recovers the PPD when the model family
contains it (Cor. 1.2). Regression targets use a **Riemann (bucketed) output distribution** — a
discretised density over fixed buckets. They demonstrate the approach on Gaussian-Process
regression, Bayesian-neural-network (with architecture uncertainty) priors, and small tabular
classification on 20 OpenML AutoML Benchmark datasets using the GP and BNN priors — the
beginnings of what would become TabPFN.

The crucial conceptual contribution: there is no learning at *inference* time. Once trained, the
network is a fixed function; calling it on a new dataset is one forward pass. This sidesteps
both the brittleness of MCMC sampling for non-conjugate priors and the slowness of variational
fitting for every new task.

**Strengths.** Theoretically grounded (loss = KL to true PPD, so more training cannot overfit),
extremely fast (1,000–8,000× vs NUTS), and natively well-calibrated (ECE 0.025 vs 0.066 XGB).

**Limitations.** Tiny scale — ~30 labeled rows, ≤60 features, balanced binary only, simplistic
GP/BNN priors, no categoricals/missing values, and quadratic attention limits context.

---

## 2023-05 — Müller et al. — PFNs4BO

**Venue:** ICML 2023 (PMLR 202) · **arXiv:** [2305.17535](https://arxiv.org/abs/2305.17535) · **PDF:**
[open](papers/2023/05_Muller_et_al._PFNs4BO_In_Context_Learning_for_Bayesian_Optimization.pdf)

**Where it fits.** Sister paper to TabPFN — applies PFNs to a different domain
(Bayesian-optimisation surrogate models).

**What it contains.** A PFN trained on synthetic (configuration, value) datasets from one of
three priors — a simple **GP** prior, a **HEBO-inspired** GP prior (HEBO / HEBO+), and a
**BNN** prior. At inference time, given past evaluations of an unknown objective, the PFN outputs
a full predictive distribution (a Riemann/bar distribution) at unseen configurations, from which
acquisition functions such as EI are computed. Used as a drop-in replacement for
Gaussian-Process surrogates inside an acquisition-function loop. The advantages over GPs: no
kernel choice, no quadratic-time fitting, and the ability to encode arbitrary prior knowledge
(user priors on the optimum, irrelevant dimensions) by designing the prior generator. Evaluated
on GP samples and three HPO testbeds: HPO-B, Bayesmark and PD1.

**Strengths.** Encodes priors GPs cannot (BNNs, user beliefs, irrelevant features); on HPO-B the
HEBO+ prior outperforms the baselines while the BNN prior performs similar to the best baseline
(§7.1), and inference is a single forward pass.

**Limitations.** Fragile when data has low likelihood under the prior, no joint sampling across
points, and validated only to ~1000 context points. About 10% of HPO-B hyperparameters lack a
declared log scale; the authors handle this with inference-time input warping rather than
treating it as standard BO, so HPO-B results partly measure that warping.

---

<a id="nagler-theory"></a>


## 2023-07 — Nagler — Statistical Foundations of Prior-Data Fitted Networks

**Venue:** ICML 2023 (PMLR v202) · Thomas Nagler, LMU Munich / Munich Center for Machine
Learning · **PDF:**
[open](papers/2023/07_Nagler_Statistical_Foundations_of_Prior_Data_Fitted_Networks.pdf)

**Where it fits.** The theory paper the rest of this corpus leans on without always citing.
Müller 2021 justified PFNs with a Bayesian argument; Nagler asks what actually happens
statistically, and arrives at a *frequentist* reading that explains PFN behaviour more
completely — including the phenomenon nobody had accounted for, that accuracy keeps improving
when a PFN is fed datasets far larger than anything it saw in pretraining.

**What it contains.** The central move is to stop treating the network as an approximate
posterior and treat it as a **pre-tuned but untrained predictor**: a fixed function of the
context set. Under that lens the usual bias–variance decomposition applies, and two conditions
emerge:

* **Variance vanishes** if the predictor's sensitivity to any *individual*
training sample vanishes as the context grows. The transformer architecture, with attention
averaging over context rows, delivers this — which is why PFNs behave stably and improve with
more context.
* **Bias vanishes only if the predictor is appropriately *localised*
around the test feature** — i.e. it must weight nearby context points more than distant ones.
**Current PFN transformer implementations do not guarantee this.**

So PFNs get the variance half of consistency for free, but not the bias half. Transformers can
still reduce bias through implicit model selection over sub-models (multi-head attention), and in
the numerical validation (§6.5) TabPFN v1's bias decreases until n ≈ 1000 and then plateaus
rather than vanishing. A simple post-hoc fix — a **localised TabPFN** that keeps only the k
nearest neighbours of the query as context (§6.4) — lets the bias keep falling beyond n = 1000
at the cost of slightly larger variance. That asymmetry is the paper's real contribution and it
is predictive: it says a PFN will look excellent in-distribution and plateau where localisation
matters, and it tells architects what to fix.

**Strengths.** This is the only rigorous account of *why* the paradigm works, and it is
constructive rather than merely critical — "design for localisation" is actionable, and the
later retrieval-based models (LoCalPFN, TabDPT) can be read as exactly that fix arrived at
empirically.

**Limitations.** The results are asymptotic, they concern classification with a fixed
pretraining distribution, and they say nothing about how much bias a given architecture actually
carries on a given table. It also predates TabPFN v2, so the analysis is of the v1-era
architecture — though the argument is about attention-based context aggregation in general and
transfers.

---

## 2023-09 — Hollmann et al. — TabPFN

**Venue:** ICLR 2023 · **arXiv:** [2207.01848](https://arxiv.org/abs/2207.01848) · **PDF:**
[open](papers/2023/09_Hollmann_et_al._TabPFN_A_Transformer_That_Solves_Small_Tabular_Classification_Problems_in_a_Second.pdf)

**Where it fits.** The first TabPFN. Applies the PFN recipe to small tabular classification with
a structural-causal-model prior tailored for tabular data.

**What it contains.** A transformer takes ``(X_context, y_context, X_query) → ŷ_query`` in one
forward pass. The prior is a mixture: it samples either small structural causal models (with a
preference for simple structures) or Bayesian neural networks, each specifying a joint
distribution over features and a target; millions of these are sampled and the transformer is
trained to predict held-out targets given context. At inference time, no gradient updates: a
held-out test set is just appended to the training set in the input, the transformer
marginalises over its implicit prior, and predictions come out one forward pass later.

Empirical headline: on the 18 OpenML-CC18 datasets with ≤ 1k training rows, ≤ 100 purely
numerical features, no missing values and ≤ 10 classes, TabPFN clearly outperforms boosted trees
and performs on par with state-of-the-art AutoML systems (AutoGluon, Auto-sklearn 2.0) — in about
a second where the AutoML systems take minutes; results are validated on 67 further small
numerical OpenML datasets. The paper also discusses
calibration (TabPFN's predictive probabilities are sharp and well-calibrated) and robustness to
small-sample noise.

**Strengths.** Instant (0.62s GPU, ~5,700× speedup), calibrated, and competitive with tuned
GBDTs/AutoML on 18 OpenML-CC18 numerical datasets.

**Limitations.** Hard caps (~1000 rows, 100 features, 10 classes, classification only) and
degradation on categorical features, missing values, and uninformative features.

---

## 2024-03 — Rundel et al. — Interpretable Machine Learning for TabPFN

**Venue:** xAI 2024 (Springer CCIS 2154) · **arXiv:** [2403.10923](https://arxiv.org/abs/2403.10923) · **PDF:**
[open](papers/2024/03_Rundel_et_al._Interpretable_Machine_Learning_for_TabPFN.pdf)

**Where it fits.** Interpretability tooling for TabPFN.

**What it contains.** Adapts popular interpretability methods to TabPFN's in-context inference
path (Table 1): ICE/PD/ALE with improved efficiency, Kernel SHAP and SAGE with *exact
retraining*, LOCO and leave-one-out made tractable, and Data Shapley for data valuation. The key
observation is that "retraining" a PFN on a feature or row subset is just a forward pass with a
different context, so methods that normally need approximate retraining become exact and cheap.
Data Shapley is then used for **context optimisation**: from a training set of n_train = 3072,
select a 512-row context; on three OpenML-CC18 datasets this beats random contexts by 0.57%
(eeg-eye-state), 1.52% (albert) and 3.3% (higgs) ROC AUC (§4.3). Released as the `tabpfn_iml`
package.

**Strengths.** Exact subset-retraining yields lower Shapley approximation error and variance
than imputation-based SHAP, making faithful attributions cheap.

**Limitations.** Binary classification only, small experiments (the Kernel SHAP comparison uses
n_train = 256 and six features), TabPFN v1 base, and the Data-Shapley context optimisation costs
nearly 10,000 forward passes.

---

## 2024-06 — Breugel and Schaar — Why Tabular Foundation Models Should Be a Research Priority

**Venue:** ICML 2024 (PMLR 235) · **arXiv:** [2405.01147](https://arxiv.org/abs/2405.01147) · **PDF:**
[open](papers/2024/06_Breugel_and_Schaar_Why_Tabular_Foundation_Models_Should_Be_a_Research_Priority.pdf)

**Where it fits.** Position / agenda paper. Pre-dates Real-TabPFN and TabPFN-2.5; argues that
tabular ML is an under-invested research area despite tabular data being the dominant modality
in many fields.

**What it contains.** Coins the term **Large Tabular Model (LTM)** for a tabular foundation model
and proposes four desiderata (D1–D4) for one (§2). It hypothesises **three reasons** LTMs have
been overlooked (§1): (1) data — a lack of large tabular metadatasets, messy or unlabelled tables,
and privacy/ownership limits on some domains; (2) the difficulty of tabular ML — strong
baselines that new methods may not consistently beat; (3) human perception — text and vision
outputs are easier for humans to judge. It then reviews the state of LTMs (§3), their potential
real-world impact (§4), challenges (§5), and compares LTM and LLM impact (§6), with appendix
taxonomies for evaluation tasks and settings.

**Strengths.** Crisp reusable design/evaluation checklist (D1–D4, adaptation and benchmark
taxonomies) that effectively framed the TFM research agenda.

**Limitations.** Purely argumentative — no numbers — and confined to single independent tables,
with diversity of web corpora and coverage of sensitive/proprietary domains left unproven.

---

## 2024-10 — den Breejen et al. — TabForestPFN

**Venue:** ICLR 2025 submission / OpenReview `pE0UM18TQh` (the copy held here is the
double-blind review version) · **PDF:**
[open](papers/2024/10_Breejen_et_al._Fine_tuned_In_Context_Learning_Transformers_are_Excellent_Tabular_Data_Classifiers.pdf)

**Where it fits.** The origin of the **tree-based prior**, and therefore a direct ancestor of
Mitra's prior-mixing framework, and an early argument that fine-tuning ICL transformers is
worthwhile rather than a compromise.

**What it contains.** Two findings that interact.

* **Fine-tuning gives ICL transformers complex decision boundaries.**
The paper extends TabPFN to the fine-tuning setting and reports a significant performance boost,
then observes *why*: fine-tuned ICL-transformers can form decision boundaries that ordinary
neural networks do not produce.
* **So pretrain on data that has complex boundaries, even if it is
unrealistic.** They build a **forest dataset generator** — synthetic tables sampled from
decision-tree/forest structures, explicitly described as unrealistic — and pretrain
**TabForest** on it. It fine-tunes better the more complex the pretraining data, and beats
TabPFN on some real datasets after fine-tuning *despite worse zero-shot performance*, precisely
because the prior is unrealistic.
* **TabForestPFN** is the combination: pretrain on both the TabPFN
generator and the forest generator, yielding good zero-shot *and* excellent fine-tuning
performance.

Evaluation uses **94 of the 176 TabZilla** classification datasets and the **23 WhyTrees**
(Grinsztajn et al.) medium-sized datasets. On WhyTrees, fine-tuned TabForest/TabForestPFN lead
the ICL variants (Table 2). On TabZilla, fine-tuned TabForestPFN is effectively tied with tuned
GBDTs: mean normalised accuracy 0.840 vs CatBoost 0.842 and XGBoost 0.836, with the best mean
rank (8.4, shared with fine-tuned retrained TabPFN) (Table 3).

**Strengths.** The zero-shot/fine-tuned trade-off is the insight worth carrying: prior realism
buys zero-shot quality, prior *complexity* buys adaptability, and they are not the same axis.
This directly motivates Mitra's later claim that priors should be selected on measured criteria
rather than realism intuitions.

**Limitations.** The copy held here is an anonymous review version rather than a camera-ready,
so final numbers may differ; it is classification-only; and its gains are demonstrated in the
fine-tuning regime, which means they do not transfer to a frozen-ICL deployment.

---

## 2024-11 — Helli et al. — Drift-Resilient TabPFN

**Venue:** NeurIPS 2024 · **arXiv:** [2411.10634](https://arxiv.org/abs/2411.10634) · **PDF:**
[open](papers/2024/11_Helli_et_al._Drift_Resilient_TabPFN_In_Context_Learning_Temporal_Distribution_Shifts_on_Tabular_Data_1.pdf)

**Where it fits.** TabPFN variant trained for distribution shift — realistic temporal evolution
of the data-generating process, rather than i.i.d. test data.

**What it contains.** Modifies TabPFN's SCM prior so that the causal model shifts gradually over
ordered temporal domains, covering covariate, prior and concept shift. The shifts are generated
by a **secondary (2nd-order) SCM** that takes the temporal domain index (Time2Vec-encoded) as
input and outputs weight shifts for selected edges of the primary SCM. Training domains precede
the test domains in this ordering, so the model learns to extrapolate the shift into future
domains from the context.

The empirical message: on 18 test datasets (8 synthetic, 10 real-world), Drift-Resilient TabPFN
improves OOD accuracy from 0.688 to 0.744 and ROC AUC from 0.786 to 0.832 over the strongest
baselines (XGBoost, CatBoost, TabPFN, Wild-Time methods), with better calibration. Domain
indices are known for synthetic data and approximated from time-encoding features on real data.

**Strengths.** Unifies covariate/prior/concept shift with strong OOD calibration gains (ECE
0.119→0.091) and no deploy-time tuning at ~11s for training and prediction combined.

**Limitations.** Gains are clearly stronger on synthetic than real-world datasets, ID performance
is lower than standard TabPFN, it needs (possibly approximated) temporal domain indices, and it
inherits v1's quadratic small-data ceiling with classification only.

---

## 2024-12 — Hoo et al. — TabPFN Outperforms Specialized Time Series Forecasting Models

**Venue:** NeurIPS 2024 Workshop on Time Series in the Age of Large Models (the early version of
what became [arXiv:2501.02945](https://arxiv.org/abs/2501.02945), expanded into the 2026 "From
Tables to Time" paper below) · **PDF:**
[open](papers/2024/12_Hoo_et_al._The_Tabular_Foundation_Model_TabPFN_Outperforms_Specialized_Time_Series_Forecasting_Models_Based_on.pdf)

**Where it fits.** Application paper rather than a method paper. Shows that a frozen TabPFN
matches state-of-the-art time-series *foundation models* when forecasting is reframed as tabular
regression on timestamp-derived features.

**What it contains.** Pipeline (TabPFN-TS): take a univariate time series, derive features
**directly from the timestamps only** — a running index plus sine/cosine-encoded calendar
components; lagged and rolling-window features are *deliberately excluded* (they conflict with
non-autoregressive multi-step prediction) — and feed each (features → value) pair to the TabPFN
regressor, predicting the whole horizon in one pass. Evaluated on 24 of the 29 datasets of the
AutoGluon-TS benchmark: despite only 11M parameters and zero time-series pretraining, TabPFN-TS
outperforms Chronos-Mini and matches or slightly beats Chronos-Large (65× more parameters).
Grouping by Chronos's own in-domain/zero-shot split shows Chronos wins where test sets overlap
its pretraining corpus, while TabPFN-TS wins decisively on the 17 truly zero-shot datasets.

The narrative is that TabPFN's synthetic prior — free of any real time-series pretraining, hence
of contamination — transfers to forecasting through feature engineering alone, where dedicated
TS foundation models rely on having seen similar series.

**Strengths.** Wins on the 17 true zero-shot datasets against Chronos-Large (0.772 vs 0.841
relative MASE) with a tiny model and no contamination risk, and ablations show the gain is
TabPFN-specific (CatBoost swap fails).

**Limitations.** Severe latency because each series is processed individually (Table 3: average
2,210 s per dataset vs Chronos-Large 148 s and Chronos-Mini 14 s), point-forecast
evaluation only, local univariate modelling with no covariates, and reliance on a closed hosted
checkpoint.

---

## 2024-12 — Feuer et al. — TuneTables

**Venue:** NeurIPS 2024 · NYU / U. Freiburg / U. Maryland / Abacus.AI · [DOI
10.52202/079017-2654](https://doi.org/10.52202/079017-2654) · arXiv
[2402.11137](https://arxiv.org/abs/2402.11137) · **PDF:**
[open](papers/2024/12_Feuer_et_al._TuneTables_Context_Optimization_for_Scalable_Prior_Data_Fitted_Networks.pdf)

**Where it fits.** The paper that defined the *context-optimisation* branch of TFM adaptation,
and the specific piece of prior art Rubachev 2025 (*On Finetuning Tabular Foundation Models*) later argued against. Where LoCalPFN localises
the context by retrieval and Real-TabPFN changes the weights, TuneTables changes what the
context *is* — making it the third distinct answer to "how do you adapt a frozen PFN?".

**What it contains.** The problem is stated bluntly: TabPFN performs very well on small tables
but is not designed to predict for datasets larger than ~1000 rows, and that ceiling blocks
adoption. TuneTables lifts it by **compressing a large dataset into a smaller learned context**
— a parameter-efficient fine-tuning strategy in which the context itself is optimised rather
than the network, the tabular analogue of prompt tuning. Concretely, a learned matrix of p
synthetic feature embeddings (with class-balanced initial labels) is optimised by gradient
descent on the full labelled set; at test time it is either prepended to real context rows (*C*)
or used alone (*NC*, "no context"), and NC is often as good or better. Last-layer retraining
extends the method beyond 10 classes; *TuneTables-medium* and *-light* trade a little accuracy
for speed.

The evaluation is unusually broad for the era: **nineteen algorithms across 98 datasets**, where
TuneTables achieves the **best average performance**, outperforming boosted trees including
CatBoost, while **optimising fewer than 5% of TabPFN's parameters**. Two secondary results widen
its relevance: the learned context can be read as an **interpretability tool**, and because the
context is optimised against an objective, it can be optimised against a **fairness objective**
to mitigate bias — a mechanism entirely different from FairPFN's prior-level approach to the
same goal. Code and raw results are open.

**Strengths.** The efficiency argument is strong (a sub-5%-parameter method beating tuned
CatBoost), the evaluation is wide, and the fairness-by-context-optimisation idea is genuinely
novel — it makes the context a place where constraints can be imposed, which no other paper here
exploits.

**Limitations.** It targets TabPFN **v1**, whose row ceiling v2 raised architecturally, so part
of the motivation evaporated; and Rubachev 2025 (*On Finetuning Tabular Foundation Models*) found that for v2 the "use parameter-efficient
methods to avoid destroying the prior" premise does not hold — full fine-tuning matches PEFT
variants while converging faster. Because of the prompt-training step, end-to-end runtime is
over 7× that of CatBoost and XGBoost (§4). Classification only.

---

<a id="localpfn"></a>


## 2024-12 — Thomas et al. — LoCalPFN

**Venue:** NeurIPS 2024 · Layer 6 AI, Toronto · [DOI
10.52202/079017-3442](https://doi.org/10.52202/079017-3442) · **PDF:**
[open](papers/2024/12_Thomas_et_al._Retrieval_Fine_Tuning_for_In_Context_Tabular_Models.pdf)

**Where it fits.** The retrieval branch of the adaptation literature, and — read alongside
[Nagler 2023, *Statistical Foundations of Prior-Data Fitted Networks*](#nagler-theory) — arguably the empirical answer to his localisation gap. Same lab
as TabDPT, which carries the same kNN-retrieved-context idea into pretraining.

**What it contains.** The diagnosis is that in-context learning had shown promise on small
tables but failed to scale to large, complex ones. The fix combines two mechanisms that each
address one half of the problem:

* **Retrieval** — instead of passing a global sample as context, collect
the **k nearest neighbours of the query** and pass that local subset, so the model is
conditioned on the region of feature space it is being asked about.
* **Fine-tuning on the retrieved context** — task-specific fine-tuning is
then performed with those neighbours in context, jointly rather than as a post-hoc step.

Retrieval alone, without fine-tuning, is **TabPFN-kNN**, which already lets TabPFN benefit from
larger datasets; kNN search uses the faiss library. Applied together to TabPFN, the two yield the **locally-calibrated PFN (LoCalPFN)**, evaluated on the **95
TabZilla datasets** curated from OpenML, where it sets a new state of the art — including
against *tuned* tree-based models — and shows a large gain over the base in-context model.

**Strengths.** The retrieve-then-fine-tune pairing is theoretically well-motivated (it is
localisation, which Nagler shows is what the bias term needs) and is the largest single reported
jump over base TabPFN in the v1 era.

**Limitations.** The costs are real: retrieval makes inference per-query rather than
per-dataset, which complicates deployment and assumes exchangeable rows; the method is
classification-focused; and it is built on TabPFN v1, so the scaling ceilings it lifts were
partly lifted by v2 architecturally instead.

---

<a id="tabpfn-v2-nature"></a>


## 2025-01 — Hollmann et al. — Accurate predictions on small data with a tabular foundation model

**Journal:** *Nature*, 2025 · **PDF:**
[open](papers/2025/01_Hollmann_et_al._Accurate_predictions_on_small_data_with_a_tabular_foundation_model.pdf)

**Where it fits.** The TabPFNv2 paper. Production-grade release that raises v1's limits about
10× in rows (1,000 → 10,000) and 5× in features (100 → 500) and ships in *Nature*.

**What it contains.** A re-architected v2 with alternating sample-attention / feature-attention
layers, targeting datasets of up to 10,000 rows × 500 features. Headline ingredients (the
NaN-handling and preprocessing class names below come from the `TabPFN .txt` code dump, not the
paper):

* **Synthetic prior expansion.** Far broader and deeper than v1's
prior; covers richer noise distributions, more diverse SCMs, and inputs with realistic
categorical / numerical mixes.
* **Architecture.** Stacked transformer with two attention
patterns interleaved per layer: "sample attention" treating each row as a token, and "feature
attention" treating each column as a token. The interleaving lets the model reason about both
row-level patterns (similarity, density) and column-level patterns (interactions, redundancy) in
one pass.
* **NaN handling.** Built into the encoder via
``NanHandlingEncoderStep`` — explicit indicator features plus learned default replacements.
Categorical handling via an internal ``OrdinalEncoder`` fitted at ``.fit(X, y)`` time.
* **Inference-time ensemble.** A pool of preprocessing
configurations (``PowerTransformer``, ``QuantileTransformer``, ``RobustScaler``,
``SquashingScaler``, ``"none"``); each estimator in the ensemble cycles through one
configuration, yielding diverse predictions that are averaged at inference.
* **Headline results.** Evaluated on the 29 AutoML Benchmark (AMLB)
classification datasets and 28 regression datasets (AMLB plus OpenML-CTR23) with ≤ 10,000
samples, ≤ 500 features and ≤ 10 classes, plus five Kaggle Tabular Playground competitions. In
2.8 s, default TabPFN outperforms an ensemble of the strongest baselines tuned for 4 h on
classification, and beats tuned CatBoost, XGBoost and AutoGluon.

**Strengths.** SOTA small-data accuracy for both classification and regression (normalized ROC
0.952 vs 0.822 tuned CatBoost; 3,000–5,140× speedups) with native distributional outputs,
robustness to messy data, and foundation-model abilities (fine-tuning, generation, embeddings).

**Limitations.** Hard caps (≤10k rows, ≤500 features, ≤10 classes), memory linear in table size,
slower per-sample inference than trees, weak very-non-smooth regression, and unreleased
prior-generation code.

---

## 2025-02 — Liu and Ye — TabPFN Unleashed

**arXiv:** [2502.02527](https://arxiv.org/abs/2502.02527) · **PDF:**
[open](papers/2025/02_Liu_and_Ye_TabPFN_Unleashed_A_Scalable_and_Effective_Solution_to_Tabular_Classification_Problems.pdf)

**Where it fits.** Adaptation method for TabPFN. Re-frames TabPFN's weaknesses through a formal
**bias–variance decomposition** of its generalisation error, then proposes a method (**BETA**:
Bagging and Encoder-based Fine-tuning for TabPFN Adaptation) that attacks both sides
simultaneously.

**What it contains.** The authors observe that previous TabPFN- improvement papers each address
either bias or variance, never both — and the resulting methods leave performance on the table.
BETA combines two complementary mechanisms.

* **Bias reduction via a lightweight learned encoder.** A small
parameter-efficient adapter sits between the raw features and TabPFN's internal embedding,
mapping datasets of arbitrary dimensionality into multiple fixed-dimensional latent
representations. This both addresses TabPFN v1's 100-feature limit and lets the model adapt to
the downstream task during fine-tuning.
* **Variance reduction via Batch Ensemble plus bootstrapped
sampling.** Multiple lightweight encoders run in parallel with parameter sharing (à la Wen 2020
/ Gorishniy 2025), each fed a bootstrap-sampled context. Their predictions are averaged,
smoothing out idiosyncrasies of any single sampled context set.

The method also integrates with Error-Correcting Output Codes (ECOC) to handle multiclass tasks
with > 10 classes, beyond TabPFN v1's class limit. BETA is built on TabPFN v1; the authors treat
TabPFN v2 as concurrent work that only partially alleviates these limits (§1 remark). Evaluated
on 186 TALENT classification datasets with ≤ 10 classes, where BETA outperforms or matches state
of the art while remaining computationally lightweight.

**Strengths.** Genuinely lightweight (0.6MB trainable, 0.91s inference) and best average rank on
186 TALENT datasets against XGBoost/CatBoost/LocalPFN/MixturePFN with default hyperparameters.

**Limitations.** Classification only on TabPFN v1, assumes IID (no drift handling), keeps a
fixed 1000-row context, and the encoder can overfit on very small datasets while discarding
raw-feature alignment with the prior.

---

<a id="mccarter-tabpfn"></a>

## 2025-02 — McCarter — What exactly has TabPFN learned to do?

**Venue:** ICLR 2024 Blogposts Track; filed as the expanded **13 February 2025 arXiv v1**,
including the TabPFN-v2 appendix · **arXiv:** [2502.08978v1](https://arxiv.org/abs/2502.08978v1) ·
**PDF:** [open](papers/2025/02_McCarter_What_exactly_has_TabPFN_learned_to_do.pdf)

**Citation key:** `2025.MCCARTER.whatexactlyhastabpfnlearned`.

**Where it fits.** A behavioural counterpart to Nagler 2023
(*Statistical Foundations of Prior-Data Fitted Networks*, [summary](#nagler-theory)):
inspect the predictor produced by a context rather than infer its behaviour from the
pretraining objective. It anticipates the symmetry concerns formalised by Arbel 2025
(*EquiTabPFN*, [summary](#equitabpfn)) and the retrieval interpretation in Shaheen 2026
(*Understanding the Surprising Generalization Properties of Tabular Foundation Models*,
[summary](#shaheen-retrieval)).

**What it contains.** One-dimensional classification probes vary duplicated features,
duplicated rows, class balance and periodic patterns; two-dimensional multiclass probes
compare decision regions with Voronoi partitions. In v1, duplicating all rows leaves the
predictions essentially unchanged, repeating features increases confidence, and ensembling
turns irregular multiclass regions into something resembling nearest-neighbour classification.
The tested periodic patterns are not recovered. Real-data probes include a 57-sample,
22,283-feature gene-expression dataset with both random and held-out-batch splits, plus
MNIST and CIFAR-10 treated as tables. Transfer is possible outside the intended tabular
regime, but logistic regression or SVC can still win.

The v2 appendix is essential: its default fingerprint features can distinguish repeated
rows but produce bumpier toy probability surfaces; cell embeddings make the widest experiments
impractical on the author's setup. Conversely, ensembled v2 exceeds **99% accuracy on
10-bit parity using 127 training examples**, about 12% of the truth table. Better benchmark
performance and more complex pattern recognition do not imply uniformly better behaviour
on simple probes.

**Strengths.** Transparent, reproducible stress tests expose specific inductive biases
that average benchmark ranks obscure. The expanded version tests both v1 and v2 and
includes positive as well as negative results.

**Limitations.** Exploratory blogpost and small case studies, not a comprehensive benchmark
or a mechanistic proof. The nearest-neighbour analogy is behavioural; it does not identify
the learned algorithm. V1's duplication result cannot be carried unchanged to v2, whose
fingerprinting changes the setup. No calibration or robustness guarantee follows from the
parity experiment, and the findings do not establish how later checkpoints behave.

---

## 2025-05 — Müller et al. — Position: The Future of Bayesian Prediction Is Prior-Fitted

**Venue:** ICML 2025 (PMLR 267) · **arXiv:** [2505.23947](https://arxiv.org/abs/2505.23947) · **PDF:**
[open](papers/2025/05_Muller_et_al._Position_The_Future_of_Bayesian_Prediction_Is_Prior_Fitted.pdf)

**Where it fits.** Position paper / manifesto from the original PFN authors.

**What it contains.** Argues that PFNs and other amortised inference approaches are the future of
*predictive* Bayesian inference. The argument:

* Inference algorithms for non-conjugate priors are slow and
brittle.
* PFNs amortise inference into one forward pass, with arbitrary
user-specified priors, and cannot leak test data because they pretrain on synthetic data.
* Real-world data is scarce and growing slowly in many domains while pretraining compute scales
fast; PFNs convert abundant compute into performance on data-scarce problems.

The research agenda is organised in three parts: **PFN extensions** (§4 — extra inputs such as
fairness or user knowledge, an in-context interpreter, BO via reinforcement learning, latent
prediction), **understanding PFNs** (§5 — martingale perspective, limit behaviour, impact of
prior density, interpretability), and **improving PFNs** (§6 — scaling to more samples,
focusing pretraining on hard datasets, fast inference, adaptive compute, architectural
limitations).

**Strengths.** Endorses post-pretraining ensembling and fine-tuning in domains with many related
datasets (§6.1) and names calibrated uncertainty a core PFN advantage.

**Limitations.** Conceptual/roadmap only, with honestly stated open problems: ill-defined
support, O(n²) attention, inability to count duplicated evidence, and degraded handling of
heavy-tailed/heterogeneous features.

---

<a id="tabicl-2025"></a>

## 2025-05 — Qu et al. — TabICL

**Venue:** ICML 2025 (PMLR 267) · **arXiv:** [2502.05564](https://arxiv.org/abs/2502.05564) · **PDF:**
[open](papers/2025/05_Qu_et_al._TabICL_A_Tabular_Foundation_Model_for_In_Context_Learning_on_Large_Data.pdf)

**Where it fits.** Direct competitor to TabPFN. Different architectural approach; pretrained on
datasets of up to 60K rows, it handles 500K samples × 500 features with about 20 GB of GPU memory
by offloading intermediate activations to CPU or disk (App. E).

**What it contains.** TabICL ("Tabular In-Context Learning") adopts a **two-stage** architecture
instead of TabPFNv2's flat column-then-row alternation. First, each row is collapsed into a
single dense vector via a column-then-row attention block: distribution-aware column-wise
embedding (a Set-Transformer-style operation that treats each column as a permutation-invariant
set of cell values, enabling cross-table transferability), then within-row attention to model
feature interactions, then a [CLS]-token aggregation that produces a fixed-dimensional row
embedding. Second, ICL runs over these row embeddings — collapsing the column dimension *before*
in-context learning sidesteps TabPFNv2's `O(n²m + nm²)` cost.

The pretraining adds a tree-based synthetic prior (decision-tree ensembles) on top of the
standard SCM prior to inject GBDT-flavoured inductive biases, plus curriculum learning that
scales the pretraining dataset size from 1k → 60k rows. To handle > 10 classes (the pretraining
limit) the model uses hierarchical classification. Empirically, on the TALENT benchmark's 53
large datasets above 10 k rows TabICL **surpasses both TabPFNv2 and CatBoost**, while on smaller
datasets it matches TabPFNv2 at up to 10× faster inference.

**Strengths.** Order-of-magnitude row scalability with strong calibration (LogLoss), plus a
portable "freeze backbone, train ICL head" adaptation blueprint and memory-offload inference
tricks.

**Limitations.** Classification-only, slow inference, RoPE breaks column-permutation invariance
(patched by ensembling), and its architecture diverges from TabPFNv2 so recipes are not directly
transferable.

---

## 2025-06 — Robertson et al. — FairPFN

**arXiv:** [2506.07049](https://arxiv.org/abs/2506.07049) · **PDF:**
[open](papers/2025/06_Robertson_et_al._FairPFN_A_Tabular_Foundation_Model_for_Causal_Fairness.pdf)

**Where it fits.** Causal-PFN sibling of Do-PFN, this time aimed at the **causal-fairness**
problem rather than treatment-effect estimation. Addresses the limitation that current
causal-fairness frameworks require the user to specify the correct causal model — a tall ask in
practice and a source of "fairwashing" when the specified graph is wrong.

**What it contains.** Pretraining recipe:

* **Synthetic causal-fairness data prior.** Sparse MLPs
represent SCMs whose root nodes include exogenous protected attributes (binary: race / gender /
age). For each SCM, the paper samples both a *biased* dataset (with the protected attribute's
full causal influence) and a *fair* counterpart obtained by removing the outgoing edges of the
protected attribute — i.e. by simulating the counterfactual world in which the protected
attribute had no causal influence on the outcome.
* **Training objective.** The transformer sees the biased
observational dataset as context and is trained to predict the *fair* outcomes from the
counterfactual world. Loss is computed against the fair targets, so the network learns to
internally identify and remove the causal effect of the protected attribute.
* **At inference time**, FairPFN takes only the biased
observational data and produces fairer predictions, integrating over the simplest causal
explanations consistent with the observed bias. **No user-specified causal graph is needed.**

The paper demonstrates strong performance on hand-crafted causal case studies and two
real-world datasets with assumed causal graphs (Law School Admissions and Adult Census Income,
§5.3), relative to robust baselines. FairPFN is a fair *predictor* — it outputs predictions with
the protected attribute's causal effect removed — rather than an auditing tool.

**Strengths.** Demonstrates a prior can encode a task transformation (not just a data
distribution), with honest failure-mode ablations that gracefully revert to a plain classifier —
a useful evaluation pattern.

**Limitations.** Single binary exogenous attribute, binary classification only, two real
datasets with circular DoWhy-based "ground truth," and no calibration analysis.

---

<a id="on-finetuning"></a>


## 2025-06 — Rubachev et al. — On Finetuning Tabular Foundation Models

**arXiv:** [2506.08982](https://arxiv.org/abs/2506.08982) · **PDF:**
[open](papers/2025/06_Rubachev_et_al._On_Finetuning_Tabular_Foundation_Models_1.pdf)

**Where it fits.** Empirical study of finetuning tabular FMs on downstream datasets. The closest
published reference for single-dataset gradient-adaptation hyperparameters.

**What it contains.** A controlled study of **TabPFNv2** adaptation: full gradient updates,
LoRA, last-layer tuning, LayerNorm/head/embedding tuning, and numerical-feature embeddings,
across classification and regression datasets. Headline findings:

* **Full finetuning is the practical default.** It performs similarly
to the partial/PEFT alternatives while converging faster; the paper does not support a blanket
claim that LoRA recovers a fixed percentage of the gain.
* **Learning rate is tuned per dataset** on ten log-spaced values from
5e-6 to 5e-4. Each step scores 1 024 prediction objects while the remaining rows form the
context.
* **Early stopping** evaluates the validation subset every ten gradient
steps and stops after 16 non-improving evaluations.
* **Mechanism.** Finetuning sharpens the alignment between test-query
and context-key representations, improving TabPFNv2's retrieval-like weighting of relevant
in-context examples.

The negative results concern **temporal shift**: on subsampled TabReD datasets (gradual temporal
shift, rich feature sets) TabPFNv2 is less stable and prior methods such as TabM remain better;
finetuning improves the in-context model on almost all of them but often degrades Sberbank
Housing (§5.2).

The local ``repositories/On Finetuning Tabular Foundation Models.txt`` dump belongs to this
Rubachev study. It is **not** a Real-TabPFN code release. The studies answer complementary
questions: Rubachev adapts one target dataset at a time; Garg continues pretraining one model
across a 71-table corpus.

**Strengths.** Rare mechanistic explanation plus practical knobs to copy (LR logspace grid,
1024-object prediction batch, patience-16 early stopping, FT×5 ensembling), with honest negative
results under temporal shift.

**Limitations.** Accuracy/RMSE-only evaluation — no AUC, logloss, or calibration — leaving open
whether retrieval sharpening harms calibration, and instability on temporally shifted TabReD data
warns against i.i.d.-only evaluation.

---

## 2025-06 — Ye et al. — A Closer Look at TabPFN v2

**arXiv:** [2502.17361](https://arxiv.org/abs/2502.17361) · **PDF:**
[open](papers/2025/06_Ye_et_al._A_Closer_Look_at_TabPFN_v2_Understanding_Its_Strengths_and_Extending_Its_Capabilities.pdf)

**Where it fits.** Mechanistic analysis of TabPFNv2 (rather than a new architecture). Asks two
questions: *how* does v2 cope so well with heterogeneous tabular data, and *how* can its known
limits — 10 000 samples × 500 features × 10 classes — be lifted without retraining? Three
concrete findings.

**What it contains.**

1. **TabPFN v2 internalises attribute-token learning.** Unlike
prior tabular methods that rely on word-vector–style attribute semantics or learn
dataset-specific attribute tokens, v2 uses **randomly resampled attribute tokens at every
inference call**. The paper's analysis shows that v2 still consistently infers attribute
relationships *through ICL itself* — effectively integrating "what this column means" learning
into the same forward pass that produces predictions. This is what lets v2 transfer across
datasets with different schemas and dimensionalities without per-dataset adaptation.
2. **TabPFN v2 can be repurposed as a feature extractor.** Using
a leave-one-fold-out strategy that aligns training and test embeddings, the authors show v2 maps
tabular instances into a *near-linearly-separable* embedding space. Training a plain linear
model on those embeddings recovers most of v2's accuracy — meaning v2 is implicitly learning a
strong general- purpose tabular representation, not just a classifier.
3. **Test-time divide-and-conquer mitigates the
10 k × 500 × 10 limits.** Instead of retraining v2 on bigger data, the paper proposes post-hoc
strategies analogous to LLM test-time scaling (§7): **decimal-digit label encoding** for
many-class tasks (one v2 per digit of the class index, with random class-to-digit permutations
ensembled); random **feature-subset bagging** for wide tables; and for large-N data, **-SQ**
(10,000-row support set, v2 embeddings for the rest, a linear head, repeated four times) and
**-DF** (a forest of shallow decision trees that partitions the data, with v2 applied per
leaf). Empirical gains across all three limit regimes.

**Strengths.** Rigorous evaluation over many datasets with per-dataset results in the appendix,
a leakage-safe leave-one-fold-out embedding diagnostic, and documentation of the large-N
degradation of frozen v2.

**Limitations.** No training-side contribution (causes hypothesized, not tested), extensions
multiply inference cost yet still lose to CatBoost/RealMLP at scale, and evaluation is
accuracy/RMSE only with no calibration metrics.

---

<a id="real-tabpfn"></a>


## 2025-07 — Garg et al. — Real-TabPFN

**Venue:** 1st ICML Workshop on Foundation Models for Structured Data (2025) · **arXiv:**
[2507.03971](https://arxiv.org/abs/2507.03971) · **PDF:**
[open](papers/2025/07_Garg_et_al._Real_TabPFN_Improving_Tabular_Foundation_Models_via_Continued_Pre_training_With_Real_World_Data.pdf)

**Where it fits.** The reference recipe for **corpus-level continued pretraining**: take the
released synthetic-only TabPFNv2 checkpoint and continue pretraining it on a curated set of
real-world tables from OpenML and Kaggle.

**What it contains.**

* **Method.** Take the synthetic-only TabPFNv2 checkpoint and
continue pretraining on a hand-curated corpus of 71 datasets (≥ 10 000 rows each, mixture of
OpenML and Kaggle). *Minimal* preprocessing: ``OrdinalEncoder`` for categoricals, and if the
target has more than 10
classes, retain the nine most common and merge the remainder into a tenth "other". No
imputation, no scaling beyond what TabPFN does internally.
* **The actual Real-TabPFN recipe** (stated directly in Garg et al.):
full-model continued pretraining with **AdamW, LR 3e-7, linear warmup followed by cosine
annealing, and L2-SP λ=0.003** toward the synthetic checkpoint. It runs for **20 000 steps**,
batch size one table, samples up to 20 000 rows / 400 000 cells, and splits each table 60%
context / 40% query. The paper does not report AdamW's weight-decay value. At each step the
table is drawn from a **71-dataset corpus**; batch size one does not make this a single-dataset
finetuning study.
* **Data contamination protocol** (their §3) — a five-tier
filter: (1) only datasets > 10k samples (every evaluation dataset is smaller, so size alone
separates pretrain from eval); (2) cross-reference IDs / names / shapes; (3) compare feature
names; (4) row and column hashes; (5) manual metadata inspection for shared or subsampled
sources.
* **Headline result.** On 29 datasets from the OpenML AutoML
Benchmark, Real-TabPFN improves normalised ROC-AUC by +0.022 vs. default TabPFNv2 (Wilcoxon
signed-rank ``p = 0.0045``). The Wilcoxon test confirms this is a per-dataset improvement, not
just an average bump driven by a few outliers.
* **Ablations.** OpenML alone: +0.019. Kaggle alone: +0.015.
Union: +0.022 — heterogeneous sources are complementary. CommonCrawl as a continued-pretraining
corpus *hurts* performance (the average dataset there is only ~100 rows × 7 features — too small
to give TabPFN useful signal). GitTables (avg ~1000 rows × 9 features) helps, but less than
OpenML+Kaggle (avg 10k–100k rows × 10s of features).
* **Context-size scaling.** Continued-pretraining gains grow with
the context size used during continued pretraining: 2k → 20k context yields a monotonic
improvement curve (Figure 4 in the paper).

**Attribution warning.** There is **no public Real-TabPFN code release**. The local
``repositories/On Finetuning Tabular Foundation Models.txt`` dump belongs to **Rubachev et
al.**, not to Garg et al. — do not read that repository's hyperparameters as Garg's recipe. A
second, genuinely official reference point is the Prior Labs finetuning wrapper shipped in the
package (``FinetunedTabPFNClassifier``: 30 epochs, LR 2e-5, ``n_estimators_finetune`` 2;
``FinetunedTabPFNRegressor``: 30 epochs, LR 1e-5, ``n_estimators_finetune`` 8,
``n_finetune_ctx_plus_query_samples`` 20 000), but that is *single-dataset* finetuning, not
corpus continued pretraining.

**Strengths.** Cheap and reproducible (single consumer GPU) with statistically significant gains
(normalized ROC-AUC 0.954→0.976, p=0.0045), better calibration, and clean ablations isolating
dataset size as the driver (small CommonCrawl tables hurt).

**Limitations.** Workshop-length, classification only (no regression), 29 small eval datasets,
modest absolute ROC gains, and no sensitivity analysis on λ/LR/steps or parameter-efficient
variants.

---

<a id="mitra"></a>


## 2025-10 — Zhang et al. — Mitra: Mixed Synthetic Priors

**Venue:** NeurIPS 2025 · **arXiv:** [2510.21204](https://arxiv.org/abs/2510.21204) · **PDF:**
[open](papers/2025/10_Zhang_et_al._Mitra_Mixed_Synthetic_Priors_for_Enhancing_Tabular_Foundation_Models.pdf)

**Where it fits.** Alternative pretraining recipe from Amazon / AutoGluon team. Argues that the
right way to improve TFMs is *not* to add architectural complexity but to **design better
synthetic priors** — and proposes a principled framework for mixing them. Pretrained model is
open-source on HuggingFace as ``autogluon/mitra-classifier`` and ``autogluon/mitra-regressor``.

**What it contains.** The paper formalises three properties a good synthetic prior should have,
and operationalises each as a measurable score:

1. **Standalone performance** — a TFM pretrained *only* on this
prior should already do well on real data.
2. **Diversity** — a TFM pretrained on this prior should not
easily overfit to its own distribution (i.e. the prior covers a wide range of generative
mechanisms).
3. **Distinctiveness within a mixture** — data sampled from this
prior should be hard for TFMs trained on *other* priors to predict, meaning it adds something
the other priors miss.

The first is captured by a per-prior performance vector P; the latter two by a "Generalisability
Matrix" G with diagonal entries measuring overfitting and off-diagonal entries measuring inter-
prior overlap. Using these criteria the authors select a final mixture of **SCMs + tree-based
priors** (gradient boosting, random forest, decision tree, extra-tree). SCMs deliver standalone
performance and diversity; tree-based priors are distinctive (TFMs pretrained on SCMs alone
struggle on TBP- generated data, so adding TBPs covers ground SCMs miss).

The mixture is model-agnostic: it improves both flat row-attention architectures (à la TabPFN)
and 2D cell-attention architectures. **Mitra outperforms TabPFNv2 and TabICL on both
classification and regression benchmarks**, with better sample efficiency.

**Strengths.** Its explanation of why fine-tuning helps — compensating the pretrain/downstream
distribution gap — is a clear mechanism, and the bagged-CV ensemble,
regression checkpoint, and generalizability-matrix methodology are directly portable.

**Limitations.** Thin margins over Attic (8 Elo, overlapping CIs), tiny pretraining regime (16
features/640 rows) that loses to TabPFNv2 on wide regression, greedy prior selection risking
meta-overfitting, and no calibration analysis.

---

<a id="apt"></a>


## 2025-10 — Wu and Bergman — APT (Adversarially Pre-trained Transformer)

**Venue:** ICML 2025 (PMLR 267), Vancouver · University of California, Berkeley + **Capital
One** · **PDF:**
[open](papers/2025/10_Wu_and_Bergman_Zero_shot_Meta_learning_for_Tabular_Prediction_Tasks_with_Adversarially_Pre_trained_Transformer.pdf)

**Where it fits.** A prior-design paper, and the second in this collection after
[O'Prior](#oprior) to treat the synthetic task distribution as the variable rather than the
backdrop — but by a different route. O'Prior compares *fixed* generators against each other; APT
makes the generator **adaptive**, letting it react to the model it is training. It also attacks
the class-count cap, which [EquiTabPFN](#equitabpfn) attacks two months later by an unrelated
mechanism — two independent answers to the same weakness, and a good illustration that it was a
real one.

**What it contains.** Two contributions. First, **adversarial synthetic data agents**: alongside
the ordinary random generators, a fraction of the pretraining data comes from agents that
continuously shift their own data-generating distribution to produce datasets the model
currently handles badly. Only 12.5% of generators are adversarial (lr 1e-1, weight decay 1e-5,
soft-discretisation temperature 1e-2, resets every 2,000 gradient steps) — a small perturbation
of the prior, not a replacement. Second, a **mixture block** output design that handles an
arbitrary number of classes, removing the fixed-width final layer that caps PFN classification.

The evaluation is unusually honest about scope. On the 35 OpenML-CC18 datasets with ≤2,000 rows,
**no filtering is applied** on class count, feature count, categorical features or missing
values — the filters TabPFN v1's headline result relied on. Given a one-hour budget per
algorithm:

| | mean rank ↓ | ROC-AUC ↑ | wins | time (s) |
|---|---|---|---|---|
| **APT** | **3.86** | **0.921** | **13** | **0.90** |
| CatBoost | 4.03 | 0.918 | 6 | 3,542 |
| TabPFN | 4.57 | 0.913 | 4 | 0.86 |
| XGBoost | 5.37 | 0.914 | 4 | 3,608 |

Regression is checked separately on OpenML-CTR23, where adversarial pretraining also improves on
TabPFN. An analysis section shows the adversarial agents produce a measurably more diverse
dataset collection than the ordinary generator, and that the mixture block both generalises to
unseen class counts and accelerates pretraining convergence.

**Strengths.** The adversarial generator is a genuinely different lever on the prior from
anything else here: Mitra *mixes* fixed priors, O'Prior *compares* them, APT lets the prior
chase the model's weaknesses. Dropping the dataset filters is the right call and makes the
comparison mean something. Beating tuned CatBoost on rank while running ~4,000× faster is the
practical headline. And like [Luo et al. 2026, *Memory Efficient Tabular Foundation Models*](#memory-efficient-tfms), it is written partly from inside a
deploying institution — Capital One — which is still rare in this collection.

**Limitations.** The baseline is **TabPFN v1** (with its class cap merely raised from 10 to 26
for fairness), not v2, so the comparison is a generation behind by the time of publication. APT
does not beat GBDTs on large datasets and inherits TabPFN's quadratic attention cost, which the
paper acknowledges and does not solve. The regression evidence is thinner than the
classification evidence, and there is no calibration analysis.

---

## 2025-11 — Robertson et al. — Do-PFN

**Venue:** NeurIPS 2025 · **arXiv:** [2506.06039](https://arxiv.org/abs/2506.06039) · **PDF:**
[open](papers/2025/11_Robertson_et_al._Do_PFN_In_Context_Learning_for_Causal_Effect_Estimation.pdf)

**Where it fits.** First PFN published for causal-effect estimation. Predates the unified
CausalFM framework (Ma 2026) by ~6 months and focuses specifically on **conditional
interventional distributions** — the answer to "what would the outcome distribution look like
under an intervention that sets treatment t?", given only observational data.

**What it contains.** Pretraining recipe:

* **Sample millions of SCMs.** Each SCM has explicit treatment
variables, outcome variables, and confounders. Importantly, the prior covers a wide variety of
causal structures including cases where unconfoundedness *fails*.
* **For each SCM, sample two datasets simultaneously**: one
observational (no interventions) and one interventional (forced ``do(T = t)``). The transformer
is given the *observational* dataset as context and is trained to predict the *interventional*
outcomes — meta-learning the act of causal inference itself.
* **At inference time**, the model sees only an observational
dataset and a query intervention; the network outputs an estimate of the causal effect with
calibrated uncertainty.

The crucial property: Do-PFN does **not** require the user to specify the causal graph, and does
**not** rely on the unconfoundedness assumption that classical CATE estimators need. Where the
effect is genuinely unidentifiable (e.g. an unobserved confounder), Do-PFN does not "correct"
the confounding; its predictive uncertainty grows instead, and the PICP analysis shows it
captures that increase (§4.4).

Baselines are meta-learners, doubly robust and deep-learning CATE estimators plus DoWhy "gold
standard" variants given the true graph. On synthetic case studies Do-PFN performs strongly,
especially when unconfoundedness is violated; on the semi-synthetic RealCause benchmarks — which
satisfy unconfoundedness and so favour the baselines — it is **competitive** (§4.5).

**Strengths.** Strong where unconfoundedness is violated, with principled uncertainty that
inflates in unidentifiable cases and is overall well calibrated.

**Limitations.** Binary treatments only, validation is mostly synthetic, the base model is
pretrained on graphs of up to 10 nodes (a 60-node v1.1 was needed for larger graphs), and the
uncertainty is slightly under-confident in identifiable cases, which the authors attribute to
bar-distribution discretisation and imperfect loss minimisation.

---

## 2025-11 — Zhang et al. — TabPFN: One Model to Rule Them All

**arXiv:** [2505.20003](https://arxiv.org/abs/2505.20003) · **PDF:**
[open](papers/2025/11_Zhang_et_al._TabPFN_One_Model_to_Rule_Them_All.pdf)

**Where it fits.** A statistician's appraisal of TabPFNv2, written for a *Statistical
Science*-flavoured audience rather than an ICML one. Provides a careful re-derivation of how
TabPFN works as **approximate Bayesian inference**, and uses that lens to identify several
application domains in which out-of-the-box TabPFN matches or beats domain-specific
state-of-the-art methods.

**What it contains.** First a tailored explanation of TabPFN for statisticians (§2), then three
case studies (§3), each comparing an out-of-the-box TabPFN with the state-of-the-art method of a
recent paper in a top statistics journal, on that paper's own simulation set-up plus real data:

* **Semi-supervised parameter estimation** (§3.1) — TabPFN, fitted on
the labelled set, **imputes labels** for labelled and unlabelled rows, and the parameter is
estimated by ERM on the imputed data, with (TabPFN-D) or without (TabPFN-I) a debiasing
correction. It can outperform the specialised method.
* **Heterogeneous treatment-effect estimation** (§3.2) — TabPFN as
the base learner inside S-, T-, X-, R- and DR-learners; S-Learner (TabPFN) is among the most
accurate.
* **Prediction under covariate shift** (§3.3) — plain TabPFN, with no
shift-specific modification, against importance-weighting and pseudo-labelling approaches.

A key theoretical observation: **TabPFN can adapt to both nonparametric *and* parametric
structure simultaneously**. Sometimes outperforms LASSO even when the data is genuinely
sparse-linear (i.e. when LASSO's modelling assumptions are correctly specified) — because
TabPFN's implicit prior over SCMs already covers sparse-linear data, plus everything else. This
blurs the classical bias-variance trade-off and makes TabPFN attractive as a *default* tabular
regressor / classifier even in regimes where simple parametric models are usually preferred.

**Strengths.** Unique calibration/robustness evidence — near-nominal coverage, label-noise
consistency to ρ=0.4, and covariate-shift wins — supporting the reading of v2 as approximate
Bayesian inference.

**Limitations.** Purely empirical with no theory for the implicit-regularization benefits, and
documents the exact ceilings a downstream user must work around: MSE plateau at n≳10K,
~500-feature cap, dense high-d regression failures, and no weighted-loss support.

---

## 2025-11 — Bouadi et al. — Orion-MSP

**arXiv:** [2511.02818](https://arxiv.org/abs/2511.02818) · Lexsi Labs (India / France) ·
**PDF:**
[open](papers/2025/11_Bouadi_et_al._Orion_MSP_Multi_Scale_Sparse_Attention_for_Tabular_In_Context_Learning.pdf)

**Where it fits.** One of the two Orion architectures from Lexsi Labs — the models benchmarked
by that lab's own TabTune library and fine-tuning study, both of which this library already
holds. Holding the tooling papers without the model papers left an obvious gap.

**What it contains.** Orion-MSP **extends the TabICL architecture** (column embedding → row
interaction → ICL). The paper names three limitations of TabPFN- and TabICL-style architectures
and addresses each:

1. **Single-scale feature processing** overlooks hierarchical
dependencies → **multi-scale processing** to capture feature interactions at several
granularities.
2. **Dense attention scales quadratically in table width** →
**block-sparse attention** combining windowed, global and random patterns, keeping long-range
connectivity at lower cost.
3. **Strictly sequential components** prevent iterative refinement →
an *optional* **Perceiver-style memory** (Alg. 2) allowing bidirectional information flow between
components, so the column and row stages can inform each other instead of running once in
sequence.

Across TALENT, OpenML-CC18 and TabZilla, Orion-MSP has the best overall zero-shot mean rank
(3.58, vs TabPFN 4.61 and TabDPT 5.42; Table 1). By width (Table 3) it leads on narrow tables,
but on wide tables (> 100 features) its rank is 5.69, behind XGBoost (4.79) and CatBoost (5.50).
Weights and code are public.

**Strengths.** The bidirectional-memory point is a genuine architectural observation: the
three-stage consensus design (column → row → ICL) is strictly feed-forward, and there is no
principled reason it should be.

**Limitations.** Evaluation is by the authors of the benchmark library used to evaluate it —
Lexsi Labs' own TabTune and fine-tuning study place Orion models at or near the top of their
leaderboards — so independent replication matters more here than usual, and no calibration
analysis is reported.

---

<a id="spectral-adaptivity"></a>

## 2025-11 — Zheng et al. — From Tables to Signals: Revealing Spectral Adaptivity in TabPFN

**arXiv:** [2511.18278](https://arxiv.org/abs/2511.18278) · preprint ·
Australian Institute for Machine Learning, University of Adelaide ·
**PDF:** [open](papers/2025/11_Zheng_et_al._From_Tables_to_Signals_Revealing_Spectral_Adaptivity_in_TabPFN.pdf)

**Where it fits.** One of the handful of papers here that tries to explain *why* TabPFN works
rather than to make it work better, and the third distinct mechanism offered.
[Nagler 2023, *Statistical Foundations of Prior-Data Fitted Networks*](#nagler-theory) argued
analytically that a PFN's variance vanishes for free but its bias vanishes only under
**localisation**;
[Shaheen et al. 2026, *Understanding the Surprising Generalization Properties of Tabular
Foundation Models*](#shaheen-retrieval) argued empirically that the learned procedure is
**retrieval-and-aggregation**. Zheng et al. add a **frequency** account — and the three converge
rather than compete, because the paper's own attention maps sharpen into local neighbourhoods as
context grows. That is localisation, measured spectrally.

**What it contains.** Two definitions and three experiments.

The **context kernel** (Definition 1) is the paper's portable contribution. The Neural Tangent
Kernel is meaningless for an in-context model, since there are no gradient updates to
differentiate through, so the authors define the analogous object for ICL: the Jacobian of
predicted query outputs with respect to *context labels*,

> `K_context := ∂g(X_q; X_c, y_c) / ∂y_c  ∈ R^{M×N}`

For a single attention block this collapses to the softmax attention matrix itself, which is
what makes it interpretable rather than merely formal.

**Spectral adaptivity** is what the kernel reveals. A ReLU-MLP's spectral bias evolves over
*training epochs* and is otherwise fixed once the architecture is chosen; TabPFN's effective
bandwidth instead expands with the *number of in-context samples*. Empirically the context
kernel's eigenvalues decay more slowly and its effective rank grows as sampling density rises,
and TabPFN's spectral response without any tuning already matches a well-trained deep MLP.
Self-attention maps become sharper and more local with more context, with an SVD confirming
progressively higher-rank attention.

Two consequences follow. **Positional encoding acts as a frequency dial**, mirroring the
implicit-neural-representation literature — which retrospectively explains why positional
encoding turned out to be necessary to use TabPFN on time series, as in
[Hoo et al. 2026, *From Tables to Time*](#from-tables-to-time). And TabPFN can be used
**without any training** for image denoising: patch the image, regress the pixels, and it beats
WIRE, SIREN, MFN, Gauss and ReLU(+PE) baselines on both peak PSNR and runtime, with a single
regressor nearly matching an 8-member ensemble.

**Strengths.** The context kernel is a genuinely reusable definition — it gives the field an
NTK-shaped tool where none existed, and it is cheap to compute. The paper explains an existing
empirical practice instead of merely adding another one, which is rarer here than it should be.
The denoising result is a striking demonstration that a model marketed as *tabular* is closer to
a general training-free implicit signal model, and it costs almost nothing to reproduce.

**Limitations.** The context kernel relies on a local linearisation of a nonlinear transformer,
so how spectral adaptivity actually emerges from full attention dynamics — and from the
pretraining prior — is left open; the analysis describes the phenomenon more than it derives it.
Everything is measured on the TabPFN v2 line, so whether it holds for the row-compression
architectures ([TabICL](#tabicl-2025), [TabPFN-3](#tabpfn-3)) is untested. The vision
experiments are bounded by TabPFN's context window and input dimensionality, and the patching
needed to work around that introduces blending artefacts a globally trained INR does not have.
Most importantly for this library, 1D and 2D signal reconstruction are a long way from real
tabular data: the bridge is suggestive, not yet established where it would matter.

---

## 2025-12 — Pfefferle et al. — nanoTabPFN

**Venue:** AI for Tabular Data workshop at EurIPS 2025 · **arXiv:**
[2511.03634](https://arxiv.org/abs/2511.03634) · **PDF:**
[open](papers/2025/12_Pfefferle_et_al._nanoTabPFN_A_Lightweight_and_Educational_Reimplementation_of_TabPFN.pdf)

**Where it fits.** Educational reimplementation — the TabPFN v2 architecture and a training loop
in under 500 lines of PyTorch, versus over 10,000 in the TabPFN repository.

**What it contains.** A simplified TabPFN v2 model and training loop, designed to be readable
end-to-end:

* Training reads **pre-generated prior data from an HDF5 dump**; the
repository has no prior implementation of its own (the paper's data were generated with
TabICL's prior, App. A).
* The TabPFN-v2-style model — a feature encoder (training-set
normalisation plus outlier clipping), a target encoder, layers alternating attention between
features and between datapoints, and an MLP decoder producing class logits.
* A ``train()`` loop using schedule-free AdamW without weight decay.

The demo run trains a 3-layer, 96-dimensional model on **80,000 synthetic datasets of 150 rows ×
5 features × 2 classes** for about one minute on one RTX 2080 Ti — reported as over 160,000×
less compute than TabPFN v2 pretraining. Within 60 s it beats default scikit-learn kNN, decision
tree and random forest in ROC AUC, and shortly after it beats TabPFN with ensembling and
preprocessing disabled — not default TabPFN (§4).

**Strengths.** Exposes in readable form the core mechanisms of a TabPFN-style model (encoders,
two-axis attention, training loop), with a pretraining run cheap enough for teaching.

**Limitations.** Classification-only, no regression, missing-value handling or preprocessing
ensembles, no prior implementation, tiny-data regime, and the speed comparison is
apples-to-oranges (a model trained at exactly the evaluation scale vs a general model).

---

## 2025-12 — Tanna et al. — TabTune

**arXiv:** [2511.02802](https://arxiv.org/abs/2511.02802) · **PDF:**
[open](papers/2025/12_Tanna_et_al._TabTune_A_Unified_Library_for_Inference_and_Fine_Tuning_Tabular_Foundation_Models.pdf)

**Where it fits.** Software / benchmark paper from Lexsi Labs. A unified,
scikit-learn-compatible Python library that standardises the entire workflow — inference,
fine-tuning, evaluation — across seven tabular FMs: TabPFN, TabDPT, TabICL, Mitra, ContextTab,
OrionMSP and OrionBiX.

**What it contains.** TabTune addresses four operational frictions that have been slowing TFM
adoption in practice:

* **Diverse preprocessing requirements** — each TFM expects its
own data encoding (TabPFN wants numerically encoded categoricals consistent with its synthetic
priors, TabICL wants set-transformer embeddings for categoricals, etc.). TabTune handles the
per-model preprocessing internally.
* **Fragmented APIs and training protocols** — TabTune exposes four
adaptation strategies under one interface: zero-shot inference, **meta-learning** (episodic
fine-tuning on support–query splits), supervised fine-tuning (SFT), and PEFT via **LoRA**
(applicable to both SFT and meta-learning), with per-model support recorded in a matrix
(Table 2).
* **Evaluation gaps in deployment-relevant metrics** — beyond
accuracy, the library ships built-in calibration (Expected Calibration Error, Maximum
Calibration Error, Brier score) and fairness diagnostics (Statistical Parity Difference,
Equalised Odds Difference, Equalised Opportunity Difference).
* **Model selection complexity** — a benchmarking module
consistently ranks models on accuracy, calibration, fairness and resource efficiency on standard
suites (TALENT, OpenML-CC18, TabZilla).

The library targets the "experimental bed" use-case: study how zero-shot vs. PEFT vs. SFT trades
off across calibration, fairness, and compute, all under one harness.

**Strengths.** Useful cross-model evidence on how adaptation interacts with architecture: under
full SFT, TabPFN gets the best overall rank (1.97) while keeping ECE at 0.027–0.047, TabDPT (2.79)
and OrionMSP (2.88) remain competitive, whereas TabICL and OrionBiX degrade severely (TabICL's
TabZilla accuracy falls from 0.873 to 0.567).

**Limitations.** Classification-only, single untuned defaults per strategy, author-model
conflict of interest (Orion), no significance tests, and per-dataset fine-tuning only — nothing
on corpus-level continued pretraining.

---

## 2025-12 — Balazadeh Meresht et al. — CausalPFN

**Venue:** NeurIPS 2025 · University of Toronto / Vector Institute / Layer 6 AI · **PDF:**
[open](papers/2025/12_Balazadeh_Meresht_et_al._CausalPFN_Amortized_Causal_Effect_Estimation_via_In_Context_Learning.pdf)

**Where it fits.** The fourth member of the causal-PFN cluster in this library, alongside
Do-PFN, FairPFN and CausalFM — and the one the others are measured against. CausalFM's own
ablations report losing to CausalPFN on ACIC2016, which makes holding it necessary to read that
comparison honestly.

**What it contains.** The problem framing is practical rather than theoretical: dozens of
specialised causal estimators exist, and *choosing* one for a given dataset takes substantial
manual effort and domain expertise. CausalPFN amortises that choice. A single transformer is
trained once on a large library of **simulated data-generating processes that satisfy
ignorability**, and then infers causal effects for new observational datasets out of the box —
mapping raw observations directly to effects with no task-specific adjustment, and supplying
**calibrated uncertainty** on Bayesian principles.

Evaluation covers heterogeneous and average treatment effect estimation on **IHDP, Lalonde and
ACIC** — 310 tasks in total — where it achieves the best average rank for **CATE** (PEHE rank
2.30) while being much faster than EconML, deep-learning, BART and GRF baselines. For **ATE** it
is competitive rather than best (average rank 4.45 vs T-Learner 4.31 and IPW 4.41; Table 1). It
is also competitive on real-world uplift-modelling tasks. Credible intervals are calibrated
in-distribution but **severely overconfident on out-of-distribution DGPs**; a temperature
scaling tuned on observational data makes them calibrated or conservative (§5, Fig. 7).

**Strengths.** The combination of best CATE rank, order-of-magnitude speed, recalibratable
uncertainty, and released code makes this the most deployable model in the causal-PFN group.

**Limitations.** The central caveat is in its own construction: the prior assumes
**ignorability**, so unlike Do-PFN it does not target the unconfoundedness-violated regime, and
CausalFM's impossibility result argues that mixing identifiable and non-identifiable settings in
one prior is what degrades posteriors — a theoretical objection CausalPFN's strong empirics do
not settle. Its benchmarks are also the standard semi-synthetic ones, which resemble the
simulated priors it trains on.

---

## 2025-12 — Arazi et al. — TabSTAR

**Venue:** NeurIPS 2025 · Technion — Israel Institute of Technology · **PDF:**
[open](papers/2025/12_Arazi_et_al._TabSTAR_A_Tabular_Foundation_Model_for_Tabular_Data_with_Text_Fields.pdf)

**Where it fits.** The text-field branch of the TFM family, and now part of the TabPFN lineage
in a literal sense: its first author is a co-author on the TabPFN-3 report, and TabPFN-3-Plus
reports state-of-the-art on the TabSTAR benchmark. Purucker's BeyondArena also adopts that
benchmark as one of its dataset sources.

**What it contains.** The critique of prior work is specific: methods that bring language-model
capability to tables mostly use **static, target-agnostic** text representations — a column's
text is embedded the same way regardless of what is being predicted — which limits how useful
the embedding can be. TabSTAR instead:

* **unfreezes a pretrained text encoder**, so textual representations
adapt during tabular pretraining rather than being fixed features; and
* **takes target tokens as input**, giving the model the context it needs
to learn *task-specific* embeddings — the "semantically target-aware representations" of the
name.

The architecture has **no dataset-specific parameters**, which is what makes transfer across
datasets possible at all. It is pretrained on 350 datasets (classification and regression mixed)
and then **fine-tuned with LoRA on each downstream task** — it is not a training-free ICL model.
On a 50-dataset text-feature benchmark (14 classification, 36 regression), it reports
state-of-the-art classification (normalised score 0.83 vs TabM-Tuned 0.73 and CatBoost-Tuned 0.69
up to 10K rows; Fig. 2), and — the forward-looking result — its **pretraining exhibits scaling
laws in the number of datasets**.

**Strengths.** The target-aware embedding idea is a real advance over static text features, and
dataset-count scaling laws are the kind of evidence the field mostly lacks.

**Limitations.** On regression it is competitive but not state of the art, and GBDTs dominate,
especially above 10K rows (Fig. 3); per-task LoRA fine-tuning and an unfrozen text encoder make it
far heavier than table-native ICL models; and its advantage depends on natural-language column
content, so it is not a drop-in TabPFN competitor for numeric-only tables.

---

## 2025-12 — Spinaci et al. — ConTextTab

**Venue:** NeurIPS 2025 (spotlight) · SAP France / SAP SE · **PDF:**
[open](papers/2025/12_Spinaci_et_al._ConTextTab_A_Semantics_Aware_Tabular_In_Context_Learner.pdf)

**Where it fits.** The synthesis of the two halves of the tabular-ICL field, and the empirical
companion to SAP's own position paper on grounding (Klein & Hoffart 2026, also held here). It
sits exactly between the table-native models and the LLM-based ones.

**What it contains.** The framing is a clean statement of a real trade-off. Table-native ICL
architectures (TabPFN, TabICL) are architecturally efficient and well-adapted to table
structure, but training *exclusively on synthetic data* means they cannot exploit the semantics
and world knowledge that real tables carry — a column called `country` is just a categorical to
them. LLM-based tabular learners (TabuLa-8B) have the semantics and world knowledge but can only
ingest a small context because of architectural limits.

ConTextTab keeps the table-native framework and adds semantics two ways: **specialised
embeddings per data modality** (text, dates, numbers rather than one generic encoder) and
**training on large-scale real-world tabular data** instead of synthetic tables — the T4 corpus
(about 3M web tables; 2.18M remain after discarding tables under 150 rows). It **sets a new
standard on the semantically rich CARTE benchmark**, particularly in the low-data regime. On the
non-semantic benchmarks (OpenML-CC18/CTR23, TALENT-Tiny, TabReD) it is roughly on par with other
approaches but falls behind tuned, ensembled boosted trees and RealMLP in ranking, though mostly
not significantly (§4). Code and checkpoints are released.

**Strengths.** This is the strongest evidence that column *semantics* are a real source of
signal that the synthetic-prior line discards by construction — a different argument from
Real-TabPFN's, which is about distributional realism rather than meaning.

**Limitations.** Training on real tables raises contamination questions; the authors'
embedding-similarity check found no CARTE contamination in T4, but OpenML overlap is only
referred to the T4 authors' study. The gains concentrate where columns carry natural-language
meaning, which is exactly where a purely numeric domain gains least.

---

<a id="equitabpfn"></a>


## 2025-12 — Arbel et al. — EquiTabPFN

**DOI:** [10.52202/085713-2097](https://doi.org/10.52202/085713-2097) · NeurIPS 2025 (Advances
in Neural Information Processing Systems 38) · INRIA + University of Freiburg / ELLIS Institute
Tübingen + **Prior Labs** · **PDF:**
[open](papers/2025/12_Arbel_et_al._EquiTabPFN_A_Target_Permutation_Equivariant_Prior_Fitted_Network.pdf)

**Where it fits.** A critique from *inside* the lab that builds TabPFN — Frank Hutter is an
author — which makes it unusually credible. It identifies a symmetry of tabular data that the
architecture violates, where the field had previously identified only the two it respects (row
order and, since TabICL, column order).

**What it contains.** The observation is simple once stated: a classifier's target dimensions
have no canonical ordering, so permuting them should not change predictions — and in TabPFN it
does. The paper formalises this as the **target-equivariance gap**,

> `E_equi(f) := L(f) − L(f_equi)`

the loss difference between a function and its permutation-averaged counterpart. The gap is
*irreducible* for a non-equivariant architecture, and the paper shows empirically that it
shrinks only slowly over TabPFN training — the model is spending capacity learning a symmetry it
could have been given for free. This is also the real reason for the ensembling over class
permutations that TabPFN needs in practice.

The fix is architectural: equivariant encoders and decoders plus a bi-attention mechanism
extended over the **target** axis, so equivariance holds by construction. Evaluation is on
TabZilla, split deliberately into 76 tasks with ≤10 classes and 10 tasks with >10 classes — more
classes than were ever seen in pretraining. On the latter, EquiTabPFN attains the best median
relative accuracy of all models, while **TabPFN v2 falls below a linear model and random
forests**. No ensembling is used.

The baseline design deserves note. Because v2's prior and training code are not public, the
authors also train **TabPFNv2\*** — v2's exact architecture on the *public* prior they used
themselves — so the comparison isolates the architecture rather than confounding it with a
better closed prior.

**Strengths.** Names and formalises a real defect rather than reporting another benchmark win,
and the mechanism explains an existing workaround (permutation ensembling) rather than just
adding one. The TabPFNv2\* control is exactly the comparison this library has repeatedly noted
is missing when a closed prior is involved. The class-count limit is removed **by construction**
instead of by post-processing, which is what makes it cheaper rather than more expensive. Code
is released.

**Limitations.** Self-attention over targets costs quadratically in the number of target
dimensions — fine for most tabular problems, not for very many classes. More interesting: **some
targets genuinely are not permutation-equivariant.** Ordinal outcomes have a real order, and the
authors find 5 of the 86 surveyed datasets are of this kind; handling them would require
changing the prior, since it is currently equivariant by construction. Classification only.

---

<a id="from-tables-to-time"></a>

## 2026-01 — Hoo et al. — From Tables to Time

**arXiv:** [2501.02945](https://arxiv.org/abs/2501.02945) · **PDF:**
[open](papers/2026/01_Hoo_et_al._From_Tables_to_Time_Extending_TabPFN_v2_to_Time_Series_Forecasting.pdf)

**Where it fits.** A more thorough version of the 2024 forecasting paper by the same authors.
Reframes time-series forecasting as a *tabular regression problem* and shows that the
**unmodified** pretrained TabPFN-v2 — paired with a lightweight temporal featurisation — beats
specialised time-series foundation models. Released as **TabPFN-TS** at
github.com/PriorLabs/tabpfn-time-series.

**What it contains.** The construction is simple but the result is striking. Each time step
becomes one row in a tabular regression problem: features encode time progression (running
index), multi-scale seasonality (year, day-of-week, hour-of-day, …), plus optional covariates
(weather, economic indicators, control inputs). The target is the observed value at that time
step. Forecasting then reduces to predicting future rows whose temporal features are known in
advance — and TabPFN-v2 predicts the entire forecast horizon **in one forward pass**.

Headline results:

* On the 28 **fev-bench** tasks with known dynamic covariates,
TabPFN-TS (11 M parameters) has the **strongest overall performance** (§4.2).
* On **GIFT-Eval** (univariate, 97 tasks), it ranks closely behind
TiRex, Toto-1.0 and Moirai-2 and matches TimesFM-2.0 and Chronos-Bolt, which the authors
describe as over two orders of magnitude larger (§4.1, Fig. 4.1).
* No time-series–specific pretraining. No fine-tuning. The
pretrained TabPFN-v2 weights are used as-is.

The paper also includes analyses (§5): how the model exploits temporal structure (all
features are timestamp-derived — running index, calendar sin/cos encodings, FFT-selected
seasonal components; lagged/rolling features are deliberately excluded as incompatible with
non-autoregressive multi-step prediction), how it uses covariates, a backbone ablation that
swaps in TabDPT (TabDPT-TS is usable but well below TabPFN-TS, roughly Chronos-Bolt-Tiny level;
§5.4), and a featurisation ablation (index + calendar + automatic seasonal features together
work best; §5.5).

**Strengths.** Cleanest evidence that the synthetic prior transfers across modalities — best
overall on the fev-bench covariate subset and on par with much larger TSFMs on GIFT-Eval, with
quantile forecasts for free.

**Limitations.** Structurally cannot extrapolate trends (predictions stay in the convex hull of
observed targets), is ~30× slower than Chronos-Bolt, and the covariate comparison is somewhat
favorable-by-construction.

---

## 2026-01 — Klein and Hoffart — Position: Foundation Models for Tabular Data within Systemic Contexts Need Grounding

**arXiv:** [2505.19825](https://arxiv.org/abs/2505.19825) · **PDF:**
[open](papers/2026/01_Klein_and_Hoffart_Position_Foundation_Models_for_Tabular_Data_within_Systemic_Contexts_Need_Grounding.pdf)

**Where it fits.** A *contrarian* position paper from SAP that challenges the entire "isolated
tables" framing of current tabular foundation models — TabPFN, TabICL, TabDPT, Mitra all
included. Argues these models trained on individual tables (or even on schema-level multi-table
relations via GNNs) fundamentally miss the **operational context** — the procedural logic,
declarative rules, and domain knowledge — that gives tabular data its meaning in real-world
enterprise systems.

**What it contains.**

* **The diagnosis.** Current tabular FMs assume "information
completeness within tables" — that the information needed to predict an outcome is in the rows
themselves. In an enterprise setting that's almost never true. A row like `(amount=4999, ...,
approved=True)` next to `(amount=5000, ..., approved=False)` is fully explained by a rule
somewhere in the codebase: ``if amount >= 5000: require_manager_approval()``. A purely
statistical model trained on historical decisions might learn an *approximate* threshold near $4
800 and misclassify edge cases — while the actual rule is a hard `>=` boundary, sitting in
source code that the model never sees.
* **The proposal: SLT + FMSLT.** *Semantically Linked Tables* —
the relational data plus three layers of explicitly-modelled context: declarative business
knowledge (data models, business objects, business rules, process models), procedural knowledge
(agent logic in natural language, application logic as code), and world knowledge (general
business concepts, types, relationships, implicit assumptions). A *Foundation Model for SLT*
(FMSLT) is then a new model class that ingests **code as logic**, not as text — distinguishing
"branching paths define decision boundaries" from mere token co-occurrence.
* **Two-phase training recipe.** (i) Pre-train on open-source
code-data pairs and synthetic systems to learn business-logic mechanics. (ii) Apply zero-shot to
proprietary enterprise data via in-context retrieval of the relevant code/rules.
* **Call to action (§6), four items.** (1) The **Operational Turing
Test** (Def. 6.1): a model passes if it can join an unseen simulated organization and, from its
declarative knowledge (rules), procedural knowledge (code) and relational data plus a few labelled
examples, correctly predict a transaction's outcome **and explain the decision by citing the
relevant operational artifacts** (e.g. the policy section and the code line enforcing a
threshold). (2) Privacy-preserving data sandboxes for sharing code and logic without raw rows.
(3) Privacy-preserving multi-table synthetic data generation. (4) New architectures that natively
process relational structure, code and rules while keeping ICL. To motivate grounding, the paper
cites enterprise-agent benchmarks (WorkArena++, TheAgentCompany, CRMArena-Pro, AgentArch, MLGym,
…) where agents complete only ~30–35% of tasks needing implicit business knowledge.

**Strengths.** Sharp, well-referenced framing of a real gap, generalizing the PFN
synthetic-prior philosophy to operational logic with an honest alternative-views section.

**Limitations.** Zero empirical evidence — no architecture, loss, benchmark, or numbers — and
the multi-table+code synthetic generation and provenance mapping it requires are acknowledged
open problems.

---

<a id="tabdpt"></a>


## 2026-01 — Ma et al. — TabDPT

**arXiv:** [2410.18164](https://arxiv.org/abs/2410.18164) · **PDF:**
[open](papers/2026/01_Ma_et_al._TabDPT_Scaling_Tabular_Foundation_Models_on_Real_Data.pdf)

**Where it fits.** From Layer 6 AI (Toronto). Pretrained at the **opposite extreme of the
synthetic-vs-real spectrum** from TabPFN: a transformer pretrained on *real* OpenML data only,
with no synthetic prior. Open weights on [HuggingFace](https://huggingface.co/Layer6/TabDPT) and
inference + training code on [GitHub](https://github.com/layer6ai-labs/TabDPT-inference).

**What it contains.** Two methodological pillars:

* **ICL retrieval + self-supervised learning.** At each training
step the model samples a real OpenML table, randomly designates one column (with enough unique
values) as the target — standardised for a regression task or binned for a classification task
— and predicts it from the remaining columns, which are themselves shuffled and randomly dropped
(§3.2). Inspired by masked modelling, but not BERT-style token masking: the point is that the
number of auxiliary tasks grows combinatorially with the feature count. The context for each
training query is retrieved from its nearest rows in the same table, matching the kNN-retrieval
protocol used at inference (§3.3). Trained model handles both classification and regression.
* **Scaling laws on real data.** The paper's empirical contribution
is showing that **scaling both model size and pre-training data size yields consistent gains
following power-laws** (Figure 1 of the paper). This is the first demonstration of LLM-style
scaling behaviour for tabular foundation models — and crucially, it works on *real* data, not
just synthetic.

Evaluated on **OpenML-CC18** (classification) and **OpenML-CTR23** (regression). TabDPT
consistently matches or surpasses specialised per-dataset baselines that get
hyperparameter-tuned, at a fraction of the deployment cost. Particularly strong in the few-shot
regime: with minimal semi-supervised modifications, TabDPT outperforms specialised baselines on
**10-shot classification**.

**Contamination note.** The local code dump is ``repositories/TabDPT.txt``, and TabDPT publishes
the exact list of OpenML datasets it trained on
(`tabdpt_datasets/data_splits/{cls,reg}_datasets.csv`). Any evaluation that uses TabDPT as a
baseline must cross-check its held-out sets against that list, or the comparison is contaminated
in TabDPT's favour.

**Strengths.** Fully open (weights, code, data list) with an explicit contamination audit, an
honest "Bitter Lessons" failure appendix, and the first clean Chinchilla-style TFM scaling
analysis (α=0.42, β=0.39).

**Limitations.** Capped at 100 features/10 classes (requiring lossy PCA and base-C tricks),
margins over TabPFN v2 are small and mostly CI-overlapping, no calibration metrics are reported,
and per-query retrieval complicates deployment.

---

<a id="tabpfn-25"></a>


## 2026-02 — Grinsztajn et al. — TabPFN-2.5

**arXiv:** [2511.08667](https://arxiv.org/abs/2511.08667) · **PDF:**
[open](papers/2026/02_Grinsztajn_et_al._TabPFN_2.5_Advancing_the_State_of_the_Art_in_Tabular_Foundation_Models.pdf)

**Where it fits.** Successor to v2: deeper (18 layers for regression, 24 for classification),
bigger context limit (50 000 samples × 2000 features), trained purely on synthetic data, with a
separately released real-data-finetuned variant (Real-TabPFN-2.5).

**What it contains.**

* **Architecture.** TabPFNv2-style alternating attention, depth
raised from 12 to 18 layers (regression) and 24 layers (classification); feature-group size 3
(v2: 2); a 2-layer MLP encoder for regression; 64 learned "thinking" rows (§3).
* **Training data.** Synthetic-only base + a Real-TabPFN-style
real-data fine-tuned variant on 43 curated OpenML/Kaggle datasets deduplicated against internal
benchmarks and TabArena (Appendix C).
* **Headline results.** On TabArena-Lite, default TabPFN-2.5
outperforms tuned tree models and matches AutoGluon 1.4 (extreme, tuned 4 h); default
TabPFN-2.5 has a **100% win rate against default XGBoost** on small-to-medium classification
datasets (≤10 000 rows, 500 features) and 87% on larger ones up to 100K rows (abstract, §4).
* **Evaluation.** Also an internal benchmark (§4.2), a distillation
engine to MLP/tree ensembles (§4.4), and RealCause causal-effect estimation (§4.5).
* **Checkpoints (from the HuggingFace catalogue, not the paper).**
``repositories/Huggingface TabPFN.txt`` lists ``_default`` as real-finetuned and ``_default-2``
as synthetic-only, plus specialist variants (``_large-features-L``, ``_large-features-XL``,
``_large-samples``, ``_low-skew``, ``_quantiles``, ``_real``, …).

Note that v2.6 (the immediate successor described on the HuggingFace card and the TabPFN docs)
was released after v2.5 *without* a corresponding paper. v2.6 reverts the
"default-is-real-finetuned" naming convention: its single ``_default`` checkpoint is again
*synthetic-only*. The primary sources for checkpoint provenance are `repositories/Huggingface
TabPFN.txt` and `repositories/TabPFN .txt`.

**Strengths.** Verified leap over v2 (Wilcoxon p<0.0001, "never much worse") on public TabArena,
with Real-TabPFN-2.5 defaults beating every tuned+ensembled competitor on classification.

**Limitations.** Corporate, non-peer-reviewed report whose two key ingredients (new synthetic
prior, distillation engine) are undisclosed, with non-commercial-licensed weights and no
calibration (ECE/Brier) metrics despite calibration claims.

---

## 2026-02 — Ma et al. — Foundation Models for Causal Inference via Prior-Data Fitted Networks

**arXiv:** [2506.10914](https://arxiv.org/abs/2506.10914) · **PDF:**
[open](papers/2026/02_Ma_et_al._Foundation_Models_for_Causal_Inference_via_Prior_Data_Fitted_Networks.pdf)

**Where it fits.** Unified causal-PFN framework, published at ICLR 2026. Introduces
**CausalFM**: a general recipe for training PFN-based foundation models for Bayesian causal
inference, instantiated per identification setting (back-door, front-door, IV) — extending the
causal-PFN line (CausalPFN, Do-PFN), which covers back-door adjustment only, to front-door and IV.

**What it contains.** Three layers of contribution.

1. **Theory: necessary criteria for valid SCM-priors for causal
inference.** The paper formalises how to construct prior distributions over structural causal
models such that the resulting PFN's in-context predictions are valid estimates of the causal
quantity of interest. Identifies what breaks if you naïvely take TabPFN's SCM-prior and ask it
to estimate a treatment effect.
2. **Method: CausalFM priors.** A novel family of SCM-priors
parameterised by Bayesian neural networks, structured to respect the underlying causal-inference
setting. Concretely: different priors for **back-door adjustment** (the
conditioning-on-confounders case), **front-door adjustment** (the mediator case), and
**instrumental-variable adjustment** (the natural-experiment case).
3. **Empirics: trained PFN models for CATE estimation.**
Conditional Average Treatment Effect estimation across diverse benchmarks. CausalFM is
**competitive** with CATE estimators specifically trained for the task (abstract), while
requiring no per-dataset training itself.

Key advantages over classical causal inference: (i) no retraining per new dataset (in-context
inference), (ii) principled uncertainty quantification, (iii) identifiability guarantees baked
into the prior design. Identification is **not** learned: the setting (back-door, IV, front-door)
must be chosen before estimation, and each setting has its own trained model (Appendix A.1).

**Strengths.** Clean identifiability-vs-estimation separation backed by an impossibility
theorem, first PFN handling front-door and IV, fully disclosed prior hyperparameters, and ~0.5 s
inference.

**Limitations.** Evaluated only on synthetic/semi-synthetic data resembling its own prior
(losing clearly to CausalPFN on ACIC2016), requires one model per setting, and claims Bayesian
uncertainty without ever evaluating calibration or coverage.

---

<a id="tabpfn-wide"></a>


## 2026-03 — Kolberg et al. — TabPFN-Wide

**arXiv:** [2510.06162](https://arxiv.org/abs/2510.06162) · **PDF:**
[open](papers/2026/03_Kolberg_et_al._TabPFN_Wide_Continued_Pre_Training_for_Extreme_Feature_Counts.pdf)

**Where it fits.** Continued-pretraining sibling to Real-TabPFN, focused on the
extreme-feature-count regime.

**What it contains.** Continues pretraining the TabPFNv2 classifier for 10 000 steps on
synthetic high-dimensional, low-sample-size (HDLSS) datasets with thousands of features (the
multi-omics regime). Training is **synthetic-only**: a set of real omics and synthetic SNP
datasets is used only to monitor convergence, not for fine-tuning or checkpoint selection.
Specifically:

* **Synthetic prior augmentation (the actual method)** — because the
TabPFNv2 prior is not public, the authors take the open-source **TabICL prior** and widen its
datasets to a target dimension via sparse random linear projections of the existing features
(plus sparse dependencies on categorical features and noise), optionally appending the original
features. The whole point is to handle wide data **without** reducing it.
* **FeatureAgglomeration is a baseline, not the method** — the
paper evaluates agglomerative feature reduction only as a comparison point that its widened
model beats (Fig. 3 / Appendix B). Its method is prior-widening, **not** feature reduction — a
distinction routinely misread.
* **Released checkpoints** — TabPFN-Wide models continued-pretrained
per maximum synthetic width (evaluated up to 60,000 features), **classifier-only** (the
regressor is explicitly left as future work — so there is no wide *regressor*). Not to be
confused with Prior Labs' own v2.5 ``_large-features-L`` (≤ 500) / ``_large-features-XL`` (≤
1000) specialist checkpoints from the TabPFN-2.5 release.

**Strengths.** Large AUROC gains on multi-omics (e.g., BRCA 0.733→0.971) and a 92% HDLSS win
rate with no catastrophic forgetting (Spearman ρ=0.9935 on original-range tasks).

**Limitations.** Classifier-only (regressor explicitly left open), the recipe failed to train
TabICL, attention-as-importance is validated only on synthetic needle-in-a-haystack tasks (its
use on real biomedical data is flagged as needing caution), and no calibration analysis is
reported.

---

## 2026-04 — Tanna et al. — Exploring Fine-Tuning for Tabular Foundation Models

**Venue:** ACM Web Conference 2026 (WWW '26) · **DOI:**
[10.1145/3774904.3792923](https://doi.org/10.1145/3774904.3792923) · **PDF:**
[open](papers/2026/04_Tanna_et_al._Exploring_Fine_Tuning_for_Tabular_Foundation_Models.pdf)

**Where it fits.** A companion empirical study from the same lab as the TabTune library — the
broad "when does fine-tuning actually help a tabular FM?" benchmark that Rubachev et al. 2025
(*On Finetuning Tabular Foundation Models*) began, now widened to six TFMs and three large suites.

**What it contains.** Compares four adaptation strategies — zero-shot, meta-learning (episodic,
48–512 support samples, 5 epochs), supervised fine-tuning (full-parameter AdamW, LR 1e-5–5e-5,
early stopping ≤ 10 epochs), and PEFT (LoRA r=8, α=16) — over TabPFN, TabICL, OrionMSP,
OrionBiX, TabDPT and Mitra on TALENT (155), OpenML-CC18 (63) and TabZilla (27), plus a 9-dataset
fairness suite. Metrics span accuracy / weighted-F1 / mean-rank, **calibration** (ECE, MCE, Brier),
and **fairness** (SPD, EOD, EOpD). Headline findings:

* **Zero-shot TFMs are already strong** — often competitive with tuned
gradient boosting, so fine-tuning has a high bar to clear.
* **Gains are highly model- and data-dependent.** Meta-learning and
PEFT give moderate, conditional gains; **full SFT frequently degrades accuracy and/or
calibration** — catastrophically for some models (TabICL / OrionBiX collapse under SFT on the
smaller suites) — while **TabPFN is comparatively robust** to fine-tuning.
* **Dataset regime matters** (Table 2): on small datasets (<1K rows)
zero-shot is clearly better because most models overfit when fine-tuned; medium datasets
(1K–10K) see small consistent gains; large ones gain little. On imbalanced datasets
meta-learning gives the most reliable improvements while SFT still degrades several models, and
wide datasets (>100 features) show some of the few clear fine-tuning boosts (e.g. TabPFN SFT).
* Calibration can worsen even when accuracy holds, so accuracy alone is
a misleading model-selection signal.

**Strengths.** Rare joint accuracy+calibration+fairness lens showing TabPFN is uniquely tolerant
of full fine-tuning while preserving calibration (ECE 0.0287 vs 0.0276 zero-shot), with concrete
regime-dependent guidelines.

**Limitations.** A 4-page paper with barely tuned recipes (single LoRA config, ≤10 epochs), an
apparent Mitra integration bug and duplicated PEFT tables undermining harness trust, an author
conflict when their own Orion-MSP tops the leaderboard, and no comparison to corpus-level
continued pretraining.

---

## 2026-04 — Bouadi et al. — Orion-BiX

**Venue:** ACM Web Conference 2026 (WWW '26), April 13–17 2026, Dubai · [DOI
10.1145/3774904.3792937](https://doi.org/10.1145/3774904.3792937) · Lexsi Labs (Paris / Mumbai /
London) · **PDF:**
[open](papers/2026/04_Bouadi_et_al._Orion_Bix_Bi_Axial_Attention_for_Tabular_In_Context_Learning.pdf)

**Where it fits.** The second Orion architecture, and the sibling of Orion-MSP. Both are the
models behind Lexsi Labs' TabTune library and fine-tuning benchmark, which this library holds.

**What it contains.** A four-page conference paper built on the TabICL codebase. It keeps
TabICL's SetTransformer column encoder and its label-aware in-context learner (including
hierarchical classification trees for more than C_max classes) **unchanged**, and makes two
changes (§2):

* a **biaxial row encoder** replacing TabICL's single-stage row encoder:
it **alternates standard, grouped, hierarchical and relational attention**, fusing outputs by
**multi-CLS summarisation** to capture local and global feature interactions;
* **episodic meta-training**: explicit support/query episodes built
from synthetic tables, optionally with kNN-based support selection, to align pretraining with
few-shot inference.

**Results (§3).** On domain suites drawn from TALENT and OpenML-CC18, Orion-BiX has the best mean
rank in Medical (4.10 vs TabICL 5.54) and Finance (5.39 vs 6.60), though TabPFN has higher
Medical accuracy. In few-shot curves (k = 5–128) it leads all baselines by 2–4 points for
k ≤ 32; on OpenML-CC18 TabPFN overtakes it at k = 128. Uniform support sampling beats kNN-based
selection by 3–5 points, and Orion-BiX beats TabICL under both.

**Strengths.** A cleanly scoped TabICL modification whose few-shot gains are tied to a specific
change (episodic meta-training), released as a scikit-learn-compatible model.

**Limitations.** At four pages there are no ablations separating the four attention types or the
row encoder from meta-training, no calibration analysis, and the claim is "competitive with"
rather than beating the frontier. As with Orion-MSP, the evaluation is by the same lab that
produces the benchmark library, so treat the leaderboard position as self-reported.

---

## 2026-05 — Tanna et al. — Data Presentation Over Architecture

**arXiv:** [2605.18635](https://arxiv.org/abs/2605.18635) · Lexsi Labs · **PDF:**
[open](papers/2026/05_Tanna_et_al._Data_Presentation_Over_Architecture_Resampling_Strategies_for_Credit_Risk_Prediction_with_Tabular_Foundation_Models.pdf)

**Where it fits.** The most directly applied paper in this library: TFMs evaluated on real
credit-default prediction, by the Lexsi Labs group behind TabTune and the Orion models. It is
the natural counterpart to Purucker's BeyondArena — where that paper shows *split protocol*
changes TFM rankings, this one shows *context construction* does.

**What it contains.** The premise is that because TFMs predict by in-context learning, their
output is sensitive to **how the context window is built** — which, under severe class
imbalance, is a design decision nobody had systematically varied. The study benchmarks **four
classical models and five TFMs** (TabPFN, TabICL, Orion-MSP, Orion-BiX among them) on **Home
Credit** and **Lending Club**, crossing **seven context-construction strategies** with **context
sizes from 1K to 50K**.

The headline finding is a genuine reordering of priorities:

* **The choice of context strategy explains more variance in AUC-ROC than
the choice of TFM family** (§5.2, Table 2). The best class-aware strategy beats uniform sampling
by ~3 AUC points on Home Credit (Balanced 0.734 vs 0.703) but only ~1 point on Lending Club
(Hybrid 0.686 vs 0.673); in both cases the best–worst strategy gap exceeds the inter-TFM gap.
* **The 5K–10K crossover holds on Home Credit only** (§5.3): there TabPFN
and TabICL pass the best classical baseline (Random Forest, 0.739) with 5K–10K context rows
versus 246K training rows. On Lending Club most TFMs do not reach XGBoost (0.718) even at 50K
context (best: TabPFN 0.703).
* **Default-class recall.** Balanced contexts recover meaningful
default-class recall, while three of the four classical baselines predict no defaults at all on
Home Credit at the 0.5 threshold. Those baselines run with default hyperparameters and **no
class weighting or threshold tuning** (§4, §5.1); the authors note `scale_pos_weight` would
restore recall for GBDTs.
* Conclusion: **context construction, not architecture choice, is the
primary deployment lever** for TFMs in imbalanced credit settings.

**Strengths.** An actionable, controlled result for imbalanced deployment: context construction
is a cheap lever with an effect at least as large as model choice.

**Limitations.** The recall comparison is against deliberately untuned, unweighted baselines, so
it shows an operating-point fix rather than a failure of GBDTs; the AUC parity claim does not
replicate on the second dataset; and only two datasets are used. Author-affiliation caveat as
with the rest of the Orion line: the TFMs being compared include the authors' own.

---

<a id="oprior"></a>


## 2026-05 — Bouadi et al. — O'Prior (Shaping the Prior)

**arXiv:** [2605.18971](https://arxiv.org/abs/2605.18971) (v1, 18 May 2026) · Lexsi Labs · Code:
[o-prior/O-prior](https://github.com/o-prior/O-prior) · **PDF:**
[open](papers/2026/05_Bouadi_et_al._Shaping_the_Prior_How_Synthetic_Task_Distributions_Determine_Tabular_Foundation_Model_Quality.pdf)

**Where it fits.** The paper the field needed: the **first study to isolate prior design as the
scientific variable**. Its framing is a direct criticism of how the line has progressed — "prior
work conflates architectural improvements with prior improvements, TabPFN v2, for instance,
enriched both simultaneously, making attribution impossible." Where [Mitra](#mitra) proposed
criteria for *selecting* priors, O'Prior builds a prior and then measures which of its parts
actually pay.

**What it contains.** O'Prior is a "compositional realism prior" with four coupled components:

1. a **hierarchical SCM meta-generator** spanning diverse functional
families — the "Hybrid SCM" composes five mechanism families (MLPs, decision trees, 1-D
convolutions, RBF Gaussian processes, time-lagged VARs) within one random DAG;
2. a **modular realism engine** — marginal morphing, feature augmentation,
**MCAR / MAR / MNAR missingness**, and target reshaping;
3. an explicit **stress module** injecting confounding and support–query
mismatch (i.e. shortcut and shift pressure); and
4. a **curriculum-governed, leakage-safe generation protocol**.

**The methodology is the most valuable part, and it is cheap.** The controlled principle is
stated plainly: hold architecture, optimizer, training budget and evaluation pipeline fixed;
vary only the synthetic task distribution, so any downstream difference is attributable to the
prior alone. Concretely they use **nanoTabPFN** as the base — chosen deliberately, because "at
reduced scale, pretraining requires only tens of thousands of synthetic datasets rather than
millions, making controlled prior ablations computationally feasible without sacrificing the
qualitative conclusions" — under the **TFM-Playground** training protocol, with an identical
budget per condition: **40,000 synthetic datasets per prior**, tables of 512–1,024 rows and 3–50
features, batch size 4 tables per step, 1,000 steps per epoch, 10 epochs, and no hyperparameter
tuning between conditions. Nine O'Prior variants are compared in four sequential groups against
three baseline generators run under the same budget and model: the **TabPFN v1**, **TabICL-v1**
and **TabICL-v2** priors.

**Results.** The baseline progression alone shows prior choice dominates: the TabPFN v1 prior
reaches ROC-AUC **0.576** on TabArena and **0.519** on OpenML-CC18 (macro F1 below 0.37 on
both); TabICL-v1's tree-based structural equations improve on it, but "the improvement is
consistent but small"; TabICL-v2 improves further (0.791 / 0.724). O'Prior variants improve
further still: the basic SCM prior (G1a) already matches TabICL-v2, and the Hybrid SCM alone
(G1b) gives the largest single-component gain (TabArena ROC-AUC 0.834). The full curriculum
configuration (G4) beats TabICL-v2 by 2.8 ROC-AUC points on TabArena and 10.1 on OpenML-CC18,
but **does not beat the best single-component variants** (G1b, G1c, G2b outperform it on several
metric–benchmark pairs), which the authors attribute to the curriculum spending a fixed budget on
easy tasks (§4). The headline ablation finding is that
**structural mechanism diversity is the strongest driver of transfer**, while observational
realism and shift-aware stress contribute *complementary* — explicitly not interchangeable —
gains. Two supporting analyses go beyond benchmark scores: a structural-alignment analysis
showing stronger dependency realism against real tabular data, and probing experiments showing
that O'Prior-pretrained models learn deeper, more discriminative internal representations on
structurally hard tasks.

**Strengths.** The controlled protocol is the contribution and it is reusable by anyone;
releasing the code makes prior-design research tractable for groups without frontier compute.

**Limitations.** Three real limits. First, **everything is at nano scale** — the absolute
numbers are low (a 0.576 ROC-AUC baseline is a budget-starved regime), and the authors argue
only that the *qualitative* orderings survive; whether the component ranking holds at TabICL or
TabPFN-2.5 scale is untested. Second, the evaluation is **classification only** (ROC-AUC,
accuracy, macro F1 on TabArena and OpenML-CC18) — so the target-reshaping component of the
realism engine is never exercised on a regression target, and bounded or multi-modal targets are
outside the study entirely. Third, this is the sixth Lexsi Labs paper in this collection, the
baselines are other labs' generators, and the winner is the authors' own; the same
self-evaluation caveat that applies to the Orion line applies here, and independent replication
matters more than usual.

---

<a id="tabdpt-turbo"></a>


## 2026-05 — Hosseinzadeh et al. — TabDPT-Turbo

**Venue:** 2nd ICML Workshop on Foundation Models for Structured Data (FMSD), Seoul, 2026 ·
[OpenReview `Y00pwFyrHR`](https://openreview.net/forum?id=Y00pwFyrHR) · Layer 6 AI, Toronto
(Valentin Thomas now at Cohere; work done at Layer 6) · **PDF:**
[open](papers/2026/05_Hosseinzadeh_et_al._TabDPT_Turbo_Efficient_In_Context_Learning_for_Tabular_Prediction.pdf)

**Where it fits.** The retrieval branch **recanting**, which makes this more interesting than a
routine efficiency paper. The same lab introduced retrieval-based context construction
([LoCalPFN](#localpfn), 2024) and shipped FAISS retrieval in [TabDPT](#tabdpt) v1; here it
argues retrieval sacrifices too much efficiency and removes it, replacing it with **long-context
pretraining**. It is also a deliberate refusal of the architectural convergence: where TabPFN-3,
TabICLv2 and Google's TabFM all moved to column-embed → row-compress → ICL, TabDPT-Turbo stays
**row-based**, arguing that efficiency and low-resource deployment are easier to attain that way
as context length grows.

**What it contains.** Four changes on top of TabDPT, which it extends because TabDPT is the
highest-performing *row-based* architecture on TabArena and fully open-source:

* **Retrieval-free long context.** Rather than retrieving a local
neighbourhood per query, the model is pretrained on long contexts so it can consume the context
directly. The efficiency argument is stark: the paper reports retrieval-style inference as
**100×–1000× slower** than full-context inference.
* **A corpus an order of magnitude larger.** Same TabDPT SSL objective
(a random column as pseudo-target), but the OpenML corpus is scaled to **1,445 filtered and
deduplicated datasets**, with an added duplicate-detection step beyond TabDPT's own
deduplication code.
* **Architecture and loss changes:** attention temperature scaling,
per-layer target routing through the transformer value projections, **learned "thinking rows"**
(the register-token idea TabPFN-2.5 also uses), **regression-as-classification trained with
CRPS** (Continuous Ranked Probability Score) rather than a bar-distribution or pinball head,
plus an auxiliary loss.
* **Results.** Comparable *default* performance to TabDPT v1.1 on
TabArena-Lite, OpenML-CC18 and CTR23, at orders of magnitude lower inference cost than
retrieval-based TabDPT. In a same-hardware rerun of TabArena-Lite (1×H100 + 96 vCPUs, ensemble
size 8; Table 1) it is the fastest leading TFM: fit + predict ≈0.63 s per 1K rows versus ≈1.51 s
for TabPFN-3 (≈2.4×) and ≈8.2 s for TabICLv2 (≈13×), though TabICLv2 fits slightly faster
(0.41 s vs 0.44 s) and loses on prediction time. (The 2.86×–12.90× ratios in Appendix Table 2 are
corpus-size ratios versus TabDPT v1.1, not speedups.)

Released as **TabDPT v1.2** in `layer6ai-labs/TabDPT-inference` — the same repository this
library already snapshots as `TabDPT.txt`, so the Turbo code arrives there on the next refresh.

**Strengths.** The headline is an *efficiency* result, not a quality one: "comparable
performance, much faster" is the honest reading, and the paper says so.

**Limitations.** At nine workshop pages there are no calibration metrics, and evaluation uses
**TabArena-Lite** — a reduced protocol — rather than full TabArena, so it is not directly
comparable to the leaderboard numbers other entries here quote. Its "112 datasets" baseline
corpus refers to TabDPT **v1.1** (Appendix Table 2), which differs from the 123 datasets in the
original TabDPT paper — a version difference, not an inconsistency. Finally, the CRPS regression head is introduced without an ablation
isolating it from the corpus scaling, so the four changes cannot be individually attributed.

---

<a id="tabpfn-3"></a>


## 2026-05 — Grinsztajn et al. — TabPFN-3 (Technical Report)

**arXiv:** [2605.13986](https://arxiv.org/abs/2605.13986) · **PDF:**
[open](papers/2026/05_Grinsztajn_et_al._TabPFN_3_Technical_Report.pdf) · **Filed version:** v2, 28 May 2026

The revision explicitly attributes the retrieval decoder to earlier target-equivariant
and localization work (Section 2.2). The attention decoder is a continuation of that
line, rather than an isolated invention. Provider-reported benchmark gains remain
subject to the report's comparator, hardware and licensing conditions.


**Where it fits.** Prior Labs' next-generation tabular foundation model after TabPFN-2.5 / 2.6.
A clean architectural reset rather than a continued-pretraining variant: a three-stage
transformer that scales in-context learning to **one million training rows on a single H100**,
adds native many-class classification, and introduces test-time-compute ("Thinking mode") for
accuracy at the cost of latency. Released under the TABPFN-3.0 license (permissive for research
and internal evaluation); enterprise / API tier ships TabPFN-3-Plus.

**What it contains — architecture.** TabPFN-3 abandons the TabPFN-2.x alternating row/feature
attention in favour of a three-stage design borrowed from Qu et al.'s TabICL line:

1. **Feature distribution embedding (column-wise).** Each
column independently embedded by a transformer with inducing-point attention — sidesteps the
O(n²) cost of full cross-row attention.
2. **Feature aggregation (row-wise).** Learned `cls` tokens
attend to all features within each row; concatenated `cls`-hidden states form a single
fixed-dimensional row embedding decoupled from the input feature count.
3. **In-context learning.** A TabPFN-v1-style ICL transformer
on the row embeddings — sequence length proportional to rows only, so scaling to 1M rows is
feasible.

On top of this they layer (i) an **attention-based many-class decoder** that frames class
prediction as soft nearest-neighbour retrieval over the in-context training rows (non-parametric
in class count); (ii) **row-chunking inference** that precomputes the inducing-vector summary
once and then streams rows through the column-aggregator in fixed-size chunks, decoupling peak
activation memory from dataset size; (iii) **multi-query attention** in the ICL stage — test
rows share a single KV head, shrinking the per-estimator KV cache to ~7 GB at 1M rows.
Pretrained purely on synthetic data from an improved SCM prior; no real-data continued
pretraining in the base release.

*From the code dump (`repositories/TabPFN .txt`), not the paper:* one integration consequence
worth flagging for anyone writing checkpoints is that the **regressor criterion handling differs
between v2.6 and v3**. TabPFN regressors predict a *bar distribution*
over a fixed grid of borders, and the two generations save that grid in different places: up to
v2.6 as ``criterion.*`` state stored beside the model, from v3 as a ``regression_borders`` buffer
on the model itself. The loader keeps ``criterion.*`` out of the model state either way, then
``_resolve_regression_borders`` prefers the checkpoint's saved borders and falls back to the
buffer. Writing ``criterion.*`` unconditionally therefore round-trips for both bases. The checkpoint format
itself is the standard four-key ``torch.save`` dict (``state_dict``, ``config``,
``architecture_name``, ``inference_config``); valid ``architecture_name`` strings are
``tabpfn_v2``, ``tabpfn_v2_5``, ``tabpfn_v2_6``, ``tabpfn_v3``.

**What it contains — results.** On full TabArena, a single forward pass of open TabPFN-3 beats
every other model including tuned-and-ensembled baselines (+72 Elo over tuned+ensembled
Real-TabPFN-2.5) and pareto-dominates the time/accuracy frontier. TabPFN-3-Plus (Thinking) beats
every non-TabPFN model by **over 200 Elo** and AutoGluon 1.5 extreme (4 h) by over 100 Elo in
<1/10 the runtime, with no LLMs, no real data, no internet search. On the 15 largest TabArena
datasets (10k–100k rows), TabPFN-3 leads by 100 Elo and Plus (Thinking) by **over 420 Elo**
against non-TabPFN models (220 over AutoGluon 1.5 extreme) (§5). Up to **20× faster than TabPFN-2.5 inference**. SOTA on many-class
classification, on the RelBenchV1 relational benchmark via a relational checkpoint, on TabSTAR
(tabular-text) via Plus, and 2nd on the fev-bench time-series benchmark via a TabPFN-TS-3
checkpoint.

**Strengths.** Genuine scaling breakthrough with exact-equivalence row chunking, calibrated full
predictive distributions, up to 20× faster inference, and zero real-data contamination.

**Limitations.** Vendor report with no peer review or prior ablations, a closed-box "Thinking"
mode, a cell-budget bottleneck when rows and features are both large (where Real-TabPFN-2.5 can
still win), and a license barring commercial/production use.

---

<a id="attention-benchmark"></a>

## 2026-05 — Schambach et al. — Benchmarking Attention for Tabular Foundation Models

**Venue:** Proceedings of the 2nd ICML Workshop on Foundation Models for Structured Data,
2026 · **SAP SE** · [OpenReview](https://openreview.net/forum?id=rwtcugrpDq) ·
**PDF:** [open](papers/2026/05_Schambach_et_al._Benchmarking_Attention_for_Tabular_Foundation_Models.pdf)

**Citation key:** `2026.SCHAMBACH.benchmarkingattentiontabularfoundationmodels`.

**Where it fits.** Measures the implementation cost beneath the architectural scaling
arguments in Hollmann 2025 (*Accurate predictions on small data with a tabular foundation
model*, [summary](#tabpfn-v2-nature)). It complements Hosseinzadeh 2026 (*TabDPT-Turbo*,
[summary](#tabdpt-turbo)): a model can become faster through a better attention backend
and memory layout as well as through a different architecture. The paper explicitly notes
that its alternating-attention pattern does not directly describe TabICL's staged design.

**What it contains.** Forward/backward microbenchmarks of PyTorch SDPA's efficient and
cuDNN backends and FlashAttention-2/3/4 on an H100 NVL, using bfloat16 and non-causal
attention. The main setting has batch size 1, 12 heads and head dimension 64. Attention
across features varies 16–2,048 columns at 1,024 rows; attention across samples varies
32–16,384 rows at 64 columns. Each timing uses warmup and 50 repetitions, with wrappers
checked against PyTorch's mathematical attention implementation.

In this paper's terminology, **column attention attends across features**, and **row
attention across samples**. Very short sequences favour efficient SDPA; for column attention
between 128 and 2,048 features cuDNN SDPA dominates, at **2.5–3×** the efficient-SDPA baseline
and ~1.5× FlashAttention-3. FlashAttention-3 dominates row attention above ~128 rows, reaching up
to **3.5×** the efficient-SDPA baseline and ~1.5× cuDNN. Recommended mix (H100, 12 heads, d=64):
cuDNN for column attention with more than 64 features, efficient SDPA below that; FA3 for row
attention, falling back to efficient SDPA for ≤128 rows. Its layout accepts strided
views and avoids copies required by the benchmark's SDPA wrappers. FlashAttention-4 cannot
run the main head-dimension-64 setting on Hopper. The implication is to benchmark each
axis with the actual strides, dimensions and hardware.

**Strengths.** Separates kernel throughput from tensor-layout overhead, measures backward
as well as forward execution, and publishes code and supplementary shape sweeps. Explains
why a backend optimised for long language-model sequences need not win on tabular shapes.

**Limitations.** Hardware- and software-version-specific microbenchmarks, not whole-model
training or serving measurements. The main batch-size-1 SDPA wrapper deliberately retains
copies for a layout that also supports larger batches; the authors acknowledge those copies
are not strictly required at batch size 1. Reported speedups therefore compare complete
wrappers, not kernels alone. No evidence here establishes the same ranking on A100/B200,
with causal masks, or for every TFM architecture.

---

<a id="beyond-iid"></a>

## 2026-06 — Purucker et al. — Beyond IID: How General Are Tabular Foundation Models, Really?

**arXiv:** [2606.30410](https://arxiv.org/abs/2606.30410) · **Venue:** preprint (TabArena team:
Prior Labs, U. Freiburg, INRIA, ELLIS) · **PDF:**
[open](papers/2026/06_Purucker_et_al._Beyond_IID_How_General_Are_Tabular_Foundation_Models_Really.pdf)

**Where it fits.** The empirical counterpart to the position-paper critiques: the most
systematic test to date of whether TFM "generality" survives outside the IID academic benchmark
regime — co-authored by TabPFN's own developers, which lends the negative result weight.

**What it contains.** Introduces **BeyondArena** — 142 datasets hand-curated from 1,128
candidates (via the released DataFoundry framework, now integrated into TabArena) spanning IID /
**temporal** / **grouped** splits, 100–1M rows, text and high-cardinality features — and
evaluates the *in-context learning* of three TFMs (TabPFN-2.6, TabICLv2, TabDPT) against 8
default and tuned+ensembled baselines (CatBoost, XGBoost, LightGBM, RealMLP, TabM, RF, ET,
Linear; ~$50k compute). Headline findings:

* **TFM ICL dominates tiny/small IID, low-dimensional data** — the
regime the TabPFN line was built for.
* **On BOTH non-IID sub-benchmarks — temporal and grouped splits —
tuned+ensembled RealMLP wins**, and tuned CatBoost takes high-cardinality data.
* The best-GBDT-over-best-TFM margin **grows with sample size
(Spearman ρ=+0.60) and high-cardinality categoricals (ρ=+0.47)**.
* **TFMs can still reach peak performance on 70% of datasets** (Fig. 6):
they significantly beat all other models on 49% and at least one TFM ties the best non-TFM on a
further 21%; TabICLv2 ranks first on 19% of datasets, TabPFN-2.6 on 10.5%. They are clearly
outperformed on 42 datasets — large, high-dimensional, non-IID or high-cardinality.
* Calibration ablation: TabPFN-2.6 was one of only two models that
post-hoc calibration made *worse* — native TFM calibration is already strong (GBDTs benefit most
from recalibration).

**Strengths.** Exceptional protocol rigor — application-appropriate outer/inner splits
(an ablation shows IID outer splits distort rankings on two exemplary grouped datasets to
Kendall τ=0.49 and 0.60), Friedman/Wilcoxon significance testing, per-regime practitioner
recommendations.

**Limitations.** Tests in-context learning ONLY — TFM fine-tuning / continued pretraining is
explicitly listed as untested future work; the non-IID sub-benchmarks are small (21 temporal /
18 grouped, noisy grouped rankings); TabPFN-2.6/TabDPT results beyond 100k rows are
Random-Forest-imputed.

---

<a id="tabfm"></a>


## 2026-06 — Kong and Das (Google Research) — Introducing TabFM

**Venue:** **Google Research blog post, 30 June 2026** — *not* a paper: no arXiv preprint, no
technical report, no peer review. The GitHub README states this outright ("A technical report is
not included in this repository at this time"). Authors Weihao Kong and Abhimanyu Das; the
acknowledgements credit Erez Louidor Ilan, Taman Narayan, Shuxin Nie, Rajat Sen, Yichen Zhou,
Joe Toth, Deqing Fu and Samet Oymak · **PDF:**
[open](papers/2026/06_Kong_and_Das_Introducing_TabFM_A_zero_shot_foundation_model_for_tabular_data.pdf)
(print-to-PDF of the web page; the inline links and the results figure do not survive text
extraction) · **Weights:**
[`google/tabfm-1.0.0-pytorch`](https://huggingface.co/google/tabfm-1.0.0-pytorch) · **Code:**
[`google-research/tabfm`](https://github.com/google-research/tabfm) (JAX + PyTorch)

> **Citation trap.** The Hugging Face model card ships a BibTeX entry
> (`@article{tabfm2026, … author={Google Research} …}`) whose URL is the
> blog post. It is not a publication — do not cite it as one.

**Where it fits.** The first **big-tech entrant** into the TFM race: the post opens by framing
TabFM as bringing TimesFM's "zero-shot" logic to tabular data, and announces BigQuery
integration. Architecturally it is a TabPFN × TabICL hybrid, the same column/row-attention →
row-compression → ICL pattern that [TabPFN-3](#tabpfn-3) and Qu et al.'s TabICLv2 also adopted.

**What it contains.** The post describes three mechanisms, and is candid that each is borrowed:

* **Alternating row/column attention** over the raw table — "similar
to TabPFN" — to learn feature interactions without manual feature engineering.
* **Row compression** — each cross-attended row is collapsed into a
single dense vector.
* **ICL over compressed rows** — a dedicated Transformer attends over
the row embeddings rather than the raw grid, "adopting the highly efficient approach of TabICL",
which is what keeps inference cheap on larger tables.

**Training data is 100% synthetic**, and the post argues this is forced rather than chosen:
high-quality industrial tables are proprietary, so "synthetic tables … are effectively the only
viable option for pre-training a foundation model at this scale." It reports **hundreds of
millions of synthetic datasets**, generated dynamically from structural causal models with a
wide variety of random functions.

**Evaluation** is on **TabArena** (Elo from head-to-head win rates): 38 classification and 13
regression datasets, 700–150,000 samples, in two configurations —

| Configuration | What it is |
|---|---|
| **TabFM** | out-of-the-box, single forward pass, no tuning or cross-validation |
| **TabFM-Ensemble** | adds cross features and SVD features; 32-way ensemble whose weights come from a non-negative least-squares solver; **Platt scaling** as a calibration step for classification |

The headline claim is that TabFM "consistently outperforms heavily tuned, industry-standard
supervised algorithms". The post announces that TabFM is being integrated into **BigQuery**: "in
the coming weeks" users will be able to call it via an `AI.PREDICT` SQL command — announced, not
yet live at the time of the post. Weights and code are on Hugging Face and GitHub; the post points
to the GitHub page for per-fold TabArena results.

**From the released repository and model card, not the post (not verified in this library).**
The classification `config.json` follows the TabICL-style three-stage layout (column stage with
256 inducing points, row stage, 24-block ICL stage, embedding dimension 256); the model card
describes a hard cap of 10 classes; code is Apache-2.0 but the pretrained weights carry a
non-commercial, non-production licence (`tabfm-non-commercial-v1.0`). No parameter count is
published.

**Strengths.** A third lab arriving at the column/row attention → row compression → ICL design,
released with weights, code and per-fold results, plus an announced SQL deployment path.

**Limitations.** A blog post, not a paper: no specification of the synthetic prior beyond "SCMs
with random functions", no ablations, no significance tests and no calibration metrics. The Elo
comparison exists **only as a figure** (separate classification and regression top-10 pools);
the text names only AdaBoost, XGBoost, random forests and unversioned TabPFN/TabICL, so it
supports no quotable claim about ranking against the current TabPFN or TabICL frontier.
**TabFM-Ensemble is not single-forward-pass zero-shot** — it adds cross/SVD features, a 32-way
NNLS-weighted ensemble and Platt scaling. Attribute claims to Google's blog, not the literature.

---

<a id="memory-efficient-tfms"></a>


## 2026-07 — Luo et al. — Memory Efficient Tabular Foundation Models

**arXiv:** [2607.27546](https://arxiv.org/abs/2607.27546) (30 July 2026) · 2nd Foundation Models
for Structured Data (FMSD) Workshop @ ICML 2026 · Commonwealth Bank of Australia + Australian
Institute for Machine Learning, University of Adelaide · **PDF:**
[open](papers/2026/07_Luo_et_al._Memory_Efficient_Tabular_Foundation_Models.pdf)

**Where it fits.** The deployment-cost counterpart to [TabDPT-Turbo](#tabdpt-turbo), written
from an industry-practitioner perspective. Where Turbo redesigns the model to cut inference cost,
this compresses an existing model's weights after the fact to cut storage and distribution
cost. Post-training quantization is an open alternative to the proprietary v2.5/v3 distillation
engines, though it targets a different cost.

**What it contains.** The framing is explicitly practitioner-side: adoption depends "not only on
predictive performance, but also on whether these models can be deployed and communicated
efficiently", with enterprises contending with memory movement, hardware constraints and
bandwidth. The paper applies three post-training **INT4 weight-quantization** methods — **GPTQ**,
**AWQ** and **K-Means** codebook quantization — to **TabPFN v2.5 and v2.6** only (TabICL is
discussed but not quantized), on 30 OpenML datasets against default and tuned GBDT, kNN and RF
baselines.

The headline "**7.6×**" (≈87% reduction) is the ratio of **BZIP2-compressed checkpoint file
sizes** (≈41 MB → ≈5.4 MB for K-Means INT4), i.e. storage/distribution cost (§3.2, Table 1).
All three methods reach 6.0–7.65× with accuracy loss ≤0.005 (K-Means best, −0.001), and all
quantized variants stay above the best classical baseline (tuned LightGBM, 0.864). A K-Means
bit-width ablation (Table 2) makes INT4 the practical optimum: 2-bit recovers only ~90% of
baseline accuracy and 1-bit collapses to near-random. **Inference memory (~4.7 GB) and runtime
are essentially unchanged** (<2% and ±10%; Appendix Table 4), because inference cost is
dominated by attention activations rather than weights.

**Strengths.** The contribution is practical rather than methodological: it applies known
compression methods, and its value is in having measured them on this model class and reported
the trade-off curve. That is precisely what a practitioner needs and what the research
literature had not supplied.

**Limitations.** Being a workshop paper it is short (12 pages), the evaluation is narrower than
a full benchmark, and — as the authors state — weight quantization leaves the activation-dominated
inference memory untouched (activation quantization is future work), so it is complementary to,
not a substitute for, the architectural work in TabDPT-Turbo and the row-compression line. No calibration analysis is reported, which matters because quantization
can plausibly perturb predicted probabilities more than it perturbs accuracy.

---

<a id="credit-risk-benchmark"></a>

## 2026-07 — Baesens et al. — Foundation Models for Credit Risk Prediction: A Game Changer?

**arXiv:** [2605.18147v2](https://arxiv.org/abs/2605.18147v2), **15 July 2026** · preprint;
no publication venue recorded in Zotero · **KU Leuven-led multi-institution collaboration** ·
**PDF:** [open](papers/2026/07_Baesens_et_al._Foundation_Models_for_Credit_Risk_Prediction_A_Game_Changer.pdf)

**Citation key:** `2026.BAESENS.foundationmodelscreditriskpredictiongamechangera`.

**Where it fits.** Tests whether general-purpose TFMs transfer to both default prediction
and loss severity without domain-specific adaptation. It complements Tanna 2026
(*Data Presentation Over Architecture*) on context construction, and qualifies any broad
reading of Purucker 2026 (*Beyond IID: How General Are Tabular Foundation Models, Really?*,
[summary](#beyond-iid)): strong credit-domain cross-validation results do not answer the
separate question of temporal or grouped generalisation.

**What it contains.** **14 PD and 7 LGD datasets**, public and proprietary, evaluated against
29 classification and 22 regression methods in total — counts that **include** the TFMs (five
for PD: TabPFN, TabPFNv2, TabPFN-Real, Mitra, TabICL; only TabPFNv2 for LGD) alongside classical,
GBDT and deep tabular baselines (§4.3). TFMs use their default configurations while
competitors receive up to 20 Optuna trials within each training fold. Five-fold evaluation
uses a 20% validation subset of each training fold; preprocessing is fitted within the fold,
classification thresholds maximise validation F1, and LGD predictions are clipped to [0,1].
The study reports discrimination, proper probability scores, threshold-based metrics and
regression errors, alongside Friedman and Holm-corrected Wilcoxon comparisons.

TabICL has the highest mean PD AUC (**0.7517**, versus CatBoost's **0.7494**) and wins
18/70 PD folds; TFMs together win 44.3%. TabPFNv2 is the **only LGD TFM** and wins 16/35
folds, with mean R² **0.4455** versus CatBoost's **0.4401**. Probability quality changes
the PD ordering: TabPFNv2's Brier score/log loss are **0.1320/0.4119**, versus TabICL's
**0.1619/0.5081**. Learning curves show the largest TFM advantage with little data;
XGBoost overtakes v2 beyond roughly 8,000 rows in the reported LGD experiment.

**Strengths.** Includes regression on bounded, often bimodal losses rather than treating
credit risk as classification alone. Reports probability scores, respects fold boundaries
in preprocessing and tuning, and distinguishes average performance from pairwise evidence.

**Limitations.** **None of the 231 LGD pairwise comparisons is significant after Holm
correction**; the results establish competitiveness and promising small-data behaviour,
not universal superiority. The protocol provides no temporal/grouped holdout result;
distribution shift, reject inference, fairness and low-default-specific testing are future
work. Only one regression TFM is evaluated, proprietary data restrict reproducibility,
and beta/two-part LGD baselines are left for future work. Brier/log loss assess probability
quality but do not isolate calibration, and clipped point-error metrics do not validate
the full LGD predictive distribution. This benchmark does not test continued pretraining.

---

<a id="shaheen-retrieval"></a>

## 2026-08 — Shaheen et al. — Understanding the Surprising Generalization Properties of Tabular Foundation Models

**arXiv:** [2608.17957](https://arxiv.org/abs/2608.17957) (18 August 2026, preprint) ·
Polytechnique Montréal / Mila / Chandar Lab · University of Toronto · **Layer 6 AI** ·
**Prior Labs** / ELLIS Institute Tübingen / University of Freiburg · Cohere ·
**PDF:** [open](papers/2026/08_Shaheen_et_al._Understanding_the_Surprising_Generalization_Properties_of_Tabular_Foundation_Models.pdf)

**Where it fits.** The most direct challenge in this collection to the claim the
whole paradigm was built on. Every model here descends from
[Müller et al. 2021, *Transformers Can Do Bayesian Inference*](#pfns-2021)'s argument that a PFN approximates the Bayesian posterior
predictive *under its prior* — which entails that downstream tasks must lie in the
prior's support. This paper shows a model pretrained on **one real table** transferring
to a semantically unrelated one, and argues the Bayesian account cannot accommodate
that. It is also the strongest confirmation yet of [Nagler 2023, *Statistical Foundations of Prior-Data Fitted Networks*](#nagler-theory)'s 2023
localisation analysis, and it is written across the two rival labs: the Layer 6 AI team
behind [TabDPT](#tabdpt) together with **Frank Hutter**, TabPFN's own senior author.

**What it contains.** The setup is deliberately austere: the row-based backbone shared
by TabPFN v1 and TabDPT, TabDPT's pretraining procedure, retrieval disabled during
pretraining (enabled at inference), and **one real dataset per model**. Eighty-eight
such models are trained, one per TabDPT pretraining dataset, and each is evaluated on
107 held-out datasets — 72 CC-18 classification and 35 CTR-23 regression tasks, with no
overlap between pretraining and evaluation.

The headline is the title's "surprising": a transformer trained only on **vectorized MNIST**
produces strong in-context performance on **California Housing**, and one trained only on the
COLLEGES table roughly matches a random forest across both benchmark suites. Three regularities
follow.

- **Transfer is universal or absent.** Rank correlation across evaluation sets is high:
  a pretraining table that helps on one downstream task tends to help on all of them.
  There is *no* within-domain advantage — some domains are simply better to pretrain on
  (other-science good, deterministic-simulated poor).
- **Feature count predicts transfer; row count does not.** An XGBoost regressor over
  simple dataset meta-features recovers **R² = 0.67** of the variance in downstream
  generalisation, and **number of features dominates the importances** while number of
  instances has negligible predictive power.
- **Unique task count is the active ingredient.** Because pretraining manufactures tasks
  by picking a target column and a feature subset, a wide table yields combinatorially
  many tasks — which is why width, not height, matters. More unique tasks during pretraining
  consistently gives better transfer (Fig. 4).

Scaled to a 1,732-dataset OpenML corpus (§3), the task-centric view gives an asymmetric and
practically useful result: **column-level** cleaning (dropping constant/near-constant,
excessively correlated or uninformative columns) consistently improves downstream performance;
**exact deduplication** (1,732 → 1,535 datasets) makes no significant difference; and
**filtering to feature-rich datasets (≥30 features, 607 datasets) degrades performance across the
board**, because dropping low-feature datasets removes task diversity that higher per-dataset
quality does not offset.

The interpretive claim is the paper's real contribution. It argues the prior-fitting account is
unsatisfying because it requires the downstream task to be covered by the prior, which
single-table transfer contradicts outright, and proposes instead that TFMs learn a
**retrieval-and-aggregation procedure** — closer to k-nearest neighbours than to a fitted
predictor. Three pieces of evidence: a "retrieve and copy" probe showing model quality tracks
its ability to locate relevant rows *within its own context* (offered as the tabular analogue of
induction heads in LLMs); an architectural intervention tying `W_Q = W_K` under
qk-normalisation, which makes each attention score an explicit negative squared distance and so
strictly more kNN-like; and the observation that the strongest single-dataset models converge on
similar attention-map patterns, hinting at a shared retrieval space.

**Strengths.** The experiment is the argument: 88 single-table pretrainings against 107
held-out datasets is an expensive, clean design, and holding architecture and procedure
fixed while varying only the pretraining table is the same controlled discipline
[O'Prior](#oprior) brought to synthetic priors. The width-over-height finding is
immediately actionable for anyone assembling a real-data corpus, and the
column-versus-dataset asymmetry is the rare corpus-design result that tells you what
*not* to bother doing. The retrieval account also retrofits an explanation onto several
otherwise loose ends in this literature — why retrieval-based models (LoCalPFN, TabDPT)
gained most, why Nagler's localisation gap was where the headroom lay, and why
context construction can outweigh model choice. Cross-lab authorship including TabPFN's
senior author makes the challenge to the Bayesian framing hard to dismiss as rivalry.

**Limitations.** The authors are candid: they cannot exclude mechanisms besides learned
retrieval, so the account is the best available reading rather than a demonstration. Two
scope limits matter more for this collection. The study uses **only real-data
pretraining**, so it does not directly license claims about the synthetic-prior models
that dominate the frontier — the very models whose Bayesian justification it questions.
And it uses **only row-based attention** (TabPFN v1 / TabDPT), not the cell-based
bi-attention of TabPFN v2 or the column-compress designs of TabICL and v3, so whether
the retrieval story holds for the current architectures is untested. Being a preprint,
it is also unreviewed, and no calibration is reported — which is a real gap given that
calibrated posteriors are precisely what the Bayesian framing was invoked to explain.

---

<a id="exaone-tabular-1"></a>

## 2026-08 — Eo et al. — EXAONE Tabular 1.0: Technical Report

**arXiv:** [2608.25774](https://arxiv.org/abs/2608.25774) · technical report ·
LG AI Research · weights and code released ·
**PDF:** [open](papers/2026/08_Eo_et_al._EXAONE_Tabular_1.0_Technical_Report.pdf)

**Where it fits.** A direct intervention in the architectural argument that has quietly become
the field's main design question: *where, if anywhere, should a model collapse a row into a
single vector?* Two camps had formed.
[TabPFN v2](#tabpfn-v2-nature) keeps a representation per **cell** and alternates attention
along the feature and sample axes.
[TabICL](#tabicl-2025), [TabICLv2](#tabiclv2) and
[TabPFN-3](#tabpfn-3) instead compress each row into a fixed-dimensional embedding *before* a
separate dataset-level ICL stage — the move that bought them their row-count scaling.
EXAONE Tabular argues the compression boundary itself is the defect, and removes it. It is also
a fourth industrial lab entering the field, after Prior Labs, Amazon
([Mitra](#mitra)) and Google ([TabFM](#tabfm)).

**What it contains.** The architecture is the **Cross-Axis Summary Transformer (CAST)**. Every
layer performs feature-axis attention within an item, then support-conditioned item-axis
attention within a feature, so cell-level state survives the whole depth of the network and
support-set context formed at one layer can still reshape feature representations at the next.
The two axes are stitched together by learned summary tokens with complementary roles: 32
feature-summary tokens per feature join that feature's item-axis sequence, while item-summary
tokens join each item's feature-axis sequence. Query items neither attend to one another nor
update support state, preserving the conditional independence of test predictions that
[Müller et al. 2021, *Transformers Can Do Bayesian Inference*](#pfns-2021) built in from the
start.

Pretraining is **exclusively synthetic**, from a structural-causal-model prior, with no real
tables at any stage. Classification and regression are separate checkpoints of 20.81M and 21.1M
parameters sharing the architecture. Missing values are consumed natively — no imputation, with
missingness itself informing the representation. The regression head directly predicts **999
conditional quantiles** (τ = k/1000); the point prediction is a trapezoidal average over the
central 99.8% of the sorted quantile function (§2.2). By default classification uses eight
test-time estimators (preprocessing and permutation variants) — test-time ensembling, distinct
from the post-hoc ensembling it does not use.

The results are the reason to care:

| Benchmark | Classification | Regression |
|---|---|---|
| **TabArena** (51 tasks) | **1st overall**, single default config, no tuning or post-hoc ensembling; ≈125 Elo over TabPFN-3 at comparable latency | reaches [TabFM](#tabfm)'s regime at ≈1/11 the inference cost |
| **BCCO / TALENT** | 2nd | **1st** |
| **ScoringBench** | — | **best mean rank** on R², RMSE *and* CRPS |

On the combined TabArena Pareto plot EXAONE is statistically tied with TabFM at roughly **1.3% of
the parameters** (Fig. 1). The tie is softer than it reads: on regression TabFM still ranks first,
with EXAONE within overlapping 95% CIs; the 1.64B figure counts the weights stored in TabFM's
evaluated checkpoint rather than a published parameter count; and both sides use ensembling at
inference (EXAONE's 8 test-time estimators; TabFM's leaderboard numbers are taken as reported).

**Strengths.** The compression-boundary claim is a real, falsifiable architectural argument
rather than another benchmark entry, and the efficiency result is the strongest evidence for it.
Ranking first *on a single default configuration*, against tuned-and-ensembled baselines and
4-hour AutoML pipelines, is the honest form of the comparison — the form that
[Purucker et al. 2026, *Beyond IID*](#beyond-iid) and others have repeatedly argued the field
skips. Native missing-data handling is unglamorous and matters enormously on real tables. The
**ScoringBench** result is notable because leading CRPS rewards the whole predictive
distribution, not just the conditional mean — a property most benchmarks never measure.

**Limitations.** It is a technical report, not a peer-reviewed paper, and the headline numbers
are taken from official leaderboards rather than re-run in a matched environment. More
substantively, **there is no ablation isolating CAST** from the prior and the training recipe —
so the central architectural claim is supported by end-to-end wins rather than by the controlled
comparison that would actually establish it, the same gap this library has flagged whenever a
closed prior is involved. The classification head caps at **10 classes**, falling back to an
ECOC decomposition whose cost grows with the label space: the same ceiling that
[APT](#apt) and [EquiTabPFN](#equitabpfn) had each already attacked by different routes, back
again. And the synthetic-only prior plants it firmly on one side of the question that
[Real-TabPFN](#real-tabpfn) and [Shaheen et al. 2026, *Understanding the Surprising Generalization Properties of Tabular Foundation Models*](#shaheen-retrieval) keep prying open.

---

<a id="tabiclv2"></a>

## 2026-09 — Qu et al. — TabICLv2

**arXiv:** [2602.11139](https://arxiv.org/abs/2602.11139) · **PDF:**
[open](papers/2026/09_Qu_et_al._TabICLv2_A_better_faster_scalable_and_open_tabular_foundation_model.pdf)

**Provenance.** ICML 2026 / PMLR 306; first released 11 February 2026.
The filed PDF is arXiv v2, dated 16 September 2026. Appendix L adds ensemble-size,
direct statistical, few-shot, LLM-comparison and label-noise experiments. Most
ensemble gains occur by eight members; the 16-example benchmark ranks behind
RealTabPFN-2.5. LLM comparisons cover only nine classification datasets. Random
forest routing reduces memory but worsens TabICLv2 accuracy and runtime. These
bounded comparisons do not establish universal superiority or robustness.


**Where it fits.** Direct successor to TabICL — full state-of-the- art tabular FM, **fully
open** (inference code, model weights, synthetic-data engine, and pretraining code), explicitly
framed as a "let's democratize the recipe so the field can build on top" release. Beats
RealTabPFN-2.5 on TabArena even after RealTabPFN-2.5 is hyperparameter-tuned, ensembled, and
fine-tuned on real data.

**What it contains.** Three pillars of contributions, each with substantial detail.

1. **A novel synthetic-data generation engine** focused on
*diversity*: random graphs whose nodes apply eight random function types (MLPs, CatBoost-inspired
symmetric tree ensembles, discretisation, GPs, linear, quadratic, EM-style plateaus, products),
with no node-level Gaussian noise, plus ExtraTrees-based filtering of too-easy/degenerate
datasets (§3, Fig. 4). (The controllable-difficulty hierarchical SCM is LimiX's, cited as
related work.) The release of this generator is part of the paper's open-science contribution.
2. **Architectural innovations.** The most interesting one for
the TabPFN line addresses the "attention fading" problem — as context length n grows, vanilla
softmax's denominator grows too, flattening the attention distribution. Scalable Softmax (SSMax,
Nakanishi 2025) scales logits by `s log n` with a learnable per-head s, and concurrent theory
(Chen et al. 2025) shows `log n` scaling is necessary. TabICLv2's own variant is **QASSMax**
(query-aware scalable softmax): queries are rescaled by an MLP of `log n` (base scaling) times a
query-dependent tanh gate, applied in the column and ICL transformers. This is what unlocks
generalisation to **million-scale datasets in under 50 GB GPU memory**.
3. **Optimisation protocol.** Replaces AdamW with the **Muon**
optimizer (Jordan 2024), which converges faster on the transformer-style training loop. Combined
with the new prior and architecture, this delivers TabICLv2's headline result: surpassing the
strongest previously-published TFM (RealTabPFN-2.5) on TabArena and TALENT benchmarks **without
any hyperparameter tuning**.

Comprehensive ablations quantify each contribution.

**Strengths.** Strong untuned benchmark results with open weights and synthetic pretraining, and
ablations showing the prior is the largest effect (with strong architecture×prior interaction).

**Limitations.** Mean-imputes missing values (harmful for informative missingness), ignores
column-name semantics, never reports calibration despite log-loss metrics, and the
small auxiliary benchmarks limit broader robustness claims. The v2 paper reports the prior and pretraining code released; the earlier pending-release limitation is superseded.

---

<a id="tabpfn-3-5"></a>

## 2026-09 — Jäger et al. — TabPFN-3.5: Technical Report

**arXiv:** [2609.17895](https://arxiv.org/abs/2609.17895) · technical report · **Prior Labs** (47 authors) ·
code Apache 2.0, weights under a bespoke *TabPFN-3.5 License v1.0* ·
**PDF:** [open](papers/2026/09_Jager_et_al._TabPFN_3.5_Technical_Report.pdf)

**Filed version.** arXiv v2, 22 September 2026; the report itself is dated 14 September 2026.
The revised report expands the architecture presentation and comparator references.
Its seven-suite headline uses the best family member per suite, including API-only
variants; it is not a seven-suite win by a single downloadable checkpoint.


**Where it fits.** The successor to [TabPFN-3](#tabpfn-3), four months on — but the more
interesting relationship is with
[Purucker et al. 2026, *Beyond IID*](#beyond-iid). That paper, **co-authored by Prior Labs
itself**, found that TFMs win on clean i.i.d. benchmarks and then lose to tuned RealMLP and
CatBoost exactly where practitioners live: temporal and grouped splits, wide tables, and
high-cardinality categoricals. TabPFN-3.5 targets those slices specifically and measures itself
on that same benchmark. It is the cleanest critique → targeted fix → re-measurement loop in this
collection, and rare in a literature where critiques usually go unanswered.

**What it contains.** The architecture *keeps* TabPFN-3's overall design and revises four things.
Per-cell encodings now pass standardised values through **Fourier features** — a bank of learned
frequencies with sine and cosine — rather than a linear projection only, explicitly borrowed from
[TabFM](#tabfm); the model **width doubles while the KV-cache size stays unchanged**, which is
what keeps cached inference deployable; classification and regression collapse into a **single
jointly trained checkpoint** where v3 had two; and the synthetic prior is retuned toward
high-cardinality categoricals, wide tables, and *grouped* data where the test set comes from a
different group than the training set, taking some inspiration from the
[TabICLv2](#tabiclv2) prior.

The release is a family. **TabPFN-3.5** and **TabPFN-3.5-Fast** are open checkpoints in the
`tabpfn` package, Fast running up to 6× faster than 3.5 with a small accuracy drop; **-Plus**
(multimodal text and date handling, plus proprietary inference optimisations) and **-Thinking**
(inference-time compute scaling, up to 12× faster than TabPFN-3-Thinking) are API-only.

The headline is a clean sweep — first place on all seven benchmarks:

| Benchmark | What it probes | Win rate vs. best other TFM |
|---|---|---|
| TabArena | standard i.i.d. tabular | 57% (TabFM) |
| **BeyondArena** | **grouped / temporal / wide** | 83% (TabICLv2) |
| STRABLE | string-valued columns | 98% (TabICLv2) |
| MulTaBench | text and images | 90% (TabICLv2) |
| RelArena-α | relational data | 57% (RT-PluRel) |
| TALENT | 300-dataset breadth | 80% (TabICLv2) |
| ScoringBench | predictive distributions | 78% (EXAONE) |

Mean win rate 78% against the best competing TFM and 89% against the best non-foundation model.

**Strengths.** The evaluation is the broadest in this corpus, and — unusually — most of it runs
on benchmarks built to *expose* TFM weakness rather than confirm strength. Answering your own
lab's published critique, on that critique's own benchmark, is the right way to close a loop, and
it makes the BeyondArena column the most load-bearing number in the report. Doubling width while
holding the cache fixed is a deployment-minded choice rather than a leaderboard one. Taking the
Fourier encoding from TabFM and prior ideas from TabICLv2 is also a healthy sign: the frontier
labs are now reading each other rather than diverging.

**Limitations.** No ablation separates the four changes, so which of encoding, width, joint
training or prior produced the BeyondArena gain is unknown — the attribution problem
[O'Prior](#oprior) named, in the paper best placed to have avoided it. The TabPFN-3.5 and -Fast
**weights are downloadable but restrictively licensed** (TABPFN-3.5 License v1.0: research and
internal evaluation allowed; no commercial or production use of the models, derivatives or
outputs; §4), the strongest members are API-only, and **-Plus**/**-Thinking** implementation
details are proprietary, so several headline numbers cannot be reproduced from released
artifacts. It is self-reported and unreviewed. And a 78% mean win rate means roughly one
split in five still goes to another model, with no analysis of which or why.

---

<a id="mitra-v2"></a>

## 2026-09 — Tao et al. — Mitra-v2 Technical Report

**arXiv:** [2609.04540](https://arxiv.org/abs/2609.04540) · technical report · **Amazon** ·
weights, inference and finetuning code all **Apache-2.0** ·
**PDF:** [open](papers/2026/09_Tao_et_al._Mitra_v2_Technical_Report.pdf)

**Where it fits.** The successor to [Mitra](#mitra), and a sharper version of its thesis. Mitra-v1
argued for *mixing* priors; Mitra-v2 argues for *widening the task distribution* while keeping
the backbone. It is **not** a controlled prior-versus-architecture comparison of the kind
[O'Prior](#oprior) calls for: the authors' own Limitations state that context length, feature
range, prior mixture, optimizer, distributed recipe and checkpoint all changed at once.

**What it contains.** The backbone barely moves: the same 12-layer 2D-attention Tab2D stack,
hidden width 512, four heads; the classification model stays at 75.7M parameters and only the
regression model grows (75.7M → 76.7M). What changes is what it is trained *on*:

| | Mitra-v1 | Mitra-v2 |
|---|---|---|
| Max support rows in pretraining | 512 | **5,120** |
| Query rows | 128 | 1,280 |
| Max features | 16 | **50** |
| Prior mixture | SCM + tree | SCM + **Hybrid SCM** + tree |
| Optimizer | AdamW | **Muon** |
| Hardware | 8× A100 40GB | 4 nodes × 8 H200 |

The **Hybrid SCM** is the new ingredient: a prior that can place *qualitatively different*
mechanisms at successive nodes of a single causal graph, so heterogeneity appears within a task
rather than only between tasks.

On TabArena it reaches overall Elo 1,775 against TabFM's 1,774, EXAONE's 1,749 and TabPFN-3's
1,638 — matching a **1.64B**-parameter model with **77M**, about 5% of the size. On TALENT's 12
datasets with **more than ten classes** it ranks first, via a wrapper rather than natively: the
head emits at most 10 logits, so labels are split into a balanced hierarchical tree of ≤10-class
subproblems (a root Mitra node routes, one leaf node per group predicts; recursing above 100
classes), with a different class-to-group assignment per bagged member (§2).

**Strengths.** Shows how far a fixed backbone can be pushed by widening the pretraining task
distribution, and the hierarchical wrapper extends a 10-class head to many-class tasks with
first-place results. The licence matters too: weights
*and* finetuning code under Apache-2.0, at a moment when
[TabPFN-3.5](#tabpfn-3-5) ships restricted weights and its best variants behind an API.

But the real distinction is the **Limitations section, which is the most candid in this
collection** — see below.

**Limitations.** Stated by the authors, in their own words and worth repeating because almost no
other technical report here does it. The bootstrap intervals across the leading group **overlap**,
so the top of the board "is best read as a statistical tie rather than a strict ordering", and the
regression board rests on 13 datasets. The headline system uses finetuning and eight-fold bagging,
so it "should not be described as zero-shot or Pareto-dominant" — a caveat that quietly undercuts
the single-forward-pass framing the whole paradigm markets itself on. And under **incomplete
training provenance** they concede that context length, feature range, prior mixture, optimizer,
distributed recipe and checkpoint all changed at once with no ablation isolating any of them,
and that accelerator hours and realised prior-mixture frequencies are not recoverable.

That last admission is the same gap as [EXAONE](#exaone-tabular-1) and
[TabPFN-3.5](#tabpfn-3-5). The difference is that Mitra-v2 declares it, which makes the paper more
useful than its competitors even where it is weaker.

---

<a id="xiaomi-tabldm"></a>

## 2026-09 — Team et al. — Xiaomi-TabLDM: A Tabular Foundation Model Technical Report

**arXiv:** [2609.03880](https://arxiv.org/abs/2609.03880) · technical report · **Xiaomi** ·
weights and code released ·
**PDF:** [open](papers/2026/09_Team_et_al._Xiaomi_TabLDM_A_Tabular_Foundation_Model_Technical_Report.pdf)

**Where it fits.** A fifth industrial lab, after Prior Labs, Amazon ([Mitra](#mitra)), Google
([TabFM](#tabfm)) and LG ([EXAONE](#exaone-tabular-1)). Architecturally it sits squarely in the
row-compression camp — column embed → row aggregate → ICL — and borrows QASSMax directly from
[TabICLv2](#tabiclv2), so it is confirmation rather than challenge on that axis. What is new is
**conditional capacity**: it is the first model in this collection to put a **sparse
Mixture-of-Experts** inside a TFM. Its strongest results are on **regression**.

**What it contains.** Three stages, each modified.

**Column-wise embedding** uses **dual-stream feature grouping**, extending TabICLv2's
circular-shift trick. TabICLv2 groups each column with two others at fixed dyadic offsets
(1, 2, 4); Xiaomi runs that stream *and* a second with width-adaptive offsets
`(1, ⌊√s⌋, s)` that stretch as wide as the table allows, summing the two embeddings. Grouped
columns are then encoded by a Set Transformer with inducing-point attention.

**Row-wise aggregation** prepends learnable CLS tokens and replaces the plain additive residual
with a lightweight **Attention Residual**, adaptively fusing the outputs of preceding blocks.

**ICL prediction** keeps the usual asymmetry — training rows attend to each other, test rows
attend only to training rows — and replaces the feed-forward sub-layer of *selected* layers with
a **sparse MoE**, so different experts can specialise across heterogeneous datasets.

**Test-time scaling** is context-adaptive: feature shuffling and subsampling, complementary
preprocessing views (normalisation schemes, quantile transforms, SVD representations, feature
interactions, and target transforms for heavy-tailed regression), combined by non-negative least
squares — the NNLS combination of SVD/cross-feature views is credited by the authors to
[TabFM](#tabfm) (§3). Pretraining uses a three-stage curriculum over dataset size (1,024 →
10,240 → 60,000 samples; §2.2), a standard progressive-length schedule rather than a new idea;
the regressor uses a pinball loss over 999 quantiles.

Results are strongest on regression: **1st on OpenML-CTR23** across 33 regression datasets
(average rank 3.03), and 2nd on regression across TALENT, TabArena and BCCO. On TabArena
regression it takes second place on Elo while using **82% less training time and 68% less
prediction time** than the top-ranked TabFM. Classification is also competitive: on TALENT it
ranks **2nd overall** (behind TabFM) and **ties TabFM for best on binary classification**; it is
4th overall on TabArena (§4).

**Strengths.** Regression is the neglected half of this literature — most models are tuned and
reported on classification — and leading a 33-dataset regression suite is a meaningful result.
The MoE is the first serious attempt to give a TFM conditional capacity rather than uniformly
more of it, which is a different scaling lever from anything else here. Weights and code are
released.

**Limitations.** There is **no limitations section at all**, which is conspicuous beside
[Mitra-v2](#mitra-v2)'s unusually frank one. No ablation separates the five changes — MoE,
dual-stream grouping, Attention Residual, three-stage schedule and enlarged prior — so the
paper's novel component is unevidenced as a *cause* of anything. Several test-time and training
ingredients are borrowed (QASSMax from TabICLv2, NNLS view-ensembling from TabFM). And like its
peers it is a self-reported technical report scored against public leaderboards, not a reviewed
paper.

---

<a id="limix-2"></a>

## 2026-09 — Zhang et al. — LimiX-2: A Contextual Mechanism Network Towards General Structured-Data Intelligence

**arXiv:** [2609.17488v1](https://arxiv.org/abs/2609.17488v1), 15 September 2026 · technical
report · **LimiX Team, Stable AI & Tsinghua University** ·
**PDF:** [open](papers/2026/09_Zhang_et_al._LimiX_2_A_Contextual_Mechanism_Network_Towards_General_Structured_Data_Intelligence.pdf)

**Citation key:** `2026.ZHANG.limix2contextualmechanismnetworkgeneralstructureddataintelligence`.

**Where it fits.** Extends the case for retaining cell representations made by Eo 2026
(*EXAONE Tabular 1.0*, [summary](#exaone-tabular-1)), while broadening the training
objective beyond a designated target. Its Contextual Mechanism Network (CMN) framing
seeks the conditional joint structure of a table through target prediction and masked
feature reconstruction. This is a different causal claim from Robertson 2025 (*Do-PFN*)
or Ma 2026 (*Foundation Models for Causal Inference via Prior-Data Fitted Networks*):
the new empirical test is graph-skeleton recovery, not treatment-effect estimation.

**What it contains.** Synthetic-SCM pretraining with **Context-Conditional Masked Modeling
(CCMM)** over entry, column and block masks. Dual-axis attention retains separate cell
representations, with separate feature/task pathways and four task embeddings. A query
can attend to context but not other queries, and context representations cannot absorb
queries. The same conditional interface supports classification, regression and feature
reconstruction. Capacity is scaled from **12.5M to 406.2M parameters** under a fixed
data-generation, optimisation and inference recipe.

The report evaluates 51 TabArena datasets, 288 TALENT datasets (12 tasks with more than
10 classes excluded), and 156 BCCO datasets. The 406.2M model **ranks first on all three
benchmarks** (Fig. 1), with aggregate Elo **1935, 1506 and 1432**, respectively, with bootstrap
intervals; TALENT/BCCO use 15 seeds. On six causal
discovery datasets, thresholded feature-attention scores recover undirected skeletons
with mean F1 **0.7972**, compared with **0.6591** for EXAONE. These are the report's own
benchmark snapshots, not scores directly comparable with Elo from another comparison set.

**Strengths.** Makes feature reconstruction an explicit pretraining task and evaluates
more than label prediction. The controlled capacity sweep is stronger evidence for
parameter scaling than comparing unrelated models, and the report supplies detailed
prediction protocols and causal-skeleton baselines.

**Limitations.** Unreviewed technical report; scaling fits extrapolated to 2B parameters
are projections, not measurements. The reported conditional-prediction objective does
not by itself prove a globally consistent joint distribution or identify interventions.
Skeleton recovery neither orients edges nor estimates causal effects; distributing each
group's attention uniformly across its features disadvantages compressed/grouped models
in that probe. No controlled CCMM-versus-target-only ablation isolates the objective's
contribution from architecture and prior changes. The main prediction benchmarks do not
establish temporal/grouped robustness or predictive calibration.

---

<a id="causilo"></a>

## 2026-09 — Cho et al. — Causilo Technical Report

**arXiv:** [2609.22866v1](https://arxiv.org/abs/2609.22866v1), 19 September 2026 · technical
report · **Nums AI** ·
**PDF:** [open](papers/2026/09_Cho_et_al._Causilo_Technical_Report.pdf)

**Citation key:** `2026.CHO.causilotechnicalreport`.

**Where it fits.** A compromise between Qu 2026 (*TabICLv2*, [summary](#tabiclv2)) and
the persistent-cell route of Eo 2026 (*EXAONE Tabular 1.0*, [summary](#exaone-tabular-1))
and Zhang 2026 (*LimiX-2*, [summary](#limix-2)). It retains row compression for efficient
ICL, but first gives cells another exchange across both features and context rows.
Despite the name, the report concerns predictive tabular modelling rather than causal
effect estimation.

**What it contains.** **Column encoding → row refinement → column refinement → row
compression → ICL**. The row-refinement stage exchanges information through persistent
summary tokens; the second column stage lets enriched cells revisit the context before
compression. Both row modules use a fixed number of summary tokens, making feature-side
attention linear rather than quadratic in feature count. Inducing tokens bound the
column stages, while the final ICL stage still has quadratic context attention. Bounded
QASSMax and normalisation/feature/class-permutation ensembles complete the recipe.

Classification/regression models have **36.08M/37.08M parameters**, trained on roughly
**36M synthetic tables**. In its September 2026 TabArena snapshot, Causilo reports
**1785.4 Elo at 0.1043 seconds per 1K test samples** (median): it **outperforms
TabPFN-3.5-Fast with 31.6% less inference time** and exceeds TabFM's Elo with **63.8× faster
inference** (abstract, §1), occupying a faster, lower-Elo point than full TabPFN-3.5 or LimiX-2. BeyondArena results lead the evaluated set at combined Elo
**1359**, but that comparison adds Causilo to published baselines only through TabPFN-3.
ScoringBench additionally reports **CRPS** alongside point-error metrics: Causilo lies
on the reported performance/latency frontier, while full TabPFN-3.5 remains more accurate
at greater latency.

**Strengths.** Gives an explicit feature-scaling argument and a targeted timing probe,
reports serving cost alongside accuracy, and includes non-IID and distributional-regression
evaluation. Supplies a concrete design between immediate row compression and retaining
cells throughout the model.

**Limitations.** Unreviewed report without an ablation isolating refinement, bounded
QASSMax, prior and ensembling. Linear feature-side attention does **not** imply linear
scaling in context rows; the microbenchmark times selected modules, not whole-model
scaling. The BeyondArena result does not compare against TabPFN-3.5 or LimiX-2, and Elo
depends on the benchmark snapshot and comparator set. CRPS is a proper distributional
score, not a standalone calibration guarantee. The report distinguishes Apache-2.0 code
from separately licensed weights restricted to non-commercial research, with commercial
or hosted use requiring a separate licence.

---

<a id="multabench-benchmarking-multimodal"></a>

## 2026-09 — Arazi et al. — MulTaBench: Benchmarking Multimodal Tabular Learning with Text and Image

**arXiv:** [2605.10616v2](https://arxiv.org/abs/2605.10616v2), **27 September 2026** ·
**NeurIPS 2026, Evaluations and Datasets track** (identified on the filed PDF;
Zotero records the arXiv preprint) · **Technion-led multi-institution collaboration** ·
**PDF:** [open](papers/2026/09_Arazi_et_al._MulTaBench_Benchmarking_Multimodal_Tabular_Learning_with_Text_and_Image.pdf)

**Citation key:** `2026.ARAZI.multabenchbenchmarkingmultimodaltabularlearningtextimage`.

**Where it fits.** Turns the representation argument in Arazi 2025 (*TabSTAR: A Tabular
Foundation Model for Tabular Data with Text Fields*) into an explicit evaluation target
for both text and images. Spinaci 2025 (*ConTextTab: A Semantics-Aware Tabular In-Context
Learner*) shows that frozen semantic embeddings can work well on CARTE; MulTaBench asks
where they lose target-relevant information. Like Purucker 2026 (*Beyond IID*,
[summary](#beyond-iid)), it qualifies the generality implied by a benchmark win, but
through modality and representation requirements rather than temporal/grouped splits.
It is an owner-selected evaluation paper in the mirrored Zotero collection, not a new TFM.

**What it contains.** **40 datasets: 20 text-tabular and 20 image-tabular**, spanning
classification/regression, 400–114,000 rows and 1–245 structured features. A further
**40 candidates** meet the joint-signal criterion, producing an 80-dataset extended
collection. The main set deliberately requires both **Joint Signal** (joint frozen
representations outperform either modality alone) and **Task-awareness** (target-aware
representations outperform joint frozen ones). Both gains must reach **0.001** in
rounded mean AUC/R² for the same **at least three of five** curation learners:
LightGBM, CatBoost, TabM, TabPFNv2 and TabPFN-2.5.

The four conditions are structured-only, unstructured-only, joint frozen, and joint
target-aware. Text/image encoders are **e5-small-v2 / DINOv3-small**; target-aware
representations (TAR) tune their last three layers with LoRA, then use 30 PCA components
as tabular inputs. Encoder adaptation uses training labels only, with an internal 90/10
checkpoint-selection split. It is performed **without the structured features**, so it
is target adaptation rather than evidence for a jointly trained fusion architecture.
Regression labels are discretised into 20 quantile bins for this encoder-training step.
The curation experiments use five seeds and cap training at 10,000 examples per fold.

TAR gains extend to learners outside the curation panel, including TabICLv2 and TabDPT.
The authors report significant TAR-over-frozen gains on **37/40 datasets** (Appendix G.1), but
that test pools all learners with both conditions — up to 12 per dataset, **including the five
curation models** whose results selected the datasets — so it is not an out-of-panel result. Larger encoders and
15/60-dimensional projections preserve the pattern, with a smaller experiment also
removing PCA. ConTextTab's CARTE strength does not transfer to this selected text subset.
Only two of the nine main image-tabular datasets containing text pass the paper's strict
trimodal criterion. No new multimodal TFM is trained or proposed as a finished solution.

**Strengths.** Makes complementary modality information and representation adaptation
separately testable; includes unimodal controls, additional learners, encoder-size and
dimension ablations, and sensitivity to the curation panel and thresholds. Releases
the broader candidate collection so evaluation can also cover cases where frozen
embeddings suffice. The PDF explicitly acknowledges selection bias and adaptation cost.

**Limitations.** Selection deliberately favours tasks on which the tested TAR recipe
helps, so neither its model ranking nor the prevalence of TAR gains estimates general
multimodal performance. The curation models have an intrinsic selection advantage;
new-learner robustness reduces, but does not remove, dependence on the chosen encoders
and selection rule. There is no per-dataset HPO, and tuning cost can dominate downstream
learning. Supervised encoder tuning must be repeated within each evaluation fold; a
globally target-tuned embedding cache would leak labels. The results motivate joint
modelling but do not establish that an ICL-only, label-free or jointly conditioned
representation method reproduces the supervised TAR gains.

---

<a id="test-time-compute"></a>

## 2026-10 — Ning et al. — Test-Time Compute for Tabular Foundation Models: Mechanisms, Gains, and Limits

**arXiv:** [2610.12005v1](https://arxiv.org/abs/2610.12005v1), **8 October 2026** · preprint;
no publication venue recorded in Zotero · **University of Connecticut / Morgan Stanley** ·
**PDF:** [open](papers/2026/10_Ning_et_al._Test_Time_Compute_for_Tabular_Foundation_Models_Mechanisms_Gains_and_Limits.pdf)

**Citation key:** `2026.NING.testtimecomputetabularfoundationmodelsmechanismsgainslimits`.

**Code reference:** [upstream implementation](https://github.com/kanghui-learning/test-time-compute-for-tabular-foundation-models),
mirrored in `Test-Time Compute for Tabular Foundation Models.txt` with automatic refresh;
the [repository guide](REPOSITORIES.md#test-time-compute-code) maps adaptation,
aggregation, retrieval and evaluation to the corresponding source files.

**Where it fits.** Revisits Rubachev 2025 (*On Finetuning Tabular Foundation Models*,
[summary](#on-finetuning)) on newer backbones and separates mechanisms that Thomas 2024
(*Retrieval & Fine-Tuning for In-Context Tabular Models*, [LoCalPFN summary](#localpfn))
combines. It tests how much Grinsztajn 2026 (*TabPFN-3*, [summary](#tabpfn-3)) gains
beyond its already ensembled default. Here **test-time compute includes supervised
task-specific fitting after pretraining**, not access to unseen query labels.

**What it contains.** Three axes: **adaptation, aggregation and context construction**.
Adaptation is evaluated on **51 TabArena classification/regression datasets** with
TabPFN-3, TabICLv2 and TabFM; aggregation/context studies focus on TabPFN-3, with
additional wide and large OpenML tables. A 25-setting adaptation sweep motivates
**DiagScale**: freeze pretrained weights and learn a zero-initialised diagonal
query–key multiplier, changing attention logits to `qᵀ(I + diag(δ))k`. At the logit
level this is equivalent to IA³ key scaling. Only **0.003–0.03%** of parameters train;
on regression checkpoints this is 12.7K for TabPFN-3, 7.3K for TabICLv2 and 53.8K for
TabFM. Their respective Elo gains are **+26/+82/+20**, versus **+25/+77/+28** for full
finetuning, each relative to its own frozen baseline in the specified comparison fit.
Checkpoint selection includes fallback to the pretrained model.

Increasing TabPFN-3's native ensemble from eight to 32 views reduces error by only
**0.60%**, with little further gain at 64. For a separate pool of **96 configurations**,
greedy selection using training-side out-of-fold predictions reduces error by **2.44%**
(95% CI −4.75% to −0.80%; +67 Elo), while uniform averaging **increases** it by 3.68%.
Using only one eighth of selector labels erases the estimated gain. Combining DiagScale
and greedy aggregation reaches **+93 Elo**, but costs **253.1 GPU-hours** over the
benchmark workload versus 6.61 for DiagScale alone and 247.5 for aggregation; fewer
trainable parameters do not imply a comparable reduction in fitting time.

Attention-guided retrieval can use source pools up to **10M rows**, beyond the tested
4–4.5M full-context memory boundary on an 80 GB H100. Matched random-context controls
show that *which* rows are selected matters. Yet on **COMET_MC**, retrieval raises log
loss from **0.0151 to 0.2302**, concentrating a 1.7% rare class to a median 40.3% of
retrieved contexts; correcting proportions only partially repairs the loss. Column
selection also varies by dataset. Synthetic/optimised rows, pseudo-labels and derived
features provide no consistent gain in the tested context-expansion experiments.

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
on a few datasets and the tested predictors barely forecast their magnitude (best
cross-validated R² 0.012). Frozen TabFM exceeds the heavily adapted/ensembled TabPFN-3
at lower measured total cost, so this is not evidence that extra compute on a fixed
backbone is always the best purchase. The retrieval failure and context-expansion null
results constrain the tested recipes; they do not prove all retrieval or learned-context
methods ineffective, nor do these experiments establish probability calibration.

---

<a id="tabrelibench"></a>

## 2026-10 — Zhao et al. — TabReliBench: Evaluating Tabular Foundation Models Beyond Predictive Accuracy

**arXiv:** [2610.13654](https://arxiv.org/abs/2610.13654) · preprint ·
Renmin University of China, Cerebras, National University of Singapore, MBZUAI · code released ·
**PDF:** [open](papers/2026/10_Zhao_et_al._TabReliBench_Evaluating_Tabular_Foundation_Models_Beyond_Predictive_Accuracy.pdf)

**Where it fits.** The synthesis has long listed calibration as the paradigm's most glaring
evaluation gap — claimed everywhere because a PFN approximates a posterior predictive, measured
almost nowhere. Scattered evidence existed: Brier and log loss in
[Baesens et al. 2026, *Foundation Models for Credit Risk Prediction: A Game Changer?*](#credit-risk-benchmark),
CRPS in [Cho et al. 2026, *Causilo*](#causilo), ScoringBench results in the
[EXAONE](#exaone-tabular-1) and [TabPFN-3.5](#tabpfn-3-5) reports. TabReliBench is the first paper
here built *for* the question, across eleven TFMs at once, and it separates what a single proper
score blends together: accuracy, calibration, marginal coverage, subgroup coverage and interval
width. It also tests the founding promise of
[Müller et al. 2021, *Transformers Can Do Bayesian Inference*](#pfns-2021) — that calibration
falls out of the objective — and finds it true on average and false locally.

**What it contains.** A benchmark of **160 classification and 81 regression** OpenML datasets,
five train–test repetitions each, capped at 10,000 rows so every model stays in its operating
regime. Eleven TFMs — TabPFN v2, 2.5, 3 and 3.5; TabICL v1 and v2; TabDPT 1.1 and 1.3; Causilo;
LimiX-2; TabFM — against BART, RealMLP and XGBoost, tuned and untuned. All 11 TFMs enter
classification; TabICLv1 and TabDPT 1.1 are classification-only, leaving **9 regression TFMs**,
and LimiX-2 and TabFM give no regression predictive distribution, leaving **7 distributional
TFMs** (§3). The main benchmark fixes the inference ensemble at **E = 8** members per TFM; an
ensemble-size study varies E over {1, 4, 8, 16, 32} (§5.1). The dataset is the unit of analysis,
which is why it needs far more datasets than TabArena's 51.

Five findings, each a correction to how this literature usually reads a leaderboard:

| Finding | What it qualifies |
|---|---|
| **Rankings move** between TabArena and TabReliBench, and between metrics: LimiX-2 leads accuracy and R², TabPFN-3.5 leads Brier, classwise ECE and CRPS, Causilo leads confidence-ECE and regression calibration | "the best TFM" is not a well-defined object |
| Regression TFMs reach **near-nominal 90% marginal coverage** with narrow intervals, untouched | the Bayesian promise — on average |
| **Worst-slab (subgroup) coverage stays heterogeneous**, often poor | the same promise — locally |
| **Ensembling** improves accuracy and proper scores but does **not** consistently improve calibration | the default 4/8-way ensemble as a calibration device |
| **Conformal post-processing** — four global and five covariate-adaptive variants — helps BART far more than TFMs, and does not remove subgroup undercoverage | conformal as the standard fix |

A dataset-level analysis adds that most score variation is *between datasets* rather than
between TFMs, so meta-features predict whether TFMs will do well much better than which TFM
will. Local class overlap is a warning sign for both classification accuracy and calibration;
for regression, prediction quality and calibration track *different* dataset properties.

TFMs nonetheless dominate the classical baselines: all eleven rank ahead of every baseline on
accuracy and Brier, and all seven distributional regression TFMs rank ahead on CRPS and every
calibration diagnostic.

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

**arXiv:** [2610.13253](https://arxiv.org/abs/2610.13253) · preprint · ETH Zurich · code released ·
**PDF:** [open](papers/2026/10_Cannistraci_and_Vogt_Tabular_Foundation_Models_Are_Effectively_Shallow.pdf)

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

**What it contains.** The tool is a **closed-form, label-free affine translator**: fit on a small
unlabelled calibration split, it maps the hidden state *entering* a contiguous window of
transformer blocks to the state *leaving* it, so the window can be skipped. The window is chosen
by minimising forward KL divergence of the outputs. Single-axis models get one shared map;
dual-axis models (TabPFN v2, LimiX) need a separate map per feature index. If the outputs survive,
those blocks were doing work a linear map can absorb; if they collapse, they were doing
genuinely nonlinear composition.

Across **8 TFMs from 6 families on 171 classification datasets**:

- Replacing **half** the blocks costs at most **0.002 median AUROC** for every architecture, with
  up to 97% of datasets within one point of the full model. Half-depth TabFM still beats every
  other *full-depth* TFM and tuned GBDTs.
- Pushing to **a single block** keeps TabPFN-3, Orion-BiX and TabICL within a median 0.007
  AUROC; a one-block TabPFN-3 serves cached queries **2.4× faster in 6× less memory**.
- Families are over-parameterised **differently**: TabPFN-3 leans on its encoders and survives
  whichever single block is kept; other single-axis models do most of their work in the first
  block; dual-axis models concentrate it in one critical block.
- Naively dropping blocks collapses the model, and early exit is worse than the translator —
  the map is doing real work.
- A controlled study at nanoTabPFN scale (Pfefferle et al. 2025, *nanoTabPFN*) shows a 12-layer model compressed to *k*
  layers matches one trained from scratch at depth *k*, and a natively trained 6-layer model
  matches the full 12.

Overall: the translator can replace **up to 96% of blocks** (one block kept), removing up to
**1.5B parameters** (TabFM) with up to **6× faster** GPU inference at a median cost of 0.03 AUROC.

**Regression (§5.2, 41 datasets).** At half depth regression is near-lossless (median R² cost
0.001–0.026), but with one block kept most regressors degrade sharply (TabPFN-3 −0.132 R²;
TabFM the exception at −0.022): predictions shrink toward the mean and rankings worsen, so late
blocks refine output ordering in regression.

**Strengths.** Intervention rather than observation: instead of inferring redundancy from
representation similarity or attention maps — which the paper shows correspond inconsistently
with actual replaceability — it removes the blocks and measures. The translator is closed-form
and label-free, so it costs almost nothing and needs no downstream labels, which is what makes
it usable in the privacy-constrained settings the paper motivates. Breadth (eight models, six
families) turns a curiosity into a property of the paradigm. And the per-family diagnosis of
*where* depth lives is new information about architectures that the model papers themselves
never report.

**Limitations.** The main 171-dataset study is classification scored by AUROC — a ranking
metric that is blind to calibration, which is precisely what [TabReliBench](#tabrelibench) shows
can degrade while ranking metrics hold. The smaller regression study shows the extreme
(single-block) headline does not carry over to regression without loss. Dual-axis models whose per-feature maps grow with width (LimiX-16M) lose the
memory advantage on very wide tables. The compression-equals-shallow-training result is shown
only on a 1.4M-parameter nanoTabPFN; whether it holds at production scale is explicitly open. It
is a preprint, and a closely related ICML 2026 study (*Is one layer enough?*, not in this
collection) reached a neighbouring conclusion independently.

---

<a id="survicl-a-foundation"></a>

## 2026-10 — Alberge et al. — SurvICL: a Foundation Model for in-context Survival Analysis

**arXiv:** [2610.22242v1](https://arxiv.org/abs/2610.22242v1), **15 October 2026** · preprint;
no publication venue recorded in Zotero · **Inria Saclay / EPFL / Probabl** ·
**PDF:** [open](papers/2026/10_Alberge_et_al._SurvICL_a_Foundation_Model_for_in_context_Survival_Analysis.pdf)

**Citation key:** `2026.ALBERGE.surviclfoundationmodelincontextsurvivalanalysis`.

**Where it fits.** Extends Qu 2026 (*TabICLv2: A better, faster, scalable, and open
tabular foundation model*, [summary](#tabiclv2)) to **right-censored time-to-event
prediction**. Like Robertson 2025 (*Do-PFN*), it uses simulator-accessible outcomes
that real observations do not reveal: the context remains censored, while synthetic
query targets are uncensored event times. Its controlled prior ablations complement
Bouadi 2026 (*O'Prior*, [summary](#oprior)). It also broadens the distributional evidence
alongside Zhao 2026 (*TabReliBench*, [summary](#tabrelibench)), while evaluating a
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
stages. Development ablations hold the architecture fixed: the PO prior beats Cox,
AFT and alternative survival priors, while adding a censoring-time prediction head
hurts. These ablations use a shallower model trained for only 10,000 steps.

The benchmark has **103 datasets: 40 for development and 63 held out from design
decisions**, compared against **20 baselines**. Each held-out dataset receives ten
event-stratified 80/20 train/test splits. SurvICL uses at most **4,096 context rows**
without per-dataset tuning; test sets are also capped at 4,096. Tunable baselines
receive up to 50 random-search trials, with their seed-0 choice reused across splits.

On the held-out set, the reported **pairwise IBS win rate is 82.9%**, versus Cox's
71.3%; for the median-horizon IPCW C-index it is **77.7%**, versus random survival
forests' 71.6%. These percentages aggregate comparisons over datasets and competitors;
they are not direct head-to-head win rates against the named runner-up. SurvICL leads
overall IBS significantly. Below 1,000 samples it ranks above Cox in IBS, but that
subgroup difference is **not statistically significant**; above 1,000, SurvivalBoost
leads IBS. It is competitive on the runtime/performance frontier, while reported
baseline runtime excludes hyperparameter search. Additional metrics are MAE-Hinge and
**KM-calibration**, comparing the mean predicted survival curve with the test-set
Kaplan–Meier curve. Its average KM-calibration rank is 6.0, behind the covariate-free KM
estimator (4.3), Cox (5.0), DeepSurv (5.6) and sksurv GBS-Cox (5.9); KM and Cox's Breslow
baseline enforce this calibration by construction.

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
