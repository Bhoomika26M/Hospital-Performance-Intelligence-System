# Testing Report

## Scope and execution status

This report records source-level inspection of the Streamlit page scripts and data files. No Streamlit app session, Tableau workbook, or interactive dashboard test was run while preparing this documentation. Therefore runtime, visual, filter, navigation, download, and cross-filter behavior remain **pending** unless specifically noted as static source inspection.

The expected Tableau packaged workbook `MedTrack_DV.twbx` was not present in the repository at inspection time. Tableau testing cannot proceed until the workbook is supplied.

## Test cases

| ID | Area | Test case | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| T-01 | Dashboard functionality | Launch `streamlit run app.py` with the project datasets available. | App starts without errors and renders the home page and dashboard controls. | Not executed; no runtime result recorded. | Pending |
| T-02 | Dashboard functionality | Open Hospital Overview, Patient Flow, Department Analytics, and Resource Utilization. | Each page renders its documented KPIs, charts, tables, and unavailable-metric notices. | Source files for the four Streamlit pages were inspected; interactive rendering was not tested. | Pending |
| T-03 | KPI | Compare admission count and average length of stay to calculations from the selected source rows. | Counts use records rather than unique people; average stay uses valid `length_of_stay` records. | Not executed in the app. | Pending |
| T-04 | Filter | Change department and condition filters on Hospital Overview. | Filtered KPIs, tables, and applicable charts update consistently. | Filter widgets and filtered dataframe logic exist in source. Runtime response was not tested; the standalone donut chart uses the unfiltered dataframe. | Pending |
| T-05 | Filter | Change admission type and condition filters on Patient Flow. | Filtered KPIs, monthly charts, table, and download reflect selected values. | Filter widgets and filtered dataframe logic exist in source. Runtime response was not tested; the Plotly histogram and box plot use the unfiltered dataframe. | Pending |
| T-06 | Filter | Select and clear departments on Department Analytics and Resource Utilization. | Department-level KPIs, charts, tables, and downloads reflect the selection, including empty-selection behavior. | Department multiselect logic exists in source. Runtime response and empty-selection behavior were not tested. | Pending |
| T-07 | Filter | Change the App page admission-date range. | App page records and date-dependent summaries respect the selected inclusive range. | Date widget and filtered dataframe logic exist in `home.py`. Runtime behavior was not tested. | Pending |
| T-08 | Navigation | Use top navigation to switch among App and the four named pages. | Each destination opens and displays the intended page. | `app.py` statically registers all five Streamlit pages with `st.navigation`; browser navigation was not tested. | Pending |
| T-09 | Interaction | Use chart selections, tooltips, and any cross-filter actions in the Tableau dashboards. | Interactions behave according to the Tableau workbook specification. | Workbook `MedTrack_DV.twbx` was not found; no Tableau interactions could be inspected or tested. | Pending |
| T-10 | Interaction | Download overview, flow, department, and resource CSV outputs after applying filters. | Download starts and contains the corresponding selected data/summary. | Download buttons and CSV serialization are present in source. Download behavior and content were not tested. | Pending |
| T-11 | Metric availability | Verify original-data occupancy/readmission indicators are not represented as measured source values. | Original-data occupancy/readmission remain unavailable; supplemental synthetic metrics are visibly identified as demonstration data. | KPI summary marks source occupancy/readmission unavailable; Resource Utilization displays occupancy unavailable. App pages do not load supplemental files. Visual labeling at runtime was not tested. | Pending |
| T-12 | Data limitation | Verify staff allocation and equipment utilization are not claimed from doctor-name or room-number fields. | Documentation and dashboard labels distinguish listed records from measured allocation/utilization. | Source has listed-doctor ratios and room information but no staff allocation or equipment-use measurements. No dashboard runtime check was performed. | Pending |

## Static inspection notes

- The app navigation registration and Streamlit controls/charts described in [dashboard_documentation.md](dashboard_documentation.md) are present in the checked-in Python source.
- Some standalone Plotly charts use the unfiltered dataframe: the Hospital Overview department donut, and the Patient Flow length-of-stay histogram and box plot. Confirm whether that behavior is intended before claiming every chart responds to filters.
- The Resource Utilization page does not read `milestone3_data/daily_occupancy.csv`; its occupancy and bed-utilization cards remain unavailable.
- The source pages do not read the synthetic patient readmission or transfer files.
- The repository includes no Tableau workbook to test. No test in this report should be interpreted as a passed end-to-end dashboard test.

## Recommended completion checks

1. Supply `MedTrack_DV.twbx`, open it in Tableau, and compare its sheets, navigation, filters, and actions with the dashboard reference.
2. Run the Streamlit app and execute T-01 through T-08 and T-10 through T-12 in a browser, recording observed results and evidence.
3. Resolve the noted chart/filter scope differences or explicitly document them as intentional.
4. Retest any changes and update each case's actual result and status.



## Milestone 4 – Testing and Validation

### 1. KPI Validation

Independent Python validation was performed using
hospital_cleaned.csv.

Results:
- Total admissions: 54,966 – PASS
- Average length of stay: 15.50 days – PASS
- Negative length-of-stay records: 0 – PASS
- Department admissions total: 54,966 – PASS

### 2. Healthcare Metrics Validation

Supplementary datasets were independently inspected
and validated.

- Daily occupancy records: 87,696
- Synthetic readmission records: 4,522
- Synthetic transfer records: 936
- Average synthetic occupancy: 69.88%
- Synthetic readmission flags: 548
- Synthetic flagged-record percentage: 12.12%

Bed calculations, occupancy rates, duplicate checks,
readmission flags and transfer relationships passed
the implemented validation checks.

### 3. Tableau Dashboard Testing

Four dashboards were visually inspected:

1. Hospital Overview
2. Patient Flow
3. Department Analytics
4. Resource Utilization

Hospital Overview:
- Dashboard loading: Passed
- Department filter: Passed
- Date filter: Passed
- Navigation: Passed

Patient Flow:
- Four expected charts visually verified.
- Department and date filters are not provided.
- Cross-chart filtering was not available.

Department Analytics:
- Four expected charts visually verified.
- Department filter showed inconsistent behaviour
  during testing and requires further verification.

Resource Utilization:
- Four expected charts visually verified.

### 4. Patient Flow Validation

Department-wise incoming transfer counts were compared
with the supplementary transfer dataset.

All six department counts matched, with 936 total
transfers.

### 5. Pending Issues

The synthetic readmission KPI differs between Python
and Tableau (12.12% versus 36.01%).

This discrepancy requires investigation before the
readmission KPI can be marked accurate.

Department Analytics filter behaviour also requires
final verification.

### 6. Testing Conclusion

Core KPI calculations and supplementary dataset
consistency checks passed.

All four dashboards were visually inspected.

The project has completed substantial testing, but
final QA closure remains pending until the outstanding
issues are investigated and documented.
