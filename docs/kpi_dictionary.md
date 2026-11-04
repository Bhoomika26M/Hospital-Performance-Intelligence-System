# Aegis.dv – Comprehensive Healthcare KPI & Metrics Dictionary

**Standard:** CMS Hospital-Wide All-Cause Readmission (HWR), National Quality Forum (NQF), Agency for Healthcare Research and Quality (AHRQ).  
**Author:** Ananya Biju (Infosys Springboard Internship)  
**Project:** Aegis.dv – Hospital Operations & Patient Analytics Dashboard  
**Version:** 1.0 (Production Release)  

---

## Metric 1: Total Inpatient Admissions

* **Metric Name:** Total Admissions
* **Category:** Hospital Operations / Inpatient Census Volume
* **Dashboards Featured:** Hospital Overview (D1), Patient Flow (D2), Department Analytics (D3)
* **Formal Definition:** The absolute count of distinct valid patient admissions initiated within the specified reporting period.
* **Mathematical Formula:**  
  $$\text{Total Admissions} = \text{COUNT\_DISTINCT}(\text{encounter\_id})$$
* **Required Columns:** `encounter_id`, `admission_date`
* **Calculation Methodology:** Counts unique encounter identifiers. In datasets where multiple records may represent procedural sub-charges for a single stay, this measure strictly deduplicates by `encounter_id` to prevent double-counting.
* **Edge-Case Handling:** Empty dataset returns 0. Null `encounter_id` rows are rejected during schema validation.
* **Clinical Interpretation:** Core volume indicator of acute inpatient service demand. Used as the denominator for admission growth, emergency intake share, and department volume distributions.
* **Limitations:** Does not reflect outpatient clinic visits or observations stays under 24 hours without inpatient admission.

---

## Metric 2: Total Inpatient Discharges

* **Metric Name:** Total Discharges
* **Category:** Hospital Operations / Throughput
* **Dashboards Featured:** Hospital Overview (D1), Patient Flow (D2), Department Analytics (D3)
* **Formal Definition:** The absolute count of completed inpatient stays where the patient departed the acute hospital setting.
* **Mathematical Formula:**  
  $$\text{Total Discharges} = \text{COUNT\_DISTINCT}(\text{encounter\_id}) \quad \text{where stay is terminated}$$
* **Required Columns:** `encounter_id`, `discharge_disposition_id`, `discharge_date`
* **Calculation Methodology:** In the Cerner inpatient database, every encounter represents a completed discharge with an assigned `discharge_disposition_id`.
* **Edge-Case Handling:** Stays without discharge dispositions are audited separately; never imputed.
* **Clinical Interpretation:** Primary throughput measure. Balanced against admissions to assess inpatient flow equilibrium.

---

## Metric 3: Average Length of Stay (ALOS)

* **Metric Name:** Average Length of Stay (ALOS)
* **Category:** Efficiency & Bed Utilization
* **Dashboards Featured:** Hospital Overview (D1), Patient Flow (D2), Department Analytics (D3)
* **Formal Definition:** The arithmetic mean duration of hospital stays (in elapsed days) across all discharged inpatient encounters in the reporting window.
* **Mathematical Formula:**  
  $$\text{ALOS} = \frac{\sum_{i=1}^{N} \text{time\_in\_hospital}_i}{N}$$
  Where $N = \text{Total Discharged Encounters with valid } \text{time\_in\_hospital} > 0$.
* **Required Columns:** `time_in_hospital`, `encounter_id`
* **Calculation Methodology:** Computed across all completed inpatient stays. Direct duration `time_in_hospital` (integer days, range 1–14) is validated against admission and discharge timestamps.
* **Edge-Case Handling:** If $N = 0$, returns `null` (rendered in Tableau as `"–"`). Same-day stays are evaluated consistently. Stays exceeding 365 days are flagged as invalid outliers.
* **Clinical Interpretation:** Primary benchmark of clinical throughput and inpatient resource efficiency. High ALOS may indicate discharge bottlenecks, social placement delays, or high clinical acuity.
* **Limitations:** Right-skewed by high-acuity outliers, necessitating complementary median and percentile reporting.

---

## Metric 4: Median Length of Stay & Percentiles (P75, P90)

* **Metric Name:** Median LOS, P75, P90
* **Category:** Operational Distribution & Outlier Profiling
* **Dashboards Featured:** Patient Flow (D2), Department Analytics (D3)
* **Formal Definition:** The 50th, 75th, and 90th percentiles of inpatient length of stay distribution.
* **Mathematical Formula:**  
  $$\text{Median LOS} = \text{PERCENTILE}(\text{time\_in\_hospital}, 0.50)$$  
  $$\text{P75 LOS} = \text{PERCENTILE}(\text{time\_in\_hospital}, 0.75), \quad \text{P90 LOS} = \text{PERCENTILE}(\text{time\_in\_hospital}, 0.90)$$
* **Required Columns:** `time_in_hospital`
* **Calculation Methodology:** Non-parametric order statistics. Evaluated on sorted non-null durations.
* **Edge-Case Handling:** Returns `null` if dataset is empty.
* **Clinical Interpretation:** Median provides the truest measure of central tendency for acute stays (typical experience of the average patient). P75 and P90 capture the resource burden of the acute "long-stay" tail.

---

## Metric 5: 30-Day Hospital Readmission Rate (CMS / NQF Standard)

* **Metric Name:** 30-Day Readmission Rate (Risk-Eligible)
* **Category:** Clinical Quality & Care Continuity
* **Dashboards Featured:** Hospital Overview (D1), Department Analytics (D3)
* **Formal Definition:** The percentage of eligible index inpatient discharges that resulted in an unplanned acute readmission to any participating hospital within 30 days of discharge.
* **Mathematical Formula:**  
  $$\text{Readmission Rate}_{30\text{d}} = \frac{\sum \text{readmitted\_30d\_flag}}{\sum \text{is\_readmission\_eligible}} \times 100$$
  Where:
  - $\text{readmitted\_30d\_flag} = 1$ if `readmitted == '<30'`, else $0$.
  - $\text{is\_readmission\_eligible} = 1$ if `discharge_disposition_id` $\notin \{11, 19, 20, 21\}$ (survived index stay).
* **Required Columns:** `readmitted`, `discharge_disposition_id`, `encounter_id`
* **Calculation Methodology:**  
  1. Identifies index discharges surviving inpatient care ($N = 100,114$).
  2. Excludes $1,652$ in-hospital mortality events (discharge dispositions 11, 19, 20, 21: Expired).
  3. Divides early readmissions ($11,357$) by eligible survivors.
  4. Result: **11.34%** (compared to unadjusted rate of 11.16%).
* **Edge-Case Handling:** Returns `null` if eligible denominator is zero. Does not claim re-computation from dates when pre-computed outcome flags are provided by the Cerner warehouse.
* **Clinical Interpretation:** Core quality and patient safety indicator under the CMS Hospital Readmissions Reduction Program (HRRP). High rates indicate premature discharge, medication reconciliation breakdowns, or insufficient outpatient coordination.

---

## Metric 6: Total Patient-Days (Workload Proxy)

* **Metric Name:** Total Patient-Days
* **Category:** Inpatient Workload & Bed Consumption Proxy
* **Dashboards Featured:** Hospital Overview (D1), Department Analytics (D3), Resource Utilization (D4)
* **Formal Definition:** Aggregate days of acute care delivered across all active inpatient beds in the reporting window.
* **Mathematical Formula:**  
  $$\text{Total Patient-Days} = \sum_{i=1}^{N} \text{time\_in\_hospital}_i$$
* **Required Columns:** `time_in_hospital`, `encounter_id`
* **Calculation Methodology:** Sum of stay lengths for all admissions.
* **Context & Section 3 Compliance:** In the absence of physical hospital bed inventory telemetry, Total Patient-Days serves as the authentic, un-fabricated clinical workload proxy. It is explicitly labeled as a workload proxy and never misrepresented as percentage bed occupancy.
* **Clinical Interpretation:** Key driver of nursing care hours, linen, pharmaceuticals, and facility operational costs.

---

## Metric 7: Emergency Admission Share

* **Metric Name:** Emergency Admission Rate
* **Category:** Intake Acuity & Patient Flow
* **Dashboards Featured:** Patient Flow (D2), Department Analytics (D3)
* **Formal Definition:** Percentage of total admissions entering unscheduled through the Emergency Department or Trauma Center.
* **Mathematical Formula:**  
  $$\text{Emergency Rate} = \frac{\text{COUNT}(\text{admission\_type\_id} \in \{1, 7\})}{\text{Total Admissions}} \times 100$$
* **Required Columns:** `admission_type_id`, `encounter_id`
* **Clinical Interpretation:** Reflects hospital dependency on unscheduled urgent care vs. planned elective procedures. High emergency share complicates bed forecasting and staffing schedules.

---

## Metric 8: Clinical Intensity Index

* **Metric Name:** Clinical Intensity Index (Weighted Workload Score)
* **Category:** Operational Resource Demand & Patient Complexity
* **Dashboards Featured:** Department Analytics (D3), Resource Utilization (D4)
* **Formal Definition:** A standardized composite index reflecting the diagnostic, procedural, and pharmacological consumption per encounter.
* **Mathematical Formula:**  
  $$\text{Intensity Index} = (0.15 \times \text{num\_lab}) + (1.20 \times \text{num\_proc}) + (0.40 \times \text{num\_med}) + (0.60 \times \text{num\_diag})$$
* **Weights Justification:**
  - Procedures ($1.20$): Highly resource-intensive (operating room, surgeon, specialized nursing).
  - Diagnoses ($0.60$): Multimorbidity requires multi-specialist coordination.
  - Medications ($0.40$): High pharmacy and nursing administration burden.
  - Lab Procedures ($0.15$): Automated high-throughput clinical laboratory testing.
* **Limitations:** Operational workload heuristic; not a formal DRG Case Mix Index (CMI). Published with full transparency per Section 4 rules.

---

## Metric 9: Bed Occupancy Rate (Synthetic Reference Telemetry)

* **Metric Name:** Bed Occupancy Rate (Synthetic Reference)
* **Category:** Capacity Utilization (Dashboard 4 Only)
* **Dashboards Featured:** Resource Utilization (D4)
* **Formal Definition:** Percentage of available staffed beds occupied by inpatients.
* **Mathematical Formula:**  
  $$\text{Occupancy Rate} = \frac{\text{Occupied Bed-Days}}{\text{Available Staffed Bed-Days}} \times 100$$
* **Data Source & Label:** `synthetic_hospital_capacity.csv`. **Mandatory Label:** `"Synthetic reference data – not real hospital figures"`.
* **Threshold Bands:**
  - Normal Operating Range: $75\% - 90\%$
  - Critical Bottleneck: $\ge 90\%$ (Risk of emergency department boarding)
  - Underutilized: $< 75\%$

