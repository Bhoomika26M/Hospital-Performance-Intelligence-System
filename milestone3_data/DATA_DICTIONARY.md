# Milestone 3 Supplementary Data Dictionary

## Important disclaimer

**Every row in the three CSV files in this folder is synthetic demonstration data.** These files are not actual hospital operational or patient records, are not linked to any patient/admission rows in the source dataset, and must not be used for clinical, operational, financial, or research decisions. Hospital and department labels are reused only to keep dashboard filters consistent with `hospital_cleaned.csv`; bed capacities, occupancy, patient/admissions, and transfers are generated data.

## Generation scope and rules

- Source labels were inspected from `hospital_cleaned.csv`. The eight most frequent hospital-name labels and all six department labels were reused for consistency.
- The source admission dates cover 2019-05-08 through 2024-05-07. The occupancy and synthetic admission cohorts use that same inclusive admission-date window; synthetic discharges may occur after the final admission date.
- All dates use ISO `YYYY-MM-DD` format. Synthetic IDs use the `DEMO-` prefix.
- A **30-day readmission** is defined here as a subsequent synthetic admission occurring 1 to 30 calendar days (inclusive) after that patient's previous synthetic discharge. It is an all-cause demonstration definition, with no planned/unplanned distinction. The flag is 0 for first admissions and for later admissions outside the 30-day window.
- `previous_admission_date` means the previous synthetic admission's admission date; `days_since_previous_discharge` is the calendar-day difference from its discharge to the current admission. Both are blank (null) for each patient's first synthetic admission because no prior episode exists in this file.

## Standard synthetic KPI definitions and full-file reference values

These are separate synthetic demonstration metrics, not actual hospital measures. The ratios below were calculated from the CSVs currently in this folder:

| KPI | Formula and denominator | Verified value |
|---|---|---:|
| Weighted Bed Occupancy Rate | `SUM(occupied_beds) / SUM(total_beds) * 100`; denominator is total beds summed across valid occupancy observations. | 4,990,126 / 7,141,743 = **69.87%** |
| Average Daily Occupancy Rate | `AVERAGE(occupancy_rate) * 100`; average the non-null daily rates stored as ratios from 0 to 1. | 87,696 observations = **69.88%** |
| Overall Synthetic Readmission Rate | `SUM(readmission_flag) / total synthetic admission records * 100`. | 548 / 4,522 = **12.12%** |
| Readmission Percentage Among Records with Previous Admission | Sum `readmission_flag` only where `previous_admission_date` is non-null, divided by the number of such rows, times 100. | 548 / 1,522 = **36.01%** |

Both readmission metrics have 548 flagged records but different denominators. The 12.12% overall rate includes first synthetic admissions; the 36.01% percentage is limited to records with a previous admission date. They are distinct metrics, not competing calculations. Neither is clinically validated, and neither synthetic dataset is joined to original patient records. These figures are unfiltered full-file references; dashboard filters produce cohort-specific values.

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

## `synthetic_staff_allocation.csv`

All rows and values are **synthetic demonstrations**. The file reuses the eight hospital labels and six department labels in `daily_occupancy.csv` and contains one record per date, hospital, department, shift, and staff role. Its inclusive date coverage matches `daily_occupancy.csv`.

| Column | Meaning | Data type | Provenance |
|---|---|---|---|
| `date` | Calendar date for the staffing demonstration. | Date (`YYYY-MM-DD`) | Synthetic |
| `hospital` | Hospital label for the demonstration record. | String | Label reused from `daily_occupancy.csv`; row is synthetic |
| `department` | Department label for the demonstration record. | String | Label reused from `daily_occupancy.csv`; row is synthetic |
| `shift` | Demonstration shift: Morning, Evening, or Night. | String | Synthetic |
| `staff_role` | Demonstration role: Doctors, Nurses, Technicians, or Support Staff. | String | Synthetic |
| `allocated_staff` | Integer staff count allocated to the role and shift. | Non-negative integer | Synthetic |
| `required_staff` | Integer estimated staffing requirement based on synthetic bed capacity, role, department, and shift assumptions. | Non-negative integer | Synthetic estimate |
| `available_staff` | Allocated staff remaining after absences. | Non-negative integer | Synthetic, calculated as `allocated_staff - absent_staff` |
| `absent_staff` | Integer count of allocated staff absent in the demonstration record. | Non-negative integer | Synthetic |

`required_staff` is estimated as the ceiling of synthetic `total_beds` times a role/shift staffing ratio and a department adjustment, with a minimum of one. Allocations are sampled to demonstrate shortage (78%-98% of requirement), typical (98%-108%), and surplus (103%-125%) cases, with probabilities 25%, 50%, and 25%. Absences are sampled by role at 3.5% for Doctors, 5.5% for Nurses, 4.5% for Technicians, and 6% for Support Staff. These assumptions are illustrative, not staffing standards.

## `synthetic_equipment_utilization.csv`

All rows and values are **synthetic demonstrations**. The file reuses the eight hospital labels and six department labels in `daily_occupancy.csv` and contains one record per date, hospital, department, and equipment type. Its inclusive date coverage matches `daily_occupancy.csv`.

| Column | Meaning | Data type | Provenance |
|---|---|---|---|
| `date` | Calendar date for the equipment demonstration. | Date (`YYYY-MM-DD`) | Synthetic |
| `hospital` | Hospital label for the demonstration record. | String | Label reused from `daily_occupancy.csv`; row is synthetic |
| `department` | Department label for the demonstration record. | String | Label reused from `daily_occupancy.csv`; row is synthetic |
| `equipment_type` | Demonstration category: Ventilators, Patient Monitors, Infusion Pumps, ECG Machines, Ultrasound Machines, X-Ray Machines, Dialysis Machines, or Defibrillators. | String | Synthetic |
| `total_units` | Total demonstration units in the category. | Non-negative integer | Synthetic |
| `in_use_units` | Units in use. | Non-negative integer | Synthetic |
| `available_units` | Operational units not currently in use. | Non-negative integer | Synthetic, calculated |
| `maintenance_units` | Units unavailable due to simulated maintenance. | Non-negative integer | Synthetic |
| `utilization_rate` | Percentage of operational equipment in use; stored as a percentage from 0 to 100. | Float | Synthetic, calculated |

Equipment totals are estimated from synthetic bed capacity, equipment-category scaling factors, and department adjustments, with at least one unit per category. Maintenance is sampled at category-specific rates. In-use units are sampled from operational units using category and department utilization assumptions adjusted by the synthetic occupancy rate and random variation. Counts satisfy `in_use_units + available_units + maintenance_units = total_units`. Utilization is `in_use_units / (total_units - maintenance_units) * 100`. When no operational units remain, utilization is defined as 0% to avoid division by zero.

## Synthetic resource-data disclaimer

**Staff allocation and equipment utilization datasets are synthetically generated for demonstration and academic project purposes. They do not represent actual hospital staffing or equipment records.**

Both resource datasets use NumPy's default random generator with fixed seed `20261104` for reproducibility. Their staffing and equipment assumptions are illustrative, are not clinically validated, and must not be used for operational or clinical decisions. They are separate from original patient records and are not linked to patient or admission rows.

## Validation performed

The existing generated CSVs were re-read and checked for expected columns, nulls (allowing only the two not-applicable previous-episode fields on first admissions), invalid dates, duplicate records/keys, date ordering, admission/transfer linkage, distinct transfer departments, bed-capacity bounds, and calculated occupancy/readmission values. The staff and equipment datasets are checked by the root-level `validate_resource_data.py` script for required values, count constraints, formulas, categories, source labels, date coverage, and duplicate keys. Generation is reproducible with a fixed random seed.
