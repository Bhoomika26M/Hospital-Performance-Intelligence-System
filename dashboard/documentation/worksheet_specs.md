# Aegis.dv – Tableau Worksheet Technical Specifications Repository

**Document ID:** AD-WS-001  
**Project:** Aegis.dv – Hospital Operations & Patient Analytics Dashboard  
**Author:** Ananya Biju (Infosys Springboard Internship)  
**Standard:** Production Reusable Worksheet Specifications  

---

## Overview & Worksheet Inventory

```
+----+--------------------------------+--------------------------+-----------------------+------------------------+
| #  | Worksheet Name                 | Dashboard                | Chart Type            | Data Source            |
+----+--------------------------------+--------------------------+-----------------------+------------------------+
| 01 | D1_KPI_Admissions              | 1. Hospital Overview     | KPI Scorecard Card    | Hospital_Encounters    |
| 02 | D1_KPI_Discharges              | 1. Hospital Overview     | KPI Scorecard Card    | Hospital_Encounters    |
| 03 | D1_KPI_ALOS                    | 1. Hospital Overview     | KPI Scorecard Card    | Hospital_Encounters    |
| 04 | D1_KPI_Readmission             | 1. Hospital Overview     | KPI Scorecard Card    | Hospital_Encounters    |
| 05 | D1_KPI_PatientDays             | 1. Hospital Overview     | KPI Scorecard Card    | Hospital_Encounters    |
| 06 | D1_Trend_Adm_vs_Disch          | 1. Hospital Overview     | Dual-Line Time Series | Hospital_Encounters    |
| 07 | D1_Bar_Dept_Volume             | 1. Hospital Overview     | Horizontal Bar Chart  | Hospital_Encounters    |
| 08 | D1_Donut_Readmission_Breakdown | 1. Hospital Overview     | Donut / Pie Chart     | Hospital_Encounters    |
| 09 | D1_Bar_Age_Distribution        | 1. Hospital Overview     | Stacked Bar Chart     | Hospital_Encounters    |
| 10 | D2_Trend_Volume_Flow           | 2. Patient Flow          | Area / Line Chart     | Hospital_Encounters    |
| 11 | D2_Heatmap_Day_vs_Month        | 2. Patient Flow          | Density Matrix Heatmap| Hospital_Encounters    |
| 12 | D2_Hist_LOS_Distribution       | 2. Patient Flow          | Histogram with Markers| Hospital_Encounters    |
| 13 | D2_Funnel_Care_Pathway         | 2. Patient Flow          | Staged Funnel / Sankey| Hospital_Encounters    |
| 14 | D2_Bar_Admission_Sources       | 2. Patient Flow          | Horizontal Bar Chart  | Hospital_Encounters    |
| 15 | D3_Bar_Dept_ALOS_Rank          | 3. Department Analytics  | Ranked Horizontal Bar | Hospital_Encounters    |
| 16 | D3_Scatter_Volume_Readmit      | 3. Department Analytics  | Scatter Plot (4-Quad) | Hospital_Encounters    |
| 17 | D3_Bar_Clinical_Intensity      | 3. Department Analytics  | Ranked Bar Chart      | Hospital_Encounters    |
| 18 | D3_Matrix_Dept_Performance     | 3. Department Analytics  | Highlight Table Heatmap| Department_Analytics  |
| 19 | D4_Trend_Bed_Occupancy         | 4. Resource Utilization  | Dual-Axis Trend w/Band| Synthetic_Capacity_D4  |
| 20 | D4_Bar_Staffed_vs_Occupied     | 4. Resource Utilization  | Side-by-Side Bar Chart| Synthetic_Capacity_D4  |
| 21 | D4_Scatter_Nurse_Patient_Ratio | 4. Resource Utilization  | Correlation Scatter   | Synthetic_Capacity_D4  |
| 22 | D4_Card_Workload_Proxy         | 4. Resource Utilization  | Status Scorecard      | Hospital_Encounters    |
+----+--------------------------------+--------------------------+-----------------------+------------------------+
```

---

## Detailed Specifications per Worksheet

### 01. `D1_KPI_Admissions`
* **Purpose:** Display total inpatient intake volume.
* **Data Source:** `Hospital_Encounters`
* **Columns Shelf:** Blank
* **Rows Shelf:** Blank
* **Marks Card:** Text
  - Text: `[Total Admissions]` (Font: Bold, 28pt, `#F5F5F5` Dark / `#1E293B` Light)
  - Detail: `[admission_year]`
* **Tooltip:**  
  ```
  Total Inpatient Admissions: <[Total Admissions]>
  Surviving Patient Cohort: <COUNTD([patient_nbr])>
  Reference Timeline: 1999–2008 (Synthetic)
  ```
* **Number Format:** `#,##0` (e.g. `101,766`)
* **Title:** `"TOTAL ADMISSIONS"` (10pt, `#929292`, uppercase tracking)

---

### 03. `D1_KPI_ALOS`
* **Purpose:** Display overall average length of stay in days.
* **Marks Card:** Text
  - Text: `[Average Length of Stay]` (Bold, 28pt, `#5ACB57` Accent Green)
  - Subtext: `"Median: " + STR([Median Length of Stay]) + " d"` (11pt, `#929292`)
* **Tooltip:**  
  ```
  Average Length of Stay: <[Average Length of Stay]> days
  Median LOS: <[Median Length of Stay]> days
  IQR: 2.0 to 6.0 days | P90: 9.0 days
  ```
* **Number Format:** `0.00 "days"`

---

### 04. `D1_KPI_Readmission`
* **Purpose:** Display CMS risk-eligible 30-day readmission rate.
* **Marks Card:** Text
  - Text: `[Readmission Rate 30d (CMS)]` (Bold, 28pt, `#F5F5F5`)
  - Subtext: `"Target: < 12.0%"` (11pt, `#5ACB57`)
* **Tooltip:**  
  ```
  CMS 30-Day Readmission Rate: <[Readmission Rate 30d (CMS)]>%
  Surviving Eligible Discharges: <SUM([is_readmission_eligible])>
  In-Hospital Deaths Excluded: <SUM([is_in_hospital_death])>
  Early Readmissions (<30d): <SUM([readmitted_30d_flag])>
  ```
* **Number Format:** `0.00 "%"`

---

### 06. `D1_Trend_Adm_vs_Disch`
* **Purpose:** Longitudinal comparison of monthly admissions vs discharges.
* **Columns Shelf:** `YEAR([admission_date])`, `MONTH([admission_date])` (Continuous)
* **Rows Shelf:** `Measure Values`
  - Measure 1: `[Total Admissions]`
  - Measure 2: `[Total Discharges]`
* **Marks Card:** Line Chart
  - Color: `Measure Names`
    - `[Total Admissions]`: Vibrant Green (`#5ACB57`)
    - `[Total Discharges]`: Cool Slate Gray (`#818CF8` or `#94A3B8`)
  - Size: 2.5pt stroke
* **Caption / Footnote:** *"Reference timeline (synthetic) spanning 1999–2008 Cerner study period."*

---

### 07. `D1_Bar_Dept_Volume`
* **Purpose:** Patient volume breakdown across hospital clinical departments.
* **Columns Shelf:** `[Total Admissions]` (Continuous)
* **Rows Shelf:** `[department]` (Categorical, sorted descending by `[Total Admissions]`)
* **Marks Card:** Horizontal Bar
  - Color: `[Volume Share %]` gradient (Dark charcoal `#222222` to Vibrant green `#5ACB57`)
  - Label: `[Total Admissions]` + `" (" + STR(ROUND([Department Volume Share], 1)) + "%)"`
* **Sort Order:** Descending by `SUM(Number of Records)`

---

### 11. `D2_Heatmap_Day_vs_Month`
* **Purpose:** Temporal concentration heatmap showing peak admission periods.
* **Columns Shelf:** `[admission_month]` (Discrete 1–12, labeled Jan–Dec)
* **Rows Shelf:** `[admission_day_of_week]` (Mon, Tue, Wed, Thu, Fri, Sat, Sun)
* **Marks Card:** Square / Heatmap
  - Color: `[Total Admissions]` (Sequential dark green palette: `#141414` -> `#1B4D1A` -> `#5ACB57`)
  - Tooltip: Day of Week, Month, Admissions Volume, % of Weekly Total.

---

### 12. `D2_Hist_LOS_Distribution`
* **Purpose:** Histogram showing the skewed distribution of hospital stay duration.
* **Columns Shelf:** `[time_in_hospital]` (Discrete integer days 1 to 14)
* **Rows Shelf:** `[Total Admissions]`
* **Marks Card:** Vertical Bar
  - Color: `[los_band]` (4 distinct accessible palette tones)
  - Reference Lines:
    - Reference Line 1: Mean ALOS (`4.40 days`, dashed line `#5ACB57`)
    - Reference Line 2: Median LOS (`4.00 days`, solid line `#FFFFFF`)
* **Tooltip:** Duration (Days), Volume of Stays, Cumulative Percentage.

---

### 13. `D2_Funnel_Care_Pathway`
* **Purpose:** Visual care pathway transition: Admission Source -> Department -> Discharge Disposition.
* **Structure:** Multi-stage bar/flow diagram mapping patient flow across the three validated dimensions.
* **Stages:**
  1. Intake Stage: Emergency Room (53.1%), Referrals (30.4%), Transfers (12.2%), Other (4.3%)
  2. Inpatient Treatment: 15 Clinical Departments
  3. Discharge Destination: Routine Home (60.4%), Care Facilities (22.8%), Home Health (12.7%), Mortality (1.6%), Other (2.5%).

---

### 15. `D3_Bar_Dept_ALOS_Rank`
* **Purpose:** Ranked comparison of Average Length of Stay across departments.
* **Columns Shelf:** `[Average Length of Stay]`
* **Rows Shelf:** `[department]` (Sorted descending by ALOS)
* **Marks Card:** Horizontal Bar
  - Color: `IF [Average Length of Stay] > 5.0 THEN "Extended (>5d)" ELSE "Standard (<=5d)" END`
  - Reference Line: Hospital Overall ALOS (`4.40 days`)

---

### 16. `D3_Scatter_Volume_Readmit`
* **Purpose:** 4-quadrant strategic portfolio analysis comparing Patient Volume vs 30-Day Readmission Rate.
* **Columns Shelf:** `[Total Admissions]` (X-axis, Logarithmic or Linear)
* **Rows Shelf:** `[Readmission Rate 30d (CMS)]` (Y-axis)
* **Marks Card:** Circle / Shape
  - Detail: `[department]`
  - Size: `[Total Patient-Days]`
  - Color: `[Department Sample Flag]` (`#5ACB57` for Robust, `#EAB308` for Low Sample)
  - Quadrant Lines:
    - Vertical Benchmark: Median Department Admissions
    - Horizontal Benchmark: Overall Readmission Rate (11.34%)

---

### 19. `D4_Trend_Bed_Occupancy`
* **Purpose:** Daily bed occupancy trend against capacity threshold bands.
* **Data Source:** `Synthetic_Capacity_D4` (Mandatory Section 3 label applied)
* **Columns Shelf:** `[date]` (Continuous Day)
* **Rows Shelf:** `[bed_occupancy_rate_pct]`
* **Marks Card:** Line Chart
  - Color: Emerald green `#5ACB57`
  - Reference Band: $75\% - 90\%$ (Optimal Operating Band, Subtle Charcoal/Green tint)
  - Reference Line: $90.0\%$ (Critical Bottleneck Alert threshold, Amber/Red `#EF4444`)
* **Header Disclaimer:** *"Synthetic reference data – not real hospital figures"*

