# Aegis.dv – Comprehensive Data Quality & Validation Audit Report

**Report Identifier:** `DQR-AEGIS-2026-001`  
**Project:** Aegis.dv – Hospital Operations & Patient Analytics Dashboard  
**Developer Attribution:** Ananya Biju (Infosys Springboard Internship)  
**Execution Timestamp:** `2026-11-04T06:51:20.893509+00:00`  
**Pipeline Execution Duration:** `31.79 seconds`  

---

## 1. Executive Summary & Verification Matrix

The Aegis.dv deterministic data pipeline was executed end-to-end against the primary clinical encounter dataset (**UCI Diabetes 130-US Hospitals, 1999–2008**). Zero records were arbitrarily deleted or altered; all data transformations strictly followed documented clinical domain rules and Section 6 quality standards.

| Quality Objective | Benchmark Target | Actual Measured Metric | Audit Status |
| :--- | :--- | :--- | :--- |
| **Encounter Key Uniqueness** | Zero duplicates on `encounter_id` | **0 duplicate records** detected | **PASS (100%)** |
| **Overall Dataset Completeness** | Target > 95.0% completeness | **96.73%** complete | **PASS** |
| **Row Count Preservation** | Zero unexplained drops | **101,766 -> 101,766** (0 dropped) | **PASS (100%)** |
| **Specialty Taxonomy Mapping** | 100% of specialties mapped | **73/73 mapped** (0 unmapped) | **PASS (100%)** |
| **Mortality Readmission Handling**| In-hospital deaths excluded | **1,652 expired stays excluded** | **PASS (CMS Standard)** |
| **Temporal Sequence Validity** | Discharge >= Admission | **100% stays valid sequence** | **PASS (100%)** |

---

## 2. Before & After Data Pipeline Metrics

```
+-----------------------------------+--------------------+--------------------+
| Dimension                         | Ingestion (Raw)    | Production Output  |
+-----------------------------------+--------------------+--------------------+
| Total Inpatient Records (Rows)    | 101,766            | 101,766            |
| Total Dimensional Attributes      | 50                 | 84                 |
| Unique Patients Tracked           | 71,518             | 71,518             |
| Encounters per Patient Ratio      | 1.423                | 1.423                |
| Primary Key Duplication Count     | 0                  | 0                  |
| Overall Cell Completeness         | ~94.1% (with '?')  | 96.73%              |
+-----------------------------------+--------------------+--------------------+
```

---

## 3. Operational Headline KPIs (Mathematically Validated)

* **Total Admissions:** `101,766` distinct patient encounters.
* **Total Discharges:** `101,766` completed inpatient stays.
* **Average Length of Stay (ALOS):** `4.4 days` (Standard deviation: 2.99 days).
* **Median Length of Stay:** `4.0 days` (IQR: 2 to 6 days; right-skewed acute distribution).
* **Total Patient-Days (Workload Proxy):** `447,362 patient-days`.
* **CMS 30-Day Readmission Rate:** `11.34%` (Surviving eligible cohort: 100,114 encounters).
* **Unadjusted 30-Day Readmission Rate:** `11.16%` (Over all 101,766 encounters).
* **In-Hospital Mortality Count:** `1,652 patient stays` (1.62% mortality rate).
* **Total Standardized Departments:** `15 clinical departments`.

---

## 4. Missing Value Treatment Audit

In accordance with healthcare data ethics and Section 6 rules, **zero clinical measurements were synthetically imputed**:
1. **`medical_specialty` (49,949 records):** Mapped to categorized department `"General Inpatient / Unspecified"`. Explicit indicator flag `is_specialty_unspecified` added.
2. **`race` (2,273 records):** Categorized transparently as `"Unknown / Not Reported"`. Indicator flag `is_race_unreported` added.
3. **`gender` (3 records):** Replaced `"Unknown/Invalid"` with `"Not Specified"`.
4. **`payer_code` (40,256 records):** Preserved and labeled `"Not Disclosed"`.
5. **`weight` (98,569 records):** 96.86% missingness charted. Preserved with explicit indicator flag `has_recorded_weight`.
6. **`diag_1`, `diag_2`, `diag_3` (21 records):** Labeled `"000.0"` (`"Uncoded"`).

---

## 5. Statistical Outlier Audit (Tukey IQR, k=1.5)

Zero acute care records were deleted. Clinical outliers represent genuine acute complexity:
* **Length of Stay (`time_in_hospital`):** Q1=2.0, Q3=6.0, IQR=4.0. Upper threshold=12.0 days. Outliers: **2,252 encounters (2.21%)** with stays of 13–14 days. Flagged with `is_time_in_hospital_outlier`.
* **Lab Procedures (`num_lab_procedures`):** Q1=31.0, Q3=57.0. Outliers: **143 encounters**. Flagged with `is_num_lab_procedures_outlier`.
* **Medications Administered (`num_medications`):** Q1=10.0, Q3=20.0. Outliers: **2,557 encounters**. Flagged with `is_num_medications_outlier`.

---

## 6. Output Artifacts Produced

1. `data/processed/hospital_cleaned.csv` (101,766 rows, 84 columns)
2. `data/processed/hospital_final_dataset.xlsx` (Multi-tab production Excel workbook)
3. `data/processed/Aegis_Hospital_Extract.hyper` (Native Tableau Hyper binary extract)
4. `data/processed/synthetic_hospital_capacity.csv` (Illustrative capacity telemetry for D4, Section 3 compliant)
5. `reports/data_quality/data_quality_report.json` (Machine-readable audit record)
