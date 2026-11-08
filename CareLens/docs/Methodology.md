# Methodology

## Pipeline
Collect → Clean → KPIs → Dashboard → Test → Document.

## Cleaning decisions
| Problem found | What I did | Count |
|---|---|---|
| Random capital letters in names | Title case | all rows |
| Duplicate rows | Removed (after fixing capitals) | 534 |
| Negative billing amounts | Replaced with median bill for same condition + admission type, flagged in `billing_fixed` | 106 |
| Blank nurse counts (resource file) | Filled by interpolating between neighbouring months | 2 |
| Department names in different cases (feedback file) | Trimmed and title-cased | ~10% of rows |

## Choices that affect the numbers
1. **Analysis window: Jul 2019 – Apr 2024.** The data begins on 8 May 2019, so patients admitted earlier are missing and the first weeks look empty. The end of the data has the same issue. I only use the full months in between.
2. **Patient-days** are counted from admission day until the day before discharge.
3. **Departments** are grouped from medical conditions (see `Dataset_Sources.md`).
4. **Readmission** uses name + gender + blood type as a stand-in for a patient ID. Only 45 matches were found (about 0.1%). Some of those may be different people with the same name, so treat this KPI as approximate.
5. **Occupancy with an admission-type filter** shows how much of the beds that admission type uses, not the occupancy of a separate ward.

## Limits
- The admissions data is synthetic and almost perfectly evenly spread. Departments, years and admission types look alike, so the dashboards show few strong patterns. A real hospital would show more.
- Beds, staff, equipment and feedback are simulated.
- No cost or outcome data apart from the billing amount and test result.
