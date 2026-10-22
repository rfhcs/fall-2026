"""
"After" chart: weekly U.S. stocks of crude oil and petroleum products, 2026 vs. 2019-2025.

Replaces the overlapping one-line-per-year chart (chart_3_before.png) with a single
min-max band for 2019-2025, a dashed 2019-2025 average, and 2026 as the one
highlighted line, so no lines cross and no label points into a tangle.

The original showed global crude inventories (Kpler), which we don't have. This
version uses EIA's weekly U.S. series instead and is labeled as such.

Reads ../data/chart-3.csv (EIA series WTTSTUS1) and writes chart_3_after.png.

Run:  .venv/bin/python chart_3/chart_3.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ---------------------------------------------------------------- settings
DATA_PATH = Path(__file__).parent.parent / "data" / "chart-3.csv"
OUT_PATH = Path(__file__).parent / "chart_3_after.png"

RANGE_YEARS = (2019, 2025)  # inclusive; the comparison band
HIGHLIGHT_YEAR = 2026
# True: y-axis starts at 0. False: zoom to the data and say so in the note.
START_AT_ZERO = False

# Vertical event marker; position read off chart_3_before.png. Set to None to hide.
EVENT_DATE = "2026-02-28"
EVENT_LABEL = "Start\nof war"

HIGHLIGHT_COLOR = "#5C4A1E"  # dark brown, as in the original
EVENT_COLOR = "#B5564F"
BAND_COLOR = "#E4E4E4"
AVERAGE_COLOR = "#9A9A9A"
INK = "#121212"
INK_SECONDARY = "#555555"
INK_MUTED = "#8A8A8A"
GRID = "#E6E6E6"
BACKGROUND = "#FFFFFF"

TITLE = "U.S. oil stocks have fallen below their recent range"
SUBTITLE = ("Weekly U.S. stocks of crude oil and petroleum products, "
            f"{HIGHLIGHT_YEAR} vs. {RANGE_YEARS[0]}–{RANGE_YEARS[1]}")
SOURCE = ("Note: Includes commercial stocks and the Strategic Petroleum Reserve.\n"
          "Source: U.S. Energy Information Administration (series WTTSTUS1).")
if not START_AT_ZERO:
    SOURCE = SOURCE.replace("Note: ", "Note: Vertical axis does not start at zero. ", 1)

# ---------------------------------------------------------------- data
# File has two title rows above the header and a trailing blank row
df = pd.read_csv(DATA_PATH, skiprows=2, encoding="utf-8-sig").dropna()
df.columns = ["date", "stocks"]
df["date"] = pd.to_datetime(df["date"], format="%b %d, %Y")
df["stocks"] = df["stocks"].astype(float) / 1e6  # thousand barrels -> billion barrels
df["year"] = df["date"].dt.year
df["doy"] = df["date"].dt.dayofyear
# Align years by week of year; fold the occasional 53rd week into week 52
df["week"] = ((df["doy"] - 1) // 7).clip(upper=51)

history = df[df["year"].between(*RANGE_YEARS)]
band = history.groupby("week")["stocks"].agg(["min", "max", "mean"])
band_x = band.index * 7 + 4  # mid-week, in day-of-year units

current = df[df["year"] == HIGHLIGHT_YEAR]
latest = current.iloc[-1]

# ---------------------------------------------------------------- style
sns.set_theme(style="white", rc={
    "font.family": ["Helvetica Neue", "Helvetica", "Arial", "sans-serif"],
    "axes.facecolor": BACKGROUND,
    "figure.facecolor": BACKGROUND,
})

fig, ax = plt.subplots(figsize=(10, 7), dpi=200)
fig.subplots_adjust(left=0.04, right=0.88, top=0.80, bottom=0.14)

ax.fill_between(band_x, band["min"], band["max"], color=BAND_COLOR, linewidth=0, zorder=1)
ax.plot(band_x, band["mean"], color=AVERAGE_COLOR, linewidth=1.2,
        linestyle=(0, (3, 3)), zorder=2)
ax.plot(current["doy"], current["stocks"], color=HIGHLIGHT_COLOR, linewidth=2.6,
        solid_capstyle="round", zorder=4)
ax.scatter([latest["doy"]], [latest["stocks"]], s=36, color=HIGHLIGHT_COLOR,
           edgecolor=BACKGROUND, linewidth=1.5, zorder=5)

# ---------------------------------------------------------------- axes
y_min = min(band["min"].min(), current["stocks"].min())
y_max = band["max"].max()
data_pad = (y_max - y_min) * 0.08
y_bottom = 0 if START_AT_ZERO else y_min - data_pad
y_top = y_max + data_pad
ax.set_ylim(y_bottom, y_top)
pad = (y_top - y_bottom) * 0.065  # label offsets scale with axis height
ax.set_xlim(1, 366)

month_starts = pd.date_range("2026-01-01", periods=12, freq="MS")
ax.set_xticks(month_starts.dayofyear, month_starts.strftime("%b."))
ax.tick_params(axis="x", length=0, labelsize=9.5, labelcolor=INK_MUTED, pad=6)

# Y labels sit on the right, at the end of each gridline
ax.yaxis.tick_right()
y_step = 0.5 if START_AT_ZERO else 0.1
y_ticks = np.arange(0 if START_AT_ZERO else 1.5, y_top, y_step)
ax.set_yticks(y_ticks, ["0" if t == 0 else f"{t:.1f} bil." for t in y_ticks])
ax.tick_params(axis="y", length=0, labelsize=9.5, labelcolor=INK_MUTED, pad=6)
ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
sns.despine(ax=ax, left=True, right=True, bottom=True)

# ---------------------------------------------------------------- annotations
# Band and average are labeled directly, in an open stretch of each
range_week = 30
ax.text(range_week * 7 + 4, band.loc[range_week, "max"] + pad * 0.35,
        f"{RANGE_YEARS[0]}–{RANGE_YEARS[1]} range", ha="center", va="bottom",
        fontsize=9, color=INK_SECONDARY)
avg_week = 44
ax.text(avg_week * 7 + 4, band.loc[avg_week, "mean"] + pad * 0.5,
        f"{RANGE_YEARS[0]}–{RANGE_YEARS[1]} average", ha="center", va="bottom",
        fontsize=9, color=INK_SECONDARY)

# Year label below the line's early peak, clear of the average line above it
peak = current.loc[current["stocks"].idxmax()]
ax.text(peak["doy"], peak["stocks"] - pad * 0.5, str(HIGHLIGHT_YEAR), ha="center",
        va="top", fontsize=13, fontweight="bold", color=HIGHLIGHT_COLOR)

ax.text(latest["doy"] + 5, latest["stocks"],
        f"{latest['stocks']:.2f} bil.\nbarrels", ha="left", va="center",
        fontsize=10.5, color=HIGHLIGHT_COLOR, linespacing=1.2)

if EVENT_DATE:
    event_x = pd.Timestamp(EVENT_DATE).dayofyear
    ax.axvline(event_x, color=EVENT_COLOR, linewidth=0.9, linestyle=(0, (1, 2)), zorder=3)
    ax.text(event_x + 3, y_top - pad * 0.1, EVENT_LABEL, ha="left", va="top",
            fontsize=9.5, color=EVENT_COLOR, linespacing=1.15)

# ---------------------------------------------------------------- text
fig.text(0.04, 0.955, TITLE, fontsize=17, fontweight="bold", color=INK, va="top")
fig.text(0.04, 0.895, SUBTITLE, fontsize=10.5, color=INK_SECONDARY, va="top",
         style="italic")
fig.text(0.04, 0.03, SOURCE, fontsize=8.5, color=INK_MUTED, va="bottom", linespacing=1.4)

fig.savefig(OUT_PATH, bbox_inches="tight", pad_inches=0.25)
print(f"Saved {OUT_PATH}")
