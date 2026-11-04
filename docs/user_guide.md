# Aegis.dv – End-User Operational Guide

**Product:** Aegis.dv – Hospital Operations & Patient Analytics Dashboard  
**Developer Attribution:** Ananya Biju (Infosys Springboard Internship)  
**Intended Roles:** Hospital Executives, Medical Directors, Clinical Operations Analysts, Tableau Administrators  

---

## 1. Getting Started

Aegis.dv can be consumed through three primary delivery channels:
1. **Interactive Web Companion:** Open `dashboard/companion/index.html` in any modern web browser for immediate interactive exploration.
2. **Tableau Desktop / Tableau Public:** Open `dashboard/documentation/build_guide.md` and connect to `data/processed/Aegis_Hospital_Extract.hyper` or `data/processed/hospital_final_dataset.xlsx`.
3. **Storyboard Layout PDF:** Open `dashboard_storyboard.pdf` to review the architectural wireframes and container layouts in both dark and light modes.

---

## 2. Navigating the Interface

### Navigation Rail (Left Sidebar)
* Click **🏥 Hospital Overview** to view overall enterprise volume, throughput, and 30-day readmissions.
* Click **🔄 Patient Flow** to analyze intake routes, stay duration distributions, and discharge placements.
* Click **📊 Department Analytics** to benchmark service line throughput, acuity, and quality.
* Click **⚡ Resource Utilization** to review unit bed capacity, staffing ratios, and bottleneck warnings.
* Click **🌙 Dark Mode / ☀️ Light Mode** to switch between visual themes.

---

## 3. Interpreting Key Indicators

* **Length of Stay Skewness:** A hospital's average length of stay (4.40 days) is almost always higher than its median (4.00 days) due to a long tail of acute, complex patients (stays of 10–14 days). Always examine both metrics together.
* **CMS Readmission Quality:** The Centers for Medicare & Medicaid Services (CMS) 30-day readmission metric (11.34%) excludes in-hospital mortality events (1,652 expired stays) because patients who did not survive their index hospitalization cannot be at risk of readmission.
* **Workload vs Occupancy:** Total Patient-Days (447,362 days) represents authentic acute care workload delivered. Bed occupancy percentage on Dashboard 4 is modeled from synthetic reference telemetry in compliance with Section 3 data ethics.

---

## 4. Troubleshooting & FAQ

* **Why does a department show "Low Sample (<30)"?**  
  To prevent misleading statistical conclusions, departments with fewer than 30 discharges are flagged. You can adjust this threshold using the `p_Min_Sample_Size` parameter.
* **How can I export the underlying data?**  
  Use `data/processed/hospital_cleaned.csv` for raw flat analysis or `data/processed/hospital_final_dataset.xlsx` for multi-tab Excel workbooks.

