# MedTrack_DV Dashboard Storyboard (Module 4)

Planned layout, filters, navigation, actions and department comparisons for the four
dashboard pages. The dashboard is built in Streamlit (`dashboard/app.py`) instead of
Tableau. Screenshots of the finished pages are in `docs/screens/`.

## Purpose and audience

Help hospital administrators, healthcare managers and medical staff monitor patient flow,
compare departments and plan resources. All pages read the same dataset
(`data/processed/hospital_final.csv`) and the same KPI functions (`scripts/kpi_utils.py`),
so a number shown on any page matches `data/processed/kpi_*.csv`.

## Global filters (sidebar, apply to every page)

| Filter | Type | Effect |
|---|---|---|
| Date range | Date picker | Limits admissions, discharges and trends to the chosen window |
| Department | Multi-select | Cardiology, Endocrinology, General Medicine, Oncology, Orthopedics, Pulmonology |
| Admission type | Multi-select | Filters admissions by type of admission |
| Region | Multi-select | North, South, East, West, Central (project-created grouping) |
| Hospital (top 200) | Multi-select | The 200 hospitals with the most admissions |
| Total beds (Capacity settings) | Number input | Denominator for occupancy and bed utilization (default: sum of beds allocated) |
| Reset filters | Button | Returns every filter to its default |
| Download filtered data | Button | Exports the currently filtered records as CSV |
| Dark mode | Toggle | Switches the dashboard theme |

An empty multi-select means "All".

## Navigation

A "Navigate" radio selector in the sidebar switches between the four pages in this order:
1. Hospital Overview
2. Patient Flow
3. Department Analytics
4. Resource Utilization

Filters stay set when the page changes.

## Page 1: Hospital Overview

Goal: one-glance health check of the hospital.

```
+---------------------------------------------------------------+
| KPI cards: Total Admissions | Occupancy | Avg LOS | Readmission |
|            Bed Utilization (peak) | Discharge Count            |
+----------------------------+----------------------------------+
| Monthly admissions trend   | Monthly occupancy trend          |
+----------------------------+----------------------------------+
| Monthly readmission trend  | Admissions by department / region|
+----------------------------+----------------------------------+
```

## Page 2: Patient Flow

Goal: how patients move in and out over time.

```
+---------------------------------------------------------------+
| Admission trend (daily / monthly)                              |
+----------------------------+----------------------------------+
| Admissions vs discharges   | Patients in hospital (daily      |
| (discharge tracking)       | census) with peak marked         |
+----------------------------+----------------------------------+
| Average stay analysis (length-of-stay distribution / by dept)  |
+---------------------------------------------------------------+
```

## Page 3: Department Analytics

Goal: compare the six departments side by side.

```
+---------------------------------------------------------------+
| Department table: admissions, avg LOS, readmission rate,       |
| efficiency score, admissions per bed, admissions per doctor    |
+----------------------------+----------------------------------+
| Patient volume by dept     | Readmission rate by dept         |
+----------------------------+----------------------------------+
| Efficiency score comparison| Treatment capacity (admissions   |
|                            | per bed / per doctor)            |
+---------------------------------------------------------------+
```

## Page 4: Resource Utilization

Goal: whether beds, staff and equipment match demand.

```
+---------------------------------------------------------------+
| Bed utilization (average vs peak against capacity)             |
+----------------------------+----------------------------------+
| Staff allocation by dept   | Equipment utilization            |
| (doctors, nurses, techs)   | (from generated equipment data)  |
+----------------------------+----------------------------------+
| Capacity planning: resource availability vs admissions         |
+---------------------------------------------------------------+
```

## Dashboard actions and interactions

- Changing any sidebar filter refreshes every chart and KPI card on the current page.
- Hovering over a chart shows the exact value and date.
- Department comparisons are available on Pages 3 and 4 and respond to the Department filter.
- KPI cards use the same definitions as `docs/kpi_definitions.md`.

## Department comparison design

Each department is compared on the same measures: admissions, average length of stay,
readmission rate, efficiency score, beds, doctors, nurses, technicians, admissions per bed
and admissions per doctor. Efficiency score is scaled 0-100 across the six departments.

## Known limits

- The data is synthetic: departments, regions and the readmission flag are derived columns
  (see `docs/methodology.md`), so differences between them are small.
- Region has no coordinates, so there is no map.
- Readmission is about 0.08% of admissions, so monthly readmission charts are noisy.