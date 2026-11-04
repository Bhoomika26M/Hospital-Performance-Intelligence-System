# Dashboard Documentation

## Scope and implementation status

The repository contains four Streamlit page scripts and an app-level navigation setup. Streamlit is the required dashboard implementation. `MedTrack_DV.twbx` is an optional legacy Tableau workbook; it was not modified or runtime-tested as part of this KPI update. The supplied [dashboard reference PDF](<DV_Hospital Operations & Patient Analytics Dashboard (1).pdf>) is a design reference.

The pages load original/project-prepared patient data and relevant `milestone3_data/` CSVs separately. Synthetic occupancy, readmission, and transfer records are demonstration data and are not joined to original patient records.

## Standard synthetic KPI definitions

The following full-file reference values are from the currently available supplementary CSVs. Dashboard values recalculate for their selected cohorts.

| KPI | Formula and denominator | Full-file reference |
|---|---|---:|
| Weighted Bed Occupancy Rate | `SUM(occupied_beds) / SUM(total_beds) * 100`; denominator is total beds summed across observations. | 4,990,126 / 7,141,743 = **69.87%** |
| Average Daily Occupancy Rate | `AVERAGE(occupancy_rate) * 100`; denominator is non-null daily occupancy-rate observations. | 87,696 observations = **69.88%** |
| Overall Synthetic Readmission Rate | `SUM(readmission_flag) / total synthetic admission records * 100`. | 548 / 4,522 = **12.12%** |
| Readmission Percentage Among Records with Previous Admission | Sum of flags for non-null `previous_admission_date` records, divided by that subset's record count, times 100. | 548 / 1,522 = **36.01%** |

The readmission measures have the same flagged-record numerator (548) but distinct denominators. They are not competing calculations. The original patient dataset has no reliable longitudinal ID/history, so these synthetic measures are not original-patient readmission rates. Average Daily Occupancy Rate is a descriptive mean, separate from the primary weighted occupancy KPI.

## Navigation

`app.py` registers a top navigation bar with these entries:

- **App** — `home.py`; a consolidated page containing overview, patient-flow, department, resource, and readmission sections.
- **Hospital Overview** — `pages/Hospital_Overview.py`.
- **Patient Flow** — `pages/Patient_Flow.py`.
- **Department Analytics** — `pages/Department_Analytics.py`.
- **Resource Utilization** — `pages/Resource_Utilization.py`.

This navigation is implemented in Streamlit. No Tableau navigation or cross-dashboard actions can be confirmed without `MedTrack_DV.twbx`.

## Hospital Overview

**Data:** `hospital_cleaned.csv`; synthetic occupancy and readmission files are loaded separately.

**KPIs:** total admission records, average patient age, average length of stay, and average billing from original patient data; weighted bed occupancy and overall synthetic readmission rate from their respective synthetic datasets. The occupancy and readmission cards identify the measures as synthetic.

**Charts and tables:**

- Bar chart of admission records by department.
- Bar chart of admission records by medical condition.
- Monthly admissions line chart.
- Department summary table with admissions, average stay, and average billing.
- A Plotly donut chart of department admission distribution.
- The App page also includes patient-flow, department analytics, resource availability notices, and a patient-record explorer.

**Filters:** the standalone page provides department and medical-condition multiselects. The App page also provides admission type and admission-date range filters.

**Interactions:** Streamlit multiselect/date widgets filter the page's main dataframe; the overview table and CSV download use the resulting filtered data. The donut chart is built from the unfiltered dataframe in the standalone page, so it does not follow the sidebar selections. AppTest rendered this page without exceptions; browser interactions were not tested.

## Patient Flow

**Data:** `hospital_cleaned.csv` plus separate synthetic occupancy and transfer datasets.

**KPIs:** admission-record count, average stay, count of valid admission dates, and count of valid discharge dates from the original dataset; peak occupancy is calculated from synthetic occupancy records.

**Charts and tables:**

- Monthly admissions line chart.
- Admissions by admission type bar chart.
- Monthly discharge counts bar chart.
- Length-of-stay frequency bar chart (up to 60 displayed stay values).
- Plotly length-of-stay histogram and length-of-stay-by-department box plot.
- Patient-flow table with available name, condition, admission type, admission date, discharge date, and length-of-stay columns.

**Filters:** admission type and medical condition multiselects.

**Interactions:** the primary KPIs, monthly charts, frequency chart, table, and download use the filtered dataframe. The Plotly histogram and box plot use the unfiltered dataframe, so they do not follow the sidebar selections. There is no standalone date-range or hospital filter in this page. AppTest rendered this page without exceptions; browser interactions were not tested.

## Department Analytics

**Data:** `hospital_cleaned.csv`, `hospital_department_analytics.csv`, and separate synthetic occupancy/readmission datasets.

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

**Interactions:** the page derives displayed admission, stay, billing, workload, detailed-summary, and scatter-plot values from the selected departments. The efficiency scores are loaded from a precomputed summary and are not recalculated from interactive selections. The listed-doctor ratio is not staff allocation or a measured clinical workload. AppTest rendered this page without exceptions; browser interactions were not tested.

Department readmission percentages use flagged synthetic admissions divided by all synthetic admissions in the corresponding selected cohort. Occupancy by department/month is weighted from summed occupied beds divided by summed total beds.

## Resource Utilization

**Data:** separate synthetic occupancy, staff-allocation, and equipment-utilization datasets, with the original patient dataset used only for its source-patient section.

**KPIs:** total, occupied, and available bed observations and **Weighted Bed Occupancy Rate** (`SUM(occupied_beds) / SUM(total_beds) * 100`), plus staff and equipment metrics from their respective synthetic datasets. Occupancy, staff, and equipment values are explicitly synthetic demonstrations.

**Charts and tables:**

- Admission workload by department bar chart.
- Admissions per listed doctor by department, with a supporting table.
- Average length of stay by department bar chart.
- Resource summary table and CSV download.
- Bed availability and occupancy comparisons are derived from `daily_occupancy.csv`; summed counts across dates represent repeated observations (bed-days), not unique capacity.
- Staff allocation and equipment utilization are loaded from their separate synthetic demonstration CSVs.

**Filters:** department multiselect.

**Interactions:** date, hospital, and department filters apply to the relevant synthetic resource datasets and original patient data separately. The unique listed-doctor count and admissions-per-listed-doctor ratio are descriptive counts, not staff allocation, staffing levels, or time-based workload. Resource observations do not represent actual hospital operations.

## Known gaps and interpretation

- The four Streamlit page scripts are not evidence of four completed Tableau dashboards; workbook presence and Tableau interactions remain pending.
- The supplemental datasets are integrated into relevant Streamlit pages as synthetic demonstrations and remain separate from original patient records.
- The original/project-prepared patient table lacks a stable longitudinal patient ID; readmission rate is unavailable for that source.
- Bed occupancy and utilization cannot be measured from the original patient table; synthetic occupancy is available separately in the app.
- Synthetic staff and equipment data is available for demonstration; no actual staff allocation, equipment inventory, or equipment utilization is established.
- The legacy Tableau workbook is optional and its calculations/interactions are not certified by this Streamlit documentation. Its older readmission worksheets may use the previous-admission subset denominator (36.01%), distinct from the overall 12.12% rate.
- Some Plotly charts intentionally use the unfiltered page dataframe, as noted in the relevant dashboard sections.
