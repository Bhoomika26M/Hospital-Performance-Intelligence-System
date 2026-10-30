# Methodology

## 1. Project workflow

MedTrack_DV follows this workflow:

1. Collect and inspect project-local datasets.
2. Standardize and prepare working CSV copies.
3. Validate patient and resource fields.
4. Engineer KPI values and definitions.
5. Export the validated workbook used by the dashboard.
6. Load the workbook in Streamlit.
7. Present patient and resource analytics with Pandas and Plotly.
8. Validate calculations, filters, page behavior, edge cases, and downloads.

## 2. Data collection and preparation

The collection workflow is implemented in `scripts/data_collection.py`.

It:

- Locates the three project-local input CSV files.
- Loads them with Pandas.
- Standardizes column names by trimming whitespace, lowercasing, and replacing spaces with underscores.
- Converts available date fields with coercion where applicable.
- Removes exact duplicate rows.
- Writes prepared CSV copies:
  - `hospital_raw_data.csv`
  - `patient_analysis_raw.csv`
  - `hospital_resource_raw.csv`

The repository also contains `hospital_cleaned.csv` and a cleaning notebook. The dashboard does not load those files directly; it loads the generated Excel workbook.

No external source URL or author information is recorded in the project, so no external provenance is asserted here.

## 3. Validation

The validation workflow is implemented in `scripts/validate_kpis.py` and in the checks within `scripts/generate_hospital_kpis.py`.

Patient validation checks include:

- Required fields are present.
- Readmission values normalize to Yes/No.
- Length of stay is non-missing and positive.
- Cost is non-missing.
- Duplicate and missing-value inspection.

Resource validation checks include:

- Required bed and staffing fields are present.
- Checked resource values are non-negative.
- Occupied beds do not exceed allocated beds.
- Hospital/date duplication is inspected.
- Allocation and staffing rates are recalculated.

The validation script reports zero invalid readmission values, zero non-positive stays, zero bed over-capacity rows, and no missing or duplicate values in the validated patient/resource CSVs.

## 4. KPI engineering

`scripts/generate_hospital_kpis.py` reads:

- `data/hospital data analysis.csv`
- `data/hospital-resource-allocation-records.csv`

It creates:

- Patient KPI calculations.
- Resource rate calculations.
- A `KPI Summary` sheet.
- A `KPI Definitions` sheet.

It exports:

- `Patient Data`
- `Resource Data`
- `KPI Summary`
- `KPI Definitions`

The dashboard loads these four sheets from `data/hospital_final_dataset.xlsx`.

The formulas and definitions are documented in `docs/KPI_Documentation.md`.

## 5. Dashboard development

The root-level `app.py`:

- Loads the generated workbook with `pd.read_excel`.
- Applies patient filters to patient analysis data.
- Applies bed, staff, and equipment filters to resource data.
- Uses Streamlit for navigation, controls, KPI cards, tables, and downloads.
- Uses Plotly Express for charts.
- Uses shared helpers for page headers, chart styling, patient metrics, and resource metrics.

The dashboard preserves a four-page structure:

- Overview
- Patient Analytics
- Resource Utilization
- Data Explorer

The UI uses a dark navy and blue design. No Tableau workbook is used.

## 6. Resource calculations

Resource rates use aggregate filtered values:

```text
Bed occupancy = sum(beds_occupied) / sum(beds_allocated) * 100
Staff on-duty rate = sum(staff_on_duty) / sum(staff_allocated) * 100
Equipment utilization = sum(equipment_in_use) / sum(equipment_allocated) * 100
```

Available capacity uses:

```text
Available beds = beds_allocated - beds_occupied
Available staff = staff_allocated - staff_on_duty
Available equipment = equipment_allocated - equipment_in_use
```

The dashboard resource helper coerces invalid numeric values and fills missing values with zero for aggregate calculations. Zero denominators are displayed as `N/A`.

Monthly resource trends parse `allocation_date`, remove invalid dates, group by month, and sum resource measures. They are not patient-flow trends.

## 7. Validation and delivery testing

Module 7 testing used:

- The existing `scripts/validate_kpis.py`.
- Independent Pandas calculations against source CSVs.
- Workbook-to-source KPI comparisons.
- Streamlit `AppTest` page and filter interactions.
- Controlled in-memory edge-case frames.
- CSV serialization checks.
- A live Streamlit health endpoint.

Verified areas include:

- Seven primary KPI values.
- Four dashboard pages.
- Patient and resource filters.
- Combined and empty filter states.
- Missing values and zero denominators.
- Invalid dates and no-valid-date messaging.
- Plotly chart rendering.
- CSV download controls.
- Navigation and application startup.

The detailed evidence is recorded in:

- `docs/QA_Checklist.md`
- `docs/Dashboard_Testing_Report.md`

## 8. Methodological limitations

The validated datasets do not provide reliable:

- Admission dates
- Discharge dates
- Patient movement events
- Daily patient census
- Peak patient load
- Department fields
- Patient-to-resource linkage

Accordingly, the dashboard does not fabricate admission, discharge, movement, census, peak-load, or department analytics. “Total Admissions” is documented as patient-record count, and resource trends are documented as allocation-record aggregations.

