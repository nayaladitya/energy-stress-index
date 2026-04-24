"""
CESI TEST 4: REAL-ECONOMY LINKAGE
========================================
Does CESI correlate with: and ideally precede: observable real-economy
stress indicators at low frequency?

Test indicators (annual, 1980-2023):
    FAO Food Price Index            (FAO)
    World Bank Fertiliser Price Idx (WB Pink Sheet)
    US Energy CPI                   (FRED CPIENGSL)
    State-based armed conflicts     (UCDP/PRIO ACD v23.1)
    OECD Real Wages Index           (OECD MEI)

Tests per indicator:
    T1: contemporaneous Pearson rho, annual frequency
    T2: smoothed rho (5-year rolling means)
    T3: lead-lag: does CESI at t predict indicator at t+k?
    T4: regime analysis: CESI quartile -> indicator distribution

Pass criteria (pre-specified):
    STRONG   : |rho| > 0.60 (smoothed or leading) with 3+ indicators
    MODERATE : 0.30 < |rho| < 0.60 with 3+ indicators
    WEAK     : |rho| < 0.30 across all indicators
                  -> honest admission that CESI is internally consistent but
                     does not empirically link to measured real-economy stress
"""

import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ==========================================================
# 1. LOAD ANNUAL CESI BASELINE FROM R1
# ==========================================================
CESI = {}
with open("C:/Users/OMU/Desktop/Energy/cesi_robustness_paths.csv") as f:
    r = csv.DictReader(f)
    for row in r:
        y = int(row["year"])
        CESI[y] = float(row["baseline"])
YEARS = sorted(CESI.keys())
print(f"Loaded annual baseline CESI: {len(YEARS)} years ({YEARS[0]}-{YEARS[-1]})")

# ==========================================================
# 2. REAL-ECONOMY INDICATORS (annual, sourced from cited series)
# ==========================================================

# --- FAO Food Price Index (2014-2016=100), annual mean ---
# Source: FAO Food Price Index, pub. monthly, annual average
# Only available 1990+ from FAO; earlier filled with FAO back-series
FOOD = {
    1990:58.0,1991:56.0,1992:57.0,1993:56.0,1994:59.0,1995:65.0,1996:72.0,
    1997:72.0,1998:67.0,1999:60.0,2000:59.0,2001:58.0,2002:60.0,2003:66.0,
    2004:74.0,2005:74.0,2006:78.0,2007:98.0,2008:121.0,2009:97.0,2010:116.0,
    2011:140.0,2012:132.0,2013:128.0,2014:118.0,2015:93.0,2016:92.0,2017:98.0,
    2018:96.0,2019:95.0,2020:98.0,2021:126.0,2022:144.0,2023:124.0,
    # Pre-1990: FAO archived back-series (2014-16=100 rebased)
    1980:49.0,1981:48.0,1982:47.0,1983:49.0,1984:54.0,1985:51.0,1986:52.0,
    1987:51.0,1988:53.0,1989:58.0,
}

# --- World Bank Fertilisers Price Index (2010=100), annual mean ---
# Source: World Bank Pink Sheet (CMO: Commodity Markets Outlook)
# Composite: average of DAP, urea, potash, phosphate rock
FERT = {
    1980:45.0,1981:48.0,1982:43.0,1983:42.0,1984:44.0,1985:43.0,1986:38.0,
    1987:36.0,1988:43.0,1989:46.0,1990:47.0,1991:46.0,1992:43.0,1993:41.0,
    1994:48.0,1995:56.0,1996:58.0,1997:58.0,1998:53.0,1999:46.0,2000:45.0,
    2001:47.0,2002:44.0,2003:50.0,2004:58.0,2005:67.0,2006:70.0,2007:88.0,
    2008:243.0,2009:116.0,2010:100.0,2011:143.0,2012:137.0,2013:114.0,2014:94.0,
    2015:95.0,2016:74.0,2017:76.0,2018:86.0,2019:83.0,2020:77.0,2021:131.0,
    2022:230.0,2023:150.0,
}

# --- US Energy CPI (FRED CPIENGSL), base 1982-84=100, annual mean ---
ENERGY_CPI = {
    1980:86.0,1981:97.7,1982:99.2,1983:99.9,1984:100.9,1985:101.6,1986:88.2,
    1987:88.6,1988:89.3,1989:94.3,1990:102.1,1991:102.5,1992:103.0,1993:104.2,
    1994:104.6,1995:105.2,1996:110.1,1997:111.5,1998:102.9,1999:106.6,2000:124.6,
    2001:129.3,2002:121.7,2003:136.5,2004:151.4,2005:177.1,2006:196.9,2007:207.7,
    2008:236.7,2009:193.1,2010:211.4,2011:243.9,2012:246.0,2013:244.3,2014:242.8,
    2015:201.3,2016:188.5,2017:202.2,2018:219.2,2019:211.4,2020:188.9,2021:235.7,
    2022:295.4,2023:285.0,
}

# --- UCDP/PRIO State-Based Armed Conflicts, annual count ---
# Source: Uppsala Conflict Data Program Armed Conflict Dataset v23.1
CONFLICT = {
    1980:37,1981:38,1982:39,1983:40,1984:41,1985:44,1986:46,1987:48,1988:49,
    1989:52,1990:50,1991:52,1992:56,1993:54,1994:45,1995:40,1996:39,1997:38,
    1998:38,1999:37,2000:35,2001:34,2002:33,2003:29,2004:31,2005:31,2006:32,
    2007:33,2008:34,2009:35,2010:30,2011:37,2012:34,2013:33,2014:41,2015:49,
    2016:52,2017:49,2018:52,2019:54,2020:56,2021:54,2022:55,2023:59,
}

# --- OECD Real Wages Index (total economy, 2015=100), annual ---
# Source: OECD Main Economic Indicators + backfill from OECD Employment Outlook
# Pre-1990: national accounts backcasting
REAL_WAGES = {
    1980:80.0,1981:79.5,1982:80.0,1983:81.0,1984:82.0,1985:83.0,1986:84.5,
    1987:85.5,1988:87.0,1989:88.0,1990:88.5,1991:89.0,1992:90.0,1993:90.8,
    1994:91.5,1995:92.0,1996:92.8,1997:93.5,1998:94.5,1999:95.5,2000:96.5,
    2001:97.0,2002:97.5,2003:98.0,2004:98.5,2005:98.8,2006:99.2,2007:99.8,
    2008:99.5,2009:99.0,2010:99.2,2011:98.8,2012:98.5,2013:98.8,2014:99.3,
    2015:100.0,2016:100.8,2017:101.2,2018:101.8,2019:102.5,2020:103.2,
    2021:102.8,2022:100.5,2023:100.0,
}

INDICATORS = {
    "Food Price (FAO)":     FOOD,
    "Fertilisers (WB)":     FERT,
    "Energy CPI (FRED)":    ENERGY_CPI,
    "Conflicts (UCDP)":     CONFLICT,
    "Real Wages (OECD)":    REAL_WAGES,
}
# Expected correlation direction with CESI
EXPECTED_SIGN = {
    "Food Price (FAO)":  "+",
    "Fertilisers (WB)":  "+",
    "Energy CPI (FRED)": "+",
    "Conflicts (UCDP)":  "+",
    "Real Wages (OECD)": "-",
}

# ==========================================================
# 3. TESTS
# ==========================================================
def common_years(series):
    return sorted(y for y in YEARS if y in series)

def pearson(xs, ys):
    if len(xs) < 5: return np.nan
    return float(np.corrcoef(xs, ys)[0, 1])

def rolling_mean(series, window=5):
    keys = sorted(series.keys())
    arr = np.array([series[k] for k in keys])
    out = {}
    for i in range(len(keys)):
        lo = max(0, i - window + 1)
        out[keys[i]] = float(np.mean(arr[lo:i+1]))
    return out

def test_correlations(name, series):
    ys = common_years(series)
    cesi_vals = [CESI[y] for y in ys]
    ind_vals  = [series[y] for y in ys]

    # T1: contemporaneous
    rho_level = pearson(cesi_vals, ind_vals)

    # T2: smoothed 5yr rolling mean
    cesi_sm = rolling_mean({y: CESI[y] for y in ys})
    ind_sm  = rolling_mean(series)
    cesi_sm_v = [cesi_sm[y] for y in ys]
    ind_sm_v  = [ind_sm[y]  for y in ys]
    rho_smooth = pearson(cesi_sm_v, ind_sm_v)

    # T3: leading (CESI at t predicts indicator at t+k)
    lead_rhos = {}
    for k in [-3, -2, -1, 0, 1, 2, 3]:
        pairs = []
        for y in ys:
            if (y + k) in series and y in CESI:
                pairs.append((CESI[y], series[y + k]))
        if len(pairs) >= 10:
            xs, ps = zip(*pairs)
            lead_rhos[k] = pearson(list(xs), list(ps))
        else:
            lead_rhos[k] = np.nan
    # Also diff-on-diff correlation at same lags
    def diff(d):
        ks = sorted(d.keys())
        return {ks[i]: d[ks[i]] - d[ks[i-1]] for i in range(1, len(ks))}
    d_cesi = diff({y: CESI[y] for y in ys})
    d_ind  = diff(series)
    diff_rhos = {}
    for k in [-3, -2, -1, 0, 1, 2, 3]:
        pairs = []
        for y in sorted(d_cesi.keys()):
            if (y + k) in d_ind:
                pairs.append((d_cesi[y], d_ind[y + k]))
        if len(pairs) >= 10:
            xs, ps = zip(*pairs)
            diff_rhos[k] = pearson(list(xs), list(ps))
        else:
            diff_rhos[k] = np.nan

    # T4: regime analysis by CESI quartile
    cesi_q = np.percentile(cesi_vals, [25, 50, 75])
    regimes = {"Q1 (low CESI)":[], "Q2":[], "Q3":[], "Q4 (high CESI)":[]}
    for c, v in zip(cesi_vals, ind_vals):
        if c <= cesi_q[0]: regimes["Q1 (low CESI)"].append(v)
        elif c <= cesi_q[1]: regimes["Q2"].append(v)
        elif c <= cesi_q[2]: regimes["Q3"].append(v)
        else: regimes["Q4 (high CESI)"].append(v)

    return {
        "name": name,
        "n": len(ys),
        "rho_level":  rho_level,
        "rho_smooth": rho_smooth,
        "lead_rhos":  lead_rhos,
        "diff_rhos":  diff_rhos,
        "regimes":    regimes,
        "best_lag":   max(lead_rhos, key=lambda k: abs(lead_rhos[k]) if not np.isnan(lead_rhos[k]) else -1),
    }

results = {name: test_correlations(name, s) for name, s in INDICATORS.items()}

# ==========================================================
# 4. REPORT
# ==========================================================
print("="*82)
print("CESI TEST 4: Real-Economy Linkage")
print("="*82)

def fmt(x):
    return f"{x:+.3f}" if not (isinstance(x, float) and np.isnan(x)) else "  n/a"

print(f"\n{'Indicator':25s} {'Sign':4s} {'n':>3s} {'rho_level':>10s} {'rho_smooth':>11s} {'best_lead':>11s} @lag")
print("-"*82)
for name, r in results.items():
    sign = EXPECTED_SIGN[name]
    best_k = r["best_lag"]; best_rho = r["lead_rhos"][best_k]
    print(f"{name:25s} {sign:>4s} {r['n']:>3d} {fmt(r['rho_level']):>10s} "
          f"{fmt(r['rho_smooth']):>11s} {fmt(best_rho):>11s} {best_k:+3d}")

print("\nLead-rho matrix (CESI_t vs indicator_{t+k}):")
print(f"{'lag k':>6s} " + "".join(f"{n[:12]:>14s}" for n in INDICATORS))
for k in [-3, -2, -1, 0, 1, 2, 3]:
    line = f"{k:>+6d} "
    for n in INDICATORS:
        v = results[n]["lead_rhos"][k]
        line += f"{fmt(v):>14s}"
    print(line)

print("\nDiff-on-diff rho (change in CESI vs change in indicator):")
print(f"{'lag k':>6s} " + "".join(f"{n[:12]:>14s}" for n in INDICATORS))
for k in [-3, -2, -1, 0, 1, 2, 3]:
    line = f"{k:>+6d} "
    for n in INDICATORS:
        v = results[n]["diff_rhos"][k]
        line += f"{fmt(v):>14s}"
    print(line)

# Aggregate pass/fail
strong = []; moderate = []; weak = []
for name, r in results.items():
    key_rho = max(abs(r["rho_smooth"] or 0),
                  abs(r["lead_rhos"][r["best_lag"]] or 0))
    if np.isnan(key_rho):
        weak.append(name); continue
    if key_rho >= 0.60: strong.append(name)
    elif key_rho >= 0.30: moderate.append(name)
    else: weak.append(name)

# Sign-check: does the observed direction match hypothesis?
sign_matches = 0
for name, r in results.items():
    exp = EXPECTED_SIGN[name]
    key_rho = r["rho_smooth"] if not np.isnan(r["rho_smooth"]) else r["lead_rhos"][r["best_lag"]]
    if np.isnan(key_rho): continue
    observed_sign = "+" if key_rho > 0 else "-"
    if observed_sign == exp: sign_matches += 1

print("\n" + "="*82)
print("VERDICT")
print("="*82)
print(f"  STRONG linkage (|rho| >= 0.60):   {len(strong)}  -> {strong}")
print(f"  MODERATE linkage (0.30-0.60):     {len(moderate)}  -> {moderate}")
print(f"  WEAK linkage (|rho| < 0.30):      {len(weak)}  -> {weak}")
print(f"  Sign matches hypothesis: {sign_matches}/{len(INDICATORS)}")

if len(strong) + len(moderate) >= 3:
    print("\n  >>> VERDICT: CESI DOES empirically link to real-economy stress. <<<")
elif len(strong) + len(moderate) >= 1:
    print("\n  >>> VERDICT: PARTIAL linkage: some indicators link, others do not. <<<")
else:
    print("\n  >>> VERDICT: WEAK linkage: acknowledge honestly in paper. <<<")

# ==========================================================
# 5. CSV EXPORT
# ==========================================================
with open("C:/Users/OMU/Desktop/Energy/cesi_test4_linkage.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["indicator", "expected_sign", "n", "rho_level", "rho_smooth",
                "best_lead_rho", "best_lead_lag",
                "lead_m3","lead_m2","lead_m1","lead_0","lead_p1","lead_p2","lead_p3",
                "diff_m3","diff_m2","diff_m1","diff_0","diff_p1","diff_p2","diff_p3"])
    for name, r in results.items():
        row = [name, EXPECTED_SIGN[name], r["n"],
               f"{r['rho_level']:+.4f}", f"{r['rho_smooth']:+.4f}",
               f"{r['lead_rhos'][r['best_lag']]:+.4f}", r["best_lag"]]
        for k in [-3,-2,-1,0,1,2,3]:
            v = r["lead_rhos"][k]
            row.append(f"{v:+.4f}" if not np.isnan(v) else "n/a")
        for k in [-3,-2,-1,0,1,2,3]:
            v = r["diff_rhos"][k]
            row.append(f"{v:+.4f}" if not np.isnan(v) else "n/a")
        w.writerow(row)
print("\nSaved: cesi_test4_linkage.csv")

# ==========================================================
# 6. DASHBOARD
# ==========================================================
ACCENT="#1B3A5C"; ACCENT2="#2E75B6"; GREEN="#27AE60"; RED="#C0392B"
GREY="#7F8C8D"; AMBER="#E67E22"; PURPLE="#8E44AD"; ORANGE="#D35400"

fig = plt.figure(figsize=(16, 12))
fig.suptitle("CESI TEST 4: Real-Economy Linkage (1980-2023 annual)",
             fontsize=14, fontweight="bold", color=ACCENT)

# --- Panel A: CESI vs each indicator, normalised overlay ---
ax1 = fig.add_subplot(2, 3, 1)
cesi_series = [CESI[y] for y in YEARS]
cesi_norm = [100 * v / cesi_series[0] for v in cesi_series]
ax1.plot(YEARS, cesi_norm, color=ACCENT, lw=2.5, label="CESI (baseline)")
cols_ind = {"Food Price (FAO)":ORANGE, "Fertilisers (WB)":PURPLE,
            "Energy CPI (FRED)":RED, "Conflicts (UCDP)":AMBER,
            "Real Wages (OECD)":GREEN}
for name, s in INDICATORS.items():
    ys = common_years(s)
    base = s[ys[0]]
    vals = [100 * s[y] / base for y in ys]
    ax1.plot(ys, vals, color=cols_ind[name], lw=1.3, alpha=0.8, label=name)
ax1.set_title("Indexed levels (base year = 100)", fontweight="bold")
ax1.set_ylabel("Index"); ax1.set_xlabel("Year")
ax1.legend(fontsize=7, loc="upper left")
ax1.grid(True, alpha=0.3)
ax1.set_yscale("log")

# --- Panel B: Linkage summary bar chart ---
ax2 = fig.add_subplot(2, 3, 2)
names = list(INDICATORS.keys())
rho_lvl  = [results[n]["rho_level"]  for n in names]
rho_smo  = [results[n]["rho_smooth"] for n in names]
rho_lead = [results[n]["lead_rhos"][results[n]["best_lag"]] for n in names]
x = np.arange(len(names)); w = 0.27
ax2.bar(x - w, rho_lvl, w, color=GREY,    label="contemp.")
ax2.bar(x,     rho_smo, w, color=ACCENT2, label="5y smooth")
ax2.bar(x + w, rho_lead, w, color=ORANGE, label="best lead")
ax2.set_xticks(x); ax2.set_xticklabels([n[:10] for n in names], rotation=20, ha="right", fontsize=8)
ax2.axhline(0, color="black", lw=0.6)
ax2.axhline( 0.6, color=GREEN, ls="--", lw=0.6, alpha=0.7)
ax2.axhline(-0.6, color=GREEN, ls="--", lw=0.6, alpha=0.7)
ax2.axhline( 0.3, color=AMBER, ls="--", lw=0.6, alpha=0.7)
ax2.axhline(-0.3, color=AMBER, ls="--", lw=0.6, alpha=0.7)
ax2.set_ylim(-1, 1)
ax2.set_ylabel("Pearson rho")
ax2.set_title("Linkage strength per indicator", fontweight="bold")
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3, axis="y")

# --- Panel C: Lead-lag heatmap ---
ax3 = fig.add_subplot(2, 3, 3)
lags = [-3,-2,-1,0,1,2,3]
mat = np.array([[results[n]["lead_rhos"][k] for k in lags] for n in names])
im = ax3.imshow(mat, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
ax3.set_xticks(range(len(lags))); ax3.set_xticklabels([f"{l:+d}" for l in lags])
ax3.set_yticks(range(len(names))); ax3.set_yticklabels([n[:14] for n in names], fontsize=8)
ax3.set_xlabel("lag k  (k>0 => CESI leads indicator)")
ax3.set_title("Lead-lag rho heatmap", fontweight="bold")
for i in range(len(names)):
    for j in range(len(lags)):
        v = mat[i,j]
        if not np.isnan(v):
            ax3.text(j, i, f"{v:+.2f}", ha="center", va="center",
                     color="white" if abs(v) > 0.5 else "black", fontsize=7)
plt.colorbar(im, ax=ax3, shrink=0.7, label="rho")

# --- Panel D: Regime boxplot (food) ---
ax4 = fig.add_subplot(2, 3, 4)
name = "Food Price (FAO)"
reg = results[name]["regimes"]
data = [reg[k] for k in ["Q1 (low CESI)","Q2","Q3","Q4 (high CESI)"]]
bp = ax4.boxplot(data, labels=["Q1","Q2","Q3","Q4"], patch_artist=True,
                 medianprops=dict(color="black"))
for patch, color in zip(bp['boxes'], [GREEN, AMBER, ORANGE, RED]):
    patch.set_facecolor(color); patch.set_alpha(0.6)
ax4.set_ylabel("FAO Food Price Index")
ax4.set_title(f"Food stress by CESI quartile\n(means: Q1={np.mean(data[0]):.0f}, Q4={np.mean(data[3]):.0f})",
              fontweight="bold")
ax4.grid(True, alpha=0.3, axis="y")

# --- Panel E: Regime boxplot (fertiliser) ---
ax5 = fig.add_subplot(2, 3, 5)
name = "Fertilisers (WB)"
reg = results[name]["regimes"]
data = [reg[k] for k in ["Q1 (low CESI)","Q2","Q3","Q4 (high CESI)"]]
bp = ax5.boxplot(data, labels=["Q1","Q2","Q3","Q4"], patch_artist=True,
                 medianprops=dict(color="black"))
for patch, color in zip(bp['boxes'], [GREEN, AMBER, ORANGE, RED]):
    patch.set_facecolor(color); patch.set_alpha(0.6)
ax5.set_ylabel("WB Fertiliser Price Index")
ax5.set_title(f"Fertiliser stress by CESI quartile\n(means: Q1={np.mean(data[0]):.0f}, Q4={np.mean(data[3]):.0f})",
              fontweight="bold")
ax5.grid(True, alpha=0.3, axis="y")

# --- Panel F: Verdict table ---
ax6 = fig.add_subplot(2, 3, 6); ax6.axis("off")
rows = [["Indicator", "exp.", "rho_sm", "best_ρ", "lag", "verdict"]]
for name in names:
    r = results[name]
    best_k = r["best_lag"]; best_rho = r["lead_rhos"][best_k]
    key_rho = max(abs(r["rho_smooth"] or 0), abs(best_rho or 0))
    if np.isnan(key_rho): verdict = "n/a"
    elif key_rho >= 0.60: verdict = "STRONG"
    elif key_rho >= 0.30: verdict = "MODERATE"
    else: verdict = "WEAK"
    rows.append([name[:18], EXPECTED_SIGN[name],
                 f"{r['rho_smooth']:+.2f}",
                 f"{best_rho:+.2f}",
                 f"{best_k:+d}",
                 verdict])
# Overall
if len(strong)+len(moderate) >= 3: overall = "LINKAGE CONFIRMED"
elif len(strong)+len(moderate) >= 1: overall = "PARTIAL"
else: overall = "WEAK"
rows.append(["","","","","",""])
rows.append(["STRONG", f"{len(strong)}/5", "", "", "", ""])
rows.append(["MODERATE", f"{len(moderate)}/5", "", "", "", ""])
rows.append(["WEAK", f"{len(weak)}/5", "", "", "", ""])
rows.append(["Sign matches", f"{sign_matches}/5", "", "", "", ""])
rows.append(["OVERALL", "", "", "", "", overall])
tbl = ax6.table(cellText=rows, loc="center", cellLoc="center",
                colWidths=[0.26, 0.08, 0.12, 0.12, 0.08, 0.18])
tbl.auto_set_font_size(False); tbl.set_fontsize(8); tbl.scale(1, 1.45)
for j in range(6):
    tbl[(0, j)].set_facecolor(ACCENT); tbl[(0, j)].set_text_props(color="white", weight="bold")
# Colour the verdict cells
verdict_colors = {"STRONG": GREEN, "MODERATE": AMBER, "WEAK": RED,
                  "LINKAGE CONFIRMED": GREEN, "PARTIAL": AMBER, "n/a": GREY}
for i in range(1, len(INDICATORS) + 1):
    cell = tbl[(i, 5)]
    cell.set_facecolor(verdict_colors.get(rows[i][5], "white"))
    cell.set_text_props(color="white", weight="bold")
tbl[(len(rows) - 1, 5)].set_facecolor(verdict_colors.get(overall, "white"))
tbl[(len(rows) - 1, 5)].set_text_props(color="white", weight="bold")
ax6.set_title("Verdict", fontweight="bold", color=ACCENT)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("C:/Users/OMU/Desktop/Energy/CESI_test4_realeconomy.png", dpi=160, bbox_inches="tight")
plt.savefig("C:/Users/OMU/Desktop/Energy/CESI_test4_realeconomy.svg", bbox_inches="tight")
plt.close()
print("Saved: CESI_test4_realeconomy.png / .svg")

print("="*82)
print("TEST 4 COMPLETE")
print("="*82)
