# QA checklist

Run `python scripts/validate_kpis.py` for the first block. Tick the manual block yourself in a browser.

## Automated (script)
- [x] Patient-days match an independent calculation (20 random department-months)
- [x] Occupancy and bed-utilization formulas
- [x] Total admissions match the cleaned data
- [x] Average length of stay per department
- [x] Every readmission has an earlier matching stay
- [x] Missing values < 2% · raw completeness > 95%
- [x] No negative billing / length of stay · no duplicates
- [x] Department names standardised
- [x] Dashboard holds every cleaned record
- [x] Dashboard opens in a headless browser with no errors

## Manual (you)
- [ ] Each of the 4 pages opens
- [ ] From/To filter changes the KPI cards (try one year)
- [ ] Department filter changes the numbers; Reset restores them
- [ ] Clicking a row in the Departments table sets the department filter
- [ ] Works on a phone-width window
- [ ] Dark mode looks readable
- [ ] Tableau: filters and navigation buttons work on all four dashboards
- [ ] Tableau: three KPI numbers match the Python results (see Testing Report)
