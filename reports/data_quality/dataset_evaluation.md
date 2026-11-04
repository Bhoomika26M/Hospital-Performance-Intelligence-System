# Aegis.dv – Dataset Capability Matrix & Evaluation Report

**Document ID:** AD-DQR-001  
**Project:** Aegis.dv – Hospital Operations & Patient Analytics Dashboard  
**Author:** Ananya Biju (Infosys Springboard Internship)  
**Standard:** Section 3 Capability Evaluation Protocol  

---

## 1. Capability Matrix (KPIs & Visualizations vs. Candidate Datasets)

**Rating Legend:**
* **Supported (S):** Genuinely present at individual encounter/operational granularity.
* **Partially Supported (P):** Present with domain limitations (e.g., proxy measure, duration without calendar dates, or grouped categories).
* **Not Supported (N):** Metric/variable entirely absent from the dataset.

```
+---------------------------------------------+-------------+-------------+-------------+-------------+-------------+-------------+
| KPI / Visualization Requirement             | Candidate 1 | Candidate 2 | Candidate 3 | Candidate 4 | Candidate 5 | Candidate 6 |
| (Sections 4 & 5)                            | UCI 130-US  | HHS COVID   | NYS SPARCS  | MIMIC-IV D  | NHS KH03    | Kaggle P22  |
+---------------------------------------------+-------------+-------------+-------------+-------------+-------------+-------------+
| Total Admissions (Distinct Encounters)      | S [1]       | P [2]       | S [3]       | P [4]       | N           | S [5]       |
| Total Discharges                            | S [6]       | P [7]       | S [8]       | P [9]       | N           | S [10]      |
| Average Length of Stay (ALOS)               | S [11]      | N           | S [12]      | S [13]      | P [14]      | S [15]      |
| Median LOS, P75, P90 Percentiles            | S [16]      | N           | S [17]      | S [18]      | N           | S [19]      |
| 30-Day Readmission Rate                     | S [20]      | N           | P [21]      | P [22]      | N           | N           |
| In-Hospital Mortality Exclusion             | S [23]      | N           | S [24]      | S [25]      | N           | N           |
| Department / Specialty Patient Distribution | S [26]      | N           | S [27]      | S [28]      | P [29]      | N           |
| Department ALOS Comparisons                 | S [30]      | N           | S [31]      | S [32]      | P [33]      | N           |
| Admission Source Distribution               | S [34]      | N           | S [35]      | S [36]      | N           | N           |
| Discharge Disposition Distribution          | S [37]      | N           | S [38]      | S [39]      | N           | N           |
| Emergency vs Elective Admissions            | S [40]      | N           | S [41]      | S [42]      | N           | N           |
| Patient Flow / Care Pathway Funnel          | S [43]      | N           | S [44]      | S [45]      | N           | N           |
| Age & Gender Demographic Profiling          | S [46]      | N           | S [47]      | S [48]      | N           | S [49]      |
| Clinical Complexity / Lab & Med Workload    | S [50]      | N           | P [51]      | S [52]      | N           | N           |
| Calendar Date Trends (MoM / YoY Time Series)| P [53]      | S [54]      | P [55]      | S [56]      | P [57]      | S [58]      |
| Physical Bed Inventory / Occupancy Rate     | N [59]      | S [60]      | N           | N           | S [61]      | N           |
| Staffing Counts / Nurse-to-Patient Ratios   | N [62]      | P [63]      | N           | N           | N           | N           |
| Equipment Utilization (Telemetry/Scanners)  | N [64]      | N           | N           | P [65]      | N           | N           |
+---------------------------------------------+-------------+-------------+-------------+-------------+-------------+-------------+
```

### Specific Justifying Columns / Evidence:
* `[1]`: `encounter_id` (101,766 distinct encounter rows)
* `[2]`: Aggregate facility-week admissions only; no patient-level encounter records.
* `[3]`: Discharge records represent individual institutional encounters.
* `[4]`: Only 100 patient encounters in public uncredentialed demo.
* `[5]`: Synthetic row counter.
* `[6]`: `discharge_disposition_id` records completion of stay across all encounters.
* `[7]`: Derived from weekly facility discharge aggregates.
* `[8]`: Record is by definition a discharge.
* `[9]`: Demographic demo discharges only (N=100).
* `[10]`: Synthetic discharge date field.
* `[11]`: `time_in_hospital` (integer days, range 1–14).
* `[12]`: `length_of_stay` in integer days.
* `[13]`: `los` in decimal days from ICU/hospital in/out timestamps.
* `[14]`: Aggregate bed-days divided by admissions.
* `[15]`: Difference between synthetic admission and discharge dates.
* `[16]`: Directly computable from `time_in_hospital` distribution.
* `[17]`: Computable from SPARCS length of stay field.
* `[18]`: Computable from MIMIC demo stay timestamps.
* `[19]`: Computable from synthetic dates.
* `[20]`: `readmitted` attribute with distinct categories: `<30` (early readmit), `>30`, and `NO`.
* `[21]`: SPARCS requires complex multi-file patient linkage; suppressed in public files.
* `[22]`: MIMIC demo has too small an N (100) to yield statistically valid 30-day rates.
* `[23]`: `discharge_disposition_id` in {11, 19, 20, 21} ("Expired" / in-hospital mortality).
* `[24]`: Discharge disposition "Expired".
* `[25]`: Hospital expire flag (`hospital_expire_flag`).
* `[26]`: `medical_specialty` (72 clinical specialties grouped into core departments).
* `[27]`: APR-DRG Major Diagnostic Category (MDC).
* `[28]`: Care unit / service provider codes.
* `[29]`: High-level sector only (General & Acute, Maternity, Mental Health).
* `[30]`: `time_in_hospital` grouped by `medical_specialty`.
* `[31]`: Length of stay grouped by MDC.
* `[32]`: LOS grouped by Care Unit.
* `[33]`: Quarterly sector averages.
* `[34]`: `admission_source_id` (25 clinical referral sources via `IDs_mapping.csv`).
* `[35]`: Admitting source category codes.
* `[36]`: Admission location in transfers.
* `[37]`: `discharge_disposition_id` (30 clinical discharge destinations via `IDs_mapping.csv`).
* `[38]`: Discharge disposition codes.
* `[39]`: Discharge location.
* `[40]`: `admission_type_id` (Emergency [1], Urgent [2], Elective [3], Trauma [7]).
* `[41]`: Type of admission (Emergency, Urgent, Elective, Newborn).
* `[42]`: Admission type.
* `[43]`: Supported sequence: `admission_source_id` -> `medical_specialty` -> `discharge_disposition_id`.
* `[44]`: Supported sequence: Source -> MDC -> Disposition.
* `[45]`: Supported: ED -> ICU -> Floor -> Discharge.
* `[46]`: `age` (10-year age cohorts `[0-10)` to `[90-100)`), `gender`, `race`.
* `[47]`: Age group, gender, race/ethnicity.
* `[48]`: Age, gender.
* `[49]`: Synthetic age and gender columns.
* `[50]`: `num_lab_procedures` (1–132), `num_procedures` (0–6), `num_medications` (1–81), `number_diagnoses` (1–16).
* `[51]`: Diagnosis and procedure counts.
* `[52]`: Lab events and pharmacy events.
* `[53]`: Time horizon is known 10-year span (1999–2008), but exact Gregorian dates are omitted at source. Per Section 3, timeline is modeled as "Reference timeline (synthetic)".
* `[54]`: Weekly calendar dates present (2020–2024).
* `[55]`: Year is present, but specific day and month are masked.
* `[56]`: Full timestamps present (shifted).
* `[57]`: Quarterly dates present.
* `[58]`: Completely synthetic dates (uniform random distribution).
* `[59]`: No physical bed inventory in Cerner outpatient/inpatient extract. Section 3 Missing Capability Policy invoked.
* `[60]`: Aggregate staffed and licensed bed counts present.
* `[61]`: Available bed-days per quarter present.
* `[62]`: No physician/nurse headcount in clinical billing extract. Section 3 policy invoked.
* `[63]`: Critical staffing shortage binary flags only.
* `[64]`: No scanner/OR telemetry.
* `[65]`: Ventilator and ICU equipment usage timestamps present.

---

## 2. Definitive Architecture & Strategy Decision

Based on the capability matrix:
1. **Candidate 1 (UCI 130-US Hospitals)** is selected as the primary analytical engine. It supports 14 of the 18 core operational requirements with 100% genuine clinical encounter data.
2. **Missing Variables Protocol (Section 3):**
   - **Bed Occupancy & Staffing:** Real data does not contain physical bed counts or nurse rosters. Aegis.dv computes and presents **Total Patient-Days** as the authentic workload proxy on primary views, marks physical bed occupancy as **"Unavailable – requires bed capacity data"**, and provides a clearly isolated, labeled synthetic module (`synthetic_hospital_capacity.csv`) for the Resource Utilization dashboard with visible on-dashboard disclaimers.
   - **Calendar Timeline:** Sequence and duration cohorts are preserved; timeline trends are labeled **"Reference timeline (synthetic)"** per Section 3 policy.

