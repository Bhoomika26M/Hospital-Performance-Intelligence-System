# Aegis.dv – Comprehensive Dashboard Guide

**Project:** Aegis.dv – Hospital Operations & Patient Analytics Dashboard  
**Author:** Ananya Biju (Infosys Springboard Internship)  
**Target Audience:** Hospital Administrators, Service Line Directors, Healthcare BI Analysts  

---

## 1. Executive Summary & Purpose

Aegis.dv is an enterprise healthcare business intelligence solution designed to transform complex electronic health record (EHR) data into actionable operational and clinical insights. It addresses four critical managerial priorities:
1. Executive operational throughput and clinical care continuity.
2. Inpatient admission routing, length of stay dynamics, and discharge placement.
3. Cross-departmental service line performance and fair comparative benchmarking.
4. Physical resource utilization, bed capacity forecasting, and staffing equilibrium.

---

## 2. Walkthrough of the Four Dashboards

### Dashboard 1: Hospital Overview (Executive Summary)
* **Objective:** Give C-suite healthcare leaders an immediate, holistic assessment of facility throughput and quality.
* **Key Visuals:**
  - **Longitudinal Admissions vs Discharges Trend:** Tracks monthly inpatient intake against completed discharges across the 10-year Cerner study window. Identifies whether hospital discharge throughput is keeping pace with admission surges.
  - **Department Volume Breakdown:** Sorted distribution showing the proportion of acute encounters handled across 15 clinical departments.
  - **Readmission Outcome Donut:** Displays the overall breakdown between non-readmitted patients, early 30-day readmissions, and readmissions beyond 30 days.
  - **Age Demographic Distribution:** Inpatient age bracket composition showing elderly utilization patterns.

### Dashboard 2: Patient Flow (Throughput & Care Pathways)
* **Objective:** Map the physical and organizational journey of patients from arrival to post-acute discharge.
* **Key Visuals:**
  - **Care Pathway Transition Funnel:** Visualizes the three-stage transition from admission source (Emergency, Referral, Transfer) through treating clinical department to final discharge disposition (Home, Skilled Nursing Facility, Home Health, Hospice).
  - **Right-Skewed Length of Stay (LOS) Histogram:** Evaluates acute stay duration against hospital benchmarks (Mean: 4.40 days, Median: 4.00 days).
  - **Temporal Admission Heatmap (Day of Week × Month):** Identifies recurrent weekday and seasonal admission spikes to optimize shift scheduling.

### Dashboard 3: Department Analytics (Fair Service Line Comparison)
* **Objective:** Compare clinical departments on throughput, acuity, and readmission outcomes without penalizing high-volume or specialized units.
* **Fair Comparison Protocol:**
  - Enforces minimum sample size parameter (`p_Min_Sample_Size`, default $n \ge 30$) to suppress statistical noise in rare specialties.
  - Analyzes normalized rates rather than raw counts.
* **Key Visuals:**
  - **4-Quadrant Strategic Portfolio (Volume vs Readmission Rate):** Categorizes departments into strategic quadrants based on patient volume and CMS readmission risk.
  - **Ranked Department ALOS:** Compares average stay duration across departments against the 4.40-day hospital benchmark.
  - **Clinical Intensity Index:** Weighted diagnostic, procedural, and pharmacological consumption score highlighting high-acuity surgical and critical care services.

### Dashboard 4: Resource Utilization (Capacity & Infrastructure)
* **Objective:** Monitor inpatient bed utilization, nursing staff allocation, and capacity alert thresholds.
* **Section 3 Policy Compliance:**
  - Prominently displays: *"Synthetic reference data – not real hospital figures"*.
  - Highlights authentic workload delivered: **447,362 delivered patient-days**.
* **Key Visuals:**
  - **Daily Bed Occupancy Rate Trend:** Tracks daily occupancy percentage against the 75%–90% target operating band and the 90% critical bottleneck redline.
  - **Staffed vs Occupied Beds:** Side-by-side unit capacity comparison across 10 inpatient nursing units.
  - **Nurse-to-Patient Staffing Ratio:** Correlation scatter plot auditing nurse staffing adequacy against fluctuating patient census.

---

## 3. Global Filters & Interactivity

* **Date Range / Reporting Period:** Filters all timeline-enabled sheets to analyze specific seasonal or multi-year trends.
* **Department Selector:** Isolates specific clinical service lines across the entire dashboard view.
* **Cross-Sheet Cross-Filtering:** Clicking any department bar automatically filters demographic and readmission breakdowns.
* **Theme Switching:** Persistent toggle in the navigation rail enables instant switching between Dark Enterprise Mode and Light Clinical Mode.

