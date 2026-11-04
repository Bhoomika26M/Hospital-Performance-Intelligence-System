# Aegis.dv – Data Directory Architecture & Provenance

This directory contains raw, interim, and processed data artifacts for Aegis.dv, adhering strictly to HIPAA de-identification standards, open research licenses, and reproducibility guidelines.

---

## Directory Structure

```
data/
├── raw/                      # Immutable raw data artifacts as received from source
│   ├── diabetes_130_us_hospitals.zip  # Original downloaded ZIP archive from UCI repository
│   ├── diabetic_data.csv              # Extracted primary encounter data (101,766 rows, 50 features)
│   ├── IDs_mapping.csv                # Code lookup tables for admission types, dispositions, sources
│   ├── hospital_raw_data.csv          # Canonical raw encounter dataset for the pipeline
│   └── MANIFEST.json                  # Cryptographic checksums (SHA-256), date accessed, source URLs
├── interim/                  # Intermediate transformed data artifacts (standardized, typed, validated)
│   ├── encounters_cleaned_stage1.csv # Cleaned encounter rows prior to feature derivations
│   └── specialty_mapping.csv         # Medical specialty to clinical department taxonomy mapping
└── processed/                # Production-grade, validated, Tableau-ready analytical datasets
    ├── hospital_cleaned.csv          # Full cleaned encounter dataset with derived metrics (101,766 rows)
    ├── hospital_final_dataset.xlsx   # Multi-tab production workbook (Encounters, Departments, Workload)
    ├── synthetic_hospital_capacity.csv # Clearly labelled illustrative capacity dataset (Section 3 policy)
    └── Aegis_Hospital_Extract.hyper  # Native Tableau Hyper extract compiled via tableauhyperapi
```

---

## Dataset Provenance & Attribution

* **Primary Dataset:** Diabetes 130-US Hospitals for Years 1999–2008
* **Source:** UCI Machine Learning Repository (Donated by Strack et al., 2014)
* **Underlying Database:** Cerner Health Facts Clinical Data Warehouse
* **Source URL:** `https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008`
* **Direct Archive:** `https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip`
* **Licensing:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Citation:** 
  > Strack, B., DeShazo, J. P., Gennings, C., Olmo, J. S., Ventura, S., Cios, K. J., & Clore, J. N. (2014). *Impact of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000 Clinical Database Patient Records.* BioMed Research International, 2014, 781670.

---

## Data Privacy & Ethical Compliance

* **HIPAA Safe Harbor Compliance:** All records are fully de-identified. No patient names, Social Security numbers, telephone numbers, or direct personal health identifiers exist in the raw or processed files.
* **Patient Linkage:** Patient identifiers (`patient_nbr`) and encounter keys (`encounter_id`) are cryptographically randomized surrogate keys provided by Cerner Health Facts.
* **Integrity Validation:** Every raw file is cryptographically hashed with SHA-256 upon ingestion and tracked in `data/raw/MANIFEST.json`.

