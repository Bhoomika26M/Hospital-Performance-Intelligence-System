# Milestone 3 Supplementary Data Dictionary

## Important disclaimer

**Every row in the three CSV files in this folder is synthetic demonstration data.** These files are not actual hospital operational or patient records, are not linked to any patient/admission rows in the source dataset, and must not be used for clinical, operational, financial, or research decisions. Hospital and department labels are reused only to keep dashboard filters consistent with `hospital_cleaned.csv`; bed capacities, occupancy, patient/admissions, and transfers are generated data.

## Generation scope and rules

- Source labels were inspected from `hospital_cleaned.csv`. The eight most frequent hospital-name labels and all six department labels were reused for consistency.
- The source admission dates cover 2019-05-08 through 2024-05-07. The occupancy and synthetic admission cohorts use that same inclusive admission-date window; synthetic discharges may occur after the final admission date.
- All dates use ISO `YYYY-MM-DD` format. Synthetic IDs use the `DEMO-` prefix.
- A **30-day readmission** is defined here as a subsequent synthetic admission occurring 1 to 30 calendar days (inclusive) after that patient's previous synthetic discharge. It is an all-cause demonstration definition, with no planned/unplanned distinction. The flag is 0 for first admissions and for later admissions outside the 30-day window.
- `previous_admission_date` means the previous synthetic admission's admission date; `days_since_previous_discharge` is the calendar-day difference from its discharge to the current admission. Both are blank (null) for each patient's first synthetic admission because no prior episode exists in this file.

## `daily_occupancy.csv`

All rows and numerical values are **synthetic**. Hospital and department text labels are reused from the cleaned dataset.

| Column | Meaning | Data type | Provenance |
|---|---|---|---|
| `date` | Calendar day of the occupancy snapshot. | Date (`YYYY-MM-DD`) | Synthetic |
| `hospital` | Hospital label for this demonstration series. | String | Label reused from original cleaned dataset; row is synthetic |
| `department` | Department label for this demonstration series. | String | Label reused from original cleaned dataset; row is synthetic |
| `total_beds` | Demonstration bed capacity for this hospital/department pair. | Integer | Synthetic |
| `occupied_beds` | Demonstration beds occupied on the date; never exceeds capacity. | Integer | Synthetic |
| `available_beds` | `total_beds - occupied_beds`. | Integer | Synthetic, calculated |
| `occupancy_rate` | `occupied_beds / total_beds`, represented as a ratio from 0 to 1 (rounded to four decimal places). | Float | Synthetic, calculated |

## `synthetic_patient_readmissions.csv`

All records and IDs are **synthetic** and are not linked to source patients or source admissions. Hospital and department text labels are reused from the cleaned dataset.

| Column | Meaning | Data type | Provenance |
|---|---|---|---|
| `patient_id` | Synthetic person identifier; repeated across that person's synthetic admissions. | String | Synthetic |
| `admission_id` | Unique synthetic admission identifier. | String | Synthetic |
| `admission_date` | Date of the synthetic admission. | Date (`YYYY-MM-DD`) | Synthetic |
| `discharge_date` | Date of discharge for that synthetic admission; on or after admission. | Date (`YYYY-MM-DD`) | Synthetic |
| `hospital` | Hospital label assigned to this synthetic admission. | String | Label reused from original cleaned dataset; row is synthetic |
| `department` | Department label assigned to this synthetic admission. | String | Label reused from original cleaned dataset; row is synthetic |
| `previous_admission_date` | Admission date of the same synthetic patient's immediately preceding episode; blank for the first episode. | Nullable date (`YYYY-MM-DD`) | Synthetic |
| `days_since_previous_discharge` | Calendar days from previous episode's discharge to this admission; blank for the first episode. | Nullable integer | Synthetic, calculated |
| `readmission_flag` | 1 when admission is 1-30 days after previous discharge; otherwise 0, including first episodes. | Integer (0/1) | Synthetic, calculated |

## `patient_transfers.csv`

All transfer rows and identifiers are **synthetic** and refer only to admissions in `synthetic_patient_readmissions.csv`. Hospital and department text labels are reused from the cleaned dataset.

| Column | Meaning | Data type | Provenance |
|---|---|---|---|
| `patient_id` | Synthetic person identifier matching the referenced synthetic admission. | String | Synthetic |
| `admission_id` | Synthetic admission identifier to which this transfer belongs. | String | Synthetic; references synthetic admission file |
| `hospital` | Hospital label for the synthetic transfer. | String | Label reused from original cleaned dataset; row is synthetic |
| `from_department` | Source department, matching the admission's department. | String | Label reused from original cleaned dataset; transfer is synthetic |
| `to_department` | Destination department, different from the source. | String | Label reused from original cleaned dataset; transfer is synthetic |
| `transfer_date` | Transfer date within the associated synthetic admission/discharge interval. | Date (`YYYY-MM-DD`) | Synthetic |
| `transfer_reason` | Demonstration reason assigned to the transfer. | String | Synthetic |

## Validation performed

The generated CSVs were re-read and checked for expected columns, nulls (allowing only the two not-applicable previous-episode fields on first admissions), invalid dates, duplicate records/keys, date ordering, admission/transfer linkage, distinct transfer departments, bed-capacity bounds, and calculated occupancy/readmission values. Generation is reproducible with a fixed random seed.
