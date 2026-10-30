# MedTrack_DV Dashboard Testing Report

## 1. Executive summary

Milestone 4 Module 7 testing was completed against the existing Streamlit dashboard using the current root-level `app.py`. The application code, datasets, Excel workbook, dependencies, and configuration were not modified.

The validated KPI summary matches independently calculated values from the source CSV datasets for all seven KPI rows. All four Streamlit pages loaded successfully. Patient and resource filters passed independently and in combination. Empty selections, missing numeric values, zero denominators, invalid dates, charts, navigation, and CSV download controls were exercised successfully.

No application defect requiring a code change was identified.

## 2. Scope and inspected project assets

Inspected:

- `app.py` - active Streamlit entry point
- `README.md`
- `scripts/generate_hospital_kpis.py`
- `scripts/validate_kpis.py`
- `data/hospital data analysis.csv`
- `data/hospital-resource-allocation-records.csv`
- `data/hospital_final_dataset.xlsx`
- Other available CSV datasets under `data/`
- Existing `docs/` and `scripts/` assets

No existing automated test files were present. Testing was performed with:

- The existing `scripts/validate_kpis.py`
- Independent Pandas calculations
- Streamlit `AppTest`
- A live Streamlit health check
- Controlled in-memory frames for edge cases

## 3. Independent KPI verification

The source datasets were loaded independently from:

- `data/hospital data analysis.csv`
- `data/hospital-resource-allocation-records.csv`

The generated workbook was read from:

- `data/hospital_final_dataset.xlsx`

| KPI | Independent value | Workbook value | Result |
|---|---:|---:|---|
| Total Admissions | 984 | 984 | PASS |
| Average Length of Stay | 37.663617886179 | 37.663617886179 | PASS |
| Readmission Rate (%) | 26.829268292683 | 26.829268292683 | PASS |
| Average Patient Cost | 8367.479674796748 | 8367.479674796748 | PASS |
| Recovery Rate (%) | 60.060975609756 | 60.060975609756 | PASS |
| Bed Occupancy Rate (%) | 90.713706407137 | 90.713706407137 | PASS |
| Staff On-Duty Rate (%) | 93.888710196205 | 93.888710196205 | PASS |

The workbook values matched the independent calculations exactly within the test tolerance. No unsupported KPI accuracy percentage is claimed.

## 4. Data-validation evidence

### Patient analysis dataset

- 984 records
- 0 duplicate rows
- 0 missing values
- Readmission values: 720 No and 264 Yes
- Outcome values: 591 Recovered and 393 Stable
- Length of stay: minimum 1; no non-positive values
- No admission-date field
- No discharge-date field
- No department field

### Resource allocation dataset

- 200 records
- 0 duplicate rows
- 0 missing values
- 0 negative values in checked resource measures
- 0 records with occupied beds greater than allocated beds
- 0 repeated `hospital_id` + `allocation_date` rows
- 200 of 200 valid `allocation_date` values
- Zero denominators exist and are expected:
  - 1 zero `beds_allocated`
  - 9 zero `staff_allocated`
  - 13 zero `equipment_allocated`

### Other available data

`healthcare_data.csv` contains 500 records and a `Follow_Up_Date`, but it is not the validated patient-analysis source for the dashboard KPIs. It contains 95 missing values and does not provide admission, discharge, department, movement, or resource-linkage fields.

## 5. Streamlit regression results

| Page | Result | Details |
|---|---|---|
| Overview | PASS | 2 Plotly charts and 8 metrics rendered |
| Patient Analytics | PASS | 4 Plotly charts and 5 metrics rendered |
| Resource Utilization | PASS | 6 Plotly charts and 6 metrics rendered |
| Data Explorer | PASS | Dataset selector, preview, metrics, and download control rendered |

The live Streamlit application started successfully. The health endpoint returned:

```text
HTTP 200
ok
```

## 6. Filter results

### Patient filters

The Gender and Condition filters were each tested independently and together on Patient Analytics. The displayed total patient-record KPI matched independent filtered Pandas counts.

Empty Gender and Condition selections displayed the existing no-record warning and did not raise an application exception.

### Resource filters

The Bed type, Staff type, and Equipment type filters were each tested independently. Two combined filter combinations were also tested.

For every case:

- Beds Allocated matched the filtered source sum.
- Beds Occupied matched the filtered source sum.
- Bed Occupancy matched the filtered ratio.
- Staff On-Duty Rate matched the filtered ratio.
- Equipment In Use matched the filtered source sum.
- Equipment Utilization matched the filtered ratio.
- All six detailed resource charts rendered for non-empty selections.

Empty resource selections displayed:

```text
No resource records match the selected filters.
```

No detailed charts were rendered for the empty selection, and no exception occurred.

## 7. Calculation and edge-case results

### Utilization formulas

Verified formulas:

```text
Bed occupancy = beds_occupied / beds_allocated * 100
Staff on-duty rate = staff_on_duty / staff_allocated * 100
Equipment utilization = equipment_in_use / equipment_allocated * 100
```

### Missing numeric values

The resource helper uses numeric coercion followed by `fillna(0)`. Controlled tests confirmed that missing numeric values are treated as zero in aggregate calculations.

### Zero denominators

The helper returns no numeric rate when the denominator is zero. The display formatter renders the result as `N/A`. Controlled tests confirmed safe behavior for beds, staff, and equipment.

### Available capacity

Verified calculations:

```text
Available beds = beds_allocated - beds_occupied
Available staff = staff_allocated - staff_on_duty
Available equipment = equipment_allocated - equipment_in_use
```

### Allocation trends

The trend logic:

1. Parses `allocation_date` with coercion.
2. Drops invalid dates.
3. Groups valid records by month.
4. Aggregates beds and equipment measures.

Controlled tests confirmed invalid dates are excluded. The no-valid-date branch displays:

```text
No valid allocation dates are available for trend analysis.
```

These are resource allocation-record trends only. They are not admission, discharge, movement, or census trends.

## 8. Charts and CSV downloads

All expected Plotly chart counts rendered on the corresponding pages.

Data Explorer download controls were tested for:

- Patient Data
- Resource Data
- KPI Summary

Each control clicked successfully without an exception. Independent CSV serialization produced non-empty outputs:

| Dataset | Rows | Serialized size |
|---|---:|---:|
| Patient Data | 984 | 71,750 bytes |
| Resource Data | 200 | 39,679 bytes |
| KPI Summary | 7 | 277 bytes |

## 9. Issues and warnings

### Application defects

No application defects were found during this audit. No minimal code fix is recommended at this time.

### Non-blocking warning

Streamlit emitted deprecation warnings for `use_container_width`, recommending `width="stretch"` or `width="content"` in a future compatibility update. This was not changed during the audit because the task prohibited application changes and the warning did not affect runtime behavior.

### Test-harness note

An initial exploratory download-payload check incorrectly expected the Streamlit `AppTest` download widget value to contain raw bytes. The widget exposes a boolean click state in this testing API. The corrected test clicked each control, verified no exception, and independently verified the generated CSV serialization. This was a test-harness issue, not an application failure.

## 10. Unsupported analytics confirmed

The available validated datasets do not support:

- Reliable admission-date trends
- Discharge tracking
- Patient movement analysis
- Daily patient census
- Verified peak patient load
- Department volume
- Department readmission
- Department efficiency
- Patient-to-resource linkage

No fabricated values were introduced to represent these unsupported analytics. fabricated values were introduced during testing.

## 11. Files changed

Created:

- `docs/QA_Checklist.md`
- `docs/Dashboard_Testing_Report.md`

Not changed:

- `app.py`
- Any CSV or Excel dataset
- KPI generation or validation scripts
- Dependencies
- Configuration

No commit or push was performed.

## 12. Milestone 4 progress and Module 8 remaining work

### Module 7 status

**Complete for the current validation scope.** The current application is functionally verified across KPI calculations, data validation, page regression, filters, empty states, edge cases, charts, navigation, and downloads.

### Module 8 remaining work

Module 8 should focus on delivery readiness:

1. Review and approve the two QA documents.
2. Decide whether to address the non-blocking `use_container_width` deprecation warnings in a separate compatibility change.
3. Update the minimal project documentation or README with the validated run/test commands if desired.
4. Perform a final clean-worktree review, excluding pre-existing untracked PDF/storyboard assets.
5. Commit the approved application and QA documentation changes.
6. Push the approved commit to the current branch only after explicit approval.
