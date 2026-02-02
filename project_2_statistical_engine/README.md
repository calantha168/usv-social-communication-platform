# Project 2 — Context & Genotype Statistical Analysis Engine

This module implements a **statistically rigorous framework** to quantify how **genotype** and other experimental grouping factors influence ultrasonic vocal behavior in mouse models. The focus is on **defensible inference**, **effect size estimation**, and **reproducible reporting**, rather than ad-hoc or call-level comparisons.

Project 2 serves as the **inferential core** of the USV Social Communication Platform, ensuring that all statistical conclusions respect the true experimental design and hierarchical structure of the data.

Importantly, this project **does not assume that social context is known a priori**. Context may be:
- explicitly labeled (if available),
- partially specified,
- or inferred downstream from experimental metadata or behavioral structure.

---

## Objectives

The primary objectives of this project are to:

- Enforce correct **experimental units** and prevent pseudoreplication  
- Encode the **hierarchical structure** of USV data (call → session → mouse → genotype)  
- Support analysis with **known, unknown, or inferred contextual variables**  
- Separate **exploratory analysis** from **formal hypothesis testing**  
- Produce **analysis-ready summary tables** at appropriate aggregation levels  
- Enable statistically valid comparisons across genotype and other grouping factors  
- Support transparent, reproducible, and reviewer-defensible inference  

---

## Scientific Questions

This engine is designed to address questions such as:

- Do different **genotypes** exhibit distinct vocalization patterns?
- How does vocal behavior vary **within and across individual mice**?
- Which acoustic features differ most strongly across experimental groups?
- Are observed effects robust at the **mouse (experimental unit) level**, rather than driven by call counts?
- How do results change when additional contextual variables are introduced or inferred?

---

## Input Data

Project 2 consumes a **canonical, analysis-ready call-level dataset** produced upstream in Project 1 (Phase 1.0).

**Input characteristics:**
- One row per detected call  
- Schema-validated and metadata-joined  
- No statistical aggregation applied  
- Stored in a columnar format (e.g., Parquet)

Contextual variables (e.g., social target, condition, arena state) are **optional** and may be added later without altering the core inference framework.

> Project 2 does **not** ingest raw Excel outputs directly.

---

## Output Artifacts

Project 2 produces three core analysis tables:

1. **Call-level table**
   - Used for exploratory visualization and mixed-effects modeling only

2. **Session-level summary table**
   - Used for secondary inference, sensitivity analysis, and QC diagnostics

3. **Mouse-level summary table (PRIMARY)**
   - One row per mouse × grouping variables
   - Used for hypothesis testing, effect size estimation, and final reporting

Grouping variables may include genotype alone or genotype combined with contextual factors when available.

---

## Statistical Design Principles

### Data Hierarchy

Call -> Session -> Mouse -> Genotype


### Units of Inference

| Level   | Intended Use |
|--------|--------------|
| Call   | Exploratory analysis only |
| Session| Secondary / robustness checks |
| Mouse  | **Primary experimental unit** |

### Hard Constraints

- No hypothesis testing treating calls as independent samples  
- Call-level modeling requires random effects  
- Mouse-level summaries are required for final inference  

These constraints apply **regardless of whether context is known**.

---

## Project Structure

```text
project_2_statistical_engine/
├── schemas/ # Hierarchy definitions and table contracts
├── src/stat_engine/ # Data loading, aggregation, QC, modeling
├── data/
│ ├── raw/ # Placeholders only
│ ├── derived/ # Analysis tables
│ └── results/ # Statistical outputs
├── docs/ # Inference policy and data dictionary
└── tests/ # Smoke and validation tests
```

---

## Phase Overview

### Phase 1.0 — Analysis-Ready Data (Upstream)
- Merge and validate raw outputs  
- Freeze call-level dataset  
- No statistics performed  

---

### Phase 2.0 — Hierarchy & Inference Lock-In
- Declare hierarchy and experimental units  
- Define analysis table contracts  
- Remain agnostic to unknown or future context variables  

---

### Phase 2.1+ — Modeling & Hypothesis Testing
- Quality control and outlier policy  
- Mixed-effects models and hypothesis tests  
- Optional incorporation of contextual or inferred variables  
- Effect sizes, figures, and reports  

---

## Role in the Platform

Project 2 provides the **scientific backbone** of the USV Social Communication Platform by bridging cleaned acoustic data and higher-level behavioral modeling. It ensures that all conclusions are statistically valid, reproducible, and extensible as new experimental context becomes available.


