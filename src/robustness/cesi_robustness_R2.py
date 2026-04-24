"""
CESI ROBUSTNESS SUITE: R2: STRUCTURAL VARIANTS
==================================================
Tests CESI's survival under structural mutation, not parameter jitter.

  V1. JACKKNIFE : rebuild CESI four times, dropping one component each time
                   and renormalising remaining weights to sum=1.
                   Tests whether any single demand variable secretly drives
                   the index ("is CESI just an electricity index?").

  V2. ALTERNATIVE PROXIES : replace each demand component with a different
                             plausible proxy:
                               E -> final-energy (instead of primary)
                               X -> world cement production (heavy industry
                                    activity proxy, independent of grid)
                               I -> Baltic Dry Index annual mean (freight)
                               P -> raw population (no per-capita weighting)

  V3. PER-CAPITA : CESI_pc = (D/P) / S.  Directly answers "is CESI just a
                    population story?" If per-capita CESI also rises
                    monotonically, the population objection is dead.

  V4. SUPPLY-SIDE STRUCTURAL VARIANTS
                 : Replace EROI step with continuous PCHIP
                 : Replace OPEC haircut with the era-based opec_share()
                    function from energy_graph.py (more conservative)
                 : Use undeflated reserves, see how bad it gets

Outputs:
  cesi_R2_runs.csv            : every variant + metrics
  cesi_R2_paths.csv           : full CESI(t) for each variant
  CESI_robustness_R2.png/.svg : 4-panel dashboard
"""

import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Reuse the carefully embedded data + core function from R1
from cesi_robustness_R1 import (
    YEARS, E_EJ, ELEC_TWH, I_INDEX, P_INDEX_RAW, POPULATION,
    OIL_RES, PROD_GBBL, EROI_POINTS_BASE, eroi_from_points,
    eroi_pchip_path, compute_cesi, metrics, rank_corr,
)

# =============================================================
# ALTERNATIVE PROXY DATA SERIES
# =============================================================

# --- Final energy consumption (EJ) ---
# Source: IEA WEB final consumption + back-extrapolation from primary
# Approximated as 0.68 * primary (consistent ~32% conversion losses globally)
# Slight upward drift in efficiency (final/primary rises 0.65 -> 0.71 over 1980-2023)
def final_energy_ej(y):
    eff = 0.65 + (y - 1980) * (0.71 - 0.65) / (2023 - 1980)
    return E_EJ[y] * eff

E_FINAL = {y: final_energy_ej(y) for y in YEARS}

# --- World cement production (Mt/yr) ---
# Source: USGS Mineral Commodity Summaries, cement chapter
CEMENT_MT = {
    1980:880,1981:900,1982:910,1983:945,1984:970,1985:1000,1986:1040,
    1987:1080,1988:1130,1989:1130,1990:1140,1991:1160,1992:1230,1993:1300,
    1994:1380,1995:1450,1996:1480,1997:1530,1998:1570,1999:1660,2000:1660,
    2001:1730,2002:1830,2003:1990,2004:2120,2005:2310,2006:2540,2007:2770,
    2008:2840,2009:3000,2010:3310,2011:3590,2012:3800,2013:4080,2014:4180,
    2015:4180,2016:4170,2017:4080,2018:4100,2019:4120,2020:4170,
    2021:4400,2022:4100,2023:4100,
}

# --- Baltic Dry Index annual mean ---
# Source: Lloyd's List / TradingEconomics historical
BDI = {
    1980:1700,1981:1300,1982:870,1983:830,1984:880,1985:710,1986:580,
    1987:1080,1988:1430,1989:1690,1990:1450,1991:1340,1992:1140,1993:1280,
    1994:1840,1995:2090,1996:1370,1997:1420,1998:1160,1999:1230,2000:1610,
    2001:1170,2002:1120,2003:2620,2004:4470,2005:3370,2006:3180,2007:7070,
    2008:6390,2009:2620,2010:2755,2011:1549,2012:920,2013:1206,2014:1105,
    2015:710,2016:673,2017:1150,2018:1352,2019:1353,2020:1066,2021:2942,
    2022:1934,2023:1378,
}

# --- Raw population index (no per-capita weighting) ---
P_RAW = {y: 100*POPULATION[y]/POPULATION[1980] for y in YEARS}

# =============================================================
# GENERIC CESI BUILDER (variable demand mix)
# =============================================================
def build_cesi(D_components, weights, supply_kwargs=None):
    """D_components: list of (series_dict, base_year_value) tuples.
       weights: list of weights summing to 1.
       supply_kwargs: dict passed to compute_cesi for the supply side only
                      (we will hijack compute_cesi by overriding the
                      D in post.): simpler approach: replicate supply locally."""
    # Compute D
    D = {}
    for y in YEARS:
        d = 0.0
        for (series, base), w in zip(D_components, weights):
            d += w * 100.0 * series[y] / base
        D[y] = d

    # Supply (use baseline parameters from compute_cesi)
    sk = supply_kwargs or {}
    haircut  = sk.get("haircut", 0.25)
    eroi_pts = sk.get("eroi_points", EROI_POINTS_BASE)
    eroi_arr = sk.get("eroi_path_array", None)
    rp_crit  = sk.get("rp_crit", 20.0)
    eroi_crit= sk.get("eroi_crit", 7.0)
    base_y   = sk.get("base_year", 1980)

    if eroi_arr is not None:
        eroi = eroi_arr
    else:
        eroi = {y: eroi_from_points(y, eroi_pts) for y in YEARS}

    Res = {y: OIL_RES[y] if y <= 1987 else OIL_RES[y]*(1.0 - haircut) for y in YEARS}
    RP  = {y: Res[y]/PROD_GBBL[y] for y in YEARS}
    RP_n  = {y: 100*RP[y]/RP[base_y] for y in YEARS}
    ER_n  = {y: 100*eroi[y]/eroi[base_y] for y in YEARS}

    def calc_S_raw(y):
        S = (RP_n[y]*ER_n[y])/100.0
        if RP[y] < rp_crit:
            Tr = rp_crit - RP[y]; S = S/(1.0 + (Tr/rp_crit)**2)
        if eroi[y] < eroi_crit:
            Te = eroi_crit - eroi[y]; S = S/(1.0 + (Te/eroi_crit)**2)
        return S

    S_raw = {y: calc_S_raw(y) for y in YEARS}
    S = {y: S_raw[y]*100.0/S_raw[base_y] for y in YEARS}

    cesi = {y: (D[y]/S[y])*100.0 for y in YEARS}
    cesi = {y: cesi[y]*100.0/cesi[base_y] for y in YEARS}
    return cesi, D, S

# Baseline references
baseline_components = [
    (E_EJ,        E_EJ[1980]),
    (ELEC_TWH,    ELEC_TWH[1980]),
    (I_INDEX,     I_INDEX[1980]),
    (P_INDEX_RAW, P_INDEX_RAW[1980]),
]
baseline_w = [0.40, 0.30, 0.20, 0.10]
baseline_cesi, _, _ = build_cesi(baseline_components, baseline_w)
baseline_vals = [baseline_cesi[y] for y in YEARS]
baseline_m = metrics(baseline_cesi)

# =============================================================
# VARIANTS
# =============================================================
runs = []   # (run_id, family, cesi)

def add(run_id, family, cesi):
    m = metrics(cesi)
    vals = [cesi[y] for y in YEARS]
    m["rank_corr_vs_base"] = rank_corr(vals, baseline_vals)
    m["delta_cesi2023_pct"] = 100*(m["cesi_2023"]-baseline_m["cesi_2023"])/baseline_m["cesi_2023"]
    runs.append((run_id, family, cesi, m))

# Baseline
add("baseline", "baseline", baseline_cesi)

# ---------- V1. JACKKNIFE: drop one component, rebalance ----------
labels = ["E", "X", "I", "P"]
for drop_idx, lbl in enumerate(labels):
    keep_idx = [i for i in range(4) if i != drop_idx]
    keep_components = [baseline_components[i] for i in keep_idx]
    keep_w_raw = [baseline_w[i] for i in keep_idx]
    s = sum(keep_w_raw)
    keep_w = [w/s for w in keep_w_raw]
    cesi, _, _ = build_cesi(keep_components, keep_w)
    add(f"jackknife_drop_{lbl}", "jackknife", cesi)

# ---------- V2. ALTERNATIVE PROXIES: swap one component, keep weight ----------
# Swap E -> final-energy
comp_E_final = [(E_FINAL, E_FINAL[1980])] + baseline_components[1:]
add("alt_E=final_energy", "alt_proxy",
    build_cesi(comp_E_final, baseline_w)[0])

# Swap X -> cement production
comp_X_cement = [baseline_components[0], (CEMENT_MT, CEMENT_MT[1980])] + baseline_components[2:]
add("alt_X=cement_Mt", "alt_proxy",
    build_cesi(comp_X_cement, baseline_w)[0])

# Swap I -> Baltic Dry Index (very volatile: averaged in metrics)
comp_I_bdi = baseline_components[:2] + [(BDI, BDI[1980])] + baseline_components[3:]
add("alt_I=BalticDryIdx", "alt_proxy",
    build_cesi(comp_I_bdi, baseline_w)[0])

# Swap P -> raw population (no per-capita weighting)
comp_P_raw = baseline_components[:3] + [(P_RAW, P_RAW[1980])]
add("alt_P=raw_population", "alt_proxy",
    build_cesi(comp_P_raw, baseline_w)[0])

# Swap ALL: E_final + cement + BDI + raw_pop
comp_all_alt = [(E_FINAL, E_FINAL[1980]), (CEMENT_MT, CEMENT_MT[1980]),
                (BDI, BDI[1980]), (P_RAW, P_RAW[1980])]
add("alt_ALL_swapped", "alt_proxy",
    build_cesi(comp_all_alt, baseline_w)[0])

# ---------- V3. PER-CAPITA CESI ----------
# CESI_pc = (D/P) / S: divide demand by raw population
def build_cesi_per_capita():
    cesi_normal, D, S = build_cesi(baseline_components, baseline_w)
    pop_norm = {y: POPULATION[y]/POPULATION[1980] for y in YEARS}
    D_pc = {y: D[y]/pop_norm[y] for y in YEARS}
    cesi_pc_raw = {y: (D_pc[y]/S[y])*100 for y in YEARS}
    base = cesi_pc_raw[1980]
    return {y: cesi_pc_raw[y]*100/base for y in YEARS}

add("per_capita_CESI", "per_capita", build_cesi_per_capita())

# ---------- V4. SUPPLY-SIDE STRUCTURAL ----------
# Continuous EROI (PCHIP) instead of step
add("supply_eroi_PCHIP", "supply_struct",
    build_cesi(baseline_components, baseline_w,
               supply_kwargs={"eroi_path_array": eroi_pchip_path()})[0])

# Era-based OPEC share (energy_graph.py methodology: more conservative)
def era_haircut_cesi():
    def opec_share(y):
        if y < 1988: return 0.67
        elif y < 2003: return 0.78
        elif y < 2010: return 0.73
        else: return 0.72
    Res = {y: OIL_RES[y]*(1.0 - opec_share(y)*0.25) for y in YEARS}
    RP  = {y: Res[y]/PROD_GBBL[y] for y in YEARS}
    RP_n  = {y: 100*RP[y]/RP[1980] for y in YEARS}
    eroi = {y: eroi_from_points(y, EROI_POINTS_BASE) for y in YEARS}
    ER_n  = {y: 100*eroi[y]/eroi[1980] for y in YEARS}
    def calc_S(y):
        S = (RP_n[y]*ER_n[y])/100.0
        if RP[y] < 20:  S /= (1.0 + ((20-RP[y])/20)**2)
        if eroi[y] < 7: S /= (1.0 + ((7-eroi[y])/7)**2)
        return S
    S_raw = {y: calc_S(y) for y in YEARS}
    S = {y: S_raw[y]*100/S_raw[1980] for y in YEARS}
    D = {}
    for y in YEARS:
        D[y] = (0.40*100*E_EJ[y]/E_EJ[1980] + 0.30*100*ELEC_TWH[y]/ELEC_TWH[1980]
              + 0.20*100*I_INDEX[y]/I_INDEX[1980] + 0.10*100*P_INDEX_RAW[y]/P_INDEX_RAW[1980])
    cesi = {y: (D[y]/S[y])*100 for y in YEARS}
    return {y: cesi[y]*100/cesi[1980] for y in YEARS}

add("supply_era_OPEC_share", "supply_struct", era_haircut_cesi())

# Undeflated reserves (haircut = 0%): known to fail in R1, included for context
add("supply_undeflated", "supply_struct",
    build_cesi(baseline_components, baseline_w,
               supply_kwargs={"haircut": 0.0})[0])

# =============================================================
# REPORT
# =============================================================
print("="*70)
print(f"R2 STRUCTURAL VARIANTS  --  {len(runs)} configurations")
print("="*70)
print(f"\nBaseline CESI_2023 = {baseline_m['cesi_2023']:.2f}\n")

print(f"{'Run':35s} {'Family':15s} {'CESI_2023':>10s} {'d%':>8s} {'Crit A':>7s} {'Crit C':>7s} {'rho':>6s}")
print("-"*92)
for rid, fam, cesi, m in runs:
    flag_A = "PASS" if m["crit_A_monotonic"] else "FAIL"
    flag_C = "PASS" if m["crit_C_rising_floor"] else "FAIL"
    print(f"{rid:35s} {fam:15s} {m['cesi_2023']:10.2f} {m['delta_cesi2023_pct']:+8.1f} "
          f"{flag_A:>7s} {flag_C:>7s} {m['rank_corr_vs_base']:6.3f}")

# Aggregate
non_base = [r for r in runs if r[0] != "baseline"]
critA = sum(1 for r in non_base if r[3]["crit_A_monotonic"])
critC = sum(1 for r in non_base if r[3]["crit_C_rising_floor"])
rcs = np.array([r[3]["rank_corr_vs_base"] for r in non_base])
print(f"\nNon-baseline structural variants: {len(non_base)}")
print(f"  Crit A pass rate: {critA}/{len(non_base)} = {100.0*critA/len(non_base):.1f}%")
print(f"  Crit C pass rate: {critC}/{len(non_base)} = {100.0*critC/len(non_base):.1f}%")
print(f"  Median rank-corr vs baseline: {np.median(rcs):.3f}")
print(f"  Min rank-corr vs baseline:    {rcs.min():.3f}")

# By family pass rates
families = sorted(set(r[1] for r in non_base))
print("\nBy family:")
for fam in families:
    fam_runs = [r for r in non_base if r[1] == fam]
    nA = sum(1 for r in fam_runs if r[3]["crit_A_monotonic"])
    nC = sum(1 for r in fam_runs if r[3]["crit_C_rising_floor"])
    rc_med = np.median([r[3]["rank_corr_vs_base"] for r in fam_runs])
    print(f"  {fam:15s}  n={len(fam_runs):2d}  CritA={nA}/{len(fam_runs)}  "
          f"CritC={nC}/{len(fam_runs)}  median rho={rc_med:.3f}")

# =============================================================
# CSV exports
# =============================================================
with open("C:/Users/OMU/Desktop/Energy/cesi_R2_runs.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["run_id","family","CESI_1980","CESI_2023","delta_pct",
                "max_dd_pct","crit_A","crit_C","rank_corr_vs_base"])
    for rid, fam, cesi, m in runs:
        w.writerow([rid, fam,
                    f"{m['cesi_1980']:.3f}", f"{m['cesi_2023']:.3f}",
                    f"{m['delta_cesi2023_pct']:+.2f}",
                    f"{m['max_dd_pct']*100:.2f}",
                    int(m['crit_A_monotonic']), int(m['crit_C_rising_floor']),
                    f"{m['rank_corr_vs_base']:.4f}"])
print("\nSaved: cesi_R2_runs.csv")

with open("C:/Users/OMU/Desktop/Energy/cesi_R2_paths.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["year"] + [r[0] for r in runs])
    for y in YEARS:
        w.writerow([y] + [f"{r[2][y]:.3f}" for r in runs])
print("Saved: cesi_R2_paths.csv")

# =============================================================
# DASHBOARD
# =============================================================
ACCENT="#1B3A5C"; ACCENT2="#2E75B6"; GREEN="#27AE60"; RED="#C0392B"
GREY="#7F8C8D"; AMBER="#E67E22"; PURPLE="#8E44AD"; ORANGE="#D35400"

family_colors = {
    "baseline":     ACCENT,
    "jackknife":    ORANGE,
    "alt_proxy":    PURPLE,
    "per_capita":   GREEN,
    "supply_struct":AMBER,
}

fig = plt.figure(figsize=(15, 11))
fig.suptitle(f"CESI ROBUSTNESS R2: Structural Variants ({len(runs)} configurations)",
             fontsize=14, fontweight="bold", color=ACCENT)

# Panel 1: All paths overlaid
ax1 = fig.add_subplot(2, 2, 1)
for rid, fam, cesi, m in runs:
    vals = [cesi[y] for y in YEARS]
    if rid == "baseline":
        ax1.plot(YEARS, vals, color=ACCENT, lw=2.6, label="baseline")
    else:
        col = family_colors.get(fam, GREY)
        ls = "-" if m["crit_A_monotonic"] else ":"
        ax1.plot(YEARS, vals, color=col, lw=1.0, alpha=0.7, ls=ls)
# Custom legend (one entry per family)
import matplotlib.lines as mlines
handles = [mlines.Line2D([],[],color=family_colors[fam], lw=2, label=fam)
           for fam in family_colors]
handles.append(mlines.Line2D([],[],color=GREY, lw=1, ls=":", label="failed Crit A"))
ax1.legend(handles=handles, loc="upper left", fontsize=8)
ax1.set_title("CESI(t) under structural variants", fontweight="bold")
ax1.set_ylabel("CESI (1980=100)"); ax1.set_xlabel("Year")
ax1.grid(True, alpha=0.3)

# Panel 2: Per-family bar chart of pass rates
ax2 = fig.add_subplot(2, 2, 2)
family_data = []
for fam in families:
    fam_runs = [r for r in non_base if r[1] == fam]
    nA = sum(1 for r in fam_runs if r[3]["crit_A_monotonic"])
    nC = sum(1 for r in fam_runs if r[3]["crit_C_rising_floor"])
    family_data.append((fam, len(fam_runs),
                        100.0*nA/len(fam_runs), 100.0*nC/len(fam_runs)))
x = np.arange(len(family_data))
w = 0.35
fa = [d[2] for d in family_data]
fc = [d[3] for d in family_data]
b1 = ax2.bar(x-w/2, fa, w, color=ACCENT2, label="Crit A (monotonic)")
b2 = ax2.bar(x+w/2, fc, w, color=GREEN,   label="Crit C (rising floor)")
ax2.set_xticks(x); ax2.set_xticklabels([d[0] for d in family_data], rotation=15, ha="right")
ax2.set_ylim(0, 110); ax2.axhline(80, color="black", ls="--", lw=0.6)
ax2.set_title("Pass rate by structural family (%)", fontweight="bold")
ax2.set_ylabel("Pass rate (%)")
ax2.grid(True, alpha=0.3, axis="y"); ax2.legend(fontsize=8)
for bars in (b1, b2):
    for b in bars:
        ax2.text(b.get_x()+b.get_width()/2, b.get_height()+1,
                 f"{b.get_height():.0f}", ha="center", fontsize=8)

# Panel 3: Per-capita CESI alongside baseline (key chart)
ax3 = fig.add_subplot(2, 2, 3)
pc_run = next(r for r in runs if r[0] == "per_capita_CESI")
ax3.plot(YEARS, [baseline_cesi[y] for y in YEARS], color=ACCENT, lw=2.4, label="baseline CESI")
ax3.plot(YEARS, [pc_run[2][y] for y in YEARS], color=GREEN, lw=2.4, label="per-capita CESI")
ax3.set_title("Per-capita variant: answers \"is this just population?\"", fontweight="bold")
ax3.set_ylabel("Index (1980=100)"); ax3.set_xlabel("Year")
ax3.grid(True, alpha=0.3); ax3.legend(loc="upper left")
# Annotate
pc2023 = pc_run[3]["cesi_2023"]
b2023  = baseline_m["cesi_2023"]
ax3.annotate(f"PC = {pc2023:.0f}\nbaseline = {b2023:.0f}",
             xy=(2023, pc2023), xytext=(2005, pc2023*0.7),
             fontsize=9, arrowprops=dict(arrowstyle="->", color=GREY))

# Panel 4: Summary table
ax4 = fig.add_subplot(2, 2, 4); ax4.axis("off")
rows = [["Family", "n", "Crit A", "Crit C", "median rho", "median d%"]]
for fam in families:
    fam_runs = [r for r in non_base if r[1] == fam]
    nA = sum(1 for r in fam_runs if r[3]["crit_A_monotonic"])
    nC = sum(1 for r in fam_runs if r[3]["crit_C_rising_floor"])
    rcm = np.median([r[3]["rank_corr_vs_base"] for r in fam_runs])
    dcm = np.median([r[3]["delta_cesi2023_pct"] for r in fam_runs])
    rows.append([fam, str(len(fam_runs)),
                 f"{nA}/{len(fam_runs)}", f"{nC}/{len(fam_runs)}",
                 f"{rcm:.3f}", f"{dcm:+.1f}%"])
rows.append(["OVERALL (non-baseline)", str(len(non_base)),
             f"{critA}/{len(non_base)} ({100*critA/len(non_base):.0f}%)",
             f"{critC}/{len(non_base)} ({100*critC/len(non_base):.0f}%)",
             f"{np.median(rcs):.3f}",
             f"{np.median([r[3]['delta_cesi2023_pct'] for r in non_base]):+.1f}%"])
tbl = ax4.table(cellText=rows, loc="center", cellLoc="center",
                colWidths=[0.25, 0.08, 0.13, 0.13, 0.13, 0.13])
tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1, 1.5)
for j in range(6):
    tbl[(0,j)].set_facecolor(ACCENT); tbl[(0,j)].set_text_props(color="white", weight="bold")
for j in range(6):
    tbl[(len(rows)-1,j)].set_facecolor("#EAEFF5"); tbl[(len(rows)-1,j)].set_text_props(weight="bold")
ax4.set_title("Per-family summary", fontweight="bold", color=ACCENT)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("C:/Users/OMU/Desktop/Energy/CESI_robustness_R2.png", dpi=160, bbox_inches="tight")
plt.savefig("C:/Users/OMU/Desktop/Energy/CESI_robustness_R2.svg", bbox_inches="tight")
plt.close()
print("Saved: CESI_robustness_R2.png / .svg")

print("="*70)
print("R2 COMPLETE")
print("="*70)
