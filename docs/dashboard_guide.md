# Dashboard Guide

Run: `python -m streamlit run dashboard/app.py`

## Sidebar (all pages):
 Provides page navigation, a dark/light theme toggle, filters for date range, department, admission type, region and hospital, a total-bed-capacity setting, a reset button, and a CSV download of the filtered data. Filters are shared across pages, so selections remain consistent when navigating between dashboard pages.
## 1. Hospital Overview
Six KPI cards with change vs the previous period (admissions, occupancy, ALOS, readmission, peak bed utilization, discharges). Monthly trends, admissions by type, department and region, discharges vs admissions, top hospitals. Read it first to see whether volume or stay length is changing.

## 2. Patient Flow
Admissions vs discharges by month, length-of-stay distribution, weekday x month heatmap, daily patients in hospital with the peak day marked, and a Sankey from admission type to department. Use it to find peak days and busy weekdays.

## 3. Department Analytics
Volume, ALOS, readmission rate, efficiency score, admissions per bed and per doctor. Use it to compare departments and spot the ones with the highest load per bed or doctor.

## 4. Resource Utilization
Bed utilization and available beds by department, capacity planning notes (red at 100% or more, orange at 90% or more, green below 60%), staffing mix, patients per staff member, and simulated equipment usage.
