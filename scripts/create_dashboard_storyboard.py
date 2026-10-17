
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, KeepTogether
)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT = BASE_DIR / "dashboard_storyboard.pdf"

PAGE_SIZE = landscape(A4)
NAVY = colors.HexColor("#0B1220")
CARD = colors.HexColor("#172B46")
TEAL = colors.HexColor("#2DD4BF")
BLUE = colors.HexColor("#60A5FA")
LIGHT = colors.HexColor("#F1F5F9")
MUTED = colors.HexColor("#475569")
WHITE = colors.white

doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=PAGE_SIZE,
    rightMargin=38,
    leftMargin=38,
    topMargin=35,
    bottomMargin=35
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="MainTitle", parent=styles["Title"],
    fontName="Helvetica-Bold", fontSize=25,
    leading=31, textColor=NAVY, alignment=TA_CENTER,
    spaceAfter=12
))
styles.add(ParagraphStyle(
    name="Subtitle", parent=styles["Normal"],
    fontSize=11, leading=16, textColor=MUTED,
    alignment=TA_CENTER, spaceAfter=18
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading1"],
    fontSize=17, leading=22, textColor=NAVY,
    spaceBefore=8, spaceAfter=10
))
styles.add(ParagraphStyle(
    name="Subheading", parent=styles["Heading2"],
    fontSize=12, leading=16, textColor=CARD,
    spaceBefore=6, spaceAfter=5
))
styles.add(ParagraphStyle(
    name="BodyCustom", parent=styles["BodyText"],
    fontSize=9, leading=13, textColor=MUTED,
    spaceAfter=6
))
styles.add(ParagraphStyle(
    name="Cell", parent=styles["BodyText"],
    fontSize=8, leading=11, textColor=NAVY
))
styles.add(ParagraphStyle(
    name="CellWhite", parent=styles["BodyText"],
    fontSize=8, leading=11, textColor=WHITE
))

story = []


def P(text, style="BodyCustom"):
    return Paragraph(text, styles[style])


def add_table(headers, rows, widths=None):
    data = [[P(str(h), "CellWhite") for h in headers]]
    for row in rows:
        data.append([P(str(value), "Cell") for value in row])

    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [WHITE, LIGHT]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def add_page(canvas, document):
    canvas.saveState()
    width, height = PAGE_SIZE
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 8, width, 8, fill=1, stroke=0)
    canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
    canvas.line(38, 25, width - 38, 25)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(38, 13, "MedTrack_DV | Streamlit Dashboard Storyboard")
    canvas.drawRightString(width - 38, 13, f"Page {document.page}")
    canvas.restoreState()


# COVER
story.append(Spacer(1, 35))
story.append(P("MedTrack_DV", "MainTitle"))
story.append(P(
    "Hospital Operations &amp; Patient Analytics Dashboard",
    "Subtitle"
))
story.append(P(
    "Dashboard Storyboard and Interaction Plan",
    "MainTitle"
))
story.append(Spacer(1, 12))
story.append(P(
    "Technology: Python, Pandas, Plotly, Streamlit and Excel",
    "Subtitle"
))
story.append(Spacer(1, 15))
story.append(P("Project Objective", "Section"))
story.append(P(
    "Transform hospital patient and resource datasets into interactive "
    "visual insights that help users explore patient outcomes, readmissions, "
    "length of stay, costs, bed occupancy and staffing."
))
story.append(P("Implementation Approach", "Section"))
story.append(P(
    "The project uses Streamlit instead of the Tableau workbook originally "
    "specified. The existing application has four pages: Overview, Patient "
    "Analytics, Resource Utilization and Data Explorer. This storyboard "
    "documents the intended use of those pages and identifies areas where "
    "the available data limits the analysis."
))
story.append(Spacer(1, 12))
story.append(add_table(
    ["Dataset", "Records", "Purpose"],
    [
        ["Patient analysis dataset", "984", "Patient outcomes, readmissions, stay and cost"],
        ["Resource allocation dataset", "200", "Bed allocation, occupancy and staffing"],
        ["Healthcare dataset", "500", "Additional clinical information collected during preparation"],
    ],
    [2.0 * inch, 1.0 * inch, 5.8 * inch]
))
story.append(PageBreak())


# USER JOURNEY
story.append(P("1. Dashboard Storyline", "Section"))
story.append(P(
    "The user begins with an overall snapshot, investigates patient metrics, "
    "examines available resources, and finally inspects the underlying data."
))
story.append(add_table(
    ["Order", "Dashboard Page", "Question Answered", "Main Content"],
    [
        ["1", "Overview", "What does the overall patient and resource picture look like?",
         "Patient KPIs, outcome distribution, readmission status and resource snapshot."],
        ["2", "Patient Analytics", "What patterns appear in patient records?",
         "Patient metrics, outcome comparisons, length-of-stay distribution and cost by condition."],
        ["3", "Resource Utilization", "How are beds and staff allocated and used?",
         "Bed occupancy, hospital bed comparisons and allocated versus on-duty staff."],
        ["4", "Data Explorer", "Can the figures be inspected and verified?",
         "Dataset selection, previews, row and column counts, missing values and CSV export."],
    ],
    [0.55 * inch, 1.55 * inch, 2.7 * inch, 4.0 * inch]
))
story.append(Spacer(1, 12))
story.append(P("Shared Controls", "Subheading"))
story.append(P(
    "The existing application provides sidebar navigation and patient filters "
    "for gender and condition, plus a reset button. These filters should affect "
    "patient-focused pages consistently. Resource records should not be filtered "
    "by patient attributes because the datasets do not have a verified common key."
))
story.append(P("Visual Design", "Subheading"))
story.append(P(
    "Use the existing dark navy background, blue and teal chart accents, "
    "clear headings, KPI cards, readable labels and consistent spacing. "
    "Avoid unnecessary new pages or decorative charts."
))
story.append(PageBreak())


# OVERVIEW
story.append(P("2. Overview — Hospital Snapshot", "Section"))
story.append(P(
    "Purpose: Give users a quick view of patient performance and resource status."
))
story.append(add_table(
    ["Component", "Planned Visualization", "Interpretation"],
    [
        ["Patient KPIs", "Metric cards",
         "Total patient records, average recorded length of stay, readmission rate and recovery rate."],
        ["Patient outcomes", "Donut chart",
         "Compare the recorded Recovered and Stable outcomes."],
        ["Readmission status", "Bar chart",
         "Compare records marked Yes and No."],
        ["Resource snapshot", "Metric cards",
         "Show allocated beds, occupied beds, aggregate occupancy and staff on-duty rate."],
    ],
    [1.5 * inch, 1.7 * inch, 5.6 * inch]
))
story.append(Spacer(1, 12))
story.append(P("Design notes", "Subheading"))
story.append(P(
    "Keep the highest-value metrics at the top and supporting charts below. "
    "Clearly distinguish patient-derived metrics from resource-derived metrics. "
    "The resource figures are sums across resource records and must not automatically "
    "be interpreted as unique hospital-wide totals."
))
story.append(PageBreak())


# PATIENT ANALYTICS
story.append(P("3. Patient Analytics", "Section"))
story.append(P(
    "Purpose: Explore differences in outcomes, recorded length of stay and patient costs."
))
story.append(add_table(
    ["Component", "Visualization", "Required Fields"],
    [
        ["Patient outcome comparison", "Bar or donut chart",
         "Outcome, patient record count"],
        ["Length of stay", "Histogram",
         "Length_of_Stay"],
        ["Average cost", "KPI card",
         "Cost"],
        ["Average cost by condition", "Horizontal bar chart",
         "Condition, Cost"],
        ["Patient filters", "Sidebar multiselects",
         "Gender, Condition"],
    ],
    [2.0 * inch, 2.0 * inch, 4.8 * inch]
))
story.append(Spacer(1, 12))
story.append(P("Interpretation cautions", "Subheading"))
story.append(P(
    "The dataset contains 984 patient analysis records. The length-of-stay "
    "unit is not verified, so label it as recorded length of stay rather than "
    "assuming days. The dataset does not contain verified admission and discharge "
    "dates for a reliable time-series patient-flow analysis."
))
story.append(PageBreak())


# RESOURCE UTILIZATION
story.append(P("4. Resource Utilization", "Section"))
story.append(P(
    "Purpose: Show how available bed and staffing allocations compare with usage."
))
story.append(add_table(
    ["Component", "Visualization", "Calculation / Field"],
    [
        ["Beds allocated", "KPI card", "Sum of beds_allocated"],
        ["Beds occupied", "KPI card", "Sum of beds_occupied"],
        ["Bed occupancy rate", "KPI card",
         "Total occupied beds / total allocated beds × 100"],
        ["Hospital comparison", "Grouped bar chart",
         "beds_allocated and beds_occupied grouped by hospital_name"],
        ["Staffing comparison", "Bar chart",
         "staff_allocated compared with staff_on_duty"],
        ["Staff on-duty rate", "KPI card",
         "Total staff_on_duty / total staff_allocated × 100"],
    ],
    [1.7 * inch, 2.0 * inch, 5.1 * inch]
))
story.append(Spacer(1, 12))
story.append(P("Interpretation cautions", "Subheading"))
story.append(P(
    "Some records have zero allocated beds or staff. Per-record rate calculations "
    "must handle division by zero. Aggregated rates should be described as rates "
    "across the available resource records until the dataset's record grain is confirmed."
))
story.append(PageBreak())


# DATA EXPLORER AND INTERACTIONS
story.append(P("5. Data Explorer and Interactions", "Section"))
story.append(add_table(
    ["Feature", "Expected Behavior"],
    [
        ["Dataset selector", "Switch between Patient Data, Resource Data and KPI Summary."],
        ["Dataset preview", "Display a configurable sample of rows."],
        ["Quality indicators", "Show row count, column count and missing-value count."],
        ["CSV export", "Allow users to download the selected table."],
        ["View all records", "Expand a full table when needed."],
        ["Sidebar navigation", "Move between the four existing pages."],
        ["Patient filters", "Filter patient analysis by gender and condition."],
        ["Reset filters", "Restore the default filter selections."],
    ],
    [2.0 * inch, 6.8 * inch]
))
story.append(Spacer(1, 12))
story.append(P("Navigation Flow", "Subheading"))
story.append(P(
    "Overview → Patient Analytics → Resource Utilization → Data Explorer. "
    "Users can also jump directly to any page through the sidebar."
))
story.append(PageBreak())


# KPI DEFINITIONS AND LIMITATIONS
story.append(P("6. KPI Reference and Data Limitations", "Section"))
story.append(add_table(
    ["KPI", "Definition"],
    [
        ["Total Admissions", "Count of patient analysis records; this is a record count, not verified unique admissions."],
        ["Average Length of Stay", "Mean of Length_of_Stay; the measurement unit is unverified."],
        ["Readmission Rate", "Records marked Yes / all eligible records × 100."],
        ["Average Patient Cost", "Mean of Cost in the patient analysis dataset."],
        ["Recovery Rate", "Records with Outcome = Recovered / all eligible records × 100."],
        ["Bed Occupancy Rate", "Sum of beds_occupied / sum of beds_allocated × 100."],
        ["Staff On-Duty Rate", "Sum of staff_on_duty / sum of staff_allocated × 100."],
    ],
    [2.0 * inch, 6.8 * inch]
))
story.append(Spacer(1, 12))
story.append(P("Known limitations", "Subheading"))
story.append(P(
    "The current datasets do not provide a reliable shared key to link patient "
    "records to resource records. They do not support a verified department "
    "efficiency score, department-level comparisons, monthly admission trends, "
    "discharge tracking or patient movement analysis. These features require "
    "additional suitable data and must not be fabricated."
))
story.append(P("Quality and validation", "Subheading"))
story.append(P(
    "Re-run the KPI generation and validation scripts after source data changes. "
    "Compare workbook totals with independently calculated values, check missing "
    "values and duplicates, and confirm that dashboard labels match KPI definitions."
))
story.append(Spacer(1, 12))
story.append(P("Milestone 2 Deliverables", "Section"))
story.append(add_table(
    ["Deliverable", "Status / Purpose"],
    [
        ["hospital_final_dataset.xlsx", "Excel workbook containing prepared datasets and KPI sheets."],
        ["generate_hospital_kpis.py", "Repeatable KPI calculation and workbook generation."],
        ["dashboard_storyboard.pdf", "This dashboard planning and interaction document."],
        ["Streamlit app.py", "Interactive dashboard prototype replacing the planned Tableau prototype."],
    ],
    [2.7 * inch, 6.1 * inch]
))


doc.build(story, onFirstPage=add_page, onLaterPages=add_page)

print(f"Dashboard storyboard created successfully: {OUTPUT}")
