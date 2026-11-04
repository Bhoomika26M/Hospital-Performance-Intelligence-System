# Aegis.dv – Tableau Dashboard Layout & Container Architecture Specifications

**Document ID:** AD-DS-001  
**Project:** Aegis.dv – Hospital Operations & Patient Analytics Dashboard  
**Author:** Ananya Biju (Infosys Springboard Internship)  
**Canvas Resolution:** Fixed 1600 × 900 pixels (16:9 Enterprise Widescreen)  
**Layout Paradigm:** 100% Structured Tiled Containers (Zero floating overlaps for cross-device stability)  

---

## 1. Unified Master Layout Framework (All 4 Dashboards)

Every dashboard in Aegis.dv shares an identical root layout hierarchy to ensure visual rhythm, consistent user navigation, and predictable accessibility:

```
Root Canvas (Fixed 1600 x 900)
└── Horizontal Master Container (1600 x 900)
    ├── Left Navigation Rail (Fixed Width: 240px x 900px)
    │   ├── Brand Block (Logo, Wordmark, Tagline) [Height: 120px]
    │   ├── Primary Navigation Buttons (D1, D2, D3, D4) [Height: 280px]
    │   ├── Quick Stat / System Health Widget [Height: 200px]
    │   ├── Theme Toggle Button (Dark <-> Light) [Height: 60px]
    │   └── Attribution Footer (Developer & Org Credits) [Height: 160px]
    │
    └── Main Content Canvas (Flexible Width: 1360px x 900px, Padding: 16px)
        └── Vertical Content Container
            ├── Top Header & Global Filter Bar (Height: 70px)
            │   ├── Dashboard Title & Dynamic Subtitle (Left: 60%)
            │   └── Global Controls (Reporting Period, Department Filter, Reset) (Right: 40%)
            │
            ├── KPI Card Scorecard Row (Height: 120px)
            │   └── Horizontal Container (4 or 5 Uniform Cards with 12px Gaps)
            │
            ├── Primary Analytical Visual Zone (Height: 380px)
            │   └── Dominant operational time-series or multi-dimension matrix
            │
            ├── Secondary Analytical Dual-Zone (Height: 260px)
            │   └── Horizontal Container (50% / 50% split for complementary visuals)
            │
            └── Operational Compliance Footer (Height: 30px)
                └── Data Source, Provenance Disclaimer & Licensing Citation
```

---

## 2. Dashboard 1: Hospital Overview (Executive Summary)

* **Target Audience:** Chief Medical Officer (CMO), Chief Operating Officer (COO), Hospital Board.
* **Core Question Answered:** "What is the overall operational pulse, throughput balance, and clinical quality across the enterprise?"
* **KPI Row Cards (5 Cards, 256px width each):**
  1. `D1_KPI_Admissions`: 101,766
  2. `D1_KPI_Discharges`: 101,766
  3. `D1_KPI_ALOS`: 4.40 days (Median: 4.0 d)
  4. `D1_KPI_Readmission`: 11.34% (CMS Risk-Eligible)
  5. `D1_KPI_PatientDays`: 447,362 days (Workload Proxy)
* **Primary Analytical Zone (Height 380px):**
  - Left Container (65% width): `D1_Trend_Adm_vs_Disch` (Longitudinal admissions vs discharges over time).
  - Right Container (35% width): `D1_Donut_Readmission_Breakdown` (Readmission outcomes: No Readmit, >30d, <30d).
* **Secondary Zone (Height 260px):**
  - Left Container (55% width): `D1_Bar_Dept_Volume` (Patient volume by clinical department).
  - Right Container (45% width): `D1_Bar_Age_Distribution` (Inpatient demographic cohort volume).

---

## 3. Dashboard 2: Patient Flow (Intake to Discharge)

* **Target Audience:** Patient Access Directors, Nursing Supervisors, Bed Board Coordinators.
* **Core Question Answered:** "Where do patients originate, what is the acute stay duration profile, and where are discharge bottlenecks occurring?"
* **KPI Row Cards (4 Cards, 320px width each):**
  1. Total Encounters: 101,766
  2. Emergency Intake Share: 53.1%
  3. Routine Home Discharge Share: 60.4%
  4. Extended Stay Cohort (>9 days): 7.2%
* **Primary Analytical Zone (Height 380px):**
  - Full-Width Tiled Container: `D2_Funnel_Care_Pathway` (Integrated intake-to-discharge transition flow).
* **Secondary Zone (Height 260px):**
  - Left Container (50% width): `D2_Hist_LOS_Distribution` (Length of stay histogram with Mean 4.4d and Median 4.0d reference lines).
  - Right Container (50% width): `D2_Heatmap_Day_vs_Month` (Day of week vs month admission volume matrix).

---

## 4. Dashboard 3: Department Analytics (Fair Comparative Benchmarking)

* **Target Audience:** Clinical Department Chairs, Service Line Directors, Operations Analysts.
* **Core Question Answered:** "How do clinical departments compare on throughput, acuity, clinical intensity, and readmission risk, adjusted for volume?"
* **Fair Comparison Safeguard:** Incorporates `[p_Min_Sample_Size]` parameter (default n=30) to suppress or flag low-sample statistical noise.
* **KPI Row Cards (4 Cards):**
  1. Active Clinical Departments: 15
  2. High-Volume Leader: General & Internal Medicine (49.6% volume)
  3. Highest Clinical Intensity: General Surgery (26.4 index)
  4. Enterprise ALOS Benchmark: 4.40 days
* **Primary Analytical Zone (Height 380px):**
  - Left Container (50% width): `D3_Bar_Dept_ALOS_Rank` (Ranked department ALOS vs 4.40d hospital benchmark).
  - Right Container (50% width): `D3_Scatter_Volume_Readmit` (4-quadrant scatter of Volume vs CMS Readmission Rate, sized by Patient-Days).
* **Secondary Zone (Height 260px):**
  - Left Container (50% width): `D3_Bar_Clinical_Intensity` (Ranked weighted clinical procedure/diagnostic intensity index).
  - Right Container (50% width): `D3_Matrix_Dept_Performance` (Cross-metric highlight table: Admissions, ALOS, Readmit %, Workload Days).

---

## 5. Dashboard 4: Resource Utilization (Capacity & Operations)

* **Target Audience:** Hospital Capacity Command Center, Facilities Planning, Staffing Operations.
* **Core Question Answered:** "What is the physical bed occupancy trend, nurse-to-patient staffing ratio, and capacity alert status across units?"
* **Provenance & Ethics Compliance (Section 3):**
  - Prominent Banner at Top: *"Synthetic reference data – not real hospital figures (Section 3 Compliance)"*.
  - Workload proxy card on real data: Total Patient-Days (447,362).
* **KPI Row Cards (4 Cards):**
  1. Total Staffed Inpatient Beds: 650 beds (Synthetic)
  2. Average Bed Occupancy Rate: 78.4% (Target: 75%–90%)
  3. Average Nurse-to-Patient Ratio: 1:3.4
  4. Real Clinical Workload Delivered: 447,362 Patient-Days (Authentic Data)
* **Primary Analytical Zone (Height 380px):**
  - `D4_Trend_Bed_Occupancy`: Daily occupancy line against the 75%–90% normal operating band and 90% critical bottleneck threshold.
* **Secondary Zone (Height 260px):**
  - Left Container (50% width): `D4_Bar_Staffed_vs_Occupied` (Unit-by-unit licensed vs occupied beds).
  - Right Container (50% width): `D4_Scatter_Nurse_Patient_Ratio` (Daily nurse staffing level vs inpatient census).

---

## 6. Color Themes & Accessibility Specification

```
+---------------------------+-----------------------+-----------------------+----------------------+
| Element                   | Dark Theme (Default)  | Light Theme Counter   | WCAG Contrast Ratio  |
+---------------------------+-----------------------+-----------------------+----------------------+
| Master Canvas Background  | #080808               | #F8F9FA               | N/A (Canvas Root)    |
| Navigation Rail Sidebar   | #1E1E1E               | #F1F5F9               | N/A (Container)      |
| Card / Container Surface  | #141414               | #FFFFFF               | N/A (Card Surface)   |
| Primary Text (Headings)   | #F5F5F5               | #0F172A               | 16.2:1 (Passes AAA)  |
| Secondary Text (Labels)   | #929292               | #64748B               | 4.8:1 (Passes AA)    |
| Accent Primary (Hospital) | #5ACB57 (Neon Green)  | #2E7D32 (Forest Green)| 5.1:1 (Passes AA)    |
| Accent Secondary (Alert)  | #EF4444 (Crimson)     | #DC2626 (Ruby Red)    | 4.6:1 (Passes AA)    |
| Accent Warning (Caution)  | #F59E0B (Amber Gold)  | #D97706 (Tuscan Gold) | 4.5:1 (Passes AA)    |
| Subtle Borders            | #303030               | #E2E8F0               | Structural outline   |
+---------------------------+-----------------------+-----------------------+----------------------+
```

