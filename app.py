"""
app.py — BankMind, Track A
Rebuilt dashboard: opinionated, RM-centric, story-driven.
"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

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
# DESIGN SYSTEM
# ──────────────────────────────────────────────────────────────────
C = {
    "bg":         "#080C14",
    "surface":    "#0D1220",
    "surface2":   "#111827",
    "border":     "#1C2538",
    "border2":    "#243048",
    "text":       "#E2E8F0",
    "muted":      "#64748B",
    "accent":     "#3B82F6",
    "accent2":    "#8B5CF6",
    "success":    "#10B981",
    "danger":     "#EF4444",
    "warning":    "#F59E0B",
    "yes":        "#3B82F6",
    "no":         "#EF4444",
    "grid":       "#1C2538",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* ── Global font ── */
/* NOTE: we exclude stIconMaterial spans from this rule.
   Our !important Inter override strips the Material Symbols Rounded font
   that Streamlit sets on icon elements, causing ligature text to show raw. */
*, html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}}

/* ── Restore Material Symbols font on icon spans ── */
/* Specificity of [data-testid] (0,1,0) beats * (0,0,0) when both use !important */
[data-testid="stIconMaterial"] {{
    font-family: 'Material Symbols Rounded' !important;
    font-size: 20px !important;
    font-style: normal !important;
    font-weight: 400 !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    word-break: normal !important;
    -webkit-font-feature-settings: 'liga';
    font-feature-settings: 'liga';
}}

/* ── Backgrounds ── */
.stApp {{
    background: {C["bg"]};
}}
section[data-testid="stSidebar"] {{
    background: {C["surface"]} !important;
    border-right: 1px solid {C["border"]} !important;
}}
.block-container {{
    padding: 4.5rem 2rem 3rem 2rem !important;
    max-width: 1400px;
}}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {{
    gap: 4px;
    border-bottom: 1px solid {C["border"]};
    padding-bottom: 0;
    background: transparent;
}}
[data-testid="stTabs"] button[role="tab"] {{
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    color: {C["muted"]} !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em;
    padding: 0.5rem 0.9rem !important;
    margin-bottom: -1px;
    transition: all 0.15s ease;
}}
[data-testid="stTabs"] button[role="tab"]:hover {{
    color: {C["text"]} !important;
    border-bottom-color: {C["border2"]} !important;
}}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
    color: {C["accent"]} !important;
    border-bottom-color: {C["accent"]} !important;
    font-weight: 600 !important;
}}

/* ── Metric overrides ── */
[data-testid="stMetric"] {{
    background: {C["surface2"]};
    border: 1px solid {C["border"]};
    border-radius: 12px;
    padding: 1rem 1.2rem !important;
}}
[data-testid="stMetricLabel"] {{
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: {C["muted"]} !important;
}}
[data-testid="stMetricValue"] {{
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    color: {C["text"]} !important;
}}
[data-testid="stMetricDelta"] {{
    font-size: 0.78rem !important;
}}
[data-testid="stMetricDelta"] svg {{
    display: none;
}}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{
    border: 1px solid {C["border"]};
    border-radius: 10px;
    overflow: hidden;
}}
[data-testid="stDataFrame"] th {{
    background: {C["surface"]} !important;
    color: {C["muted"]} !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}}

/* ── Selectbox / Multiselect ── */
[data-testid="stMultiSelect"] [data-baseweb="select"] div,
[data-testid="stSelectbox"] [data-baseweb="select"] div {{
    background: {C["surface2"]} !important;
    border-color: {C["border"]} !important;
    color: {C["text"]} !important;
    font-size: 0.83rem !important;
}}

/* ── Slider ── */
[data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stSliderThumb"] {{
    background: {C["accent"]} !important;
}}

/* ── Custom components ── */
.stat-row {{
    display: flex;
    gap: 12px;
    margin: 1rem 0;
}}
.pill {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
}}
.pill-blue  {{ background: {C["accent"]}22; color: {C["accent"]}; border: 1px solid {C["accent"]}44; }}
.pill-red   {{ background: {C["danger"]}22; color: {C["danger"]}; border: 1px solid {C["danger"]}44; }}
.pill-green {{ background: {C["success"]}22; color: {C["success"]}; border: 1px solid {C["success"]}44; }}
.pill-amber {{ background: {C["warning"]}22; color: {C["warning"]}; border: 1px solid {C["warning"]}44; }}

.callout {{
    border: 1px solid {C["border"]};
    border-left: 3px solid {C["accent"]};
    border-radius: 0 10px 10px 0;
    background: {C["surface"]};
    padding: 0.85rem 1.1rem;
    font-size: 0.84rem;
    color: #94A3B8;
    line-height: 1.65;
    margin: 0.75rem 0;
}}
.callout.danger  {{ border-left-color: {C["danger"]}; }}
.callout.success {{ border-left-color: {C["success"]}; }}
.callout.warning {{ border-left-color: {C["warning"]}; }}
.callout strong, .callout b {{ color: {C["text"]}; }}

.section-label {{
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {C["muted"]};
    margin-bottom: 0.5rem;
}}

.rank-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.7rem 0.9rem;
    border-radius: 8px;
    margin-bottom: 6px;
    background: {C["surface2"]};
    border: 1px solid {C["border"]};
    transition: border-color 0.15s;
}}
.rank-row:hover {{ border-color: {C["border2"]}; }}
.rank-num {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    color: {C["muted"]};
    width: 22px;
    text-align: center;
}}
.rank-label {{
    flex: 1;
    font-size: 0.85rem;
    font-weight: 500;
    color: {C["text"]};
    text-transform: capitalize;
}}
.rank-bar-wrap {{
    width: 120px;
    height: 6px;
    background: {C["border"]};
    border-radius: 3px;
    overflow: hidden;
}}
.rank-bar {{
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, {C["accent"]}, {C["accent2"]});
}}
.rank-pct {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    color: {C["text"]};
    width: 46px;
    text-align: right;
}}

.divider {{
    border: none;
    border-top: 1px solid {C["border"]};
    margin: 1.25rem 0;
}}

.sidebar-section {{
    background: {C["surface2"]};
    border: 1px solid {C["border"]};
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.75rem;
}}

/* Score badge */
.score-badge {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(135deg, #0F172A, #0D1220);
    border: 1px solid {C["border"]};
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-top: 0.5rem;
}}
.score-number {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: {C["text"]};
    line-height: 1;
}}
.score-label {{
    font-size: 0.7rem;
    color: {C["muted"]};
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 2px;
}}

/* Heatmap legend */
.legend-strip {{
    height: 8px;
    border-radius: 4px;
    background: linear-gradient(90deg, {C["danger"]}, {C["warning"]}, {C["success"]});
    margin: 0.25rem 0;
}}

/* Header */
.page-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 1.25rem 0;
    border-bottom: 1px solid {C["border"]};
    margin-bottom: 1.5rem;
}}
.page-title {{
    font-size: 1.35rem;
    font-weight: 700;
    color: {C["text"]};
    letter-spacing: -0.02em;
}}
.page-desc {{
    font-size: 0.8rem;
    color: {C["muted"]};
    margin-top: 2px;
}}

/* Compact table */
.compact-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.83rem;
}}
.compact-table th {{
    text-align: left;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: {C["muted"]};
    padding: 0.4rem 0.6rem;
    border-bottom: 1px solid {C["border"]};
}}
.compact-table td {{
    padding: 0.5rem 0.6rem;
    color: #94A3B8;
    border-bottom: 1px solid {C["border"]};
    vertical-align: middle;
}}
.compact-table tr:last-child td {{ border-bottom: none; }}
.compact-table tr:hover td {{ background: {C["surface2"]}; color: {C["text"]}; }}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# PLOTLY BASE LAYOUT
# ──────────────────────────────────────────────────────────────────
def base_layout(**kwargs):
    defaults = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=C["surface"],
        font=dict(family="Inter", color="#94A3B8", size=12),
        xaxis=dict(
            gridcolor=C["grid"], gridwidth=1,
            zerolinecolor=C["grid"], linecolor=C["border"],
            showgrid=True, tickfont=dict(size=11),
        ),
        yaxis=dict(
            gridcolor=C["grid"], gridwidth=1,
            zerolinecolor=C["grid"], linecolor=C["border"],
            showgrid=True, tickfont=dict(size=11),
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11, color="#94A3B8"),
            borderwidth=0,
        ),
        margin=dict(t=24, b=32, l=48, r=16),
        hoverlabel=dict(
            bgcolor=C["surface2"],
            bordercolor=C["border"],
            font=dict(family="Inter", size=12, color=C["text"]),
        ),
    )
    defaults.update(kwargs)
    return defaults


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
    labels = ["18–30", "31–45", "46–60", "60+"]
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=True)
    # Simple lead score: reward high balance, no loans, retired/student
    df["lead_score"] = (
        (df["balance"] > df["balance"].median()).astype(int) * 30
        + (df["housing"] == "no").astype(int) * 25
        + (df["loan"] == "no").astype(int) * 20
        + df["job"].isin(["retired", "student"]).astype(int) * 25
    )
    return df


df_raw = load_data()

if df_raw is None:
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:center;
                height:60vh;flex-direction:column;gap:1rem;">
        <div style="font-size:2.5rem;">📂</div>
        <div style="font-size:1.1rem;font-weight:600;color:{C["text"]};">Dataset not found</div>
        <div style="font-size:0.85rem;color:{C["muted"]};text-align:center;max-width:400px;">
            Download <code>bank-full.csv</code> from the
            <a href="https://archive.ics.uci.edu/dataset/222/bank+marketing"
               style="color:{C["accent"]};">UCI Bank Marketing Dataset</a>
            and place it in the <code>data/</code> folder.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

GLOBAL_RATE = df_raw["subscribed"].mean() * 100
ALL_JOBS       = sorted(df_raw["job"].dropna().unique().tolist())
ALL_AGE_GROUPS = ["18–30", "31–45", "46–60", "60+"]
BAL_MIN = int(df_raw["balance"].min())
BAL_MAX = int(df_raw["balance"].max())


# ──────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:0 0 1rem 0;">
        <div style="font-size:1.05rem;font-weight:700;color:{C['text']};letter-spacing:-0.01em;">
            🏦 BankMind
        </div>
        <div style="font-size:0.72rem;color:{C['muted']};margin-top:2px;">
            Term Deposit Campaign · UCI Dataset
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick presets ──
    st.markdown('<div class="section-label">Quick Segment</div>', unsafe_allow_html=True)
    preset = st.selectbox(
        "preset",
        ["Custom", "Best Leads", "Hard Sells", "Middle-Aged", "Loan-Free Only"],
        label_visibility="collapsed",
    )

    # Snap a value to the nearest multiple of STEP from BAL_MIN
    # so the slider never gets a value that falls between steps.
    STEP = 500
    def snap(v):
        return int(BAL_MIN + round((v - BAL_MIN) / STEP) * STEP)

    if preset == "Best Leads":
        default_ages = ["60+", "18–30"]
        default_jobs = ["retired", "student"]
        default_bal  = (snap(1000), BAL_MAX)
    elif preset == "Hard Sells":
        default_ages = ["31–45", "46–60"]
        default_jobs = ["blue-collar", "services", "admin."]
        default_bal  = (BAL_MIN, snap(1000))
    elif preset == "Middle-Aged":
        default_ages = ["31–45", "46–60"]
        default_jobs = ALL_JOBS
        default_bal  = (BAL_MIN, BAL_MAX)
    elif preset == "Loan-Free Only":
        default_ages = ALL_AGE_GROUPS
        default_jobs = ALL_JOBS
        default_bal  = (snap(0), BAL_MAX)
    else:
        default_ages = ALL_AGE_GROUPS
        default_jobs = ALL_JOBS
        default_bal  = (BAL_MIN, BAL_MAX)

    st.markdown("<hr style='border-color:#1C2538;margin:0.75rem 0'>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Age Group</div>', unsafe_allow_html=True)
    sel_age = st.multiselect("age", ALL_AGE_GROUPS, default=default_ages,
                              label_visibility="collapsed")

    st.markdown('<div class="section-label" style="margin-top:0.6rem;">Occupation</div>',
                unsafe_allow_html=True)
    sel_jobs = st.multiselect("job", ALL_JOBS, default=default_jobs,
                               label_visibility="collapsed")

    st.markdown('<div class="section-label" style="margin-top:0.6rem;">Account Balance (€)</div>',
                unsafe_allow_html=True)
    sel_bal = st.slider("bal", BAL_MIN, BAL_MAX, value=default_bal,
                         step=STEP, label_visibility="collapsed")

    st.markdown("<hr style='border-color:#1C2538;margin:0.75rem 0'>", unsafe_allow_html=True)

    # ── Housing / Loan toggles ──
    st.markdown('<div class="section-label">Loan Status</div>', unsafe_allow_html=True)
    col_h, col_l = st.columns(2)
    with col_h:
        housing_only = st.checkbox("No mortgage", value=False)
    with col_l:
        loan_only = st.checkbox("No personal loan", value=False)

    st.markdown("<hr style='border-color:#1C2538;margin:0.75rem 0'>", unsafe_allow_html=True)

    # Apply filters
    if not sel_age or not sel_jobs:
        st.warning("Pick at least one age group and job type.")
        st.stop()

    mask = (
        df_raw["age_group"].isin(sel_age)
        & df_raw["job"].isin(sel_jobs)
        & df_raw["balance"].between(*sel_bal)
    )
    if housing_only:
        mask &= df_raw["housing"] == "no"
    if loan_only:
        mask &= df_raw["loan"] == "no"
    df = df_raw[mask].copy()

    # ── Segment quality score ──
    if len(df) > 0:
        seg_rate  = df["subscribed"].mean() * 100
        seg_score = min(100, int((seg_rate / GLOBAL_RATE) * 50))
        if seg_rate >= GLOBAL_RATE * 1.5:
            score_color  = C["success"]
            score_word   = "Strong"
        elif seg_rate >= GLOBAL_RATE:
            score_color  = C["warning"]
            score_word   = "Decent"
        else:
            score_color  = C["danger"]
            score_word   = "Weak"

        st.markdown(f"""
        <div style="background:{C['surface2']};border:1px solid {C['border']};
                    border-radius:10px;padding:0.85rem 1rem;">
            <div class="section-label">Segment Quality</div>
            <div style="display:flex;align-items:baseline;gap:8px;margin-top:6px;">
                <span style="font-family:'JetBrains Mono',monospace;font-size:1.7rem;
                             font-weight:700;color:{score_color};line-height:1;">
                    {seg_rate:.1f}%
                </span>
                <span style="font-size:0.8rem;color:{C['muted']};">sub. rate</span>
            </div>
            <div style="margin-top:6px;height:5px;background:{C['border']};border-radius:3px;overflow:hidden;">
                <div style="width:{min(100, seg_rate/40*100):.0f}%;height:100%;
                            background:{score_color};border-radius:3px;"></div>
            </div>
            <div style="margin-top:5px;font-size:0.72rem;color:{score_color};font-weight:600;">
                {score_word} · {len(df):,} customers in segment
            </div>
        </div>
        """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────
# GUARD
# ──────────────────────────────────────────────────────────────────
if len(df) == 0:
    st.warning("No customers match your current filters.")
    st.stop()

seg_rate   = df["subscribed"].mean() * 100
seg_vs_avg = seg_rate - GLOBAL_RATE

# ──────────────────────────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Snapshot",
    "Who buys?",
    "Money matters",
    "Loan drag",
    "Top segments",
    "Find leads",
])
tab_snap, tab_who, tab_money, tab_loans, tab_segs, tab_leads = tabs


# ════════════════════════════════════════════════════════════════
# TAB 1 — SNAPSHOT
# ════════════════════════════════════════════════════════════════
with tab_snap:
    direction = "above" if seg_vs_avg >= 0 else "below"
    arrow     = "↑" if seg_vs_avg >= 0 else "↓"
    d_color   = C["success"] if seg_vs_avg >= 0 else C["danger"]

    st.markdown(f"""
    <div class="page-header">
        <div>
            <div class="page-title">Segment Snapshot</div>
            <div class="page-desc">
                {len(df):,} customers · filtered from {len(df_raw):,} total ·
                <span style="color:{d_color};font-weight:600;">
                    {arrow} {abs(seg_vs_avg):.1f}pp {direction} campaign average
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI row ──
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Customers", f"{len(df):,}",
                  delta=f"{len(df)/len(df_raw)*100:.0f}% of total")
    with k2:
        st.metric("Subscription rate", f"{seg_rate:.1f}%",
                  delta=f"{seg_vs_avg:+.1f}pp vs avg")
    with k3:
        st.metric("Converted", f"{df['subscribed'].sum():,}")
    with k4:
        st.metric("Median balance", f"€{df['balance'].median():,.0f}")
    with k5:
        st.metric("Avg age", f"{df['age'].mean():.0f} yrs")

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    left, right = st.columns([2, 3])

    # ── Donut ──
    with left:
        sub_yes = int(df["subscribed"].sum())
        sub_no  = len(df) - sub_yes

        fig_donut = go.Figure(go.Pie(
            values=[sub_no, sub_yes],
            labels=["Didn't subscribe", "Subscribed"],
            hole=0.68,
            sort=False,
            direction="clockwise",
            marker=dict(
                colors=[C["surface2"], C["accent"]],
                line=dict(color=C["bg"], width=3),
            ),
            textinfo="none",
            hovertemplate="<b>%{label}</b><br>%{value:,} customers · %{percent}<extra></extra>",
        ))
        fig_donut.add_annotation(
            text=f"<b>{seg_rate:.1f}%</b>",
            x=0.5, y=0.55, showarrow=False,
            font=dict(size=26, color=C["text"], family="Inter"),
        )
        fig_donut.add_annotation(
            text="subscribed",
            x=0.5, y=0.38, showarrow=False,
            font=dict(size=12, color=C["muted"], family="Inter"),
        )
        fig_donut.update_layout(**base_layout(height=280, showlegend=False,
                                               margin=dict(t=8, b=8, l=8, r=8)))
        st.plotly_chart(fig_donut, width='stretch')

        # Segment vs campaign context
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;gap:8px;">
            <div style="display:flex;align-items:center;justify-content:space-between;
                        padding:0.55rem 0.75rem;background:{C['surface2']};
                        border:1px solid {C['border']};border-radius:8px;">
                <span style="font-size:0.78rem;color:{C['muted']};">This segment</span>
                <span style="font-size:0.85rem;font-weight:700;color:{C['text']};">{seg_rate:.1f}%</span>
            </div>
            <div style="display:flex;align-items:center;justify-content:space-between;
                        padding:0.55rem 0.75rem;background:{C['surface2']};
                        border:1px solid {C['border']};border-radius:8px;">
                <span style="font-size:0.78rem;color:{C['muted']};">Campaign average</span>
                <span style="font-size:0.85rem;font-weight:700;color:{C['muted']};">{GLOBAL_RATE:.1f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Subscription by age group within segment ──
    with right:
        age_snap = (
            df.groupby("age_group", observed=True)["subscribed"]
            .agg(["mean", "count", "sum"])
            .reset_index()
        )
        age_snap["rate_pct"] = age_snap["mean"] * 100
        age_snap.columns     = ["Age Group", "mean", "Total", "Subscribed", "Rate"]

        fig_age = go.Figure()
        max_r   = age_snap["Rate"].max()
        for _, row in age_snap.iterrows():
            pct = row["Rate"] / max_r if max_r else 0
            color = C["accent"] if row["Rate"] >= GLOBAL_RATE else C["muted"]
            fig_age.add_trace(go.Bar(
                x=[row["Age Group"]],
                y=[row["Rate"]],
                name=row["Age Group"],
                marker_color=color,
                marker_line_width=0,
                hovertemplate=(
                    f"<b>{row['Age Group']}</b><br>"
                    f"Rate: {row['Rate']:.1f}%<br>"
                    f"Subscribers: {int(row['Subscribed']):,} / {int(row['Total']):,}"
                    "<extra></extra>"
                ),
            ))

        # Campaign average line
        fig_age.add_hline(
            y=GLOBAL_RATE, line_dash="dot", line_color=C["warning"], line_width=1.5,
            annotation_text=f"Campaign avg {GLOBAL_RATE:.1f}%",
            annotation_position="top right",
            annotation_font=dict(color=C["warning"], size=11),
        )
        fig_age.update_layout(
            **base_layout(height=280, showlegend=False,
                          yaxis_ticksuffix="%", yaxis_title="Subscription rate",
                          xaxis_title="",
                          yaxis_range=[0, max(age_snap["Rate"].max() * 1.3, GLOBAL_RATE * 1.3)]),
        )
        st.plotly_chart(fig_age, width='stretch')

        # Dynamic callout
        best_age  = age_snap.sort_values("Rate", ascending=False).iloc[0]
        worst_age = age_snap.sort_values("Rate").iloc[0]
        diff_pct  = best_age["Rate"] - worst_age["Rate"]
        cls       = "success" if seg_rate >= GLOBAL_RATE else "danger"
        st.markdown(f"""
        <div class="callout {cls}">
            In this segment, <strong>{best_age['Age Group']}</strong> customers subscribe
            at <strong>{best_age['Rate']:.1f}%</strong> — 
            {f"{diff_pct:.1f}pp higher than {worst_age['Age Group']} ({worst_age['Rate']:.1f}%)."
             if diff_pct > 1 else "rates are fairly uniform across age groups."}
            {'Your segment beats the campaign average — good targeting.' 
             if seg_rate >= GLOBAL_RATE 
             else f'This segment is {abs(seg_vs_avg):.1f}pp below campaign average. Adjust filters to find warmer leads.'}
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# TAB 2 — WHO BUYS?
# ════════════════════════════════════════════════════════════════
with tab_who:
    st.markdown(f"""
    <div class="page-header">
        <div>
            <div class="page-title">Who buys?</div>
            <div class="page-desc">Subscription rate by job, education, and contact history</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Job ranking ──
    job_df = (
        df.groupby("job")["subscribed"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "rate", "count": "n"})
        .reset_index()
        .sort_values("rate", ascending=False)
    )
    job_df["rate_pct"] = job_df["rate"] * 100
    top_job = job_df.iloc[0]
    bot_job = job_df.iloc[-1]
    max_r   = job_df["rate_pct"].max()

    st.markdown('<div class="section-label">Subscription rate by occupation</div>',
                unsafe_allow_html=True)

    # Ranked list (HTML) + bar chart side by side
    r_left, r_right = st.columns([2, 3])

    with r_left:
        rows_html = ""
        for i, row in job_df.iterrows():
            bar_w  = int(row["rate_pct"] / max_r * 100)
            is_top = row["rate_pct"] >= GLOBAL_RATE
            color  = C["accent"] if is_top else C["muted"]
            rank_i = job_df.index.get_loc(i) + 1
            rows_html += f"""
            <div class="rank-row">
                <div class="rank-num">#{rank_i}</div>
                <div class="rank-label">{row['job']}</div>
                <div class="rank-bar-wrap">
                    <div class="rank-bar" style="width:{bar_w}%;background:{color};"></div>
                </div>
                <div class="rank-pct" style="color:{color};">{row['rate_pct']:.1f}%</div>
            </div>"""
        st.markdown(rows_html, unsafe_allow_html=True)

    with r_right:
        fig_job = go.Figure()
        colors  = [C["accent"] if r >= GLOBAL_RATE else "#2A3450"
                   for r in job_df["rate_pct"]]
        fig_job.add_trace(go.Bar(
            x=job_df["job"],
            y=job_df["rate_pct"],
            marker_color=colors,
            marker_line_width=0,
            text=[f"{r:.0f}%" for r in job_df["rate_pct"]],
            textposition="outside",
            textfont=dict(size=10, color="#64748B"),
            hovertemplate="<b>%{x}</b><br>%{y:.1f}%  ·  n=%{customdata:,}<extra></extra>",
            customdata=job_df["n"],
        ))
        fig_job.add_hline(y=GLOBAL_RATE, line_dash="dot", line_color=C["warning"],
                          line_width=1.5,
                          annotation_text=f"Avg {GLOBAL_RATE:.1f}%",
                          annotation_font=dict(color=C["warning"], size=10))
        fig_job.update_layout(
            **base_layout(
                height=340,
                yaxis_ticksuffix="%",
                yaxis_title="",
                xaxis_title="",
                yaxis_range=[0, job_df["rate_pct"].max() * 1.3],
                xaxis_tickangle=-25,
            )
        )
        st.plotly_chart(fig_job, width='stretch')

    gap = top_job["rate_pct"] - bot_job["rate_pct"]
    st.markdown(f"""
    <div class="callout {'success' if top_job['rate_pct'] >= GLOBAL_RATE else 'warning'}">
        <b>{top_job['job'].title()}</b> is your best-converting occupation at
        <b>{top_job['rate_pct']:.1f}%</b> — 
        {f"<b>{gap:.1f}pp</b> ahead of <b>{bot_job['job']}</b> ({bot_job['rate_pct']:.1f}%)." }
        {'Retired and student customers tend to convert well because they have less financial pressure and more openness to savings products.'
         if top_job['job'] in ('retired', 'student')
         else 'Focus outreach time on this occupation first before moving to lower-converting groups.'}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── Education × previous campaign outcome ──
    bot_left, bot_right = st.columns(2)

    with bot_left:
        st.markdown('<div class="section-label">Education level</div>',
                    unsafe_allow_html=True)
        edu_df = (
            df.groupby("education")["subscribed"]
            .agg(["mean", "count"])
            .rename(columns={"mean": "rate", "count": "n"})
            .reset_index()
            .sort_values("rate", ascending=True)
        )
        edu_df["rate_pct"] = edu_df["rate"] * 100
        fig_edu = go.Figure(go.Bar(
            y=edu_df["education"],
            x=edu_df["rate_pct"],
            orientation="h",
            marker_color=[C["accent"] if r >= GLOBAL_RATE else "#2A3450"
                          for r in edu_df["rate_pct"]],
            marker_line_width=0,
            text=[f"{r:.1f}%" for r in edu_df["rate_pct"]],
            textposition="outside",
            textfont=dict(size=11, color="#64748B"),
            hovertemplate="<b>%{y}</b>: %{x:.1f}%<extra></extra>",
        ))
        fig_edu.add_vline(x=GLOBAL_RATE, line_dash="dot", line_color=C["warning"], line_width=1)
        fig_edu.update_layout(
            **base_layout(height=220, xaxis_ticksuffix="%",
                          xaxis_range=[0, edu_df["rate_pct"].max() * 1.3])
        )
        st.plotly_chart(fig_edu, width='stretch')

    with bot_right:
        st.markdown('<div class="section-label">Previous campaign outcome</div>',
                    unsafe_allow_html=True)
        pout_df = (
            df.groupby("poutcome")["subscribed"]
            .agg(["mean", "count"])
            .rename(columns={"mean": "rate", "count": "n"})
            .reset_index()
            .sort_values("rate", ascending=False)
        )
        pout_df["rate_pct"] = pout_df["rate"] * 100

        color_map = {"success": C["success"], "failure": C["danger"],
                     "other": C["warning"], "unknown": "#2A3450"}
        fig_pout = go.Figure(go.Bar(
            x=pout_df["poutcome"],
            y=pout_df["rate_pct"],
            marker_color=[color_map.get(p, C["accent"]) for p in pout_df["poutcome"]],
            marker_line_width=0,
            text=[f"{r:.0f}%" for r in pout_df["rate_pct"]],
            textposition="outside",
            textfont=dict(size=11, color="#64748B"),
            hovertemplate="<b>%{x}</b>: %{y:.1f}%<br>n=%{customdata:,}<extra></extra>",
            customdata=pout_df["n"],
        ))
        fig_pout.update_layout(
            **base_layout(height=220, yaxis_ticksuffix="%",
                          yaxis_range=[0, pout_df["rate_pct"].max() * 1.35])
        )
        st.plotly_chart(fig_pout, width='stretch')

        prev_success = pout_df[pout_df["poutcome"] == "success"]["rate_pct"]
        prev_unknown = pout_df[pout_df["poutcome"] == "unknown"]["rate_pct"]
        if not prev_success.empty and not prev_unknown.empty:
            st.markdown(f"""
            <div class="callout success">
                Customers who subscribed in a <b>previous campaign</b> convert at
                <b>{prev_success.values[0]:.1f}%</b> — roughly
                <b>{prev_success.values[0] / prev_unknown.values[0]:.1f}×</b>
                the rate of first-time contacts. Always prioritise callbacks to previous
                subscribers before cold outreach.
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# TAB 3 — MONEY MATTERS
# ════════════════════════════════════════════════════════════════
with tab_money:
    st.markdown(f"""
    <div class="page-header">
        <div>
            <div class="page-title">Money matters</div>
            <div class="page-desc">How account balance, age, and financial health relate to conversion</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cap     = df["balance"].quantile(0.97)
    df_bal  = df[df["balance"] < cap].copy()
    med_yes = df_bal[df_bal["subscribed"] == 1]["balance"].median()
    med_no  = df_bal[df_bal["subscribed"] == 0]["balance"].median()

    top_row, bot_row = st.columns([3, 2])

    with top_row:
        st.markdown('<div class="section-label">Balance distribution — subscribers vs non-subscribers</div>',
                    unsafe_allow_html=True)
        fig_hist = go.Figure()
        for label, val, color in [("Subscribed", 1, C["accent"]), ("Not subscribed", 0, C["danger"])]:
            d = df_bal[df_bal["subscribed"] == val]["balance"]
            fig_hist.add_trace(go.Histogram(
                x=d, name=label, nbinsx=70,
                marker_color=color, opacity=0.55,
                histnorm="probability density",
                hovertemplate=f"<b>{label}</b><br>Balance: €%{{x:,.0f}}<extra></extra>",
            ))
        # Median lines
        for val, color, label in [(med_yes, C["accent"], f"Median (sub) €{med_yes:,.0f}"),
                                   (med_no,  C["danger"],  f"Median (non) €{med_no:,.0f}")]:
            fig_hist.add_vline(x=val, line_dash="dash", line_color=color, line_width=1.5,
                               annotation_text=label,
                               annotation_font=dict(color=color, size=10))
        fig_hist.update_layout(
            **base_layout(height=290, barmode="overlay",
                          xaxis_title="Account balance (€)",
                          xaxis_tickprefix="€", xaxis_tickformat=",",
                          yaxis_title="Density")
        )
        st.plotly_chart(fig_hist, width='stretch')

    with bot_row:
        st.markdown('<div class="section-label">Balance quartile → conversion lift</div>',
                    unsafe_allow_html=True)

        # Put customers into balance quartiles and show conversion rate per quartile
        df_bal2 = df_bal.copy()
        df_bal2["quartile"] = pd.qcut(
            df_bal2["balance"], 4,
            labels=["Bottom 25%", "25–50%", "50–75%", "Top 25%"]
        )
        q_rates = (
            df_bal2.groupby("quartile", observed=True)["subscribed"]
            .agg(["mean", "count"])
            .reset_index()
        )
        q_rates["rate_pct"] = q_rates["mean"] * 100

        colors_q = [
            C["danger"] if r < GLOBAL_RATE * 0.8 else
            C["warning"] if r < GLOBAL_RATE else
            C["success"]
            for r in q_rates["rate_pct"]
        ]
        fig_q = go.Figure(go.Bar(
            x=q_rates["quartile"].astype(str),
            y=q_rates["rate_pct"],
            marker_color=colors_q,
            marker_line_width=0,
            text=[f"{r:.1f}%" for r in q_rates["rate_pct"]],
            textposition="outside",
            textfont=dict(size=11, color="#64748B"),
            hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>",
        ))
        fig_q.add_hline(y=GLOBAL_RATE, line_dash="dot", line_color=C["warning"], line_width=1)
        fig_q.update_layout(
            **base_layout(height=290, yaxis_ticksuffix="%",
                          yaxis_range=[0, q_rates["rate_pct"].max() * 1.3])
        )
        st.plotly_chart(fig_q, width='stretch')

    top25 = q_rates[q_rates["quartile"] == "Top 25%"]["rate_pct"]
    bot25 = q_rates[q_rates["quartile"] == "Bottom 25%"]["rate_pct"]
    if not top25.empty and not bot25.empty:
        lift = top25.values[0] / bot25.values[0] if bot25.values[0] > 0 else 0
        st.markdown(f"""
        <div class="callout">
            Median balance for subscribers in this segment is
            <b>€{med_yes:,.0f}</b> vs <b>€{med_no:,.0f}</b> for non-subscribers.
            The top balance quartile converts at <b>{top25.values[0]:.1f}%</b> —
            <b>{lift:.1f}× higher</b> than the bottom quartile ({bot25.values[0]:.1f}%).
            Balance is one of the strongest passive signals an RM has without ever speaking to the customer.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── Scatter: age vs balance, coloured by subscription ──
    st.markdown('<div class="section-label">Age vs balance (sampled 2,000 customers)</div>',
                unsafe_allow_html=True)

    df_sample = df_bal.sample(min(2000, len(df_bal)), random_state=42)
    fig_scatter = go.Figure()
    for label, val, color in [("Not subscribed", 0, C["danger"]), ("Subscribed", 1, C["accent"])]:
        d = df_sample[df_sample["subscribed"] == val]
        fig_scatter.add_trace(go.Scatter(
            x=d["age"], y=d["balance"],
            mode="markers",
            name=label,
            marker=dict(color=color, size=5, opacity=0.45,
                        line=dict(width=0)),
            hovertemplate=(
                f"<b>{label}</b><br>"
                "Age: %{x}<br>Balance: €%{y:,.0f}<extra></extra>"
            ),
        ))
    fig_scatter.update_layout(
        **base_layout(height=320,
                      xaxis_title="Age",
                      yaxis_title="Account balance (€)",
                      yaxis_tickprefix="€", yaxis_tickformat=",")
    )
    st.plotly_chart(fig_scatter, width='stretch')


# ════════════════════════════════════════════════════════════════
# TAB 4 — LOAN DRAG
# ════════════════════════════════════════════════════════════════
with tab_loans:
    st.markdown(f"""
    <div class="page-header">
        <div>
            <div class="page-title">Loan drag</div>
            <div class="page-desc">How existing debt burdens suppress new product uptake</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Calculate the 4-way split: housing × personal loan
    loan_cross = (
        df.groupby(["housing", "loan"])["subscribed"]
        .agg(["mean", "count"])
        .reset_index()
    )
    loan_cross["rate_pct"] = loan_cross["mean"] * 100
    loan_cross["label"]    = loan_cross.apply(
        lambda r: (
            "No loans" if r["housing"] == "no" and r["loan"] == "no" else
            "Mortgage only" if r["housing"] == "yes" and r["loan"] == "no" else
            "Personal loan only" if r["housing"] == "no" and r["loan"] == "yes" else
            "Both loans"
        ), axis=1
    )
    loan_cross = loan_cross.sort_values("rate_pct", ascending=False)

    top_rate  = loan_cross.iloc[0]["rate_pct"]
    worst     = loan_cross[loan_cross["label"] == "Both loans"]
    worst_r   = worst["rate_pct"].values[0] if not worst.empty else 0
    drag      = top_rate - worst_r

    a_col, b_col = st.columns([3, 2])

    with a_col:
        st.markdown('<div class="section-label">Subscription rate by debt profile</div>',
                    unsafe_allow_html=True)

        # Waterfall-style bar
        fill_colors = {
            "No loans":           C["success"],
            "Mortgage only":      C["warning"],
            "Personal loan only": C["warning"],
            "Both loans":         C["danger"],
        }
        fig_loan = go.Figure(go.Bar(
            x=loan_cross["label"],
            y=loan_cross["rate_pct"],
            marker_color=[fill_colors.get(l, C["accent"]) for l in loan_cross["label"]],
            marker_line_width=0,
            text=[f"{r:.1f}%<br><span style='font-size:0.8em'>n={n:,}</span>"
                  for r, n in zip(loan_cross["rate_pct"], loan_cross["count"])],
            textposition="outside",
            textfont=dict(size=11, color="#64748B"),
            hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>",
        ))
        fig_loan.add_hline(y=GLOBAL_RATE, line_dash="dot", line_color=C["warning"], line_width=1.5,
                           annotation_text=f"Campaign avg {GLOBAL_RATE:.1f}%",
                           annotation_font=dict(color=C["warning"], size=10))
        fig_loan.update_layout(
            **base_layout(height=340, yaxis_ticksuffix="%",
                          yaxis_range=[0, top_rate * 1.35],
                          xaxis_tickangle=-10)
        )
        st.plotly_chart(fig_loan, width='stretch')

    with b_col:
        st.markdown('<div class="section-label">Loan status vs subscription heatmap</div>',
                    unsafe_allow_html=True)

        pivot = loan_cross.pivot_table(
            index="housing", columns="loan", values="rate_pct"
        ).rename(index={"yes": "Has mortgage", "no": "No mortgage"},
                 columns={"yes": "Has personal loan", "no": "No personal loan"})

        fig_hm = go.Figure(go.Heatmap(
            z=pivot.values,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale=[[0, C["danger"]], [0.5, C["warning"]], [1, C["success"]]],
            text=[[f"{v:.1f}%" for v in row] for row in pivot.values],
            texttemplate="%{text}",
            textfont=dict(size=16, color="white", family="Inter"),
            hoverongaps=False,
            showscale=False,
            hovertemplate="<b>%{y} / %{x}</b><br>%{z:.1f}%<extra></extra>",
        ))
        fig_hm.update_layout(
            **base_layout(height=220, margin=dict(t=16, b=16, l=16, r=16),
                          xaxis=dict(showgrid=False, tickfont=dict(size=11)),
                          yaxis=dict(showgrid=False, tickfont=dict(size=11)))
        )
        st.plotly_chart(fig_hm, width='stretch')

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px;">
            <div style="background:{C['success']}22;border:1px solid {C['success']}44;
                        border-radius:8px;padding:0.6rem 0.8rem;">
                <div style="font-size:0.68rem;color:{C['success']};font-weight:700;
                            text-transform:uppercase;letter-spacing:0.08em;">No loans</div>
                <div style="font-size:1.3rem;font-weight:700;color:{C['text']};
                            font-family:'JetBrains Mono',monospace;">
                    {loan_cross[loan_cross['label']=='No loans']['rate_pct'].values[0]:.1f}%
                </div>
            </div>
            <div style="background:{C['danger']}22;border:1px solid {C['danger']}44;
                        border-radius:8px;padding:0.6rem 0.8rem;">
                <div style="font-size:0.68rem;color:{C['danger']};font-weight:700;
                            text-transform:uppercase;letter-spacing:0.08em;">Both loans</div>
                <div style="font-size:1.3rem;font-weight:700;color:{C['text']};
                            font-family:'JetBrains Mono',monospace;">{worst_r:.1f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="callout danger">
        Existing loan burden is the clearest drag signal in this dataset.
        Customers with no active loans convert at <b>{top_rate:.1f}%</b>
        — a <b>{drag:.1f}pp gap</b> over customers carrying both a mortgage and a personal loan
        ({worst_r:.1f}%).
        When building a call list, filter out dual-loan customers first.
        The incremental effort to convert them rarely justifies the time cost.
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# TAB 5 — TOP SEGMENTS
# ════════════════════════════════════════════════════════════════
with tab_segs:
    st.markdown(f"""
    <div class="page-header">
        <div>
            <div class="page-title">Top segments</div>
            <div class="page-desc">Ranked combinations — where to focus your outreach</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Build segment combinations: job × age_group × housing
    seg_df = (
        df.groupby(["job", "age_group", "housing"], observed=True)["subscribed"]
        .agg(["mean", "count", "sum"])
        .reset_index()
        .rename(columns={"mean": "rate", "count": "n", "sum": "subscribers"})
    )
    seg_df["rate_pct"] = seg_df["rate"] * 100
    # Only show segments with at least 30 customers for statistical relevance
    seg_df = seg_df[seg_df["n"] >= 30].sort_values("rate_pct", ascending=False)

    top_segs = seg_df.head(12)
    bot_segs = seg_df.tail(8)

    t_left, t_right = st.columns(2)

    with t_left:
        st.markdown('<div class="section-label" style="color:#10B981;">🏆 Best converting segments</div>',
                    unsafe_allow_html=True)
        table_rows = ""
        for i, (_, row) in enumerate(top_segs.iterrows()):
            bar_w  = int(row["rate_pct"] / seg_df["rate_pct"].max() * 100)
            label  = f"{row['job'].title()}, {row['age_group']}, {'No mortgage' if row['housing']=='no' else 'Has mortgage'}"
            table_rows += f"""
            <tr>
                <td style="font-weight:600;color:{C['text']};width:16px;">#{i+1}</td>
                <td>{label}</td>
                <td>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <div style="width:70px;height:5px;background:{C['border']};border-radius:3px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;background:{C['success']};border-radius:3px;"></div>
                        </div>
                        <span style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;
                                     font-weight:700;color:{C['success']};">{row['rate_pct']:.1f}%</span>
                    </div>
                </td>
                <td style="color:{C['muted']};text-align:right;font-size:0.78rem;">{row['n']:,}</td>
            </tr>"""

        st.markdown(f"""
        <table class="compact-table">
            <thead><tr>
                <th>#</th><th>Segment</th><th>Conv. rate</th><th>Size</th>
            </tr></thead>
            <tbody>{table_rows}</tbody>
        </table>
        """, unsafe_allow_html=True)

    with t_right:
        st.markdown('<div class="section-label" style="color:#EF4444;">⚠ Hardest to convert</div>',
                    unsafe_allow_html=True)
        table_rows2 = ""
        for i, (_, row) in enumerate(bot_segs.iterrows()):
            label  = f"{row['job'].title()}, {row['age_group']}, {'No mortgage' if row['housing']=='no' else 'Has mortgage'}"
            table_rows2 += f"""
            <tr>
                <td>{label}</td>
                <td>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;
                                 font-weight:600;color:{C['danger']};">{row['rate_pct']:.1f}%</span>
                </td>
                <td style="color:{C['muted']};font-size:0.78rem;">{row['n']:,}</td>
            </tr>"""

        st.markdown(f"""
        <table class="compact-table">
            <thead><tr>
                <th>Segment</th><th>Conv. rate</th><th>Size</th>
            </tr></thead>
            <tbody>{table_rows2}</tbody>
        </table>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── Scatter of segments (size = n, colour = rate) ──
    st.markdown('<div class="section-label">All segments — size vs conversion (bubble = customer count)</div>',
                unsafe_allow_html=True)

    fig_bubble = go.Figure()
    for _, row in seg_df.iterrows():
        color = (C["success"] if row["rate_pct"] >= GLOBAL_RATE * 1.5 else
                 C["warning"] if row["rate_pct"] >= GLOBAL_RATE else
                 C["danger"])
        fig_bubble.add_trace(go.Scatter(
            x=[row["n"]],
            y=[row["rate_pct"]],
            mode="markers",
            marker=dict(
                size=max(6, min(30, row["n"] / 30)),
                color=color,
                opacity=0.65,
                line=dict(width=0),
            ),
            hovertemplate=(
                f"<b>{row['job'].title()}, {row['age_group']}, "
                f"{'No mortgage' if row['housing']=='no' else 'Mortgage'}</b><br>"
                f"Conversion: {row['rate_pct']:.1f}%<br>"
                f"Segment size: {row['n']:,}<extra></extra>"
            ),
            showlegend=False,
        ))
    fig_bubble.add_hline(y=GLOBAL_RATE, line_dash="dot", line_color=C["warning"],
                         line_width=1.5,
                         annotation_text=f"Campaign avg {GLOBAL_RATE:.1f}%",
                         annotation_font=dict(color=C["warning"], size=10))
    fig_bubble.update_layout(
        **base_layout(height=320,
                      xaxis_title="Segment size (customers)",
                      yaxis_title="Subscription rate (%)",
                      yaxis_ticksuffix="%")
    )
    st.plotly_chart(fig_bubble, width='stretch')


# ════════════════════════════════════════════════════════════════
# TAB 6 — FIND LEADS
# ════════════════════════════════════════════════════════════════
with tab_leads:
    st.markdown(f"""
    <div class="page-header">
        <div>
            <div class="page-title">Find leads</div>
            <div class="page-desc">Search, score, and export individual customers</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    ctrl1, ctrl2, ctrl3 = st.columns(3)
    with ctrl1:
        outcome_filter = st.selectbox(
            "Outcome", ["All customers", "Subscribed only", "Didn't subscribe"],
            key="lead_outcome"
        )
    with ctrl2:
        housing_f = st.selectbox("Mortgage", ["Any", "No mortgage", "Has mortgage"], key="lead_h")
    with ctrl3:
        sort_col = st.selectbox(
            "Sort by", ["Lead score", "Balance (high→low)", "Age", "Subscription rate potential"],
            key="lead_sort"
        )

    df_leads = df.copy()
    if outcome_filter == "Subscribed only":
        df_leads = df_leads[df_leads["y"] == "yes"]
    elif outcome_filter == "Didn't subscribe":
        df_leads = df_leads[df_leads["y"] == "no"]
    if housing_f == "No mortgage":
        df_leads = df_leads[df_leads["housing"] == "no"]
    elif housing_f == "Has mortgage":
        df_leads = df_leads[df_leads["housing"] == "yes"]

    if sort_col == "Lead score":
        df_leads = df_leads.sort_values("lead_score", ascending=False)
    elif sort_col == "Balance (high→low)":
        df_leads = df_leads.sort_values("balance", ascending=False)
    elif sort_col == "Age":
        df_leads = df_leads.sort_values("age")

    # Summary bar
    st.markdown(f"""
    <div style="display:flex;gap:16px;margin-bottom:1rem;align-items:center;">
        <span style="font-size:0.85rem;color:{C['muted']};">
            <b style="color:{C['text']};font-family:'JetBrains Mono',monospace;">{len(df_leads):,}</b>
            customers matched
        </span>
        <span class="pill pill-blue">
            {df_leads['subscribed'].mean()*100:.1f}% conversion rate
        </span>
        <span class="pill pill-green">
            Avg lead score: {df_leads['lead_score'].mean():.0f}/100
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Display table with colour-coded lead score
    display = df_leads[["age", "job", "marital", "education",
                         "balance", "housing", "loan", "age_group",
                         "lead_score", "y"]].head(400).copy()
    display.columns = ["Age", "Job", "Marital", "Education",
                       "Balance (€)", "Mortgage", "Personal Loan", "Age Group",
                       "Lead Score", "Subscribed"]

    st.dataframe(
        display,
        width='stretch',
        height=380,
        column_config={
            "Balance (€)":  st.column_config.NumberColumn(format="€%d"),
            "Lead Score":   st.column_config.ProgressColumn(
                                min_value=0, max_value=100, format="%d"),
            "Subscribed":   st.column_config.TextColumn(),
        }
    )

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── Lead score distribution ──
    st.markdown('<div class="section-label">Lead score distribution in this segment</div>',
                unsafe_allow_html=True)
    fig_ls = go.Figure()
    for label, val, color in [("Didn't subscribe", 0, C["danger"]),
                               ("Subscribed", 1, C["accent"])]:
        d = df_leads[df_leads["subscribed"] == val]["lead_score"]
        fig_ls.add_trace(go.Histogram(
            x=d, name=label, nbinsx=20,
            marker_color=color, opacity=0.6,
            hovertemplate=f"<b>{label}</b><br>Score: %{{x}}<extra></extra>",
        ))
    fig_ls.update_layout(
        **base_layout(height=240, barmode="overlay",
                      xaxis_title="Lead score (0–100)",
                      yaxis_title="Customers")
    )
    st.plotly_chart(fig_ls, width='stretch')

    st.markdown(f"""
    <div class="callout">
        <b>Lead score methodology:</b> Each customer is scored out of 100 based on four
        passive signals — <b>high balance (+30)</b>, <b>no mortgage (+25)</b>,
        <b>no personal loan (+20)</b>, and <b>job type</b> (retired or student +25).
        No call history required. High-score customers are worth calling first.
    </div>
    """, unsafe_allow_html=True)
