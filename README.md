# USV Social Communication Platform

A modular research and data science platform for analyzing ultrasonic vocalizations (USVs) in mouse behavioral studies. This platform integrates scalable data pipelines, statistical modeling, sequence analysis, and validation frameworks to quantify how **genotype and session-level behavioral states** shape vocal communication.

---

##  Motivation

Ultrasonic vocalizations are a key behavioral signal in rodent communication and are widely used in neuroscience and autism-related research. However, USV datasets are often large, fragmented, and difficult to analyze reproducibly, with incomplete or inconsistent experimental metadata.

This platform was designed to:
- Standardize and validate USV call-level data
- Enable statistically rigorous inference while respecting experimental hierarchy
- Model vocal behavior as dynamic sequences rather than isolated events
- Support transparent validation and future multimodal expansion

Because explicit social condition labels are not always available, this platform avoids assuming known interaction contexts and instead infers **behavioral structure directly from vocalization patterns**.

---

##  Platform Architecture

The repository is organized as a **multi-project ecosystem**, where each project can stand alone while contributing to a unified analysis framework.

```text
USV-Social-Communication-Platform/
│
├── project_1_data_intake/ # Data validation & schema enforcement
├── project_2_statistical_engine/ # Statistical inference & reporting
├── project_3_vocal_networks/ # Sequence & network modeling
├── project_4_social_scoring/ # Behavioral feature engineering
├── project_5_validation/ # Detection accuracy benchmarking
├── project_6_multimodal_design/ # Future neural integration (design)
│
├── shared/ # Common utilities, schemas, configs
├── data/ # Data access rules & documentation
└── README.md
```

---

##  Project Overview

### **Project 1 — USV Data Intake & Quality Control**
- Validates and standardizes merged VocalMat call-level outputs  
- Enforces schemas, data types, and experimental hierarchy  
- Performs quality control checks and metadata augmentation  

**Focus:** data engineering, reproducibility, scientific hygiene

---

### **Project 2 — Genotype & Session-Level Statistical Engine**
- Mixed-effects models with mouse and session structure  
- Nonparametric testing when assumptions are violated  
- Effect size estimation and automated statistical reporting  

This module avoids pseudoreplication by treating the mouse as the primary unit of inference and modeling session-level variability explicitly.

**Focus:** applied statistics, experimental design

---

### **Project 3 — Vocal Transition & Behavioral Network Modeling**
- Transition probability matrices between call classes  
- Markov-style sequence modeling of vocal behavior  
- Network-based comparisons across genotype and inferred behavioral states  

Rather than relying on predefined social labels, this project infers **latent behavioral regimes** directly from vocal structure.

**Focus:** time-series analysis, network science

---

### **Project 4 — Behavioral Engagement Scoring**
- Feature engineering of vocal activity and structure  
- Composite behavioral engagement indices  
- Per-mouse behavioral profiles across inferred states  

**Focus:** behavioral quantification, product-style analytics

---

### **Project 5 — Validation & Accuracy Benchmarking**
- Comparison of VocalMat outputs against STFT-based pipelines  
- Precision, recall, F1, and overlap-based accuracy metrics  
- Systematic error pattern analysis  

**Focus:** validation, scientific rigor, ML-style evaluation

---

### **Project 6 — Multimodal Expansion (Design)**
- Timestamp alignment architecture for neural and vocal data  
- Schema and visualization design for multimodal studies  
- Scalable systems planning for future integration  

**Focus:** systems thinking, computational neuroscience

---

##  Reproducibility & Data Policy

- Raw and processed experimental data are **not tracked** in Git  
- All analyses are reproducible from standardized inputs  
- Configuration files and schemas define expected formats and assumptions  

See `data/README.md` for details.

---

##  Tech Stack

- **Python** (pandas, numpy, statsmodels, networkx)
- **SQL / Postgres** (schema-driven storage)
- **Jupyter** for exploratory analysis
- **Git + GitHub** for version control
- Modular design for future ML and neural data integration

---

##  Intended Use

This platform is designed for:
- Neuroscience and bioacoustics research
- Autism-model behavioral analysis
- Data science and ML-oriented behavioral modeling
- Reproducible academic or industry-facing pipelines

---

##  Author

**Calantha Mohanraj**  
Data Science & Statistics  
GitHub: https://github.com/calantha168

---

##  License

MIT License

