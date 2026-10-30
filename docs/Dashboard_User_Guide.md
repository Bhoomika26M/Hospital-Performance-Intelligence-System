# Dashboard User Guide

## Starting the dashboard

From the project folder, run:

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

Open the local URL displayed by Streamlit.

## Navigation

Use the sidebar Navigation control to switch between:

1. Overview
2. Patient Analytics
3. Resource Utilization
4. Data Explorer

The sidebar also contains patient filters and a Reset filters button.

## Patient filters

The Gender and Condition multiselect controls apply to patient-focused pages:

- Overview
- Patient Analytics

They are not applied to resource records because the validated datasets do not contain a reliable patient-to-resource key.

To clear all patient selections, remove the selected values. The relevant patient page displays a warning when no patient records match.

## 1. Overview

The Overview page presents a high-level snapshot:

### KPI cards

- Total Admissions, defined as patient-record count
- Average Length of Stay
- Readmission Rate
- Recovery Rate
- Beds Allocated
- Beds Occupied
- Bed Occupancy Rate
- Staff On-Duty Rate

### Charts

- Patient Outcomes donut chart
- Readmission Status bar chart

The resource snapshot is based on aggregated resource allocation records and should not automatically be interpreted as unique hospital-wide totals.

## 2. Patient Analytics

Patient Analytics responds to the Gender and Condition filters.

### KPI cards

- Total Admissions/patient records
- Average Length of Stay
- Readmission Rate
- Recovery Rate

### Charts and analysis

- Readmission Comparison
- Outcome Comparison
- Patient Stay Distribution histogram
- Average Patient Cost
- Average Patient Cost by Condition

If the filters return no patient records, the page displays a warning instead of rendering patient charts.

## 3. Resource Utilization

Resource Utilization has independent resource filters:

- Bed type
- Staff type
- Equipment type

All resource KPI values and detailed resource charts use the intersection of the selected resource filters.

### KPI cards

- Beds Allocated
- Beds Occupied
- Bed Occupancy
- Staff On-Duty Rate
- Equipment In Use
- Equipment Utilization

Rates display `N/A` when the relevant denominator is zero.

### Charts

- Bed Allocation and Occupancy by Bed Type
- Top 10 Hospitals by Allocated Beds
- Staff Allocation and On-Duty Counts
- Equipment Allocation and Utilization
- Monthly Resource Allocation Records
- Resource Capacity Not Currently in Use

### Resource notes

- Available capacity is calculated as allocated minus occupied, on-duty, or in-use values.
- Missing numeric resource values are treated as zero in aggregate calculations.
- Monthly trends are sums of allocation records, not admissions, discharges, daily census, or unique hospital-wide totals.
- Surge status is reported as a resource-record indicator.
- Department analytics are not generated because no reliable department field exists.

If all resource filter selections are empty, the page displays a warning and omits the detailed charts.

## 4. Data Explorer

Select one of:

- Patient Data
- Resource Data
- KPI Summary

The page displays:

- Row count
- Column count
- Missing-value count
- A configurable preview of 10, 25, 50, or 100 rows
- An expandable full-record view

Use **Download selected data as CSV** to export the currently selected dataset. The export is generated from the selected DataFrame and does not modify the source workbook.

## Reading the charts

Charts use the dashboard's dark Plotly styling. Hover over chart marks for values. Legends and axis labels identify the plotted measures.

Resource charts use allocation-record data. Patient charts use the filtered patient analysis data.

## Data limitations to keep in mind

The dashboard does not show verified:

- Admission-date trends
- Discharge tracking
- Patient movement
- Daily census
- Peak patient load
- Department-level patient or resource analytics

These features require fields that are not present in the validated datasets.

