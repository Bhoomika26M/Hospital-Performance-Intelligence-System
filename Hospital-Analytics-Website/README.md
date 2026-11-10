# Hospital Operations & Patient Analytics Website

A responsive multi-page website built with plain HTML, CSS, and JavaScript.

## Folder structure

```text
Hospital-Analytics-Website/
├── index.html
├── overview.html
├── patient-flow.html
├── conditions.html
├── resources.html
├── about.html
├── css/
│   └── style.css
├── js/
│   └── script.js
├── assets/
│   └── images/
└── README.md
```

## Run the website

1. Extract `Hospital-Analytics-Website.zip`.
2. Open the extracted folder.
3. Double-click `index.html` to open it in a browser.

For local development, open the folder in Visual Studio Code and use the Live Server extension if installed. No frameworks, package installs, or build steps are required.

## Pages

- `index.html`: homepage and navigation
- `overview.html`: Hospital Overview dashboard section
- `patient-flow.html`: Patient Flow dashboard section
- `conditions.html`: Medical Condition Analysis section
- `resources.html`: Resource Utilization dashboard section
- `about.html`: scope, datasets, KPI definitions, and limitations

## Tableau dashboard embeds

The four dashboard pages are configured with the Tableau Public links supplied for this project:

- `overview.html`: Hospital Overview
- `patient-flow.html`: Patient Flow
- `conditions.html`: Medical Condition Analysis
- `resources.html`: Resource Utilization

The JavaScript in `js/script.js` creates a responsive iframe for each approved Tableau Public URL. If a dashboard does not appear, open its Tableau Public page directly and confirm that the view is publicly accessible and that embedding is allowed.

**Privacy:** Tableau Public content is publicly accessible. The workbook contains embedded patient-admissions and hospital-infrastructure extracts. I have not independently verified every row of those extracts or whether they contain personal, confidential, or restricted information. Before sharing this website or its links, confirm that the data is appropriately de-identified and that you have authorization to publish it. If not, unpublish the workbook or replace it with an approved, privacy-safe version. Embedding does not make a public Tableau view private.

## Data interpretation notes

- Patient Admissions and PMC Hospital Infrastructure are analysed separately because a reliable shared hospital identifier was not verified.
- Total Admissions is a count of admission-date records, not unique patients.
- Medical Condition is not treated as a hospital department.
- Billing currency is not assumed because it has not been confirmed.
- Reported bed capacity is not described as occupied or available beds.
- Patient footfall is not described as bed occupancy.
- The available data does not support readmission-rate or equipment-utilization calculations.

## Customization

- Edit colours, spacing, and typography in `css/style.css`.
- Edit navigation, animations, and optional Tableau embedding in `js/script.js`.
- Edit page content directly in the relevant `.html` file.
- Place approved local images in `assets/images/`.

The design loads Google Fonts (DM Sans and Space Grotesk). If the site must work fully offline, remove the Google Fonts links in the HTML files and the `@import` line in `css/style.css`; fallback sans-serif fonts will be used.


## Responsive Tableau display
The Tableau iframe now fills a wider, responsive dashboard frame. If the chart content is still clipped inside the frame, open each dashboard in Tableau and set its dashboard Size to **Automatic** (or use a suitable Range size), then republish the workbook to Tableau Public. The website CSS cannot resize a fixed-size canvas inside Tableau itself.


## Full-screen dashboard viewing
Each Tableau dashboard page includes a **Full screen** button above the embedded view. Click it to expand the dashboard viewer to the full browser screen. Press **Esc** or click **Exit full screen** to return to the page. This uses the browser Fullscreen API and requires a browser that supports fullscreen mode.
