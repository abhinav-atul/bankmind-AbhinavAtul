"""
app.py — BankMind · Track A
SaaS-style Streamlit dashboard for UCI Bank Marketing data.
"""

import os, math
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime

# ──────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BankMind",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────
# DESIGN TOKENS
# ──────────────────────────────────────────────────────────────────
T = {
    "bg":       "#080C14",
    "surface":  "#0D1220",
    "surface2": "#111827",
    "border":   "#1C2538",
    "border2":  "#243048",
    "text":     "#E2E8F0",
    "muted":    "#64748B",
    "accent":   "#3B82F6",
    "accent2":  "#8B5CF6",
    "success":  "#10B981",
    "danger":   "#EF4444",
    "warning":  "#F59E0B",
    "grid":     "#1C2538",
}

# ──────────────────────────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

*, html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
}}
[data-testid="stIconMaterial"] {{
    font-family: 'Material Symbols Rounded' !important;
    font-size: 20px !important; font-style: normal !important;
    font-weight: 400 !important; line-height: 1 !important;
    -webkit-font-feature-settings: 'liga'; font-feature-settings: 'liga';
}}
.block-container {{ padding: 2.5rem 2rem 3rem 2rem !important; max-width: 1440px; }}
section[data-testid="stSidebar"] {{
    background: {T["surface"]} !important;
    border-right: 1px solid {T["border"]} !important;
}}
[data-testid="stMetric"] {{
    background: {T["surface2"]}; border: 1px solid {T["border"]};
    border-radius: 12px; padding: 1rem 1.2rem !important;
    transition: border-color 0.15s ease;
}}
[data-testid="stMetric"]:hover {{ border-color: {T["border2"]}; }}
[data-testid="stMetricLabel"] {{
    font-size: 0.72rem !important; font-weight: 600 !important;
    letter-spacing: 0.1em !important; text-transform: uppercase !important;
    color: {T["muted"]} !important;
}}
[data-testid="stMetricValue"] {{
    font-size: 1.8rem !important; font-weight: 700 !important;
    color: {T["text"]} !important;
}}
[data-testid="stMetricDelta"] {{ font-size: 0.78rem !important; }}
[data-testid="stMetricDelta"] svg {{ display: none; }}
[data-testid="stSelectbox"] [data-baseweb="select"] div,
[data-testid="stMultiSelect"] [data-baseweb="select"] div {{
    background: {T["surface2"]} !important; border-color: {T["border"]} !important;
    color: {T["text"]} !important; font-size: 0.83rem !important;
}}
[data-testid="stDataFrame"] {{
    border: 1px solid {T["border"]}; border-radius: 10px; overflow: hidden;
}}
[data-testid="stDownloadButton"] button {{
    background: {T["surface2"]} !important; border: 1px solid {T["border"]} !important;
    color: {T["muted"]} !important; border-radius: 8px !important;
    font-size: 0.8rem !important; font-weight: 500 !important;
    padding: 0.45rem 1rem !important; transition: all 0.15s ease;
}}
[data-testid="stDownloadButton"] button:hover {{
    border-color: {T["accent"]} !important; color: {T["text"]} !important;
}}
.card-title {{
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: {T["muted"]}; margin-bottom: 0.6rem;
}}
.callout {{
    border: 1px solid {T["border"]}; border-left: 3px solid {T["accent"]};
    border-radius: 0 10px 10px 0; background: {T["surface"]};
    padding: 0.85rem 1.1rem; font-size: 0.84rem; color: #94A3B8;
    line-height: 1.65; margin: 0.75rem 0;
}}
.callout.danger  {{ border-left-color: {T["danger"]}; }}
.callout.success {{ border-left-color: {T["success"]}; }}
.callout.warning {{ border-left-color: {T["warning"]}; }}
.callout strong  {{ color: {T["text"]}; }}
.pill {{
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 10px; border-radius: 999px; font-size: 0.72rem;
    font-weight: 600; letter-spacing: 0.04em;
}}
.pill-blue  {{ background: {T["accent"]}22; color: {T["accent"]}; border: 1px solid {T["accent"]}44; }}
.pill-green {{ background: {T["success"]}22; color: {T["success"]}; border: 1px solid {T["success"]}44; }}
.pill-red   {{ background: {T["danger"]}22; color: {T["danger"]}; border: 1px solid {T["danger"]}44; }}
.pill-amber {{ background: {T["warning"]}22; color: {T["warning"]}; border: 1px solid {T["warning"]}44; }}
.divider {{ border: none; border-top: 1px solid {T["border"]}; margin: 1.25rem 0; }}
.rank-row {{
    display: flex; align-items: center; gap: 10px;
    padding: 0.6rem 0.8rem; border-radius: 8px; margin-bottom: 4px;
    background: {T["surface2"]}; border: 1px solid {T["border"]};
    transition: border-color 0.15s;
}}
.rank-row:hover {{ border-color: {T["border2"]}; }}
.rank-num {{
    font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
    font-weight: 600; color: {T["muted"]}; width: 20px; text-align: center;
}}
.rank-label {{
    flex: 1; font-size: 0.82rem; font-weight: 500;
    color: {T["text"]}; text-transform: capitalize;
}}
.rank-bar-wrap {{
    width: 90px; height: 5px; background: {T["border"]};
    border-radius: 3px; overflow: hidden;
}}
.rank-bar {{ height: 100%; border-radius: 3px; }}
.rank-pct {{
    font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;
    font-weight: 600; width: 44px; text-align: right;
}}
.compact-table {{
    width: 100%; border-collapse: collapse; font-size: 0.82rem;
}}
.compact-table th {{
    text-align: left; font-size: 0.66rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase; color: {T["muted"]};
    padding: 0.4rem 0.5rem; border-bottom: 1px solid {T["border"]};
}}
.compact-table td {{
    padding: 0.45rem 0.5rem; color: #94A3B8;
    border-bottom: 1px solid {T["border"]}; vertical-align: middle;
}}
.compact-table tr:last-child td {{ border-bottom: none; }}
.compact-table tr:hover td {{ background: {T["surface2"]}; color: {T["text"]}; }}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# PLOTLY DEFAULTS
# ──────────────────────────────────────────────────────────────────
def base_layout(**kw):
    d = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=T["surface"],
        font=dict(family="Inter", color="#94A3B8", size=12),
        xaxis=dict(gridcolor=T["grid"], zerolinecolor=T["grid"],
                   linecolor=T["border"], showgrid=True, tickfont=dict(size=11)),
        yaxis=dict(gridcolor=T["grid"], zerolinecolor=T["grid"],
                   linecolor=T["border"], showgrid=True, tickfont=dict(size=11)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11, color="#94A3B8"), borderwidth=0),
        margin=dict(t=24, b=32, l=48, r=16),
        hoverlabel=dict(bgcolor=T["surface2"], bordercolor=T["border"],
                        font=dict(family="Inter", size=12, color=T["text"])),
    )
    d.update(kw)
    return d


# ──────────────────────────────────────────────────────────────────
# DATA
# ──────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    path = "data/bank-full.csv"
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path, sep=";")
    df["subscribed"] = (df["y"] == "yes").astype(int)
    bins   = [0, 30, 45, 60, 200]
    labels = ["18-30", "31-45", "46-60", "60+"]
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=True)
    df["lead_score"] = (
        (df["balance"] > df["balance"].median()).astype(int) * 30
        + (df["housing"] == "no").astype(int) * 25
        + (df["loan"] == "no").astype(int) * 20
        + df["job"].isin(["retired", "student"]).astype(int) * 25
    )
    return df

df_raw = load_data()

if df_raw is None:
    st.error("Dataset not found. Place `bank-full.csv` in the `data/` folder.")
    st.stop()

GLOBAL_RATE    = df_raw["subscribed"].mean() * 100
ALL_JOBS       = sorted(df_raw["job"].dropna().unique().tolist())
ALL_AGE_GROUPS = ["18-30", "31-45", "46-60", "60+"]
BAL_MIN        = int(df_raw["balance"].min())
BAL_MAX        = int(df_raw["balance"].max())


# ──────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;padding-bottom:0.75rem;
                border-bottom:1px solid {T['border']};margin-bottom:1rem;">
        <div style="width:36px;height:36px;border-radius:10px;
                    background:linear-gradient(135deg,{T['accent']},{T['accent2']});
                    display:flex;align-items:center;justify-content:center;
                    font-size:1.1rem;">&#127974;</div>
        <div>
            <div style="font-size:0.95rem;font-weight:700;color:{T['text']};">BankMind</div>
            <div style="font-size:0.68rem;color:{T['muted']};">Term Deposit Campaign</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    page = st.radio(
        "Navigation",
        ["Overview", "Who Buys?", "Money Matters", "Loan Drag",
         "Top Segments", "Find Leads"],
        label_visibility="collapsed",
    )

    st.markdown(f"<hr style='border-color:{T['border']};margin:0.75rem 0'>",
                unsafe_allow_html=True)

    # Filters
    preset = st.selectbox("Quick segment",
        ["Custom", "Best Leads", "Hard Sells", "Middle-Aged", "Loan-Free Only"])

    STEP = 500
    def snap(v):
        return int(BAL_MIN + round((v - BAL_MIN) / STEP) * STEP)

    if preset == "Best Leads":
        d_ages, d_jobs, d_bal = ["60+", "18-30"], ["retired", "student"], (snap(1000), BAL_MAX)
    elif preset == "Hard Sells":
        d_ages, d_jobs, d_bal = ["31-45", "46-60"], ["blue-collar", "services", "admin."], (BAL_MIN, snap(1000))
    elif preset == "Middle-Aged":
        d_ages, d_jobs, d_bal = ["31-45", "46-60"], ALL_JOBS, (BAL_MIN, BAL_MAX)
    elif preset == "Loan-Free Only":
        d_ages, d_jobs, d_bal = ALL_AGE_GROUPS, ALL_JOBS, (snap(0), BAL_MAX)
    else:
        d_ages, d_jobs, d_bal = ALL_AGE_GROUPS, ALL_JOBS, (BAL_MIN, BAL_MAX)

    sel_age  = st.multiselect("Age group", ALL_AGE_GROUPS, default=d_ages)
    sel_jobs = st.multiselect("Occupation", ALL_JOBS, default=d_jobs)
    sel_bal  = st.slider("Balance range", BAL_MIN, BAL_MAX, value=d_bal, step=STEP)

    col_h, col_l = st.columns(2)
    with col_h:
        no_mortgage = st.checkbox("No mortgage")
    with col_l:
        no_loan = st.checkbox("No personal loan")

    if not sel_age or not sel_jobs:
        st.warning("Select at least one age group and job.")
        st.stop()

    mask = (
        df_raw["age_group"].isin(sel_age)
        & df_raw["job"].isin(sel_jobs)
        & df_raw["balance"].between(*sel_bal)
    )
    if no_mortgage:
        mask &= df_raw["housing"] == "no"
    if no_loan:
        mask &= df_raw["loan"] == "no"
    df = df_raw[mask].copy()

    # Segment quality
    if len(df) > 0:
        seg_rate = df["subscribed"].mean() * 100
        if seg_rate >= GLOBAL_RATE * 1.5:
            sq_c, sq_w = T["success"], "Strong"
        elif seg_rate >= GLOBAL_RATE:
            sq_c, sq_w = T["warning"], "Decent"
        else:
            sq_c, sq_w = T["danger"], "Weak"
        st.markdown(f"""
        <div style="margin-top:0.75rem;background:{T['surface2']};border:1px solid {T['border']};
                    border-radius:10px;padding:0.8rem 1rem;">
            <div style="font-size:0.66rem;font-weight:700;letter-spacing:0.12em;
                        text-transform:uppercase;color:{T['muted']};margin-bottom:6px;">
                Segment Quality</div>
            <div style="display:flex;align-items:baseline;gap:8px;">
                <span style="font-family:'JetBrains Mono',monospace;font-size:1.5rem;
                             font-weight:700;color:{sq_c};line-height:1;">{seg_rate:.1f}%</span>
                <span style="font-size:0.75rem;color:{T['muted']};">sub. rate</span>
            </div>
            <div style="margin-top:6px;height:4px;background:{T['border']};border-radius:2px;overflow:hidden;">
                <div style="width:{min(100,seg_rate/40*100):.0f}%;height:100%;background:{sq_c};border-radius:2px;"></div>
            </div>
            <div style="margin-top:4px;font-size:0.7rem;color:{sq_c};font-weight:600;">
                {sq_w} &middot; {len(df):,} customers</div>
        </div>
        """, unsafe_allow_html=True)

    # User profile
    st.markdown(f"<hr style='border-color:{T['border']};margin:0.75rem 0'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;">
        <div style="width:32px;height:32px;border-radius:50%;background:{T['accent']};
                    display:flex;align-items:center;justify-content:center;
                    font-size:0.8rem;color:white;font-weight:700;">AA</div>
        <div>
            <div style="font-size:0.82rem;font-weight:600;color:{T['text']};">Abhinav Atul</div>
            <div style="font-size:0.68rem;color:{T['muted']};">Track A &middot; Analyst</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Guard
if len(df) == 0:
    st.warning("No customers match your current filters.")
    st.stop()

seg_rate   = df["subscribed"].mean() * 100
seg_vs_avg = seg_rate - GLOBAL_RATE


def page_header(title, desc):
    st.markdown(f"""
    <div style="padding:0 0 1rem 0;border-bottom:1px solid {T['border']};margin-bottom:1.25rem;">
        <div style="font-size:1.3rem;font-weight:700;color:{T['text']};letter-spacing:-0.02em;">{title}</div>
        <div style="font-size:0.8rem;color:{T['muted']};margin-top:2px;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════
if page == "Overview":
    d_color = T["success"] if seg_vs_avg >= 0 else T["danger"]
    arrow   = "+" if seg_vs_avg >= 0 else ""
    page_header("Overview",
        f"{len(df):,} customers from {len(df_raw):,} total | "
        f'<span style="color:{d_color};font-weight:600;">'
        f'{arrow}{seg_vs_avg:.1f}pp vs campaign average</span>')

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: st.metric("Customers", f"{len(df):,}", delta=f"{len(df)/len(df_raw)*100:.0f}% of total")
    with k2: st.metric("Subscription Rate", f"{seg_rate:.1f}%", delta=f"{seg_vs_avg:+.1f}pp vs avg")
    with k3: st.metric("Converted", f"{df['subscribed'].sum():,}")
    with k4: st.metric("Median Balance", f"EUR {df['balance'].median():,.0f}")
    with k5: st.metric("Avg Age", f"{df['age'].mean():.0f} yrs")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    left, right = st.columns([2, 3])

    with left:
        sub_yes = int(df["subscribed"].sum())
        sub_no  = len(df) - sub_yes
        fig_donut = go.Figure(go.Pie(
            values=[sub_no, sub_yes], labels=["Didn't subscribe", "Subscribed"],
            hole=0.68, sort=False, direction="clockwise",
            marker=dict(colors=[T["surface2"], T["accent"]], line=dict(color=T["bg"], width=3)),
            textinfo="none",
            hovertemplate="<b>%{label}</b><br>%{value:,} | %{percent}<extra></extra>",
        ))
        fig_donut.add_annotation(text=f"<b>{seg_rate:.1f}%</b>", x=0.5, y=0.55, showarrow=False,
                                  font=dict(size=26, color=T["text"], family="Inter"))
        fig_donut.add_annotation(text="subscribed", x=0.5, y=0.38, showarrow=False,
                                  font=dict(size=12, color=T["muted"], family="Inter"))
        fig_donut.update_layout(**base_layout(height=280, showlegend=False,
                                               margin=dict(t=8, b=8, l=8, r=8)))
        st.plotly_chart(fig_donut, width="stretch")

        st.markdown(f"""
        <div style="display:flex;flex-direction:column;gap:6px;">
            <div style="display:flex;align-items:center;justify-content:space-between;
                        padding:0.5rem 0.7rem;background:{T['surface2']};
                        border:1px solid {T['border']};border-radius:8px;">
                <span style="font-size:0.76rem;color:{T['muted']};">This segment</span>
                <span style="font-size:0.82rem;font-weight:700;color:{T['text']};">{seg_rate:.1f}%</span>
            </div>
            <div style="display:flex;align-items:center;justify-content:space-between;
                        padding:0.5rem 0.7rem;background:{T['surface2']};
                        border:1px solid {T['border']};border-radius:8px;">
                <span style="font-size:0.76rem;color:{T['muted']};">Campaign average</span>
                <span style="font-size:0.82rem;font-weight:700;color:{T['muted']};">{GLOBAL_RATE:.1f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        age_snap = df.groupby("age_group", observed=True)["subscribed"].agg(["mean","count","sum"]).reset_index()
        age_snap.columns = ["Age Group", "mean", "Total", "Subscribed"]
        age_snap["Rate"] = age_snap["mean"] * 100
        fig_age = go.Figure()
        for _, row in age_snap.iterrows():
            color = T["accent"] if row["Rate"] >= GLOBAL_RATE else T["muted"]
            fig_age.add_trace(go.Bar(x=[row["Age Group"]], y=[row["Rate"]], marker_color=color,
                                      marker_line_width=0, showlegend=False,
                                      hovertemplate=f"<b>{row['Age Group']}</b><br>{row['Rate']:.1f}%<br>"
                                                    f"{int(row['Subscribed']):,} / {int(row['Total']):,}<extra></extra>"))
        fig_age.add_hline(y=GLOBAL_RATE, line_dash="dot", line_color=T["warning"], line_width=1.5,
                          annotation_text=f"Campaign avg {GLOBAL_RATE:.1f}%",
                          annotation_font=dict(color=T["warning"], size=11))
        fig_age.update_layout(**base_layout(height=280, yaxis_ticksuffix="%",
                                             yaxis_range=[0, max(age_snap["Rate"].max()*1.3, GLOBAL_RATE*1.3)]))
        st.plotly_chart(fig_age, width="stretch")

        best = age_snap.sort_values("Rate", ascending=False).iloc[0]
        worst = age_snap.sort_values("Rate").iloc[0]
        cls = "success" if seg_rate >= GLOBAL_RATE else "danger"
        st.markdown(f"""
        <div class="callout {cls}">
            <strong>{best['Age Group']}</strong> customers subscribe at <strong>{best['Rate']:.1f}%</strong>
            {f"- {best['Rate']-worst['Rate']:.1f}pp higher than {worst['Age Group']}." if best['Rate']-worst['Rate'] > 1 else "- rates are fairly uniform."}
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: WHO BUYS?
# ══════════════════════════════════════════════════════════════════
elif page == "Who Buys?":
    page_header("Who Buys?", "Subscription rate by job, education, and contact history")

    job_df = df.groupby("job")["subscribed"].agg(["mean","count"]).rename(
        columns={"mean":"rate","count":"n"}).reset_index().sort_values("rate", ascending=False)
    job_df["rate_pct"] = job_df["rate"] * 100
    top_job, bot_job = job_df.iloc[0], job_df.iloc[-1]
    max_r = job_df["rate_pct"].max()

    rl, rr = st.columns([2, 3])
    with rl:
        st.markdown('<div class="card-title">Occupation ranking</div>', unsafe_allow_html=True)
        rows_html = ""
        for i, (_, row) in enumerate(job_df.iterrows()):
            bw = int(row["rate_pct"]/max_r*100)
            c = T["accent"] if row["rate_pct"] >= GLOBAL_RATE else T["muted"]
            rows_html += f"""<div class="rank-row"><div class="rank-num">#{i+1}</div>
                <div class="rank-label">{row['job']}</div>
                <div class="rank-bar-wrap"><div class="rank-bar" style="width:{bw}%;background:{c};"></div></div>
                <div class="rank-pct" style="color:{c};">{row['rate_pct']:.1f}%</div></div>"""
        st.markdown(rows_html, unsafe_allow_html=True)

    with rr:
        colors = [T["accent"] if r >= GLOBAL_RATE else "#2A3450" for r in job_df["rate_pct"]]
        fig_job = go.Figure(go.Bar(x=job_df["job"], y=job_df["rate_pct"], marker_color=colors,
            text=[f"{r:.0f}%" for r in job_df["rate_pct"]], textposition="outside",
            textfont=dict(size=10, color="#64748B"),
            hovertemplate="<b>%{x}</b><br>%{y:.1f}% | n=%{customdata:,}<extra></extra>",
            customdata=job_df["n"]))
        fig_job.add_hline(y=GLOBAL_RATE, line_dash="dot", line_color=T["warning"], line_width=1.5,
                          annotation_text=f"Avg {GLOBAL_RATE:.1f}%",
                          annotation_font=dict(color=T["warning"], size=10))
        fig_job.update_layout(**base_layout(height=340, yaxis_ticksuffix="%",
                                             yaxis_range=[0, max_r*1.3], xaxis_tickangle=-25))
        st.plotly_chart(fig_job, width="stretch")

    gap = top_job["rate_pct"] - bot_job["rate_pct"]
    st.markdown(f"""<div class="callout success"><b>{top_job['job'].title()}</b> converts at
        <b>{top_job['rate_pct']:.1f}%</b> - <b>{gap:.1f}pp</b> ahead of <b>{bot_job['job']}</b>
        ({bot_job['rate_pct']:.1f}%).</div>""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    bl, br = st.columns(2)
    with bl:
        st.markdown('<div class="card-title">Education level</div>', unsafe_allow_html=True)
        edu_df = df.groupby("education")["subscribed"].agg(["mean","count"]).rename(
            columns={"mean":"rate","count":"n"}).reset_index().sort_values("rate", ascending=True)
        edu_df["rate_pct"] = edu_df["rate"] * 100
        fig_edu = go.Figure(go.Bar(y=edu_df["education"], x=edu_df["rate_pct"], orientation="h",
            marker_color=[T["accent"] if r >= GLOBAL_RATE else "#2A3450" for r in edu_df["rate_pct"]],
            text=[f"{r:.1f}%" for r in edu_df["rate_pct"]], textposition="outside",
            textfont=dict(size=11, color="#64748B"),
            hovertemplate="<b>%{y}</b>: %{x:.1f}%<extra></extra>"))
        fig_edu.add_vline(x=GLOBAL_RATE, line_dash="dot", line_color=T["warning"], line_width=1)
        fig_edu.update_layout(**base_layout(height=220, xaxis_ticksuffix="%",
                                             xaxis_range=[0, edu_df["rate_pct"].max()*1.3]))
        st.plotly_chart(fig_edu, width="stretch")

    with br:
        st.markdown('<div class="card-title">Previous campaign outcome</div>', unsafe_allow_html=True)
        pout_df = df.groupby("poutcome")["subscribed"].agg(["mean","count"]).rename(
            columns={"mean":"rate","count":"n"}).reset_index().sort_values("rate", ascending=False)
        pout_df["rate_pct"] = pout_df["rate"] * 100
        cm = {"success": T["success"], "failure": T["danger"], "other": T["warning"], "unknown": "#2A3450"}
        fig_pout = go.Figure(go.Bar(x=pout_df["poutcome"], y=pout_df["rate_pct"],
            marker_color=[cm.get(p, T["accent"]) for p in pout_df["poutcome"]],
            text=[f"{r:.0f}%" for r in pout_df["rate_pct"]], textposition="outside",
            textfont=dict(size=11, color="#64748B"),
            hovertemplate="<b>%{x}</b>: %{y:.1f}%<br>n=%{customdata:,}<extra></extra>",
            customdata=pout_df["n"]))
        fig_pout.update_layout(**base_layout(height=220, yaxis_ticksuffix="%",
                                              yaxis_range=[0, pout_df["rate_pct"].max()*1.35]))
        st.plotly_chart(fig_pout, width="stretch")

        prev_s = pout_df[pout_df["poutcome"]=="success"]["rate_pct"]
        prev_u = pout_df[pout_df["poutcome"]=="unknown"]["rate_pct"]
        if not prev_s.empty and not prev_u.empty and prev_u.values[0] > 0:
            st.markdown(f"""<div class="callout success">Previous subscribers convert at
                <b>{prev_s.values[0]:.1f}%</b> - <b>{prev_s.values[0]/prev_u.values[0]:.1f}x</b>
                the rate of first-time contacts.</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: MONEY MATTERS
# ══════════════════════════════════════════════════════════════════
elif page == "Money Matters":
    page_header("Money Matters", "How account balance and financial health relate to conversion")

    cap = df["balance"].quantile(0.97)
    df_bal = df[df["balance"] < cap].copy()
    med_yes = df_bal[df_bal["subscribed"]==1]["balance"].median()
    med_no  = df_bal[df_bal["subscribed"]==0]["balance"].median()

    tr, br = st.columns([3, 2])
    with tr:
        st.markdown('<div class="card-title">Balance distribution</div>', unsafe_allow_html=True)
        fig_hist = go.Figure()
        for label, val, color in [("Subscribed",1,T["accent"]),("Not subscribed",0,T["danger"])]:
            d = df_bal[df_bal["subscribed"]==val]["balance"]
            fig_hist.add_trace(go.Histogram(x=d, name=label, nbinsx=70, marker_color=color,
                opacity=0.55, histnorm="probability density",
                hovertemplate=f"<b>{label}</b><br>EUR %{{x:,.0f}}<extra></extra>"))
        for val, color, lbl in [(med_yes,T["accent"],f"Median (sub) EUR {med_yes:,.0f}"),
                                 (med_no,T["danger"],f"Median (non) EUR {med_no:,.0f}")]:
            fig_hist.add_vline(x=val, line_dash="dash", line_color=color, line_width=1.5,
                               annotation_text=lbl, annotation_font=dict(color=color, size=10))
        fig_hist.update_layout(**base_layout(height=290, barmode="overlay",
                                              xaxis_title="Account balance (EUR)", yaxis_title="Density"))
        st.plotly_chart(fig_hist, width="stretch")

    with br:
        st.markdown('<div class="card-title">Balance quartile conversion</div>', unsafe_allow_html=True)
        df_bal2 = df_bal.copy()
        df_bal2["quartile"] = pd.qcut(df_bal2["balance"], 4,
            labels=["Bottom 25%","25-50%","50-75%","Top 25%"])
        q_rates = df_bal2.groupby("quartile", observed=True)["subscribed"].agg(["mean","count"]).reset_index()
        q_rates["rate_pct"] = q_rates["mean"] * 100
        cq = [T["danger"] if r < GLOBAL_RATE*0.8 else T["warning"] if r < GLOBAL_RATE else T["success"]
              for r in q_rates["rate_pct"]]
        fig_q = go.Figure(go.Bar(x=q_rates["quartile"].astype(str), y=q_rates["rate_pct"],
            marker_color=cq, text=[f"{r:.1f}%" for r in q_rates["rate_pct"]],
            textposition="outside", textfont=dict(size=11, color="#64748B"),
            hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>"))
        fig_q.add_hline(y=GLOBAL_RATE, line_dash="dot", line_color=T["warning"], line_width=1)
        fig_q.update_layout(**base_layout(height=290, yaxis_ticksuffix="%",
                                           yaxis_range=[0, q_rates["rate_pct"].max()*1.3]))
        st.plotly_chart(fig_q, width="stretch")

    top25 = q_rates[q_rates["quartile"]=="Top 25%"]["rate_pct"]
    bot25 = q_rates[q_rates["quartile"]=="Bottom 25%"]["rate_pct"]
    if not top25.empty and not bot25.empty and bot25.values[0] > 0:
        st.markdown(f"""<div class="callout">Median balance: subscribers <b>EUR {med_yes:,.0f}</b> vs
            non-subscribers <b>EUR {med_no:,.0f}</b>. Top quartile converts at
            <b>{top25.values[0]:.1f}%</b> - <b>{top25.values[0]/bot25.values[0]:.1f}x</b>
            higher than bottom quartile.</div>""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">Age vs balance (sampled 2,000)</div>', unsafe_allow_html=True)
    df_sample = df_bal.sample(min(2000, len(df_bal)), random_state=42)
    fig_sc = go.Figure()
    for label, val, color in [("Not subscribed",0,T["danger"]),("Subscribed",1,T["accent"])]:
        d = df_sample[df_sample["subscribed"]==val]
        fig_sc.add_trace(go.Scatter(x=d["age"], y=d["balance"], mode="markers", name=label,
            marker=dict(color=color, size=5, opacity=0.45, line=dict(width=0)),
            hovertemplate=f"<b>{label}</b><br>Age: %{{x}}<br>EUR %{{y:,.0f}}<extra></extra>"))
    fig_sc.update_layout(**base_layout(height=320, xaxis_title="Age",
                                        yaxis_title="Account balance (EUR)", yaxis_tickformat=","))
    st.plotly_chart(fig_sc, width="stretch")


# ══════════════════════════════════════════════════════════════════
# PAGE: LOAN DRAG
# ══════════════════════════════════════════════════════════════════
elif page == "Loan Drag":
    page_header("Loan Drag", "How existing debt burdens suppress new product uptake")

    loan_cross = df.groupby(["housing","loan"])["subscribed"].agg(["mean","count"]).reset_index()
    loan_cross["rate_pct"] = loan_cross["mean"] * 100
    loan_cross["label"] = loan_cross.apply(lambda r: (
        "No loans" if r["housing"]=="no" and r["loan"]=="no" else
        "Mortgage only" if r["housing"]=="yes" and r["loan"]=="no" else
        "Personal loan only" if r["housing"]=="no" and r["loan"]=="yes" else
        "Both loans"), axis=1)
    loan_cross = loan_cross.sort_values("rate_pct", ascending=False)
    top_rate = loan_cross.iloc[0]["rate_pct"]
    worst = loan_cross[loan_cross["label"]=="Both loans"]
    worst_r = worst["rate_pct"].values[0] if not worst.empty else 0
    drag = top_rate - worst_r

    ac, bc = st.columns([3, 2])
    with ac:
        st.markdown('<div class="card-title">Rate by debt profile</div>', unsafe_allow_html=True)
        fc = {"No loans":T["success"],"Mortgage only":T["warning"],"Personal loan only":T["warning"],"Both loans":T["danger"]}
        fig_loan = go.Figure(go.Bar(x=loan_cross["label"], y=loan_cross["rate_pct"],
            marker_color=[fc.get(l, T["accent"]) for l in loan_cross["label"]],
            text=[f"{r:.1f}%" for r in loan_cross["rate_pct"]],
            textposition="outside", textfont=dict(size=11, color="#64748B"),
            hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>"))
        fig_loan.add_hline(y=GLOBAL_RATE, line_dash="dot", line_color=T["warning"], line_width=1.5,
                           annotation_text=f"Avg {GLOBAL_RATE:.1f}%",
                           annotation_font=dict(color=T["warning"], size=10))
        fig_loan.update_layout(**base_layout(height=340, yaxis_ticksuffix="%",
                                              yaxis_range=[0, top_rate*1.35]))
        st.plotly_chart(fig_loan, width="stretch")

    with bc:
        st.markdown('<div class="card-title">Heatmap</div>', unsafe_allow_html=True)
        pivot = loan_cross.pivot_table(index="housing", columns="loan", values="rate_pct")
        pivot = pivot.rename(index={"yes":"Has mortgage","no":"No mortgage"},
                              columns={"yes":"Has personal loan","no":"No personal loan"})
        fig_hm = go.Figure(go.Heatmap(z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
            colorscale=[[0,T["danger"]],[0.5,T["warning"]],[1,T["success"]]],
            text=[[f"{v:.1f}%" for v in row] for row in pivot.values], texttemplate="%{text}",
            textfont=dict(size=16, color="white", family="Inter"), showscale=False,
            hovertemplate="<b>%{y} / %{x}</b><br>%{z:.1f}%<extra></extra>"))
        fig_hm.update_layout(**base_layout(height=220, margin=dict(t=16,b=16,l=16,r=16),
            xaxis=dict(showgrid=False, tickfont=dict(size=11)),
            yaxis=dict(showgrid=False, tickfont=dict(size=11))))
        st.plotly_chart(fig_hm, width="stretch")

        nl_r = loan_cross[loan_cross["label"]=="No loans"]["rate_pct"]
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px;">
            <div style="background:{T['success']}22;border:1px solid {T['success']}44;
                        border-radius:8px;padding:0.55rem 0.75rem;">
                <div style="font-size:0.65rem;color:{T['success']};font-weight:700;
                            text-transform:uppercase;">No loans</div>
                <div style="font-size:1.2rem;font-weight:700;color:{T['text']};
                            font-family:'JetBrains Mono',monospace;">{nl_r.values[0]:.1f}%</div>
            </div>
            <div style="background:{T['danger']}22;border:1px solid {T['danger']}44;
                        border-radius:8px;padding:0.55rem 0.75rem;">
                <div style="font-size:0.65rem;color:{T['danger']};font-weight:700;
                            text-transform:uppercase;">Both loans</div>
                <div style="font-size:1.2rem;font-weight:700;color:{T['text']};
                            font-family:'JetBrains Mono',monospace;">{worst_r:.1f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""<div class="callout danger">No-loan customers convert at <b>{top_rate:.1f}%</b> -
        a <b>{drag:.1f}pp gap</b> over dual-loan customers ({worst_r:.1f}%).
        Filter out dual-loan customers when building call lists.</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# PAGE: TOP SEGMENTS
# ══════════════════════════════════════════════════════════════════
elif page == "Top Segments":
    page_header("Top Segments", "Ranked combinations - where to focus outreach")

    seg_df = df.groupby(["job","age_group","housing"], observed=True)["subscribed"].agg(
        ["mean","count","sum"]).reset_index().rename(columns={"mean":"rate","count":"n","sum":"subscribers"})
    seg_df["rate_pct"] = seg_df["rate"] * 100
    seg_df = seg_df[seg_df["n"] >= 30].sort_values("rate_pct", ascending=False)

    tl, trr = st.columns(2)
    with tl:
        st.markdown(f'<div class="card-title" style="color:{T["success"]};">Best converting</div>',
                    unsafe_allow_html=True)
        rows = ""
        for i, (_, row) in enumerate(seg_df.head(12).iterrows()):
            bw = int(row["rate_pct"]/seg_df["rate_pct"].max()*100)
            label = f"{row['job'].title()}, {row['age_group']}, {'No mortgage' if row['housing']=='no' else 'Mortgage'}"
            rows += f"""<tr><td style="font-weight:600;color:{T['text']};">#{i+1}</td><td>{label}</td>
                <td><div style="display:flex;align-items:center;gap:6px;">
                    <div style="width:60px;height:4px;background:{T['border']};border-radius:2px;overflow:hidden;">
                        <div style="width:{bw}%;height:100%;background:{T['success']};border-radius:2px;"></div></div>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;
                                 font-weight:700;color:{T['success']};">{row['rate_pct']:.1f}%</span></div></td>
                <td style="color:{T['muted']};text-align:right;font-size:0.76rem;">{row['n']:,}</td></tr>"""
        st.markdown(f"""<table class="compact-table"><thead><tr><th>#</th><th>Segment</th>
            <th>Rate</th><th>Size</th></tr></thead><tbody>{rows}</tbody></table>""", unsafe_allow_html=True)

    with trr:
        st.markdown(f'<div class="card-title" style="color:{T["danger"]};">Hardest to convert</div>',
                    unsafe_allow_html=True)
        rows2 = ""
        for _, row in seg_df.tail(8).iterrows():
            label = f"{row['job'].title()}, {row['age_group']}, {'No mortgage' if row['housing']=='no' else 'Mortgage'}"
            rows2 += f"""<tr><td>{label}</td>
                <td><span style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;
                    font-weight:600;color:{T['danger']};">{row['rate_pct']:.1f}%</span></td>
                <td style="color:{T['muted']};font-size:0.76rem;">{row['n']:,}</td></tr>"""
        st.markdown(f"""<table class="compact-table"><thead><tr><th>Segment</th><th>Rate</th>
            <th>Size</th></tr></thead><tbody>{rows2}</tbody></table>""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">All segments - size vs conversion</div>', unsafe_allow_html=True)
    fig_b = go.Figure()
    for _, row in seg_df.iterrows():
        color = T["success"] if row["rate_pct"] >= GLOBAL_RATE*1.5 else T["warning"] if row["rate_pct"] >= GLOBAL_RATE else T["danger"]
        fig_b.add_trace(go.Scatter(x=[row["n"]], y=[row["rate_pct"]], mode="markers",
            marker=dict(size=max(6, min(30, row["n"]/30)), color=color, opacity=0.65, line=dict(width=0)),
            hovertemplate=f"<b>{row['job'].title()}, {row['age_group']}</b><br>{row['rate_pct']:.1f}%<br>n={row['n']:,}<extra></extra>",
            showlegend=False))
    fig_b.add_hline(y=GLOBAL_RATE, line_dash="dot", line_color=T["warning"], line_width=1.5,
                    annotation_text=f"Avg {GLOBAL_RATE:.1f}%", annotation_font=dict(color=T["warning"], size=10))
    fig_b.update_layout(**base_layout(height=320, xaxis_title="Segment size", yaxis_title="Rate (%)",
                                       yaxis_ticksuffix="%"))
    st.plotly_chart(fig_b, width="stretch")


# ══════════════════════════════════════════════════════════════════
# PAGE: FIND LEADS
# ══════════════════════════════════════════════════════════════════
elif page == "Find Leads":
    page_header("Find Leads", "Search, score, and export individual customers")

    c1, c2, c3 = st.columns(3)
    with c1: outcome_f = st.selectbox("Outcome", ["All","Subscribed only","Didn't subscribe"])
    with c2: housing_f = st.selectbox("Mortgage", ["Any","No mortgage","Has mortgage"])
    with c3: sort_col = st.selectbox("Sort by", ["Lead score","Balance (high to low)","Age"])

    df_leads = df.copy()
    if outcome_f == "Subscribed only": df_leads = df_leads[df_leads["y"]=="yes"]
    elif outcome_f == "Didn't subscribe": df_leads = df_leads[df_leads["y"]=="no"]
    if housing_f == "No mortgage": df_leads = df_leads[df_leads["housing"]=="no"]
    elif housing_f == "Has mortgage": df_leads = df_leads[df_leads["housing"]=="yes"]

    if sort_col == "Lead score": df_leads = df_leads.sort_values("lead_score", ascending=False)
    elif sort_col == "Balance (high to low)": df_leads = df_leads.sort_values("balance", ascending=False)
    else: df_leads = df_leads.sort_values("age")

    st.markdown(f"""
    <div style="display:flex;gap:14px;margin-bottom:1rem;align-items:center;flex-wrap:wrap;">
        <span style="font-size:0.84rem;color:{T['muted']};">
            <b style="color:{T['text']};font-family:'JetBrains Mono',monospace;">{len(df_leads):,}</b> matched</span>
        <span class="pill pill-blue">{df_leads['subscribed'].mean()*100:.1f}% conversion</span>
        <span class="pill pill-green">Avg score: {df_leads['lead_score'].mean():.0f}/100</span>
    </div>
    """, unsafe_allow_html=True)

    display = df_leads[["age","job","marital","education","balance","housing","loan",
                         "age_group","lead_score","y"]].head(500).copy()
    display.columns = ["Age","Job","Marital","Education","Balance","Mortgage",
                       "Personal Loan","Age Group","Lead Score","Subscribed"]
    st.dataframe(display, width="stretch", height=400,
        column_config={
            "Balance": st.column_config.NumberColumn(format="%d EUR"),
            "Lead Score": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d"),
        })

    csv_data = display.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered leads as CSV", data=csv_data,
                        file_name=f"bankmind_leads_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">Lead score distribution</div>', unsafe_allow_html=True)
    fig_ls = go.Figure()
    for label, val, color in [("Didn't subscribe",0,T["danger"]),("Subscribed",1,T["accent"])]:
        d = df_leads[df_leads["subscribed"]==val]["lead_score"]
        fig_ls.add_trace(go.Histogram(x=d, name=label, nbinsx=20, marker_color=color, opacity=0.6,
            hovertemplate=f"<b>{label}</b><br>Score: %{{x}}<extra></extra>"))
    fig_ls.update_layout(**base_layout(height=240, barmode="overlay",
                                        xaxis_title="Lead score (0-100)", yaxis_title="Customers"))
    st.plotly_chart(fig_ls, width="stretch")

    st.markdown(f"""<div class="callout"><b>Lead score:</b> Each customer scored out of 100 -
        <b>high balance (+30)</b>, <b>no mortgage (+25)</b>, <b>no personal loan (+20)</b>,
        <b>retired/student (+25)</b>. High-score customers are worth calling first.</div>""",
        unsafe_allow_html=True)
