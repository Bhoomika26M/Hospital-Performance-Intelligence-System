# KPI Definitions

## Provenance and interpretation

The original patient/admission data is in `hospital_cleaned.csv`. The project-provided source file does not establish independent real-world provenance, so its authenticity is not independently verified. Synthetic demonstration KPIs use only the CSVs under `milestone3_data/` and must never be presented as actual hospital performance.

The current Streamlit pages calculate some descriptive measures from the original/project-prepared dataset. The KPI summary CSV marks original-data occupancy and readmission unavailable. The synthetic datasets are not currently loaded by the Streamlit pages.

## Required KPIs

| KPI | Purpose | Calculation | Source and status |
|---|---|---|---|
| **Total admissions** | Count admission records in the selected dataset/filter scope. | Count rows in the selected patient/admission records. It is a record count, not a count of unique people. | `hospital_cleaned.csv`; calculated in the Streamlit prototype and summarized in `hospital_kpi_summary.csv`. |
| **Average length of stay** | Summarize time between admission and discharge for records with valid stay values. | Arithmetic mean of non-null `length_of_stay` values, where the cleaned pipeline derives days as `discharge_date - date_of_admission`. | `hospital_cleaned.csv`; also summarized in `hospital_kpi_summary.csv`. The summary file stores 15.5 days. |
| **Occupancy rate** | Show what share of staffed/operational beds are occupied at a snapshot. | For the synthetic snapshot: `occupied_beds / total_beds * 100`. When rolling up multiple departments/hospitals for the same snapshot, use `sum(occupied_beds) / sum(total_beds) * 100`, not an unweighted mean of unit rates. The CSV stores the ratio from 0 to 1 rounded to four decimals; multiply by 100 for a percentage display. | Original data: unavailable (`hospital_kpi_summary.csv` has no value). Demonstration-only calculation is possible from `milestone3_data/daily_occupancy.csv`; current Streamlit Resource Utilization page does not load that file and shows unavailable. |
| **Readmission rate** | Demonstrate a repeat-admission measure under the documented synthetic rule. | For this synthetic file only: `sum(readmission_flag) / number of synthetic admission records * 100`. `readmission_flag` is 1 when an admission occurs 1-30 calendar days after the same synthetic patient's previous discharge; first episodes and gaps outside that window are 0. | Original data: unavailable because reliable patient IDs and longitudinal visit history are absent. Demonstration-only fields are in `milestone3_data/synthetic_patient_readmissions.csv`; current Streamlit pages do not load them. This simple demo ratio is not a validated or risk-adjusted clinical readmission measure. |
| **Total discharges** | Count admission records with a recorded discharge date, or count discharge events by discharge date. | For the original dataset, count rows with a valid `discharge_date`; for a monthly series, group those rows by discharge month. This is a record/event count, not unique patients. | `hospital_cleaned.csv`. Patient Flow displays valid discharge-date count and monthly discharge counts, but does not show a dedicated total-discharges KPI card. |

## Related descriptive metrics

| Metric | Calculation | Source and caveat |
|---|---|---|
| Average billing | Mean of non-null `billing_amount` for the selected records. | `hospital_cleaned.csv`; descriptive billing field, not a hospital revenue or cost measure. |
| Admissions per listed doctor | Department admission-record count divided by distinct doctor-name count. | Calculated from `hospital_cleaned.csv` and also present in `hospital_department_analytics.csv`. Doctor names are not staffing allocation, FTE, work hours, patient assignments, or actual workload. |
| Provisional department efficiency score | Precomputed combination of min-max admissions-per-listed-doctor score and inverse min-max average length-of-stay score, averaged and rounded to two decimals. | `hospital_department_analytics.csv`. The source labels this score provisional and not clinically validated; it should not be treated as a validated efficiency KPI. |
| Bed utilization rate | Requires defined bed capacity and bed-use measurements over a stated time interval. | Unavailable from original data. The synthetic daily snapshot file supports an occupancy ratio, not a validated time-based utilization measure or real operational capacity. |

## Missing measures

The original patient dataset does not supply reliable patient identity/visit history, operational beds and occupied-bed observations, staff allocation or working hours, or equipment inventory/use. Room numbers and listed doctor names do not substitute for these missing operational measures. Synthetic examples are clearly labeled and are for dashboard demonstration only.
