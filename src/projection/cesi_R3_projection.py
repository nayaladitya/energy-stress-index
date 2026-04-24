"""
CESI R3 — CAUSAL-ISOLATION PROJECTION + IMPLICATION LAYER
==========================================================
Per GPT redesign: instead of one "thesis-breaker" projection that mixes
mechanisms, run four CAUSAL-ISOLATION scenarios (C1-C4) plus three
REGIME BUNDLES (Pess/Central/Optim), and for each project the implied
trajectories of the four real-economy anchors validated in Test 4
(Energy CPI, Food, Fertilisers, Real Wages).

CAUSAL ISOLATION (each freezes ONE mechanism, others on baseline trend):
  C1  EROI freeze       — EROI stays at 2023=9          (isolates EROI decline)
  C2  R/P stabilises    — reserves track production     (isolates reserve drag)
  C3  Demand plateau    — E,X,I,P stay at 2023 levels   (isolates demand growth)
  C4  Everything frozen — true null control             (isolates baseline inertia)

REGIME BUNDLES:
  Pessimistic — EROI -> 5, R/P -> 35, demand at historical CAGR
  Central     — linear continuation of all trends
  Optimistic  — EROI recovers to 12, demand plateau 2035, reserves stable

IMPLICATION LAYER:
  Calibrate log-log elasticities from 1980-2023 (5yr smoothed) for each
  Test-4 indicator: log(I_t) = a + b*log(CESI_t).
  Project I(t) from CESI(t) per scenario. Report as conditional structural
  bands, NOT annual forecasts.

Outputs:
  cesi_R3_paths.csv         — annual CESI per scenario
  cesi_R3_implications.csv  — implied indicator paths per scenario
  cesi_R3_elasticities.csv  — fitted log-log betas
  CESI_R3_projection.png/.svg — six-panel dashboard
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Reuse R1 data + compute_cesi
from cesi_robustness_R1 import (
    YEARS, E_EJ, ELEC_TWH, I_INDEX, P_INDEX_RAW, POPULATION,
    OIL_RES, OIL_PROD_KBPD, compute_cesi
)

# Load real-economy indicators from Test 4
from cesi_test4_realeconomy import FOOD, FERT, ENERGY_CPI, REAL_WAGES, CESI as CESI_HIST

YEARS_HIST = list(range(1980, 2024))
YEARS_FUT  = list(range(2024, 2051))
YEARS_ALL  = YEARS_HIST + YEARS_FUT

# ===================================================================
# 1. PROJECT INPUT TRAJECTORIES 2024-2050
# ===================================================================
# Using historical CAGR observed 1980-2023, applied to the same input
# series feeding compute_cesi(). We derive 2024-2050 values for each.

def cagr(d, y0, y1):
    return (d[y1]/d[y0])**(1.0/(y1-y0)) - 1.0

# --- Demand inputs ---
g_E = cagr(E_EJ,        1980, 2023)   # ~1.6%
g_X = cagr(ELEC_TWH,    1980, 2023)   # ~2.7%
g_I = cagr(I_INDEX,     1980, 2023)   # ~2.5%
g_P = cagr(POPULATION,  1980, 2023)   # ~1.4%

# Project two demand modes:
def project_demand(mode):
    """mode in {'baseline','plateau','high'}"""
    out_E = dict(E_EJ); out_X = dict(ELEC_TWH); out_I = dict(I_INDEX)
    out_P = dict(POPULATION); out_PI = dict(P_INDEX_RAW)
    if mode == "baseline":
        gE, gX, gI, gP = g_E*0.85, g_X*0.75, g_I*0.80, 0.007
    elif mode == "plateau":
        gE = gX = gI = gP = 0.0
    elif mode == "high":
        gE, gX, gI, gP = g_E, g_X, g_I, 0.010
    else:
        raise ValueError(mode)
    for y in YEARS_FUT:
        out_E[y]  = out_E[y-1]  * (1+gE)
        out_X[y]  = out_X[y-1]  * (1+gX)
        out_I[y]  = out_I[y-1]  * (1+gI)
        out_P[y]  = out_P[y-1]  * (1+gP)
        out_PI[y] = out_P[y] / out_P[1980] * 100.0
    return out_E, out_X, out_I, out_P, out_PI

# --- Supply inputs ---
def project_supply(mode):
    """mode in {'baseline','rp_stable','reserves_collapse','reserves_grow'}"""
    res = dict(OIL_RES); prod = dict(OIL_PROD_KBPD)
    # Production: held near 2023 ~ 81000 kbpd, slow decline
    g_prod = -0.005 if mode != "reserves_grow" else 0.0
    for y in YEARS_FUT:
        prod[y] = prod[y-1] * (1+g_prod)
    if mode == "baseline":
        # Reserves: grow ~0.3%/yr (discoveries minus depletion)
        for y in YEARS_FUT:
            res[y] = res[y-1] * 1.003
    elif mode == "rp_stable":
        # Reserves grow exactly with production drawdown to keep R/P at 2023 level
        rp_2023 = res[2023] / (prod[2023] * 365.0 / 1e6)  # production in Mbbl/yr
        for y in YEARS_FUT:
            target = rp_2023 * prod[y] * 365.0 / 1e6
            res[y] = target
    elif mode == "reserves_collapse":
        # Shale write-down + OPEC reckoning: reserves -2%/yr
        for y in YEARS_FUT:
            res[y] = res[y-1] * 0.98
    elif mode == "reserves_grow":
        for y in YEARS_FUT:
            res[y] = res[y-1] * 1.010
    return res, prod

# --- EROI trajectories (passed as eroi_path_array indexed to YEARS_ALL) ---
EROI_HIST_POINTS = {1980:25, 1992:22, 2000:18, 2006:16, 2010:15, 2015:12, 2020:10, 2023:9}

def build_eroi_path(mode):
    """Returns dict year->EROI for YEARS_ALL"""
    # historical via piecewise linear (matches compute_cesi default behavior)
    keys = sorted(EROI_HIST_POINTS.keys())
    hist = {}
    for y in YEARS_HIST:
        if y <= keys[0]:    hist[y] = EROI_HIST_POINTS[keys[0]]
        elif y >= keys[-1]: hist[y] = EROI_HIST_POINTS[keys[-1]]
        else:
            for i in range(len(keys)-1):
                if keys[i] <= y <= keys[i+1]:
                    f = (y - keys[i])/(keys[i+1]-keys[i])
                    hist[y] = EROI_HIST_POINTS[keys[i]] + f*(EROI_HIST_POINTS[keys[i+1]]-EROI_HIST_POINTS[keys[i]])
                    break
    fut = {}
    if mode == "baseline":   # extrapolate -0.15/yr down to floor 5
        v = hist[2023]
        for y in YEARS_FUT:
            v = max(5.0, v - 0.15)
            fut[y] = v
    elif mode == "freeze":   # C1 — EROI fixed at 9
        for y in YEARS_FUT: fut[y] = 9.0
    elif mode == "decline_steep":  # Pessimistic — -0.25/yr to floor 5
        v = hist[2023]
        for y in YEARS_FUT:
            v = max(5.0, v - 0.25)
            fut[y] = v
    elif mode == "recover":  # Optimistic — climbs back to 12 by 2050
        v0, v1 = hist[2023], 12.0
        for i, y in enumerate(YEARS_FUT, start=1):
            fut[y] = v0 + (v1 - v0) * (i / len(YEARS_FUT))
    elif mode == "frozen_2023":  # C4 — exactly 9 (same as freeze, kept for clarity)
        for y in YEARS_FUT: fut[y] = 9.0
    return {**hist, **fut}

# ===================================================================
# 2. SCENARIO DEFINITIONS
# ===================================================================
SCENARIOS = {
    # --- causal isolation ---
    "C1 EROI freeze":     dict(demand="baseline", supply="baseline",      eroi="freeze"),
    "C2 R/P stabilises":  dict(demand="baseline", supply="rp_stable",     eroi="baseline"),
    "C3 Demand plateau":  dict(demand="plateau",  supply="baseline",      eroi="baseline"),
    "C4 All frozen":      dict(demand="plateau",  supply="rp_stable",     eroi="frozen_2023"),
    # --- regime bundles ---
    "Pessimistic":        dict(demand="high",     supply="reserves_collapse", eroi="decline_steep"),
    "Central":            dict(demand="baseline", supply="baseline",      eroi="baseline"),
    "Optimistic":         dict(demand="plateau",  supply="reserves_grow", eroi="recover"),
}

# ===================================================================
# 3. RUN SCENARIOS
# ===================================================================
# Patch compute_cesi inputs by temporarily extending the YEARS list and
# substituting projected dicts. We achieve this by importing the bare
# computation logic and re-deriving CESI on YEARS_ALL with custom inputs.

def compute_cesi_extended(E, X, I, P_idx, P_pop, res, prod, eroi_path,
                          weights=(0.40,0.30,0.20,0.10), haircut=0.25,
                          rp_crit=20.0, eroi_crit=7.0, base_year=1980):
    """Replicates compute_cesi() but on YEARS_ALL with explicit input dicts."""
    wE,wX,wI,wP = weights
    Y = YEARS_ALL
    # base values
    bE, bX, bI, bP = E[base_year], X[base_year], I[base_year], P_idx[base_year]
    D = {}
    for y in Y:
        D[y] = (wE*(E[y]/bE) + wX*(X[y]/bX) + wI*(I[y]/bI) + wP*(P_idx[y]/bP)) * 100.0
    # Supply: R/P and EROI thresholds
    res_haircut = {y: res[y] * (1 - (haircut if y >= 1987 else 0.0)) for y in Y}
    rp = {y: res_haircut[y] / (prod[y] * 365.0 / 1e6) for y in Y}
    # threshold-adjusted multipliers
    S = {}
    base_rp   = rp[base_year]
    base_eroi = eroi_path[base_year]
    for y in Y:
        rp_eff   = rp[y]   if rp[y]   > rp_crit   else rp[y]   * (rp[y]/rp_crit)**1.5
        er_eff   = eroi_path[y] if eroi_path[y] > eroi_crit else eroi_path[y] * (eroi_path[y]/eroi_crit)**1.5
        rp_b     = base_rp if base_rp > rp_crit else base_rp * (base_rp/rp_crit)**1.5
        er_b     = base_eroi if base_eroi > eroi_crit else base_eroi * (base_eroi/eroi_crit)**1.5
        S[y] = (rp_eff/rp_b) * (er_eff/er_b) * 100.0
    cesi = {y: (D[y]/S[y]) * 100.0 for y in Y}
    # renormalise so cesi[base_year] = 100
    norm = cesi[base_year]
    return {y: cesi[y]/norm * 100.0 for y in Y}

scenario_paths = {}
for name, cfg in SCENARIOS.items():
    E, X, I, P_pop, P_idx = project_demand(cfg["demand"])
    res, prod = project_supply(cfg["supply"])
    eroi = build_eroi_path(cfg["eroi"])
    cesi = compute_cesi_extended(E, X, I, P_idx, P_pop, res, prod, eroi)
    scenario_paths[name] = cesi

# ===================================================================
# 4. CALIBRATE LOG-LOG ELASTICITIES (1980-2023, 5yr smoothed)
# ===================================================================
def smooth(d, w=5):
    keys = sorted(d.keys())
    arr = np.array([d[k] for k in keys])
    out = {}
    for i,k in enumerate(keys):
        lo = max(0,i-w+1); out[k] = float(arr[lo:i+1].mean())
    return out

def fit_loglog(cesi_dict, ind_dict):
    ys = sorted(set(cesi_dict)&set(ind_dict))
    cs = smooth({y:cesi_dict[y] for y in ys})
    is_ = smooth({y:ind_dict[y] for y in ys})
    x = np.log(np.array([cs[y]  for y in ys]))
    y = np.log(np.array([is_[y] for y in ys]))
    b, a = np.polyfit(x, y, 1)
    yhat = a + b*x
    ss_res = np.sum((y-yhat)**2); ss_tot = np.sum((y-y.mean())**2)
    r2 = 1 - ss_res/ss_tot
    return float(a), float(b), float(r2)

INDICATORS = {
    "Energy CPI": ENERGY_CPI,
    "Food":       FOOD,
    "Fertiliser": FERT,
    "Real Wages": REAL_WAGES,
}
elast = {}
for name, d in INDICATORS.items():
    a,b,r2 = fit_loglog(CESI_HIST, d)
    elast[name] = (a,b,r2)
    print(f"  {name:15s}  log-log:  a={a:+.3f}  beta={b:+.3f}  R^2={r2:.3f}")

# ===================================================================
# 5. PROJECT IMPLICATIONS PER SCENARIO
# ===================================================================
def project_indicator(cesi_dict, name):
    a, b, _ = elast[name]
    return {y: float(np.exp(a + b*np.log(c))) for y,c in cesi_dict.items()}

implications = {scen: {name: project_indicator(path, name) for name in INDICATORS}
                for scen, path in scenario_paths.items()}

# ===================================================================
# 6. CSV OUTPUTS
# ===================================================================
with open("cesi_R3_paths.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["year"] + list(scenario_paths.keys()))
    for y in YEARS_ALL:
        w.writerow([y] + [f"{scenario_paths[s][y]:.3f}" for s in scenario_paths])

with open("cesi_R3_implications.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["year","scenario","indicator","value"])
    for s in scenario_paths:
        for ind in INDICATORS:
            for y in YEARS_ALL:
                w.writerow([y, s, ind, f"{implications[s][ind][y]:.3f}"])

with open("cesi_R3_elasticities.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["indicator","alpha","beta","R2"])
    for n,(a,b,r2) in elast.items(): w.writerow([n,a,b,r2])

# ===================================================================
# 7. DASHBOARD (six-panel)
# ===================================================================
fig = plt.figure(figsize=(20,12))
fig.suptitle("CESI R3 — Causal-Isolation Projection + Real-Economy Implications  (2024-2050)",
             fontsize=14, fontweight="bold")

ISO_COLOURS = {"C1 EROI freeze":"#1f77b4","C2 R/P stabilises":"#2ca02c",
               "C3 Demand plateau":"#9467bd","C4 All frozen":"#7f7f7f"}
REG_COLOURS = {"Pessimistic":"#d62728","Central":"#ff7f0e","Optimistic":"#17becf"}

# --- Panel 1: causal-isolation CESI ---
ax1 = plt.subplot(2,3,1)
ax1.plot(YEARS_HIST, [CESI_HIST[y] for y in YEARS_HIST], "k-", lw=2.0, label="Historical")
for s,c in ISO_COLOURS.items():
    ax1.plot(YEARS_FUT, [scenario_paths[s][y] for y in YEARS_FUT], color=c, lw=1.6, label=s)
ax1.axvline(2023, color="grey", ls=":", alpha=0.5)
ax1.set_title("Causal Isolation — which mechanism drives CESI?", fontsize=11)
ax1.set_ylabel("CESI (1980=100)"); ax1.legend(fontsize=8, loc="upper left")
ax1.grid(alpha=0.3)

# --- Panel 2: regime bundles CESI ---
ax2 = plt.subplot(2,3,2)
ax2.plot(YEARS_HIST, [CESI_HIST[y] for y in YEARS_HIST], "k-", lw=2.0, label="Historical")
for s,c in REG_COLOURS.items():
    ax2.plot(YEARS_FUT, [scenario_paths[s][y] for y in YEARS_FUT], color=c, lw=2.0, label=s)
ax2.axvline(2023, color="grey", ls=":", alpha=0.5)
ax2.set_title("Regime Bundles — Pessimistic / Central / Optimistic", fontsize=11)
ax2.set_ylabel("CESI (1980=100)"); ax2.legend(fontsize=9)
ax2.grid(alpha=0.3)

# --- Panel 3: implied Energy CPI band ---
ax3 = plt.subplot(2,3,3)
hist = [ENERGY_CPI[y] for y in YEARS_HIST]
ax3.plot(YEARS_HIST, hist, "k-", lw=1.8, label="Historical")
for s,c in REG_COLOURS.items():
    proj = [implications[s]["Energy CPI"][y] for y in YEARS_FUT]
    ax3.plot(YEARS_FUT, proj, color=c, lw=1.8, label=s)
ax3.axvline(2023, color="grey", ls=":", alpha=0.5)
ax3.set_title(f"Implied Energy CPI  (elasticity beta={elast['Energy CPI'][1]:+.2f})", fontsize=11)
ax3.set_ylabel("FRED CPIENGSL  (1982-84=100)"); ax3.legend(fontsize=9)
ax3.grid(alpha=0.3)

# --- Panel 4: implied Food + Fertiliser bands ---
ax4 = plt.subplot(2,3,4)
ax4.plot(YEARS_HIST, [FOOD[y] for y in YEARS_HIST], "k-", lw=1.6, label="Food (hist)")
ax4.plot(YEARS_HIST, [FERT[y] for y in YEARS_HIST], "k--", lw=1.4, label="Fert (hist)")
for s,c in REG_COLOURS.items():
    ax4.plot(YEARS_FUT, [implications[s]["Food"][y]       for y in YEARS_FUT], color=c, lw=1.6)
    ax4.plot(YEARS_FUT, [implications[s]["Fertiliser"][y] for y in YEARS_FUT], color=c, lw=1.0, ls="--")
ax4.axvline(2023, color="grey", ls=":", alpha=0.5)
ax4.set_title(f"Implied Food (solid) & Fertiliser (dashed)  beta_food={elast['Food'][1]:+.2f}, beta_fert={elast['Fertiliser'][1]:+.2f}",
              fontsize=10)
ax4.set_ylabel("Index"); ax4.legend(fontsize=8); ax4.grid(alpha=0.3)

# --- Panel 5: implied Real Wages band (LOG-LOG WARNING NOTE) ---
ax5 = plt.subplot(2,3,5)
ax5.plot(YEARS_HIST, [REAL_WAGES[y] for y in YEARS_HIST], "k-", lw=1.8, label="Historical")
for s,c in REG_COLOURS.items():
    ax5.plot(YEARS_FUT, [implications[s]["Real Wages"][y] for y in YEARS_FUT], color=c, lw=1.8, label=s)
ax5.axvline(2023, color="grey", ls=":", alpha=0.5)
beta_w = elast["Real Wages"][1]
ax5.set_title(f"Implied Real Wages  (beta={beta_w:+.2f})  -- caveat: positive level beta is trend artefact",
              fontsize=10)
ax5.set_ylabel("OECD Index (2015=100)"); ax5.legend(fontsize=9); ax5.grid(alpha=0.3)

# --- Panel 6: Causal contribution table ---
ax6 = plt.subplot(2,3,6); ax6.axis("off")
cesi_2050 = {s: scenario_paths[s][2050] for s in scenario_paths}
cesi_C4   = scenario_paths["C4 All frozen"][2050]
cesi_central_2050 = scenario_paths["Central"][2050]

# How much of Central's 2050 rise above 2023 is removed by each freeze?
base_2023 = CESI_HIST[2023]
delta_central = cesi_central_2050 - base_2023
contrib = {}
for c in ["C1 EROI freeze","C2 R/P stabilises","C3 Demand plateau"]:
    removed = cesi_central_2050 - cesi_2050[c]   # how much rise this freeze suppresses
    contrib[c] = 100.0 * removed / delta_central if delta_central > 0 else 0.0

rows = [
    ["Scenario", "CESI 2050", "vs 2023", "% of Central rise"],
    ["Historical 2023", f"{base_2023:.0f}", "—", "—"],
    ["—" * 4, "", "", ""],
    ["C1 EROI freeze",     f"{cesi_2050['C1 EROI freeze']:.0f}",     f"{cesi_2050['C1 EROI freeze']-base_2023:+.0f}",     f"removes {contrib['C1 EROI freeze']:.0f}%"],
    ["C2 R/P stabilises",  f"{cesi_2050['C2 R/P stabilises']:.0f}",  f"{cesi_2050['C2 R/P stabilises']-base_2023:+.0f}",  f"removes {contrib['C2 R/P stabilises']:.0f}%"],
    ["C3 Demand plateau",  f"{cesi_2050['C3 Demand plateau']:.0f}",  f"{cesi_2050['C3 Demand plateau']-base_2023:+.0f}",  f"removes {contrib['C3 Demand plateau']:.0f}%"],
    ["C4 All frozen",      f"{cesi_2050['C4 All frozen']:.0f}",      f"{cesi_2050['C4 All frozen']-base_2023:+.0f}",      "control"],
    ["—" * 4, "", "", ""],
    ["Pessimistic",        f"{cesi_2050['Pessimistic']:.0f}",        f"{cesi_2050['Pessimistic']-base_2023:+.0f}",        ""],
    ["Central",            f"{cesi_2050['Central']:.0f}",            f"{cesi_2050['Central']-base_2023:+.0f}",            ""],
    ["Optimistic",         f"{cesi_2050['Optimistic']:.0f}",         f"{cesi_2050['Optimistic']-base_2023:+.0f}",         ""],
]
tbl = ax6.table(cellText=rows, colWidths=[0.30,0.18,0.18,0.30], loc="center", cellLoc="left")
tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1,1.4)
for j in range(4):
    tbl[(0,j)].set_facecolor("#404040"); tbl[(0,j)].set_text_props(color="white", weight="bold")
ax6.set_title("Causal Contribution to 2050 Rise (Central baseline)", fontsize=11, pad=20)

plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig("CESI_R3_projection.png", dpi=140, bbox_inches="tight")
plt.savefig("CESI_R3_projection.svg", bbox_inches="tight")

# ===================================================================
# 8. CONSOLE SUMMARY
# ===================================================================
print("\n" + "="*78)
print("CESI R3 — PROJECTION RESULTS")
print("="*78)
print(f"\n{'Scenario':25s} {'CESI 2023':>10} {'CESI 2050':>10} {'Delta':>10} {'CAGR%':>8}")
print("-"*78)
for s in scenario_paths:
    c23, c50 = base_2023, scenario_paths[s][2050]
    cg = ((c50/c23)**(1/27)-1)*100
    print(f"{s:25s} {c23:10.1f} {c50:10.1f} {c50-c23:+10.1f} {cg:+8.2f}")

print("\nCAUSAL CONTRIBUTION TO 2050 RISE (vs Central):")
for c in ["C1 EROI freeze","C2 R/P stabilises","C3 Demand plateau"]:
    print(f"  {c:25s} removes {contrib[c]:5.1f}% of Central rise")

print("\nIMPLIED 2050 INDICATORS (Central scenario):")
for ind in INDICATORS:
    v_2023 = INDICATORS[ind][2023]
    v_2050 = implications["Central"][ind][2050]
    print(f"  {ind:15s} 2023={v_2023:7.1f}  ->  2050={v_2050:7.1f}  ({(v_2050/v_2023-1)*100:+.0f}%)")

print("\nIMPLIED 2050 INDICATORS (Pessimistic scenario):")
for ind in INDICATORS:
    v_2023 = INDICATORS[ind][2023]
    v_2050 = implications["Pessimistic"][ind][2050]
    print(f"  {ind:15s} 2023={v_2023:7.1f}  ->  2050={v_2050:7.1f}  ({(v_2050/v_2023-1)*100:+.0f}%)")

print("\nIMPLIED 2050 INDICATORS (Optimistic scenario):")
for ind in INDICATORS:
    v_2023 = INDICATORS[ind][2023]
    v_2050 = implications["Optimistic"][ind][2050]
    print(f"  {ind:15s} 2023={v_2023:7.1f}  ->  2050={v_2050:7.1f}  ({(v_2050/v_2023-1)*100:+.0f}%)")

print("\nSaved: cesi_R3_paths.csv, cesi_R3_implications.csv, cesi_R3_elasticities.csv")
print("Saved: CESI_R3_projection.png/.svg")
print("="*78)
