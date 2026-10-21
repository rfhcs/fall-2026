"""
"After" chart: average feeling-thermometer rating of G20 countries, by party.

Replaces the side-by-side thermometer slope chart (chart_2_before.png) with a
grouped horizontal bar chart on a plain 0-100 scale, with 50 marked as neutral.

Reads ../data/chart-2.csv (built by build_chart_2_data.py) and writes
chart_2_after.png.

Run:  .venv/bin/python chart_2/chart_2.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ---------------------------------------------------------------- settings
DATA_PATH = Path(__file__).parent.parent / "data" / "chart-2.csv"
OUT_PATH = Path(__file__).parent / "chart_2_after.png"

# "overall" (avg of both parties), "dem", "rep", or "gap" (Dem minus Rep)
SORT_BY = "overall"
SHOW_GAP_COLUMN = True

# Party colors (muted red/blue)
REP_COLOR = "#E3A39B"
DEM_COLOR = "#AFC6DC"
# darker shades for the gap labels so the text stays readable on white
REP_TEXT = "#B5564F"
DEM_TEXT = "#41709E"
INK = "#121212"
INK_SECONDARY = "#555555"
INK_MUTED = "#8A8A8A"
GRID = "#E6E6E6"
NEUTRAL_LINE = "#9A9A9A"
BACKGROUND = "#FFFFFF"

TITLE = "Democrats give most G20 countries higher\naverage ratings than Republicans"
SUBTITLE = "Average rating of each country on a 0–100 scale, by party"
SOURCE = ("Source: Pew Research Center survey of U.S. adults conducted Sept. 14–20, 2026.\n"
          "Party includes those who lean toward each party.")

BAR_HEIGHT = 0.36   # each party's bar; the pair fills 2 * BAR_HEIGHT of a row
BAR_GAP = 0.04      # white gap between a country's two bars

# ---------------------------------------------------------------- data
df = pd.read_csv(DATA_PATH)
df["overall"] = df[["rep_avg", "dem_avg"]].mean(axis=1)
df["gap"] = df["dem_avg"] - df["rep_avg"]
sort_col = {"overall": "overall", "dem": "dem_avg", "rep": "rep_avg", "gap": "gap"}[SORT_BY]
df = df.sort_values(sort_col, ascending=True).reset_index(drop=True)  # top of chart = highest

y = np.arange(len(df))
offset = BAR_HEIGHT / 2 + BAR_GAP / 2

# ---------------------------------------------------------------- style
sns.set_theme(style="white", rc={
    "font.family": ["Helvetica Neue", "Helvetica", "Arial", "sans-serif"],
    "axes.facecolor": BACKGROUND,
    "figure.facecolor": BACKGROUND,
})

fig, ax = plt.subplots(figsize=(9, 11), dpi=200)
fig.subplots_adjust(left=0.17, right=0.86 if SHOW_GAP_COLUMN else 0.95, top=0.80, bottom=0.10)

# Dem bar on top within each pair, Rep below — matches the legend order
ax.barh(y + offset, df["dem_avg"], height=BAR_HEIGHT, color=DEM_COLOR, zorder=3)
ax.barh(y - offset, df["rep_avg"], height=BAR_HEIGHT, color=REP_COLOR, zorder=3)

# white box keeps values readable where they cross the neutral line
label_box = dict(facecolor=BACKGROUND, edgecolor="none", pad=0.6)
for yi, (rep, dem) in enumerate(zip(df["rep_avg"], df["dem_avg"])):
    ax.text(dem + 0.8, yi + offset, f"{dem:.0f}", va="center", ha="left", fontsize=9,
            color=INK, bbox=label_box, zorder=4)
    ax.text(rep + 0.8, yi - offset, f"{rep:.0f}", va="center", ha="left", fontsize=9,
            color=INK, bbox=label_box, zorder=4)

# ---------------------------------------------------------------- axes
ax.set_xlim(0, 100)
ax.set_ylim(-0.6, len(df) - 0.4)
ax.set_yticks(y, df["country"])
ax.tick_params(axis="y", length=0, labelsize=11, labelcolor=INK, pad=8)
ax.set_xticks([0, 25, 50, 75, 100])
ax.tick_params(axis="x", length=0, labelsize=9.5, labelcolor=INK_MUTED, pad=6)
ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
sns.despine(ax=ax, left=True, bottom=True)

# Neutral midpoint
ax.axvline(50, color=NEUTRAL_LINE, linewidth=1, linestyle=(0, (3, 3)), zorder=2)
ax.text(50, len(df) - 0.35, "Neutral", ha="center", va="bottom", fontsize=9.5,
        color=INK_SECONDARY, fontweight="bold")

# ---------------------------------------------------------------- gap column
if SHOW_GAP_COLUMN:
    gap_x = 1.09  # in axes-fraction units, right of the plot
    ax.text(gap_x, len(df) - 0.35, "Dem–Rep\ngap", transform=ax.get_yaxis_transform(),
            ha="center", va="bottom", fontsize=9, color=INK_SECONDARY, fontweight="bold")
    for yi, gap in enumerate(df["gap"]):
        label = f"+{gap:.0f}" if gap > 0 else f"−{abs(gap):.0f}"
        # color by the party that rates the country higher
        color = DEM_TEXT if round(gap) > 0 else REP_TEXT if round(gap) < 0 else INK
        ax.text(gap_x, yi, label, transform=ax.get_yaxis_transform(),
                ha="center", va="center", fontsize=10, color=color, fontweight="bold")

# ---------------------------------------------------------------- legend
legend_y = 0.835
for i, (label, color) in enumerate([("Dem/Lean Dem", DEM_COLOR), ("Rep/Lean Rep", REP_COLOR)]):
    x0 = 0.17 + i * 0.2
    fig.patches.append(plt.Rectangle((x0, legend_y - 0.004), 0.018, 0.009, color=color,
                                     transform=fig.transFigure, figure=fig))
    fig.text(x0 + 0.026, legend_y, label, va="center", fontsize=10.5, color=INK)

# ---------------------------------------------------------------- text
fig.text(0.04, 0.955, TITLE, fontsize=17, fontweight="bold", color=INK, va="top",
         linespacing=1.15)
fig.text(0.04, 0.89, SUBTITLE, fontsize=10.5, color=INK_SECONDARY, va="top",
         style="italic", linespacing=1.35)
fig.text(0.04, 0.03, SOURCE, fontsize=8.5, color=INK_MUTED, va="bottom", linespacing=1.4)

fig.savefig(OUT_PATH, bbox_inches="tight", pad_inches=0.25)
print(f"Saved {OUT_PATH}")
