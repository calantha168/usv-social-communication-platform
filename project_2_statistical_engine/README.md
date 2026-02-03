# Project 2 — Context & Genotype Statistical Analysis Engine

This module implements a **statistically rigorous framework** to quantify how **genotype, sex, and other dyad-level experimental factors** influence ultrasonic vocal behavior during mouse social interaction sessions.

The focus is on **defensible statistical inference**, **effect size estimation**, and **reproducible reporting**, rather than ad-hoc or call-level comparisons that violate independence assumptions.

Project 2 serves as the **inferential core** of the USV Social Communication Platform.

---

## Key Design Constraint (Important)

In this dataset, **individual ultrasonic vocalizations cannot be attributed to a specific mouse** within an interaction.  
Each session represents a **dyadic interaction between two mice**, and calls are only known to occur *within that session*.

As a result:

- Calls are **not independent samples**
- Mouse-level inference is **not valid**
- The **interaction session (dyad)** is the experimental unit

All statistical logic in this project is built around this constraint.

---

## Objectives

The primary objectives of Project 2 are to:

- Enforce correct **experimental units** and prevent pseudoreplication  
- Encode the **true hierarchical structure** of the data (call → session)  
- Support analysis with **known, unknown, or inferred contextual variables**  
- Separate **exploratory analysis** from **formal hypothesis testing**  
- Produce **analysis-ready summary tables** at valid aggregation levels  
- Enable statistically valid comparisons across **genotype and sex compositions**  
- Ensure all results are **transparent, reproducible, and reviewer-defensible**

---

## Data Hierarchy

The hierarchy used in Project 2 reflects the data-generating process:

Call -> Session (Dyadic Interaction)

- **Call**: individual detected ultrasonic vocalization  
- **Session**: interaction between two mice (dyad)  

Genotype and sex are treated as **dyad-level attributes**, not nesting levels.

---

## Scientific Questions

This engine is designed to address questions such as:

- Do interaction sessions with different **genotype compositions** (e.g., WT–WT vs WT–KO) differ in vocal behavior?
- Do **sex compositions** (MM, MF, FF) influence vocal duration or frequency?
- Which acoustic features (e.g., duration, frequency) show the strongest differences across dyad types?
- Are observed effects robust at the **session level**, rather than driven by call counts?
- How do results change when additional contextual variables are introduced or inferred?

---

## Input Data

Project 2 consumes a **canonical, analysis-ready call-level dataset** produced upstream in **Project 1 (Phase 1.0)**.

### Input Characteristics
- One row per detected call  
- Schema-validated and metadata-joined  
- No statistical aggregation applied  
- Stored in a columnar format (e.g., Parquet)

Contextual variables (e.g., condition, arena state) are **optional** and may be added later without altering the inference framework.

> Project 2 does **not** ingest raw Excel outputs directly.

---

## Output Artifacts

Project 2 produces the following analysis tables:

### 1. Call-Level Table
- Grain: **one row per call**
- Used for:
  - Exploratory visualization
  - Distributional inspection
  - Optional mixed-effects modeling with session as a random effect
- **Not used** for hypothesis testing assuming independence

---

### 2. Session-Level Summary Table (**PRIMARY**)
- Grain: **one row per interaction session**
- Used for:
  - Hypothesis testing
  - Effect size estimation
  - Final reporting and figures

Typical session-level metrics include:
- Number of calls per session
- Mean and median call duration
- Mean call frequency
- Proportion of harmonic or noisy calls
- Call class composition (optional)

---

### 3. Dyad-Type Summary Table (Optional)
- Grain: **genotype/sex composition**
- Used for descriptive summaries across sessions only

---

## Statistical Analysis Plan

### Experimental Unit
- **Primary unit:** session (dyadic interaction)

Calls within a session are treated as repeated measurements.

---

### Duration and Frequency (Continuous Outcomes)

All tests are performed on **session-level summaries**.

#### Two-Group Comparisons
- **Welch’s t-test** (default)
- **Mann–Whitney U** (nonparametric fallback)

#### Three or More Groups
- **Welch ANOVA** (default)
- **Games–Howell** post-hoc tests
- **Kruskal–Wallis** with **Dunn’s test** (nonparametric alternative)

---

### Call Counts per Session
- **Negative Binomial regression** (preferred when overdispersed)
- Welch-based tests on session counts (simpler alternative)

---

### Effect Sizes (Always Reported)
- Cohen’s *d* / Hedges’ *g* (two groups)
- η² / partial η² (ANOVA)
- Rate ratios for count models
- 95% confidence intervals where applicable

---

## Hard Constraints

- No hypothesis testing on raw calls assuming independence  
- Session is the experimental unit unless emitter identity becomes available  
- Effect sizes accompany all p-values  
- Social context is **not assumed** to exist  

---

## Project Structure

```text
project_2_statistical_engine/
├── schemas/          # Hierarchy and table contracts
├── src/stat_engine/  # Loading, aggregation, QC, statistics
├── data/
│   ├── raw/          # Placeholders only
│   ├── derived/      # Session-level analysis tables
│   └── results/      # Statistical outputs and figures
├── docs/             # Inference policy and data dictionary
└── tests/            # Smoke and validation tests
```
