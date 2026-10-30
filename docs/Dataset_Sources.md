# Dataset Sources

## Scope and provenance

The project contains three primary datasets used during data collection and preparation. Their original external URLs, authors, licensing details, and collection provenance are not recorded in the repository. This document therefore identifies each source by its project-local filename and does not invent external attribution.

The dashboard's validated KPI and resource views use:

- `data/hospital data analysis.csv`
- `data/hospital-resource-allocation-records.csv`
- `data/hospital_final_dataset.xlsx`

`healthcare_data.csv` is the third collected CSV dataset and is documented below, but it is not the source of the dashboard's primary patient KPIs.

## 1. Healthcare dataset

**Project-local file:** `data/healthcare_data.csv`  
**Rows:** 500  
**Columns:** 10  
**Purpose:** Additional clinical and follow-up information collected during the preparation stage.

### Columns

| Column | Description supported by the field name |
|---|---|
| `Patient_ID` | Patient identifier |
| `Age` | Patient age |
| `Gender` | Patient gender |
| `Blood_Pressure` | Blood pressure value |
| `Heart_Rate` | Heart rate value |
| `Cholesterol_Level` | Cholesterol level |
| `BMI` | Body mass index |
| `Diagnosis` | Diagnosis |
| `Treatment_Plan` | Treatment plan |
| `Follow_Up_Date` | Follow-up date |

### Observed limitations

- The file contains 95 missing values.
- It has a follow-up date but no validated admission date or discharge date.
- It has no department, movement, resource-allocation, or equipment-utilization fields.
- It is not loaded by the current dashboard workbook loader.

## 2. Hospital patient analysis dataset

**Project-local file:** `data/hospital data analysis.csv`  
**Rows:** 984  
**Columns:** 10  
**Purpose:** Validated patient-analysis source for the patient KPIs, filters, and patient-focused charts.

### Columns

| Column | Dashboard use |
|---|---|
| `Patient_ID` | Patient identifier; no cross-dataset resource link is established |
| `Age` | Patient attribute available for analysis |
| `Gender` | Patient filter |
| `Condition` | Patient filter and cost grouping |
| `Procedure` | Patient attribute available in the source |
| `Cost` | Average patient cost and cost-by-condition chart |
| `Length_of_Stay` | Average and distribution analysis |
| `Readmission` | Readmission rate and comparison charts |
| `Outcome` | Recovery rate and outcome charts |
| `Satisfaction` | Available source field; not a current dashboard KPI |

### Observed validation results and limitations

- No missing values or duplicate rows were found during Module 7 validation.
- `Readmission` contains only Yes/No values after normalization.
- `Outcome` contains Recovered/Stable values.
- Length of stay is positive for all records.
- There is no admission date, discharge date, department, movement history, or daily census field.
- “Total Admissions” is defined as patient-record count, not verified admission-event count.

## 3. Hospital resource allocation dataset

**Project-local file:** `data/hospital-resource-allocation-records.csv`  
**Rows:** 200  
**Columns:** 20  
**Purpose:** Bed, staff, equipment, hospital, surge, and allocation-date analysis.

### Columns

| Column | Dashboard use |
|---|---|
| `allocation_id` | Allocation record identifier |
| `hospital_id` | Hospital identifier |
| `hospital_name` | Hospital bed comparison |
| `hospital_street_address` | Hospital location attribute |
| `hospital_city` | Hospital location attribute |
| `hospital_state` | Hospital location attribute |
| `hospital_postal_code` | Hospital location attribute |
| `hospital_country` | Hospital location attribute |
| `allocation_date` | Monthly resource allocation-record trend |
| `bed_type` | Bed filter and bed utilization grouping |
| `beds_allocated` | Bed capacity denominator |
| `beds_occupied` | Bed utilization numerator |
| `staff_type` | Staff filter and staff grouping |
| `staff_allocated` | Staff capacity denominator |
| `staff_on_duty` | Staff on-duty numerator |
| `equipment_type` | Equipment filter and equipment grouping |
| `equipment_allocated` | Equipment capacity denominator |
| `equipment_in_use` | Equipment utilization numerator |
| `surge_status` | Resource-record surge indicator |
| `notes` | Source notes |

### Observed validation results and limitations

- No missing values or duplicate rows were found during Module 7 validation.
- All 200 allocation dates parsed successfully.
- No negative checked resource values were found.
- No record had occupied beds greater than allocated beds.
- Zero allocations exist for beds, staff, and equipment and are handled by guarded rate calculations.
- Resource records do not include patient identifiers or department fields.
- Monthly values are sums of allocation records and should not automatically be treated as unique hospital-wide totals.

## 4. Generated Excel workbook

**Project-local file:** `data/hospital_final_dataset.xlsx`  
**Purpose:** Dashboard input workbook generated by `scripts/generate_hospital_kpis.py`.

### Sheets

- `Patient Data`: Patient analysis data plus `Readmission_Flag`.
- `Resource Data`: Resource allocation data plus row-level bed/staff rate columns.
- `KPI Summary`: Seven validated KPI values.
- `KPI Definitions`: KPI definitions and source labels.

The workbook is a generated project artifact rather than an independent source dataset.

## 5. Prepared and cleaned copies

The data folder also contains prepared copies produced during the collection workflow:

- `hospital_raw_data.csv`
- `patient_analysis_raw.csv`
- `hospital_resource_raw.csv`
- `hospital_cleaned.csv`

These copies are retained as project artifacts. The dashboard reads the generated Excel workbook, not these files directly.

