# R Statistical Analysis — Project 2

This directory contains all **statistical analyses performed in R** for **Project 2 — Context & Genotype Statistical Analysis Engine**.

R is used here as the **analysis and reporting layer**, while Python serves as the **data intake and aggregation engine**. This separation ensures statistical rigor, reproducibility, and clarity.

---

## Purpose of This Folder

The R analysis layer is responsible for:

- Running all **formal statistical tests**
- Computing **effect sizes and confidence intervals**
- Generating **publication-ready tables and figures**
- Ensuring all inference respects the **true experimental unit**

Importantly, **no hypothesis testing is performed in Python**.

---

## Experimental Unit (Critical)

In this dataset, **individual ultrasonic vocalizations cannot be attributed to a specific mouse**.  
Calls occur during **dyadic interaction sessions**, and are therefore **not independent samples**.

As a result:

- **Calls** are treated as repeated measurements  
- **Sessions (dyadic interactions)** are treated as the **independent experimental units**

All statistical inference in this folder is performed at the **session level**, in accordance with best practices for avoiding pseudoreplication.

---

## Analysis Workflow

The R analysis follows a strict, reproducible sequence:

### Step 1 — Build Session-Level Summary Table
**Script:** `01_build_session_summary.R`

- Reads the analysis-ready call-level dataset
- Aggregates calls into **one row per session**
- Computes:
  - number of calls
  - mean / median duration
  - mean / median frequency
  - proportions (harmonic, noisy, call classes if available)
- Saves the session summary table to `data/derived/`

This table is the **sole input** for all downstream hypothesis testing.

---

### Step 2 — Duration & Frequency Analysis
**Script:** `02_duration_frequency_tests.R`

Analyzes **continuous acoustic outcomes**:

- Call duration
- Call frequency

Tests used (depending on number of groups):

- Welch’s *t*-test (2 groups)
- Welch ANOVA (3+ groups)
- Games–Howell post-hoc tests
- Nonparametric fallbacks:
  - Mann–Whitney U
  - Kruskal–Wallis + Dunn’s test

All results include **effect sizes** and **confidence intervals**.

---

### Step 3 — Call Count Models
**Script:** `03_counts_models.R`

Analyzes **number of calls per session**:

- Preferred approach:
  - Negative Binomial regression
- Simpler fallback:
  - Welch-based tests on session counts

Outputs include:
- rate ratios (IRR)
- confidence intervals
- diagnostic plots

---

### Step 4 — Proportions & Call Class Analysis
**Script:** `04_proportions_and_classes.R`

Analyzes session-level proportions such as:

- proportion of harmonic calls
- proportion of noisy calls
- call class composition (if available)

Proportions are **computed per session first**, then compared across groups using
Welch or nonparametric tests.

Raw call-level categorical tests are **not used**, to avoid pseudoreplication.

---

## Folder Structure

```text
analysis/r/
├── README.md
├── 00_setup.R
├── 01_build_session_summary.R
├── 02_duration_frequency_tests.R
├── 03_counts_models.R
├── 04_proportions_and_classes.R
└── helpers/
├── stats_utils.R
└── plotting_utils.R
```
---

## How to Run the Analysis

From the `project_2_statistical_engine/` directory:

```bash
Rscript analysis/r/00_setup.R
Rscript analysis/r/01_build_session_summary.R
Rscript analysis/r/02_duration_frequency_tests.R
Rscript analysis/r/03_counts_models.R
Rscript analysis/r/04_proportions_and_classes.R

