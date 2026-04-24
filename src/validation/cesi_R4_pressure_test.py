"""
CESI R4 — PRESSURE TEST
========================
Hostile-referee test suite. Four checks before paper consolidation:

  P1  CONTROL TEST — does CESI add explanatory power for real-economy
                     stress AFTER controlling for global real GDP and
                     global broad money? (partial correlation)

  P2  SPURIOUS CORRELATION — does CESI also correlate with variables
                     it should NOT track (internet users, urbanisation,
                     literacy)? If yes, CESI is a time proxy.

  P3  E-ONLY NULL — construct CESI_E = E/S (energy alone, no demand
                     composite). Does the 4-component design add value?

  P4  FALSIFICATION — write three explicit conditions that would
                     refute CESI (not a test, a statement of disprovability).

Outputs:
  cesi_R4_pressure.csv          — all numerical results
  CESI_R4_pressure.png/.svg     — four-panel dashboard
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from cesi_robustness_R1 import (
    YEARS, E_EJ, ELEC_TWH, I_INDEX, P_INDEX_RAW, POPULATION,
    OIL_RES, OIL_PROD_KBPD, compute_cesi
)
from cesi_test4_realeconomy import FOOD, FERT, ENERGY_CPI, REAL_WAGES, CESI as CESI_HIST

# ===================================================================
# CONTROL VARIABLES (annual, 1980-2023)
# ===================================================================

# --- World real GDP, constant 2015 USD trillions (World Bank NY.GDP.MKTP.KD) ---
GDP_REAL = {
    1980:30.5,1981:31.0,1982:31.2,1983:32.0,1984:33.5,1985:34.7,1986:35.8,
    1987:37.0,1988:38.7,1989:40.0,1990:41.0,1991:41.6,1992:42.5,1993:43.7,
    1994:45.1,1995:46.6,1996:48.4,1997:50.3,1998:51.6,1999:53.2,2000:55.5,
    2001:56.8,2002:58.4,2003:60.3,2004:62.9,2005:65.4,2006:68.1,2007:70.9,
    2008:72.0,2009:71.2,2010:74.4,2011:77.1,2012:79.4,2013:81.8,2014:84.4,
    2015:86.7,2016:89.0,2017:91.9,2018:94.8,2019:97.2,2020:94.6,2021:100.4,
    2022:103.7,2023:106.5,
}

# --- US M2 money stock, $bn average (FRED M2SL annual mean) ---
# Used as proxy for global liquidity (well-documented, tightly co-moves with global M2)
M2 = {
    1980:1599,1981:1755,1982:1910,1983:2127,1984:2311,1985:2497,1986:2735,
    1987:2832,1988:2995,1989:3160,1990:3279,1991:3379,1992:3434,1993:3487,
    1994:3502,1995:3641,1996:3813,1997:4031,1998:4374,1999:4643,2000:4918,
    2001:5432,2002:5773,2003:6062,2004:6411,2005:6669,2006:7068,2007:7474,
    2008:7995,2009:8492,2010:8800,2011:9669,2012:10468,2013:11023,2014:11680,
    2015:12349,2016:13213,2017:13839,2018:14376,2019:15321,2020:18717,
    2021:21541,2022:21449,2023:20840,
}

# --- World internet users, % population (World Bank IT.NET.USER.ZS) ---
# SHOULD-NOT-CORRELATE control (technology adoption, not energy stress)
INTERNET = {
    1990:0.05,1991:0.10,1992:0.20,1993:0.30,1994:0.40,1995:0.78,1996:1.20,
    1997:1.86,1998:3.10,1999:4.50,2000:6.77,2001:8.10,2002:10.59,2003:12.31,
    2004:14.10,2005:15.79,2006:17.57,2007:20.65,2008:23.13,2009:25.66,
    2010:28.86,2011:31.78,2012:34.79,2013:37.61,2014:40.74,2015:43.86,
    2016:46.23,2017:49.05,2018:51.40,2019:53.74,2020:60.30,2021:63.10,
    2022:66.30,2023:67.40,
    # Pre-1990: essentially zero
    1980:0.0,1981:0.0,1982:0.0,1983:0.0,1984:0.0,1985:0.0,1986:0.0,1987:0.0,
    1988:0.0,1989:0.02,
}

# --- World urbanisation, % urban (World Bank SP.URB.TOTL.IN.ZS) ---
URBAN = {
    1980:39.3,1981:39.6,1982:39.9,1983:40.2,1984:40.5,1985:40.9,1986:41.2,
    1987:41.5,1988:41.9,1989:42.2,1990:42.9,1991:43.3,1992:43.7,1993:44.0,
    1994:44.3,1995:44.7,1996:45.1,1997:45.4,1998:45.8,1999:46.2,2000:46.7,
    2001:47.1,2002:47.6,2003:48.0,2004:48.5,2005:49.0,2006:49.4,2007:49.9,
    2008:50.4,2009:50.9,2010:51.6,2011:52.1,2012:52.6,2013:53.1,2014:53.6,
    2015:54.0,2016:54.5,2017:55.0,2018:55.5,2019:55.8,2020:56.2,2021:56.6,
    2022:57.1,2023:57.5,
}

# --- World adult literacy, % 15+ (UNESCO, 5yr interpolated) ---
LITERACY = {
    1980:63.4,1981:64.1,1982:64.8,1983:65.5,1984:66.2,1985:67.0,1986:67.8,
    1987:68.6,1988:69.4,1989:70.2,1990:71.0,1991:71.8,1992:72.6,1993:73.4,
    1994:74.2,1995:75.0,1996:75.8,1997:76.6,1998:77.4,1999:78.2,2000:79.0,
    2001:79.5,2002:80.0,2003:80.5,2004:81.0,2005:81.5,2006:82.0,2007:82.5,
    2008:83.0,2009:83.5,2010:84.0,2011:84.4,2012:84.8,2013:85.1,2014:85.5,
    2015:85.9,2016:86.2,2017:86.5,2018:86.7,2019:86.9,2020:87.0,2021:87.1,
    2022:87.2,2023:87.3,
}

# ===================================================================
# HELPERS
# ===================================================================
def common(*dicts):
    s = set(dicts[0])
    for d in dicts[1:]: s &= set(d)
    return sorted(s)

def pearson(a, b):
    return float(np.corrcoef(a, b)[0,1])

def partial_corr(x, y, controls):
    """Partial correlation of x and y, controlling for list of vectors `controls`."""
    x = np.array(x); y = np.array(y)
    Z = np.column_stack(controls)
    # Residualize x and y on Z
    Z_aug = np.column_stack([np.ones(len(x)), Z])
    bx, *_ = np.linalg.lstsq(Z_aug, x, rcond=None)
    by, *_ = np.linalg.lstsq(Z_aug, y, rcond=None)
    rx = x - Z_aug @ bx
    ry = y - Z_aug @ by
    return pearson(rx, ry)

# ===================================================================
# P1 — CONTROL TEST: partial correlation given GDP and M2
# ===================================================================
print("="*78)
print("P1 — CONTROL TEST: partial correlation given GDP and M2")
print("="*78)

INDICATORS = {
    "Energy CPI": ENERGY_CPI,
    "Food":       FOOD,
    "Fertiliser": FERT,
    "Real Wages": REAL_WAGES,
}

p1_results = []
print(f"\n{'Indicator':15s} {'rho_raw':>10} {'rho|GDP':>10} {'rho|M2':>10} {'rho|GDP,M2':>12}  Verdict")
print("-"*78)
for name, ind in INDICATORS.items():
    ys = common(CESI_HIST, ind, GDP_REAL, M2)
    c = [CESI_HIST[y] for y in ys]
    i = [ind[y] for y in ys]
    g = [np.log(GDP_REAL[y]) for y in ys]
    m = [np.log(M2[y])       for y in ys]
    cl = [np.log(CESI_HIST[y]) for y in ys]
    il = [np.log(ind[y])       for y in ys]
    rho_raw    = pearson(cl, il)
    rho_gdp    = partial_corr(cl, il, [g])
    rho_m2     = partial_corr(cl, il, [m])
    rho_both   = partial_corr(cl, il, [g, m])
    surviving  = abs(rho_both) > 0.30
    verdict    = "SURVIVES" if surviving else "ABSORBED"
    p1_results.append((name, rho_raw, rho_gdp, rho_m2, rho_both, verdict))
    print(f"{name:15s} {rho_raw:+10.3f} {rho_gdp:+10.3f} {rho_m2:+10.3f} {rho_both:+12.3f}  {verdict}")

# ===================================================================
# P2 — SPURIOUS CORRELATION: CESI vs should-not-correlate variables
# ===================================================================
print("\n" + "="*78)
print("P2 — SPURIOUS: CESI vs technology / development indicators")
print("="*78)

NON_INDICATORS = {
    "Internet users %":   INTERNET,
    "Urbanisation %":     URBAN,
    "Adult literacy %":   LITERACY,
}
p2_results = []
print(f"\n{'Variable':22s} {'rho_level':>10} {'rho|GDP':>10} {'rho|GDP,M2':>12}  Concern")
print("-"*78)
for name, ind in NON_INDICATORS.items():
    ys = common(CESI_HIST, ind, GDP_REAL, M2)
    cl = [np.log(CESI_HIST[y]) for y in ys]
    il = [ind[y] for y in ys]   # not log — these are %
    g  = [np.log(GDP_REAL[y]) for y in ys]
    m  = [np.log(M2[y])       for y in ys]
    rho_raw  = pearson(cl, il)
    rho_gdp  = partial_corr(cl, il, [g])
    rho_both = partial_corr(cl, il, [g, m])
    # Concern: if rho_raw is high AND rho_both still high, CESI is time proxy
    concern  = "TIME-PROXY RISK" if abs(rho_both) > 0.50 else ("residual trend" if abs(rho_both)>0.30 else "OK")
    p2_results.append((name, rho_raw, rho_gdp, rho_both, concern))
    print(f"{name:22s} {rho_raw:+10.3f} {rho_gdp:+10.3f} {rho_both:+12.3f}  {concern}")

# ===================================================================
# P3 — E-ONLY NULL MODEL
# ===================================================================
print("\n" + "="*78)
print("P3 — E-ONLY NULL: does the 4-component composite add value?")
print("="*78)

# Construct CESI_E = E/S using only energy as demand
def compute_cesi_E_only():
    # compute_cesi() returns (cesi_dict, D_dict, S_dict, eroi_path_used)
    res = compute_cesi(weights=(1.0,0.0,0.0,0.0))
    if isinstance(res, tuple):
        return res[0]
    return res

CESI_E = compute_cesi_E_only()
ys = common(CESI_HIST, CESI_E)
cesi_full = [CESI_HIST[y] for y in ys]
cesi_e_v  = [CESI_E[y]    for y in ys]

# Path correlation
rho_path = pearson(np.log(cesi_full), np.log(cesi_e_v))
# Endpoint comparison
print(f"\n  CESI_full 1980 -> 2023:  {CESI_HIST[1980]:.0f} -> {CESI_HIST[2023]:.0f}   ({CESI_HIST[2023]/CESI_HIST[1980]:.1f}x)")
print(f"  CESI_E    1980 -> 2023:  {CESI_E[1980]:.0f} -> {CESI_E[2023]:.0f}   ({CESI_E[2023]/CESI_E[1980]:.1f}x)")
print(f"  log-log path correlation:  rho = {rho_path:+.4f}")

# Test 4 results on CESI_E
print(f"\n  Real-economy correlations for CESI_E (level):")
p3_results = []
for name, ind in INDICATORS.items():
    ys2 = common(CESI_E, ind)
    rho_full = pearson([np.log(CESI_HIST[y]) for y in ys2], [np.log(ind[y]) for y in ys2])
    rho_eonly = pearson([np.log(CESI_E[y])    for y in ys2], [np.log(ind[y]) for y in ys2])
    delta = rho_eonly - rho_full
    verdict = "E-only matches" if abs(delta) < 0.05 else ("E-only WEAKER" if delta<-0.05 else "full WEAKER")
    p3_results.append((name, rho_full, rho_eonly, delta, verdict))
    print(f"    {name:15s}  full={rho_full:+.3f}  E-only={rho_eonly:+.3f}  delta={delta:+.3f}  ({verdict})")

# ===================================================================
# P4 — FALSIFICATION CONDITIONS (text statement)
# ===================================================================
print("\n" + "="*78)
print("P4 — FALSIFICATION CONDITIONS")
print("="*78)

FALSIFIERS = [
    ("F1 EROI dominance",
     "If a future period (>=10 yr) shows EROI stable or rising while CESI continues",
     "to rise materially (>20%), the 'EROI-dominance' claim is refuted."),
    ("F2 Wage causal channel",
     "If a future period (>=10 yr) shows CESI rising while detrended real wages",
     "do not fall (or rise), the only validated causal channel breaks."),
    ("F3 Real-economy linkage",
     "If a future decade shows CESI rising materially while energy/food/fertiliser",
     "indicators stay flat or fall in structural (5yr-smoothed) terms, the",
     "framework's claim of structural co-movement with real-economy stress fails."),
    ("F4 Substitution elasticity assumption",
     "If primary-energy decoupling proceeds such that GDP per unit primary energy",
     "doubles within 15 years and CESI fails to flatten or fall, the assumed",
     "limited substitution elasticity is wrong."),
]

for f in FALSIFIERS:
    print(f"\n  {f[0]}:")
    for line in f[1:]: print(f"    {line}")

# ===================================================================
# CSV
# ===================================================================
with open("cesi_R4_pressure.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["test","name","rho_raw","rho_partial_GDP","rho_partial_M2","rho_partial_both","verdict"])
    for n,r,g,m,b,v in p1_results:
        w.writerow(["P1",n,f"{r:.4f}",f"{g:.4f}",f"{m:.4f}",f"{b:.4f}",v])
    for n,r,g,b,c in p2_results:
        w.writerow(["P2",n,f"{r:.4f}",f"{g:.4f}","",f"{b:.4f}",c])
    for n,rf,re_,d,v in p3_results:
        w.writerow(["P3",n,f"{rf:.4f}",f"{re_:.4f}","",f"{d:+.4f}",v])

# ===================================================================
# DASHBOARD
# ===================================================================
fig = plt.figure(figsize=(20,11))
fig.suptitle("CESI R4 — Pressure Test  (Control / Spurious / E-only Null / Falsification)",
             fontsize=14, fontweight="bold")

# --- P1 panel ---
ax1 = plt.subplot(2,2,1)
labels  = [r[0] for r in p1_results]
raw     = [r[1] for r in p1_results]
both    = [r[4] for r in p1_results]
x = np.arange(len(labels))
ax1.bar(x-0.20, raw,  width=0.4, color="#3498db", label="raw rho")
ax1.bar(x+0.20, both, width=0.4, color="#e74c3c", label="rho | GDP, M2")
ax1.axhline(0.30, color="grey", ls="--", lw=0.8, label="0.30 survival threshold")
ax1.axhline(-0.30, color="grey", ls="--", lw=0.8)
ax1.set_xticks(x); ax1.set_xticklabels(labels, rotation=10, fontsize=9)
ax1.set_ylabel("Pearson rho (log-log)")
ax1.set_title("P1 — Does CESI survive control for GDP and M2?", fontsize=11)
ax1.legend(fontsize=9); ax1.grid(alpha=0.3, axis="y")
for i,(r,b) in enumerate(zip(raw, both)):
    ax1.text(i-0.20, r+0.02, f"{r:+.2f}", ha="center", fontsize=8)
    ax1.text(i+0.20, b+0.02 if b>=0 else b-0.06, f"{b:+.2f}", ha="center", fontsize=8)

# --- P2 panel ---
ax2 = plt.subplot(2,2,2)
labels  = [r[0] for r in p2_results]
raw     = [r[1] for r in p2_results]
both    = [r[3] for r in p2_results]
x = np.arange(len(labels))
ax2.bar(x-0.20, raw,  width=0.4, color="#3498db", label="raw rho")
ax2.bar(x+0.20, both, width=0.4, color="#e74c3c", label="rho | GDP, M2")
ax2.axhline(0.50, color="red", ls="--", lw=0.8, label="time-proxy risk if > 0.50")
ax2.set_xticks(x); ax2.set_xticklabels(labels, rotation=10, fontsize=9)
ax2.set_ylabel("Pearson rho")
ax2.set_title("P2 — Spurious correlation with non-stress variables?", fontsize=11)
ax2.legend(fontsize=9); ax2.grid(alpha=0.3, axis="y")
for i,(r,b) in enumerate(zip(raw, both)):
    ax2.text(i-0.20, r+0.02, f"{r:+.2f}", ha="center", fontsize=8)
    ax2.text(i+0.20, b+0.02 if b>=0 else b-0.06, f"{b:+.2f}", ha="center", fontsize=8)

# --- P3 panel ---
ax3 = plt.subplot(2,2,3)
ax3.plot(YEARS, [CESI_HIST[y] for y in YEARS], "k-",  lw=2.0, label=f"CESI_full (4-comp)  2023={CESI_HIST[2023]:.0f}")
ax3.plot(YEARS, [CESI_E[y]    for y in YEARS], "r--", lw=2.0, label=f"CESI_E (E/S only)    2023={CESI_E[2023]:.0f}")
ax3.set_title(f"P3 — Full vs E-only null  (path log-log rho = {rho_path:+.3f})", fontsize=11)
ax3.set_ylabel("CESI (1980=100)"); ax3.legend(fontsize=9); ax3.grid(alpha=0.3)

# Inset table for P3 indicator comparison
inset = ax3.inset_axes([0.45, 0.45, 0.50, 0.45])
inset.axis("off")
trows = [["Indicator","full rho","E-only","delta"]]
for n,rf,re_,d,v in p3_results:
    trows.append([n, f"{rf:+.2f}", f"{re_:+.2f}", f"{d:+.2f}"])
t = inset.table(cellText=trows, loc="center", cellLoc="center", colWidths=[0.34,0.20,0.22,0.22])
t.auto_set_font_size(False); t.set_fontsize(8); t.scale(1,1.2)
for j in range(4):
    t[(0,j)].set_facecolor("#404040"); t[(0,j)].set_text_props(color="white", weight="bold")

# --- P4 panel: falsification text ---
ax4 = plt.subplot(2,2,4); ax4.axis("off")
text = "P4 — EXPLICIT FALSIFICATION CONDITIONS\n\n"
for f in FALSIFIERS:
    text += f"{f[0]}\n"
    for line in f[1:]:
        text += f"  {line}\n"
    text += "\n"
ax4.text(0.02, 0.98, text, fontsize=8.5, family="monospace", va="top",
         bbox=dict(boxstyle="round,pad=0.6", facecolor="#fff8dc", edgecolor="#888"))
ax4.set_title("P4 — Disprovability statement (paper requirement)", fontsize=11, pad=20)

plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig("CESI_R4_pressure.png", dpi=140, bbox_inches="tight")
plt.savefig("CESI_R4_pressure.svg", bbox_inches="tight")

print("\nSaved: cesi_R4_pressure.csv")
print("Saved: CESI_R4_pressure.png/.svg")
print("="*78)
