# Building the Tableau workbook (CareLens.twbx)

Tableau files can only be made in Tableau, so this is the recipe. Use **Tableau Public** (free).
Data to connect: `data/hospital_final_dataset.xlsx` (sheets **Admissions** and **Monthly_KPIs**).

## 0. Connect
1. Tableau Public → Connect → Microsoft Excel → pick the file.
2. Drag **Monthly_KPIs** in. Add **Admissions** as a second table, **do not join** them (keep two separate data sources by dragging the sheets into separate connections) because one is monthly and one is per-patient.
3. Make sure `month` is a Date and `department` is a Dimension.

## 1. Calculated fields (Monthly_KPIs)
```
Occupancy Rate        = SUM([patient_days]) / SUM([licensed_beds] * [days_in_month])
Bed Utilization Rate  = SUM([patient_days]) / SUM([staffed_beds] * [days_in_month])
Avg Length of Stay    = SUM([avg_los_days] * [admissions]) / SUM([admissions])
Readmission Rate      = SUM([readmissions_30d]) / SUM([admissions])
Equipment Utilization = SUM([equipment_hours_used]) / SUM([equipment_hours_available])
```
Check: with no filters, Occupancy should be about 86.4% and Admissions 53,178.

## 2. Sheets to build (one per chart)
| Dashboard | Sheets |
|---|---|
| Hospital Overview | 6 KPI text cards · Admissions by month (line) · Occupancy by month (line + reference line 85%) · Admissions by department (bar) |
| Patient Flow | Admissions vs Discharges (dual line) · Peak census by month · Admissions by weekday (Admissions sheet, `admit_weekday`) · Length of stay bands |
| Department Analytics | Department table (admissions, ALOS, readmission, efficiency) · Efficiency bar · Readmission bar |
| Resource Utilization | Bed utilization by department (reference line 85%) · Equipment utilization · Staffed vs licensed · Satisfaction |

## 3. Look (keep it different and clean)
- Background `#F7F5F1`, text `#1F2933`, one accent green `#2A6F5B`, warning orange `#D9694F`.
- One font (Tableau Book). No gridlines except light horizontal ones. No borders around sheets.
- Short sheet titles in plain words ("How busy was the hospital?").

## 4. Dashboards
New Dashboard → size **Automatic** → drag sheets in using tiled layout.

## 5. Integration (Module 6 requirement)
- **Global filters:** on a filter card → Apply to Worksheets → *All Using This Data Source*. Filters: Month, Department.
- **Navigation:** add 4 *Navigation* buttons (Dashboard → Objects → Navigation), one per dashboard, with the same position on each.
- **Dashboard actions:** Dashboard → Actions → Add Action → *Filter*: source = Department table, run on *Select*, target = all other sheets.
- **Parameter action (optional):** create a Parameter "Metric" (Admissions / Occupancy / ALOS) and use it in a calculated field that changes the line chart.

## 6. Save and publish
File → Save to Tableau Public As… → then File → Export As Packaged Workbook → save as `dashboard/CareLens.twbx`.
Put the public link in the README.
