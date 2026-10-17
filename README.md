# Hospital-Performance-Intelligence-System
# MedTrack – Hospital Operations & Patient Analytics

## About the Project
MedTrack is a hospital analytics dashboard built with Python, Streamlit, Pandas, and Plotly. It helps visualize patient admissions, length of stay, billing, patient flow, and resource-related metrics.

## Dashboards
1. **Hospital Overview** – Admission trends, average stay, billing, and admission distributions.
2. **Patient Flow** – Monthly admissions and discharges, daily admission patterns, length of stay, and simulated transfers.
3. **Department Analytics** – Admission distribution, length of stay, and billing comparisons across simulated departments.
4. **Resource Utilization** – Monthly workload, admission heatmap, and simulated staffing, bed occupancy, and equipment metrics.

## Technologies Used
- Python
- Pandas
- Streamlit
- Plotly
- Excel and CSV datasets

## Setup and Run

1. Clone the repository and open the project folder.
2. Install the required libraries:

   ```bash
   pip install pandas streamlit plotly openpyxl
   ```

3. Generate the demonstration dataset:

   ```bash
   python scripts/add_demo_resource_columns.py
   ```

4. Run the dashboard:

   ```bash
   python -m streamlit run scripts/hospital_dashboard_app.py
   ```

## Data Note
Patient admission and billing analyses use the supplied dataset. Department assignments, transfer destinations, bed occupancy, staffing, and equipment metrics are simulated for demonstration and must not be treated as actual hospital operational measurements.
data/hospital_dashboard_demo_data.csv is the final datset after adding the demo datas.

## Project Status
Milestone 3 – Interactive hospital analytics dashboard.completed
