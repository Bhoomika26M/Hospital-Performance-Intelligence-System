# Healthcare Operations Methodology

## Data
- `healthcare_dataset(1).csv` (supplied by the internship provider) (55,500 rows), cleaned to 54,966 admissions
- `department_resources.csv`: beds, doctors, nurses and technicians for 6 departments
- `equipment_utilization.csv`: **simulated** (see below)

## Cleaning (notebooks/hospital_cleaning.ipynb)
- 534 duplicate rows were removed (55,500 to 54,966 records); the notebook verifies that the rows removed equal the duplicates found.
- No missing values were found in the columns used by the dashboard, so nothing needed filling or dropping.
- Patient names were trimmed and title-cased. Other text columns were checked for stray spaces.
- Admission and discharge dates were converted to dates, and length of stay was calculated as discharge date minus admission date, in days. Date validity checks are run at the end of the notebook.
- 106 records (0.19%) have negative billing amounts (from -2,008.49 to -23.87). They were kept, because the data does not show whether they are refunds, credits or errors. Billing is not used in any KPI.
- Billing outliers were checked with the IQR rule and left in the data.

## Pipeline
1. `scripts/data_collection.py` collects the raw files.
2. `notebooks/hospital_cleaning.ipynb` produces `hospital_cleaned.csv`. `notebooks/01_data_preprocessing.ipynb` then adds the derived columns (department, region, readmission flag and others) and writes `hospital_featured.csv`.
3. `scripts/generate_hospital_kpis.py` merges department resources, writes `hospital_final.csv`, the KPI tables and `hospital_final_dataset.xlsx`.
4. `dashboard/app.py` (Streamlit) reads `hospital_final.csv`. `tests/validate_kpi.py` checks the KPIs.

## Assumptions
- Total capacity is 600 beds (sum of allocated beds). Patients are counted in hospital from admission day up to, not including, discharge day.
- The first 30 days of data are excluded from occupancy and peak load, because patients admitted before 8 May 2019 are not recorded.
- Months only partly inside the selected date range are hidden from trend charts.
- Department, Region and the readmission flag are derived columns added in `notebooks/01_data_preprocessing.ipynb`; they are not in the original source data.
- Equipment hours are **simulated** with a fixed seed (42), by `scripts/generate_equipment_data.py`. They are not real measurements.

## Limitations
- The supplied data appears to be synthetic. Hospital names, regions (5 almost equal groups) and departments (about 9,100-9,200 admissions each, ALOS 15.4-15.7 days) show almost no real variation.
- Readmission is very low (0.08%, 45 admissions) because few patient names repeat; patients are matched on name. Read it as a data property, not a real hospital rate.
- Efficiency scores stretch very small differences between departments across 0-100. Treat the ranking with caution.
- Facility and Region are project-created groupings, not real locations: each hospital name is hashed (MD5) into one of 10 facilities ("Facility 01" to "Facility 10"), and the facilities are grouped into five labelled regions (North, South, East, West, Central). The near-equal split across regions is a result of the hashing. Both columns are added in `notebooks/01_data_preprocessing.ipynb`.
- Region has no real geography or coordinates, so differences between regions carry no meaning. It is used as a demonstration filter, and there is no map.



- Department is derived from Medical Condition with a fixed lookup in 01_data_preprocessing.ipynb (Cancer → Oncology, Diabetes → Endocrinology, Hypertension → Cardiology, Obesity → General Medicine, Arthritis → Orthopedics, Asthma → Pulmonology). Ward is derived from Room Number.


- Readmitted 30d is derived in `notebooks/01_data_preprocessing.ipynb`. The data has no patient ID, so a patient is identified by Name + Gender + Blood Type; two different people sharing all three would be treated as one patient. An admission is flagged when the same patient was discharged 0 to 30 days before it. A patient's first admission is never flagged, and overlapping stays (negative gaps) are ignored. The readmission rate is the share of admissions flagged, about 0.08% here (45 admissions), so monthly readmission charts are noisy.
