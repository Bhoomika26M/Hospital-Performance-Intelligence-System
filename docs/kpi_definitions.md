# KPI Definitions

The KPI calculations are implemented in `scripts/kpi_utils.py`. The dashboard, KPI generation script, and validation tests use these calculations to maintain consistency.

| KPI | Definition |
|-----|-----------|
| Total admissions | Count of records whose admission date falls in the selected range. |
| Discharges | Count of records whose discharge date falls in the selected range. This may be lower than admissions because some patients remain in hospital at the end of the selected period. |
| Daily in-house patients (census) | A patient counts from the admission day up to, but not including, the discharge day. |
| Occupancy rate | Mean daily in-house patient count divided by total beds, multiplied by 100. The first 30 days of the data are excluded as a warm-up period. |
| Bed utilization (peak) | Highest daily in-house patient count in the selected range divided by total beds, multiplied by 100. |
| Average length of stay (ALOS) | Mean of `Length of Stay` in days for admissions in the selected range. |
| Readmission rate | |The flag is based on a previous discharge 0-30 days before the admission, using the available patient attributes for matching.
| Department efficiency score | `100 x (1 - (normalised ALOS + normalised readmission rate) / 2)`. Min-max normalised across departments using the full dataset and clipped to 0–100. Higher is better. |
| Admissions per bed / per doctor | Department admissions in the selected period divided by the number of beds allocated or doctors, as recorded in `department_resources.csv`. |
| Total beds | Sum of `Beds Allocated` in `department_resources.csv`, currently 600. The dashboard allows the capacity to be edited in the sidebar. |
| Change vs previous period | Comparison with the immediately preceding window of the same length, shown only when the required comparison data is available. |

## Full-range values (8 May 2019 – 7 May 2024)

- Total admissions: 54,966
- Discharges: 54,438
- Occupancy rate: 77.73%
- Peak bed utilization: 92.0% (552 of 600 beds)
- Average length of stay: 15.5 days
- Estimated readmission rate: 0.082% (45 flagged admissions)

The readmission rate should be interpreted as an estimate, not a definitive clinical readmission rate, because patient matching relies on available attributes rather than a unique patient identifier.