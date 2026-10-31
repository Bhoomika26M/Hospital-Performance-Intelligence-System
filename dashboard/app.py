"""Hospital Performance Intelligence System - Streamlit dashboard (dark / light mode).
Run from the repo root:  python -m streamlit run dashboard/app.py
Data: data/processed/hospital_final.csv, data/raw/department_resources.csv,
      data/raw/equipment_utilization.csv (simulated)
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from kpi_utils import (load_dataset, load_resources, daily_inhouse, window_kpis, warmup_end,
                       department_table, efficiency_score)

DATA_PATH = ROOT / "data" / "processed" / "hospital_final.csv"
RES_PATH = ROOT / "data" / "raw" / "department_resources.csv"
EQ_PATH = ROOT / "data" / "raw" / "equipment_utilization.csv"
PAGES = ["Hospital Overview", "Patient Flow", "Department Analytics", "Resource Utilization"]

st.set_page_config(page_title="Hospital Performance Intelligence", page_icon="🏥", layout="wide")

THEMES = {
    "dark": dict(bg="#0b1220", side="#0f192b", card="#141f33", border="#243350", text="#e8eef8",
                 muted="#94a3bd", grid="rgba(148,163,189,0.15)", accent="#2dd4bf", input="#1a2740",
                 tpl="plotly_dark"),
    "light": dict(bg="#f3f6fb", side="#ffffff", card="#ffffff", border="#dde4ef", text="#10203a",
                  muted="#5d6c85", grid="rgba(16,32,58,0.10)", accent="#0d9488", input="#f3f6fb",
                  tpl="plotly_white"),
}
PAL = ["#2dd4bf", "#60a5fa", "#a78bfa", "#f59e0b", "#f472b6", "#34d399", "#fb7185"]


# ------------------------------------------------------------------ data
@st.cache_data
def get_data(path):
    return load_dataset(path)


@st.cache_data
def get_resources(path):
    return load_resources(path)


@st.cache_data
def get_equipment(path):
    return pd.read_csv(path, parse_dates=["month"])


# ------------------------------------------------------------------ sidebar: nav + theme
st.sidebar.markdown("### 🏥 Hospital Performance\n**Intelligence System**")
page = st.sidebar.radio("Navigate", PAGES, label_visibility="collapsed")
dark = st.sidebar.toggle("🌙 Dark mode", value=True, key="dark")
T = THEMES["dark" if dark else "light"]

CSS = """
<style>
.stApp {background: __BG__;}
.stApp, [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
h1, h2, h3, h4, [data-testid="stRadio"] label, [data-testid="stToggle"] label {color: __TEXT__;}
header[data-testid="stHeader"] {background: transparent;}
.block-container {padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1550px;}
section[data-testid="stSidebar"] {background: __SIDE__; border-right: 1px solid __BORDER__;}
[data-testid="stWidgetLabel"] p {color: __MUTED__; font-size: 0.78rem; text-transform: uppercase; letter-spacing: .04em;}
div[data-baseweb="select"] > div, div[data-baseweb="input"], div[data-baseweb="base-input"] {
    background: __INPUT__ !important; border-color: __BORDER__ !important;}
div[data-baseweb="select"] *, div[data-baseweb="input"] input {color: __TEXT__ !important;}
div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li, div[data-baseweb="calendar"] {
    background: __CARD__ !important; color: __TEXT__ !important;}
div[data-baseweb="calendar"] * {color: __TEXT__ !important;}
span[data-baseweb="tag"] {background: __ACCENT__ !important;}
span[data-baseweb="tag"] span {color: #04201c !important;}
.stButton > button, .stDownloadButton > button {background: __CARD__; color: __TEXT__;
    border: 1px solid __BORDER__; border-radius: 10px; width: 100%;}
.stButton > button:hover, .stDownloadButton > button:hover {border-color: __ACCENT__; color: __ACCENT__;}
[data-testid="stPlotlyChart"] {border: 1px solid __BORDER__; border-radius: 14px; overflow: hidden;
    background: __CARD__;}
[data-testid="stDataFrame"] {border: 1px solid __BORDER__; border-radius: 12px; overflow: hidden;}
.kpi {background: __CARD__; border: 1px solid __BORDER__; border-top: 3px solid var(--c);
    border-radius: 14px; padding: 14px 16px; min-height: 112px;}
.kpi-label {font-size: .72rem; color: __MUTED__; text-transform: uppercase; letter-spacing: .06em;}
.kpi-value {font-size: 1.85rem; font-weight: 700; color: __TEXT__; line-height: 1.25;}
.kpi-delta {font-size: .76rem; margin-top: 2px;}
.good {color: #22c55e;} .bad {color: #ef4444;} .flat {color: __MUTED__;}
.page-title {font-size: 1.7rem; font-weight: 700; color: __TEXT__; margin: 0;}
.page-sub {color: __MUTED__; font-size: .9rem; margin: 2px 0 14px 0;}
.sec {font-size: .8rem; font-weight: 600; color: __ACCENT__; text-transform: uppercase;
    letter-spacing: .08em; margin: 18px 0 8px 2px;}
.note {color: __MUTED__; font-size: .8rem;}
</style>
"""
for k, v in {"__BG__": T["bg"], "__SIDE__": T["side"], "__CARD__": T["card"], "__BORDER__": T["border"],
             "__TEXT__": T["text"], "__MUTED__": T["muted"], "__ACCENT__": T["accent"],
             "__INPUT__": T["input"]}.items():
    CSS = CSS.replace(k, v)
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------ load
try:
    df = get_data(DATA_PATH)
except Exception as e:
    st.error(f"Could not load `{DATA_PATH}`: {e}")
    st.stop()
try:
    res = get_resources(RES_PATH)
except Exception as e:
    st.error(f"Could not load `{RES_PATH}`: {e}")
    st.stop()
try:
    eq_all = get_equipment(EQ_PATH)
except Exception:
    eq_all = None

# ------------------------------------------------------------------ sidebar: filters
dmin, dmax = df["admit"].min().date(), df["admit"].max().date()
DEFAULTS = {"dr": (dmin, dmax), "dept": [], "adm": [], "hosp": [], "reg": []}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)


def reset():
    for k, v in DEFAULTS.items():
        st.session_state[k] = v


st.sidebar.markdown("---")
st.sidebar.markdown("**Filters**")
st.sidebar.date_input("Date range", min_value=dmin, max_value=dmax, key="dr")
st.sidebar.multiselect("Department", sorted(df["department"].unique()), key="dept", placeholder="All")
st.sidebar.multiselect("Admission type", sorted(df["admission_type"].unique()), key="adm", placeholder="All")
st.sidebar.multiselect("Region", sorted(df["region"].unique()), key="reg", placeholder="All")
st.sidebar.multiselect("Hospital (top 200)", list(df["hospital"].value_counts().index[:200]),
                       key="hosp", placeholder="All")
total_beds = int(res["Beds Allocated"].sum())
with st.sidebar.expander("Capacity settings"):
    capacity = st.number_input("Total beds", min_value=1, value=total_beds, key="cap",
                               help="Default = sum of Beds Allocated in department_resources.csv")
st.sidebar.button("↺ Reset filters", on_click=reset)

dr = st.session_state["dr"]
start, end = (dr[0], dr[1]) if isinstance(dr, (tuple, list)) and len(dr) == 2 else (dmin, dmax)
start, end = pd.Timestamp(start), pd.Timestamp(end)

# first days of data have no "already in hospital" patients -> exclude from occupancy
OCC_FROM = warmup_end(df)
occ_lo = max(start, OCC_FROM) if max(start, OCC_FROM) <= end else start

base = df
if st.session_state["dept"]:
    base = base[base["department"].isin(st.session_state["dept"])]
if st.session_state["adm"]:
    base = base[base["admission_type"].isin(st.session_state["adm"])]
if st.session_state["hosp"]:
    base = base[base["hospital"].isin(st.session_state["hosp"])]
if st.session_state["reg"]:
    base = base[base["region"].isin(st.session_state["reg"])]
a_norm = base["admit"].dt.normalize()
f = base[(a_norm >= start) & (a_norm <= end)]

st.sidebar.download_button("⬇ Download filtered data", f.to_csv(index=False).encode(),
                           "filtered_hospital_data.csv", "text/csv")

# ------------------------------------------------------------------ helpers
_k = [0]


def show(fig):
    _k[0] += 1
    try:
        st.plotly_chart(fig, width="stretch", key=f"pc{_k[0]}")
    except TypeError:
        st.plotly_chart(fig, use_container_width=True, key=f"pc{_k[0]}")


def show_df(d):
    try:
        st.dataframe(d, width="stretch", hide_index=True)
    except TypeError:
        st.dataframe(d, use_container_width=True, hide_index=True)


def style(fig, title, h=330, legend=False):
    fig.update_layout(template=T["tpl"], paper_bgcolor=T["card"], plot_bgcolor=T["card"], height=h,
                      margin=dict(l=14, r=14, t=52, b=14), showlegend=legend,
                      title=dict(text=title, x=0.02, y=0.95, font=dict(size=15, color=T["text"])),
                      font=dict(color=T["text"], size=12),
                      legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=1,
                                  title_text=""))
    fig.update_xaxes(gridcolor=T["grid"], zeroline=False)
    fig.update_yaxes(gridcolor=T["grid"], zeroline=False)
    return fig


def section(t):
    st.markdown(f'<div class="sec">{t}</div>', unsafe_allow_html=True)


def trim_partial(d, col="month"):
    """Hide first/last months only partly inside the selected date range."""
    m_end = d[col] + pd.offsets.MonthEnd(0)
    ok = (d[col] >= start) & (m_end <= end)
    return d[ok] if ok.any() else d


def delta_html(cur, prev, mode, good_up=True, unit=""):
    if prev is None or cur is None or pd.isna(cur) or pd.isna(prev) or (mode == "pct" and prev == 0):
        return '<div class="kpi-delta flat">no prior period</div>'
    d = (cur - prev) / prev * 100 if mode == "pct" else cur - prev
    txt = f"{d:+.1f}%" if mode == "pct" else f"{d:+.1f} {unit}"
    cls = "flat" if abs(d) < 1e-9 else ("good" if (d > 0) == good_up else "bad")
    arrow = "▲" if d > 0 else ("▼" if d < 0 else "■")
    return f'<div class="kpi-delta {cls}">{arrow} {txt} vs prev. period</div>'


def kpi_card(col, label, value, delta, color):
    col.markdown(f'<div class="kpi" style="--c:{color}"><div class="kpi-label">{label}</div>'
                 f'<div class="kpi-value">{value}</div>{delta}</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------ header
st.markdown(f'<p class="page-title">{page}</p>', unsafe_allow_html=True)
if f.empty:
    st.warning("No records match the current filters.")
    st.stop()
st.markdown(f'<p class="page-sub">{start:%d %b %Y} – {end:%d %b %Y} &nbsp;·&nbsp; '
            f'{len(f):,} admissions &nbsp;·&nbsp; {f["hospital"].nunique():,} hospitals</p>',
            unsafe_allow_html=True)

ih = daily_inhouse(base)
cur = window_kpis(base, ih, start, end, capacity, OCC_FROM)
span = (end - start).days + 1
prev = window_kpis(base, ih, start - pd.Timedelta(days=span), start - pd.Timedelta(days=1), capacity, OCC_FROM)
P = lambda k: prev[k] if prev else None

dep = department_table(f)

# ================================================================== PAGE 1
if page == PAGES[0]:
    c = st.columns(6)
    kpi_card(c[0], "Total admissions", f"{cur['adm']:,}", delta_html(cur["adm"], P("adm"), "pct"), PAL[0])
    kpi_card(c[1], "Occupancy rate", f"{cur['occ']:.1f}%", delta_html(cur["occ"], P("occ"), "pp", True, "pp"), PAL[1])
    kpi_card(c[2], "Avg length of stay", f"{cur['los']:.1f} d", delta_html(cur["los"], P("los"), "pp", False, "d"), PAL[2])
    kpi_card(c[3], "Readmission rate", f"{cur['readm']:.2f}%", delta_html(cur["readm"], P("readm"), "pp", False, "pp"), PAL[4])
    kpi_card(c[4], "Bed utilization (peak)", f"{cur['bed']:.1f}%", delta_html(cur["bed"], P("bed"), "pp", True, "pp"), PAL[3])
    kpi_card(c[5], "Discharges", f"{cur['disc']:,}", delta_html(cur["disc"], P("disc"), "pct"), PAL[5])

    section("Monthly trends")
    adm_m = trim_partial(f.groupby("month").size().reset_index(name="Admissions"))
    occ_m = (ih.loc[occ_lo:end].resample("MS").mean() / capacity * 100).reset_index()
    occ_m.columns = ["month", "Occupancy %"]
    occ_m = trim_partial(occ_m)
    red_m = trim_partial((f.groupby("month")["readmit"].mean() * 100).reset_index(name="Readmission %"))
    st.caption("Months only partly covered by the date range are hidden. "
               "Occupancy ignores the first 30 days of data (no earlier patients are recorded).")
    a, b, d = st.columns(3)
    with a:
        show(style(px.line(adm_m, x="month", y="Admissions", markers=True,
                           color_discrete_sequence=[PAL[0]]), "Admissions trend"))
    with b:
        show(style(px.line(occ_m, x="month", y="Occupancy %", markers=True,
                           color_discrete_sequence=[PAL[1]]), "Occupancy rate trend"))
    with d:
        show(style(px.line(red_m, x="month", y="Readmission %", markers=True,
                           color_discrete_sequence=[PAL[4]]), "Readmission rate trend"))

    section("Where the volume sits")
    a, b, d = st.columns(3)
    at = f["admission_type"].value_counts().reset_index()
    at.columns = ["Admission type", "count"]
    donut = px.pie(at, names="Admission type", values="count", hole=0.62, color_discrete_sequence=PAL)
    donut.update_traces(textinfo="percent", marker=dict(line=dict(color=T["card"], width=2)))
    donut.add_annotation(text=f"<b>{len(f):,}</b><br>total", showarrow=False, font=dict(size=16))
    with a:
        show(style(donut, "Admissions by patient type", legend=True))
    with b:
        t = dep.sort_values("admissions")
        show(style(px.bar(t, x="admissions", y="department", orientation="h", text_auto=",.0f",
                          color_discrete_sequence=[PAL[1]]), "Admissions by department"))
    with d:
        t = dep.sort_values("avg_los")
        show(style(px.bar(t, x="avg_los", y="department", orientation="h", text_auto=".1f",
                          color_discrete_sequence=[PAL[2]]), "Avg length of stay by department (days)"))

    section("Flow and ranking")
    a, b, d = st.columns([1, 1.3, 1])
    with a:
        t = dep.sort_values("readmit_rate")
        show(style(px.bar(t, x="readmit_rate", y="department", orientation="h", text_auto=".2f",
                          color_discrete_sequence=[PAL[4]]), "Readmission rate by department (%)"))
    with b:
        ad = f.groupby("month").size().rename("Admissions")
        dn = f.groupby(f["discharge"].dt.to_period("M").dt.to_timestamp()).size().rename("Discharges")
        fl = pd.concat([ad, dn], axis=1).fillna(0)
        fl = fl[(fl.index >= start.to_period("M").to_timestamp()) & (fl.index <= end)].reset_index()
        fl.columns = ["month", "Admissions", "Discharges"]
        fl = trim_partial(fl)
        show(style(px.bar(fl, x="month", y=["Admissions", "Discharges"], barmode="group",
                          color_discrete_sequence=[PAL[0], PAL[1]]), "Monthly admissions vs discharges",
                   legend=True))
    with d:
        top = f["hospital"].value_counts().head(5).reset_index()
        top.columns = ["hospital", "admissions"]
        show(style(px.bar(top.sort_values("admissions"), x="admissions", y="hospital", orientation="h",
                          text_auto=",.0f", color_discrete_sequence=[PAL[5]]), "Top 5 hospitals by admissions"))

    section("Regional view")
    rg = f.groupby("region").agg(admissions=("los", "size"), avg_los=("los", "mean")).reset_index()
    a, b = st.columns(2)
    with a:
        show(style(px.bar(rg.sort_values("admissions"), x="admissions", y="region", orientation="h",
                          text_auto=",.0f", color_discrete_sequence=[PAL[1]]), "Admissions by region"))
    with b:
        show(style(px.bar(rg.sort_values("avg_los"), x="avg_los", y="region", orientation="h",
                          text_auto=".1f", color_discrete_sequence=[PAL[2]]),
                   "Avg length of stay by region (days)"))

# ================================================================== PAGE 2
elif page == PAGES[1]:
    section("Admissions and discharges")
    a, b = st.columns([1.6, 1])
    ad = f.groupby("month").size().rename("Admissions")
    dn = f.groupby(f["discharge"].dt.to_period("M").dt.to_timestamp()).size().rename("Discharges")
    fl = pd.concat([ad, dn], axis=1).fillna(0)
    fl = fl[(fl.index >= start.to_period("M").to_timestamp()) & (fl.index <= end)].reset_index()
    fl.columns = ["month", "Admissions", "Discharges"]
    fl = trim_partial(fl)
    with a:
        show(style(px.line(fl, x="month", y=["Admissions", "Discharges"], markers=True,
                           color_discrete_sequence=[PAL[0], PAL[3]]), "Admissions vs discharges by month",
                   legend=True))
    with b:
        show(style(px.histogram(f, x="los", nbins=30, color_discrete_sequence=[PAL[2]],
                                labels={"los": "Length of stay (days)"}), "Length of stay distribution"))

    section("Peak load")
    a, b = st.columns([1.6, 1])
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    months = ["January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "December"]
    hm = f.groupby([f["admit"].dt.day_name(), f["admit"].dt.month_name()]).size().unstack(fill_value=0)
    hm = hm.reindex(index=days, columns=[m for m in months if m in hm.columns], fill_value=0)
    with a:
        show(style(px.imshow(hm, aspect="auto", color_continuous_scale="Teal"),
                   "Admissions heatmap: weekday x month", h=360))
    with b:
        dow = f["admit"].dt.day_name().value_counts().reindex(days).reset_index()
        dow.columns = ["day", "admissions"]
        show(style(px.bar(dow, x="day", y="admissions", color_discrete_sequence=[PAL[1]]),
                   "Admissions by weekday", h=360))

    section("Peak patient load")
    census = ih.loc[occ_lo:end]
    if len(census):
        pk_day, pk_val = census.idxmax(), int(census.max())
        cdf = census.rename("In-house patients").rename_axis("date").reset_index()
        fig = px.line(cdf, x="date", y="In-house patients", color_discrete_sequence=[PAL[3]])
        fig.add_hline(y=capacity, line_dash="dash", line_color="#ef4444", annotation_text="Total beds")
        fig.add_annotation(x=pk_day, y=pk_val, text=f"Peak {pk_val:,}", showarrow=True, arrowhead=2, ay=-40)
        show(style(fig, "Patients in hospital per day"))
        st.markdown(f'<p class="note">Peak load: <b>{pk_val:,}</b> patients on {pk_day:%d %b %Y} '
                    f'({pk_val / capacity * 100:.1f}% of beds).</p>', unsafe_allow_html=True)

    section("Patient pathway")
    s = f.groupby(["admission_type", "department"]).size().reset_index(name="n")
    nodes = list(s["admission_type"].unique()) + list(s["department"].unique())
    ix = {n: i for i, n in enumerate(nodes)}
    sk = go.Figure(go.Sankey(
        node=dict(label=nodes, pad=18, thickness=16, color=[PAL[i % len(PAL)] for i in range(len(nodes))]),
        link=dict(source=s["admission_type"].map(ix), target=s["department"].map(ix), value=s["n"],
                  color="rgba(130,150,180,0.35)")))
    show(style(sk, "Admission type → department", h=420))

# ================================================================== PAGE 3
elif page == PAGES[2]:
    dep["efficiency"] = efficiency_score(dep, department_table(df))
    cap_cols = res[["Department", "Beds Allocated", "Doctors"]].rename(columns={"Department": "department"})
    dep = dep.merge(cap_cols, on="department", how="left")
    dep["adm_per_bed"] = dep["admissions"] / dep["Beds Allocated"]
    dep["adm_per_doctor"] = dep["admissions"] / dep["Doctors"]

    best = dep.sort_values("efficiency", ascending=False).iloc[0]
    st.markdown(f'<p class="note">Most efficient department in this view: <b>{best["department"]}</b> '
                f'(score {best["efficiency"]}). Score = 100 × (1 − average of normalised length of stay '
                f'and readmission rate), normalised against all departments in the full dataset; '
                f'higher is better.</p>', unsafe_allow_html=True)

    section("Department comparison")
    a, b, d = st.columns(3)
    with a:
        show(style(px.bar(dep.sort_values("admissions"), x="admissions", y="department", orientation="h",
                          text_auto=",.0f", color_discrete_sequence=[PAL[1]]), "Patient volume"))
    with b:
        show(style(px.bar(dep.sort_values("avg_los"), x="avg_los", y="department", orientation="h",
                          text_auto=".1f", color_discrete_sequence=[PAL[2]]), "Avg length of stay (days)"))
    with d:
        show(style(px.bar(dep.sort_values("readmit_rate"), x="readmit_rate", y="department", orientation="h",
                          text_auto=".2f", color_discrete_sequence=[PAL[4]]), "Readmission rate (%)"))

    section("Efficiency")
    a, b = st.columns([1.2, 1])
    with a:
        show(style(px.bar(dep.sort_values("efficiency"), x="efficiency", y="department", orientation="h",
                          text_auto=".1f", color_discrete_sequence=[PAL[0]]),
                   "Efficiency score (higher = shorter stay, fewer readmissions)", h=360))
    with b:
        show(style(px.scatter(dep, x="avg_los", y="readmit_rate", size="admissions", color="department",
                              color_discrete_sequence=PAL),
                   "Length of stay vs readmission (bubble = volume)", h=360, legend=False))

    section("Treatment capacity")
    a, b = st.columns(2)
    with a:
        show(style(px.bar(dep.dropna(subset=["adm_per_bed"]).sort_values("adm_per_bed"), x="adm_per_bed",
                          y="department", orientation="h", text_auto=".1f", color_discrete_sequence=[PAL[3]]),
                   "Admissions per allocated bed (selected period)"))
    with b:
        show(style(px.bar(dep.dropna(subset=["adm_per_doctor"]).sort_values("adm_per_doctor"), x="adm_per_doctor",
                          y="department", orientation="h", text_auto=".1f", color_discrete_sequence=[PAL[2]]),
                   "Admissions per doctor (selected period)"))

    section("Detail table")
    show_df(dep.round(2).sort_values("efficiency", ascending=False))

# ================================================================== PAGE 4
else:
    st.markdown('<p class="note">Beds and staff come from department_resources.csv. '
                'Equipment usage is <b>simulated</b> (data/raw/equipment_utilization.csv).</p>',
                unsafe_allow_html=True)
    days_idx = pd.date_range(occ_lo, end)
    rows = []
    for _, r in res.iterrows():
        sub = base[base["department"] == r["Department"]]
        avg_in = daily_inhouse(sub).reindex(days_idx, fill_value=0).mean() if len(sub) else 0.0
        rows.append({"department": r["Department"], "beds": int(r["Beds Allocated"]),
                     "avg_occupied": round(avg_in, 1),
                     "bed_utilization_%": round(avg_in / r["Beds Allocated"] * 100, 1),
                     "doctors": int(r["Doctors"]), "nurses": int(r["Nurses"]),
                     "technicians": int(r["Technicians"]), "staff": int(r["Staff"]),
                     "patients_per_staff": round(avg_in / r["Staff"], 2)})
    ru = pd.DataFrame(rows)

    only_res = set(res["Department"]) - set(df["department"])
    only_data = set(df["department"]) - set(res["Department"])
    if only_res or only_data:
        st.warning(f"Department names do not match. Only in resources file: {sorted(only_res)}. "
                   f"Only in patient data: {sorted(only_data)}.")
    ru["available_beds"] = (ru["beds"] - ru["avg_occupied"]).round(1)

    section("Beds and capacity")
    a, b = st.columns([1.5, 1])
    with a:
        fig = px.bar(ru, x="department", y="bed_utilization_%", text_auto=".1f",
                     color_discrete_sequence=[PAL[1]])
        fig.add_hline(y=100, line_dash="dash", line_color="#ef4444")
        show(style(fig, "Bed utilization by department (%) — red line = 100%", h=360))
    with b:
        occ_val = 0.0 if pd.isna(cur["occ"]) else cur["occ"]
        top_rng = max(100, occ_val * 1.1)
        g = go.Figure(go.Indicator(
            mode="gauge+number", value=round(occ_val, 1), number={"suffix": "%"},
            gauge={"axis": {"range": [0, top_rng]}, "bar": {"color": PAL[0]},
                   "steps": [{"range": [0, 70], "color": "rgba(34,197,94,0.25)"},
                             {"range": [70, 90], "color": "rgba(245,158,11,0.25)"},
                             {"range": [90, top_rng], "color": "rgba(239,68,68,0.25)"}]}))
        show(style(g, "Hospital capacity: average occupancy", h=360))

    section("Resource availability and capacity planning")
    a, b = st.columns([1.3, 1])
    with a:
        fig = px.bar(ru, x="department", y="available_beds", text_auto=".0f",
                     color_discrete_sequence=[PAL[5]])
        fig.add_hline(y=0, line_color="#ef4444")
        show(style(fig, "Available beds by department (negative = over capacity)"))
    with b:
        st.markdown("**Capacity planning insights**")
        shown = False
        for _, r in ru.sort_values("bed_utilization_%", ascending=False).iterrows():
            u = r["bed_utilization_%"]
            if u >= 100:
                st.markdown(f"🔴 **{r['department']}**: about {r['avg_occupied']:.0f} patients for "
                            f"{r['beds']} beds ({u:.0f}%). Short by roughly "
                            f"{r['avg_occupied'] - r['beds']:.0f} beds.")
                shown = True
            elif u >= 90:
                st.markdown(f"🟠 **{r['department']}**: {u:.0f}% utilised, close to capacity.")
                shown = True
            elif u < 60:
                st.markdown(f"🟢 **{r['department']}**: {u:.0f}% utilised, about "
                            f"{r['beds'] - r['avg_occupied']:.0f} spare beds.")
                shown = True
        if not shown:
            st.markdown("All departments are between 60% and 90% utilisation.")

    section("Staffing")
    a, b = st.columns(2)
    sl = ru.melt(id_vars="department", value_vars=["doctors", "nurses", "technicians"],
                 var_name="role", value_name="count")
    with a:
        show(style(px.bar(sl, x="department", y="count", color="role", barmode="stack",
                          color_discrete_sequence=[PAL[0], PAL[1], PAL[2]]),
                   "Staff allocation by department", legend=True))
    with b:
        show(style(px.bar(ru, x="department", y="patients_per_staff", text_auto=".2f",
                          color_discrete_sequence=[PAL[3]]), "Workload: avg patients in-house per staff member"))

    section("Equipment (simulated)")
    if eq_all is None:
        st.warning("equipment_utilization.csv not found. Run: python scripts/generate_equipment_data.py")
    else:
        m0 = start.to_period("M").to_timestamp()
        eq = eq_all[(eq_all["month"] >= m0) & (eq_all["month"] <= end)]
        eq = eq.groupby("department")[["used_hours", "available_hours"]].sum().reset_index()
        eq["usage_%"] = eq["used_hours"] / eq["available_hours"] * 100
        a, b = st.columns([1, 1.4])
        with a:
            show(style(px.bar(eq, x="department", y="usage_%", text_auto=".1f",
                              color_discrete_sequence=[PAL[5]]), "Equipment usage % (simulated)"))
        with b:
            show_df(ru)

st.markdown('<p class="note" style="margin-top:18px">Source: hospital_final.csv, department_resources.csv. '
            'All metrics respect the selected filters. Occupancy uses total beds from the sidebar.</p>',
            unsafe_allow_html=True)