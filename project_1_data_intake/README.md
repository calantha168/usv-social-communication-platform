# Project 1 — USV Data Intake, Validation & Schema Locking

This module defines the **data contract** for the USV Social Communication Platform. It transforms a merged, call-level VocalMat output into a **validated, analysis-ready dataset** by enforcing schema rules, locking experimental hierarchy, and documenting all assumptions before statistical modeling.

Project 1 does **not** perform inference. Its role is to ensure that all downstream analyses are reproducible, interpretable, and scientifically defensible.

---

##  Objectives

- Validate and standardize merged VocalMat call-level data
- Define and enforce a canonical schema
- Explicitly lock the experimental hierarchy
- Perform transparent quality control (QC)
- Augment metadata **without inventing unknown variables**

---

##  Input Data

### Primary Input
- `merged_vocalmat.xlsx`

Each row represents **one ultrasonic vocalization (call)** extracted using VocalMat.

### Observed Characteristics
- Call-level temporal information
- Acoustic frequency and intensity features
- Call class labels
- Partial experimental metadata (e.g., genotype, session identifiers)

---

##  Experimental Hierarchy (Locked)

Project 1 explicitly defines the hierarchy used throughout the platform:

Call → Session → Mouse → Genotype


- **Call**: individual ultrasonic vocalization (row-level unit)
- **Session**: recording session grouping calls
- **Mouse**: biological subject (may be derived or mapped)
- **Genotype**: experimental group

 **Important:**  
Explicit social interaction context (e.g., female, male, bully) is **not assumed**. Session-level variation is preserved without assigning predefined social labels.

---

##  Canonical Schema

Project 1 enforces required columns, data types, and units. Example categories include:

### Temporal Features
- `Start_time` (seconds)
- `End_time` (seconds)
- `Duration` (seconds)
- `Inter_vocal_interval` (seconds)

### Acoustic Features
- `mean_freq_main` (kHz)
- `min_freq_main` (kHz)
- `max_freq_main` (kHz)
- `Bandwidth` (kHz)
- Intensity-related measures

### Labels & Metadata
- `Class` (call category)
- `Harmonic` (binary)
- `Noisy` (binary)
- `Session`
- `Genotype`
- `source_file`

All column expectations, units, and allowed ranges are documented in shared schemas.

---

##  Quality Control (QC)

Project 1 performs **non-destructive QC checks**, including:

- Negative or zero durations
- Impossible frequency values
- Inconsistent timestamps
- Duplicate calls
- Missing critical identifiers

QC results are:
- Flagged (not silently removed)
- Reported in structured outputs
- Available for downstream inspection

---

##  Metadata Augmentation (Conservative)

Derived fields may include:
- `session_id`
- `mouse_id` (if derivable from reliable mappings)
- `recording_batch`

 No behavioral or social context labels are fabricated.  
All derived fields are explicitly documented.

---

##  Outputs

Project 1 produces:

| Output | Description |
|-----|------------|
| `clean_calls.csv` | Schema-compliant, QC-passed call-level data |
| `qc_report.csv` | Flagged rows and QC diagnostics |
| `schema.json` | Canonical column definitions |
| `README.md` | Assumptions, hierarchy, and limitations |

These outputs are the **only allowed inputs** to downstream projects.

---

##  Design Principles

- No raw or processed experimental data is committed to Git
- All transformations are deterministic and documented
- Missing metadata is acknowledged, not inferred
- Statistical validity is prioritized over convenience

---

##  Downstream Dependencies

- **Project 2** consumes aggregated outputs from this module
- **Project 3** relies on preserved call order and class labels
- **Project 4** uses validated features for behavioral scoring
- **Project 5** compares validated calls against alternative pipelines

---

##  Why This Matters

Project 1 prevents pseudoreplication, silent data leakage, and assumption drift. It establishes a transparent foundation that allows all downstream analyses to be interpreted with confidence.

This module is the **scientific backbone** of the platform.




