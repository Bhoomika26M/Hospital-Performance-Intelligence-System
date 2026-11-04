# Data Dictionary

## Provenance and limitations

`healthcare_dataset.csv` is the project-supplied original source table. The repository does not establish independent provenance or verify that the records describe real-world patients. This dictionary distinguishes that source and its prepared derivatives from the clearly synthetic demonstration files under `milestone3_data/`.

The original source includes person names and date/billing/demographic fields, but it does not include a stable patient ID suitable for reliable longitudinal linkage. Hospital and doctor values are names/labels in the source, not validated institutional identifiers or staff rosters. The files do not provide measured operational bed capacity/occupancy, staff allocation or hours, equipment inventory/use, or time-based equipment utilization. Derived counts and ratios cannot fill those gaps.

## Standard synthetic KPI definitions

These are full-file reference values, calculated from separate synthetic datasets. They are not original-patient KPIs.

| KPI | Formula and denominator | Verified value |
|---|---|---:|
| Weighted Bed Occupancy Rate | `SUM(occupied_beds) / SUM(total_beds) * 100`; denominator: 7,141,743 total-bed observations. | 4,990,126 / 7,141,743 = **69.87%** |
| Average Daily Occupancy Rate | `AVERAGE(occupancy_rate) * 100`; denominator: 87,696 non-null daily rates. | **69.88%** |
| Overall Synthetic Readmission Rate | `SUM(readmission_flag) / total synthetic admission records * 100`; denominator: 4,522 records. | 548 / 4,522 = **12.12%** |
| Readmission Percentage Among Records with Previous Admission | Sum of flags only for non-null `previous_admission_date` rows, divided by those rows, times 100; denominator: 1,522 records. | 548 / 1,522 = **36.01%** |

The two readmission percentages use different denominators and are distinct metrics. Occupancy/readmission data is synthetic, stays separate from original patient data, and is not clinically validated.

## Original source: `healthcare_dataset.csv`

The CSV has 15 source fields. Values are one record per source admission row; date values are stored as date-like text in the CSV. The table below describes the source fields and their observed representations.

| Column | Meaning / purpose | Observed type or format | Provenance |
|---|---|---|---|
| `Name` | Person name field carried by the source row. | Text | Original project-supplied source; authenticity not independently verified |
| `Age` | Age value associated with the row. | Integer-like numeric | Original project-supplied source |
| `Gender` | Gender category. | Text/category | Original project-supplied source |
| `Blood Type` | Blood type category. | Text/category | Original project-supplied source |
| `Medical Condition` | Condition category associated with the row. | Text/category | Original project-supplied source |
| `Date of Admission` | Admission date. | Date text (`YYYY-MM-DD` in observed data) | Original project-supplied source |
| `Doctor` | Doctor name/label associated with the row. | Text | Original project-supplied source; not a staffing allocation record |
| `Hospital` | Hospital name/label associated with the row. | Text | Original project-supplied source; not a verified facility identifier |
| `Insurance Provider` | Insurance provider category/name. | Text | Original project-supplied source |
| `Billing Amount` | Billing amount value associated with the row. | Decimal numeric | Original project-supplied source; not validated revenue/cost |
| `Room Number` | Room number/label on the row. | Integer-like numeric | Original project-supplied source; not a bed-capacity or equipment measure |
| `Admission Type` | Admission type category. | Text/category | Original project-supplied source |
| `Discharge Date` | Discharge date. | Date text (`YYYY-MM-DD` in observed data) | Original project-supplied source |
| `Medication` | Medication category/name. | Text | Original project-supplied source |
| `Test Results` | Test-result category. | Text/category | Original project-supplied source |

## Prepared patient data: `hospital_cleaned.csv`

This is the 54,966-row prepared table used by the current Streamlit pages. CSV date columns are serialized as text; pandas code parses them as datetimes when calculating time-series values. The department field is mapped from `Medical Condition` by the cleaning pipeline. The three normalized fields are min-max-scaled derived values.

| Column | Meaning / purpose | Type in the CSV / use | Provenance |
|---|---|---|---|
| `name` | Person name carried from source. | Text | Original field, standardized |
| `age` | Age value. | Integer | Original field |
| `gender` | Gender category. | Text/category | Original field |
| `blood_type` | Blood type category. | Text/category | Original field |
| `medical_condition` | Condition category. | Text/category | Original field |
| `date_of_admission` | Admission date. | Date text; parsed as datetime by app code | Original field, standardized |
| `doctor` | Doctor name/label. | Text | Original field; not staff allocation |
| `hospital` | Hospital name/label. | Text | Original field; many distinct values |
| `insurance_provider` | Insurance provider. | Text/category | Original field |
| `billing_amount` | Billing amount. | Decimal numeric | Original field |
| `room_number` | Room number/label. | Integer | Original field; not bed capacity or equipment use |
| `admission_type` | Admission type category. | Text/category | Original field |
| `discharge_date` | Discharge date. | Date text; parsed as datetime by app code | Original field |
| `medication` | Medication category/name. | Text | Original field |
| `test_results` | Test-result category. | Text/category | Original field |
| `department` | Broad department mapped from the condition category. | Text/category | Derived by project mapping |
| `length_of_stay` | Difference in calendar days between discharge and admission. | Numeric (observed float in CSV) | Derived |
| `age_normalized` | Min-max-scaled age value. | Float, typically 0-1 | Derived |
| `billing_amount_normalized` | Min-max-scaled billing amount. | Float, typically 0-1 | Derived |
| `length_of_stay_normalized` | Min-max-scaled length of stay. | Float, typically 0-1 | Derived |

Source rows lack a stable patient/admission identifier. A row is treated as an admission record for descriptive record counts, not necessarily a unique patient.

## Other original/prepared outputs

| File | Columns and purpose | Provenance / limitation |
|---|---|---|
| `hospital_raw_data.csv` | Patient/source fields plus `length_of_stay`, `department`, hospital aggregates (`total_patients`, `total_doctors`, `total_rooms_used`, `average_billing`) and department aggregates (`patient_count`, `doctors_available`, `rooms_used`, `average_billing_department`). | Derived output of `data_collection.py`; these aggregates are calculated from the source rows and do not provide measured staffing, bed, or equipment utilization. |
| `hospital_final_patient_data.csv` | Same 20-column patient schema as `hospital_cleaned.csv`. | Output/variant from KPI script, not an independent source. |
| `hospital_tableau_ready.csv` | Same 20-column schema as `hospital_cleaned.csv`. | Copy prepared for Tableau use; not a separate source. |
| `hospital_kpi_summary.csv` | `KPI` (text label), `Value` (numeric or blank), `Status` (text). | Derived summary. It reports total admissions and average stay; source occupancy, readmission, and bed utilization are unavailable. |
| `hospital_department_analytics.csv` | `department`, `total_admissions`, `average_length_of_stay`, `average_billing_amount`, `unique_doctors`, `admissions_per_doctor`, `admissions_score`, `stay_score`, `department_efficiency_score`, `efficiency_score_note`. | Derived department summary. The efficiency score is provisional and explicitly not clinically validated. `unique_doctors` and admissions-per-doctor are name counts/ratios, not actual staff allocation/workload. |

## Synthetic demonstration data

**All records and measurements described in this section are synthetic, are not actual hospital or patient observations, and are not linked to the original source rows.** Hospital and department labels are reused for dashboard filter consistency only. See [`../milestone3_data/DATA_DICTIONARY.md`](../milestone3_data/DATA_DICTIONARY.md) for the generation rules and full field notes.

### `milestone3_data/daily_occupancy.csv`

Purpose: demonstrate daily occupancy charts. Synthetic rows cover 2019-05-08 through 2024-05-07 for selected source hospital labels and all six source department labels.

| Column | Meaning | Type | Provenance |
|---|---|---|---|
| `date` | Occupancy snapshot day. | Date text (`YYYY-MM-DD`) | Synthetic |
| `hospital` | Reused hospital label. | Text | Label reused from source; synthetic row |
| `department` | Reused department label. | Text | Label reused from source; synthetic row |
| `total_beds` | Demonstration capacity assigned to the hospital/department pair. | Integer | Synthetic |
| `occupied_beds` | Demonstration occupied-bed count for the snapshot. | Integer | Synthetic |
| `available_beds` | Total beds minus occupied beds. | Integer | Synthetic, calculated |
| `occupancy_rate` | Daily occupied beds divided by total beds; ratio from 0 to 1, rounded to four decimals. Used in the separate Average Daily Occupancy Rate; weighted cohort occupancy uses the sums of occupied and total beds. | Float | Synthetic, calculated |

This is a generated snapshot series, not verified or measured bed capacity; it does not establish real occupancy or time-based bed utilization. The Streamlit Hospital Overview, Patient Flow, Department Analytics, and Resource Utilization pages load synthetic occupancy data separately from original patient data.

### `milestone3_data/synthetic_patient_readmissions.csv`

Purpose: demonstrate repeat-admission analysis. Synthetic IDs use a `DEMO-` prefix; hospital and department labels are reused from the source.

| Column | Meaning | Type | Provenance |
|---|---|---|---|
| `patient_id` | Synthetic person key repeated across that person's generated admissions. | Text | Synthetic |
| `admission_id` | Unique synthetic admission key. | Text | Synthetic |
| `admission_date` | Synthetic admission date. | Date text (`YYYY-MM-DD`) | Synthetic |
| `discharge_date` | Synthetic discharge date, on or after admission. | Date text (`YYYY-MM-DD`) | Synthetic |
| `hospital` | Reused hospital label. | Text | Label reused from source; synthetic row |
| `department` | Reused department label. | Text | Label reused from source; synthetic row |
| `previous_admission_date` | Previous synthetic episode's admission date; blank for first episode. | Nullable date text | Synthetic |
| `days_since_previous_discharge` | Calendar-day gap from prior synthetic discharge to this admission; blank for first episode. | Nullable integer | Synthetic, calculated |
| `readmission_flag` | 1 if gap is 1-30 calendar days inclusive; otherwise 0, including first episode. Overall rate denominator is all 4,522 records; the previous-admission subset denominator is the 1,522 rows with non-null `previous_admission_date`. | Integer (0/1) | Synthetic, calculated |

The rule is a simple all-cause demonstration definition, not an actual or clinically validated readmission measure. The data does not represent original patients.

### `milestone3_data/patient_transfers.csv`

Purpose: demonstrate transfer-flow charts. Each row references an admission in the synthetic readmission file.

| Column | Meaning | Type | Provenance |
|---|---|---|---|
| `patient_id` | Synthetic person ID matching the referenced synthetic admission. | Text | Synthetic |
| `admission_id` | Synthetic admission key. | Text | Synthetic |
| `hospital` | Reused hospital label. | Text | Label reused from source; synthetic row |
| `from_department` | Source department for the demonstration transfer. | Text | Label reused from source; synthetic row |
| `to_department` | Destination department, different from source. | Text | Label reused from source; synthetic row |
| `transfer_date` | Transfer date within the associated synthetic admission period. | Date text (`YYYY-MM-DD`) | Synthetic |
| `transfer_reason` | Demonstration reason assigned to the transfer. | Text | Synthetic |

These are not actual transfers and are not linked to the source patient table.

## Data limitations

- Project-supplied source provenance and real-world authenticity are not independently established.
- There is no stable patient ID or complete visit history in the original dataset; original-data readmission cannot be reliably determined.
- Original bed capacity, operational status, occupied beds, and time-based availability are absent; original occupancy and utilization are unavailable.
- The source includes doctor names and room numbers, but no staffing assignments, shifts, FTE, work hours, equipment inventory, equipment usage, or utilization duration.
- Source hospital labels have high cardinality and should not be treated as validated facility identifiers.
- Synthetic data is exclusively for dashboard demonstration and must be visibly distinguished from source data.
