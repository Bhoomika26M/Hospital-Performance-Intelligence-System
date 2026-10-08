# Hospital Performance Intelligence System

## Milestone 1: Data Collection and Preparation

The supplied `healthcare_dataset.csv` contains combined patient-admission and hospital attributes. The pipeline derives hospital and department operational measures from this source; it does not download or integrate a separate external operational dataset.

Run the pipeline from this folder:

```powershell
python data_collection.py
```

The pipeline creates:

- `hospital_raw_data.csv`: deduplicated, standardized patient records integrated with hospital and department aggregates.
- `hospital_cleaned.csv`: Tableau-ready dataset with numeric measures, admission dates, length of stay, department mapping, and operational aggregates.
- `hospital_cleaning.ipynb`: reproducible pipeline run, aggregate quality report, and milestone assertions.

The script stops with an error if there are remaining duplicate rows, completeness is at or below 95%, or missing values reach 2% of the integrated dataset. The cleaning notebook reports aggregate counts only and does not display patient-level rows.

### Current Validation

- Source records: 55,500
- Exact duplicates removed: 534
- Prepared records: 54,966
- Prepared dataset completeness: 100%
- Missing values: 0%
- Department categories mapped: 6