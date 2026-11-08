# Putting this on GitHub (step by step)

Your team repo already exists (`Hospital-Performance-Intelligence-System`) and each person has their own branch. Work on **your own branch** so you don't overwrite anyone.

```bash
git clone https://github.com/Bhoomika26M/Hospital-Performance-Intelligence-System.git
cd Hospital-Performance-Intelligence-System
git checkout -b harsha            # your branch (use your name)
```

Copy the contents of this project folder into the repo folder, then commit **once per milestone** so the history tells the story:

```bash
# Milestone 1 – data
git add data/raw data/hospital_raw_data.csv data/hospital_cleaned.csv data/resource_cleaned.csv data/feedback_cleaned.csv scripts/config.py scripts/utils.py scripts/make_supporting_data.py scripts/data_collection.py scripts/clean_data.py notebooks
git commit -m "Milestone 1: collect and clean hospital datasets"

# Milestone 2 – KPIs and planning
git add data/hospital_final_dataset.xlsx data/monthly_kpis.csv scripts/generate_hospital_kpis.py dashboard/dashboard_storyboard.pdf docs/KPI_Documentation.md
git commit -m "Milestone 2: KPI engineering and dashboard storyboard"

# Milestone 3 – dashboards
git add dashboard scripts/build_dashboard.py docs/screenshots docs/Tableau_Build_Guide.md
git commit -m "Milestone 3: four dashboards"

# Milestone 4 – testing and docs
git add .
git commit -m "Milestone 4: testing, documentation and delivery"

git push -u origin harsha
```

Then on GitHub: **Compare & pull request** (only if your team wants merging into `main`).

## Turn the dashboard into a link (optional)
Your own fork/repo → Settings → Pages → Branch: `harsha` (or main), folder `/dashboard` → Save. After a minute the dashboard opens from a normal web address; put it in the README.

## Before you submit
- [ ] Add your Tableau file to `dashboard/` (see `Tableau_Build_Guide.md`)
- [ ] Tick the manual boxes in `docs/QA_Checklist.md`
- [ ] Read every script once. You'll be asked how it works.
