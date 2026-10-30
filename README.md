# MedTrack_DV

## Hospital Operations & Patient Analytics Dashboard

MedTrack_DV is a Streamlit dashboard for exploring validated hospital patient-analysis and resource-allocation data. It presents patient outcomes, readmissions, length of stay, costs, beds, staffing, equipment, and resource allocation activity using Pandas and Plotly.

The project uses the existing root-level `app.py` as its Streamlit entry point. It does not use Tableau.

## Features

- Hospital Overview with patient and resource KPI cards.
- Patient Analytics for readmissions, outcomes, length of stay, costs, and condition comparisons.
- Resource Utilization for:
  - Bed allocation and occupancy.
  - Staff allocation and on-duty rates.
  - Equipment allocation and utilization.
  - Resource availability.
  - Monthly resource allocation-record trends.
  - Bed type, staff type, and equipment type filters.
- Data Explorer with dataset previews, row/column/missing-value summaries, and CSV downloads.
- Gender and Condition filters for patient-focused pages.
- Dark navy and blue responsive dashboard styling.
- Explicit limitation notices where the available data cannot support a requested analysis.

## Technology stack

- Python
- Pandas
- Streamlit
- Plotly
- Excel workbook support through `openpyxl`

## Project structure

```text
MedTrack_DV/
├── app.py
├── dashboard_storyboard.pdf
├── LICENSE
├── data/
│   ├── healthcare_data.csv
│   ├── hospital data analysis.csv
│   ├── hospital-resource-allocation-records.csv
│   ├── hospital_cleaned.csv
│   ├── hospital_final_dataset.xlsx
│   ├── hospital_raw_data.csv
│   ├── hospital_resource_raw.csv
│   └── patient_analysis_raw.csv
├── docs/
│   ├── DV_Hospital Operations & Patient Analytics Dashboard.pdf
│   ├── Dashboard_Testing_Report.md
│   ├── Dashboard_User_Guide.md
│   ├── Dataset_Sources.md
│   ├── KPI_Documentation.md
│   ├── Methodology.md
│   └── QA_Checklist.md
├── notebooks/
│   └── hospital_cleaning.ipynb
├── scripts/
│   ├── dashboard_storyboard.pdf
│   ├── create_dashboard_storyboard.py
│   ├── data_collection.py
│   ├── generate_hospital_kpis.py
│   ├── inspect_resource_issues.py
│   └── validate_kpis.py
├── inspect_data.py
└── README.md
```

`ConfirmationPage-265630069393.pdf` is a local submission artifact and
should not be included in the Git commit. The root `dashboard_storyboard.pdf`
is the project storyboard to retain.

## Installation on Windows

Open PowerShell in the project folder:

```powershell
cd C:\path\to\MedTrack_DV
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pandas openpyxl streamlit plotly
```

If PowerShell prevents activation, the environment can be used directly:

```powershell
.\.venv\Scripts\python.exe -m pip install pandas openpyxl streamlit plotly
```

The repository does not currently contain a dependency lock file or `requirements.txt`; the command above installs the packages imported by the application and validation scripts.

## Prepare the Excel workbook

The dashboard reads `data/hospital_final_dataset.xlsx`. If the workbook needs to be regenerated from the validated CSV inputs, run:

```powershell
.\.venv\Scripts\python.exe scripts\generate_hospital_kpis.py
```

This writes the `Patient Data`, `Resource Data`, `KPI Summary`, and `KPI Definitions` sheets.

## Run the Streamlit application

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

Then open the local URL shown by Streamlit, normally `http://localhost:8501`.

## Testing and validation

Run the existing validation script:

```powershell
.\.venv\Scripts\python.exe scripts\validate_kpis.py
```

Run a syntax check:

```powershell
.\.venv\Scripts\python.exe -m py_compile app.py
```

The completed Module 7 evidence is documented in:

- `docs/QA_Checklist.md`
- `docs/Dashboard_Testing_Report.md`

The audit verified KPI values independently, all four pages, patient/resource filters, empty states, edge cases, charts, navigation, and CSV download controls.

## Dataset and KPI limitations

- The patient analysis dataset contains patient records but no reliable admission or discharge dates.
- The patient analysis and resource datasets do not provide a reliable department field or patient-to-resource link.
- Admission totals are patient-record counts, not verified admission events.
- Resource monthly trends are aggregated allocation records, not patient admission, discharge, movement, or census trends.
- Daily patient census, peak patient load, discharge tracking, patient movement, and department analytics are not supported by the validated data.
- Resource totals should not automatically be interpreted as unique hospital-wide totals without a confirmed snapshot grain.
- Zero resource denominators are handled safely; corresponding rates display as unavailable rather than dividing by zero.
- Missing numeric resource values are treated as zero in the dashboard's aggregate resource helper.

## Documentation

- [Dataset sources](docs/Dataset_Sources.md)
- [KPI documentation](docs/KPI_Documentation.md)
- [Dashboard user guide](docs/Dashboard_User_Guide.md)
- [Methodology](docs/Methodology.md)
- [QA checklist](docs/QA_Checklist.md)
- [Dashboard testing report](docs/Dashboard_Testing_Report.md)
