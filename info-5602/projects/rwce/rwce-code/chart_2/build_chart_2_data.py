"""
Convert the Pew topline PDF (data/chart_2_data.pdf) into data/chart-2.csv.

One row per country with:
  rep_avg, dem_avg   average feeling-thermometer rating (0-100) among
                     Rep/Lean Rep and Dem/Lean Dem. The topline PDF does NOT
                     break results out by party, so these are transcribed from
                     the published chart (chart_2/chart_2_before.png).
  very_cold ... no_answer, n
                     Sept 14-20, 2026 response distribution (% of all U.S.
                     adults asked about that country), parsed from the PDF.
                     "*" (less than 0.5%) is stored as 0.

Run:  .venv/bin/python chart_2/build_chart_2_data.py
"""
import re
from pathlib import Path

import pandas as pd
from pypdf import PdfReader

ROOT = Path(__file__).parent.parent
PDF_PATH = ROOT / "data" / "chart_2_data.pdf"
CSV_PATH = ROOT / "data" / "chart-2.csv"

# Party averages from chart_2_before.png: country -> (Rep/Lean Rep, Dem/Lean Dem)
PARTY_AVERAGES = {
    "Canada":       (58, 77),
    "Australia":    (65, 69),
    "Japan":        (65, 67),
    "U.K.":         (55, 66),
    "Italy":        (64, 65),
    "France":       (51, 64),
    "Mexico":       (46, 64),
    "Germany":      (55, 61),
    "South Korea":  (53, 58),
    "Brazil":       (53, 56),
    "South Africa": (41, 52),
    "India":        (42, 50),
    "Indonesia":    (45, 50),
    "Turkey":       (42, 47),
    "Argentina":    (49, 46),
    "China":        (29, 43),
    "Saudi Arabia": (37, 34),
    "Russia":       (28, 24),
}

COLUMNS = ["very_cold", "somewhat_cold", "neutral", "somewhat_warm", "very_warm", "no_answer"]

# "ASK IF ASSIGNED TO ... [N=1,151]" / "<code> <Country>" / "Sept 14-20, 2026 <6 values>"
ROW = re.compile(
    r"ASK IF ASSIGNED TO .+?\[N=([\d,]+)\]\s*\n\S+\s+(?:The )?(.+?)\s*\n"
    r"\s*Sept 14-20, 2026\s+((?:[\d*]+\s+){5}[\d*]+)"
)

text = "\n".join(page.extract_text() for page in PdfReader(PDF_PATH).pages)
rows = []
for n, country, values in ROW.findall(text):
    pct = [0 if v == "*" else int(v) for v in values.split()]
    rep, dem = PARTY_AVERAGES[country]
    rows.append({"country": country, "rep_avg": rep, "dem_avg": dem,
                 **dict(zip(COLUMNS, pct)), "n": int(n.replace(",", ""))})

df = pd.DataFrame(rows)
missing = set(PARTY_AVERAGES) - set(df.country)
assert not missing, f"Countries not found in PDF: {missing}"

df = df.sort_values("dem_avg", ascending=False)
df.to_csv(CSV_PATH, index=False)
print(f"Saved {CSV_PATH} ({len(df)} countries)")
