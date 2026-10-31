# Dashboard Testing Report

## 1. Scope
KPI calculations, filters, navigation, patient-flow analytics, data quality.

## 2. KPI validation
The KPI validation script completed successfully. All 25 checks recorded in `docs/kpi_validation.csv` passed, covering overall, monthly, department and region KPIs, department resources, and efficiency-score bounds.

## 3. Data quality
Duplicate rows: 0. Missing values (core columns): 0.00% (target < 2%). Completeness: 100.00% (target > 95%). Department names match between the patient data and the resources file.

## 4. Interaction tests
See `qa_checklist.md`. Passed: 15 / 15.

## 5. Issues found and fixed
| Issue | Fix |
|-------|-----|
| Partial first/last months distorted trends | Hidden by `trim_partial()` |
| Occupancy artificially low at the start of the data | First 30 days excluded |
| Efficiency score was 100 for a single department | Normalised against the full-data reference |
| Readmission column `Readmitted 30d` was not recognised, showing 1.06% from a name-match fallback | Column added to the lookup; rate is 0.08% |
| Dashboard and Milestone 2 script defined bed utilization and efficiency differently | One shared module, `scripts/kpi_utils.py` |
| Census counted the discharge day, giving a 97% peak against 92% in Milestone 2 | Patients counted up to, not including, discharge day |

## 6. Known limitations
Synthetic data with little variation between departments, very low readmission, simulated equipment data, no region map.
