# MedTrack_DV – Milestone 1 Data Audit

## Source files and verified structure
- Patient admissions source: healthcare_dataset (1)(3).csv
  - Original size: 55,500 rows × 15 columns
  - Missing cells: 0
  - Exact duplicate rows: 534
  - Admission dates: 2019-05-08 to 2024-05-07
  - Discharge dates: 2019-05-09 to 2024-06-06
  - Length of stay: calculated from discharge date minus admission date; observed range 1–30 days.
- PMC infrastructure source: PMC Hospital Infrastructure.csv
  - Original size: 737 rows × 17 columns
  - Missing cells: 819 (6.54%)
  - Exact duplicate rows: 0
  - `Ward No.` is entirely empty and is removed from the cleaned file.
  - Missing `Zone Name`, `Ward Name`, and `Average Monthly Patient Footfall` values are retained/handled without inventing numeric values.

## Cleaning performed
1. Trimmed leading/trailing whitespace from column names and text values.
2. Parsed patient admission/discharge dates.
3. Converted age and billing amount to numeric values.
4. Removed 534 exact duplicate patient rows.
5. Added `Length of Stay (Days)`, `Admission Month`, and `Admission Year`.
6. Standardized case for public/private and service availability labels.
7. Converted infrastructure numeric fields to numeric types; non-numeric `N.A.` entries become null.
8. Removed the fully empty `Ward No.` field and labeled missing zone/ward names as `Unknown`.
9. Kept patient and infrastructure datasets separate.

## Critical integration limitation
The patient file contains 39,876 distinct hospital-name values, while the PMC file contains 708 distinct facility names. No verified shared hospital identifier is supplied. These datasets must not be merged as if patient records belong to the PMC facilities. They can be presented as separate analytical sources within the same Tableau workbook.

## KPI feasibility
- Supported: total admissions, admission trends, average length of stay, billing analysis, patient age/gender/condition/admission-type breakdowns.
- Infrastructure-supported: facility counts, total reported beds, staff counts, staff-to-bed ratios (where denominator is valid), monthly patient footfall, service availability.
- Not supported by supplied data alone: verified readmission rate, true bed occupancy rate, patient-level bed utilization over time, department efficiency, equipment utilization. These require patient IDs/readmission history, occupied-bed time series, department identifiers, and equipment inventory/utilization data respectively.

## Output files
- `data/raw/patient_admissions_raw.csv`
- `data/raw/pmc_infrastructure_raw.csv`
- `data/processed/patient_admissions_cleaned.csv`
- `data/processed/pmc_infrastructure_cleaned.csv`
- `scripts/data_collection.py`
- `notebooks/hospital_cleaning.ipynb`
