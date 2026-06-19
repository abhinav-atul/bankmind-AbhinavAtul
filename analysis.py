"""
analysis.py — BankMind Challenge, Track A
EDA + answers to the 4 business questions using the UCI Bank Marketing dataset.
Saves chart PNGs to assets/ folder for use in the Streamlit dashboard.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────
DATA_PATH = "data/bank-full.csv"
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# Premium colour palette
PALETTE_YES = "#4F8EF7"
PALETTE_NO  = "#F76F6F"
BG_COLOR    = "#0F1117"
TEXT_COLOR  = "#E8ECF0"

MATPLOTLIB_THEME = {
    "figure.facecolor": BG_COLOR,
    "axes.facecolor":   "#1A1D27",
    "axes.edgecolor":   "#2E3040",
    "axes.labelcolor":  TEXT_COLOR,
    "axes.titlecolor":  TEXT_COLOR,
    "xtick.color":      TEXT_COLOR,
    "ytick.color":      TEXT_COLOR,
    "text.color":       TEXT_COLOR,
    "grid.color":       "#2E3040",
    "grid.linestyle":   "--",
    "grid.alpha":       0.5,
    "legend.facecolor": "#1A1D27",
    "legend.edgecolor": "#2E3040",
}
plt.rcParams.update(MATPLOTLIB_THEME)
sns.set_theme(style="dark", rc=MATPLOTLIB_THEME)


# ─────────────────────────────────────────────
# 1. Load & Inspect
# ─────────────────────────────────────────────
def load_data(path: str) -> pd.DataFrame:
    """Load the bank-full.csv (semicolon-delimited)."""
    df = pd.read_csv(path, sep=";")
    # Normalise the target to 0/1
    df["subscribed"] = (df["y"] == "yes").astype(int)
    return df


def print_summary(df: pd.DataFrame) -> None:
    print("=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)
    print(f"Shape          : {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"\nData types:\n{df.dtypes.value_counts().to_string()}")
    print(f"\nMissing values :\n{df.isnull().sum()[df.isnull().sum() > 0].to_string() or '  None'}")
    vc = df["y"].value_counts()
    total = len(df)
    print(f"\nClass distribution (y):")
    for label, count in vc.items():
        print(f"  {label:>3} → {count:>6,}  ({count/total*100:.1f}%)")
    print("=" * 60)


# ─────────────────────────────────────────────
# 2. Business Question 1
#    Which job types have the highest subscription rate?
# ─────────────────────────────────────────────
def q1_job_subscription_rate(df: pd.DataFrame) -> None:
    job_rate = (
        df.groupby("job")["subscribed"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "rate", "count": "n"})
        .sort_values("rate", ascending=True)
    )
    job_rate["rate_pct"] = job_rate["rate"] * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(
        job_rate.index,
        job_rate["rate_pct"],
        color=[PALETTE_YES if r > job_rate["rate_pct"].median() else "#5C6073"
               for r in job_rate["rate_pct"]],
        edgecolor="none",
        height=0.65,
    )
    ax.set_xlabel("Subscription Rate (%)", fontsize=12, labelpad=10)
    ax.set_title("Subscription Rate by Job Type", fontsize=15, fontweight="bold", pad=15)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax.axvline(job_rate["rate_pct"].mean(), color="#FFD166", linewidth=1.5,
               linestyle="--", label=f"Average: {job_rate['rate_pct'].mean():.1f}%")
    ax.legend(fontsize=10)
    ax.set_xlim(0, job_rate["rate_pct"].max() * 1.2)

    # Annotate with n
    for bar, (_, row) in zip(bars, job_rate.iterrows()):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{row['rate_pct']:.1f}%  (n={row['n']:,})",
                va="center", ha="left", fontsize=9, color=TEXT_COLOR)

    plt.tight_layout()
    path = os.path.join(ASSETS_DIR, "q1_job_subscription.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[Q1] Saved → {path}")


# ─────────────────────────────────────────────
# 3. Business Question 2
#    Balance vs subscription likelihood
# ─────────────────────────────────────────────
def q2_balance_vs_subscription(df: pd.DataFrame) -> None:
    # Cap extreme outliers for a cleaner view
    cap = df["balance"].quantile(0.98)
    df_plot = df[df["balance"] < cap].copy()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Box plot
    sub_labels = {0: "No", 1: "Yes"}
    for sub_val, color in [(0, PALETTE_NO), (1, PALETTE_YES)]:
        data = df_plot[df_plot["subscribed"] == sub_val]["balance"]
        ax1.boxplot(data, positions=[sub_val], widths=0.4,
                    patch_artist=True,
                    boxprops=dict(facecolor=color, alpha=0.7, linewidth=0),
                    medianprops=dict(color="white", linewidth=2),
                    whiskerprops=dict(color=TEXT_COLOR),
                    capprops=dict(color=TEXT_COLOR),
                    flierprops=dict(marker=".", color=color, alpha=0.2, markersize=3))

    ax1.set_xticks([0, 1])
    ax1.set_xticklabels(["No", "Yes"])
    ax1.set_xlabel("Subscribed", fontsize=12)
    ax1.set_ylabel("Account Balance (€)", fontsize=12)
    ax1.set_title("Balance Distribution by Subscription", fontsize=13, fontweight="bold")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x:,.0f}"))

    # KDE
    for sub_val, label, color in [(0, "No", PALETTE_NO), (1, "Yes", PALETTE_YES)]:
        data = df_plot[df_plot["subscribed"] == sub_val]["balance"]
        ax2.hist(data, bins=60, alpha=0.45, color=color, label=label,
                 density=True, edgecolor="none")

    ax2.set_xlabel("Account Balance (€)", fontsize=12)
    ax2.set_ylabel("Density", fontsize=12)
    ax2.set_title("Balance Distribution (Density)", fontsize=13, fontweight="bold")
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{x:,.0f}"))
    ax2.legend(title="Subscribed", fontsize=10)

    plt.suptitle("Account Balance vs Subscription Likelihood",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = os.path.join(ASSETS_DIR, "q2_balance_subscription.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[Q2] Saved → {path}")


# ─────────────────────────────────────────────
# 4. Business Question 3
#    Subscription rate across age groups
# ─────────────────────────────────────────────
def q3_age_group_subscription(df: pd.DataFrame) -> None:
    bins   = [18, 30, 45, 60, 120]
    labels = ["18–30", "31–45", "46–60", "60+"]
    df = df.copy()
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=True)

    age_stats = (
        df.groupby("age_group", observed=True)["subscribed"]
        .agg(["mean", "count", "sum"])
        .rename(columns={"mean": "rate", "count": "total", "sum": "subscribed_n"})
    )
    age_stats["rate_pct"] = age_stats["rate"] * 100

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = [PALETTE_YES if r > age_stats["rate_pct"].mean() else "#5C6073"
              for r in age_stats["rate_pct"]]
    bars = ax.bar(age_stats.index, age_stats["rate_pct"],
                  color=colors, edgecolor="none", width=0.55)

    ax.axhline(age_stats["rate_pct"].mean(), color="#FFD166", linewidth=1.5,
               linestyle="--", label=f"Average: {age_stats['rate_pct'].mean():.1f}%")
    ax.set_xlabel("Age Group", fontsize=12, labelpad=10)
    ax.set_ylabel("Subscription Rate (%)", fontsize=12)
    ax.set_title("Subscription Rate Across Age Groups", fontsize=15, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax.legend(fontsize=10)

    for bar, (_, row) in zip(bars, age_stats.iterrows()):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                f"{row['rate_pct']:.1f}%\n(n={row['total']:,})",
                ha="center", va="bottom", fontsize=9.5, color=TEXT_COLOR)

    ax.set_ylim(0, age_stats["rate_pct"].max() * 1.25)
    plt.tight_layout()
    path = os.path.join(ASSETS_DIR, "q3_age_subscription.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[Q3] Saved → {path}")


# ─────────────────────────────────────────────
# 5. Business Question 4
#    Housing loan vs subscription rate
# ─────────────────────────────────────────────
def q4_housing_loan_effect(df: pd.DataFrame) -> None:
    housing_rate = (
        df.groupby("housing")["subscribed"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "rate", "count": "n"})
    )
    housing_rate["rate_pct"] = housing_rate["rate"] * 100

    # Also cross-tabulate with personal loan
    cross = (
        df.groupby(["housing", "loan"])["subscribed"]
        .mean()
        .unstack("loan")
        .rename(columns={"no": "No Personal Loan", "yes": "Has Personal Loan"})
        * 100
    )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Simple housing vs rate
    bar_colors = [PALETTE_NO if h == "yes" else PALETTE_YES
                  for h in housing_rate.index]
    bars = ax1.bar(["No Housing Loan", "Has Housing Loan"],
                   housing_rate["rate_pct"],
                   color=bar_colors, width=0.45, edgecolor="none")
    ax1.set_ylabel("Subscription Rate (%)", fontsize=12)
    ax1.set_title("Housing Loan vs Subscription Rate", fontsize=13, fontweight="bold")
    ax1.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=1))
    for bar, (_, row) in zip(bars, housing_rate.iterrows()):
        ax1.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.2,
                 f"{row['rate_pct']:.1f}%\n(n={row['n']:,})",
                 ha="center", va="bottom", fontsize=10, color=TEXT_COLOR)
    ax1.set_ylim(0, housing_rate["rate_pct"].max() * 1.3)

    # Cross with personal loan
    x = np.arange(len(cross.index))
    w = 0.35
    ax2.bar(x - w / 2, cross["No Personal Loan"],  width=w, label="No Personal Loan",
            color=PALETTE_YES, edgecolor="none")
    ax2.bar(x + w / 2, cross["Has Personal Loan"], width=w, label="Has Personal Loan",
            color=PALETTE_NO, edgecolor="none")
    ax2.set_xticks(x)
    ax2.set_xticklabels(["No Housing Loan", "Has Housing Loan"], fontsize=10)
    ax2.set_ylabel("Subscription Rate (%)", fontsize=12)
    ax2.set_title("Effect of Both Loans on Subscription", fontsize=13, fontweight="bold")
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=1))
    ax2.legend(fontsize=10)

    plt.suptitle("Existing Loan Burden vs New Product Uptake",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = os.path.join(ASSETS_DIR, "q4_housing_loan.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[Q4] Saved → {path}")


# ─────────────────────────────────────────────
# 6. Bonus: Overall Class Distribution (used by dashboard)
# ─────────────────────────────────────────────
def overall_class_chart(df: pd.DataFrame) -> None:
    vc = df["y"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 4))
    colors_pie = [PALETTE_NO, PALETTE_YES]
    wedges, texts, autotexts = ax.pie(
        vc.values, labels=["No", "Yes"],
        autopct="%1.1f%%", colors=colors_pie,
        startangle=90, wedgeprops=dict(edgecolor="#0F1117", linewidth=2),
        textprops=dict(color=TEXT_COLOR, fontsize=11),
    )
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_fontweight("bold")
    ax.set_title("Overall Subscription Distribution", fontsize=13, fontweight="bold", pad=10)
    plt.tight_layout()
    path = os.path.join(ASSETS_DIR, "class_dist.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[Overview] Saved → {path}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\nLoading data...")
    df = load_data(DATA_PATH)
    print_summary(df)

    print("\nGenerating charts...")
    q1_job_subscription_rate(df)
    q2_balance_vs_subscription(df)
    q3_age_group_subscription(df)
    q4_housing_loan_effect(df)
    overall_class_chart(df)

    print("\n✅ All charts saved to assets/")
    print("   Run:  streamlit run app.py")
