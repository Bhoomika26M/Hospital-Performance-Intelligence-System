# MedTrack - Hospital Performance Intelligence System

MedTrack is a hospital analytics project for exploring patient admission records, length of stay, department-level patterns, and the limitations of the available operational data. The repository contains a data preparation and KPI pipeline, a multi-page Streamlit prototype, and supplementary synthetic demonstration datasets.

## Objectives

- Prepare and validate the supplied healthcare dataset for analysis.
- Summarize admission, length-of-stay, billing, and department patterns.
- Provide a Streamlit prototype for exploring the available records.
- Document which operational measures are unavailable from the source and which supplementary files are synthetic.

## Technologies

- Python
- pandas
- Streamlit (`st.navigation` / `st.Page`)
- Plotly Express
- CSV datasets and a Jupyter cleaning notebook
- An optional legacy Tableau packaged workbook is present; Streamlit is the required dashboard implementation.

There is no dependency manifest in the project root. The current scripts import pandas, Streamlit, and Plotly Express. Install the packages in your Python environment before running the prototype if they are not already installed.

## Project structure

```text
.
|-- app.py
|-- home.py
|-- pages/
|   |-- Hospital_Overview.py
|   |-- Patient_Flow.py
|   |-- Department_Analytics.py
|   `-- Resource_Utilization.py
|-- data_collection.py
|-- hospital_cleaning.py
|-- hospital_cleaning.ipynb
|-- generate_hospital_kpis.py
|-- healthcare_dataset.csv
|-- hospital_cleaned.csv
|-- hospital_raw_data.csv
|-- hospital_final_patient_data.csv
|-- hospital_tableau_ready.csv
|-- hospital_kpi_summary.csv
|-- hospital_department_analytics.csv
|-- milestone3_data/
|   |-- daily_occupancy.csv
|   |-- patient_transfers.csv
|   |-- synthetic_patient_readmissions.csv
|   |-- synthetic_staff_allocation.csv
|   |-- synthetic_equipment_utilization.csv
|   `-- DATA_DICTIONARY.md
|-- validate_hospital_kpis.py
|-- validate_healthcare_metrics.py
|-- validate_resource_data.py
`-- docs/
    |-- DV_Hospital Operations & Patient Analytics Dashboard (1).pdf
    |-- dashboard_documentation.md
    |-- kpi_definitions.md
    |-- testing_report.md
    `-- data_dictionary.md
```

`MedTrack_DV.twbx` is an optional legacy Tableau workbook. It is not required by the Streamlit application and was not changed as part of KPI standardization. Tableau rendering, interactions, and portability remain unverified. The PDF in `docs/` is a dashboard reference.

## Data sources and limitations

- `healthcare_dataset.csv` is the project-supplied source patient/admission table (55,500 source rows as reported by the existing README). The repository does not establish independent provenance or confirm whether the names and records are real-world data; do not treat that authenticity as verified.
- `hospital_cleaned.csv` is the prepared 54,966-row dataset. The existing project reports 534 exact duplicates removed, 100% completeness, no remaining missing values, and six department categories.
- `hospital_raw_data.csv`, `hospital_final_patient_data.csv`, and `hospital_tableau_ready.csv` are pipeline outputs/variants, not independent sources.
- `hospital_kpi_summary.csv` reports total admissions and average length of stay; occupancy, readmission, and bed-utilization values are unavailable from the original dataset.
- `hospital_department_analytics.csv` contains department summaries and an explicitly provisional, non-clinically-validated efficiency score.
- Files under `milestone3_data/` contain synthetic demonstration values. Their hospital/department labels are reused for filter consistency, but their beds, occupancy, patient/admission histories, and transfers are not real records and are not linked to the source dataset.
- Synthetic occupancy and readmission datasets are integrated into the relevant Streamlit pages, kept separate from original patient data, and clearly identified as demonstrations.
- The source has no reliable patient identifier and longitudinal visit history. It also lacks measured staff allocation, working hours, equipment inventories/use, and original bed occupancy/capacity time series. Listed doctor names and room numbers do not establish staff or equipment utilization.

See [docs/data_dictionary.md](docs/data_dictionary.md), [docs/kpi_definitions.md](docs/kpi_definitions.md), and [milestone3_data/DATA_DICTIONARY.md](milestone3_data/DATA_DICTIONARY.md) for field-level details and calculation limitations.

## Standard synthetic KPI definitions

These are separate synthetic demonstration metrics; none is a measured original-patient KPI.

| KPI | Formula and denominator | Verified full-dataset value |
|---|---|---:|
| Weighted Bed Occupancy Rate | `SUM(occupied_beds) / SUM(total_beds) * 100`; denominator is 7,141,743 total-bed observations. | 69.87% |
| Average Daily Occupancy Rate | `AVERAGE(occupancy_rate) * 100`; denominator is 87,696 non-null daily occupancy-rate observations. | 69.88% |
| Overall Synthetic Readmission Rate | `SUM(readmission_flag) / total synthetic admission records * 100`; denominator is 4,522 records. | 12.12% |
| Readmission Percentage Among Records with Previous Admission | Sum of flags only for records with non-null `previous_admission_date`, divided by that subset's 1,522 records, times 100. | 36.01% |

Both readmission rates have 548 flagged records as numerator. The percentages differ because their denominators differ; they are not competing calculations. The readmission and occupancy files remain synthetic and are not joined to original patient records.

## Milestones

1. **Data collection and preparation:** the supplied `healthcare_dataset.csv` combines patient-admission and hospital attributes; the pipeline does not download or integrate a separate external operational dataset. `data_collection.py` removes exact duplicates, standardizes values, derives length of stay and department mapping, and creates hospital/department aggregates. It writes `hospital_raw_data.csv` and `hospital_cleaned.csv`. The existing `hospital_cleaning.ipynb` records a reproducible cleaning run, aggregate quality report, and milestone assertions.

   The existing README reports 55,500 source records, 534 exact duplicates removed, 54,966 prepared records, 100% prepared-dataset completeness, 0% missing values, and six department categories. The pipeline enforces no remaining duplicate rows, completeness above 95%, and missing values below 2%; it stops with an error when those checks fail.
2. **KPI engineering:** summary and department CSV outputs are present. Synthetic occupancy and readmission measures are separate from unavailable original-source operational measures.
3. **Dashboard development:** the Streamlit pages integrate supplementary synthetic demonstration data where appropriate, without joining it to original patient records. The legacy Tableau workbook is optional.
4. **Documentation and delivery:** dashboard, KPI, dataset, and test documentation are included under `docs/`; see [docs/testing_report.md](docs/testing_report.md) for the latest recorded validation and AppTest status.

## Dashboard descriptions

The Streamlit app exposes Hospital Overview, Patient Flow, Department Analytics, and Resource Utilization pages, plus a home/app page. The pages summarize original admission counts, dates, length of stay, billing, and department comparisons. Synthetic occupancy and readmission are displayed from their separate demonstration datasets. Original-source occupancy and readmission remain unavailable, and no synthetic records are joined to the original patient data.

Detailed implementation notes and known filter-scope caveats are in [docs/dashboard_documentation.md](docs/dashboard_documentation.md). These notes describe the checked-in Streamlit code, not an inspected Tableau workbook.

## Run the Streamlit prototype

1. Open a terminal in the project root.
2. Ensure Python is installed and install the imports required by this project if needed:

   ```powershell
   python -m pip install pandas streamlit plotly
   ```

3. Start the app:

   ```powershell
   streamlit run app.py
   ```

4. Open the local URL printed by Streamlit and use the top navigation to select a page.

The prototype reads `hospital_cleaned.csv`, `hospital_kpi_summary.csv`, and/or `hospital_department_analytics.csv` from the project root and the relevant supplementary synthetic files in `milestone3_data/`, depending on the page. Keep those files in place.

To regenerate pipeline outputs, review the relevant script before running it because `data_collection.py` and `generate_hospital_kpis.py` write CSV files in the project root. The documentation task did not modify those scripts or datasets.
