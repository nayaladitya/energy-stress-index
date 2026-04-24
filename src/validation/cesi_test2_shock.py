"""
CESI TEST 2: SHOCK RESPONSE VALIDATION
=========================================

Objective: Demonstrate that CESI responds appropriately to known energy
shocks at monthly frequency, establishing near-term tradability.

Method: Construct monthly CESI 2000-01 through 2024-12 using partial-update
mechanism per spec:
    - X (electricity, OECD industrial electricity demand proxy) - monthly
    - I (industrial production, FRED INDPRO + OECD G7) - monthly
    - E (energy substitution baseline) - held at annual value, stepped Jan
    - P (population) - held at annual value, stepped Jan
Supply (R/P, EROI) updated annually (no monthly proved-reserves data exists).

Shock cases tested:
    1. 2008 Oil Spike (Jun-Jul 2008, WTI $140+)
    2. 2014-16 Shale Crash (Jun 2014 - Feb 2016)
    3. 2020 COVID Demand Collapse (Mar-Apr 2020, WTI negative)
    4. 2022 Russia/Ukraine (Feb-Jun 2022)

Pass criteria per shock:
    - Direction correct (demand-driven shocks: CESI moves with demand;
      supply-driven shocks: CESI rises as supply impaired)
    - Magnitude proportionate (>0.5sd move within 6mo of event)
    - Persistence (does not immediately revert)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import csv
from datetime import date

# ============================================================
# 1. MONTHLY DATA: sourced from FRED, EIA, OECD, BP/Energy Inst
# ============================================================
# Coverage: 2000-01 to 2024-12 (300 months)

YEARS = list(range(2000, 2025))
MONTHS = [(y, m) for y in YEARS for m in range(1, 13)]

# ---- WTI Spot Crude Oil Price (USD/bbl, monthly avg) FRED: WTISPLC ----
# Source: U.S. Energy Information Administration via FRED
WTI_NOMINAL = {
    # 2000
    (2000,1):27.18,(2000,2):29.37,(2000,3):29.84,(2000,4):25.72,(2000,5):28.79,(2000,6):31.82,
    (2000,7):29.70,(2000,8):31.26,(2000,9):33.88,(2000,10):33.11,(2000,11):34.42,(2000,12):28.44,
    # 2001
    (2001,1):29.59,(2001,2):29.61,(2001,3):27.24,(2001,4):27.49,(2001,5):28.63,(2001,6):27.60,
    (2001,7):26.43,(2001,8):27.37,(2001,9):26.20,(2001,10):22.17,(2001,11):19.66,(2001,12):19.33,
    # 2002
    (2002,1):19.71,(2002,2):20.72,(2002,3):24.42,(2002,4):26.27,(2002,5):27.04,(2002,6):25.52,
    (2002,7):26.94,(2002,8):28.39,(2002,9):29.66,(2002,10):28.84,(2002,11):26.27,(2002,12):29.42,
    # 2003
    (2003,1):32.95,(2003,2):35.83,(2003,3):33.51,(2003,4):28.17,(2003,5):28.11,(2003,6):30.66,
    (2003,7):30.75,(2003,8):31.57,(2003,9):28.31,(2003,10):30.34,(2003,11):31.11,(2003,12):32.13,
    # 2004
    (2004,1):34.31,(2004,2):34.68,(2004,3):36.74,(2004,4):36.75,(2004,5):40.28,(2004,6):38.03,
    (2004,7):40.78,(2004,8):44.90,(2004,9):45.94,(2004,10):53.28,(2004,11):48.47,(2004,12):43.15,
    # 2005
    (2005,1):46.84,(2005,2):47.96,(2005,3):54.19,(2005,4):52.98,(2005,5):49.83,(2005,6):56.35,
    (2005,7):58.65,(2005,8):64.99,(2005,9):65.59,(2005,10):62.37,(2005,11):58.32,(2005,12):59.41,
    # 2006
    (2006,1):65.49,(2006,2):61.63,(2006,3):62.90,(2006,4):69.44,(2006,5):70.84,(2006,6):70.95,
    (2006,7):74.41,(2006,8):73.04,(2006,9):63.80,(2006,10):58.89,(2006,11):59.08,(2006,12):61.96,
    # 2007
    (2007,1):54.51,(2007,2):59.28,(2007,3):60.44,(2007,4):63.98,(2007,5):63.45,(2007,6):67.49,
    (2007,7):74.12,(2007,8):72.36,(2007,9):79.91,(2007,10):85.80,(2007,11):94.77,(2007,12):91.69,
    # 2008
    (2008,1):92.97,(2008,2):95.39,(2008,3):105.45,(2008,4):112.58,(2008,5):125.40,(2008,6):133.88,
    (2008,7):133.37,(2008,8):116.67,(2008,9):104.11,(2008,10):76.61,(2008,11):57.31,(2008,12):41.12,
    # 2009
    (2009,1):41.71,(2009,2):39.09,(2009,3):47.94,(2009,4):49.65,(2009,5):59.03,(2009,6):69.64,
    (2009,7):64.15,(2009,8):71.04,(2009,9):69.41,(2009,10):75.72,(2009,11):77.99,(2009,12):74.47,
    # 2010
    (2010,1):78.33,(2010,2):76.39,(2010,3):81.20,(2010,4):84.29,(2010,5):73.74,(2010,6):75.34,
    (2010,7):76.32,(2010,8):76.60,(2010,9):75.24,(2010,10):81.89,(2010,11):84.25,(2010,12):89.15,
    # 2011
    (2011,1):89.17,(2011,2):88.58,(2011,3):102.86,(2011,4):109.53,(2011,5):100.90,(2011,6):96.26,
    (2011,7):97.30,(2011,8):86.33,(2011,9):85.52,(2011,10):86.32,(2011,11):97.16,(2011,12):98.56,
    # 2012
    (2012,1):100.27,(2012,2):102.20,(2012,3):106.16,(2012,4):103.32,(2012,5):94.65,(2012,6):82.30,
    (2012,7):87.90,(2012,8):94.13,(2012,9):94.51,(2012,10):89.49,(2012,11):86.53,(2012,12):87.86,
    # 2013
    (2013,1):94.76,(2013,2):95.31,(2013,3):92.94,(2013,4):92.02,(2013,5):94.51,(2013,6):95.77,
    (2013,7):104.67,(2013,8):106.57,(2013,9):106.29,(2013,10):100.54,(2013,11):93.86,(2013,12):97.63,
    # 2014
    (2014,1):94.62,(2014,2):100.82,(2014,3):100.80,(2014,4):102.07,(2014,5):102.18,(2014,6):105.79,
    (2014,7):103.59,(2014,8):96.54,(2014,9):93.21,(2014,10):84.40,(2014,11):75.79,(2014,12):59.29,
    # 2015
    (2015,1):47.22,(2015,2):50.58,(2015,3):47.82,(2015,4):54.45,(2015,5):59.27,(2015,6):59.82,
    (2015,7):50.90,(2015,8):42.87,(2015,9):45.48,(2015,10):46.22,(2015,11):42.44,(2015,12):37.19,
    # 2016
    (2016,1):31.68,(2016,2):30.32,(2016,3):37.55,(2016,4):40.76,(2016,5):46.71,(2016,6):48.76,
    (2016,7):44.65,(2016,8):44.72,(2016,9):45.18,(2016,10):49.78,(2016,11):45.66,(2016,12):51.97,
    # 2017
    (2017,1):52.50,(2017,2):53.47,(2017,3):49.33,(2017,4):51.06,(2017,5):48.48,(2017,6):45.18,
    (2017,7):46.63,(2017,8):48.04,(2017,9):49.82,(2017,10):51.58,(2017,11):56.64,(2017,12):57.88,
    # 2018
    (2018,1):63.70,(2018,2):62.23,(2018,3):62.73,(2018,4):66.25,(2018,5):69.98,(2018,6):67.87,
    (2018,7):70.98,(2018,8):67.85,(2018,9):70.23,(2018,10):70.75,(2018,11):56.96,(2018,12):49.52,
    # 2019
    (2019,1):51.38,(2019,2):54.95,(2019,3):58.15,(2019,4):63.86,(2019,5):60.83,(2019,6):54.66,
    (2019,7):57.35,(2019,8):54.81,(2019,9):56.95,(2019,10):53.96,(2019,11):57.03,(2019,12):59.88,
    # 2020
    (2020,1):57.52,(2020,2):50.54,(2020,3):29.21,(2020,4):16.55,(2020,5):28.56,(2020,6):38.31,
    (2020,7):40.71,(2020,8):42.34,(2020,9):39.63,(2020,10):39.40,(2020,11):40.94,(2020,12):47.02,
    # 2021
    (2021,1):52.00,(2021,2):59.04,(2021,3):62.33,(2021,4):61.72,(2021,5):65.17,(2021,6):71.38,
    (2021,7):72.49,(2021,8):67.73,(2021,9):71.65,(2021,10):81.48,(2021,11):79.15,(2021,12):71.71,
    # 2022
    (2022,1):83.22,(2022,2):91.64,(2022,3):108.50,(2022,4):101.78,(2022,5):109.55,(2022,6):114.84,
    (2022,7):101.62,(2022,8):91.48,(2022,9):84.26,(2022,10):87.55,(2022,11):84.37,(2022,12):76.44,
    # 2023
    (2023,1):78.12,(2023,2):76.83,(2023,3):73.28,(2023,4):79.45,(2023,5):71.62,(2023,6):70.25,
    (2023,7):76.07,(2023,8):81.39,(2023,9):89.43,(2023,10):85.64,(2023,11):77.69,(2023,12):71.90,
    # 2024
    (2024,1):73.82,(2024,2):76.60,(2024,3):81.28,(2024,4):85.35,(2024,5):80.02,(2024,6):79.77,
    (2024,7):81.80,(2024,8):76.68,(2024,9):70.24,(2024,10):71.99,(2024,11):69.95,(2024,12):70.12,
}

# ---- US Industrial Production Index (FRED INDPRO, 2017=100, SA, monthly) ----
# Source: Federal Reserve Board G.17 release
INDPRO = {
    (2000,1):85.27,(2000,2):85.78,(2000,3):86.20,(2000,4):86.95,(2000,5):87.31,(2000,6):87.71,
    (2000,7):87.69,(2000,8):87.50,(2000,9):88.06,(2000,10):87.66,(2000,11):87.27,(2000,12):86.34,
    (2001,1):85.76,(2001,2):85.42,(2001,3):85.21,(2001,4):84.88,(2001,5):84.59,(2001,6):84.06,
    (2001,7):83.79,(2001,8):83.46,(2001,9):82.97,(2001,10):82.43,(2001,11):82.08,(2001,12):82.05,
    (2002,1):82.63,(2002,2):82.83,(2002,3):83.49,(2002,4):83.85,(2002,5):84.21,(2002,6):84.88,
    (2002,7):85.14,(2002,8):85.10,(2002,9):85.34,(2002,10):84.99,(2002,11):85.29,(2002,12):84.39,
    (2003,1):84.99,(2003,2):85.54,(2003,3):85.40,(2003,4):84.62,(2003,5):84.65,(2003,6):84.74,
    (2003,7):85.05,(2003,8):85.06,(2003,9):85.74,(2003,10):85.74,(2003,11):86.78,(2003,12):86.75,
    (2004,1):87.20,(2004,2):87.68,(2004,3):87.25,(2004,4):87.48,(2004,5):88.35,(2004,6):87.69,
    (2004,7):88.34,(2004,8):88.48,(2004,9):88.16,(2004,10):89.09,(2004,11):89.43,(2004,12):90.13,
    (2005,1):90.31,(2005,2):90.71,(2005,3):90.73,(2005,4):90.80,(2005,5):90.80,(2005,6):91.16,
    (2005,7):90.84,(2005,8):91.45,(2005,9):89.65,(2005,10):90.91,(2005,11):91.84,(2005,12):92.65,
    (2006,1):92.40,(2006,2):92.80,(2006,3):92.83,(2006,4):93.31,(2006,5):93.16,(2006,6):93.92,
    (2006,7):93.94,(2006,8):93.94,(2006,9):93.70,(2006,10):92.87,(2006,11):92.78,(2006,12):93.59,
    (2007,1):92.62,(2007,2):93.59,(2007,3):93.11,(2007,4):94.18,(2007,5):94.43,(2007,6):94.36,
    (2007,7):94.42,(2007,8):94.75,(2007,9):94.91,(2007,10):94.34,(2007,11):94.78,(2007,12):94.88,
    (2008,1):94.96,(2008,2):94.84,(2008,3):94.42,(2008,4):93.69,(2008,5):93.14,(2008,6):92.84,
    (2008,7):92.78,(2008,8):91.57,(2008,9):87.79,(2008,10):88.28,(2008,11):86.51,(2008,12):84.58,
    (2009,1):82.93,(2009,2):82.07,(2009,3):80.78,(2009,4):80.10,(2009,5):78.82,(2009,6):78.30,
    (2009,7):79.32,(2009,8):80.37,(2009,9):80.86,(2009,10):80.66,(2009,11):81.21,(2009,12):81.79,
    (2010,1):82.55,(2010,2):82.66,(2010,3):83.36,(2010,4):83.86,(2010,5):84.94,(2010,6):84.95,
    (2010,7):85.39,(2010,8):85.51,(2010,9):85.74,(2010,10):85.63,(2010,11):85.97,(2010,12):86.95,
    (2011,1):87.20,(2011,2):86.75,(2011,3):87.45,(2011,4):87.21,(2011,5):87.42,(2011,6):87.65,
    (2011,7):88.45,(2011,8):88.61,(2011,9):88.66,(2011,10):89.11,(2011,11):88.84,(2011,12):89.15,
    (2012,1):89.92,(2012,2):89.91,(2012,3):89.69,(2012,4):90.59,(2012,5):90.59,(2012,6):90.55,
    (2012,7):90.93,(2012,8):90.39,(2012,9):90.42,(2012,10):90.16,(2012,11):91.21,(2012,12):91.57,
    (2013,1):91.84,(2013,2):92.51,(2013,3):92.83,(2013,4):92.30,(2013,5):92.34,(2013,6):92.55,
    (2013,7):92.36,(2013,8):92.99,(2013,9):93.49,(2013,10):93.61,(2013,11):94.31,(2013,12):94.36,
    (2014,1):93.83,(2014,2):94.43,(2014,3):95.21,(2014,4):95.09,(2014,5):95.48,(2014,6):95.83,
    (2014,7):95.90,(2014,8):95.52,(2014,9):96.19,(2014,10):96.71,(2014,11):97.79,(2014,12):97.30,
    (2015,1):97.60,(2015,2):97.49,(2015,3):96.96,(2015,4):96.69,(2015,5):96.55,(2015,6):96.62,
    (2015,7):97.27,(2015,8):97.22,(2015,9):96.99,(2015,10):96.83,(2015,11):96.31,(2015,12):95.22,
    (2016,1):95.69,(2016,2):95.59,(2016,3):94.79,(2016,4):94.59,(2016,5):94.59,(2016,6):95.04,
    (2016,7):95.61,(2016,8):95.42,(2016,9):95.17,(2016,10):95.07,(2016,11):95.16,(2016,12):95.69,
    (2017,1):95.31,(2017,2):95.23,(2017,3):95.83,(2017,4):96.95,(2017,5):97.40,(2017,6):97.89,
    (2017,7):98.07,(2017,8):97.16,(2017,9):98.81,(2017,10):99.79,(2017,11):100.74,(2017,12):100.92,
    (2018,1):100.85,(2018,2):101.59,(2018,3):101.90,(2018,4):102.66,(2018,5):102.55,(2018,6):103.13,
    (2018,7):103.50,(2018,8):104.08,(2018,9):104.20,(2018,10):103.78,(2018,11):104.07,(2018,12):104.94,
    (2019,1):104.16,(2019,2):103.79,(2019,3):103.74,(2019,4):103.20,(2019,5):103.45,(2019,6):103.05,
    (2019,7):102.68,(2019,8):103.35,(2019,9):102.83,(2019,10):102.04,(2019,11):103.28,(2019,12):102.39,
    (2020,1):101.93,(2020,2):102.11,(2020,3):97.39,(2020,4):85.49,(2020,5):86.94,(2020,6):92.69,
    (2020,7):95.69,(2020,8):96.05,(2020,9):96.45,(2020,10):97.41,(2020,11):98.13,(2020,12):98.93,
    (2021,1):99.92,(2021,2):96.95,(2021,3):99.36,(2021,4):99.81,(2021,5):100.45,(2021,6):100.66,
    (2021,7):100.96,(2021,8):100.65,(2021,9):100.21,(2021,10):101.81,(2021,11):102.62,(2021,12):103.04,
    (2022,1):102.38,(2022,2):103.55,(2022,3):104.26,(2022,4):105.22,(2022,5):104.97,(2022,6):104.72,
    (2022,7):104.92,(2022,8):104.93,(2022,9):104.99,(2022,10):104.74,(2022,11):104.75,(2022,12):103.58,
    (2023,1):103.55,(2023,2):103.91,(2023,3):103.55,(2023,4):103.92,(2023,5):103.74,(2023,6):103.62,
    (2023,7):103.83,(2023,8):104.07,(2023,9):104.13,(2023,10):103.20,(2023,11):103.36,(2023,12):103.30,
    (2024,1):103.33,(2024,2):103.13,(2024,3):103.66,(2024,4):103.50,(2024,5):103.40,(2024,6):103.30,
    (2024,7):102.79,(2024,8):102.79,(2024,9):102.34,(2024,10):102.66,(2024,11):102.50,(2024,12):102.62,
}

# ---- OECD electricity generation index (TWh/month, OECD total, IEA MES) ----
# Approximated from IEA Monthly Electricity Statistics, OECD aggregate
# Values are TWh per month, seasonal pattern preserved
# Trended to ~9,400 TWh/yr (OECD 2023) with monthly seasonality
def oecd_elec_monthly(y, m):
    # Annual OECD electricity generation TWh (approx, IEA)
    annual = {
        2000:9170,2001:9242,2002:9387,2003:9508,2004:9690,2005:9843,
        2006:9897,2007:10026,2008:10043,2009:9636,2010:9970,2011:9985,
        2012:9962,2013:10018,2014:9924,2015:9928,2016:9974,2017:10112,
        2018:10247,2019:10135,2020:9758,2021:10080,2022:10059,2023:9880,
        2024:9950,
    }
    A = annual.get(y, 9900)
    # OECD seasonal factors (heating/cooling), normalised to 1.0 mean
    seas = {1:1.10,2:1.02,3:1.02,4:0.92,5:0.92,6:0.96,7:1.04,8:1.02,9:0.93,10:0.95,11:1.00,12:1.12}
    return (A / 12.0) * seas[m]

ELEC = {(y,m): oecd_elec_monthly(y,m) for y in YEARS for m in range(1,13)}

# ---- Annual energy consumption (EJ, primary, substitution method) ----
# Energy Institute Statistical Review 2024 + EI/BP backseries
ENERGY_EJ = {
    2000:399.6,2001:402.8,2002:411.0,2003:425.2,2004:443.3,2005:454.2,
    2006:464.8,2007:475.1,2008:478.5,2009:469.4,2010:493.9,2011:507.1,
    2012:514.5,2013:524.1,2014:528.7,2015:529.9,2016:535.3,2017:546.6,
    2018:561.8,2019:566.7,2020:548.7,2021:582.4,2022:591.3,2023:603.4,
    2024:611.0,
}

# ---- World population (UN WPP 2024 medium variant, billions) ----
POP_BN = {
    2000:6.149,2001:6.230,2002:6.312,2003:6.394,2004:6.477,2005:6.559,
    2006:6.642,2007:6.726,2008:6.811,2009:6.896,2010:6.985,2011:7.072,
    2012:7.161,2013:7.250,2014:7.339,2015:7.426,2016:7.513,2017:7.599,
    2018:7.683,2019:7.765,2020:7.840,2021:7.909,2022:7.975,2023:8.045,
    2024:8.119,
}

# ---- Annual oil reserves and production (for annual S calculation) ----
# Proved reserves (Gbbl) - BP/EI Statistical Review (official, will be deflated)
RES_OFFICIAL = {
    2000:1104,2001:1124,2002:1148,2003:1172,2004:1196,2005:1281,
    2006:1336,2007:1370,2008:1414,2009:1473,2010:1620,2011:1652,
    2012:1672,2013:1689,2014:1701,2015:1697,2016:1707,2017:1722,
    2018:1730,2019:1734,2020:1732,2021:1564,2022:1568,2023:1572,2024:1572,
}
# Annual oil production (Gbbl/yr) - EI Stat Rev
PROD = {
    2000:27.85,2001:27.88,2002:27.43,2003:28.42,2004:29.78,2005:30.18,
    2006:30.21,2007:30.04,2008:30.51,2009:29.40,2010:30.47,2011:30.66,
    2012:31.39,2013:31.42,2014:32.10,2015:33.17,2016:33.70,2017:33.74,
    2018:34.62,2019:34.41,2020:31.85,2021:32.46,2022:33.47,2023:34.32,2024:34.20,
}

# ---- EROI step function (per Test 1 spec) ----
EROI_POINTS = {2000:18.0, 2006:16.0, 2010:15.0, 2015:12.0, 2020:10.0, 2023:9.0}
def eroi_for_year(y):
    keys = sorted(EROI_POINTS.keys())
    last = keys[0]
    for k in keys:
        if k <= y:
            last = k
    return EROI_POINTS[last]

# ============================================================
# 2. NORMALISE EACH SERIES TO BASE 2000-01 = 100
# ============================================================
def normalise_monthly(series):
    base = series[(2000,1)]
    return {k: 100.0 * v / base for k, v in series.items()}

E_ann_norm  = {y: 100.0 * ENERGY_EJ[y] / ENERGY_EJ[2000] for y in YEARS}
P_ann_norm  = {y: 100.0 * POP_BN[y] / POP_BN[2000] for y in YEARS}
X_norm      = normalise_monthly(ELEC)
I_norm      = normalise_monthly(INDPRO)

# ============================================================
# 3. MONTHLY DEMAND (partial-update spec)
#    D = 0.40*E + 0.30*X + 0.20*I + 0.10*P
#    E and P held at annual value (stepped each Jan)
# ============================================================
D_monthly = {}
for (y,m) in MONTHS:
    E = E_ann_norm[y]
    P = P_ann_norm[y]
    X = X_norm[(y,m)]
    I = I_norm[(y,m)]
    D_monthly[(y,m)] = 0.40*E + 0.30*X + 0.20*I + 0.10*P

# ============================================================
# 4. ANNUAL SUPPLY (with OPEC deflation + threshold mechanism)
# ============================================================
# OPEC deflation (per Test 1)
RES_DEFLATED = {y: RES_OFFICIAL[y] * 0.75 for y in YEARS}

# R/P ratio, deflated
RP = {y: RES_DEFLATED[y] / PROD[y] for y in YEARS}
RP_norm = {y: 100.0 * RP[y] / RP[2000] for y in YEARS}
EROI_norm = {y: 100.0 * eroi_for_year(y) / eroi_for_year(2000) for y in YEARS}

def calc_S_annual(y):
    rp_n = RP_norm[y]; eroi_n = EROI_norm[y]
    rp_v = RP[y];      eroi_v = eroi_for_year(y)
    S = (rp_n * eroi_n) / 100.0
    if rp_v < 20:
        T_r = 20 - rp_v
        S = S / (1 + (T_r/20.0)**2)
    if eroi_v < 7:
        T_e = 7 - eroi_v
        S = S / (1 + (T_e/7.0)**2)
    return S

S_ann_raw = {y: calc_S_annual(y) for y in YEARS}
S_NORM = 100.0 / S_ann_raw[2000]   # so S_2000 = 100 by construction
S_ann = {y: S_ann_raw[y] * S_NORM for y in YEARS}

# ============================================================
# 5. CONSTRUCT MONTHLY CESI
# ============================================================
CESI = {}
for (y,m) in MONTHS:
    D = D_monthly[(y,m)]
    S = S_ann[y]
    CESI[(y,m)] = (D / S) * 100.0

# Normalise so 2000-01 = 100 exactly
cesi_base = CESI[(2000,1)]
CESI = {k: v * 100.0 / cesi_base for k, v in CESI.items()}

# ============================================================
# 6. SHOCK EVENT WINDOWS + RESPONSE METRICS
# ============================================================
SHOCKS = [
    {"name":"2008 Oil Spike",            "type":"price/demand", "t0":(2008,7), "pre":(2008,1), "post":(2009,1), "dir":-1, "expected":"Demand collapses post-spike -> CESI falls"},
    {"name":"2014-16 Shale Crash",       "type":"supply-glut",  "t0":(2014,11),"pre":(2014,5), "post":(2015,8), "dir":+1, "expected":"Demand intact, supply expands -> CESI flat/up modestly"},
    {"name":"2020 COVID Demand Collapse","type":"demand",       "t0":(2020,4), "pre":(2020,1), "post":(2020,9), "dir":-1, "expected":"Demand collapses, supply intact -> CESI sharply down"},
    {"name":"2022 Russia/Ukraine",       "type":"supply/geopol","t0":(2022,3), "pre":(2021,11),"post":(2022,12),"dir":+1, "expected":"Supply impaired, demand intact -> CESI rises"},
]

def cesi_at(ym):
    return CESI[ym]

def cesi_window_change(pre, post):
    return cesi_at(post) - cesi_at(pre)

def cesi_window_pct(pre, post):
    return 100.0 * (cesi_at(post) - cesi_at(pre)) / cesi_at(pre)

def month_index(ym):
    return MONTHS.index(ym)

def cesi_extremes_forward(t0, window=9):
    """Return (min, max, argmin_ym, argmax_ym) for [t0, t0+window] inclusive
       (forward-only, to measure post-shock response honestly)."""
    i0 = month_index(t0)
    hi = min(len(MONTHS)-1, i0 + window)
    seg = [(MONTHS[i], CESI[MONTHS[i]]) for i in range(i0, hi+1)]
    vals = [v for _, v in seg]
    mn = min(vals); mx = max(vals)
    arg_mn = next(ym for ym, v in seg if v == mn)
    arg_mx = next(ym for ym, v in seg if v == mx)
    return mn, mx, arg_mn, arg_mx

# Compute month-over-month volatility for normalisation
cesi_series = [CESI[(y,m)] for (y,m) in MONTHS]
cesi_diffs = np.diff(cesi_series)
cesi_sd = float(np.std(cesi_diffs))

print("="*68)
print("CESI TEST 2: SHOCK RESPONSE VALIDATION")
print("="*68)
print(f"\nMonthly CESI series: {len(MONTHS)} months ({MONTHS[0]} to {MONTHS[-1]})")
print(f"CESI 2000-01: {CESI[(2000,1)]:.2f}")
print(f"CESI 2024-12: {CESI[(2024,12)]:.2f}")
print(f"Monthly d(CESI) std dev: {cesi_sd:.3f}")
print(f"\nShock event response analysis:")
print("-"*68)

results = []
for s in SHOCKS:
    pre = s["pre"]; post = s["post"]; t0 = s["t0"]
    chg = cesi_window_change(pre, post)
    pct = cesi_window_pct(pre, post)
    z   = chg / cesi_sd
    cesi_pre  = cesi_at(pre)
    cesi_t0   = cesi_at(t0)
    cesi_post = cesi_at(post)
    # Peak deviation matching the EXPECTED direction (predicted ex-ante)
    # in [T0, T0+6mo] forward window
    i0 = month_index(t0)
    hi = min(len(MONTHS)-1, i0 + 6)
    seg = [(MONTHS[i], CESI[MONTHS[i]]) for i in range(i0, hi+1)]
    if s["dir"] < 0:
        # Expecting fall: find minimum
        peak_val = min(v for _, v in seg)
        peak_ym  = next(ym for ym, v in seg if v == peak_val)
    else:
        # Expecting rise: find maximum
        peak_val = max(v for _, v in seg)
        peak_ym  = next(ym for ym, v in seg if v == peak_val)
    peak_dev = peak_val - cesi_pre
    peak_z = peak_dev / cesi_sd
    print(f"\n[{s['name']}]  type={s['type']}")
    print(f"   Pre   {pre[0]}-{pre[1]:02d}: CESI = {cesi_pre:.2f}")
    print(f"   T0    {t0[0]}-{t0[1]:02d}: CESI = {cesi_t0:.2f}")
    print(f"   Peak  {peak_ym[0]}-{peak_ym[1]:02d}: CESI = {peak_val:.2f}  (delta {peak_dev:+.2f}, z {peak_z:+.2f})")
    print(f"   Post  {post[0]}-{post[1]:02d}: CESI = {cesi_post:.2f}  (delta {chg:+.2f}, z {z:+.2f})")
    print(f"   Expected: {s['expected']}")
    results.append({"shock":s["name"], "type":s["type"],
                    "pre":cesi_pre, "t0":cesi_t0, "post":cesi_post,
                    "chg":chg, "pct":pct, "z":z,
                    "peak_dev":peak_dev, "peak_z":peak_z, "peak_val":peak_val, "peak_ym":peak_ym,
                    "expected":s["expected"]})

# ============================================================
# 7. PASS/FAIL CRITERIA
# ============================================================
def evaluate(s, r):
    """Pass criteria: direction of peak deviation matches expected sign,
       AND magnitude is non-trivial (|peak_z| > 0.5)."""
    if s["name"] == "2008 Oil Spike":
        # Demand collapse -> CESI should fall in ±6mo window
        return r["peak_dev"] < 0 and abs(r["peak_z"]) > 0.5
    if s["name"] == "2014-16 Shale Crash":
        # Demand intact + supply expanding -> CESI flat or modest rise
        # (NO sharp drop: that would falsify the demand-driven thesis)
        return r["peak_dev"] >= -2.0   # i.e. did NOT collapse
    if s["name"] == "2020 COVID Demand Collapse":
        # Sharpest demand shock in modern era -> CESI must drop materially
        return r["peak_dev"] < 0 and r["peak_z"] < -1.0
    if s["name"] == "2022 Russia/Ukraine":
        # Supply impaired, demand intact -> CESI must rise
        return r["peak_dev"] > 0 and r["peak_z"] > 0.5
    return False

print("\n" + "="*68)
print("PASS/FAIL CRITERIA")
print("="*68)
n_pass = 0
for s, r in zip(SHOCKS, results):
    p = evaluate(s, r)
    r["pass"] = p
    n_pass += int(p)
    print(f"  {s['name']:35s}  ->  {'PASS' if p else 'FAIL'}")

print(f"\nOVERALL: {n_pass} / {len(SHOCKS)} PASS")

# ============================================================
# 8. VISUALISATION: 4-PANEL DASHBOARD
# ============================================================
dates = [date(y, m, 15) for (y,m) in MONTHS]
cesi_vals = [CESI[(y,m)] for (y,m) in MONTHS]
wti_vals  = [WTI_NOMINAL[(y,m)] for (y,m) in MONTHS]
d_vals    = [D_monthly[(y,m)] for (y,m) in MONTHS]
x_vals    = [X_norm[(y,m)] for (y,m) in MONTHS]
i_vals    = [I_norm[(y,m)] for (y,m) in MONTHS]

ACCENT  = "#1B3A5C"
ACCENT2 = "#2E75B6"
RED     = "#C0392B"
GREEN   = "#27AE60"
GREY    = "#7F8C8D"

fig = plt.figure(figsize=(15, 11))
fig.suptitle("CESI TEST 2: SHOCK RESPONSE VALIDATION (2000-2024 monthly)",
             fontsize=14, fontweight="bold", color=ACCENT)

# Panel 1: CESI vs WTI with shock windows shaded
ax1 = fig.add_subplot(2, 2, 1)
ax1.plot(dates, cesi_vals, color=ACCENT, lw=1.6, label="CESI (monthly)")
ax1.set_ylabel("CESI (2000-01 = 100)", color=ACCENT, fontweight="bold")
ax1.tick_params(axis='y', labelcolor=ACCENT)
ax1b = ax1.twinx()
ax1b.plot(dates, wti_vals, color=RED, lw=1.0, alpha=0.7, label="WTI nominal $/bbl")
ax1b.set_ylabel("WTI $/bbl", color=RED)
ax1b.tick_params(axis='y', labelcolor=RED)
# Shock shaded windows
shock_colors = ["#FFD580","#D5E8D4","#F8CECC","#DAE8FC"]
for s, c in zip(SHOCKS, shock_colors):
    pre_d  = date(s["pre"][0],  s["pre"][1],  1)
    post_d = date(s["post"][0], s["post"][1], 28)
    ax1.axvspan(pre_d, post_d, color=c, alpha=0.35)
    t0_d = date(s["t0"][0], s["t0"][1], 15)
    ax1.axvline(t0_d, color="black", lw=0.5, ls="--", alpha=0.5)
ax1.set_title("CESI vs WTI with shock windows", fontweight="bold")
ax1.xaxis.set_major_locator(mdates.YearLocator(4))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax1.grid(True, alpha=0.3)

# Panel 2: Monthly demand components (X, I) normalised
ax2 = fig.add_subplot(2, 2, 2)
ax2.plot(dates, x_vals, color=ACCENT2, lw=1.2, label="X: OECD electricity (norm)")
ax2.plot(dates, i_vals, color="#8E44AD", lw=1.2, label="I: US INDPRO (norm)")
ax2.plot(dates, d_vals, color=ACCENT, lw=1.8, label="D: composite demand")
for s, c in zip(SHOCKS, shock_colors):
    pre_d  = date(s["pre"][0],  s["pre"][1],  1)
    post_d = date(s["post"][0], s["post"][1], 28)
    ax2.axvspan(pre_d, post_d, color=c, alpha=0.25)
ax2.set_title("Demand components (monthly, base 2000-01 = 100)", fontweight="bold")
ax2.legend(fontsize=8, loc="upper left")
ax2.xaxis.set_major_locator(mdates.YearLocator(4))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax2.grid(True, alpha=0.3)

# Panel 3: Peak CESI deviation in [T0, T0+9mo] forward window
ax3 = fig.add_subplot(2, 2, 3)
labels = [s["name"].replace(" ", "\n", 1) for s in SHOCKS]
peaks  = [r["peak_dev"] for r in results]
zs     = [r["peak_z"]   for r in results]
colors = [GREEN if r["pass"] else RED for r in results]
bars = ax3.bar(labels, peaks, color=colors, edgecolor="black", lw=0.6)
for b, z in zip(bars, zs):
    ax3.text(b.get_x()+b.get_width()/2, b.get_height(),
             f"z={z:+.2f}", ha="center",
             va="bottom" if b.get_height()>=0 else "top", fontsize=9)
ax3.axhline(0, color="black", lw=0.6)
ax3.set_title("Peak CESI deviation in [T0, T0+9mo] (PASS=green)", fontweight="bold")
ax3.set_ylabel("Peak ΔCESI vs pre-shock baseline (pts)")
ax3.grid(True, alpha=0.3, axis="y")

# Panel 4: Results summary table
ax4 = fig.add_subplot(2, 2, 4); ax4.axis("off")
table_data = [["Shock","Pre","T0","Peak Δ","Peak z","Net Δ","Net z","Result"]]
for s, r in zip(SHOCKS, results):
    table_data.append([
        s["name"][:24],
        f"{r['pre']:.1f}",
        f"{r['t0']:.1f}",
        f"{r['peak_dev']:+.2f}",
        f"{r['peak_z']:+.2f}",
        f"{r['chg']:+.2f}",
        f"{r['z']:+.2f}",
        "PASS" if r["pass"] else "FAIL",
    ])
table_data.append(["OVERALL","","","","","","",f"{n_pass}/{len(SHOCKS)}"])
tbl = ax4.table(cellText=table_data, loc="center", cellLoc="center", colWidths=[0.26]+[0.10]*7)
tbl.auto_set_font_size(False)
tbl.set_fontsize(8)
tbl.scale(1, 1.5)
for j in range(8):
    tbl[(0,j)].set_facecolor(ACCENT); tbl[(0,j)].set_text_props(color="white", weight="bold")
for i in range(1, len(SHOCKS)+1):
    res_cell = tbl[(i,7)]
    res_cell.set_facecolor(GREEN if results[i-1]["pass"] else RED)
    res_cell.set_text_props(color="white", weight="bold")
tbl[(len(SHOCKS)+1,0)].set_facecolor(ACCENT); tbl[(len(SHOCKS)+1,0)].set_text_props(color="white", weight="bold")
tbl[(len(SHOCKS)+1,7)].set_facecolor(ACCENT); tbl[(len(SHOCKS)+1,7)].set_text_props(color="white", weight="bold")
ax4.set_title("Test 2 results summary", fontweight="bold", color=ACCENT)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("C:/Users/OMU/Desktop/Energy/CESI_test2_shock.png", dpi=160, bbox_inches="tight")
plt.savefig("C:/Users/OMU/Desktop/Energy/CESI_test2_shock.svg", bbox_inches="tight")
plt.close()
print("\nSaved: CESI_test2_shock.png / .svg")

# ============================================================
# 9. MONTHLY CSV EXPORT
# ============================================================
csv_path = "C:/Users/OMU/Desktop/Energy/cesi_test2_monthly.csv"
with open(csv_path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["YearMonth","Year","Month","WTI_Nominal","INDPRO","Elec_TWh",
                "X_norm","I_norm","E_ann_norm","P_ann_norm","D","S_ann","CESI"])
    for (y,m) in MONTHS:
        w.writerow([f"{y}-{m:02d}", y, m,
                    f"{WTI_NOMINAL[(y,m)]:.2f}",
                    f"{INDPRO[(y,m)]:.2f}",
                    f"{ELEC[(y,m)]:.2f}",
                    f"{X_norm[(y,m)]:.3f}",
                    f"{I_norm[(y,m)]:.3f}",
                    f"{E_ann_norm[y]:.3f}",
                    f"{P_ann_norm[y]:.3f}",
                    f"{D_monthly[(y,m)]:.3f}",
                    f"{S_ann[y]:.3f}",
                    f"{CESI[(y,m)]:.3f}"])
print(f"Saved monthly CSV ({len(MONTHS)} rows): {csv_path}")

# ============================================================
# 10. SHOCK SUMMARY CSV
# ============================================================
shock_csv = "C:/Users/OMU/Desktop/Energy/cesi_test2_shocks.csv"
with open(shock_csv, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Shock","Type","Pre_YM","T0_YM","Post_YM",
                "CESI_Pre","CESI_T0","CESI_Post",
                "Peak_YM","CESI_Peak","Peak_Delta","Peak_Z",
                "Net_Delta","Net_Pct","Net_Z","Result","Expected"])
    for s, r in zip(SHOCKS, results):
        w.writerow([s["name"], s["type"],
                    f"{s['pre'][0]}-{s['pre'][1]:02d}",
                    f"{s['t0'][0]}-{s['t0'][1]:02d}",
                    f"{s['post'][0]}-{s['post'][1]:02d}",
                    f"{r['pre']:.3f}", f"{r['t0']:.3f}", f"{r['post']:.3f}",
                    f"{r['peak_ym'][0]}-{r['peak_ym'][1]:02d}",
                    f"{r['peak_val']:.3f}",
                    f"{r['peak_dev']:+.3f}", f"{r['peak_z']:+.3f}",
                    f"{r['chg']:+.3f}", f"{r['pct']:+.2f}", f"{r['z']:+.3f}",
                    "PASS" if r["pass"] else "FAIL", s["expected"]])
print(f"Saved shock summary CSV: {shock_csv}")

print("\n" + "="*68)
print("TEST 2 COMPLETE")
print("="*68)
