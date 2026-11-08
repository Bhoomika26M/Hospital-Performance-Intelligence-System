# Dataset sources

| File | What it is | Real or simulated |
|---|---|---|
| `healthcare_dataset.csv` | Kaggle "Healthcare Dataset": 55,500 admissions with age, condition, admission and discharge dates, billing, room, admission type, test result | Real file, but the data itself is synthetic (generated names and values) |
| `department_master.csv` | Licensed beds, doctors, target length of stay and equipment per department | Simulated – my own assumptions |
| `hospital_resource_raw.csv` | Monthly staffed beds, nurses, doctors, equipment hours per department | Simulated – linked to the real admissions (busier ward → more equipment use) |
| `patient_feedback_raw.csv` | Monthly satisfaction score and wait time per department | Simulated – satisfaction falls and waits rise when the ward is very full |

Why simulated? The admissions file has no beds, staff or equipment columns. I could not
find a single public file that covers all of that for one hospital, so I generated them with a
fixed random seed (`seed = 42`), which means anyone running the script gets the same numbers.
The files also contain a few deliberate problems (about 1% missing nurse counts, department names
written in different cases) so the cleaning step has something real to do.

## Real public datasets I'd use for a next version
Drop any of these in `data/raw/` and map the columns:
- HHS / CDC hospital capacity and utilization time series (data.gov: "COVID-19 Estimated ICU Beds Occupied by State Timeseries")
- Definitive Healthcare – USA hospital beds (licensed beds, staffed beds, ICU beds, utilization), on data.virginia.gov
- ReOpen DC hospital bed utilization (opendata.dc.gov)
- Global hospital bed capacity (Kaggle, by Igor Kiulian)

## Department mapping
The admissions have a *medical condition*, not a department, so I grouped them:
Cancer → Oncology · Hypertension → Cardiology · Diabetes + Obesity → Endocrinology ·
Asthma → Pulmonology · Arthritis → Rheumatology.
