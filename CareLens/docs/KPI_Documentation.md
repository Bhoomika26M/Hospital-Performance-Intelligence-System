# KPI definitions

All KPIs are calculated in `scripts/generate_hospital_kpis.py` per department per month, and again in the dashboard for whatever filters you choose.

| KPI | Formula | Notes |
|---|---|---|
| Total Admissions | count of admissions in the period | |
| Occupancy Rate | patient-days ÷ (licensed beds × days in period) | patient-day = one patient in a bed for one night |
| Average Length of Stay | mean of (discharge date − admission date) | by admission month |
| Readmission Rate | admissions within 30 days of the same patient's last discharge ÷ all admissions | patient = same name + gender + blood type |
| Bed Utilization Rate | patient-days ÷ (staffed beds × days in period) | staffed beds are fewer than licensed beds, so this is higher than occupancy |
| Department Efficiency Score | 40% stay-length score + 30% bed-use score + 30% satisfaction score | 0–100, see below |

**Efficiency score parts**
- Stay-length score = target stay ÷ actual stay × 100 (capped at 100)
- Bed-use score = 100 − |bed utilization − 85%| × 400 (best when utilization is near 85%)
- Satisfaction score = satisfaction ÷ 5 × 100

I picked the weights myself (stay length matters most to patient flow). They can be changed in `generate_hospital_kpis.py`.

**Extra measures:** discharges, peak census (most patients in beds on one day), equipment utilization (hours used ÷ hours available), nurses per 10 patients.
