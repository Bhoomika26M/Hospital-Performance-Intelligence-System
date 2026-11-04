
# MedTrack – QA Checklist

## 1. KPI Validation

| Test | Expected Result | Actual Result | Status |
|---|---|---|---|
| Total Admissions | 54966 | 54966 | PASS |
| Average Length of Stay | 15.50 days | 15.50 days | PASS |
| Negative Length of Stay | 0 | 0 | PASS |
| Department Admissions Total | 54966 | 54966 | PASS |

## 2. Healthcare Metrics Validation

| Test | Expected Result | Actual Result | Status |
|---|---|---|---|
| Weighted Bed Occupancy Rate | 69.87% = 4,990,126 / 7,141,743 | 69.87% | PASS |
| Average Daily Occupancy Rate | 69.88% across 87,696 non-null rates | 69.88% | PASS |
| Overall Synthetic Readmission Rate | 12.12% = 548 / 4,522 records | 12.12% | PASS |
| Readmission Percentage Among Records with Previous Admission | 36.01% = 548 / 1,522 records with a non-null previous-admission date | 36.01% | PASS |
| Occupancy missing values | 0 | 0 | PASS |
| Bed capacity calculation | Correct | Correct | PASS |
| Occupancy rate calculation | Correct | Correct | PASS |
| Duplicate occupancy records | 0 | 0 | PASS |
| Readmission flags | Only 0 and 1 | Valid | PASS |
| Readmission previous-date consistency | Consistent | Consistent | PASS |
| Transfer missing values | 0 | 0 | PASS |
| Duplicate transfers | 0 | 0 | PASS |
| Transfer-admission linkage | Valid | Valid | PASS |
| Transfer dates | Within admission period | Valid | PASS |

## 3. Dashboard Testing

| Dashboard | AppTest result |
|---|---|
| Hospital Overview | PASS — 7 Plotly charts, 5 metrics, 0 exceptions |
| Patient Flow | PASS — 9 Plotly charts, 5 metrics, 0 exceptions |
| Department Analytics | PASS — 10 Plotly charts, 9 metrics, 0 exceptions |
| Resource Utilization | PASS — 19 Plotly charts, 18 metrics, 0 exceptions |

These are AppTest render results only; no browser/visual test is claimed here.

## 4. Readmission and occupancy interpretation

- **Overall Synthetic Readmission Rate:** flagged records / all synthetic admission records = 548 / 4,522 = 12.12%.
- **Readmission Percentage Among Records with Previous Admission:** flagged records with a previous admission date / records with a previous admission date = 548 / 1,522 = 36.01%.
- The 12.12% and 36.01% figures use different denominators and are distinct metrics, not competing calculations.
- **Weighted Bed Occupancy Rate:** total occupied beds / total beds = 4,990,126 / 7,141,743 = 69.87%.
- **Average Daily Occupancy Rate:** mean of non-null daily occupancy rates = 69.88%; this differs from weighted occupancy.
- These values are full-file synthetic references. Filtered dashboard cohorts can have different values. Synthetic records are not joined to source patient records.
- `MedTrack_DV.twbx` is an optional legacy Tableau workbook and is not part of required Streamlit validation. Its historic denominator discrepancy is not a Streamlit KPI defect.

## 5. Data Limitations

- Occupancy data is synthetic.
- Readmission data is synthetic.
- Transfer data is synthetic.
- Staff and equipment utilization are not directly measured.
- Synthetic metrics must not be represented as actual hospital performance.
