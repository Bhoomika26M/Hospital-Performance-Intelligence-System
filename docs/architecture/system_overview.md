# Aegis.dv – System Architecture & Data Engineering Overview

**Document ID:** AD-ARCH-001  
**Project:** Aegis.dv – Hospital Operations & Patient Analytics Dashboard  
**Author:** Ananya Biju (Infosys Springboard Internship)  

---

## 1. Architectural Philosophy

Aegis.dv is engineered around five fundamental software and data principles:
1. **Separation of Concerns:** Ingestion, cleaning, validation, feature derivation, KPI calculation, and export are completely decoupled into distinct Python modules within `src/`.
2. **Determinism & Reproducibility:** Every pipeline execution from raw data to Tableau extracts produces bit-for-bit identical results with verified checksums.
3. **Data Quality Transparency:** No records are silently dropped or altered. Missingness and outliers are handled through explicit indicators rather than destructive imputation.
4. **Tableau Integration:** Native support for high-performance `.hyper` extracts and structured multi-tab Excel workbooks.
5. **Ethical Compliance:** Strict adherence to HIPAA Safe Harbor de-identification standards and transparent labeling of synthetic reference elements per Section 3 policies.

---

## 2. Directory & Module Architecture

```
Aegis/
├── src/
│   ├── acquisition/          # Automated downloading, retries, SHA-256 verification
│   ├── preprocessing/        # Data loading, deduplication, missing handling, departments, timeline
│   ├── validation/           # Schema validation contracts, Tukey IQR outlier auditing
│   ├── feature_engineering/  # Derived clinical cohorts, care pathways, intensity scores
│   ├── kpi/                  # Pure tested KPI mathematical functions, summary generator
│   └── export/               # CSV, multi-tab Excel, Hyper extract, synthetic capacity generator
├── scripts/
│   ├── data_collection.py    # CLI wrapper for raw ingestion
│   ├── run_pipeline.py       # Master end-to-end deterministic runner
│   ├── generate_hospital_kpis.py # CLI scorecard generator
│   └── generate_storyboard.py# ReportLab programmatic wireframe PDF builder
├── tests/                    # Pytest test suite (20 tests covering schema, KPIs, reconciliation)
├── data/                     # Raw, interim, and processed data artifacts
├── dashboard/                # Calculations repository, specs, build guide, companion HTML
├── reports/                  # Data quality reports, test results, reconciliation, QA checklist
└── docs/                     # Full architecture, diagrams, dictionary, decision logs, guides
```

