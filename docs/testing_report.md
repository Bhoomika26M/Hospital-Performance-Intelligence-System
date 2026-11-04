# Testing Report

## Scope and execution status

This report records validator and Streamlit AppTest runs for KPI standardization. AppTest checked page rendering and exceptions; it is not browser/visual testing and does not establish that interactive behavior works in a browser.

`MedTrack_DV.twbx` is an optional legacy Tableau workbook, not required for the Streamlit implementation. It was not changed or tested in Tableau.

## Test cases

| ID | Area | Test case | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| T-01 | Dashboard functionality | Launch `streamlit run app.py` with the project datasets available. | App starts without errors and renders the home page and dashboard controls. | Not executed; no runtime result recorded. | Pending |
| T-02 | Dashboard functionality | Render all four Streamlit dashboard page scripts with AppTest. | Pages render without app exceptions. | Hospital Overview: 7 Plotly charts, 5 metrics; Patient Flow: 9 charts, 5 metrics; Department Analytics: 10 charts, 9 metrics; Resource Utilization: 19 charts, 18 metrics. No AppTest exceptions. | Pass (AppTest only) |
| T-03 | KPI | Compare admission count and average length of stay to calculations from the selected source rows. | Counts use records rather than unique people; average stay uses valid `length_of_stay` records. | Not executed in the app. | Pending |
| T-04 | Filter | Change department and condition filters on Hospital Overview. | Filtered KPIs, tables, and applicable charts update consistently. | Filter widgets and filtered dataframe logic exist in source. Runtime response was not tested; the standalone donut chart uses the unfiltered dataframe. | Pending |
| T-05 | Filter | Change admission type and condition filters on Patient Flow. | Filtered KPIs, monthly charts, table, and download reflect selected values. | Filter widgets and filtered dataframe logic exist in source. Runtime response was not tested; the Plotly histogram and box plot use the unfiltered dataframe. | Pending |
| T-06 | Filter | Select and clear departments on Department Analytics and Resource Utilization. | Department-level KPIs, charts, tables, and downloads reflect the selection, including empty-selection behavior. | Department multiselect logic exists in source. Runtime response and empty-selection behavior were not tested. | Pending |
| T-07 | Filter | Change the App page admission-date range. | App page records and date-dependent summaries respect the selected inclusive range. | Date widget and filtered dataframe logic exist in `home.py`. Runtime behavior was not tested. | Pending |
| T-08 | Navigation | Use top navigation to switch among App and the four named pages. | Each destination opens and displays the intended page. | `app.py` statically registers all five Streamlit pages with `st.navigation`; browser navigation was not tested. | Pending |
| T-09 | Interaction | Use chart selections, tooltips, and cross-filter actions in the optional legacy Tableau workbook. | Workbook interactions behave as designed. | Not tested in Tableau; the workbook is legacy/optional. | Pending |
| T-10 | Interaction | Download overview, flow, department, and resource CSV outputs after applying filters. | Download starts and contains the corresponding selected data/summary. | Download buttons and CSV serialization are present in source. Download behavior and content were not tested. | Pending |
| T-11 | Metric availability | Verify original-data occupancy/readmission indicators are not represented as measured source values. | Original-data occupancy/readmission remain unavailable; synthetic values are identified as demonstrations and kept separate. | Source KPI summary marks original measures unavailable; relevant Streamlit pages load the synthetic datasets separately. AppTest rendered without exceptions. Browser label visibility was not tested. | Pass (source/AppTest) |
| T-12 | Data limitation | Verify staff allocation and equipment utilization are not claimed from doctor-name or room-number fields. | Documentation and dashboard labels distinguish listed records from measured allocation/utilization. | Source has listed-doctor ratios and room information but no staff allocation or equipment-use measurements. No dashboard runtime check was performed. | Pending |

## Validator results

- `validate_hospital_kpis.py`: admissions 54,966, average length of stay 15.50 days, zero negative/missing stays, department total 54,966; all printed checks passed.
- `validate_healthcare_metrics.py`: **27 checks passed, 0 failed**. Occupancy denominators were 7,141,743 total beds and 87,696 non-null daily rates. Readmission denominators were 4,522 all synthetic admissions and 1,522 records with a non-null previous-admission date.
- `validate_resource_data.py`: **24 checks passed, 0 failed** for staff and equipment datasets.

### Standard synthetic KPI results

| KPI | Formula | Denominator | Result |
|---|---|---:|---:|
| Weighted Bed Occupancy Rate | `SUM(occupied_beds) / SUM(total_beds) * 100` | 7,141,743 total beds | 69.87% |
| Average Daily Occupancy Rate | `AVERAGE(occupancy_rate) * 100` | 87,696 non-null rates | 69.88% |
| Overall Synthetic Readmission Rate | `SUM(readmission_flag) / all synthetic admission records * 100` | 4,522 records | 12.12% |
| Readmission Percentage Among Records with Previous Admission | Flags in non-null previous-date subset / records in that subset * 100 | 1,522 records | 36.01% |

Both readmission rates have 548 flagged records. Their denominators differ, so 12.12% and 36.01% are distinct metrics, not competing results.

## Test limitations

- No browser/visual testing, interactive filter testing, downloads, or navigation switching was performed for this update.
- The AppTest results establish rendering without exceptions only; they do not prove browser-level chart interactions or visual layout.
- The optional legacy Tableau workbook was not tested. Older workbook calculations may use the previous-admission subset denominator; Streamlit uses the overall all-record denominator for its overall KPI.

## Recommended completion checks

1. If Tableau remains in the delivery scope, verify the optional legacy workbook's denominator labels and data-source paths in Tableau.
2. Perform separate browser checks for navigation, filters, charts, and downloads if browser-level QA is required.
