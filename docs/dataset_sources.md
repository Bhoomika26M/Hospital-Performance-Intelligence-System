# Aegis.dv – Comprehensive Dataset Sources & Comparative Evaluation

**Project:** Aegis.dv – Hospital Operations & Patient Analytics Dashboard  
**Author:** Ananya Biju (Infosys Springboard Internship)  
**Date Evaluated:** November 4, 2026  
**Standards Adhered:** HIPAA Safe Harbor De-identification, Open Science Reproducibility, Section 3 Evaluation Protocol  

---

## 1. Candidate Dataset Comparative Registry (6 Candidates)

The following six publicly referenced healthcare and hospital operations datasets were systematically audited to determine analytical viability, data reliability, licensing compliance, and alignment with Aegis.dv operational dashboards.

```
+------------------------------------------------------------------------------------------------------------------------------------+
| # | Dataset Name                      | Source / Publisher       | Source URL / Repository Identifier                             |
+---+-----------------------------------+--------------------------+----------------------------------------------------------------+
| 1 | Diabetes 130-US Hospitals         | UCI Machine Learning     | https://archive.ics.uci.edu/dataset/296/diabetes+130-us+       |
|   | (1999–2008) (Selected Primary)    | Repository / Cerner      | hospitals+for+years+1999-2008                                  |
+---+-----------------------------------+--------------------------+----------------------------------------------------------------+
| 2 | COVID-19 Facility Capacity        | HealthData.gov / U.S.    | https://healthdata.gov/Hospital/COVID-19-Reported-Patient-     |
|   | & Utilization                     | HHS / CDC NHSN           | Impact-and-Hospital-Capa/anag-cw7u                             |
+---+-----------------------------------+--------------------------+----------------------------------------------------------------+
| 3 | NYS SPARCS Hospital Inpatient     | New York State DOH /     | https://health.data.ny.gov/Health/Hospital-Inpatient-          |
|   | Discharges (De-Identified)        | Health Data NY           | Discharges-SPARCS-De-Identified/22g3-z7e7                      |
+---+-----------------------------------+--------------------------+----------------------------------------------------------------+
| 4 | MIMIC-IV Clinical Database Demo   | PhysioNet / MIT LCP /    | https://physionet.org/content/mimic-iv-demo/2.2/               |
|   | (v2.2 Open Subset)                | Beth Israel Deaconess    |                                                                |
+---+-----------------------------------+--------------------------+----------------------------------------------------------------+
| 5 | NHS England KH03 Bed Availability | NHS England / UK         | https://www.england.nhs.uk/statistics/statistical-work-areas/  |
|   | & Occupancy                       | Government Statistics    | bed-availability-and-occupancy/bed-availability-and-occupancy- |
|   |                                   |                          | kh03/                                                          |
+---+-----------------------------------+--------------------------+----------------------------------------------------------------+
| 6 | Kaggle Healthcare Dataset         | Kaggle / Prasad Patil    | https://www.kaggle.com/datasets/prasad22/healthcare-dataset    |
|   | (prasad22)                        | (Community Upload)       |                                                                |
+------------------------------------------------------------------------------------------------------------------------------------+
```

---

### Candidate 1: Diabetes 130-US Hospitals (1999–2008) – **SELECTED PRIMARY**
* **Publisher:** UCI Machine Learning Repository (Donated by Strack et al., Cerner Health Facts)
* **Verified URL:** `https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip`
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
* **Record Count:** 101,766 inpatient encounters across 71,518 unique patients
* **Dimensions:** 50 attributes
* **Time Coverage:** 10-year clinical horizon (1999–2008)
* **Geography:** United States (130 integrated hospital delivery networks)
* **Granularity:** Inpatient encounter-level
* **Key Columns:** `encounter_id`, `patient_nbr`, `race`, `gender`, `age`, `admission_type_id`, `discharge_disposition_id`, `admission_source_id`, `time_in_hospital`, `medical_specialty`, `num_lab_procedures`, `num_procedures`, `num_medications`, `number_diagnoses`, `diag_1`, `diag_2`, `diag_3`, `readmitted` (`<30`, `>30`, `NO`).
* **Dashboard Fit:** Primary data engine for **Hospital Overview (D1)**, **Patient Flow (D2)**, and **Department Analytics (D3)**.
* **Limitations:** Calendar dates and physical bed inventory counts omitted at source to protect hospital identity.

---

### Candidate 2: COVID-19 Facility Capacity & Utilization
* **Publisher:** U.S. Department of Health & Human Services (HHS) / HealthData.gov
* **URL:** `https://healthdata.gov/Hospital/COVID-19-Reported-Patient-Impact-and-Hospital-Capa/anag-cw7u`
* **License:** U.S. Public Domain / Open Government Data
* **Record Count:** ~3.4 million facility-week records
* **Time Coverage:** 2020–2024 (Mandate discontinued May 3, 2024)
* **Geography:** United States (all Medicare/Medicaid registered facilities)
* **Granularity:** Facility-week aggregation
* **Key Columns:** `hospital_pk`, `collection_week`, `total_beds_7_day_avg`, `inpatient_beds_used_7_day_avg`, `staffed_icu_adult_bed_occupancy`.
* **Evaluation & Decision:** Incompatible with Candidate 1. Highly aggregate pandemic-specific bed census without encounter-level patient demographics, medical specialties, or readmission linkages. Joining them would violate Section 3's prohibition against joining mismatched granularities.

---

### Candidate 3: NYS SPARCS Hospital Inpatient Discharges
* **Publisher:** New York State Department of Health (NYSDOH)
* **URL:** `https://health.data.ny.gov/Health/Hospital-Inpatient-Discharges-SPARCS-De-Identified/22g3-z7e7`
* **License:** New York State Open Data Terms of Use
* **Record Count:** 2.3+ million annual discharge records
* **Time Coverage:** Annual files (2010–2022)
* **Geography:** New York State, USA
* **Granularity:** Discharge-level
* **Evaluation & Decision:** Evaluated as strong secondary, but files are multi-gigabyte monolithic dumps with suppressed exact day/month values for HIPAA Safe Harbor, and no pre-computed multi-hospital readmission cohort linkage without complex fuzzy matching.

---

### Candidate 4: MIMIC-IV Clinical Database Demo (v2.2)
* **Publisher:** PhysioNet / MIT Laboratory for Computational Physiology
* **URL:** `https://physionet.org/content/mimic-iv-demo/2.2/`
* **License:** Open Access Demo / PhysioNet Credentialed Data Use Agreement for full database
* **Record Count:** 100 patient demo subset (full database: 299,712 patients)
* **Time Coverage:** 2008–2019
* **Geography:** Single academic medical center (BIDMC, Boston, MA)
* **Granularity:** Highly granular EHR (ICU stays, lab events, chart events)
* **Evaluation & Decision:** The open demo is limited to only 100 patients (insufficient for multi-department enterprise BI analysis), while the full database requires credentialed CITI human-research certification and individual DUA approval, preventing public open redistribution.

---

### Candidate 5: NHS England KH03 Bed Availability & Occupancy
* **Publisher:** NHS England Statistics
* **URL:** `https://www.england.nhs.uk/statistics/statistical-work-areas/bed-availability-and-occupancy/bed-availability-and-occupancy-kh03/`
* **License:** UK Open Government Licence (OGL v3.0)
* **Record Count:** Quarterly provider-level summaries
* **Time Coverage:** 2010–2025
* **Geography:** England, United Kingdom
* **Granularity:** Hospital Trust / Sector quarterly aggregate
* **Evaluation & Decision:** Pure aggregate macro tables (available bed-days vs. occupied bed-days by broad medical sector). Lacks individual patient encounters, length of stay distributions, and readmission outcomes.

---

### Candidate 6: Kaggle Healthcare Dataset (prasad22)
* **Publisher:** Kaggle (Uploaded by community user Prasad Patil)
* **URL:** `https://www.kaggle.com/datasets/prasad22/healthcare-dataset`
* **License:** CC0 Public Domain
* **Record Count:** 55,500 synthetic rows
* **Time Coverage:** 2019–2024 (random dates)
* **Geography:** Fictional / Randomized
* **Granularity:** Single row per patient
* **Evaluation & Decision:** Entirely synthetic mock data created with random generators (uniform age distributions, arbitrary hospital billing numbers). Lacks genuine clinical realism, real clinical length of stay distributions, and true readmission dynamics. Disqualified as primary per Section 3 rules.

---

## 2. Selection Rationale & Ethics Compliance

1. **Primary Dataset Selected:** UCI Diabetes 130-US Hospitals (1999–2008) is the sole authentic clinical encounter dataset with large-scale multi-hospital operations data (101,766 records), genuine length of stay, real clinical departments, and validated 30-day readmissions.
2. **Ethics & Privacy:** Meets all HIPAA Safe Harbor requirements (§164.514(b)(2)). All direct identifiers (names, SSNs, MRNs, phone numbers) are stripped.
3. **No Unsound Joins:** No arbitrary cross-dataset joins are performed that would compromise epidemiological or operational validity.

