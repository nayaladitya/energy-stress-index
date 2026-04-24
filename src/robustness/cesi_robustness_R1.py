"""
CESI ROBUSTNESS SUITE: R1: PARAMETER SENSITIVITY
===================================================
One-at-a-time (OAT) sensitivity of CESI(1980-2023) to the five parameter axes:

  AXIS 1: demand weights (wE, wX, wI, wP)            ~30 runs
  AXIS 2: OPEC haircut  (0% .. 40%)                   9 runs
  AXIS 3: EROI path     (-20%..+20% endpoints, +PCHIP)  7 runs
  AXIS 4: thresholds    (R/P_crit, EROI_crit)          25 runs
  AXIS 5: base year     (1980, 1990, 2000)             3 runs
  Plus multi-axis stress combinations                   5 runs

Per run we compute CESI(t) with full 4-component demand composite
(D = wE*E + wX*X + wI*I + wP*P at annual frequency) using the same
underlying series from energy_graph.py (E, X, I, P) and cesi_backtest.py
(reserves, production, EROI, WTI).

Outputs:
  cesi_robustness_runs.csv   : every run + key metrics
  cesi_robustness_paths.csv  : full CESI(t) matrix for spaghetti plot
  CESI_robustness_R1.png/.svg: 4-panel dashboard (tornado + spaghetti
                                + pass-rate bar + cherry-pick percentile)
"""

import csv
import itertools
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

YEARS = list(range(1980, 2024))

# =============================================================
# DATA: identical sources to cesi_backtest.py + energy_graph.py
# =============================================================

# --- E: primary energy EJ (EI/OWID, substitution method) ---
ENERGY_TWH = {
    1980:78010.562,1981:77654.789,1982:77277.594,1983:78599.125,1984:82129.477,
    1985:84332.883,1986:86200.781,1987:89321.430,1988:92666.555,1989:94454.031,
    1990:95856.289,1991:96516.406,1992:97104.883,1993:97894.812,1994:99137.250,
    1995:101315.359,1996:104245.836,1997:105269.266,1998:105852.398,1999:107613.984,
    2000:110416.398,2001:111493.289,2002:113894.430,2003:117849.602,2004:123841.742,
    2005:127936.719,2006:131481.203,2007:135617.984,2008:137229.406,2009:135033.219,
    2010:141602.047,2011:144913.297,2012:147002.422,2013:149599.734,2014:151239.172,
    2015:152357.625,2016:154221.484,2017:157625.312,2018:161806.125,2019:163694.609,
    2020:157993.891,2021:166043.500,2022:169061.531,2023:172238.781,
}
E_EJ = {y: ENERGY_TWH[y]*0.0036 for y in YEARS}

# --- X: electricity generation TWh ---
ELEC_TWH = {
    1980:8281,1981:8370,1982:8395,1983:8680,1984:9130,1985:9886.064,1986:10180.790,
    1987:10670.628,1988:11140.627,1989:11657.959,1990:11961.414,1991:12222.524,
    1992:12336.403,1993:12599.928,1994:12923.577,1995:13381.867,1996:13797.155,
    1997:14128.604,1998:14511.013,1999:14926.271,2000:15278.690,2001:15500.420,
    2002:16049.610,2003:16627.730,2004:17414.660,2005:18133.840,2006:18839.010,
    2007:19713.949,2008:20102.471,2009:19943.439,2010:21263.609,2011:21971.910,
    2012:22515.711,2013:23155.240,2014:23747.119,2015:24003.189,2016:24695.320,
    2017:25441.971,2018:26465.289,2019:26840.510,2020:26729.109,2021:28259.730,
    2022:28918.240,2023:29665.260,
}

# --- I: industrial production index (1980=100) ---
# Same construction as energy_graph.py
WB_MVA = {
    1997:6.125,1998:5.963,1999:6.099,2000:6.251,2001:5.846,2002:5.912,2003:6.565,
    2004:7.338,2005:7.851,2006:8.491,2007:9.551,2008:10.327,2009:9.448,2010:10.689,
    2011:11.947,2012:12.194,2013:12.431,2014:12.875,2015:12.404,2016:12.467,
    2017:13.330,2018:14.279,2019:14.143,2020:13.734,2021:16.214,2022:16.218,
    2023:16.442,
}
HIST_G = {1996:0.035,1995:0.035,1994:0.040,1993:0.025,1992:-0.005,1991:-0.010,
          1990:0.020,1989:0.035,1988:0.040,1987:0.035,1986:0.030,1985:0.020,
          1984:0.035,1983:0.015,1982:-0.010,1981:0.010}
for y in range(1996, 1979, -1):
    WB_MVA[y] = WB_MVA[y+1] / (1 + HIST_G.get(y, 0.02))
I_INDEX = {y: 100*WB_MVA[y]/WB_MVA[1980] for y in YEARS}

# --- P: population-adjusted index (pop ratio * pc_ratio^0.7) ---
POPULATION = {
    1980:4447606240,1981:4528777306,1982:4612673415,1983:4697327573,1984:4782175518,
    1985:4868943457,1986:4958072839,1987:5049746390,1988:5141992540,1989:5234431736,
    1990:5327803106,1991:5418735886,1992:5505989815,1993:5591544802,1994:5675551258,
    1995:5758878977,1996:5842055730,1997:5924787819,1998:6007066691,1999:6089006328,
    2000:6171702992,2001:6254936464,2002:6337730343,2003:6420361633,2004:6503377774,
    2005:6586970132,2006:6671452019,2007:6757308776,2008:6844457659,2009:6932766416,
    2010:7021732143,2011:7110923773,2012:7201202478,2013:7291793585,2014:7381616239,
    2015:7470491876,2016:7558554527,2017:7645617952,2018:7729902779,2019:7811293699,
    2020:7887001289,2021:7954448387,2022:8021407196,2023:8091734933,
}
PER_CAP_GJ = {y: E_EJ[y]*1000/(POPULATION[y]/1e9) for y in YEARS}
POP_1980 = POPULATION[1980]; PC_1980 = PER_CAP_GJ[1980]
P_INDEX_RAW = {y: (POPULATION[y]/POP_1980)*((PER_CAP_GJ[y]/PC_1980)**0.7)*100 for y in YEARS}

# --- Supply side ---
OIL_RES = {
    1980:642.16,1981:651.60,1982:669.90,1983:665.40,1984:667.30,1985:701.20,
    1986:698.50,1987:698.50,1988:889.30,1989:908.00,1990:1001.90,1991:999.80,
    1992:990.10,1993:996.80,1994:999.00,1995:999.80,1996:1008.50,1997:1021.19,
    1998:1023.10,1999:1036.60,2000:1020.70,2001:1032.00,2002:1034.90,2003:1215.10,
    2004:1264.80,2005:1278.90,2006:1292.20,2007:1310.50,2008:1327.40,2009:1336.40,
    2010:1349.10,2011:1468.00,2012:1521.10,2013:1642.00,2014:1647.80,2015:1615.40,
    2016:1655.00,2017:1726.70,2018:1730.00,2019:1734.00,2020:1732.00,2021:1710.00,
    2022:1664.00,2023:1572.00,
}
OIL_PROD_KBPD = {
    1980:59463.80,1981:55958.40,1982:53367.30,1983:53166.60,1984:54417.60,
    1985:53882.60,1986:56242.17,1987:56572.17,1988:58615.45,1989:59725.36,
    1990:60424.25,1991:60126.34,1992:60097.77,1993:60173.79,1994:61175.25,
    1995:62430.25,1996:63816.35,1997:65797.55,1998:67022.85,1999:65898.06,
    2000:68343.04,2001:67921.63,2002:67050.84,2003:69189.99,2004:72249.60,
    2005:73516.23,2006:73099.73,2007:72698.83,2008:73583.73,2009:72385.33,
    2010:74166.13,2011:74281.63,2012:76047.63,2013:75996.83,2014:77724.30,
    2015:79784.30,2016:80622.00,2017:80600.00,2018:82844.00,2019:82200.00,
    2020:76100.00,2021:77800.00,2022:80600.00,2023:81800.00,
}
PROD_GBBL = {y: OIL_PROD_KBPD[y]*365.0/1e6 for y in YEARS}

# Baseline EROI step points
EROI_POINTS_BASE = {1980:25.0, 1992:22.0, 2000:18.0, 2006:16.0,
                    2010:15.0, 2015:12.0, 2020:10.0, 2023:9.0}

def eroi_from_points(year, points):
    keys = sorted(points.keys())
    val = points[keys[0]]
    for k in keys:
        if year >= k:
            val = points[k]
    return val

def eroi_pchip_path():
    """Smooth monotone interpolation through the same breakpoints."""
    try:
        from scipy.interpolate import PchipInterpolator
    except Exception:
        return {y: eroi_from_points(y, EROI_POINTS_BASE) for y in YEARS}
    xs = sorted(EROI_POINTS_BASE.keys())
    ys = [EROI_POINTS_BASE[x] for x in xs]
    f = PchipInterpolator(xs, ys, extrapolate=True)
    return {y: float(f(y)) for y in YEARS}

# =============================================================
# CORE CESI CALCULATION (parameterised)
# =============================================================

def compute_cesi(
    weights=(0.40, 0.30, 0.20, 0.10),
    haircut=0.25,                   # fraction of post-1987 reserves to strip
    eroi_points=None,               # dict of breakpoints; None -> baseline step
    eroi_path_array=None,           # optional direct eroi(y) dict (e.g. PCHIP)
    rp_crit=20.0,
    eroi_crit=7.0,
    base_year=1980,
):
    """Return (cesi_dict, D_dict, S_dict) with CESI[base_year] normalised = 100."""
    wE, wX, wI, wP = weights
    # EROI path
    if eroi_path_array is not None:
        eroi = {y: eroi_path_array[y] for y in YEARS}
    else:
        pts = eroi_points if eroi_points is not None else EROI_POINTS_BASE
        eroi = {y: eroi_from_points(y, pts) for y in YEARS}

    # Normalise demand inputs to base_year = 100
    E_b = E_EJ[base_year]; X_b = ELEC_TWH[base_year]
    I_b = I_INDEX[base_year]; P_b = P_INDEX_RAW[base_year]
    E_n = {y: 100.0*E_EJ[y]/E_b for y in YEARS}
    X_n = {y: 100.0*ELEC_TWH[y]/X_b for y in YEARS}
    I_n = {y: 100.0*I_INDEX[y]/I_b for y in YEARS}
    P_n = {y: 100.0*P_INDEX_RAW[y]/P_b for y in YEARS}
    D = {y: wE*E_n[y] + wX*X_n[y] + wI*I_n[y] + wP*P_n[y] for y in YEARS}

    # Deflated reserves (post-1987 haircut)
    Res = {y: OIL_RES[y] if y <= 1987 else OIL_RES[y]*(1.0 - haircut) for y in YEARS}
    RP  = {y: Res[y]/PROD_GBBL[y] for y in YEARS}
    RP_n   = {y: 100.0*RP[y]/RP[base_year] for y in YEARS}
    ER_n   = {y: 100.0*eroi[y]/eroi[base_year] for y in YEARS}

    def calc_S_raw(y):
        S = (RP_n[y]*ER_n[y])/100.0
        if RP[y] < rp_crit:
            Tr = rp_crit - RP[y]
            S = S / (1.0 + (Tr/rp_crit)**2)
        if eroi[y] < eroi_crit:
            Te = eroi_crit - eroi[y]
            S = S / (1.0 + (Te/eroi_crit)**2)
        return S

    S_raw = {y: calc_S_raw(y) for y in YEARS}
    S_norm_factor = 100.0/S_raw[base_year]
    S = {y: S_raw[y]*S_norm_factor for y in YEARS}

    cesi = {y: (D[y]/S[y])*100.0 for y in YEARS}
    # Renormalise so CESI[base_year] = 100 exactly
    cesi_base = cesi[base_year]
    cesi = {y: cesi[y]*100.0/cesi_base for y in YEARS}
    return cesi, D, S

# =============================================================
# METRICS
# =============================================================

def metrics(cesi):
    vals = [cesi[y] for y in YEARS]
    cesi_1980 = cesi[YEARS[0]]
    cesi_2023 = cesi[YEARS[-1]]

    # Criterion A: structural monotonic rise:
    #   5-year rolling mean of CESI exhibits drawdown <= 5% of concurrent peak.
    #   This filters single-year recession noise (1982, 2009, 2020) and tests
    #   whether the underlying *trend* is monotonic, which is the actual claim.
    arr = np.array(vals)
    # 5-year trailing mean (NaN-padded for first 4 years)
    rmean = np.array([np.nan]*4 + [arr[i-4:i+1].mean() for i in range(4, len(arr))])
    # Compute drawdown on the rolling mean (skip leading NaNs)
    valid = rmean[~np.isnan(rmean)]
    max_dd = 0.0; max_dd_pct = 0.0
    peak = valid[0]
    for v in valid:
        peak = max(peak, v)
        dd = peak - v
        if dd > max_dd: max_dd = dd
        dd_pct = dd/peak if peak > 0 else 0.0
        if dd_pct > max_dd_pct: max_dd_pct = dd_pct
    crit_A = (cesi_2023 > cesi_1980) and (max_dd_pct <= 0.05)

    # Criterion C: rising decade-floor
    decades = [(1980,1989),(1990,1999),(2000,2009),(2010,2019),(2020,2023)]
    floors = []
    for lo, hi in decades:
        dec = [cesi[y] for y in YEARS if lo <= y <= hi]
        floors.append(min(dec))
    crit_C = all(floors[i] < floors[i+1] for i in range(len(floors)-1))

    return {
        "cesi_1980": cesi_1980,
        "cesi_2023": cesi_2023,
        "max_dd": max_dd,
        "max_dd_pct": max_dd_pct,
        "crit_A_monotonic": crit_A,
        "crit_C_rising_floor": crit_C,
    }

def rank_corr(a, b):
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0,1])

# =============================================================
# BASELINE
# =============================================================
baseline_cesi, _, _ = compute_cesi()
baseline_vals = [baseline_cesi[y] for y in YEARS]
baseline_m = metrics(baseline_cesi)

# =============================================================
# AXIS 1: WEIGHTS (OAT + a few cross-cuts)
# =============================================================
WEIGHT_RUNS = []
# Baseline
WEIGHT_RUNS.append(("baseline", (0.40,0.30,0.20,0.10)))
# OAT: ±0.05, ±0.10, ±0.15 on each weight, distribute to other three proportionally
def perturb_weight(base, idx, delta):
    w = list(base)
    new = w[idx] + delta
    if new < 0.02 or new > 0.90: return None
    rest_idx = [i for i in range(4) if i != idx]
    rest_total = sum(w[i] for i in rest_idx)
    if rest_total <= 0: return None
    scale = (1.0 - new)/rest_total
    for i in rest_idx:
        w[i] *= scale
    w[idx] = new
    return tuple(w)

base_w = (0.40,0.30,0.20,0.10)
names  = ["wE","wX","wI","wP"]
for i, nm in enumerate(names):
    for d in [-0.15, -0.10, -0.05, 0.05, 0.10, 0.15, 0.20, 0.30]:
        w = perturb_weight(base_w, i, d)
        if w is None: continue
        WEIGHT_RUNS.append((f"{nm}{d:+.2f}", w))
# Equal weights
WEIGHT_RUNS.append(("equal_025", (0.25,0.25,0.25,0.25)))
# E-dominant, X-dominant, I-dominant, P-dominant extremes
WEIGHT_RUNS.append(("E_dominant", (0.70,0.15,0.10,0.05)))
WEIGHT_RUNS.append(("X_dominant", (0.15,0.70,0.10,0.05)))
WEIGHT_RUNS.append(("I_dominant", (0.10,0.15,0.70,0.05)))
WEIGHT_RUNS.append(("P_dominant", (0.10,0.15,0.05,0.70)))
# EX-heavy, IP-heavy
WEIGHT_RUNS.append(("EX_heavy",  (0.45,0.45,0.05,0.05)))
WEIGHT_RUNS.append(("IP_heavy",  (0.05,0.05,0.45,0.45)))

# =============================================================
# AXIS 2: OPEC HAIRCUT
# =============================================================
HAIRCUT_RUNS = [(f"haircut_{int(h*100):02d}pct", h)
                for h in [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]]

# =============================================================
# AXIS 3: EROI PATH
# =============================================================
def scale_eroi(points, scale_endpoint):
    """Scale endpoints while keeping 1980 start; linear mix on later points."""
    keys = sorted(points.keys())
    start = points[keys[0]]
    end   = points[keys[-1]]
    new_end = end * (1.0 + scale_endpoint)
    new = {}
    for k in keys:
        t = (k - keys[0]) / (keys[-1] - keys[0])
        orig = points[k]
        target = start + (orig - start) * ((new_end - start)/(end - start)) if end != start else orig
        new[k] = target
    return new

EROI_RUNS = [("eroi_baseline", EROI_POINTS_BASE, None)]
for s in [-0.20, -0.10, +0.10, +0.20]:
    EROI_RUNS.append((f"eroi_end{int(s*100):+03d}pct",
                      scale_eroi(EROI_POINTS_BASE, s), None))
# Uniform shift
EROI_RUNS.append(("eroi_all_m10pct",
                  {k: v*0.90 for k,v in EROI_POINTS_BASE.items()}, None))
EROI_RUNS.append(("eroi_all_p10pct",
                  {k: v*1.10 for k,v in EROI_POINTS_BASE.items()}, None))
EROI_RUNS.append(("eroi_pchip_smooth", None, eroi_pchip_path()))

# =============================================================
# AXIS 4: THRESHOLDS
# =============================================================
THRESH_RUNS = []
for rp_c in [15, 18, 20, 22, 25]:
    for er_c in [5, 6, 7, 8, 9]:
        THRESH_RUNS.append((f"thr_rp{rp_c}_er{er_c}", rp_c, er_c))

# =============================================================
# AXIS 5: BASE YEAR
# =============================================================
BASE_RUNS = [("base_1980",1980),("base_1990",1990),("base_2000",2000)]

# =============================================================
# MULTI-AXIS STRESS COMBOS
# =============================================================
STRESS_RUNS = [
    ("stress_all_against", dict(weights=(0.25,0.25,0.25,0.25), haircut=0.00,
                                eroi_points={k: v*1.10 for k,v in EROI_POINTS_BASE.items()},
                                rp_crit=15, eroi_crit=5, base_year=1980)),
    ("stress_all_favor",   dict(weights=(0.40,0.30,0.20,0.10), haircut=0.40,
                                eroi_points={k: v*0.80 for k,v in EROI_POINTS_BASE.items()},
                                rp_crit=25, eroi_crit=9, base_year=1980)),
    ("stress_bear_eroi",   dict(weights=(0.40,0.30,0.20,0.10), haircut=0.25,
                                eroi_points=None, rp_crit=20, eroi_crit=7, base_year=1980,
                                _eroi_path=eroi_pchip_path())),
    ("stress_mild_opec",   dict(weights=(0.40,0.30,0.20,0.10), haircut=0.10,
                                eroi_points=None, rp_crit=20, eroi_crit=7, base_year=1980)),
    ("stress_severe_opec", dict(weights=(0.40,0.30,0.20,0.10), haircut=0.35,
                                eroi_points=None, rp_crit=20, eroi_crit=7, base_year=1980)),
]

# =============================================================
# RUN ALL
# =============================================================
runs = []   # (run_id, axis, params_dict, cesi_dict, metrics_dict)

def add_run(run_id, axis, params, cesi):
    m = metrics(cesi)
    vals = [cesi[y] for y in YEARS]
    m["rank_corr_vs_base"] = rank_corr(vals, baseline_vals) if run_id != "baseline" else 1.0
    m["delta_cesi2023_pct"] = 100.0*(m["cesi_2023"]-baseline_m["cesi_2023"])/baseline_m["cesi_2023"]
    runs.append((run_id, axis, params, cesi, m))

# Baseline
add_run("baseline", "baseline", {}, baseline_cesi)

# Weights
for rid, w in WEIGHT_RUNS:
    if rid == "baseline": continue
    cesi, _, _ = compute_cesi(weights=w)
    add_run(rid, "weights", {"weights":w}, cesi)

# Haircut
for rid, h in HAIRCUT_RUNS:
    cesi, _, _ = compute_cesi(haircut=h)
    add_run(rid, "haircut", {"haircut":h}, cesi)

# EROI
for rid, pts, arr in EROI_RUNS:
    cesi, _, _ = compute_cesi(eroi_points=pts, eroi_path_array=arr)
    add_run(rid, "eroi", {"eroi_points":pts, "eroi_array_keys": "PCHIP" if arr else None}, cesi)

# Thresholds
for rid, rp_c, er_c in THRESH_RUNS:
    cesi, _, _ = compute_cesi(rp_crit=rp_c, eroi_crit=er_c)
    add_run(rid, "thresholds", {"rp_crit":rp_c, "eroi_crit":er_c}, cesi)

# Base year
for rid, by in BASE_RUNS:
    cesi, _, _ = compute_cesi(base_year=by)
    add_run(rid, "base_year", {"base_year":by}, cesi)

# Stress
for rid, cfg in STRESS_RUNS:
    ep = cfg.get("_eroi_path", None)
    kwargs = {k:v for k,v in cfg.items() if k != "_eroi_path"}
    if ep is not None:
        cesi, _, _ = compute_cesi(**{**kwargs, "eroi_path_array": ep})
    else:
        cesi, _, _ = compute_cesi(**kwargs)
    add_run(rid, "stress", cfg, cesi)

print("="*70)
print(f"R1 ROBUSTNESS SUITE  --  {len(runs)} runs executed")
print("="*70)

# =============================================================
# AGGREGATE METRICS
# =============================================================
non_base = [r for r in runs if r[0] != "baseline"]
cesi2023 = np.array([r[4]["cesi_2023"] for r in non_base])
crit_A_pass = sum(1 for r in non_base if r[4]["crit_A_monotonic"])
crit_C_pass = sum(1 for r in non_base if r[4]["crit_C_rising_floor"])
rank_corrs  = np.array([r[4]["rank_corr_vs_base"] for r in non_base])

print(f"\nBaseline CESI_2023: {baseline_m['cesi_2023']:.2f}")
print(f"Perturbation distribution of CESI_2023:")
print(f"   min {cesi2023.min():.2f}  p10 {np.percentile(cesi2023,10):.2f}  "
      f"p25 {np.percentile(cesi2023,25):.2f}  median {np.median(cesi2023):.2f}  "
      f"p75 {np.percentile(cesi2023,75):.2f}  p90 {np.percentile(cesi2023,90):.2f}  "
      f"max {cesi2023.max():.2f}")

# Cherry-pick percentile: where does baseline sit?
baseline_pct = 100.0*(cesi2023 < baseline_m["cesi_2023"]).sum()/len(cesi2023)
print(f"Baseline CESI_2023 percentile within perturbations: {baseline_pct:.1f}%")

print(f"\nPass rates across {len(non_base)} non-baseline perturbations:")
print(f"   Criterion A (monotonic rise) : {crit_A_pass}/{len(non_base)} = {100.0*crit_A_pass/len(non_base):.1f}%")
print(f"   Criterion C (rising floor)   : {crit_C_pass}/{len(non_base)} = {100.0*crit_C_pass/len(non_base):.1f}%")
print(f"   Median rank-correlation      : {np.median(rank_corrs):.3f}")
print(f"   p10 rank-correlation         : {np.percentile(rank_corrs,10):.3f}")

# =============================================================
# TORNADO: per-axis CESI_2023 range
# =============================================================
AXES = ["weights","haircut","eroi","thresholds","base_year","stress"]
tornado_data = []
for ax in AXES:
    vals = [r[4]["cesi_2023"] for r in runs if r[1] == ax]
    if not vals: continue
    lo, hi = min(vals), max(vals)
    tornado_data.append((ax, lo, hi, hi-lo))
tornado_data.sort(key=lambda t: t[3], reverse=True)

print("\nTornado (per-axis CESI_2023 range):")
for ax, lo, hi, rng in tornado_data:
    print(f"   {ax:12s}  min={lo:7.2f}  max={hi:7.2f}  range={rng:7.2f}")

# =============================================================
# EXPORT CSVs
# =============================================================
with open("C:/Users/OMU/Desktop/Energy/cesi_robustness_runs.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["run_id","axis","params","CESI_1980","CESI_2023","max_dd",
                "crit_A","crit_C","rank_corr_vs_base","delta_vs_base_pct"])
    for rid, ax, p, _, m in runs:
        w.writerow([rid, ax, str(p),
                    f"{m['cesi_1980']:.3f}", f"{m['cesi_2023']:.3f}",
                    f"{m['max_dd']:.3f}",
                    int(m['crit_A_monotonic']), int(m['crit_C_rising_floor']),
                    f"{m['rank_corr_vs_base']:.4f}",
                    f"{m['delta_cesi2023_pct']:+.2f}"])
print("\nSaved: cesi_robustness_runs.csv")

with open("C:/Users/OMU/Desktop/Energy/cesi_robustness_paths.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["year"] + [r[0] for r in runs])
    for y in YEARS:
        w.writerow([y] + [f"{r[3][y]:.3f}" for r in runs])
print("Saved: cesi_robustness_paths.csv")

# =============================================================
# DASHBOARD
# =============================================================
ACCENT  = "#1B3A5C"; ACCENT2 = "#2E75B6"
GREEN   = "#27AE60"; RED     = "#C0392B"; GREY = "#7F8C8D"
AMBER   = "#E67E22"

fig = plt.figure(figsize=(15, 11))
fig.suptitle(f"CESI ROBUSTNESS R1: Parameter Sensitivity ({len(runs)} runs)",
             fontsize=14, fontweight="bold", color=ACCENT)

# Panel 1: Spaghetti plot
ax1 = fig.add_subplot(2, 2, 1)
for rid, ax, p, cesi, m in runs:
    vals = [cesi[y] for y in YEARS]
    col = ACCENT if rid == "baseline" else GREY
    lw  = 2.4 if rid == "baseline" else 0.7
    a   = 1.0 if rid == "baseline" else 0.28
    ax1.plot(YEARS, vals, color=col, lw=lw, alpha=a,
             label="baseline" if rid=="baseline" else None)
# Envelope band
path_matrix = np.array([[r[3][y] for y in YEARS] for r in runs if r[0]!="baseline"])
p10 = np.percentile(path_matrix, 10, axis=0)
p90 = np.percentile(path_matrix, 90, axis=0)
ax1.fill_between(YEARS, p10, p90, color=ACCENT2, alpha=0.18, label="p10-p90 envelope")
ax1.set_title("CESI(t) under all perturbations", fontweight="bold")
ax1.set_ylabel("CESI (base=100)"); ax1.set_xlabel("Year")
ax1.grid(True, alpha=0.3); ax1.legend(loc="upper left", fontsize=9)

# Panel 2: Tornado
ax2 = fig.add_subplot(2, 2, 2)
names_ord = [t[0] for t in tornado_data]
ranges    = [t[3] for t in tornado_data]
lows      = [t[1] for t in tornado_data]
highs     = [t[2] for t in tornado_data]
y_pos = np.arange(len(names_ord))
base_val = baseline_m["cesi_2023"]
for i, (nm, lo, hi, rng) in enumerate(tornado_data):
    ax2.barh(i, hi-base_val, left=base_val, color=RED,   alpha=0.6, edgecolor="black", lw=0.5)
    ax2.barh(i, lo-base_val, left=base_val, color=GREEN, alpha=0.6, edgecolor="black", lw=0.5)
    ax2.text(hi+1, i, f"{hi:.0f}", va="center", fontsize=8)
    ax2.text(lo-1, i, f"{lo:.0f}", va="center", fontsize=8, ha="right")
ax2.axvline(base_val, color="black", lw=1.2, ls="--")
ax2.set_yticks(y_pos); ax2.set_yticklabels(names_ord)
ax2.set_xlabel(f"CESI_2023 (baseline = {base_val:.1f})")
ax2.set_title("Tornado: CESI_2023 range by axis", fontweight="bold")
ax2.grid(True, alpha=0.3, axis="x")
ax2.invert_yaxis()

# Panel 3: Pass rate + cherry-pick percentile
ax3 = fig.add_subplot(2, 2, 3)
pctA = 100.0*crit_A_pass/len(non_base)
pctC = 100.0*crit_C_pass/len(non_base)
med_rc = 100.0*np.median(rank_corrs)
bars_data = [("A. Monotonic rise", pctA),
             ("C. Rising floor", pctC),
             ("Median rank-corr vs base", med_rc),
             ("Baseline CESI_2023 percentile", baseline_pct)]
lbls = [b[0] for b in bars_data]; vals_p = [b[1] for b in bars_data]
colors_p = [GREEN if v >= 80 else (AMBER if v >= 60 else RED) for v in vals_p]
# last bar is "cherry-pick"; PASS if 25<=v<=75
cp_v = bars_data[-1][1]
colors_p[-1] = GREEN if 25 <= cp_v <= 75 else (AMBER if 15 <= cp_v <= 85 else RED)
bs = ax3.barh(lbls, vals_p, color=colors_p, edgecolor="black", lw=0.5)
for b, v in zip(bs, vals_p):
    ax3.text(v+1, b.get_y()+b.get_height()/2, f"{v:.1f}%", va="center", fontsize=9)
ax3.axvline(80, color=GREEN, ls="--", lw=0.8, alpha=0.7)
ax3.axvline(60, color=AMBER, ls="--", lw=0.8, alpha=0.7)
ax3.set_xlim(0, 110)
ax3.set_title("Aggregate robustness metrics (%)", fontweight="bold")
ax3.invert_yaxis()
ax3.grid(True, alpha=0.3, axis="x")

# Panel 4: Summary table
ax4 = fig.add_subplot(2, 2, 4); ax4.axis("off")
summary_rows = [
    ["Baseline CESI_2023", f"{baseline_m['cesi_2023']:.1f}"],
    ["Perturbations run", f"{len(non_base)}"],
    ["CESI_2023 p10", f"{np.percentile(cesi2023,10):.1f}"],
    ["CESI_2023 p25", f"{np.percentile(cesi2023,25):.1f}"],
    ["CESI_2023 median", f"{np.median(cesi2023):.1f}"],
    ["CESI_2023 p75", f"{np.percentile(cesi2023,75):.1f}"],
    ["CESI_2023 p90", f"{np.percentile(cesi2023,90):.1f}"],
    ["Baseline percentile", f"{baseline_pct:.1f}%  {'PASS' if 25<=baseline_pct<=75 else 'FLAG'}"],
    ["Crit A pass rate", f"{pctA:.1f}%  {'PASS' if pctA>=80 else 'FAIL'}"],
    ["Crit C pass rate", f"{pctC:.1f}%  {'PASS' if pctC>=80 else 'FAIL'}"],
    ["Median rank-corr", f"{np.median(rank_corrs):.3f}  {'PASS' if np.median(rank_corrs)>=0.90 else 'FAIL'}"],
    ["p10 rank-corr",   f"{np.percentile(rank_corrs,10):.3f}"],
    ["Dominant axis (tornado)", tornado_data[0][0]],
    ["Most-benign axis", tornado_data[-1][0]],
]
tbl = ax4.table(cellText=summary_rows, loc="center", cellLoc="left",
                colWidths=[0.55, 0.40])
tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1, 1.5)
for i, row in enumerate(summary_rows):
    tbl[(i,0)].set_facecolor("#EAEFF5")
ax4.set_title("Summary", fontweight="bold", color=ACCENT)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("C:/Users/OMU/Desktop/Energy/CESI_robustness_R1.png", dpi=160, bbox_inches="tight")
plt.savefig("C:/Users/OMU/Desktop/Energy/CESI_robustness_R1.svg", bbox_inches="tight")
plt.close()
print("\nSaved: CESI_robustness_R1.png / .svg")
print("="*70)
print("R1 COMPLETE")
print("="*70)
