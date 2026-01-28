# USV Social Communication Platform

A modular research and data science platform for analyzing ultrasonic vocalizations (USVs) in mouse social interaction studies. This project integrates scalable data pipelines, statistical modeling, sequence analysis, and validation frameworks to quantify how genotype and social context shape vocal communication.

---

## Motivation

Ultrasonic vocalizations are a key behavioral signal in rodent social communication and are widely used in neuroscience and autism research. However, USV datasets are often large, fragmented, and difficult to analyze reproducibly.

This platform was designed to:
- Standardize multichannel USV outputs
- Enable statistically rigorous inference
- Model vocal behavior as dynamic sequences
- Support validation and future multimodal expansion

---

## Platform Architecture

The repository is organized as a **multi-project ecosystem**, where each project can stand alone while contributing to a unified analysis pipeline.
```text
USV-Social-Communication-Platform/
│
├── project_1_data_intake/ # Data ingestion & cleaning
├── project_2_statistical_engine/ # Statistical inference & reporting
├── project_3_vocal_networks/ # Sequence & network modeling
├── project_4_social_scoring/ # Behavioral feature engineering
├── project_5_validation/ # Detection accuracy & benchmarking
├── project_6_multimodal_design/ # Future neural integration (design)
│
├── shared/ # Common utilities, schemas, configs
├── data/ # Data access rules & documentation
└── README.md
```

---

##  Project Overview

### **Project 1 — Multichannel USV Data Intake**
- Ingests VocalMat outputs across sessions and microphones  
- Standardizes timestamps, frequency metrics, call classes, genotype, and context  
- Produces clean, analysis-ready datasets  

**Focus:** data engineering, automation, reproducibility

---

### **Project 2 — Context & Genotype Statistical Engine**
- Mixed-effects models (mouse as random effect)  
- Nonparametric tests across social contexts  
- Effect size estimation and automated reporting  

**Focus:** applied statistics, experimental design

---

### **Project 3 — Vocal Transition & Network Modeling**
- Transition probability matrices between call classes  
- Markov-style sequence modeling  
- Network-based comparisons across genotype and context  

**Focus:** time-series analysis, network science

---

### **Project 4 — Social Engagement Scoring**
- Feature engineering of vocal behavior  
- Composite social responsiveness metrics  
- Per-mouse engagement profiles  

**Focus:** behavioral quantification, product-style analytics

---

### **Project 5 — Validation & Accuracy Benchmarking**
- Comparison of VocalMat vs STFT-based pipelines  
- Precision, recall, F1, and overlap metrics  
- Error pattern analysis  

**Focus:** validation, scientific rigor, ML-style evaluation

---

### **Project 6 — Multimodal Expansion (Design)**
- Timestamp alignment architecture for neural + vocal data  
- Schema and visualization design for multimodal studies  

**Focus:** systems thinking, computational neuroscience

---

##  Reproducibility & Data Policy

- Raw and processed experimental data are **not tracked** in Git  
- All analyses are reproducible from standardized inputs  
- Configuration files and schemas define expected formats  

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
- Autism model behavioral analysis
- Data science and ML-oriented behavioral modeling
- Reproducible academic or industry-facing pipelines

---

##  Author

**Calantha Mohanraj**  
Data Science & Statistics 
GitHub: https://github.com/calantha168

---

## License

MIT License


