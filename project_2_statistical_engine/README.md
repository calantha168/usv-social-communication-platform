# Project 2 — Context & Genotype Statistical Analysis Engine

This module implements a statistically rigorous framework to quantify how **genotype** and **social context** influence ultrasonic vocal behavior in mouse models. The focus is on defensible inference, effect size estimation, and reproducible reporting rather than ad-hoc comparisons.

---

##  Objectives

- Quantify differences in vocal behavior across **genotypes** and **social contexts**
- Avoid pseudoreplication by respecting experimental hierarchy
- Produce interpretable statistical summaries and effect sizes
- Generate automated, reproducible analysis reports

---

##  Experimental Structure

The analysis explicitly models the hierarchical structure of the data:

Call -> Session -> Mouse -> Genotype


Primary inference is performed at the **mouse level**, with session-level analyses used for secondary validation. Call-level analyses are treated as exploratory and require appropriate aggregation or modeling assumptions.

---

##  Features Analyzed

- Call duration
- Mean / peak frequency
- Call rate per session
- Call class proportions
- Context-specific vocal profiles

---

## 📈 Statistical Methods

### Mixed-Effects Modeling
- Linear mixed-effects models
- Mouse treated as a random effect
- Fixed effects include genotype, social context, and interactions

### Nonparametric Testing
- Used when distributional assumptions are violated
- Context-wise comparisons across genotypes
- Paired and unpaired designs supported

### Effect Sizes
- Cohen’s d
- Rank-biserial correlation
- Confidence intervals where applicable

Statistical significance is always interpreted **alongside effect size**, not in isolation.

---

##  Output Artifacts

- Clean summary tables (mouse- and session-level)
- Effect size comparison tables
- Diagnostic plots and assumption checks
- Automatically generated statistical reports

Outputs are written to structured folders for downstream visualization and interpretation.

---

##  Reproducibility & Design Principles

- No raw data stored in the repository
- All analyses driven by standardized schemas
- Clear separation between data preparation and inference
- Deterministic pipelines with documented assumptions

---

##  Implementation (Planned)

src/
├── build_summary_tables.py
├── mixed_effects_models.py
├── nonparametric_tests.py
├── effect_sizes.py
└── generate_reports.py


---

##  Key Questions Addressed

- Do autism-model mice vocalize differently than controls?
- Which social contexts elicit the strongest vocal changes?
- Are observed differences driven by magnitude, structure, or variability?

---

##  Why This Matters

This engine transforms raw behavioral measurements into **statistically defensible insights**, aligning with best practices in neuroscience, biostatistics, and data science.

It is designed to scale to additional features, contexts, and future multimodal integration.


