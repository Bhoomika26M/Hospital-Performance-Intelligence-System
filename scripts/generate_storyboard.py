#!/usr/bin/env python3
"""Programmatic Generator for dashboard_storyboard.pdf.

Generates genuine layout wireframes of all four dashboards in both Dark and Light modes
using ReportLab, with exact container hierarchies, KPI cards, visual zones, and labels.
"""

from __future__ import annotations

import sys
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def draw_wireframe_page(
    c: canvas.Canvas,
    dash_title: str,
    dash_num: int,
    theme: str,
    kpi_cards: list[tuple[str, str, str]],
    primary_visual_desc: tuple[str, str],
    secondary_left_desc: tuple[str, str],
    secondary_right_desc: tuple[str, str],
    disclaimer: str | None = None,
):
    page_w, page_h = landscape(letter)  # 792 x 612 pt

    # Theme Palettes
    if theme == "dark":
        bg_col = colors.HexColor("#080808")
        rail_col = colors.HexColor("#1A1A1A")
        card_col = colors.HexColor("#141414")
        card_border = colors.HexColor("#2E2E2E")
        text_primary = colors.HexColor("#F5F5F5")
        text_secondary = colors.HexColor("#929292")
        accent_col = colors.HexColor("#5ACB57")
        accent_subtle = colors.HexColor("#1B381A")
        theme_label = "DARK ENTERPRISE MODE (DEFAULT)"
    else:
        bg_col = colors.HexColor("#F8F9FA")
        rail_col = colors.HexColor("#F1F5F9")
        card_col = colors.HexColor("#FFFFFF")
        card_border = colors.HexColor("#E2E8F0")
        text_primary = colors.HexColor("#0F172A")
        text_secondary = colors.HexColor("#64748B")
        accent_col = colors.HexColor("#2E7D32")
        accent_subtle = colors.HexColor("#E8F5E9")
        theme_label = "LIGHT CLINICAL MODE"

    # Background canvas
    c.setFillColor(bg_col)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    # 1. Left Navigation Rail (Width: 150pt)
    rail_w = 150
    c.setFillColor(rail_col)
    c.setStrokeColor(card_border)
    c.rect(0, 0, rail_w, page_h, fill=1, stroke=1)

    # Brand Wordmark
    c.setFillColor(text_primary)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(18, page_h - 36, "Aegis")
    c.setFillColor(accent_col)
    c.drawString(64, page_h - 36, ".dv")

    c.setFillColor(text_secondary)
    c.setFont("Helvetica", 7.5)
    c.drawString(18, page_h - 48, "HOSPITAL OPERATIONS BI")

    # Nav Buttons
    nav_items = [
        "1. Hospital Overview",
        "2. Patient Flow",
        "3. Department Analytics",
        "4. Resource Utilization",
    ]
    y_nav = page_h - 90
    for idx, item in enumerate(nav_items):
        is_active = (idx + 1) == dash_num
        if is_active:
            c.setFillColor(accent_subtle)
            c.roundRect(14, y_nav - 5, rail_w - 28, 24, 4, fill=1, stroke=0)
            c.setFillColor(accent_col)
            c.setFont("Helvetica-Bold", 8.5)
        else:
            c.setFillColor(text_secondary)
            c.setFont("Helvetica", 8.5)
        c.drawString(22, y_nav + 2, item)
        y_nav -= 30

    # System Health Badge in Rail
    c.setFillColor(card_col)
    c.setStrokeColor(card_border)
    c.roundRect(14, 110, rail_w - 28, 70, 6, fill=1, stroke=1)
    c.setFillColor(text_secondary)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(22, 166, "SYSTEM STATUS")
    c.setFillColor(accent_col)
    c.circle(26, 148, 3.5, fill=1, stroke=0)
    c.setFillColor(text_primary)
    c.setFont("Helvetica", 8)
    c.drawString(34, 145, "Live Telemetry Ready")
    c.setFillColor(text_secondary)
    c.setFont("Helvetica", 7)
    c.drawString(22, 128, "101,766 Clean Records")
    c.drawString(22, 118, "15 Active Departments")

    # Rail Footer
    c.setFillColor(text_secondary)
    c.setFont("Helvetica", 6.5)
    c.drawString(16, 36, "Developed by Ananya Biju")
    c.drawString(16, 26, "Infosys Springboard")
    c.drawString(16, 16, "Aegis.dv v1.0 Production")

    # 2. Main Content Canvas
    content_x = rail_w + 14
    content_w = page_w - content_x - 14

    # Top Header Bar
    c.setFillColor(text_primary)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(content_x, page_h - 32, f"Dashboard {dash_num}: {dash_title}")

    # Mode and Wireframe Badge
    c.setFillColor(accent_col)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(page_w - 18, page_h - 26, f"[{theme_label}]")
    c.setFillColor(text_secondary)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawRightString(page_w - 18, page_h - 38, "Architectural Layout Wireframe – Tableau Desktop 1600x900 Specification")

    # Optional Disclaimer Banner (e.g. for D4)
    y_top = page_h - 52
    if disclaimer:
        c.setFillColor(colors.HexColor("#F59E0B") if theme == "dark" else colors.HexColor("#B45309"))
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(content_x, y_top, f"⚠️ NOTICE: {disclaimer}")
        y_top -= 14

    # KPI Card Row (5 or 4 cards)
    n_kpi = len(kpi_cards)
    gap = 8
    card_w = (content_w - (gap * (n_kpi - 1))) / n_kpi
    card_h = 58
    y_kpi = y_top - card_h - 4

    for idx, (label, val, sub) in enumerate(kpi_cards):
        cx = content_x + idx * (card_w + gap)
        c.setFillColor(card_col)
        c.setStrokeColor(card_border)
        c.roundRect(cx, y_kpi, card_w, card_h, 5, fill=1, stroke=1)

        # Label
        c.setFillColor(text_secondary)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(cx + 10, y_kpi + card_h - 14, label.upper())

        # Value
        c.setFillColor(accent_col if idx in [1, 2] else text_primary)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(cx + 10, y_kpi + 22, val)

        # Subtext / Target
        c.setFillColor(text_secondary)
        c.setFont("Helvetica", 6.5)
        c.drawString(cx + 10, y_kpi + 9, sub)

    # Primary Analytical Visual Zone (Large center area)
    y_prim = y_kpi - 10
    prim_h = 240
    y_prim_box = y_prim - prim_h

    c.setFillColor(card_col)
    c.setStrokeColor(card_border)
    c.roundRect(content_x, y_prim_box, content_w, prim_h, 6, fill=1, stroke=1)

    # Primary Visual Header
    c.setFillColor(text_primary)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(content_x + 14, y_prim_box + prim_h - 18, primary_visual_desc[0])
    c.setFillColor(text_secondary)
    c.setFont("Helvetica", 8)
    c.drawString(content_x + 14, y_prim_box + prim_h - 30, primary_visual_desc[1])

    # Simulated chart skeleton inside primary container
    c.setStrokeColor(colors.HexColor("#333333") if theme == "dark" else colors.HexColor("#CBD5E1"))
    c.setLineWidth(1)
    c.line(content_x + 35, y_prim_box + 28, content_x + content_w - 20, y_prim_box + 28)  # X-axis
    c.line(content_x + 35, y_prim_box + 28, content_x + 35, y_prim_box + prim_h - 45)     # Y-axis

    # Decorative wave/bars to symbolize layout
    c.setStrokeColor(accent_col)
    c.setLineWidth(1.8)
    p = c.beginPath()
    p.moveTo(content_x + 45, y_prim_box + 60)
    p.curveTo(
        content_x + 180, y_prim_box + 180,
        content_x + 340, y_prim_box + 70,
        content_x + content_w - 30, y_prim_box + 160,
    )
    c.drawPath(p, fill=0, stroke=1)

    # Secondary Analytical Visual Zone (Dual 50/50 Containers)
    sec_gap = 10
    sec_w = (content_w - sec_gap) / 2
    sec_h = 160
    y_sec_box = y_prim_box - 10 - sec_h

    # Secondary Left Box
    c.setFillColor(card_col)
    c.setStrokeColor(card_border)
    c.roundRect(content_x, y_sec_box, sec_w, sec_h, 6, fill=1, stroke=1)
    c.setFillColor(text_primary)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(content_x + 12, y_sec_box + sec_h - 16, secondary_left_desc[0])
    c.setFillColor(text_secondary)
    c.setFont("Helvetica", 7.5)
    c.drawString(content_x + 12, y_sec_box + sec_h - 26, secondary_left_desc[1])

    # Decorative bars in secondary left
    c.setFillColor(accent_col)
    bar_y = y_sec_box + sec_h - 45
    for bar_len in [160, 210, 130, 95, 70]:
        c.roundRect(content_x + 60, bar_y, min(bar_len, sec_w - 80), 10, 2, fill=1, stroke=0)
        bar_y -= 18

    # Secondary Right Box
    c.setFillColor(card_col)
    c.setStrokeColor(card_border)
    c.roundRect(content_x + sec_w + sec_gap, y_sec_box, sec_w, sec_h, 6, fill=1, stroke=1)
    c.setFillColor(text_primary)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(content_x + sec_w + sec_gap + 12, y_sec_box + sec_h - 16, secondary_right_desc[0])
    c.setFillColor(text_secondary)
    c.setFont("Helvetica", 7.5)
    c.drawString(content_x + sec_w + sec_gap + 12, y_sec_box + sec_h - 26, secondary_right_desc[1])

    # Decorative scatter / points in secondary right
    c.setFillColor(accent_col)
    for px, py in [(60, 45), (100, 80), (140, 55), (190, 105), (230, 70)]:
        c.circle(content_x + sec_w + sec_gap + px, y_sec_box + py, 4, fill=1, stroke=0)

    # Footer Attribution
    c.setFillColor(text_secondary)
    c.setFont("Helvetica", 6.5)
    c.drawString(
        content_x,
        12,
        "Aegis.dv Enterprise Healthcare Analytics | Data Source: Cerner Health Facts (130 US Hospitals, 1999–2008) | CC BY 4.0 License",
    )
    c.showPage()


def build_storyboard_pdf(output_path: Path):
    """Generate complete 8-page landscape storyboard PDF."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_path), pagesize=landscape(letter))

    dashboards = [
        {
            "num": 1,
            "title": "Hospital Overview (Executive Command Center)",
            "kpi": [
                ("Total Admissions", "101,766", "10-Year Study Volume"),
                ("Total Discharges", "101,766", "Completed Stays"),
                ("Average LOS", "4.40 days", "Median: 4.00 days"),
                ("Readmit Rate (CMS)", "11.34%", "Surviving Cohort (100k)"),
                ("Total Patient-Days", "447,362", "Workload Delivery Proxy"),
            ],
            "prim": (
                "Longitudinal Monthly Admissions vs Discharges (1999–2008)",
                "Dual-line time series with period-over-period trendlines and throughput gap tracking",
            ),
            "sec_l": (
                "Department Volume Distribution",
                "Ranked inpatient admissions across 15 standardized clinical specialties",
            ),
            "sec_r": (
                "30-Day Readmission Outcomes & Demographics",
                "Donut breakdown (<30d, >30d, None) with age bracket stratification",
            ),
            "disclaimer": None,
        },
        {
            "num": 2,
            "title": "Patient Flow & Inpatient Throughput",
            "kpi": [
                ("Total Encounters", "101,766", "100% Inpatient Acuity"),
                ("Emergency Intake", "53.07%", "54,011 Emergent Cases"),
                ("Routine Home Exit", "60.45%", "61,515 Routine Discharges"),
                ("Prolonged Stays", "7.15%", ">9 Days Inpatient Care"),
            ],
            "prim": (
                "Integrated Patient Flow Transition Funnel",
                "Three-stage flow mapping: Admission Referral Source -> Clinical Specialty -> Discharge Disposition",
            ),
            "sec_l": (
                "Length of Stay (LOS) Right-Skewed Histogram",
                "Distribution of stay durations (1–14 days) with Mean (4.4d) and Median (4.0d) benchmark lines",
            ),
            "sec_r": (
                "Temporal Admission Heatmap (Day of Week x Month)",
                "Concentration matrix identifying weekly and seasonal admission surges",
            ),
            "disclaimer": None,
        },
        {
            "num": 3,
            "title": "Department Analytics & Service Line Performance",
            "kpi": [
                ("Clinical Services", "15 Units", "Standardized Taxonomy"),
                ("Volume Leader", "Internal Med", "49.6% Total Patient Load"),
                ("Highest Acuity", "General Surgery", "26.4 Clinical Intensity"),
                ("Hospital Benchmark", "4.40 Days", "Target ALOS Threshold"),
            ],
            "prim": (
                "Department 4-Quadrant Strategic Portfolio (Volume vs Readmission Rate)",
                "Scatter plot sized by Patient-Days; benchmark lines at Hospital Readmit Rate (11.34%) and Median Volume",
            ),
            "sec_l": (
                "Ranked Department Length of Stay (ALOS)",
                "Horizontal bar comparison with sample size flag (p_Min_Sample_Size >= 30)",
            ),
            "sec_r": (
                "Clinical Intensity Index by Department",
                "Weighted procedure, medication, diagnostic, and lab workload score",
            ),
            "disclaimer": None,
        },
        {
            "num": 4,
            "title": "Resource Utilization & Facility Capacity Planning",
            "kpi": [
                ("Staffed Beds", "650 Beds", "Licensed Inpatient Units"),
                ("Average Occupancy", "78.4%", "Target Range: 75%–90%"),
                ("Nurse-to-Patient", "1 : 3.4", "Daily Unit Average"),
                ("Delivered Care Days", "447,362", "Authentic Workload (Real)"),
            ],
            "prim": (
                "Daily Bed Occupancy Rate Trend vs Threshold Bands",
                "Time series featuring 75%–90% optimal operational zone and 90% critical bottleneck redline",
            ),
            "sec_l": (
                "Staffed vs Occupied Beds by Clinical Unit",
                "Side-by-side capacity comparison across 10 inpatient nursing units",
            ),
            "sec_r": (
                "Nurse Staffing Level vs Patient Census Correlation",
                "Daily on-duty nursing coverage plotted against active bed census",
            ),
            "disclaimer": "Synthetic reference data – not real hospital figures (Section 3 Policy Compliance).",
        },
    ]

    # Generate Dark Mode followed by Light Mode for each dashboard
    for theme in ["dark", "light"]:
        for d in dashboards:
            draw_wireframe_page(
                c=c,
                dash_title=d["title"],
                dash_num=d["num"],
                theme=theme,
                kpi_cards=d["kpi"],
                primary_visual_desc=d["prim"],
                secondary_left_desc=d["sec_l"],
                secondary_right_desc=d["sec_r"],
                disclaimer=d["disclaimer"],
            )

    c.save()
    print(f"Successfully generated {len(dashboards) * 2}-page storyboard PDF at: {output_path}")


if __name__ == "__main__":
    out_pdf = PROJECT_ROOT / "dashboard_storyboard.pdf"
    build_storyboard_pdf(out_pdf)

