# MedTrack_DV Milestone 4 QA Checklist

**Scope:** Module 7 - Testing and Validation  
**Application:** Streamlit root-level `app.py`  
**Branch:** `tina-kurian`  
**Test date:** 2026-10-31  

## Test status legend

- **PASS:** Executed and verified successfully.
- **LIMITATION:** The requested behavior is not supported by the validated data or test surface.
- **WARNING:** The test passed, but the application emitted a non-blocking warning.

## Repository and source audit

| Check | Status | Evidence |
|---|---|---|
| Root Streamlit entry point identified | PASS | `app.py` |
| Validated KPI generation script inspected | PASS | `scripts/generate_hospital_kpis.py` |
| Existing validation script inspected and executed | PASS | `scripts/validate_kpis.py` exited successfully |
| Existing automated test files found | LIMITATION | No files matching test patterns were present |
| Validated Excel workbook preserved | PASS | `data/hospital_final_dataset.xlsx` was read only |
| Application code, data, dependencies, and configuration preserved during audit | PASS | No audit changes made to these areas |

## KPI accuracy

| KPI | Status | Independent verification |
|---|---|---|
| Total Admissions | PASS | `len(patient dataset)` = 984; workbook = 984 |
| Average Length of Stay | PASS | Independent mean = 37.663617886179; workbook matches exactly |
| Readmission Rate | PASS | 264 Yes / 984 = 26.829268292683%; workbook matches exactly |
| Average Patient Cost | PASS | Independent mean = 8367.479674796748; workbook matches exactly |
| Recovery Rate | PASS | 591 Recovered / 984 = 60.060975609756%; workbook matches exactly |
| Bed Occupancy Rate | PASS | 8948 / 9864 = 90.713706407137%; workbook matches exactly |
| Staff On-Duty Rate | PASS | 2919 / 3109 = 93.888710196205%; workbook matches exactly |

No estimated KPI accuracy percentage is reported. The comparisons above were exact within the verification tolerance.

## Healthcare and source-data validation

| Check | Status | Result |
|---|---|---|
| Patient record count | PASS | 984 |
| Patient duplicate rows | PASS | 0 |
| Patient missing values | PASS | 0 |
| Readmission values | PASS | 720 No, 264 Yes; no invalid values |
| Outcome values | PASS | 591 Recovered, 393 Stable |
| Length-of-stay validity | PASS | Minimum 1; no non-positive values |
| Resource record count | PASS | 200 |
| Resource duplicate rows | PASS | 0 |
| Resource missing values | PASS | 0 |
| Resource negative numeric values | PASS | 0 negative cells |
| Occupied beds above allocation | PASS | 0 rows |
| Hospital/date duplicate key rows | PASS | 0 |
| Resource allocation dates | PASS | 200 of 200 parse successfully |
| Zero bed allocations | PASS | 1 record; guarded by application logic |
| Zero staff allocations | PASS | 9 records; guarded by application logic |
| Zero equipment allocations | PASS | 13 records; guarded by application logic |

## Streamlit page regression

| Page | Status | Verified behavior |
|---|---|---|
| Overview | PASS | Loaded without exception; 2 Plotly charts and 8 metrics rendered |
| Patient Analytics | PASS | Loaded without exception; 4 Plotly charts and 5 metrics rendered |
| Resource Utilization | PASS | Loaded without exception; 6 Plotly charts and 6 metrics rendered |
| Data Explorer | PASS | Loaded without exception; dataset selector, preview, metrics, and download control rendered |

## Filter testing

### Patient filters

| Test | Status | Evidence |
|---|---|---|
| Gender filter independently | PASS | KPI record count matched independently filtered patient data |
| Condition filter independently | PASS | KPI record count matched independently filtered patient data |
| Gender + Condition combination | PASS | KPI record count matched intersection of both filters |
| Empty Gender + Condition selections | PASS | Clear warning displayed; patient charts were not rendered |

### Resource filters

| Test | Status | Evidence |
|---|---|---|
| Bed Type independently | PASS | KPIs and all 6 resource charts used filtered records |
| Staff Type independently | PASS | KPIs and all 6 resource charts used filtered records |
| Equipment Type independently | PASS | KPIs and all 6 resource charts used filtered records |
| Combined resource filters | PASS | Two combinations verified against independent intersections |
| Empty resource selections | PASS | Clear warning displayed; no detailed charts rendered |

## Calculation and edge-case testing

| Test | Status | Evidence |
|---|---|---|
| Bed occupancy percentage | PASS | `beds_occupied / beds_allocated * 100` matched expected values |
| Staff on-duty percentage | PASS | `staff_on_duty / staff_allocated * 100` matched expected values |
| Equipment utilization percentage | PASS | `equipment_in_use / equipment_allocated * 100` matched expected values |
| Available capacity | PASS | Allocated minus occupied/on-duty/in-use values verified |
| Missing numeric resource values | PASS | Coerced values become zero in aggregate helper tests |
| Zero denominators | PASS | Rates render `N/A`; no division error |
| Invalid allocation dates | PASS | Invalid dates are coerced and excluded from monthly grouping |
| No valid allocation dates | PASS | Informational message branch is present and verified |

## Navigation, charts, and downloads

| Check | Status | Evidence |
|---|---|---|
| Sidebar navigation | PASS | All four page selections loaded successfully |
| Plotly chart rendering | PASS | Expected chart counts rendered on all chart pages |
| Patient Data download | PASS | Download control clicked; CSV serialization produced 71,750 bytes |
| Resource Data download | PASS | Download control clicked; CSV serialization produced 39,679 bytes |
| KPI Summary download | PASS | Download control clicked; CSV serialization produced 277 bytes |
| Live Streamlit startup | PASS | `http://127.0.0.1:8503/_stcore/health` returned `200 ok` |

## Warnings and limitations

- Streamlit emitted non-blocking deprecation warnings for `use_container_width`; no runtime error resulted.
- No standalone test suite exists in the repository; the checks in this document were run as targeted audit scripts and Streamlit `AppTest` interactions.
- The patient analysis dataset has no admission or discharge dates.
- The validated datasets do not support verified patient movement, daily census, peak patient load, or department-level analytics.
- Resource monthly trends are allocation-record aggregations, not patient-flow trends.
- Resource totals should not automatically be interpreted as unique hospital-wide totals without a confirmed snapshot grain.
