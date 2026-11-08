# Dashboard testing report

**Date tested:** 6 Nov 2026  **Tested by:** Harsha

## 1. Data and KPI validation (`validate_kpis.py`)
13 of 13 checks passed → KPI accuracy 100% (target: above 95%). Full output: `validation_output.txt`.

| Check | Result |
|---|---|
| Patient-days vs independent calculation | 20 / 20 cells identical |
| Total admissions (monthly table vs cleaned data) | 53,178 = 53,178 |
| Readmissions with a matching earlier stay | 45 / 45 |
| Missing values after cleaning | 0.000% (limit 2%) |
| Raw data completeness | 100% (limit 95%) |
| Records in dashboard file vs cleaned data | 54,966 = 54,966 |

## 2. Dashboard behaviour (headless browser)
- All four pages opened with no JavaScript errors.
- "Total Admissions" card showed 53,178, the same as pandas.
- Filtering to Oncology + Emergency admissions from Jul 2020 changed the cards (2,248 admissions) as expected.

## 3. Issues found and fixed during testing
1. "Nurses per 10 patients" mixed a per-department nurse count with the hospital-wide census, so it showed 1.0. Fixed to use total nurses for the selected departments.
2. Occupancy-by-month chart with five coloured lines was unreadable. Changed to one combined line.

## 4. Still to check by hand
Tableau workbook interactions and phone layout – see the manual block in `QA_Checklist.md`.
