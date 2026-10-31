# Dashboard Documentation

## Scope and implementation status

The repository contains four Streamlit page scripts and an app-level navigation setup. This document describes the visualizations and controls visible in those scripts. It does **not** assert that the Tableau dashboards have been built: the expected packaged workbook, `MedTrack_DV.twbx`, was not found in the project. The supplied [dashboard reference PDF](<DV_Hospital Operations & Patient Analytics Dashboard (1).pdf>) is present, but workbook implementation cannot be checked without the workbook.

The current pages read original/project-prepared CSVs. They do not load `milestone3_data/`; the synthetic occupancy, readmission, and transfer records therefore do not power the current prototype.

## Navigation

`app.py` registers a top navigation bar with these entries:

- **App** — `home.py`; a consolidated page containing overview, patient-flow, department, resource, and readmission sections.
- **Hospital Overview** — `pages/Hospital_Overview.py`.
- **Patient Flow** — `pages/Patient_Flow.py`.
- **Department Analytics** — `pages/Department_Analytics.py`.
- **Resource Utilization** — `pages/Resource_Utilization.py`.

This navigation is implemented in Streamlit. No Tableau navigation or cross-dashboard actions can be confirmed without `MedTrack_DV.twbx`.

## Hospital Overview

**Data:** `hospital_cleaned.csv`.

**KPIs:** total admission records, average patient age, average length of stay, and average billing. In the App page, the cards are total admissions, average stay, average billing, and department count.

**Charts and tables:**

- Bar chart of admission records by department.
- Bar chart of admission records by medical condition.
- Monthly admissions line chart.
- Department summary table with admissions, average stay, and average billing.
- A Plotly donut chart of department admission distribution.
- The App page also includes patient-flow, department analytics, resource availability notices, and a patient-record explorer.

**Filters:** the standalone page provides department and medical-condition multiselects. The App page also provides admission type and admission-date range filters.

**Interactions:** Streamlit multiselect/date widgets filter the page's main dataframe; the overview table and CSV download use the resulting filtered data. The donut chart is built from the unfiltered dataframe in the standalone page, so it does not follow the sidebar selections. Runtime behavior has not been tested.

## Patient Flow

**Data:** `hospital_cleaned.csv`.

**KPIs:** admission-record count, average stay, count of valid admission dates, and count of valid discharge dates.

**Charts and tables:**

- Monthly admissions line chart.
- Admissions by admission type bar chart.
- Monthly discharge counts bar chart.
- Length-of-stay frequency bar chart (up to 60 displayed stay values).
- Plotly length-of-stay histogram and length-of-stay-by-department box plot.
- Patient-flow table with available name, condition, admission type, admission date, discharge date, and length-of-stay columns.

**Filters:** admission type and medical condition multiselects.

**Interactions:** the primary KPIs, monthly charts, frequency chart, table, and download use the filtered dataframe. The Plotly histogram and box plot use the unfiltered dataframe, so they do not follow the sidebar selections. There is no standalone date-range or hospital filter in this page. Runtime behavior has not been tested.

## Department Analytics

**Data:** `hospital_cleaned.csv` and `hospital_department_analytics.csv`.

**KPIs:** admission-record count for the selected departments, number of selected departments, average length of stay, and average billing.

**Charts and tables:**

- Admissions-by-department bar chart.
- Average length-of-stay-by-department bar chart.
- Average-billing-by-department bar chart.
- Table of admissions and unique listed doctors by department, including admissions per listed doctor.
- Provisional department-efficiency-score bar chart and table, when the score field exists.
- Detailed department summary table.
- Plotly scatter plot of length of stay versus billing, colored by department and sampled to at most 1,500 rows for rendering.

**Filters:** department multiselect.

**Interactions:** the page derives displayed admission, stay, billing, workload, detailed-summary, and scatter-plot values from the selected departments. The efficiency scores are loaded from a precomputed summary and are not recalculated from interactive selections. The listed-doctor ratio is not staff allocation or a measured clinical workload. Runtime behavior has not been tested.

## Resource Utilization

**Data:** `hospital_cleaned.csv` and `hospital_department_analytics.csv`.

**KPIs:** admission-record count, unique listed-doctor count, average stay, and average billing.

**Charts and tables:**

- Admission workload by department bar chart.
- Admissions per listed doctor by department, with a supporting table.
- Average length of stay by department bar chart.
- Resource summary table and CSV download.
- Bed occupancy and bed-utilization cards are explicitly displayed as **Unavailable** in the current page.

**Filters:** department multiselect.

**Interactions:** workload summaries, stay summary, and download are based on selected departments. The page does not load `daily_occupancy.csv`, so the synthetic occupancy data does not currently change its unavailable status. The unique listed-doctor count and admissions-per-listed-doctor ratio are descriptive counts, not staff allocation, staffing levels, or time-based workload. No equipment inventory or equipment utilization measurements are available. Runtime behavior has not been tested.

## Known gaps and interpretation

- The four Streamlit page scripts are not evidence of four completed Tableau dashboards; workbook presence and Tableau interactions remain pending.
- The supplemental datasets are standalone synthetic demonstration data and are not integrated into the current app.
- The original/project-prepared patient table lacks a stable longitudinal patient ID; readmission rate is unavailable for that source.
- Bed occupancy and utilization cannot be measured from the original patient table. Synthetic bed data exists separately but is not used by the app.
- No staff allocation, staffing hours, equipment inventory, equipment use, or time-based equipment utilization measurements are available.
- Some Plotly charts intentionally use the unfiltered page dataframe, as noted in the relevant dashboard sections.
