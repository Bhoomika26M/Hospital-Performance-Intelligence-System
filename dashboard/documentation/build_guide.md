# Aegis.dv – Step-by-Step Tableau Workbook Build & Assembly Guide

**Document ID:** AD-BG-001  
**Project:** Aegis.dv – Hospital Operations & Patient Analytics Dashboard  
**Author:** Ananya Biju (Infosys Springboard Internship)  
**Target Tableau Versions:** Tableau Desktop 2022.1+ / Tableau Public Desktop  
**Estimated Assembly Time:** 45–60 minutes following this click-by-click procedure  

---

## Prerequisites & Source Files

Before launching Tableau Desktop, confirm the following pipeline outputs are present:
1. `data/processed/Aegis_Hospital_Extract.hyper` (Native Tableau Extract) OR `data/processed/hospital_final_dataset.xlsx` (Multi-tab Excel)
2. `data/processed/synthetic_hospital_capacity.csv` (Capacity telemetry for Dashboard 4)
3. `dashboard/calculations/tableau_calculations.md` (Copy-paste calculation formulas)
4. `assets/branding/aegis_logo.png` and `aegis_wordmark.png` (Brand assets)

---

## Phase 1: Connect to Data Sources

1. **Launch Tableau Desktop** (or Tableau Public Desktop).
2. Under **Connect to a File**, select **Tableau Data Extract (.hyper)**.
3. Browse to and select `data/processed/Aegis_Hospital_Extract.hyper` (or `data/processed/hospital_final_dataset.xlsx` -> `Inpatient_Encounters`).
4. Rename this connection in the Data Pane to: **`Hospital_Encounters`**.
5. Add a secondary data connection:
   - Click **Add** next to Connections.
   - Choose **Text File** -> select `data/processed/synthetic_hospital_capacity.csv`.
   - Rename to **`Synthetic_Capacity_D4`**.
   - Note: Do NOT blend or join these two data sources together! They operate as independent data sources for their respective dashboards per Section 3 compliance rules.

---

## Phase 2: Create Parameters & Calculated Fields

1. Open `dashboard/calculations/tableau_calculations.md`.
2. In the Data Pane for `Hospital_Encounters`, right-click in whitespace -> **Create Parameter**:
   - Create `[p_Min_Sample_Size]` (Integer, Default: `30`).
   - Create `[p_Occupancy_Threshold_Pct]` (Float, Default: `85.0`).
   - Create `[p_Reporting_Period]` (String List: `All Available (1999–2008)`, `Last 3 Years`).
   - Create `[p_Theme_Mode]` (String List: `Dark Mode (Default)`, `Light Mode`).
3. Right-click whitespace -> **Create Calculated Field**:
   - Create all 12 calculated fields `[Total Admissions]`, `[Total Discharges]`, `[Average Length of Stay]`, `[Median Length of Stay]`, `[Readmission Rate 30d (CMS)]`, `[Emergency Admission Rate]`, `[Clinical Intensity Index]`, etc. exactly as specified in `tableau_calculations.md`.
4. Right-click each measure -> **Default Properties** -> **Number Format**:
   - `[Total Admissions]`, `[Total Discharges]`, `[Total Patient-Days]`: Number (Standard), `#,##0`.
   - `[Average Length of Stay]`, `[Median Length of Stay]`: Number (Custom), `0.00`, Suffix: `" days"`.
   - `[Readmission Rate 30d (CMS)]`, `[Emergency Admission Rate]`: Percentage, `0.00%` or `0.0%`.

---

## Phase 3: Construct Worksheets

Follow `dashboard/documentation/worksheet_specs.md` to assemble each worksheet:

### Worksheet 1: `D1_KPI_Admissions`
1. Drag `[Total Admissions]` to **Text** on Marks card.
2. Click **Text** -> Font: Arial / Tableau Semibold, 28pt, Color: `#F5F5F5`.
3. Rename sheet to `D1_KPI_Admissions`.
4. Format Sheet: Background `#141414`.

### Worksheet 2: `D1_KPI_ALOS`
1. Drag `[Average Length of Stay]` to **Text**.
2. Format: 28pt Bold, Color: `#5ACB57`.
3. Add subtext: `"Median: 4.0 d"` in 11pt `#929292`.
4. Rename to `D1_KPI_ALOS`.

### Worksheet 3: `D1_KPI_Readmission`
1. Drag `[Readmission Rate 30d (CMS)]` to **Text**.
2. Format: 28pt Bold, Color: `#F5F5F5`.
3. Add subtext: `"Target: <12.0%"` in 11pt `#5ACB57`.
4. Rename to `D1_KPI_Readmission`.

### Worksheet 4: `D1_Trend_Adm_vs_Disch`
1. Drag `[admission_date]` to Columns -> Set to `Continuous Month` (`MONTH([admission_date])`).
2. Drag `[Total Admissions]` to Rows.
3. Drag `[Total Discharges]` to the Rows axis to create a combined/dual axis.
4. Drag `Measure Names` to Color:
   - `[Total Admissions]`: `#5ACB57` (Vibrant green).
   - `[Total Discharges]`: `#94A3B8` (Cool slate).
5. Format sheet background: `#141414`, Gridlines: Thin `#222222`.

### Worksheet 5: `D1_Bar_Dept_Volume`
1. Drag `[department]` to Rows.
2. Drag `[Total Admissions]` to Columns.
3. Sort descending by `[Total Admissions]`.
4. Drag `[Department Volume Share]` to Label.
5. Format bars: Color `#5ACB57` (or sequential green ramp).

### Worksheet 6: `D2_Hist_LOS_Distribution`
1. Drag `[time_in_hospital]` (Dimension) to Columns.
2. Drag `[Total Admissions]` to Rows.
3. Drag `[los_band]` to Color.
4. Add Reference Line on X-axis: Value `4.40` (Mean ALOS), Label: `"Mean: 4.4d"`, Color `#5ACB57`.
5. Add Reference Line on X-axis: Value `4.00` (Median), Label: `"Median: 4.0d"`, Color `#FFFFFF`.

### Worksheet 7: `D3_Scatter_Volume_Readmit`
1. Drag `[Total Admissions]` to Columns.
2. Drag `[Readmission Rate 30d (CMS)]` to Rows.
3. Drag `[department]` to Detail.
4. Drag `[Total Patient-Days]` to Size.
5. Add Horizontal Reference Line at `11.34%` (Hospital Readmission Benchmark).

### Worksheet 8: `D4_Trend_Bed_Occupancy`
1. Switch data source to `Synthetic_Capacity_D4`.
2. Drag `[date]` to Columns (Continuous Day).
3. Drag `[bed_occupancy_rate_pct]` to Rows.
4. Add Reference Band on Y-axis: From `75.0` to `90.0`, Label: `"Target Operating Range (75–90%)"`.
5. Add Reference Line at `90.0`, Color `#EF4444`, Label: `"Critical Threshold (90%)"`.

---

## Phase 4: Assemble the 4 Dashboards

1. Click **New Dashboard** -> Under Size, set to **Fixed Size: 1600 × 900**.
2. **Dashboard 1: Hospital Overview**
   - Add a Horizontal Container across the entire 1600 × 900 canvas.
   - Drag a Vertical Container into the left slot -> Set Width to `240px` (Navigation Rail, Background `#1E1E1E`).
   - Drag an Image object for `aegis_wordmark.png` to the top of the rail.
   - Add Navigation Buttons for Dashboard 1, 2, 3, and 4.
   - In the right content area (`1360px` width, Background `#080808`), assemble:
     - Header bar with title `"Hospital Operations & Clinical Executive Overview"` and filters.
     - Horizontal container with the 5 KPI cards.
     - Middle container with `D1_Trend_Adm_vs_Disch` (65%) and `D1_Donut_Readmission_Breakdown` (35%).
     - Lower container with `D1_Bar_Dept_Volume` (55%) and `D1_Bar_Age_Distribution` (45%).
     - Footer text with data provenance and credits.
3. Repeat structured container placement for:
   - **Dashboard 2: Patient Flow**
   - **Dashboard 3: Department Analytics**
   - **Dashboard 4: Resource Utilization**

---

## Phase 5: Configure Dashboard Actions & Navigation

1. In top menu: **Dashboard** -> **Actions** -> **Add Action**:
   - **Filter Action (`Act_Filter_Department`):** Source Sheet: `D1_Bar_Dept_Volume` -> Target Sheets: All other D1 sheets on Click.
   - **Highlight Action (`Act_Highlight_Dept`):** Hovering on any department highlights across all sheets.
2. Right-click the Global Filters (`[admission_date]`, `[department]`) -> **Apply to Worksheets** -> **Selected Worksheets** (check all relevant sheets).
3. Configure the Navigation buttons in the left rail to jump cleanly between dashboards.

---

## Phase 6: Save & Package Workbook

1. Select **File** -> **Save As...**
2. Choose **Tableau Packaged Workbook (*.twbx)**.
3. Save as: **`Aegis.dv.twbx`**.
4. Test opening `Aegis.dv.twbx` in Tableau Desktop / Tableau Reader.

