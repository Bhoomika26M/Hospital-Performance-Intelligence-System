# KPI Definitions

## Provenance and interpretation

The original patient/admission data is in `hospital_cleaned.csv`. The project-provided source file does not establish independent real-world provenance, so its authenticity is not independently verified. Synthetic demonstration KPIs use only the CSVs under `milestone3_data/` and must never be presented as actual hospital performance.

The Streamlit pages calculate descriptive measures from the original/project-prepared patient data and load relevant synthetic files separately. The KPI summary CSV marks original-source occupancy and readmission unavailable. Synthetic measures must be identified as demonstrations and must not be joined to original patient records.

## Required KPIs

| KPI | Purpose | Calculation | Source and status |
|---|---|---|---|
| **Total admissions** | Count admission records in the selected dataset/filter scope. | Count rows in the selected patient/admission records. It is a record count, not a count of unique people. | `hospital_cleaned.csv`; calculated in the Streamlit prototype and summarized in `hospital_kpi_summary.csv`. |
| **Average length of stay** | Summarize time between admission and discharge for records with valid stay values. | Arithmetic mean of non-null `length_of_stay` values, where the cleaned pipeline derives days as `discharge_date - date_of_admission`. | `hospital_cleaned.csv`; also summarized in `hospital_kpi_summary.csv`. The summary file stores 15.5 days. |
| **Weighted Bed Occupancy Rate** | Show the weighted share of synthetic demonstration beds occupied across the selected cohort. | `SUM(occupied_beds) / SUM(total_beds) * 100`. The denominator is the sum of total-bed observations, not the count or mean of row percentages. | `milestone3_data/daily_occupancy.csv`; verified full-file result: 4,990,126 / 7,141,743 = **69.8727%** (69.87%). Synthetic only; original-source occupancy is unavailable. Used as the weighted occupancy KPI on Streamlit pages. |
| **Average Daily Occupancy Rate** | Summarize the mean of daily synthetic occupancy rates. | `AVERAGE(occupancy_rate) * 100`; exclude missing rates from both the mean and its denominator. The CSV stores each rate as a ratio from 0 to 1. | `milestone3_data/daily_occupancy.csv`; 87,696 non-null observations yield **69.8847%** (69.88%). This is distinct from weighted occupancy and is not the primary aggregate occupancy KPI. |
| **Overall Synthetic Readmission Rate** | Demonstrate flagged synthetic admissions as a share of all synthetic admission records. | `SUM(readmission_flag) / total synthetic admission records * 100`. The denominator includes records with null `previous_admission_date`; flags must be valid 0/1 values. | `milestone3_data/synthetic_patient_readmissions.csv`; 548 / 4,522 = **12.1185%** (12.12%). Synthetic only; not a validated or risk-adjusted clinical readmission measure. Displayed in Hospital Overview and Department Analytics. |
| **Readmission Percentage Among Records with Previous Admission** | Describe the flagged share only among synthetic admissions with a recorded previous admission date. | `SUM(readmission_flag for rows where previous_admission_date is non-null) / count(rows where previous_admission_date is non-null) * 100`. | Same synthetic file; 548 / 1,522 = **36.0053%** (36.01%). This is a distinct, narrower denominator—not an alternative calculation of the overall rate. It is documented/validated separately and is not currently a separate dashboard KPI card. |
| **Total discharges** | Count admission records with a recorded discharge date, or count discharge events by discharge date. | For the original dataset, count rows with a valid `discharge_date`; for a monthly series, group those rows by discharge month. This is a record/event count, not unique patients. | `hospital_cleaned.csv`. Patient Flow displays valid discharge-date count and monthly discharge counts, but does not show a dedicated total-discharges KPI card. |

## Related descriptive metrics

The four full-file reference values above are for the unfiltered datasets. Dashboard values recalculate against the selected filters. Neither occupancy measure is available from the original patient dataset, and synthetic measures are never joined to original patient records.

| Metric | Calculation | Source and caveat |
|---|---|---|
| Average billing | Mean of non-null `billing_amount` for the selected records. | `hospital_cleaned.csv`; descriptive billing field, not a hospital revenue or cost measure. |
| Admissions per listed doctor | Department admission-record count divided by distinct doctor-name count. | Calculated from `hospital_cleaned.csv` and also present in `hospital_department_analytics.csv`. Doctor names are not staffing allocation, FTE, work hours, patient assignments, or actual workload. |
| Provisional department efficiency score | Precomputed combination of min-max admissions-per-listed-doctor score and inverse min-max average length-of-stay score, averaged and rounded to two decimals. | `hospital_department_analytics.csv`. The source labels this score provisional and not clinically validated; it should not be treated as a validated efficiency KPI. |
| Bed utilization rate | Requires defined bed capacity and bed-use measurements over a stated time interval. | Unavailable from original data. The synthetic daily snapshot file supports an occupancy ratio, not a validated time-based utilization measure or real operational capacity. |

## Missing measures

The original patient dataset does not supply reliable patient identity/visit history, operational beds and occupied-bed observations, staff allocation or working hours, or equipment inventory/use. Room numbers and listed doctor names do not substitute for these missing operational measures. Synthetic examples are clearly labeled and are for dashboard demonstration only.
