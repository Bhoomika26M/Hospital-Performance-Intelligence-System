# Aegis.dv – Architectural & Methodological Decision Log

This log documents every non-trivial design, data, algorithmic, and visualization decision made in Aegis.dv, along with the engineering justification and rejected alternatives, in compliance with Section 2 (Rule 7).

---

## Decision 1: Python Runtime & Dependency Management
- **Date:** November 4, 2026
- **Decision:** Utilize Python 3.11.15 via Homebrew in an isolated virtual environment (`.venv`) with pinned `requirements.txt`.
- **Why:** macOS default Python is 3.9.6, which lacks modern performance optimizations and compatibility with modern PyPI wheels for data science tools (e.g., pandas 3.1, numpy 2.4, tableauhyperapi). Python 3.11 provides full native ARM64 support, type annotations, and maximum package compatibility.
- **Alternatives Rejected:**
  - *System Python 3.9.6:* Rejected due to age, lack of pre-built wheels for recent libraries, and risk of polluting macOS system toolchains.
  - *Global pip install:* Rejected per best-practice sandboxing and reproducibility guidelines.

---

## Decision 2: Primary Dataset Selection
- **Date:** November 4, 2026
- **Decision:** Select the **UCI Machine Learning Repository: "Diabetes 130-US Hospitals for Years 1999-2008"** dataset (`diabetic_data.csv`) as the primary real-world clinical operations dataset (101,766 patient encounters, 130 hospitals, 50 features).
- **Why:**
  1. *Real Clinical Encounter Scale:* 101,766 real inpatient encounters representing 10 years of hospital care across 130 hospital facilities from the Cerner Health Facts clinical database.
  2. *Granular Operational Fields:* Contains genuine length of stay (`time_in_hospital`, 1–14 days), distinct patient keys (`patient_nbr`), encounter IDs (`encounter_id`), medical specialty / admitting department (`medical_specialty`), admission type (`admission_type_id`), admission source (`admission_source_id`), discharge disposition (`discharge_disposition_id`), and 30-day readmission status (`readmitted`: `<30`, `>30`, `NO`).
  3. *Zero Synthetic Fabrication of Core Records:* Provides real-world clinical variance, real ICD-9 diagnoses, real medication counts, and genuine readmission outcomes.
  4. *Permissive Open Research License:* Publicly donated for scientific research, fully de-identified under HIPAA Safe Harbor.
- **Alternatives Rejected:**
  - *Fully Synthetic Datasets (e.g., Kaggle Prasad22 Healthcare Dataset):* Rejected as primary dataset because synthetic datasets feature uniform distributions, unrealistic clinical correlations, and zero real-world operational challenges.
  - *MIMIC-IV-ED:* Rejected because the full dataset requires formal institutional CITI certification and signed data use agreements (DUAs), making it unredistributable and not fully public.
  - *NYS SPARCS Inpatient Discharges:* Massive multi-gigabyte file where individual days and exact stay sequences are blurred/generalized for public use, making encounter-level flow analysis less precise.

---

## Decision 3: Policy on Missing Variables (Calendar Dates & Bed Counts)
- **Date:** November 4, 2026
- **Decision:** Strictly adhere to Section 3's "Missing-capability policy":
  1. *Calendar Dates:* The UCI dataset records encounter sequences and `time_in_hospital` (days), but intentionally omits Gregorian calendar timestamps to preserve facility anonymity across the 10-year period (1999–2008). In compliance with Section 3, all timeline visual representations are explicitly labeled: **"Reference timeline (synthetic)"** or analyzed by operational sequence/stay duration cohorts.
  2. *Bed Capacity & Staffing:* The UCI encounter dataset does not record physical hospital bed counts or nurse rosters. Following Section 3, bed occupancy/utilization KPIs are explicitly marked **"Unavailable – requires bed capacity data"** in primary views, and patient-days are used and labeled strictly as an **operational workload proxy**. For the Resource Utilization dashboard, a clearly isolated, seeded synthetic reference module (`synthetic_hospital_capacity.csv`) is provided and explicitly labeled on all visuals: **"Synthetic reference data – not real hospital figures"**.
- **Alternatives Rejected:**
  - *Fabricating real-looking calendar dates without labeling:* Strictly rejected per the "Honesty overrides completion" and "Never fabricate data" mandates.
  - *Inventing physical bed counts and presenting them as real clinical telemetry:* Strictly rejected.

---

## Decision 4: Tableau Implementation Strategy
- **Date:** November 4, 2026
- **Decision:** Execute a three-tier Tableau delivery strategy:
  1. Generate authentic, production-grade `.hyper` extract tables using `tableauhyperapi` directly in Python.
  2. Export structured, multi-tab Excel (`hospital_final_dataset.xlsx`) and tidy CSV files for universal BI compatibility.
  3. Programmatically generate a complete, valid Tableau packaged workbook (`Aegis.dv.twbx`) with structured XML (`.twb`) adhering to Tableau Desktop schemas, accompanied by full worksheet specs, calculation dictionary, and manual build guide.
- **Why:** Maximizes reproducibility across environments where Tableau Desktop GUI may or may not be installed.

---

## Decision 5: Design System & Color Palette
- **Date:** November 4, 2026
- **Decision:** Adopt the dark enterprise UI specification from the provided reference screenshot:
  - Background: `#080808`
  - Sidebar / Rails: `#1E1E1E`
  - Primary Card Containers: `#141414`
  - Secondary Cards / Hover: `#222222`
  - Accent Primary: `#5ACB57` (Vibrant Hospital Green)
  - Primary Text: `#F5F5F5`
  - Secondary Text: `#929292`
  - Borders: `#303030`
  - Light mode counterpart: Clean hospital off-white (`#F8F9FA` background, `#FFFFFF` cards, `#1E293B` text, `#2E7D32` clinical forest green).
- **Why:** Delivers a modern executive-grade visual hierarchy that passes WCAG AA contrast standards and mirrors modern enterprise healthcare command centers.

