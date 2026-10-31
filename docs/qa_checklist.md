# QA Checklist
| # | Test | Page(s) | Expected | Pass |
|---|------|---------|----------|------|
| 1 | Date range: full range | All | KPIs equal docs/kpi_validation.csv | [x] |
| 2 | Date range: one calendar year | All | Charts update, deltas appear | [x] |
| 3 | Date range: single day | All | No crash | [x] |
| 4 | Department filter: one department | All | Charts update, efficiency not all 100 | [x] |
| 5 | Department filter: none selected | All | Treated as "All" | [x] |
| 6 | Admission type filter | All | Charts update | [x] |
| 7 | Region filter | All | Charts update | [x] |
| 8 | Hospital filter | All | Charts update | [x] |
| 9 | Filters with no matching rows | All | "No records match" warning | [x] |
| 10 | Reset filters button | All | Returns to defaults | [x] |
| 11 | Navigation keeps filters | All | Filters preserved | [x] |
| 12 | Dark / light toggle | All | Readable text and charts in both | [x] |
| 13 | Capacity setting changed | 1, 4 | Occupancy changes | [x] |
| 14 | Download filtered CSV | Sidebar | Row count matches the filter | [x] |
| 15 | Department names match resources file | 4 | No warning shown | [x] |
