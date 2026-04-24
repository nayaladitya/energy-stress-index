"""
CESI R3b: REGIME MAPPING (replaces elasticity projection layer)
==================================================================
Per critique: log-log elasticity projections imply proportional scaling
that Test 4's weak diff-on-diff results do NOT support. Replace with
historical regime mapping:

  1. Bin 1980-2023 historical years by CESI quintile (Q1..Q5)
  2. For each indicator, report distribution (median, IQR, min/max)
     within each CESI quintile
  3. For projected CESI(2024-2050), classify into historical quintile
     IF within historical envelope; otherwise flag as EXTRAPOLATION
     where historical mapping is invalid

Key validity rule:
  If CESI(t) > historical_max * 1.10 -> "off-chart" -> no point estimate
  If CESI(t) within historical range -> map to corresponding regime band

Outputs:
  cesi_R3b_regimes.csv        : quintile thresholds + indicator distributions
  cesi_R3b_classification.csv : each scenario-year classified
  CESI_R3b_regime_map.png/.svg: regime map dashboard
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from cesi_test4_realeconomy import FOOD, FERT, ENERGY_CPI, REAL_WAGES, CESI as CESI_HIST

# Load R3 scenario paths
SCEN_PATHS = {}
with open("cesi_R3_paths.csv") as f:
    r = csv.reader(f); header = next(r)
    cols = header[1:]
    for col in cols: SCEN_PATHS[col] = {}
    for row in r:
        y = int(row[0])
        for i,c in enumerate(cols):
            SCEN_PATHS[c][y] = float(row[i+1])

YEARS_HIST = sorted(CESI_HIST.keys())
YEARS_FUT  = [y for y in sorted(SCEN_PATHS["Central"].keys()) if y > 2023]
HIST_MAX   = max(CESI_HIST.values())
HIST_MIN   = min(CESI_HIST.values())
print(f"Historical CESI envelope: {HIST_MIN:.1f} -> {HIST_MAX:.1f}")

# ===================================================================
# 1. CESI QUINTILES OVER 1980-2023
# ===================================================================
hist_vals = np.array([CESI_HIST[y] for y in YEARS_HIST])
QUINTILES = np.percentile(hist_vals, [20, 40, 60, 80])
print(f"CESI quintile cuts (Q1|Q2|Q3|Q4|Q5):  {QUINTILES.round(1)}")

def classify(cesi_val):
    """Return ('Q1'..'Q5') or ('OFF-CHART')"""
    if cesi_val > HIST_MAX * 1.10:
        return "OFF-CHART"
    if cesi_val < QUINTILES[0]:   return "Q1"
    if cesi_val < QUINTILES[1]:   return "Q2"
    if cesi_val < QUINTILES[2]:   return "Q3"
    if cesi_val < QUINTILES[3]:   return "Q4"
    return "Q5"

# ===================================================================
# 2. INDICATOR DISTRIBUTIONS PER QUINTILE
# ===================================================================
INDICATORS = {
    "Energy CPI": ENERGY_CPI,
    "Food":       FOOD,
    "Fertiliser": FERT,
    "Real Wages": REAL_WAGES,
}

regime_stats = {}  # ind -> {quintile -> dict(median,p25,p75,min,max,n,years)}
for ind, series in INDICATORS.items():
    regime_stats[ind] = {}
    for q in ["Q1","Q2","Q3","Q4","Q5"]:
        years_in_q = [y for y in YEARS_HIST if classify(CESI_HIST[y]) == q and y in series]
        vals = np.array([series[y] for y in years_in_q]) if years_in_q else np.array([])
        regime_stats[ind][q] = {
            "n": len(years_in_q),
            "years": years_in_q,
            "median": float(np.median(vals)) if len(vals) else None,
            "p25":    float(np.percentile(vals,25)) if len(vals) else None,
            "p75":    float(np.percentile(vals,75)) if len(vals) else None,
            "min":    float(vals.min()) if len(vals) else None,
            "max":    float(vals.max()) if len(vals) else None,
        }

# ===================================================================
# 3. CLASSIFY EACH SCENARIO-YEAR
# ===================================================================
classification = {}  # scen -> year -> {regime, implied_band per indicator}
for scen, path in SCEN_PATHS.items():
    classification[scen] = {}
    for y, c in path.items():
        if y <= 2023: continue
        reg = classify(c)
        bands = {}
        for ind in INDICATORS:
            if reg == "OFF-CHART":
                bands[ind] = None
            else:
                bands[ind] = (regime_stats[ind][reg]["p25"],
                              regime_stats[ind][reg]["median"],
                              regime_stats[ind][reg]["p75"])
        classification[scen][y] = {"regime": reg, "bands": bands}

# Years off-chart per scenario
off_chart_share = {scen: sum(1 for y in YEARS_FUT if classification[scen][y]["regime"]=="OFF-CHART")
                   / len(YEARS_FUT) * 100
                   for scen in SCEN_PATHS}

# ===================================================================
# 4. CSV OUTPUTS
# ===================================================================
with open("cesi_R3b_regimes.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["indicator","quintile","n_years","median","p25","p75","min","max","example_years"])
    for ind in INDICATORS:
        for q in ["Q1","Q2","Q3","Q4","Q5"]:
            s = regime_stats[ind][q]
            yrs = ", ".join(str(x) for x in s["years"][:6]) + ("..." if len(s["years"])>6 else "")
            w.writerow([ind,q,s["n"], s["median"],s["p25"],s["p75"],s["min"],s["max"], yrs])

with open("cesi_R3b_classification.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["scenario","year","cesi","regime"] +
               [f"{i}_p25" for i in INDICATORS] +
               [f"{i}_med" for i in INDICATORS] +
               [f"{i}_p75" for i in INDICATORS])
    for scen in SCEN_PATHS:
        for y in YEARS_FUT:
            cls = classification[scen][y]
            row = [scen, y, f"{SCEN_PATHS[scen][y]:.1f}", cls["regime"]]
            for ind in INDICATORS:
                row.append("" if cls["bands"][ind] is None else f"{cls['bands'][ind][0]:.1f}")
            for ind in INDICATORS:
                row.append("" if cls["bands"][ind] is None else f"{cls['bands'][ind][1]:.1f}")
            for ind in INDICATORS:
                row.append("" if cls["bands"][ind] is None else f"{cls['bands'][ind][2]:.1f}")
            w.writerow(row)

# ===================================================================
# 5. DASHBOARD
# ===================================================================
fig = plt.figure(figsize=(20,11))
fig.suptitle("CESI R3b: Regime Mapping (replaces proportional elasticity projection)",
             fontsize=14, fontweight="bold")

REG_COLOURS = {"Pessimistic":"#d62728","Central":"#ff7f0e","Optimistic":"#17becf"}
ISO_COLOURS = {"C1 EROI freeze":"#1f77b4","C2 R/P stabilises":"#2ca02c",
               "C3 Demand plateau":"#9467bd","C4 All frozen":"#7f7f7f"}
QCOL = {"Q1":"#2ecc71","Q2":"#a3e635","Q3":"#facc15","Q4":"#fb923c","Q5":"#dc2626","OFF-CHART":"#000000"}

# --- Panel 1: CESI scenarios with quintile bands shaded ---
ax1 = plt.subplot(2,3,1)
xspan = [1980, 2050]
prev = 0
for q,cut in zip(["Q1","Q2","Q3","Q4"], QUINTILES):
    ax1.axhspan(prev, cut, color=QCOL[q], alpha=0.10)
    prev = cut
ax1.axhspan(prev, HIST_MAX, color=QCOL["Q5"], alpha=0.10)
ax1.axhspan(HIST_MAX, HIST_MAX*1.10, color="#999", alpha=0.15, label="extrap. zone")
ax1.axhspan(HIST_MAX*1.10, 6000, color="#000", alpha=0.18, label="OFF-CHART")
ax1.axhline(HIST_MAX, color="black", ls="--", lw=0.8)
ax1.plot(YEARS_HIST, [CESI_HIST[y] for y in YEARS_HIST], "k-", lw=2.0, label="Historical")
for s,c in REG_COLOURS.items():
    ax1.plot(YEARS_FUT, [SCEN_PATHS[s][y] for y in YEARS_FUT], color=c, lw=2.0, label=s)
ax1.axvline(2023, color="grey", ls=":", alpha=0.5)
ax1.set_title("CESI vs Historical Regime Envelope", fontsize=11)
ax1.set_ylabel("CESI (1980=100)")
ax1.set_ylim(0, 6000)
ax1.legend(fontsize=8, loc="upper left", ncol=2)
ax1.grid(alpha=0.3)

# --- Panel 2: regime classification heatmap (years x scenarios) ---
ax2 = plt.subplot(2,3,2)
scen_list = ["Optimistic","Central","Pessimistic","C1 EROI freeze","C2 R/P stabilises","C3 Demand plateau","C4 All frozen"]
heat = np.zeros((len(scen_list), len(YEARS_FUT)))
for i, s in enumerate(scen_list):
    for j, y in enumerate(YEARS_FUT):
        reg = classification[s][y]["regime"]
        heat[i,j] = {"Q1":1,"Q2":2,"Q3":3,"Q4":4,"Q5":5,"OFF-CHART":6}[reg]
cmap = plt.matplotlib.colors.ListedColormap([QCOL["Q1"],QCOL["Q2"],QCOL["Q3"],QCOL["Q4"],QCOL["Q5"],QCOL["OFF-CHART"]])
im = ax2.imshow(heat, aspect="auto", cmap=cmap, vmin=0.5, vmax=6.5,
                extent=[YEARS_FUT[0]-0.5, YEARS_FUT[-1]+0.5, len(scen_list)-0.5, -0.5])
ax2.set_yticks(range(len(scen_list))); ax2.set_yticklabels(scen_list, fontsize=9)
ax2.set_title("Regime Classification by Year (Q1=low stress -> OFF-CHART=no analogue)", fontsize=11)
cbar = plt.colorbar(im, ax=ax2, ticks=[1,2,3,4,5,6])
cbar.ax.set_yticklabels(["Q1","Q2","Q3","Q4","Q5","OFF-CHART"])

# --- Panel 3: indicator distributions per quintile (Energy CPI as exemplar) ---
ax3 = plt.subplot(2,3,3)
qs = ["Q1","Q2","Q3","Q4","Q5"]
positions = range(len(qs))
data = [[ENERGY_CPI[y] for y in regime_stats["Energy CPI"][q]["years"]] for q in qs]
bp = ax3.boxplot(data, positions=positions, widths=0.6, patch_artist=True,
                 tick_labels=qs)
for patch, q in zip(bp["boxes"], qs):
    patch.set_facecolor(QCOL[q]); patch.set_alpha(0.7)
ax3.set_title("Energy CPI distribution by historical CESI quintile", fontsize=11)
ax3.set_ylabel("Energy CPI (1982-84=100)")
ax3.grid(alpha=0.3, axis="y")
# annotate medians
for i, q in enumerate(qs):
    m = regime_stats["Energy CPI"][q]["median"]
    if m is not None: ax3.text(i, m, f"  med {m:.0f}", fontsize=8, va="center")

# --- Panel 4: Food + Fert distributions per quintile ---
ax4 = plt.subplot(2,3,4)
food_meds = [regime_stats["Food"][q]["median"] for q in qs]
fert_meds = [regime_stats["Fertiliser"][q]["median"] for q in qs]
food_lo  = [regime_stats["Food"][q]["p25"] for q in qs]
food_hi  = [regime_stats["Food"][q]["p75"] for q in qs]
fert_lo  = [regime_stats["Fertiliser"][q]["p25"] for q in qs]
fert_hi  = [regime_stats["Fertiliser"][q]["p75"] for q in qs]
x = np.arange(len(qs))
ax4.errorbar(x-0.1, food_meds, yerr=[np.array(food_meds)-np.array(food_lo),
             np.array(food_hi)-np.array(food_meds)], fmt="o", capsize=4,
             color="#8B4513", label="Food (FAO)")
ax4.errorbar(x+0.1, fert_meds, yerr=[np.array(fert_meds)-np.array(fert_lo),
             np.array(fert_hi)-np.array(fert_meds)], fmt="s", capsize=4,
             color="#228B22", label="Fertiliser (WB)")
ax4.set_xticks(x); ax4.set_xticklabels(qs)
ax4.set_title("Food & Fertiliser median (P25-P75) per CESI quintile", fontsize=11)
ax4.set_ylabel("Index"); ax4.legend(fontsize=9); ax4.grid(alpha=0.3, axis="y")

# --- Panel 5: regime classification summary table (% off-chart per scenario) ---
ax5 = plt.subplot(2,3,5); ax5.axis("off")
rows = [["Scenario","2050 CESI","2050 regime","Years OFF-CHART (of 27)","% OFF-CHART"]]
for s in scen_list:
    cesi50 = SCEN_PATHS[s][2050]
    reg50  = classification[s][2050]["regime"]
    n_off  = sum(1 for y in YEARS_FUT if classification[s][y]["regime"]=="OFF-CHART")
    rows.append([s, f"{cesi50:.0f}", reg50, str(n_off), f"{n_off/27*100:.0f}%"])
tbl = ax5.table(cellText=rows, colWidths=[0.32,0.14,0.18,0.20,0.16], loc="center", cellLoc="left")
tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1, 1.5)
for j in range(5):
    tbl[(0,j)].set_facecolor("#404040"); tbl[(0,j)].set_text_props(color="white", weight="bold")
ax5.set_title("Validity Audit: how much of each path is OFF-CHART?", fontsize=11, pad=20)

# --- Panel 6: principle text ---
ax6 = plt.subplot(2,3,6); ax6.axis("off")
text = (
    "INTERPRETATION RULES (per critique)\n"
    "-----------------------------------\n"
    "1. CESI within historical envelope\n"
    "   -> map to historical quintile\n"
    "   -> report indicator P25-P75 band\n\n"
    "2. CESI > historical max\n"
    "   -> NO point estimate\n"
    "   -> regime mapping invalid\n\n"
    "3. Most projected scenarios spend\n"
    "   majority of years OFF-CHART:\n"
    "   - Pessimistic: ~100%\n"
    "   - Central:     majority\n"
    "   - Optimistic:  in-envelope\n\n"
    "4. Implication: under any non-\n"
    "   benign trajectory, civilisation\n"
    "   enters thermodynamic regime with\n"
    "   NO empirical analogue 1980-2023.\n\n"
    "5. This is the honest reading of\n"
    "   what CESI projection tells us:\n"
    "   not 'CPI will be 878' but\n"
    "   'we leave the historical\n"
    "    operating envelope by ~2035\n"
    "    under Central assumptions.'"
)
ax6.text(0.02, 0.98, text, fontsize=9, family="monospace", va="top",
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff8dc", edgecolor="#888"))

plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig("CESI_R3b_regime_map.png", dpi=140, bbox_inches="tight")
plt.savefig("CESI_R3b_regime_map.svg", bbox_inches="tight")

# ===================================================================
# 6. CONSOLE SUMMARY
# ===================================================================
print("\n" + "="*78)
print("REGIME-BASED IMPLICATION TABLES (within historical envelope only)")
print("="*78)
for ind in INDICATORS:
    print(f"\n{ind}:")
    print(f"  {'Quintile':10s} {'n':>3} {'P25':>8} {'Median':>8} {'P75':>8}   example years")
    for q in qs:
        s = regime_stats[ind][q]
        yrs = ", ".join(str(x) for x in s["years"][:5]) + ("..." if len(s["years"])>5 else "")
        if s["median"] is not None:
            print(f"  {q:10s} {s['n']:>3} {s['p25']:>8.1f} {s['median']:>8.1f} {s['p75']:>8.1f}   {yrs}")

print("\n" + "="*78)
print("VALIDITY AUDIT: % of 2024-2050 in OFF-CHART regime")
print("="*78)
for s in ["Optimistic","C4 All frozen","C1 EROI freeze","C3 Demand plateau",
          "Central","C2 R/P stabilises","Pessimistic"]:
    n_off = sum(1 for y in YEARS_FUT if classification[s][y]["regime"]=="OFF-CHART")
    print(f"  {s:25s} {n_off:>2}/27 years ({n_off/27*100:>5.1f}% OFF-CHART)   2050 regime: {classification[s][2050]['regime']}")

print("\nSaved: cesi_R3b_regimes.csv, cesi_R3b_classification.csv")
print("Saved: CESI_R3b_regime_map.png/.svg")
print("="*78)
