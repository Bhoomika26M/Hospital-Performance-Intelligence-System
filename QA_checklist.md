
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

| Dashboard | Test | Status |
|---|---|---|
| Hospital Overview | Dashboard loading | PASS - Visual |
| Hospital Overview | Department filter | PASS |
| Hospital Overview | Date filter | PASS |
| Hospital Overview | Navigation | PASS |
| Patient Flow | Dashboard loading | PASS - Visual |
| Patient Flow | Four charts visible | PASS - Visual |
| Patient Flow | Filters | N/A |
| Patient Flow | Cross-chart filtering | Not available |
| Department Analytics | Dashboard loading | PASS - Visual |
| Department Analytics | Four charts visible | PASS - Visual |
| Department Analytics | Department filter | PARTIAL - Further testing required |
| Resource Utilization | Dashboard loading | PASS - Visual |
| Resource Utilization | Four charts visible | PASS - Visual |

## 4. KPI Accuracy Issue

Tableau displays a synthetic readmission KPI of 36.01%, whereas Python validation gives 12.12%.

Status: PENDING INVESTIGATION.

Do not consider this KPI validated until the calculation and denominator are reconciled.

## 5. Data Limitations

- Occupancy data is synthetic.
- Readmission data is synthetic.
- Transfer data is synthetic.
- Staff and equipment utilization are not directly measured.
- Synthetic metrics must not be represented as actual hospital performance.

