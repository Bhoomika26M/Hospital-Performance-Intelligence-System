# Milestone 3 – Dashboard Development

## 1. Project Overview

MedTrack is a Hospital Operations and Patient Analytics Dashboard developed using Python and Streamlit.

The dashboard provides interactive visualizations and insights into hospital admissions, patient flow, clinical analytics and resource utilization.

## 2. Dashboard Modules

The dashboard consists of four main sections:

### 1. Hospital Overview
- Total hospital admissions
- Average length of stay
- Medical condition analysis
- Admission type distribution

### 2. Patient Flow Analysis
- Monthly admission trends
- Patient outcome analysis
- Emergency vs OPD admissions
- Patient stay analysis

### 3. Department and Clinical Analytics
- Admissions by medical condition
- Top 10 doctors by patient admissions
- Average patient stay by medical condition
- Clinical workload analysis

### 4. Resource Utilization
- Room assignment frequency
- ICU stay distribution
- Hospital stay distribution
- Resource utilization analysis

## 3. Technologies Used

- Python
- Streamlit
- Pandas
- Plotly

## 4. Dataset

The project uses hospital healthcare datasets.

Data processing includes:
- Data cleaning
- Handling missing values
- Removing duplicate records
- Generating cleaned datasets
- KPI generation

## 5. Project Structure

```text
Milestone_3/
│
├── dashboard/
│   ├── app.py
│   └── cleaned_data/
│
├── screenshots/
│
├── documentation/
│
└── README.md
```

## 6. How to Run the Dashboard

1. Install the required Python packages.
2. Open the project directory in VS Code.
3. Open the terminal.
4. Run:

```bash
streamlit run app.py
```

5. Open the local URL displayed in the terminal.

## 7. Results

The dashboard successfully displays hospital performance indicators through interactive charts, visualizations and KPI summaries.

It helps users understand hospital admission patterns, patient outcomes, clinical workload and resource utilization.

## 8. Limitations

Some measurements, such as actual bed occupancy and department-wise efficiency, cannot be reliably