# MedTrack_DV – Milestone 1

This package contains raw source copies, cleaned Tableau-ready datasets, a reproducible Python cleaning script, a Jupyter notebook, and the data audit report.

## Folder structure
- `data/raw/` – unchanged source copies
- `data/processed/` – cleaned CSV files for Tableau
- `scripts/` – reusable cleaning script
- `notebooks/` – step-by-step cleaning notebook
- `docs/` – data audit and limitations

## Important
The patient admission dataset and PMC infrastructure dataset are kept separate because no reliable shared hospital identifier is present. Do not create a row-wise join between them.

## Run the cleaning script
From the project root:
```bash
pip install pandas
python scripts/data_collection.py --patient data/raw/patient_admissions_raw.csv --infrastructure data/raw/pmc_infrastructure_raw.csv
```
