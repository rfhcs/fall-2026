"""
"After" chart: U.S. daily new COVID-19 cases, 7-day average.

Reads ../data/chart-1.csv (cumulative cases/deaths, NYT format) and writes
chart_1_after.png. Colors follow the NYT coronavirus-tracker style:
pale red daily bars behind a dark red 7-day-average line.

Run:  .venv/bin/python chart_1/chart_1.py
"""

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns

# ---------------------------------------------------------------- settings
DATA_PATH = Path(__file__).parent.parent / "data" / "chart-1.csv"
OUT_PATH = Path(__file__).parent / "chart_1_after.png"

METRIC = "cases"  # "cases" or "deaths"
SHOW_DAILY_BARS = False  # pale daily bars behind the average line
START, END = None, "2022-01-06"  # END = article publish date (Jan 6, 2022)

# NYT-tracker palette
LINE_RED = "#C42B2B"  # 7-day average line
BAR_RED = "#F3C4BE"  # daily values
INK = "#121212"  # titles
INK_SECONDARY = "#555555"  # subtitle, annotations
INK_MUTED = "#8A8A8A"  # axis labels, source
GRID = "#E6E6E6"
BACKGROUND = "#FFFFFF"

TITLE = "COVID-19 cases are likely to increase with the new Omicron variant"
SUBTITLE = "Daily new reported COVID-19 cases, 7-day average"
SOURCE = "Source: The New York Times, based on reports from state and local health agencies (https://github.com/nytimes/covid-19-data)"

# Peaks to call out: (search window start, end, label, label side)
ANNOTATIONS = [
    ("2020-11-01", "2021-03-01", "Winter surge", "above"),
    ("2021-07-01", "2021-11-01", "Delta", "above"),
    ("2021-12-01", "2022-03-01", "Omicron, as of Jan. 6", "left"),
]

# Dated events marked with a dashed vertical rule: (date, label).
# Delta designated a Variant of Concern by CDC, June 15, 2021
# https://www.cdc.gov/coronavirus/2019-ncov/variants/variant-classifications.html
# First U.S. Omicron case: CDC media statement, Dec. 1, 2021
# https://archive.cdc.gov/www_cdc_gov/media/releases/2021/s1201-omicron-variant.html
EVENTS = [
    ("2021-12-01", "First U.S. Omicron case\nconfirmed, Dec. 1"),
]

# ---------------------------------------------------------------- data
df = pd.read_csv(DATA_PATH, parse_dates=["date"]).set_index("date")
daily = df[METRIC].diff().clip(lower=0)  # cumulative -> daily; drop data corrections
avg = daily.rolling(7).mean()

if START or END:
    daily, avg = daily[START:END], avg[START:END]

# ---------------------------------------------------------------- style
sns.set_theme(
    style="white",
    rc={
        "font.family": ["Helvetica Neue", "Helvetica", "Arial", "sans-serif"],
        "axes.facecolor": BACKGROUND,
        "figure.facecolor": BACKGROUND,
    },
)

fig, ax = plt.subplots(figsize=(12, 6.5), dpi=200)
fig.subplots_adjust(left=0.07, right=0.97, top=0.80, bottom=0.12)

if SHOW_DAILY_BARS:
    ax.bar(daily.index, daily.values, width=1.0, color=BAR_RED, linewidth=0, zorder=1)
ax.plot(
    avg.index,
    avg.values,
    color=LINE_RED,
    linewidth=2.2,
    solid_capstyle="round",
    zorder=3,
)

# ---------------------------------------------------------------- axes
# Clip the y-axis to the average's range so the few extreme daily reporting
# spikes don't flatten the line; those bars simply run off the top.
ymax = avg.max() * 1.08
ax.set_ylim(0, ymax)
ax.set_xlim(avg.index.min(), avg.index.max())


def fmt_count(x, _):
    if x >= 1_000_000:
        return f"{x / 1_000_000:g} million"
    if x >= 1_000:
        return f"{x / 1_000:,.0f},000"
    return f"{x:,.0f}"


ax.yaxis.set_major_locator(mticker.MaxNLocator(5))
ax.set_yticklabels([])
ax.tick_params(axis="y", length=0)
ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
# NYT-style y labels: left-aligned, sitting just above each gridline
for y in ax.get_yticks():
    if 0 < y < ymax:
        ax.text(
            0,
            y,
            fmt_count(y, None),
            transform=ax.get_yaxis_transform(),
            ha="left",
            va="bottom",
            fontsize=10,
            color=INK_MUTED,
            bbox=dict(facecolor=BACKGROUND, edgecolor="none", pad=1.5),
            zorder=5,
        )

ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(
    mticker.FuncFormatter(
        lambda x, _: (
            lambda d: (
                f"{d:%b}\n{d:%Y}"
                if d.month == 1 or x == ax.get_xticks()[0]
                else f"{d:%b}"
            )
        )(mdates.num2date(x))
    )
)
ax.tick_params(axis="x", length=4, color=INK_MUTED, labelsize=10, labelcolor=INK_MUTED)

sns.despine(ax=ax, left=True, right=True, top=True)
ax.spines["bottom"].set_color("#BBBBBB")

# ---------------------------------------------------------------- annotations
for start, end, label, side in ANNOTATIONS:
    window = avg[start:end].dropna()
    if window.empty:
        continue
    peak_date, peak_val = window.idxmax(), window.max()
    ax.plot(
        peak_date,
        peak_val,
        "o",
        markersize=6,
        color=LINE_RED,
        markeredgecolor=BACKGROUND,
        markeredgewidth=1.5,
        zorder=4,
        clip_on=False,
    )
    ax.annotate(
        f"{label}\n{peak_val:,.0f} a day",
        xy=(peak_date, peak_val),
        xytext={"above": (0, 14), "right": (22, -6), "left": (-14, -6)}[side],
        textcoords="offset points",
        ha={"above": "center", "right": "left", "left": "right"}[side],
        va="bottom" if side == "above" else "center",
        fontsize=10,
        color=INK_SECONDARY,
        linespacing=1.3,
        zorder=6,
        bbox=dict(facecolor=BACKGROUND, edgecolor="none", pad=2, alpha=0.9),
    )

for date, label in EVENTS:
    x = pd.Timestamp(date)
    ax.axvline(
        x, ymax=0.72, color=INK_SECONDARY, linewidth=1, linestyle=(0, (3, 3)), zorder=2
    )
    ax.annotate(
        label,
        xy=(x, ymax * 0.72),
        xytext=(-6, 0),
        textcoords="offset points",
        ha="right",
        va="top",
        fontsize=10,
        color=INK_SECONDARY,
        linespacing=1.3,
        zorder=6,
        bbox=dict(facecolor=BACKGROUND, edgecolor="none", pad=2, alpha=0.9),
    )

# ---------------------------------------------------------------- text
fig.text(
    0.07,
    0.93,
    TITLE,
    fontsize=19,
    fontweight="bold",
    color=INK,
    family=["Georgia", "serif"],
)
fig.text(0.07, 0.875, SUBTITLE, fontsize=12, color=INK_SECONDARY)
fig.text(0.07, 0.005, SOURCE, fontsize=8.5, color=INK_MUTED)

fig.savefig(OUT_PATH, bbox_inches="tight", pad_inches=0.25)
print(f"Saved {OUT_PATH}")
