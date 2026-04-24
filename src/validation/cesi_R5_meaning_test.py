"""
CESI R5 — MEANING & UNIQUENESS TEST
====================================
Final pre-writing check. Three questions:

  M1  Does CESI add signal BEYOND energy intensity (E/GDP) or
      energy per capita (E/P)?  If not, it's a reframe of E-intensity.

  M2  Is the wage channel STABLE?
      a) Sub-period split: 1980-2000 vs 2001-2023
      b) Horse race: does CESI beat simpler predictors of real wages
         (CPI inflation, US unemployment, US productivity, energy intensity)?

  M3  ONE-SENTENCE meaning of CESI (text statement, not a test).

Outputs:
  cesi_R5_meaning.csv
  CESI_R5_meaning.png/.svg
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from cesi_robustness_R1 import YEARS, E_EJ, POPULATION
from cesi_test4_realeconomy import REAL_WAGES, CESI as CESI_HIST
from cesi_R4_pressure_test import GDP_REAL, M2

# ===================================================================
# ADDITIONAL MACRO CONTROLS (1980-2023)
# ===================================================================

# US CPI all items, annual mean (FRED CPIAUCSL)
CPI_US = {
    1980:82.4,1981:90.9,1982:96.5,1983:99.6,1984:103.9,1985:107.6,1986:109.6,
    1987:113.6,1988:118.3,1989:124.0,1990:130.7,1991:136.2,1992:140.3,1993:144.5,
    1994:148.2,1995:152.4,1996:156.9,1997:160.5,1998:163.0,1999:166.6,2000:172.2,
    2001:177.1,2002:179.9,2003:184.0,2004:188.9,2005:195.3,2006:201.6,2007:207.3,
    2008:215.3,2009:214.5,2010:218.1,2011:224.9,2012:229.6,2013:233.0,2014:236.7,
    2015:237.0,2016:240.0,2017:245.1,2018:251.1,2019:255.7,2020:258.8,2021:271.0,
    2022:292.7,2023:304.7,
}

# US Unemployment rate, annual mean % (FRED UNRATE)
UNEMP_US = {
    1980:7.2,1981:7.6,1982:9.7,1983:9.6,1984:7.5,1985:7.2,1986:7.0,1987:6.2,
    1988:5.5,1989:5.3,1990:5.6,1991:6.8,1992:7.5,1993:6.9,1994:6.1,1995:5.6,
    1996:5.4,1997:4.9,1998:4.5,1999:4.2,2000:4.0,2001:4.7,2002:5.8,2003:6.0,
    2004:5.5,2005:5.1,2006:4.6,2007:4.6,2008:5.8,2009:9.3,2010:9.6,2011:8.9,
    2012:8.1,2013:7.4,2014:6.2,2015:5.3,2016:4.9,2017:4.4,2018:3.9,2019:3.7,
    2020:8.1,2021:5.4,2022:3.6,2023:3.6,
}

# US Nonfarm business labour productivity, index 2017=100 (FRED OPHNFB, annual avg)
PROD_US = {
    1980:53.2,1981:54.4,1982:54.4,1983:56.6,1984:58.0,1985:59.2,1986:61.0,
    1987:61.5,1988:62.5,1989:63.3,1990:65.0,1991:66.4,1992:69.1,1993:69.6,
    1994:70.4,1995:70.7,1996:72.7,1997:74.1,1998:76.4,1999:79.0,2000:81.3,
    2001:83.7,2002:87.0,2003:90.7,2004:93.2,2005:94.9,2006:95.7,2007:97.3,
    2008:98.0,2009:101.7,2010:104.6,2011:104.8,2012:105.7,2013:106.4,2014:107.3,
    2015:108.7,2016:108.9,2017:110.1,2018:111.5,2019:113.2,2020:117.9,2021:120.0,
    2022:118.4,2023:120.0,
}

YEARS_FULL = sorted(set(CESI_HIST)&set(REAL_WAGES)&set(GDP_REAL)&set(M2)&set(CPI_US)&set(UNEMP_US)&set(PROD_US)&set(E_EJ)&set(POPULATION))
print(f"Sample: {YEARS_FULL[0]}-{YEARS_FULL[-1]} ({len(YEARS_FULL)} years)")

# ===================================================================
# DERIVED VARIABLES
# ===================================================================
# Energy intensity (EJ per trillion 2015 USD GDP)
E_INTENSITY = {y: E_EJ[y] / GDP_REAL[y] for y in YEARS_FULL}
# Energy per capita (GJ per person)
E_PER_CAP   = {y: E_EJ[y] * 1e9 / POPULATION[y] for y in YEARS_FULL}
# US CPI inflation rate, annual %
CPI_INFL    = {y: (CPI_US[y]/CPI_US[y-1]-1)*100 for y in YEARS_FULL if y-1 in CPI_US}

def pearson(a,b): return float(np.corrcoef(a,b)[0,1])

def fit_ols(X, y):
    """Returns (betas, R2, residual_std)"""
    X = np.column_stack([np.ones(len(y))] + X)
    y = np.array(y)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ b
    ss_res = np.sum((y-yhat)**2); ss_tot = np.sum((y-y.mean())**2)
    r2 = 1 - ss_res/ss_tot
    return b, r2, float(np.std(y-yhat))

# ===================================================================
# M1 — CESI vs ENERGY INTENSITY / PER CAPITA
# ===================================================================
print("\n" + "="*78)
print("M1 — Does CESI add signal beyond E-intensity / E-per-capita?")
print("="*78)

# Path correlations
c_log     = [np.log(CESI_HIST[y]) for y in YEARS_FULL]
ei_log    = [np.log(E_INTENSITY[y]) for y in YEARS_FULL]
epc_log   = [np.log(E_PER_CAP[y])   for y in YEARS_FULL]
e_log     = [np.log(E_EJ[y])         for y in YEARS_FULL]

print(f"\n  Path correlations (log levels):")
print(f"    rho(CESI, E)             = {pearson(c_log, e_log):+.3f}")
print(f"    rho(CESI, E_per_capita)  = {pearson(c_log, epc_log):+.3f}")
print(f"    rho(CESI, E_intensity)   = {pearson(c_log, ei_log):+.3f}")

# Regression of real wages on each predictor alone, then add CESI
w_log = [np.log(REAL_WAGES[y]) for y in YEARS_FULL]

m1_results = []
for name, x in [("E only", e_log), ("E_per_capita", epc_log), ("E_intensity", ei_log)]:
    _, r2_alone, _ = fit_ols([x], w_log)
    _, r2_with,  _ = fit_ols([x, c_log], w_log)
    delta = r2_with - r2_alone
    verdict = "CESI ADDS" if delta > 0.05 else "CESI redundant"
    m1_results.append((name, r2_alone, r2_with, delta, verdict))
    print(f"\n  Predict log(real wages) from {name}:")
    print(f"    R^2 alone           = {r2_alone:.3f}")
    print(f"    R^2 + log(CESI)     = {r2_with:.3f}")
    print(f"    Delta R^2           = {delta:+.3f}  ({verdict})")

# Reverse: does E-intensity ADD beyond CESI?
print(f"\n  Predict log(real wages) from CESI:")
_, r2_cesi_alone, _ = fit_ols([c_log], w_log)
print(f"    R^2 alone           = {r2_cesi_alone:.3f}")
for name, x in [("+ E_intensity", ei_log), ("+ E_per_capita", epc_log)]:
    _, r2_with, _ = fit_ols([c_log, x], w_log)
    delta = r2_with - r2_cesi_alone
    print(f"    R^2 {name:18s} = {r2_with:.3f}   delta = {delta:+.3f}")

# ===================================================================
# M2 — WAGE CHANNEL STABILITY
# ===================================================================
print("\n" + "="*78)
print("M2 — Is the CESI->wage channel stable across sub-periods?")
print("="*78)

# Use detrended-residual partial correlation, period-split
def partial_corr(x, y, controls):
    x = np.array(x); y = np.array(y)
    Z = np.column_stack([np.ones(len(x))] + [np.array(c) for c in controls])
    bx, *_ = np.linalg.lstsq(Z, x, rcond=None)
    by, *_ = np.linalg.lstsq(Z, y, rcond=None)
    return pearson(x - Z@bx, y - Z@by)

# Build full panels
def panel(years):
    c   = [np.log(CESI_HIST[y]) for y in years]
    w   = [np.log(REAL_WAGES[y]) for y in years]
    g   = [np.log(GDP_REAL[y]) for y in years]
    m   = [np.log(M2[y])       for y in years]
    return c, w, g, m

m2_subperiod = []
for label, yrs in [("Full 1980-2023", YEARS_FULL),
                   ("Early 1980-2000", [y for y in YEARS_FULL if y<=2000]),
                   ("Late 2001-2023",  [y for y in YEARS_FULL if y>=2001])]:
    c, w, g, m = panel(yrs)
    rho_raw   = pearson(c, w)
    rho_part  = partial_corr(c, w, [g, m])
    # Diff-on-diff
    cd = np.diff(c); wd = np.diff(w)
    rho_diff = pearson(cd, wd)
    m2_subperiod.append((label, len(yrs), rho_raw, rho_part, rho_diff))
    print(f"\n  {label}  (n={len(yrs)}):")
    print(f"    rho(CESI, wages) raw           = {rho_raw:+.3f}")
    print(f"    rho(CESI, wages) | GDP, M2     = {rho_part:+.3f}")
    print(f"    rho(d.CESI, d.wages)           = {rho_diff:+.3f}")

# Horse race: predict log(wages) from CESI vs simpler macro
print("\n" + "="*78)
print("M2b — Horse race for predicting real wages (full sample R^2)")
print("="*78)
w = [np.log(REAL_WAGES[y]) for y in YEARS_FULL]
predictors = {
    "CESI":           [np.log(CESI_HIST[y]) for y in YEARS_FULL],
    "log GDP":        [np.log(GDP_REAL[y]) for y in YEARS_FULL],
    "log M2":         [np.log(M2[y])       for y in YEARS_FULL],
    "log Productivity": [np.log(PROD_US[y]) for y in YEARS_FULL],
    "Unemployment":   [UNEMP_US[y]          for y in YEARS_FULL],
    "log E_intensity":[np.log(E_INTENSITY[y]) for y in YEARS_FULL],
}
m2b_results = []
print(f"\n  {'Predictor':22s}  {'R^2 alone':>12}  {'R^2 +CESI':>12}  delta")
print("  " + "-"*60)
for name, x in predictors.items():
    _, r2_alone, _ = fit_ols([x], w)
    if name == "CESI":
        r2_with = r2_alone; delta = 0.0
    else:
        _, r2_with, _ = fit_ols([x, predictors["CESI"]], w)
        delta = r2_with - r2_alone
    m2b_results.append((name, r2_alone, r2_with, delta))
    print(f"  {name:22s}  {r2_alone:12.3f}  {r2_with:12.3f}  {delta:+.3f}")

# Does CESI win head-to-head?
print(f"\n  Best single predictor:  ", max(m2b_results, key=lambda r: r[1])[0],
      f"(R^2 = {max(m2b_results, key=lambda r: r[1])[1]:.3f})")

# ===================================================================
# M3 — One-sentence meaning (text-only)
# ===================================================================
M3_TEXT = """
M3 — ONE-SENTENCE MEANING OF CESI (post-pressure-test)

Candidate definitions, ranked by defensibility given R1-R5 evidence:

  V1 (NARROWEST, MOST DEFENSIBLE):
     "CESI measures the ratio of primary energy demand to a thermodynamic
      supply capacity built from reserves-to-production years and energy
      return on energy invested, normalised to a base year."

  V2 (ECONOMIC INTERPRETATION, REQUIRES ARGUMENT):
     "CESI measures the gap between civilisational energy demand and the
      surplus energy available after extraction costs, expressed as an
      index of structural pressure on real economic outcomes."

  V3 (MAXIMAL CLAIM, RISKY):
     "CESI measures the thermodynamic constraint envelope within which
      industrial economies operate, with rising values indicating
      diminishing surplus energy per unit of system demand."

RECOMMENDED HEADLINE FOR PAPER:
    A thermodynamically-derived ratio of energy demand to extraction-
    adjusted supply capacity, whose dynamics are dominated by EROI
    decline and which uniquely tracks real-wage compression after
    controlling for growth and money supply.
"""
print(M3_TEXT)

# ===================================================================
# CSV
# ===================================================================
with open("cesi_R5_meaning.csv","w",newline="") as f:
    w_csv = csv.writer(f)
    w_csv.writerow(["test","row","r2_alone","r2_with_cesi","delta","verdict_or_value"])
    for name, r1, r2, d, v in m1_results:
        w_csv.writerow(["M1", name, f"{r1:.4f}", f"{r2:.4f}", f"{d:+.4f}", v])
    for label, n, raw, part, diff in m2_subperiod:
        w_csv.writerow(["M2-period", f"{label} (n={n})", "", "", "",
                        f"raw={raw:.3f}, partial={part:.3f}, diff={diff:.3f}"])
    for name, ra, rw, d in m2b_results:
        w_csv.writerow(["M2b-horse", name, f"{ra:.4f}", f"{rw:.4f}", f"{d:+.4f}", ""])

# ===================================================================
# DASHBOARD
# ===================================================================
fig = plt.figure(figsize=(20,11))
fig.suptitle("CESI R5 — Meaning & Uniqueness Test  (E-intensity / Wage stability / Horse race)",
             fontsize=14, fontweight="bold")

# --- Panel 1: M1 incremental R^2 ---
ax1 = plt.subplot(2,2,1)
labels = [r[0] for r in m1_results]
r2_a   = [r[1] for r in m1_results]
r2_w   = [r[2] for r in m1_results]
x = np.arange(len(labels))
ax1.bar(x-0.20, r2_a, width=0.4, color="#3498db", label="R^2 (predictor alone)")
ax1.bar(x+0.20, r2_w, width=0.4, color="#e74c3c", label="R^2 (predictor + CESI)")
ax1.set_xticks(x); ax1.set_xticklabels(labels, fontsize=10)
ax1.set_ylabel("R^2 for log(real wages)")
ax1.set_title("M1 — Does CESI add R^2 beyond simpler energy variables?", fontsize=11)
ax1.legend(fontsize=9); ax1.grid(alpha=0.3, axis="y")
for i,(a,wv) in enumerate(zip(r2_a, r2_w)):
    ax1.text(i-0.20, a+0.015, f"{a:.2f}", ha="center", fontsize=9)
    ax1.text(i+0.20, wv+0.015, f"{wv:.2f}", ha="center", fontsize=9)
    d = wv-a
    ax1.text(i, max(a,wv)+0.05, f"d={d:+.2f}", ha="center", fontsize=9, weight="bold",
             color="green" if d>0.05 else "grey")

# --- Panel 2: M2 sub-period stability ---
ax2 = plt.subplot(2,2,2)
labels = [r[0].replace(" 19","\n19").replace(" 20","\n20") for r in m2_subperiod]
raw  = [r[2] for r in m2_subperiod]
part = [r[3] for r in m2_subperiod]
diff = [r[4] for r in m2_subperiod]
x = np.arange(len(labels))
ax2.bar(x-0.25, raw,  width=0.25, color="#3498db", label="raw rho")
ax2.bar(x,      part, width=0.25, color="#e74c3c", label="rho|GDP,M2")
ax2.bar(x+0.25, diff, width=0.25, color="#2ecc71", label="diff-on-diff rho")
ax2.set_xticks(x); ax2.set_xticklabels(labels, fontsize=9)
ax2.set_ylabel("Pearson rho (CESI vs Real Wages)")
ax2.set_title("M2 — Wage channel: stable across sub-periods?", fontsize=11)
ax2.axhline(0, color="black", lw=0.6)
ax2.legend(fontsize=9); ax2.grid(alpha=0.3, axis="y")

# --- Panel 3: M2b horse race ---
ax3 = plt.subplot(2,2,3)
labels = [r[0] for r in m2b_results]
r2_a   = [r[1] for r in m2b_results]
r2_w   = [r[2] for r in m2b_results]
x = np.arange(len(labels))
ax3.bar(x-0.20, r2_a, width=0.4, color="#3498db", label="alone")
ax3.bar(x+0.20, r2_w, width=0.4, color="#e74c3c", label="+ CESI")
ax3.set_xticks(x); ax3.set_xticklabels(labels, rotation=20, ha="right", fontsize=9)
ax3.set_ylabel("R^2 for log(real wages)")
ax3.set_title("M2b — Horse race: best single predictor of real wages", fontsize=11)
ax3.legend(fontsize=9); ax3.grid(alpha=0.3, axis="y")
for i,(a,wv) in enumerate(zip(r2_a, r2_w)):
    ax3.text(i-0.20, a+0.015, f"{a:.2f}", ha="center", fontsize=8)
    ax3.text(i+0.20, wv+0.015, f"{wv:.2f}", ha="center", fontsize=8)

# --- Panel 4: M3 text ---
ax4 = plt.subplot(2,2,4); ax4.axis("off")
ax4.text(0.02, 0.98, M3_TEXT.strip(), fontsize=8.5, family="monospace", va="top",
         bbox=dict(boxstyle="round,pad=0.6", facecolor="#fff8dc", edgecolor="#888"))
ax4.set_title("M3 — One-sentence meaning of CESI (write before publishing)", fontsize=11, pad=20)

plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig("CESI_R5_meaning.png", dpi=140, bbox_inches="tight")
plt.savefig("CESI_R5_meaning.svg", bbox_inches="tight")

print("\nSaved: cesi_R5_meaning.csv, CESI_R5_meaning.png/.svg")
print("="*78)
