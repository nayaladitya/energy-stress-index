"""
CESI BACKTEST — TEST 1: ANNUAL STRUCTURAL BACKTEST
===================================================
Validates CESI 1980–2023 using only genuinely annual data.
No interpolation. No proxies. No manufactured data points.

Layer 2 simplified for annual frequency:
  D = E_norm (energy consumption only — the direct measurement)
  S = (RP_norm × EROI_norm) / 100, with threshold adjustments

Five structural validation tests scored 0–5.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import csv
import os

YEARS = list(range(1980, 2024))

# ================================================================
# SERIES 1 — Global Primary Energy Consumption (EJ)
# Source: Energy Institute Statistical Review via OWID
# ================================================================
energy_twh = {
    1980: 78010.562, 1981: 77654.789, 1982: 77277.594, 1983: 78599.125,
    1984: 82129.477, 1985: 84332.883, 1986: 86200.781, 1987: 89321.430,
    1988: 92666.555, 1989: 94454.031, 1990: 95856.289, 1991: 96516.406,
    1992: 97104.883, 1993: 97894.812, 1994: 99137.250, 1995: 101315.359,
    1996: 104245.836, 1997: 105269.266, 1998: 105852.398, 1999: 107613.984,
    2000: 110416.398, 2001: 111493.289, 2002: 113894.430, 2003: 117849.602,
    2004: 123841.742, 2005: 127936.719, 2006: 131481.203, 2007: 135617.984,
    2008: 137229.406, 2009: 135033.219, 2010: 141602.047, 2011: 144913.297,
    2012: 147002.422, 2013: 149599.734, 2014: 151239.172, 2015: 152357.625,
    2016: 154221.484, 2017: 157625.312, 2018: 161806.125, 2019: 163694.609,
    2020: 157993.891, 2021: 166043.500, 2022: 169061.531, 2023: 172238.781,
}
E_ej = {y: energy_twh[y] * 0.0036 for y in YEARS}

# ================================================================
# SERIES 2 — Global Oil Proved Reserves (Billion Barrels)
# Source: US EIA International Energy Statistics via IndexMundi
# ================================================================
oil_reserves_official = {
    1980: 642.16, 1981: 651.60, 1982: 669.90, 1983: 665.40, 1984: 667.30,
    1985: 701.20, 1986: 698.50, 1987: 698.50, 1988: 889.30, 1989: 908.00,
    1990: 1001.90, 1991: 999.80, 1992: 990.10, 1993: 996.80, 1994: 999.00,
    1995: 999.80, 1996: 1008.50, 1997: 1021.19, 1998: 1023.10, 1999: 1036.60,
    2000: 1020.70, 2001: 1032.00, 2002: 1034.90, 2003: 1215.10, 2004: 1264.80,
    2005: 1278.90, 2006: 1292.20, 2007: 1310.50, 2008: 1327.40, 2009: 1336.40,
    2010: 1349.10, 2011: 1468.00, 2012: 1521.10, 2013: 1642.00, 2014: 1647.80,
    2015: 1615.40, 2016: 1655.00, 2017: 1726.70, 2018: 1730.00, 2019: 1734.00,
    2020: 1732.00, 2021: 1710.00, 2022: 1664.00, 2023: 1572.00,
}

# STEP 1: OPEC Reserve Deflation
# Pre-1988: official unchanged. Post-1987 inclusive: x0.75
oil_reserves_deflated = {}
for y in YEARS:
    if y <= 1987:
        oil_reserves_deflated[y] = oil_reserves_official[y]
    else:
        oil_reserves_deflated[y] = oil_reserves_official[y] * 0.75

# ================================================================
# SERIES 3 — Global Oil Production (kbpd -> Gbbl/yr)
# Source: EIA International Energy Statistics via IndexMundi
# ================================================================
oil_prod_kbpd = {
    1980: 59463.80, 1981: 55958.40, 1982: 53367.30, 1983: 53166.60,
    1984: 54417.60, 1985: 53882.60, 1986: 56242.17, 1987: 56572.17,
    1988: 58615.45, 1989: 59725.36, 1990: 60424.25, 1991: 60126.34,
    1992: 60097.77, 1993: 60173.79, 1994: 61175.25, 1995: 62430.25,
    1996: 63816.35, 1997: 65797.55, 1998: 67022.85, 1999: 65898.06,
    2000: 68343.04, 2001: 67921.63, 2002: 67050.84, 2003: 69189.99,
    2004: 72249.60, 2005: 73516.23, 2006: 73099.73, 2007: 72698.83,
    2008: 73583.73, 2009: 72385.33, 2010: 74166.13, 2011: 74281.63,
    2012: 76047.63, 2013: 75996.83, 2014: 77724.30, 2015: 79784.30,
    2016: 80622.00, 2017: 80600.00, 2018: 82844.00, 2019: 82200.00,
    2020: 76100.00, 2021: 77800.00, 2022: 80600.00, 2023: 81800.00,
}
oil_prod_gbbl = {y: oil_prod_kbpd[y] * 365.0 / 1e6 for y in YEARS}

# STEP 2: R/P Ratio
RP_deflated = {y: oil_reserves_deflated[y] / oil_prod_gbbl[y] for y in YEARS}
RP_official = {y: oil_reserves_official[y] / oil_prod_gbbl[y] for y in YEARS}

# ================================================================
# SERIES 4 — EROI Step Function
# Source: Hall et al. 2014, Brandt et al. 2013, Murphy & Hall 2010
# Assigned as step function: each year uses most recent data point
# ================================================================
EROI_POINTS = {1980: 25.0, 1992: 22.0, 2000: 18.0, 2006: 16.0,
               2010: 15.0, 2015: 12.0, 2020: 10.0, 2023: 9.0}
EROI_BREAKPOINTS = sorted(EROI_POINTS.keys())

def eroi_step(year):
    """Return most recent published EROI data point (step function)."""
    val = EROI_POINTS[EROI_BREAKPOINTS[0]]
    for bp in EROI_BREAKPOINTS:
        if year >= bp:
            val = EROI_POINTS[bp]
    return val

EROI = {y: eroi_step(y) for y in YEARS}

# ================================================================
# SERIES 5 — WTI Crude Oil Spot Price
# Source: FRED WTISPLC / EIA
# ================================================================
wti_nominal = {
    1980: 37.38, 1981: 36.67, 1982: 33.64, 1983: 30.40, 1984: 29.28,
    1985: 27.97, 1986: 15.04, 1987: 19.16, 1988: 15.96, 1989: 19.59,
    1990: 24.49, 1991: 21.48, 1992: 20.56, 1993: 18.46, 1994: 17.19,
    1995: 18.43, 1996: 22.15, 1997: 20.60, 1998: 14.39, 1999: 19.25,
    2000: 30.30, 2001: 25.92, 2002: 26.10, 2003: 31.14, 2004: 41.44,
    2005: 56.47, 2006: 66.10, 2007: 72.36, 2008: 99.57, 2009: 61.69,
    2010: 79.43, 2011: 95.08, 2012: 94.20, 2013: 97.94, 2014: 93.26,
    2015: 48.69, 2016: 43.14, 2017: 50.88, 2018: 64.94, 2019: 56.98,
    2020: 39.23, 2021: 67.99, 2022: 94.79, 2023: 77.64,
}

cpi_index = {
    1980: 82.4, 1981: 90.9, 1982: 96.5, 1983: 99.6, 1984: 103.9,
    1985: 107.6, 1986: 109.7, 1987: 113.6, 1988: 118.3, 1989: 123.9,
    1990: 130.7, 1991: 136.2, 1992: 140.3, 1993: 144.5, 1994: 148.2,
    1995: 152.4, 1996: 156.9, 1997: 160.5, 1998: 163.0, 1999: 166.6,
    2000: 172.2, 2001: 177.0, 2002: 179.9, 2003: 184.0, 2004: 188.9,
    2005: 195.3, 2006: 201.6, 2007: 207.3, 2008: 215.3, 2009: 214.6,
    2010: 218.1, 2011: 224.9, 2012: 229.6, 2013: 233.0, 2014: 236.7,
    2015: 237.0, 2016: 240.0, 2017: 245.1, 2018: 251.1, 2019: 255.7,
    2020: 258.8, 2021: 271.0, 2022: 292.7, 2023: 304.7,
}

wti_real_2023 = {y: wti_nominal[y] * (cpi_index[2023] / cpi_index[y]) for y in YEARS}

# ================================================================
# SERIES 6 — World GDP (constant 2015 USD, trillions)
# Source: World Bank NY.GDP.MKTP.KD
# ================================================================
world_gdp = {
    1980: 26.47, 1981: 26.97, 1982: 27.07, 1983: 27.77, 1984: 29.07,
    1985: 30.14, 1986: 31.13, 1987: 32.29, 1988: 33.75, 1989: 34.99,
    1990: 35.95, 1991: 36.39, 1992: 37.15, 1993: 37.85, 1994: 39.14,
    1995: 40.37, 1996: 41.82, 1997: 43.48, 1998: 44.72, 1999: 46.32,
    2000: 48.43, 2001: 49.41, 2002: 50.55, 2003: 52.12, 2004: 54.47,
    2005: 56.67, 2006: 59.21, 2007: 61.82, 2008: 63.12, 2009: 62.29,
    2010: 65.10, 2011: 67.28, 2012: 69.11, 2013: 71.11, 2014: 73.34,
    2015: 75.62, 2016: 77.73, 2017: 80.42, 2018: 83.05, 2019: 85.28,
    2020: 82.80, 2021: 88.11, 2022: 91.11, 2023: 93.80,
}
# Energy intensity: EJ per trillion constant 2015 USD
energy_intensity = {y: E_ej[y] / world_gdp[y] for y in YEARS}
# Energy-weighted GDP index (1980=100)
ei_gdp_index = {y: (world_gdp[y] * energy_intensity[y]) /
                    (world_gdp[1980] * energy_intensity[1980]) * 100 for y in YEARS}

# ================================================================
# STEP 3 — NORMALISATION (all to 1980 = 100)
# ================================================================
E_1980 = E_ej[1980]
RP_1980 = RP_deflated[1980]
EROI_1980 = EROI[1980]  # = 25.0
WTI_1980_real = wti_real_2023[1980]

E_norm = {y: (E_ej[y] / E_1980) * 100 for y in YEARS}
RP_norm = {y: (RP_deflated[y] / RP_1980) * 100 for y in YEARS}
EROI_norm = {y: (EROI[y] / EROI_1980) * 100 for y in YEARS}
WTI_norm = {y: (wti_real_2023[y] / WTI_1980_real) * 100 for y in YEARS}
RP_official_norm = {y: (RP_official[y] / RP_official[1980]) * 100 for y in YEARS}

# ================================================================
# CESI ANNUAL CALCULATION
# ================================================================
# Demand: D = E_norm (single variable at annual frequency)
D = {y: E_norm[y] for y in YEARS}

# Supply: S_base = (RP_norm x EROI_norm) / 100
# Then threshold adjustments
def calc_S(year, use_deflated=True):
    rp_n = RP_norm[year] if use_deflated else RP_official_norm[year]
    eroi_n = EROI_norm[year]
    S_base = (rp_n * eroi_n) / 100

    rp_val = RP_deflated[year] if use_deflated else RP_official[year]
    eroi_val = EROI[year]

    # Threshold adjustments
    if rp_val < 20:
        T_r = 20 - rp_val
        mult_r = 1 + (T_r / 20) ** 2
        S_base = S_base / mult_r

    if eroi_val < 7:
        T_e = 7 - eroi_val
        mult_e = 1 + (T_e / 7) ** 2
        S_base = S_base / mult_e

    return S_base

S_deflated = {y: calc_S(y, use_deflated=True) for y in YEARS}
S_official = {y: calc_S(y, use_deflated=False) for y in YEARS}

# Normalise S so that S_1980 = 100
S_norm_factor = 100.0 / S_deflated[1980]
S_norm_factor_off = 100.0 / S_official[1980]
S = {y: S_deflated[y] * S_norm_factor for y in YEARS}
S_off = {y: S_official[y] * S_norm_factor_off for y in YEARS}

# CESI = (D / S) x 100
CESI = {y: (D[y] / S[y]) * 100 for y in YEARS}
CESI_official = {y: (D[y] / S_off[y]) * 100 for y in YEARS}

# Divergence = CESI - WTI_norm
Divergence = {y: CESI[y] - WTI_norm[y] for y in YEARS}

# ================================================================
# STRUCTURAL VALIDATION TESTS
# ================================================================
results = {}

# --- Test A: Monotonic stress accumulation ---
rises = sum(1 for i in range(1, len(YEARS)) if CESI[YEARS[i]] > CESI[YEARS[i-1]])
total = len(YEARS) - 1
pct_rising = rises / total * 100
test_a = pct_rising > 70
results['A'] = {
    'name': 'Monotonic Rise',
    'metric': f'{rises}/{total} years rising ({pct_rising:.1f}%)',
    'target': '>70%',
    'pass': test_a,
}

# --- Test B: Declining correlation with WTI by decade ---
def pearson_r(x, y):
    n = len(x)
    if n < 3:
        return float('nan')
    mx, my = np.mean(x), np.mean(y)
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    dx = sum((xi - mx)**2 for xi in x) ** 0.5
    dy = sum((yi - my)**2 for yi in y) ** 0.5
    if dx == 0 or dy == 0:
        return float('nan')
    return num / (dx * dy)

decades = {
    '1980s': list(range(1980, 1990)),
    '1990s': list(range(1990, 2000)),
    '2000s': list(range(2000, 2010)),
    '2010s': list(range(2010, 2020)),
    '2020s': list(range(2020, 2024)),
}
corr_by_decade = {}
for name, yrs in decades.items():
    c_vals = [CESI[y] for y in yrs]
    w_vals = [WTI_norm[y] for y in yrs]
    corr_by_decade[name] = pearson_r(c_vals, w_vals)

full_corr = pearson_r([CESI[y] for y in YEARS], [WTI_norm[y] for y in YEARS])

# Test B passes if correlation trend is declining
corr_values = [v for v in corr_by_decade.values() if not np.isnan(v)]
test_b = len(corr_values) >= 3 and (corr_values[-1] < corr_values[0] or
         np.mean(corr_values[-2:]) < np.mean(corr_values[:2]))
results['B'] = {
    'name': 'Declining WTI Correlation',
    'metric': ' | '.join(f'{k}: {v:.3f}' for k, v in corr_by_decade.items()),
    'target': 'Declining trend across decades',
    'pass': test_b,
    'full_corr': full_corr,
}

# --- Test C: Rising floor at cyclical troughs ---
# Identify troughs: 1986, 1998, 2009 (post-GFC), 2020 (COVID)
trough_years = [1986, 1998, 2009, 2020]
trough_values = {y: CESI[y] for y in trough_years}
floor_rising = all(trough_values[trough_years[i]] > trough_values[trough_years[i-1]]
                   for i in range(1, len(trough_years)))
results['C'] = {
    'name': 'Rising Floor',
    'metric': ' -> '.join(f'{y}: {trough_values[y]:.1f}' for y in trough_years),
    'target': 'Each trough higher than previous',
    'pass': floor_rising,
}

# --- Test D: Component contribution analysis ---
# For each decade, which component drove CESI more: demand growth or supply deterioration?
component_analysis = {}
for name, yrs in decades.items():
    d_start, d_end = D[yrs[0]], D[yrs[-1]]
    s_start, s_end = S[yrs[0]], S[yrs[-1]]
    d_change = (d_end / d_start - 1) * 100
    s_change = (s_end / s_start - 1) * 100  # negative = supply deterioration

    # CESI rises when D grows OR S falls. Attribute proportionally.
    cesi_start, cesi_end = CESI[yrs[0]], CESI[yrs[-1]]
    cesi_change = cesi_end - cesi_start

    # Decompose: if only D changed, CESI would be (D_end/S_start)*100
    cesi_d_only = (D[yrs[-1]] / S[yrs[0]]) * 100
    cesi_s_only = (D[yrs[0]] / S[yrs[-1]]) * 100

    demand_contrib = cesi_d_only - cesi_start
    supply_contrib = cesi_s_only - cesi_start

    driver = 'DEMAND' if abs(demand_contrib) > abs(supply_contrib) else 'SUPPLY'
    component_analysis[name] = {
        'd_change_pct': d_change,
        's_change_pct': s_change,
        'demand_contrib': demand_contrib,
        'supply_contrib': supply_contrib,
        'driver': driver,
    }

# Test D: both contribute, and supply becomes more important after 2005
early_supply = abs(component_analysis['1980s']['supply_contrib']) + abs(component_analysis['1990s']['supply_contrib'])
late_supply = abs(component_analysis['2010s']['supply_contrib']) + abs(component_analysis['2020s']['supply_contrib'])
test_d = late_supply > early_supply
results['D'] = {
    'name': 'Component Contribution',
    'metric': ' | '.join(f"{k}: {v['driver']}" for k, v in component_analysis.items()),
    'target': 'Both contribute; supply increasingly important post-2005',
    'pass': test_d,
    'detail': component_analysis,
}

# --- Test E: OPEC deflation sensitivity ---
cesi_diff_pct = {y: (CESI[y] / CESI_official[y] - 1) * 100 for y in YEARS}
avg_diff_post88 = np.mean([cesi_diff_pct[y] for y in range(1988, 2024)])
max_diff = max(abs(cesi_diff_pct[y]) for y in YEARS)
# Deflation matters if average post-1988 difference > 5%
test_e = avg_diff_post88 > 5
results['E'] = {
    'name': 'OPEC Deflation Sensitivity',
    'metric': f'Avg post-1988 diff: {avg_diff_post88:.1f}%, Max: {max_diff:.1f}%',
    'target': 'Substantial difference (>5%) confirming deflation matters',
    'pass': test_e,
}

# Total score
score = sum(1 for v in results.values() if v['pass'])

# ================================================================
# DECADE SUMMARY TABLE
# ================================================================
decade_summary = {}
for name, yrs in decades.items():
    cesi_vals = [CESI[y] for y in yrs]
    wti_vals = [wti_real_2023[y] for y in yrs]
    decade_summary[name] = {
        'avg_cesi': np.mean(cesi_vals),
        'avg_wti_real': np.mean(wti_vals),
        'cesi_change_pct': (CESI[yrs[-1]] / CESI[yrs[0]] - 1) * 100,
        'wti_change_pct': (wti_real_2023[yrs[-1]] / wti_real_2023[yrs[0]] - 1) * 100,
        'rp_start': RP_deflated[yrs[0]],
        'rp_end': RP_deflated[yrs[-1]],
        'eroi_start': EROI[yrs[0]],
        'eroi_end': EROI[yrs[-1]],
        'avg_divergence': np.mean([Divergence[y] for y in yrs]),
    }

# ================================================================
# CHECK: Are thresholds ever breached historically?
# ================================================================
threshold_breaches = {
    'RP_below_20': [(y, RP_deflated[y]) for y in YEARS if RP_deflated[y] < 20],
    'EROI_below_7': [(y, EROI[y]) for y in YEARS if EROI[y] < 7],
}

# ================================================================
# EXPORT CSV
# ================================================================
csv_path = os.path.join(os.path.dirname(__file__), 'cesi_backtest_data.csv')
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Year', 'E_EJ', 'E_norm', 'Reserves_Official_Gbbl', 'Reserves_Deflated_Gbbl',
        'Production_Gbbl', 'RP_Official_yr', 'RP_Deflated_yr', 'RP_norm',
        'EROI', 'EROI_norm', 'WTI_Nominal', 'WTI_Real_2023', 'WTI_norm',
        'D', 'S', 'CESI', 'CESI_Official', 'Divergence',
        'GDP_const2015T', 'EnergyIntensity_EJ_per_T'
    ])
    for y in YEARS:
        writer.writerow([
            y, f'{E_ej[y]:.2f}', f'{E_norm[y]:.2f}',
            f'{oil_reserves_official[y]:.2f}', f'{oil_reserves_deflated[y]:.2f}',
            f'{oil_prod_gbbl[y]:.3f}',
            f'{RP_official[y]:.2f}', f'{RP_deflated[y]:.2f}', f'{RP_norm[y]:.2f}',
            f'{EROI[y]:.1f}', f'{EROI_norm[y]:.2f}',
            f'{wti_nominal[y]:.2f}', f'{wti_real_2023[y]:.2f}', f'{WTI_norm[y]:.2f}',
            f'{D[y]:.2f}', f'{S[y]:.2f}', f'{CESI[y]:.2f}', f'{CESI_official[y]:.2f}',
            f'{Divergence[y]:.2f}',
            f'{world_gdp[y]:.2f}', f'{energy_intensity[y]:.4f}',
        ])

# ================================================================
# PLOTS — Three GitHub-ready figures
# ================================================================
import os
FIG_DIRS = [
    'C:/Users/OMU/Desktop/Energy/cesi/paper/figures',
    'C:/Users/OMU/Desktop/Energy/cesi/results/figures',
]
for d in FIG_DIRS:
    os.makedirs(d, exist_ok=True)

# Consistent palette across all three figures
PAL_CESI   = '#1F3A5F'   # navy
PAL_WTI    = '#D4A017'   # amber
PAL_DIV    = '#1F3A5F'   # navy (single dominant colour)
PAL_EROI   = '#EF6C00'   # orange
PAL_RP     = '#C62828'   # red
PAL_DEMAND = '#1565C0'   # blue

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.edgecolor': '#333333',
    'axes.linewidth': 1.0,
    'axes.labelcolor': '#111111',
    'xtick.color': '#111111',
    'ytick.color': '#111111',
})


def _save(fig, name, dpi=300):
    for d in FIG_DIRS:
        fig.savefig(f'{d}/{name}.png', dpi=dpi, bbox_inches='tight',
                    pad_inches=0.15, facecolor='white')


# ── Figure 1 (hero): CESI vs WTI — both normalised, single axis ──
PAL_CESI_HERO = '#0B3D91'   # deep blue
PAL_WTI_HERO  = '#E65100'   # strong orange

fig1, ax = plt.subplots(figsize=(13, 7.2))
fig1.patch.set_facecolor('white')
ax.set_facecolor('white')

cesi_series = [CESI[y]    for y in YEARS]
wti_series  = [WTI_norm[y] for y in YEARS]

# Post-2005 divergence highlight
ax.axvspan(2005, 2023, color='#FFE0B2', alpha=0.35, zorder=0)

ax.plot(YEARS, cesi_series, color=PAL_CESI_HERO, linewidth=4.0,
        label='CESI (energy stress)', zorder=5)
ax.plot(YEARS, wti_series, color=PAL_WTI_HERO, linewidth=4.0,
        label='WTI real oil price', zorder=4)

# Annotation for divergence era
y_top = max(max(cesi_series), max(wti_series)) * 1.02
ax.annotate('Post-2005 divergence:\nstress keeps rising as\noil prices cycle',
            xy=(2014, (CESI[2014] + WTI_norm[2014]) / 2),
            xytext=(2007, y_top * 0.78),
            fontsize=14, color='#5D4037', fontweight='bold',
            ha='left', va='top',
            arrowprops=dict(arrowstyle='->', color='#5D4037', lw=1.5))

ax.set_title('Energy Stress Rising Despite Oil Price Cycles',
             fontsize=22, fontweight='bold', loc='left', pad=16, color='#0B0B0B')
ax.set_ylabel('Index (1980 = 100)', fontsize=16, fontweight='bold')
ax.set_xlabel('Year', fontsize=16, fontweight='bold')
ax.set_xlim(1980, 2023)
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.tick_params(axis='both', labelsize=14)
ax.grid(True, which='major', axis='y', alpha=0.22, linewidth=0.8)
for spine in ('top', 'right'):
    ax.spines[spine].set_visible(False)
ax.legend(fontsize=15, loc='upper left', frameon=False)

fig1.tight_layout()
_save(fig1, 'CESI_vs_WTI', dpi=320)
plt.close(fig1)


# ── Figure 2: CESI–WTI Divergence ──────────────────────────────
fig2, ax = plt.subplots(figsize=(11, 5.5))
fig2.patch.set_facecolor('white')
ax.set_facecolor('white')

div_vals = [Divergence[y] for y in YEARS]
ax.fill_between(YEARS, 0, div_vals, color=PAL_DIV, alpha=0.18, linewidth=0)
ax.plot(YEARS, div_vals, color=PAL_DIV, linewidth=2.8)
ax.axhline(0, color='#333333', linewidth=1)

ax.set_title('CESI–WTI Divergence Over Time', fontsize=17,
             fontweight='bold', loc='left', pad=14, color='#111111')
ax.set_ylabel('CESI − WTI (normalised, 1980 = 100)', fontsize=13, fontweight='bold')
ax.set_xlim(1980, 2023)
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.tick_params(labelsize=11)
ax.grid(True, which='major', axis='y', alpha=0.18, linewidth=0.8)
for spine in ('top', 'right'):
    ax.spines[spine].set_visible(False)

fig2.tight_layout()
_save(fig2, 'CESI_WTI_divergence')
plt.close(fig2)


# ── Figure 3: CESI components ──────────────────────────────────
fig3, ax = plt.subplots(figsize=(11, 6))
fig3.patch.set_facecolor('white')
ax.set_facecolor('white')

ax.plot(YEARS, [EROI_norm[y] for y in YEARS], color=PAL_EROI, linewidth=3.0,
        label='EROI (supply quality)')
ax.plot(YEARS, [RP_norm[y]   for y in YEARS], color=PAL_RP,   linewidth=3.0,
        label='Reserves-to-production')
ax.plot(YEARS, [E_norm[y]    for y in YEARS], color=PAL_DEMAND, linewidth=3.0,
        label='Energy demand')
ax.axhline(100, color='#888888', linewidth=0.8, linestyle='--', alpha=0.6)

ax.set_title('Decomposition of Energy System Stress', fontsize=17,
             fontweight='bold', loc='left', pad=14, color='#111111')
ax.set_ylabel('Component (1980 = 100)', fontsize=13, fontweight='bold')
ax.set_xlim(1980, 2023)
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.tick_params(labelsize=11)
ax.grid(True, which='major', axis='y', alpha=0.18, linewidth=0.8)
for spine in ('top', 'right'):
    ax.spines[spine].set_visible(False)
ax.legend(fontsize=11, loc='upper left', frameon=False)

fig3.tight_layout()
_save(fig3, 'CESI_decomposition')
plt.close(fig3)

print('Saved: CESI_vs_WTI.png, CESI_WTI_divergence.png, CESI_decomposition.png')


# ================================================================
# LEGACY 4-panel dashboard (kept for internal validation records)
# ================================================================
fig = plt.figure(figsize=(20, 24))
gs = fig.add_gridspec(5, 1, height_ratios=[1.5, 1, 1, 0.9, 0.05], hspace=0.32)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax3 = fig.add_subplot(gs[2])
ax4 = fig.add_subplot(gs[3])
ax_footer = fig.add_subplot(gs[4])
ax_footer.axis('off')

# Colours
C_CESI = '#0d47a1'
C_WTI = '#e65100'
C_DEMAND = '#1565c0'
C_RP = '#c62828'
C_EROI = '#ef6c00'
C_GOLD = '#d4a017'
C_ALARM = '#c0392b'
C_POS = '#ffcdd2'
C_NEG = '#bbdefb'
GREY = '#78909c'

# ── PANEL 1: CESI vs WTI ──
ax1.set_title('CESI vs WTI Real Oil Price (1980 = 100)', fontsize=15, fontweight='bold', loc='left')

ax1.plot(YEARS, [CESI[y] for y in YEARS], color=C_CESI, linewidth=3,
         label=f'CESI (Structural Energy Stress)', zorder=10)

ax1_r = ax1.twinx()
ax1_r.plot(YEARS, [wti_real_2023[y] for y in YEARS], color=C_WTI, linewidth=2, alpha=0.8,
           label='WTI Real (2023 USD/bbl)')
ax1_r.set_ylabel('WTI Real Price (2023 USD/bbl)', fontsize=12, fontweight='bold', color=C_WTI)
ax1_r.tick_params(axis='y', labelcolor=C_WTI)

# Stress thresholds
ax1.axhline(y=200, color=C_GOLD, linewidth=1.2, linestyle='--', alpha=0.5)
ax1.axhline(y=400, color=C_ALARM, linewidth=1.2, linestyle='--', alpha=0.5)
ax1.text(1981, 207, 'ELEVATED STRESS (200)', fontsize=8.5, color=C_GOLD,
         fontweight='bold', alpha=0.7)
ax1.text(1981, 407, 'CRITICAL STRESS (400)', fontsize=8.5, color=C_ALARM,
         fontweight='bold', alpha=0.7)

# Score badge
score_color = '#2e7d32' if score >= 4 else ('#f57f17' if score >= 3 else '#c62828')
ax1.text(0.98, 0.97, f'VALIDATION SCORE: {score}/5',
         transform=ax1.transAxes, fontsize=13, fontweight='bold',
         va='top', ha='right', color='white',
         bbox=dict(boxstyle='round,pad=0.5', facecolor=score_color, alpha=0.9))

# Key divergence annotation
ax1.annotate('Structural divergence\nbegins ~2005',
             xy=(2005, CESI[2005]), xytext=(1995, CESI[2005] + 80),
             fontsize=9, color=GREY,
             arrowprops=dict(arrowstyle='->', color=GREY, lw=1.2))

ax1.set_ylabel('CESI (1980 = 100)', fontsize=12, fontweight='bold', color=C_CESI)
ax1.tick_params(axis='y', labelcolor=C_CESI)
ax1.set_xlim(1980, 2023)
ax1.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax1.grid(True, alpha=0.2)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_r.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=10, loc='upper left',
           framealpha=0.9, edgecolor='gray')

# ── PANEL 2: CESI Components ──
ax2.set_title('CESI Components (all normalised 1980 = 100)', fontsize=15, fontweight='bold', loc='left')

ax2.plot(YEARS, [E_norm[y] for y in YEARS], color=C_DEMAND, linewidth=2.5,
         label='Energy Consumption D (demand)', zorder=10)
ax2.plot(YEARS, [RP_norm[y] for y in YEARS], color=C_RP, linewidth=2.5,
         label='R/P Ratio deflated (supply)', zorder=10)
ax2.plot(YEARS, [EROI_norm[y] for y in YEARS], color=C_EROI, linewidth=2.5,
         label='EROI step function (supply quality)', zorder=10)
ax2.plot(YEARS, [S[y] for y in YEARS], color='#4a148c', linewidth=2, linestyle='--',
         label='Combined Supply S', alpha=0.7)

# EROI step changes - mark with dots at actual data points
for bp in EROI_BREAKPOINTS:
    ax2.plot(bp, EROI_norm[bp], 'o', color=C_EROI, markersize=6, zorder=11)

ax2.axhline(y=100, color=GREY, linewidth=0.8, linestyle='-', alpha=0.3)
ax2.set_ylabel('Normalised (1980 = 100)', fontsize=12, fontweight='bold')
ax2.set_xlim(1980, 2023)
ax2.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax2.grid(True, alpha=0.2)
ax2.legend(fontsize=9.5, loc='upper left', framealpha=0.9, edgecolor='gray')

# Annotation: EROI step function
ax2.annotate('Step function: each year uses\nmost recent published EROI\n(dots = actual data points)',
             xy=(2015, EROI_norm[2015]), xytext=(2000, 45),
             fontsize=8.5, color=C_EROI,
             arrowprops=dict(arrowstyle='->', color=C_EROI, lw=1))

# ── PANEL 3: CESI - WTI Divergence ──
ax3.set_title('CESI - WTI Divergence (Mispricing Signal)', fontsize=15, fontweight='bold', loc='left')

div_vals = [Divergence[y] for y in YEARS]
ax3.fill_between(YEARS, 0, div_vals,
                 where=[d >= 0 for d in div_vals],
                 color=C_POS, alpha=0.6, label='CESI > WTI (stress underpriced)')
ax3.fill_between(YEARS, 0, div_vals,
                 where=[d < 0 for d in div_vals],
                 color=C_NEG, alpha=0.6, label='WTI > CESI (price above stress)')
ax3.plot(YEARS, div_vals, color=C_CESI, linewidth=2, zorder=10)
ax3.axhline(y=0, color='black', linewidth=1)

ax3.set_ylabel('Divergence (CESI - WTI normalised)', fontsize=12, fontweight='bold')
ax3.set_xlim(1980, 2023)
ax3.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax3.grid(True, alpha=0.2)
ax3.legend(fontsize=9.5, loc='upper left', framealpha=0.9, edgecolor='gray')

# ── PANEL 4: Decade Summary Table ──
ax4.axis('off')
ax4.set_title('Decade Summary Statistics', fontsize=15, fontweight='bold', loc='left', pad=15)

col_labels = ['Decade', 'Avg CESI', 'Avg WTI\nReal $',
              'CESI\n% Chg', 'WTI\n% Chg',
              'R/P\nStart', 'R/P\nEnd',
              'EROI\nStart', 'EROI\nEnd',
              'Avg\nDivergence']
table_data = []
for name, ds in decade_summary.items():
    table_data.append([
        name,
        f'{ds["avg_cesi"]:.0f}',
        f'${ds["avg_wti_real"]:.0f}',
        f'{ds["cesi_change_pct"]:+.0f}%',
        f'{ds["wti_change_pct"]:+.0f}%',
        f'{ds["rp_start"]:.0f}',
        f'{ds["rp_end"]:.0f}',
        f'{ds["eroi_start"]:.0f}',
        f'{ds["eroi_end"]:.0f}',
        f'{ds["avg_divergence"]:+.0f}',
    ])

table = ax4.table(cellText=table_data, colLabels=col_labels,
                   loc='center', cellLoc='center',
                   colColours=['#e3f2fd'] * len(col_labels))
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.8)

# Style header
for j in range(len(col_labels)):
    table[0, j].set_facecolor('#1565c0')
    table[0, j].set_text_props(color='white', fontweight='bold')

# ── VALIDATION RESULTS BOX ──
validation_text = 'STRUCTURAL VALIDATION TESTS\n'
validation_text += '=' * 45 + '\n'
for key in ['A', 'B', 'C', 'D', 'E']:
    r = results[key]
    status = 'PASS' if r['pass'] else 'FAIL'
    icon = '[+]' if r['pass'] else '[-]'
    validation_text += f"{icon} Test {key}: {r['name']}\n"
    validation_text += f"    {r['metric']}\n"
    validation_text += f"    Target: {r['target']}\n"
    validation_text += f"    Result: {status}\n\n"

validation_text += f"TOTAL SCORE: {score}/5\n"
if score == 5:
    validation_text += "Architecture fully validated structurally"
elif score == 4:
    validation_text += "Strong validation, investigate failure"
elif score == 3:
    validation_text += "Partial validation, methodology review"
else:
    validation_text += "FUNDAMENTAL ARCHITECTURE PROBLEM"

fig.text(0.02, 0.005, validation_text, fontsize=8, fontfamily='monospace',
         va='bottom', ha='left',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#fafafa', edgecolor='gray', alpha=0.95))

# ── THRESHOLD FLAG ──
threshold_text = 'THRESHOLD STATUS (Historical):\n'
if threshold_breaches['RP_below_20']:
    threshold_text += f"  R/P < 20yr: BREACHED in {', '.join(str(y) for y, _ in threshold_breaches['RP_below_20'])}\n"
else:
    threshold_text += "  R/P < 20yr: Never breached (lowest: "
    threshold_text += f"{min(RP_deflated[y] for y in YEARS):.1f}yr in {min(YEARS, key=lambda y: RP_deflated[y])})\n"
if threshold_breaches['EROI_below_7']:
    threshold_text += f"  EROI < 7: BREACHED in {', '.join(str(y) for y, _ in threshold_breaches['EROI_below_7'])}\n"
else:
    threshold_text += f"  EROI < 7: Never breached (lowest: {min(EROI[y] for y in YEARS):.0f} in {max(YEARS)})\n"
threshold_text += "  Nonlinear acceleration NOT yet validated empirically"

fig.text(0.98, 0.005, threshold_text, fontsize=8, fontfamily='monospace',
         va='bottom', ha='right',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#fff8e1', edgecolor='#f57f17', alpha=0.95))

# ── HONEST LIMITATIONS ──
limitations_text = (
    'HONEST LIMITATIONS: '
    '(1) EROI data is sparse -- step function is approximation not measurement. '
    '(2) Annual frequency cannot capture shock response (Test 2 required). '
    '(3) Single demand variable understates demand complexity but avoids proxy contamination. '
    '(4) Reserve data quality inherently uncertain even after OPEC deflation. '
    '(5) CESI has never been live-tested -- this is retrospective application only.'
)
fig.text(0.5, 0.15, limitations_text, fontsize=7.5, ha='center', color='gray',
         style='italic', wrap=True,
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#f5f5f5', edgecolor='#bdbdbd', alpha=0.8))

# ── TITLE ──
fig.suptitle(
    'CESI BACKTEST -- TEST 1: ANNUAL STRUCTURAL VALIDATION\n'
    'Civilisational Energy Stress Index  |  1980-2023  |  No interpolation  |  Annual data only',
    fontsize=18, fontweight='bold', y=0.995)

# ── SOURCES ──
source_text = (
    'Sources: Energy Institute Statistical Review via OWID (energy)  |  '
    'US EIA via IndexMundi (reserves, production)  |  '
    'Hall/Brandt/Court & Fizaine/Murphy (EROI)  |  '
    'FRED WTISPLC/BLS CPI-U (WTI, inflation)  |  '
    'World Bank NY.GDP.MKTP.KD (GDP)  |  '
    'Salameh/Simmons/Laherrere (OPEC deflation)'
)
fig.text(0.5, 0.125, source_text, fontsize=7.5, ha='center', color='gray', style='italic')

fig.text(0.5, 0.112,
         'TEST 1 OF 2: Structural validation only. Not shock response. Not forward projection. Not investment advice.',
         fontsize=8, ha='center', color=C_ALARM, fontweight='bold')

plt.savefig('C:/Users/OMU/Desktop/Energy/CESI_backtest.png', dpi=200, bbox_inches='tight')
plt.savefig('C:/Users/OMU/Desktop/Energy/CESI_backtest.svg', bbox_inches='tight')
print("Saved: CESI_backtest.png, .svg, and cesi_backtest_data.csv")

# ================================================================
# CONSOLE OUTPUT
# ================================================================
print(f"\n{'='*60}")
print(f"CESI BACKTEST -- TEST 1 RESULTS")
print(f"{'='*60}")

print(f"\n--- CESI Annual Values ---")
for y in YEARS:
    marker = ''
    if y in trough_years:
        marker = ' <-- TROUGH'
    print(f"  {y}: CESI={CESI[y]:7.1f}  D={D[y]:6.1f}  S={S[y]:6.1f}  "
          f"RP_defl={RP_deflated[y]:5.1f}yr  EROI={EROI[y]:4.1f}  "
          f"WTI_real=${wti_real_2023[y]:6.1f}  Div={Divergence[y]:+7.1f}{marker}")

print(f"\n--- Validation Tests ---")
for key in ['A', 'B', 'C', 'D', 'E']:
    r = results[key]
    status = 'PASS' if r['pass'] else 'FAIL'
    print(f"  Test {key} ({r['name']}): {status}")
    print(f"    {r['metric']}")

print(f"\n--- SCORE: {score}/5 ---")

print(f"\n--- Decade Summary ---")
for name, ds in decade_summary.items():
    ca = component_analysis[name]
    print(f"  {name}: CESI avg={ds['avg_cesi']:.0f}, "
          f"WTI avg=${ds['avg_wti_real']:.0f}, "
          f"Driver={ca['driver']}, "
          f"D_contrib={ca['demand_contrib']:+.1f}, "
          f"S_contrib={ca['supply_contrib']:+.1f}")

print(f"\n--- Threshold Status ---")
print(f"  RP < 20yr breaches: {len(threshold_breaches['RP_below_20'])}")
print(f"  EROI < 7 breaches: {len(threshold_breaches['EROI_below_7'])}")
print(f"  Nonlinear acceleration empirically validated: NO")

print(f"\n--- OPEC Deflation Sensitivity ---")
print(f"  Avg CESI diff (deflated vs official) post-1988: {avg_diff_post88:.1f}%")
print(f"  Max diff: {max_diff:.1f}%")
for y in [1987, 1988, 2000, 2010, 2020, 2023]:
    print(f"    {y}: Deflated={CESI[y]:.1f}  Official={CESI_official[y]:.1f}  "
          f"Diff={cesi_diff_pct[y]:+.1f}%")
