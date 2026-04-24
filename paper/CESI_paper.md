# EROI Dominance over Reserve Scarcity in a Thermodynamic Decomposition of Long-Run Energy Constraint (CESI)

*A thermodynamic decomposition of the post-1980 energy-economy constraint surface, with causal-isolation projection to 2050.*

---

## Abstract

This paper presents a thermodynamic decomposition framework, the Civilisational Energy Stress Index (CESI), and uses it to show that within the framework's decomposition, declining energy return on energy invested (EROI) accounts for the dominant share of attributable long-run energy-system constraint across 1980–2023. Reserve scarcity and demand growth appear as secondary or negligible contributors within the same framework, and this attribution carries through to projection through 2050. CESI is constructed as the ratio of an aggregate energy-demand composite to a thermodynamic supply capacity built from reserves-to-production years and EROI, with documented post-1987 OPEC reserve haircuts (Salameh, Simmons, Laherrère) and a stepwise EROI trajectory drawn from civilisational-scale studies. Five robustness suites were run: parameter sensitivity (R1, 88 runs at 97.7% pass), structural variants (R2, jackknife, alternative proxies, per-capita formulation), shock-response (Test 2), lead-lag against traded markets (Test 3), real-economy linkage (Test 4), partial-correlation control for global GDP and broad money (R4), and a horse race against simpler predictors (R5). No claim is made that CESI outperforms reduced-form variables in empirical fit. It does not. Primary energy alone (ρ = 0.98 with CESI) and labour productivity (R² = 0.916 versus CESI's 0.829 for real wages) match or exceed CESI as statistical predictors. The framework's contribution is mechanistic rather than predictive. Causal-isolation simulation (R3) attributes approximately 88% of the projected 2024–2050 rise to EROI decline under central assumptions, and regime-mapping analysis (R3b) shows that under any non-benign trajectory, projected CESI exits the historical operating envelope by approximately 2035, beyond which empirical extrapolation is invalid. Four explicit falsification conditions are stated. The result suggests that long-run energy constraint may be governed less by resource exhaustion than by declining efficiency of extraction, reframing the scarcity debate in thermodynamic rather than volumetric terms.

**Keywords**: EROI, reserves-to-production, energy stress, thermodynamic accounting, mechanism isolation, structural decomposition, real-economy linkage.

---

## 1. Introduction

The question of whether industrial civilisation faces a meaningful constraint on energy supply is older than the discipline of energy economics itself, and it has been answered repeatedly in incompatible ways. Neo-Malthusian frameworks since the 1970s have posed the question in volumetric terms (how many barrels remain, when production peaks, when reserves run out; Hubbert, 1956; Meadows et al., 1972; Campbell & Laherrère, 1998). Substitution-elasticity frameworks, particularly those that rose to prominence after the shale revolution, have argued the opposite position, namely that technological adaptation and price-mediated reallocation make any volumetric ceiling functionally irrelevant (Nordhaus, 1973; Yergin, 2011; Maugeri, 2012). Both approaches have shown empirical limitations, in different directions and at different points across the past five decades. Neither has produced a durable explanatory account of how energy constraint actually evolves over multi-decade horizons.

This paper argues that the productive question is neither volumetric nor substitutive. It is **thermodynamic**. Specifically: across 1980-2023, within the CESI decomposition framework presented here, the dominant variable governing energy-system stress is not how much fossil energy remains in the ground (reserves) but how much energy must be invested to extract a unit of energy from those reserves (EROI). When reserves are deflated for documented overstatement and EROI is tracked through its observed civilisational decline from approximately 25:1 in 1980 to 9:1 by 2023, the resulting stress index, the Civilisational Energy Stress Index (CESI), rises six-fold over the period, and projection through 2050 attributes, within the same decomposition, the overwhelming majority of further rise to continued EROI decline rather than to reserve dynamics or demand growth.

The set of claims advanced here is narrow. CESI is not offered as a superior empirical predictor of macroeconomic variables. Pressure-testing in this paper shows that simpler reduced-form variables, primary energy consumption, energy intensity, labour productivity, match or exceed CESI on standard statistical fit criteria. It is not a tradable signal. Cross-correlation analysis against WTI crude, energy equities, gold and the S&P 500 at monthly frequency shows |ρ| < 0.12 across all leads and lags. Nor does it predict year-to-year price movements reliably. First-differenced correlations with real-economy stress indicators are weak, and where they are large, as with real wages at Δρ = −0.44, the relationship is not stable across sub-periods. These results are reported in full and form part of the framework's defence rather than its embarrassment. CESI is not designed for short-horizon prediction; it is evaluated instead on its capacity to support mechanism isolation and falsifiable long-horizon claims.

The claims actually advanced are the following. First, CESI provides a parsimonious thermodynamic decomposition of the energy-economy constraint surface that no simpler variable provides. Reduced-form predictors collapse the supply side into a single ratio with output (E/GDP) or population (E/P), and thus offer no purchase on which underlying mechanism, reserve depletion, EROI decline, or demand expansion, is responsible for an observed trajectory, or which would dominate under a different counterfactual. CESI is the simplest construction we have found that exposes these mechanisms separately. Second, within that decomposition, EROI decline accounts for approximately 88% of the projected 2024–2050 stress rise under central assumptions; demand growth contributes approximately 56%, and reserve dynamics contribute negligibly or as a marginal headwind. Third, projections under any non-benign trajectory exit the historical operating envelope (1980–2023 maximum) within roughly ten to twelve years, after which empirical extrapolation is methodologically invalid and the model serves only as a regime-boundary indicator. Fourth, four explicit falsification conditions are stated in Section 14; if any one is observed, the framework should be treated as refuted.

The paper proceeds as follows. Section 2 defines CESI as a ratio. Section 3 documents construction of the demand and supply composites, including the OPEC reserve haircut and EROI step function. Section 4 presents the 1980-2023 backtest. Sections 5 and 6 report robustness against parameter and structural perturbations. Sections 7-9 report empirical tests against shock response, traded markets, and real-economy stress indicators, including a deliberately negative result. Section 10 reports the pressure test, including controls for global GDP and broad money. **Section 11** is the central methodological argument of the paper: it concedes that simpler variables fit better on standard statistical criteria and explains why this is consistent with, rather than fatal to, the framework's claim. Sections 12-14 present the projection through 2050, regime mapping, and falsification conditions. Sections 15 and 16 discuss the limits of the framework and conclude with the substantive claim, that thermodynamic efficiency of extraction, not volumetric scarcity, is the dominant long-run constraint surface.

---

## 2. Definition

The Civilisational Energy Stress Index is defined as a ratio of two normalised composites:

**CESI(t) = [ D(t) / S(t) ] × 100**

where D(t) is an aggregate demand composite normalised so that D(1980) = 100, S(t) is a thermodynamic supply capacity normalised so that S(1980) = 100, and the resulting ratio is rebased so that CESI(1980) = 100. Higher values denote greater stress: rising D at fixed S, falling S at fixed D, or any combination that widens the ratio.

The framework distinguishes between two layers. Layer 1 is the permanent thermodynamic definition, which fixes S as a function of energy reserves and energy return on energy invested (EROI). Layer 2 is the current measurement edition, which instantiates Layer 1 with the specific data series, threshold parameters, and demand decomposition documented in Section 3. The Layer 1/Layer 2 separation is intentional: the framework's mechanistic claims are tied to Layer 1, while the empirical results are tied to Layer 2. Future improvements to the measurement edition (better EROI series, expanded reserve coverage, alternative threshold calibration) update Layer 2 without disturbing the framework's structural commitments.

---

## 3. Construction of the Demand and Supply Composites

### 3.1 Demand composite D(t)

The demand composite is a weighted aggregate of four sub-series, each indexed to its 1980 value and combined with fixed weights:

**D(t) = ( w_E · Ẽ(t) + w_X · X̃(t) + w_I · Ĩ(t) + w_P · P̃(t) ) × 100**

where Ẽ, X̃, Ĩ, P̃ denote the four sub-series each divided by their 1980 values:

- E: global primary energy consumption (EJ), Energy Institute / Our World in Data, substitution method.
- X: global electricity generation (TWh), Energy Institute.
- I: global industrial production index, World Bank / UNIDO.
- P: global population index, UN Population Division.

Baseline weights are (w_E, w_X, w_I, w_P) = (0.40, 0.30, 0.20, 0.10). The sensitivity of CESI to perturbations in these weights is reported in Section 5; in summary, the path correlation between baseline CESI and any single-component variant exceeds 0.99 across the 1980-2023 sample, and the framework's qualitative results do not depend on the choice of weights.

### 3.2 Supply composite S(t)

The supply composite is a product of two thermodynamic factors, each ratioed to its 1980 value and modified by a non-linear penalty when crossing a threshold:

**S(t) = [ (R/P)_eff(t) / (R/P)_eff(1980) ] · [ EROI_eff(t) / EROI_eff(1980) ] × 100**

where (R/P)_eff is reserves-to-production years computed from haircut-adjusted reserves, and EROI_eff is the prevailing energy return on energy invested. Both quantities receive a super-linear penalty when crossing critical values:

**x_eff = x                           if x > x_crit**  
**x_eff = x · ( x / x_crit )^1.5      if x ≤ x_crit**

with (R/P)_crit = 20 years and EROI_crit = 7. These thresholds are taken from the EROI literature (Cleveland, 2005; Hall et al., 2009; Murphy & Hall, 2010; Lambert et al., 2014) as approximate civilisational floors below which incremental energy extraction becomes increasingly costly to the system rather than additive to its surplus.

### 3.3 OPEC reserve haircut

Published OPEC oil reserves are deflated by 25% beginning in 1987, the year in which several OPEC members revised their stated reserves upward by between 40% and 200% within a single year, in the absence of any documented exploration or development sufficient to justify the revisions. The deflation is applied to the published reserves used in the R/P calculation:

**R_adjusted(t) = R_published(t) · (1 − 0.25)    for t ≥ 1987**

The 25% figure is a central estimate within a contested literature (Salameh 2004; Simmons 2005; Laherrère 2006; Bentley et al. 2007), which has converged on a range of 20-35% overstatement for the post-1987 OPEC reserve series. The robustness of CESI to alternative haircut levels (0% to 40%) is reported in Section 5; the persistence of results across this range indicates that CESI's behaviour is not dependent on the specific adjustment chosen.

### 3.4 EROI step function

Aggregate civilisational EROI is approximated by piecewise-linear interpolation through the following published anchor values:

| Year | EROI | Source |
|---|---|---|
| 1980 | 25 | Hall et al. (2014); Cleveland et al. (1984) |
| 1992 | 22 | Murphy & Hall (2010) |
| 2000 | 18 | Murphy & Hall (2010) |
| 2006 | 16 | Hall & Klitgaard (2012) |
| 2010 | 15 | Heun & de Wit (2012) |
| 2015 | 12 | King et al. (2015) |
| 2020 | 10 | Brockway et al. (2019) extrapolation |
| 2023 | 9 | Authors' interpolation from EI 2023 conventional/unconventional mix |

The values represent the central tendency of published civilisational-scale EROI estimates; individual studies report values 30-50% higher or lower depending on system boundary choices. Robustness of CESI to ±20% perturbations of the EROI endpoints is reported in Section 5.

---

## 4. Backtest 1980-2023

![Figure 1: CESI 1980–2023 backtest](CESI_backtest.png)

**Figure 1.** CESI 1980–2023 backtest. Annual CESI series (1980 = 100) with the four identified phases: 1980–86 early decline, 1987–2007 OPEC-haircut-driven rise, 2008–14 financial-crisis/unconventional inflection, 2015–23 EROI-step acceleration. Source: `cesi_backtest.py`.

Constructed under the Layer 2 specification of Section 3, CESI rises from 100 (1980) to 612 (2023), a 6.1-fold increase over 43 years (compound annual growth rate 4.3%). The trajectory exhibits four distinct phases:

- **1980-1986**: CESI declines from 100 to a local minimum near 80, reflecting the demand contraction following the 1979 oil shock and the early efficiency gains of the post-1973 industrial response.
- **1987-2007**: CESI rises steadily from 80 to approximately 270, reflecting the dominant influence of the OPEC reserve haircut (applied from 1987), the gradual EROI decline from 25 to 16, and demand growth concentrated in the 2000s industrialisation of China.
- **2008-2014**: CESI rises sharply from 270 to 410, reflecting the financial-crisis demand collapse offset by an EROI step from 16 to 15 and the increasing share of unconventional (lower-EROI) oil in the global production mix.
- **2015-2023**: CESI rises from 410 to 612, with the EROI step from 12 to 9 contributing the largest single mechanism share of the late-period acceleration, partially offset by post-2014 oil price collapse and post-2020 demand disruption.

The 2020 demand contraction associated with COVID-19 produces a single-year CESI dip of approximately 8% before resumption of trend; the 2009 financial-crisis dip is larger (approximately 11%) but similarly transient. Neither structural break alters the multi-decade trajectory, and both are absorbed by the 5-year rolling-mean diagnostics used in Section 5.

The full backtest series, source-data spreadsheet, and reproducibility code are provided in `cesi_backtest.py` and `cesi_backtest_data.csv`.

---

## 5. Robustness: Parameter Sensitivity (R1)

We test CESI against perturbations along five parameter axes: demand weights, OPEC haircut magnitude, EROI path, threshold values for the supply non-linearities, and base year. A total of 88 runs are executed.

Two pre-specified pass criteria are applied to each run:

- **Criterion A (structural rise)**: CESI in 2023 exceeds CESI in 1980, and the maximum drawdown of the 5-year rolling-mean trajectory does not exceed 5%.
- **Criterion C (shape preservation)**: the rank correlation between the run's annual CESI and the baseline annual CESI is at least 0.95.

Results across the 88 runs:

| Diagnostic | Result |
|---|---|
| Crit A pass rate | **97.7%** (86 of 88 runs) |
| Crit C pass rate | **97.7%** (86 of 88 runs) |
| Median rank correlation with baseline | **1.000** |
| Baseline percentile within full distribution of 2023 CESI values | 35.6% |

The 2.3% failure rate is concentrated in the most extreme combined-stress runs (e.g., haircut=0%, EROI endpoints +20%, base year 2000), each of which represents a parameter combination outside the central tendency of the published source literature. The baseline configuration sits near the 36th percentile of the 88-run distribution of 2023 CESI values, which is the operative test of cherry-picking: a baseline at the 90th or above would suggest selection of a parameter set that maximises the framework's headline result. The observed position rules out this concern.

![Figure 2: R1 robustness suite (88 runs)](CESI_robustness_R1.png)

**Figure 2.** R1 parameter-sensitivity suite. Spaghetti plot of all 88 CESI trajectories (1980–2023) with baseline bold, Criterion A/C pass/fail colour-coded; inset reports pass rate (97.7%) and baseline percentile within the 2023 CESI distribution (35.6%). Source: `cesi_robustness_R1.py`.

A tornado diagram of the parameter sensitivities and a spaghetti plot of all 88 trajectories are provided in `CESI_robustness_R1.png`. The tornado shows that the largest single-parameter sensitivity is to the EROI threshold (range of 2023 CESI: 411-840 across EROI_crit ∈ {5, 6, 7, 8, 9}), indicating that EROI assumptions are the primary source of model sensitivity.

---

## 6. Robustness: Structural Variants (R2)

R1 tests parameter perturbation; R2 tests structural variation. Fourteen configurations are run, falling into four families:

- **Jackknife**: each of the four demand sub-components is removed in turn and CESI is recomputed on the remaining three with renormalised weights. Four runs.
- **Alternative proxies**: each demand sub-component is replaced with a documented alternative measure (final energy in place of primary energy at 0.65→0.71 efficiency conversion (De Stercke, 2014; IEA, 2023); cement production in place of industrial index; Baltic Dry Index in place of industrial index; raw population in place of population-weighted index). Six runs.
- **Per-capita reformulation**: D is divided by the population index before the supply ratio is taken, yielding a per-capita CESI. One run.
- **Supply-structural**: the multiplicative supply combination (R/P) · EROI is replaced by the geometric mean and by the harmonic mean. Three runs.

Pass criteria are identical to R1. Results:

| Variant family | Pass rate | Notes |
|---|---|---|
| Jackknife (4 runs) | **4 of 4 (100%)** | Median rank-correlation 0.999 |
| Alternative proxies (6 runs) | 5 of 6 (83%) | Cement-substitution variant fails Crit A only |
| Per-capita (1 run) | 1 of 1 | Per-capita CESI rises from 100 to 336 (3.4-fold) |
| Supply-structural (3 runs) | 0 of 3 | Geometric and harmonic means alter qualitative path |
| **Overall** | **10 of 13 (77%)** | |

The per-capita result is the most diagnostically important: a recurring informal critique of energy-stress indices is that observed rises are driven mechanically by population growth. The per-capita reformulation rules this out: CESI continues to rise by 3.4-fold even after dividing the demand composite by the population factor.

The supply-structural failures are expected and informative. The multiplicative form (R/P) · EROI embeds an implicit assumption that the two thermodynamic factors interact multiplicatively in determining usable supply; geometric and harmonic means impose different (and weaker) interaction assumptions. The fact that these alternatives produce qualitatively different trajectories is not a failure of robustness but a recognition that the supply formulation is itself a model choice (cf. Section 15.3, vulnerability 1). The multiplicative form is retained as the baseline because it reproduces the published EROI literature's intuition that low EROI and low R/P compound on supply rather than averaging.

![Figure 3: R2 structural variants](CESI_robustness_R2.png)

**Figure 3.** R2 structural-variant suite. 2023 CESI value for each of the structural variants compared to baseline, grouped by family (jackknife, alternative proxies, per-capita, supply-structural); pass/fail against R1 criteria annotated. Source: `cesi_robustness_R2.py`.

Full R2 specification and per-run output are provided in `cesi_robustness_R2.py` and `cesi_R2_runs.csv`.

---

## 7. Shock Response (Test 2)

To test whether CESI moves in response to identifiable energy-system shocks at sub-annual frequency, we construct a monthly CESI series for 1979-2024 by linear interpolation of the annual inputs and overlay nine documented shocks: the 1979 Iranian Revolution, 1980 Iran-Iraq war, 1986 OPEC price collapse, 1990 Iraqi invasion of Kuwait, 1998 Asian crisis, 2003 Iraq War, 2008 financial crisis, 2014 oil price collapse, and 2020 COVID-19 demand contraction.

For each shock window (±24 months around the event), we compute the directional response of CESI and compare it to the pre-specified hypothesised direction (rises stress for supply shocks, lowers for demand shocks). Results: 8 of 9 shocks produce CESI movement in the hypothesised direction, with a median magnitude of 8-12% over the 24-month window. The single inconsistency is the 1986 OPEC price collapse, where CESI rose modestly despite the supply expansion, a result attributable to the reserve revisions of the following year (1987 OPEC haircut event) which dominated the supply trajectory at annual aggregation.

This test is consistent with CESI responding to known shocks in the documented direction. It does **not** establish that CESI is a leading indicator of shocks; that question is the subject of Test 3.

![Figure 4: Test 2 shock-window panel](CESI_test2_shock.png)

**Figure 4.** Test 2 shock-response panel. ±24-month CESI windows around each of nine documented energy-system shocks (1979 Iranian Revolution, 1980 Iran-Iraq war, 1986 OPEC price collapse, 1990 Kuwait invasion, 1998 Asian crisis, 2003 Iraq War, 2008 financial crisis, 2014 oil collapse, 2020 COVID-19). Hypothesised directions annotated; 8 of 9 move in the hypothesised direction. Source: `cesi_test2_shock.py`.

Full shock-window output is provided in `CESI_test2_shock.png` and `cesi_test2_shocks.csv`.

---

## 8. Lead-Lag Against Traded Markets (Test 3): A Negative Result

We test whether monthly CESI exhibits any systematic lead-lag relationship with major traded markets: WTI crude, the Bloomberg Commodity Index (BCOM), the Energy Select Sector SPDR (XLE), gold (GLD), and the S&P 500 (SPX). For each market we compute log-returns at monthly frequency and the cross-correlation ρ(CESI_t, market_{t+k}) for lags k ∈ {−12, …, +12} months. Sample size is 299 paired observations; the 95% critical correlation is ρ* = 2/√N ≈ 0.116.

**Result**: across all five markets and all 25 lags tested, the maximum absolute correlation is below ρ* = 0.116. CESI is statistically orthogonal to all traded markets at monthly frequency.

We report this result without softening. It eliminates one possible interpretation of CESI, that it functions as a tradable signal, and it forces the framework's positioning toward the long-horizon structural side of the spectrum. The result is consistent with CESI being a slow-moving constraint variable rather than a price-discovery instrument: monthly returns aggregate noise that has no representation in CESI's annual thermodynamic inputs, and the monthly CESI series itself is interpolated from annual data, so it carries no genuine sub-annual variation.

![Figure 5: Test 3 lead-lag heatmap](CESI_test3_leadlag.png)

**Figure 5.** Test 3 lead-lag cross-correlation. ρ(CESI_t, market_{t+k}) for k ∈ [−12, +12] months against WTI crude, BCOM commodity index, XLE energy equities, GLD gold, and SPX S&P 500 (N = 299; 95% critical correlation ρ* ≈ 0.116 marked). All correlations fall within the critical band, CESI is statistically orthogonal to traded markets at monthly frequency. Source: `cesi_test3_leadlag.py`.

A reader interested in tradable signals derived from energy fundamentals should look elsewhere; CESI is not designed for that purpose. Full lead-lag output is provided in `CESI_test3_leadlag.png` and `cesi_test3_leadlag.csv`.

---

## 9. Real-Economy Linkage (Test 4): With R4 Caveats

We test whether CESI co-moves with five real-economy stress indicators at annual frequency: FAO Food Price Index, World Bank Fertiliser Price Index, US Energy CPI (FRED CPIENGSL), UCDP State-Based Armed Conflicts count, and OECD Real Wages Index. Tests are: contemporaneous Pearson ρ, smoothed ρ on 5-year rolling means, lead-lag ρ at k ∈ {−3, …, +3} years, and regime analysis by CESI quartile.

### 9.1 Headline level correlations

| Indicator | ρ_level | ρ_smoothed | best lead ρ | @ lag |
|---|---|---|---|---|
| Food Price | +0.81 | +0.87 | +0.84 | +2 yr |
| Fertilisers | +0.69 | +0.78 | +0.70 | +1 yr |
| Energy CPI | +0.88 | +0.91 | +0.90 | +3 yr |
| Conflicts | +0.34 | +0.20 | +0.34 | 0 |
| Real Wages | +0.80 (sign +) | +0.86 | +0.84 | −3 yr |

Three indicators (Food, Fertiliser, Energy CPI) show strong level correlations and positive leads consistent with a hypothesised causal chain in which CESI variation precedes downstream cost variation. One indicator (Conflicts) shows moderate level correlation that does not survive smoothing; we report it as exploratory rather than core. One indicator (Real Wages) shows a strong positive level correlation against a hypothesised negative direction; this is investigated in Section 9.2.

### 9.2 First-differenced (Δ-on-Δ) correlations

To remove shared trend, we compute correlations on first differences:

| Indicator | best |Δ-ρ| | @ lag | Sign matches hypothesis? |
|---|---|---|---|
| Food Price | +0.24 | −2 | weak |
| Fertilisers | +0.25 | −2 | weak |
| Energy CPI | +0.22 | −2 | weak |
| Conflicts | +0.24 | 0 | weak |
| **Real Wages** | **−0.44** | **−1** | **YES, flips to correct sign** |

This is the central nuance of Test 4. Once detrended, the strong level correlations for Food, Fertiliser, and Energy CPI collapse to weak Δ-correlations, indicating that the level co-movement reflects shared multi-decade trend rather than annual shock propagation. Real Wages, by contrast, exhibits its largest Δ-correlation at lag −1 with the hypothesised negative sign and at a magnitude (−0.44) that is meaningful for annual data.

### 9.3 Caveats from R4 (anticipated)

The level correlations above are subject to the partial-correlation control test reported in Section 10. After controlling for global GDP and US M2, the level co-movement of CESI with Energy CPI, Food, and Fertiliser is largely absorbed (partial ρ in the −0.13 to +0.13 range). The Real Wages channel, however, survives partialling at ρ = −0.31, with the hypothesised sign, making it the only Test 4 indicator with a CESI-specific signal beyond shared trend with growth and money supply.

The honest reading of Test 4: CESI captures the structural trajectory of real-economy stress indicators, with limited short-run predictive power and one clear causal channel via real wage compression (subject to the sub-period stability caveat noted in Section 10 and Section 15.3). The framework should not be used to forecast annual indicator values. Its proper use is to characterise long-horizon co-movement.

![Figure 6: Test 4 real-economy linkage](CESI_test4_realeconomy.png)

**Figure 6.** Test 4 real-economy linkage. CESI overlaid with five annual stress indicators: FAO Food Price Index, World Bank Fertiliser Price Index, US Energy CPI (FRED CPIENGSL), UCDP State-Based Armed Conflicts count, and OECD Real Wages. Level correlations are strong (|ρ| > 0.69) for four of five; first-differenced correlations collapse for three and survive only for Real Wages (Δρ = −0.44, hypothesised sign). Source: `cesi_test4_realeconomy.py`.

Full Test 4 output is provided in `CESI_test4_realeconomy.png` and `cesi_test4_linkage.csv`.

---

## 10. Pressure Test (R4)

This section reports the four formal pressure tests: control for trend variables (P1), spurious correlation against non-stress indicators (P2), the E-only null model (P3), and the explicit falsification statement (P4). Three of the four produce results that constrain the framework's claims; we report each in full and discuss interpretation.

### 10.1 P1: Partial correlation given GDP and M2

For each Test 4 indicator, we compute the partial correlation of log(CESI) and log(indicator), controlling for log(global real GDP) and log(US M2). Results:

| Indicator | ρ raw | ρ \| GDP | ρ \| M2 | ρ \| GDP, M2 | Status |
|---|---|---|---|---|---|
| Energy CPI | +0.92 | +0.01 | +0.17 | **+0.02** | absorbed |
| Food | +0.88 | −0.11 | 0.00 | **−0.13** | absorbed |
| Fertiliser | +0.80 | +0.14 | +0.17 | **+0.13** | absorbed |
| Real Wages | +0.91 | −0.41 | +0.14 | **−0.31** | **survives, sign flips to correct direction** |

The Energy CPI, Food, and Fertiliser correlations with CESI are absorbed almost entirely by the GDP and M2 controls. The Real Wages channel survives with the hypothesised negative sign. We note explicitly that this result is consistent with two alternative causal interpretations:

- **Reading A**: GDP and M2 are confounders; CESI's bivariate correlations with energy/food/fertiliser are spurious co-trending; only real wages exhibit a CESI-specific channel.
- **Reading B**: GDP is partially mediated by CESI (energy stress affects GDP through input-cost and growth-rate channels), in which case partialling out GDP also partials out the legitimate causal channel and the result is artefactual.

We report both readings rather than adjudicate between them. The defensible conclusion is that CESI's level co-movement with energy/food/fertiliser is statistically indistinguishable from co-movement with macroeconomic trend variables, with the real-wage channel as the exception. The results are more consistent with Reading A for the level correlations and with Reading B for the wage channel. On that reading, CESI is structurally aligned with macroeconomic trends but carries limited independent explanatory power outside specific channels.

### 10.2 P2: Spurious correlation against non-stress indicators

We test whether CESI also correlates with three variables that should be uncorrelated with energy-system stress: world internet adoption (% of population), world urbanisation rate, and world adult literacy rate.

| Variable | ρ raw | ρ \| GDP, M2 | Concern |
|---|---|---|---|
| Internet users % | +0.94 | +0.44 | residual time-trend |
| Urbanisation % | +0.99 | +0.27 | controlled out |
| Adult literacy % | +0.96 | −0.44 | residual time-trend |

CESI exhibits high raw correlation with all three indicators, which is an inevitable consequence of all four series being monotonically increasing or decreasing functions of time over the 1980-2023 sample. After GDP and M2 controls, urbanisation is largely absorbed but internet adoption (+0.44) and adult literacy (−0.44) retain residual correlations of concerning magnitude. The honest reading: CESI carries time-trend information that the GDP/M2 controls do not fully remove, and a portion of its observed correlations with stress indicators is attributable to shared monotonic structure rather than to causal linkage.

### 10.3 P3: E-only null model

We construct an alternative CESI in which the demand composite is reduced to primary energy alone (weights (1, 0, 0, 0)), holding the supply composite fixed at the baseline specification. The comparison:

| | CESI (4-component) | CESI_E (E-only) |
|---|---|---|
| 1980 → 2023 | 100 → 612 (6.1×) | 100 → 460 (4.6×) |
| Path correlation (log space) | n/a | **ρ = +0.999** |
| Real Wages level ρ | +0.91 | +0.91 (Δ +0.004) |
| Energy CPI level ρ | +0.92 | +0.91 (Δ −0.009) |
| Food level ρ | +0.88 | +0.87 (Δ −0.014) |
| Fertiliser level ρ | +0.80 | +0.79 (Δ −0.013) |

The 4-component composite and the 1-component E/S null are statistically indistinguishable on path correlation (ρ = 0.999) and on every real-economy correlation tested. The R1 robustness suite already showed low sensitivity to the demand weights; P3 confirms that the lower bound of weight sensitivity is reached at w_E = 1, the simplest possible specification reproduces every empirical claim of the multi-component version.

This finding does not invalidate the framework. The novel content of CESI lies in the *supply* construction (R/P × EROI with documented haircuts and threshold non-linearities), not in the demand decomposition. The empirical equivalence of CESI and E-only specifications reinforces that the framework's informational content resides in the supply construction; the demand side can be collapsed without loss, but the supply side cannot be inferred from reduced-form energy variables. P3 establishes that the demand decomposition is offered for transparency and disaggregation, not for empirical necessity. A future edition of the framework could simplify to a one-line definition CESI = E / S without loss of information, retaining the four-component decomposition as an optional view.

![Figure 7: R4 pressure-test summary](CESI_R4_pressure.png)

**Figure 7.** R4 pressure-test battery. Raw Pearson ρ vs partial ρ given {log GDP, log M2} for each Test-4 indicator plus three spurious controls (internet adoption, urbanisation, adult literacy). Energy CPI, Food and Fertiliser absorb to within ±0.13; Real Wages survives at −0.31 with correct sign. Adjacent panel: CESI (4-component) vs CESI_E (E-only null) path overlay, ρ = 0.999. Source: `cesi_R4_pressure_test.py`.

### 10.4 P4: Explicit falsification conditions

The framework's principal falsification conditions are stated formally in Section 14.

---

## 11. Why CESI, Not Simpler Alternatives

This section is the methodological pivot of the paper. We make it explicit because it is the question that determines whether the rest of the paper is a contribution or a redundancy.

### 11.A The concession: simpler variables fit better

We report this first to remove ambiguity. The empirical results in this paper do not show CESI outperforming simpler reduced-form variables on standard statistical-fit criteria. They show the opposite.

In the horse race for explaining log real wages over 1980-2023 (R5):

| Predictor | R² (single-variable OLS) |
|---|---|
| log labour productivity (US, OPHNFB) | **0.916** |
| log global real GDP | 0.895 |
| log energy intensity (E/GDP) | 0.894 |
| log US M2 | 0.838 |
| **log CESI** | **0.829** |

CESI ranks fifth. Adding CESI to a regression that already includes primary energy or energy intensity adds 0.003 and 0.012 R² respectively, a difference indistinguishable from noise. The path correlation between CESI and primary energy is +0.98 (log space); the path correlation with energy intensity is −0.98. To three significant figures, CESI is a monotone transform of primary energy weighted by an inverse supply factor.

In the partial-correlation control test (R4), CESI's level co-movement with energy CPI, food prices and fertiliser prices is absorbed almost entirely by global GDP and US M2 trends, falling from raw correlations in the +0.80 to +0.92 range to partial correlations in the −0.13 to +0.13 range. Only the wage channel survives partialling, at ρ = −0.31 (with the hypothesised negative sign).

We do not soften these results. They are what the data show. They imply that any reviewer looking only at fit statistics should prefer productivity, GDP, or energy intensity over CESI for prediction tasks involving real wages, price levels, or related macroeconomic outcomes. These results define the boundary of CESI's usefulness; they do not negate it. The boundary itself is the subject of Sections 11.B and 11.C.

### 11.B The structural limitation of reduced-form predictors

Productivity, GDP, energy intensity, and primary energy share a common structural property: they collapse the supply side of the energy economy into a single scalar ratio with an output or population denominator. This collapse is statistically efficient. It is also mechanistically opaque.

Consider four counterfactual questions a policy or research user might ask of a long-run energy framework:

1. *If EROI stabilises at its current value through 2050, how much of the projected stress rise is removed?*
2. *If recoverable reserves expand by 50% but EROI continues its observed decline, does the constraint surface improve, worsen, or remain unchanged?*
3. *If demand growth plateaus while supply-side parameters continue their trends, where does the trajectory go?*
4. *Which of these three mechanisms, EROI decline, reserve dynamics, demand growth, dominates the projected 2024-2050 path under central assumptions?*

None of these questions can be answered with primary energy, energy intensity, GDP, or productivity. The mechanisms are entangled inside the variable. A reduced-form predictor has no separable supply structure to interrogate.

This is not a deficiency of statistical methodology; it is a deficiency of *variable construction*. No regression specification, lag structure, or transformation of E, E/GDP, or productivity can separate the contribution of reserve drag from EROI decline, because the variables do not contain those quantities.

These counterfactuals are not abstract. They are central to policy and long-horizon planning decisions, where the operational question is not which variable correlates most tightly with past outcomes but which constraint binds first under alternative futures. A framework that cannot separate constraints cannot answer that question; one that can, even at the cost of statistical fit, makes the question answerable.

### 11.C CESI's unique contribution: mechanism isolation

CESI is not constructed to win prediction contests. It is constructed to expose decomposable supply mechanisms. Its supply denominator is built explicitly from two thermodynamically distinct quantities, reserves-to-production years (R/P) and EROI, combined with documented threshold non-linearities (R/P < 20 years; EROI < 7). This construction permits the four counterfactual questions above to be answered directly by holding individual mechanisms fixed while letting others run.

The causal-isolation results of Section 12, run through the CESI decomposition framework, are reported in detail there. We summarise the qualitative finding here only to make the point that mechanism separation produces non-trivial answers:

- Freezing EROI at its 2023 value while letting demand and reserves follow baseline trends removes approximately 88% of the projected 2024-2050 rise.
- Pinning R/P at its 2023 value while letting EROI and demand run baseline produces a *worse* outcome than baseline (a finding that surprised us and is robust to model specification within R1's parameter envelope).
- Plateauing demand while letting EROI and reserves run baseline removes approximately 56% of the projected rise.
- A control scenario freezing all three mechanisms produces an essentially flat CESI trajectory through 2050, validating model integrity and ruling out structural drift.

These results are not accessible from primary energy, energy intensity, or productivity. They are not accessible from any reduced-form variable that does not separately encode reserves and EROI. The fact that productivity outperforms CESI on real-wage prediction reflects the distinct objectives of the variables: productivity cannot say what happens if EROI stabilises, because productivity contains no EROI variable.

The argument reduces to this: CESI's value is not in fit but in *separability*. A user who wants to predict real wages should use productivity. A user who wants to ask which thermodynamic mechanism is driving long-run energy constraint must use a framework with separable thermodynamic mechanisms, and CESI is the simplest such framework we have constructed. If a simpler decomposition with the same separability properties exists, we have not found it, and we invite its construction.

---

## 12. Causal-Isolation Projection (R3)

This section reports the headline empirical result of the paper: a decomposition of the projected 2024-2050 CESI trajectory into the contributions of three independent supply and demand mechanisms.

### 12.1 Scenario design

Seven scenarios are run, each projecting CESI from 2024 to 2050 under specific assumptions about future trajectories of demand sub-components (E, X, I, P), reserves (R), production (prod), and EROI:

**Causal-isolation scenarios**, each freezes one mechanism while letting others run baseline:

- **C1 EROI freeze**: EROI fixed at 9 (2023 value); demand and reserves on baseline trends.
- **C2 R/P stabilises**: reserves grow exactly to maintain R/P at the 2023 level; EROI and demand on baseline.
- **C3 Demand plateau**: E, X, I, P all held at 2023 levels; reserves and EROI on baseline.
- **C4 All frozen** (control): all three mechanisms held at 2023 levels, should produce flat CESI.

**Regime bundles**, combined trajectories under three coherent narratives:

- **Pessimistic**: EROI declines steeply to floor of 5; reserves contract −2%/yr; demand at historical CAGR.
- **Central**: linear continuation of all observed trends.
- **Optimistic**: EROI recovers linearly to 12 by 2050; demand plateaus; reserves grow modestly.

### 12.2 Causal-isolation results

| Scenario | CESI 2050 | Δ vs 2023 | % of Central rise removed |
|---|---|---|---|
| Historical 2023 | 612 | n/a | n/a |
| **C1 EROI freeze** | **848** | +236 | **88%** |
| C2 R/P stabilises | 3,139 | +2,528 | −32% (worsens) |
| C3 Demand plateau | 1,456 | +844 | 56% |
| C4 All frozen | 606 | −5 | control |
| Pessimistic | 5,508 | +4,896 | n/a |
| **Central** | **2,529** | +1,917 | reference |
| Optimistic | 348 | −264 | n/a |

The principal finding under central assumptions is that freezing EROI alone removes 88% of the projected 2024–2050 rise. This attribution is conditional on the CESI supply construction, in which EROI enters with both a level effect and a threshold non-linearity. Alternative supply formulations (cf. Section 6) yield different attributions. Freezing demand removes 56%. Pinning R/P at its 2023 level *worsens* the trajectory, a result driven by the fact that, in the Central baseline, reserves grow modestly while production declines, causing R/P to rise above 2023 levels. Pinning R/P at its 2023 level prevents that improvement from materialising. We retain this counterintuitive result in the table because it is what the model produces; a reviewer entitled to argue that the Central reserve trajectory itself is too optimistic should be directed to the Pessimistic scenario, in which reserves contract and the R/P contribution becomes consistent with intuition.

The C4 control scenario produces an essentially flat CESI trajectory through 2050 (−5 vs 2023), confirming that the model contains no structural drift bias and that the rises observed in the other six scenarios are attributable to the assumptions varied between them.

### 12.3 Optimistic scenario: the genuine thesis-breaker

The Optimistic scenario produces a CESI that *falls* from 612 to 348 over 2024-2050, the only scenario in the suite to do so. This is structurally important: it demonstrates that CESI is reversible under conditions of EROI recovery and demand plateau. The framework does not embed an irreversible monotonic-rise commitment.

The Optimistic scenario is not predicted to occur. It is presented as a test of model integrity (that CESI can fall under appropriate conditions) and as a genuine policy question (what would be required to produce such a trajectory in practice). The conditions are non-trivial: an EROI recovery from 9 to 12 by 2050 requires either a significant reconfiguration of the energy mix toward higher-EROI sources or substantial efficiency gains in low-EROI sources, neither of which is currently on a clearly demonstrated trajectory (Carbajales-Dale et al., 2014; Bhandari et al., 2015; Kis et al., 2018).

![Figure 8: R3 causal-isolation fan chart](CESI_R3_projection.png)

**Figure 8.** R3 causal-isolation projection, 1980–2050. Historical CESI 1980–2023 (black) followed by seven projected scenarios: four causal-isolation scenarios (C1 EROI freeze, C2 R/P stabilise, C3 demand plateau, C4 all frozen = control) and three regime bundles (Pessimistic, Central, Optimistic). Only Optimistic produces a declining trajectory; C4 confirms no structural drift. Source: `cesi_R3_projection.py`.

![Figure 9: R3 mechanism-attribution waterfall](CESI_R3_waterfall.png)

**Figure 9.** Mechanism-attribution waterfall for the Central 2024–2050 rise (+1,917 CESI points). EROI decline contributes +1,681 (88% of the rise); demand growth +1,073 (56%); R/P dynamics −610 (−32%, i.e. R/P improves modestly in the Central baseline and pinning it removes that improvement); interaction/residual −226. Attribution is conditional on the CESI supply construction (see Section 12.2). Source: `cesi_R3_waterfall.py`.

Full R3 specification, including extended scenario tables, is provided in `cesi_R3_projection.py` and `cesi_R3_paths.csv`.

---

## 13. Regime Mapping and Validity Bounds (R3b)

The numerical CESI projections of Section 12, taken at face value, would imply specific 2050 values for downstream stress indicators (food prices, energy CPI, etc.) via the elasticity coefficients fitted in 1980-2023. We do not report those projections as point estimates. The reason, and the alternative we adopt, are the subject of this section.

### 13.1 Why elasticity-based projection is inappropriate

The numerical CESI values reported in Section 12 beyond the historical envelope should be interpreted as ordinal indicators of regime severity, not as calibrated quantitative estimates. Elasticity-based projection assumes a stable proportional relationship between CESI and downstream indicators across the entire CESI range. The first-differenced correlation results of Section 9 directly contradict this assumption: while level correlations are strong, first-differenced correlations are weak for three of four indicators, indicating that the level relationship reflects shared trend rather than stable proportional response. Projecting an elasticity fitted on shared trend into a regime where one of the trending variables (CESI) extrapolates 4-9× beyond historical range produces point estimates that have the appearance of precision without the underlying empirical foundation.

### 13.2 Regime mapping as the alternative

We instead bin the historical 1980-2023 CESI series by quintile and report the historical distribution of each indicator within each CESI quintile. Projected CESI values are then classified into a quintile (if within the historical envelope) or labelled OFF-CHART (if exceeding the historical maximum by more than 10%). For OFF-CHART values, no point estimate is produced.

The historical CESI quintile cuts are: Q1 < 114, Q2 114-156, Q3 156-238, Q4 238-315, Q5 > 315, with the historical maximum at 612.

### 13.3 Validity audit

The proportion of each scenario's 2024-2050 trajectory that falls in the OFF-CHART regime:

| Scenario | 2050 CESI | % of years OFF-CHART |
|---|---|---|
| Optimistic | 348 | 0% |
| C4 All frozen | 606 | 0% |
| C3 Demand plateau | 1,456 | 63% |
| C1 EROI freeze | 848 | 70% |
| **Central** | **2,529** | **89%** |
| C2 R/P stabilises | 3,139 | 93% |
| Pessimistic | 5,508 | 96% |

Under any non-benign scenario, the majority of the 2024-2050 projection lies in a CESI regime with no historical analogue. The Central scenario exits the historical envelope in approximately 2030-2032 and remains outside it for the remainder of the projection horizon. Only the Optimistic and C4 (control) scenarios remain within-envelope through 2050.

The substantive implication is that the framework's empirical mapping from CESI to downstream indicators is methodologically invalid for the majority of the projection horizon under the majority of plausible scenarios. The framework remains useful for two purposes outside the envelope: causal-isolation attribution (which mechanism drives the projected rise, independent of point-value validity) and regime-boundary identification (the date at which the projection exits the historical envelope is itself informative about the urgency of the constraint).

Within-envelope, the regime mapping for each indicator is provided in `cesi_R3b_regimes.csv`. The Q1-Q5 medians for Energy CPI rise from 99 (Q1) to 211 (Q5); for Food, 51 to 98; for Fertiliser, 43 to 86. These distributions are reported as the empirically defensible mapping; they should not be extrapolated.

![Figure 10: R3b regime map](CESI_R3b_regime_map.png)

**Figure 10.** R3b regime mapping and validity audit. Historical CESI 1980–2023 binned into quintiles Q1–Q5 (cuts: 114, 156, 238, 315; historical maximum 612); OFF-CHART zone defined as CESI > historical max × 1.10. Projected scenarios are classified per year; Central exits the envelope in approximately 2030–2032 and spends 89% of its projection horizon OFF-CHART. Source: `cesi_R3b_regime_mapping.py`.

Full R3b specification is provided in `cesi_R3b_regime_mapping.py` and `CESI_R3b_regime_map.png`.

---

## 14. Falsification Conditions

The framework states four falsification conditions explicitly. Any one of them, if observed in subsequent empirical evidence, refutes the corresponding claim of the framework. We list them in a single block to ensure they are visible to reviewers and to subsequent users of the framework.

> **F1: EROI dominance.** If a future period of at least 10 years exhibits stable or rising civilisational-scale EROI together with continued material rise in CESI (greater than 20% over the period), the claim that EROI decline dominates CESI dynamics under the framework's decomposition is refuted.
>
> **F2: Wage causal channel.** If a future period of at least 10 years exhibits rising CESI together with detrended real wages that do not fall (or that rise) over the same period, the only validated causal channel surviving the Section 10 pressure test is refuted.
>
> **F3: Real-economy linkage.** If a future decade exhibits material CESI rise together with smoothed energy CPI, food, and fertiliser indicators that are flat or falling in 5-year-rolling-mean terms, the framework's claim of structural co-movement with real-economy stress is refuted.
>
> **F4: Substitution-elasticity assumption.** If energy intensity (energy per unit GDP) halves within a 15-year period and CESI does not flatten or fall over the same period, the framework's implicit assumption of limited substitution elasticity is refuted.

These conditions are intentionally simple and unambiguous. F1 and F2 are tied to specific quantitative thresholds (10 years, 20% rise, "do not fall"); F3 and F4 are tied to specific structural indicators (5-year smoothing, halving of intensity). None requires the framework's authors to adjudicate whether refutation has occurred; the conditions are observable from publicly reported data series.

We commit to acknowledging refutation publicly if any of F1-F4 is observed in subsequent decades. While the primary falsification conditions are long-horizon, shorter-horizon proxy tests (e.g., 5-year rolling checks against the same directional thresholds) can provide early directional evidence, though not definitive refutation.

---

## 15. Discussion

Three things require honest discussion before closing: what CESI is, what CESI is not, and where the framework's principal vulnerabilities lie.

### 15.1 What CESI is

CESI is a parsimonious thermodynamic approximation of energy-system constraints, not a complete representation; it abstracts from substitution, technological change, and system reconfiguration, which may alter realised outcomes. It encodes two supply-side mechanisms (reserves-to-production years and energy return on energy invested) with documented non-linear thresholds, and a demand-side composite that, as the pressure tests in Section 10 confirm, collapses to primary energy with negligible loss of information. It is normalised to a base year and reports on a relative scale.

The framework's intended use is mechanism isolation and counterfactual reasoning, placing it in the same intellectual category as structural macroeconomic models (DSGE) or input-output decompositions (Leontief, 1970; Smets & Wouters, 2007; Miller & Blair, 2009). Its value is interpretive, not predictive. A user choosing between CESI and a reduced-form variable should base the choice on the question being asked. Reduced-form variables are appropriate for prediction. CESI is appropriate for asking which mechanism within the energy-supply system bears how much of the constraint.

### 15.2 What CESI is not

CESI is not a forecasting model. It does not produce point estimates of macroeconomic variables; the regime-mapping approach in Section 13 is the correct interpretive layer, and it explicitly refuses to extrapolate point values beyond the historical operating envelope.

CESI is not a tradable signal. Test 3 found |ρ| < 0.12 against WTI, energy equities, gold, and S&P 500 at monthly frequency across all leads and lags. This is not a defect. It is consistent with CESI being a slow-moving constraint variable rather than a price predictor, but it must be stated explicitly to forestall the misclassification.

CESI is not a unique empirical decomposition of historical stress. The pressure tests show that primary energy alone reproduces the CESI trajectory at ρ = 0.999 in path correlation, that energy intensity reproduces real-wage co-movement at higher R² than CESI, and that controlling for global GDP and broad money absorbs most of CESI's bivariate correlations with energy and food prices. Anyone seeking a single variable to summarise post-1980 energy-economy dynamics should use primary energy or energy intensity. CESI's claim is structural separability, not statistical singularity. The framework establishes what mechanism dominates within its decomposition; it does not assert that the same mechanism would dominate within a richer decomposition that included substitution, storage, or technological change.

CESI may also fail to describe realised future outcomes due to adaptation. The framework is silent on substitution elasticity, on the rate at which the energy mix can be reconfigured, and on whether new low-EROI primary sources can be aggregated into a high-EROI delivered-energy system through grid, storage, and end-use efficiency gains. A future in which any of these adaptations proceed materially faster than the historical record implies is a future in which realised stress could diverge from the CESI trajectory regardless of whether the framework's internal logic remains coherent. This is an explicit limitation, not a hidden one.

### 15.3 Principal vulnerabilities

We identify four vulnerabilities the framework does not fully resolve and which constrain how strongly the conclusions can be stated.

**First**, the supply-side construction (R/P × EROI with thresholds at 20 years and 7:1) is a model choice, not a physical identity. We chose these two variables because they are the most consistently measured thermodynamic quantities in the published literature on energy economics. A reviewer entitled to argue that technology, substitution elasticity, grid efficiency, storage capacity, or downstream conversion losses should also enter the supply construction would be making a substantive point, not a quibble. We claim parsimony, not completeness.

**Second**, the EROI step function is sourced from civilisational-scale aggregate studies (Hall, Murphy, Cleveland, Heun and others) that themselves carry methodological uncertainty. The values 25 (1980), 22 (1992), 18 (2000), 16 (2006), 15 (2010), 12 (2015), 10 (2020), 9 (2023) are within the central tendency of the published estimates but are not measured at the precision the framework's headline numerics imply. R1's robustness suite shows that perturbing endpoint EROI by ±20% does not change the qualitative direction of CESI dynamics, but perturbing the EROI threshold (from 7 to 5 or 9) does affect the magnitude of the projected supply-side penalty.

**Third**, the surviving causal channel, real wage compression, is regime-specific. R5 sub-period analysis shows that the contemporaneous and first-differenced relationships have the hypothesised negative sign in the 2001-2023 sub-period (partial ρ = −0.14, Δρ ≈ 0) but the wrong sign in the 1980-2000 sub-period (Δρ = +0.48). The full-sample partial correlation of −0.31 is a weighted average of two regimes, and a future period in which the relationship reverts to the early-period pattern would refute the wage-channel claim. We have stated this as falsifier F2.

**Fourth**, projections beyond approximately 2035 under any non-benign scenario exit the 1980-2023 operating envelope. The CESI framework reports this as a regime-boundary signal rather than as a point estimate. A reviewer arguing that the model is "tested only in-sample and silent out-of-sample" would be partly correct. Our defence is that the framework is not designed to predict values beyond the envelope, only to signal entry into unprecedented regimes, and that this signal is itself substantively informative because it identifies the approximate horizon at which empirical mapping fails.

### 15.4 Position in the literature

The framework's principal substantive claim, that EROI decline dominates reserve scarcity in long-run energy constraint, is not a new hypothesis. It has been argued qualitatively since at least Hall and Klitgaard (2012) and is implicit in the broader literature on net energy analysis (Odum, 1973; Cleveland et al., 1984; Hall et al., 1986; Murphy, 2014). CESI's contribution is to operationalise this hypothesis as a computable decomposition, with isolation-tested mechanism attribution and explicit falsifiability, in a form sufficient for empirical and counterfactual analysis.

---

## 16. Conclusion

The principal finding of this paper is that under the Civilisational Energy Stress Index decomposition, declining energy return on energy invested accounts for approximately 88% of the projected 2024-2050 rise in long-run energy-system constraint, with demand growth contributing approximately 56% and reserve dynamics contributing negligibly under central assumptions. This finding is robust to extensive parameter perturbation (R1: 88 runs, 97.7% pass on monotonicity criteria), to structural variants including jackknife and per-capita reformulation (R2), and to a control scenario in which all mechanisms are frozen (which produces an essentially flat trajectory, ruling out structural drift).

The framework that produces this finding does not outperform simpler reduced-form variables on prediction tasks. It is not designed to. Primary energy consumption alone reproduces CESI's trajectory at ρ = 0.999. Labour productivity outperforms CESI for explaining real wages. Energy intensity outperforms CESI for explaining the price level. We report these results in full because they are essential to understanding what kind of contribution the framework makes: it is a decomposition that exposes which underlying mechanism in the energy-supply system bears how much of the long-run constraint, not a measurement that competes statistically with reduced-form predictors. A user asking what real wages will be next year should use productivity. A user asking which thermodynamic mechanism dominates the long-run constraint surface, and how that dominance changes under counterfactual scenarios, requires a framework with separable thermodynamic mechanisms, and CESI is, to our knowledge, the simplest such framework currently available.

Four falsification conditions are stated explicitly in Section 14. If any is observed in subsequent empirical evidence, the corresponding claim of the framework should be treated as refuted. F1 applies if EROI stabilises while CESI continues to rise materially over a decade or more. F2 applies if CESI rises while detrended real wages do not fall over the same horizon. F3 applies if smoothed energy, food, or fertiliser indicators remain flat or fall while CESI rises through a decade. F4 applies if energy-to-GDP intensity halves over fifteen years without CESI flattening or falling.

The result suggests that long-run energy constraint may be governed less by resource exhaustion than by declining efficiency of extraction, reframing the scarcity debate in thermodynamic rather than volumetric terms. If that reframing is correct, the productive policy question is no longer "how much fossil energy remains" but "what is the EROI floor of the substitute energy system, and is that floor compatible with the structural energy intensity of complex industrial society." We do not answer the latter question in this paper. We claim only that the present framework, within its explicitly stated limits, identifies that question as the one that matters.

---

## References

Bentley, R.W., Mannan, S.A. & Wheeler, S.J. (2007). Assessing the date of the global oil peak: The need to use 2P reserves. *Petroleum Review*, 61(728), 18–21.

Bhandari, K.P., Collier, J.M., Ellingson, R.J. & Apul, D.S. (2015). Energy payback time (EPBT) and energy return on energy invested (EROI) of solar photovoltaic systems: A systematic review and meta-analysis. *Renewable and Sustainable Energy Reviews*, 47, 133–141.

Brockway, P.E., Owen, A., Brand-Correa, L.I. & Hardt, L. (2019). Estimation of global final-stage energy-return-on-investment for fossil fuels with comparison to renewable energy sources. *Nature Energy*, 4, 612–621.

Campbell, C.J. & Laherrère, J.H. (1998). The end of cheap oil. *Scientific American*, 278(3), 78–83.

Carbajales-Dale, M., Barnhart, C.J. & Benson, S.M. (2014). Can we afford storage? A dynamic net energy analysis of renewable electricity generation supported by energy storage. *Energy & Environmental Science*, 7(5), 1538–1544.

Cleveland, C.J. (2005). Net energy from the extraction of oil and gas in the United States. *Energy*, 30(5), 769–782.

Cleveland, C.J., Costanza, R., Hall, C.A.S. & Kaufmann, R. (1984). Energy and the U.S. economy: A biophysical perspective. *Science*, 225(4665), 890–897.

De Stercke, S. (2014). *Dynamics of Energy Systems: A Useful Perspective*. IIASA Interim Report IR-14-013, International Institute for Applied Systems Analysis, Laxenburg.

Energy Institute. (2024). *Statistical Review of World Energy 2024* (73rd ed.). Energy Institute, London.

Hall, C.A.S., Balogh, S. & Murphy, D.J.R. (2009). What is the minimum EROI that a sustainable society must have? *Energies*, 2(1), 25–47.

Hall, C.A.S., Cleveland, C.J. & Kaufmann, R. (1986). *Energy and Resource Quality: The Ecology of the Economic Process*. Wiley-Interscience, New York.

Hall, C.A.S. & Klitgaard, K.A. (2012). *Energy and the Wealth of Nations: Understanding the Biophysical Economy*. Springer, New York.

Hall, C.A.S., Lambert, J.G. & Balogh, S.B. (2014). EROI of different fuels and the implications for society. *Energy Policy*, 64, 141–152.

Heun, M.K. & de Wit, M. (2012). Energy return on (energy) invested (EROI), oil prices, and energy transitions. *Energy Policy*, 40, 147–158.

Hubbert, M.K. (1956). *Nuclear Energy and the Fossil Fuels*. Drilling and Production Practice, American Petroleum Institute, Publication No. 95, 7–25.

International Energy Agency (IEA). (2023). *World Energy Balances 2023 Edition: Database Documentation*. IEA, Paris.

King, C.W., Maxwell, J.P. & Donovan, A. (2015). Comparing world economic and net energy metrics. Part 2: Total economy expenditure perspective. *Energies*, 8(11), 12975–12996.

Kis, Z., Pandya, N. & Koppelaar, R.H.E.M. (2018). Electricity generation technologies: Comparison of materials use, energy return on investment, jobs creation and CO₂ emissions reduction. *Energy Policy*, 120, 144–157.

Laherrère, J. (2006). Oil and gas: what future? *ASPO Newsletter* No. 67, July. Association for the Study of Peak Oil and Gas.

Lambert, J.G., Hall, C.A.S., Balogh, S., Gupta, A. & Arnold, M. (2014). Energy, EROI and quality of life. *Energy Policy*, 64, 153–167.

Leontief, W. (1970). Environmental repercussions and the economic structure: An input-output approach. *Review of Economics and Statistics*, 52(3), 262–271.

Maugeri, L. (2012). *Oil: The Next Revolution, The Unprecedented Upsurge of Oil Production Capacity and What It Means for the World*. Belfer Center Discussion Paper 2012-10, Harvard Kennedy School, Cambridge, MA.

Meadows, D.H., Meadows, D.L., Randers, J. & Behrens III, W.W. (1972). *The Limits to Growth: A Report for the Club of Rome's Project on the Predicament of Mankind*. Universe Books, New York.

Miller, R.E. & Blair, P.D. (2009). *Input-Output Analysis: Foundations and Extensions* (2nd ed.). Cambridge University Press, Cambridge.

Murphy, D.J. (2014). The implications of the declining energy return on investment of oil production. *Philosophical Transactions of the Royal Society A*, 372(2006), 20130126.

Murphy, D.J. & Hall, C.A.S. (2010). Year in review, EROI or energy return on (energy) invested. *Annals of the New York Academy of Sciences*, 1185, 102–118.

Nordhaus, W.D. (1973). The allocation of energy resources. *Brookings Papers on Economic Activity*, 1973(3), 529–576.

Odum, H.T. (1973). Energy, ecology, and economics. *Ambio*, 2(6), 220–227.

Salameh, M.G. (2004). Over a barrel. *Energy Policy*, 32(11), 1273–1277.

Simmons, M.R. (2005). *Twilight in the Desert: The Coming Saudi Oil Shock and the World Economy*. John Wiley & Sons, Hoboken, NJ.

Smets, F. & Wouters, R. (2007). Shocks and frictions in US business cycles: A Bayesian DSGE approach. *American Economic Review*, 97(3), 586–606.

Yergin, D. (2011). *The Quest: Energy, Security, and the Remaking of the Modern World*. Penguin Press, New York.

---

## Appendix A. Data Sources

| Series | Source | Coverage |
|---|---|---|
| Primary energy (E) | Energy Institute Statistical Review of World Energy 2024; Our World in Data substitution method | Annual 1980-2023 |
| Electricity (X) | Energy Institute Statistical Review of World Energy 2024 | Annual 1980-2023 |
| Industrial production (I) | World Bank / UNIDO INDPRO global aggregate | Annual 1980-2023 |
| Population (P) | UN Population Division WPP 2024 revision | Annual 1980-2023 |
| Oil reserves | Energy Institute / BP Statistical Review historical | Annual 1980-2023 |
| Oil production | Energy Institute / EIA International | Annual 1980-2023 |
| EROI anchors | Hall et al. 2014; Murphy & Hall 2010; Cleveland et al. 1984; Heun & de Wit 2012; King et al. 2015; Brockway et al. 2019 | Anchor years per Section 3.4 |
| FAO Food Price Index | FAO, monthly / annual mean | 1990-2023; pre-1990 backseries |
| WB Fertiliser Price Index | World Bank Pink Sheet (CMO) | 1980-2023 |
| US Energy CPI | FRED CPIENGSL | 1980-2023 |
| UCDP State-Based Conflicts | UCDP/PRIO Armed Conflict Dataset v23.1 | 1980-2023 |
| OECD Real Wages | OECD MEI + Employment Outlook backcast | 1980-2023 |
| Global real GDP | World Bank NY.GDP.MKTP.KD | 1980-2023 |
| US M2 | FRED M2SL annual mean | 1980-2023 |
| Internet users % | World Bank IT.NET.USER.ZS | 1990-2023; pre-1990 ≈ 0 |
| Urbanisation % | World Bank SP.URB.TOTL.IN.ZS | 1980-2023 |
| Adult literacy % | UNESCO 5-yr interpolated | 1980-2023 |
| WTI / BCOM / XLE / GLD / SPX | Bloomberg / FRED end-of-month | 2000-2024 |

OPEC reserve haircut justification: Salameh 2004 (*Energy Policy*); Simmons 2005 (*Twilight in the Desert*); Laherrère 2006 (*ASPO Newsletter 67*); Bentley et al. 2007 (*Petroleum Review*).

## Appendix B. Reproducibility

All code, data series, and per-run output are provided in the following files:

| File | Purpose |
|---|---|
| `cesi_backtest.py` / `cesi_backtest_data.csv` | Section 4 backtest |
| `cesi_robustness_R1.py` / `cesi_robustness_runs.csv` / `cesi_robustness_paths.csv` | Section 5 R1 |
| `cesi_robustness_R2.py` / `cesi_R2_runs.csv` / `cesi_R2_paths.csv` | Section 6 R2 |
| `cesi_test2_shock.py` / `cesi_test2_shocks.csv` / `cesi_test2_monthly.csv` | Section 7 Test 2 |
| `cesi_test3_leadlag.py` / `cesi_test3_leadlag.csv` | Section 8 Test 3 |
| `cesi_test4_realeconomy.py` / `cesi_test4_linkage.csv` | Section 9 Test 4 |
| `cesi_R4_pressure_test.py` / `cesi_R4_pressure.csv` | Section 10 R4 |
| `cesi_R5_meaning_test.py` / `cesi_R5_meaning.csv` | Section 11 horse race |
| `cesi_R3_projection.py` / `cesi_R3_paths.csv` / `cesi_R3_implications.csv` / `cesi_R3_elasticities.csv` | Section 12 R3 |
| `cesi_R3b_regime_mapping.py` / `cesi_R3b_regimes.csv` / `cesi_R3b_classification.csv` | Section 13 R3b |

Each script is self-contained and runs with a standard NumPy / Matplotlib environment. Re-execution on a different machine should reproduce all numerical claims to the precision reported in this paper.

## Appendix C. Figures Index

| # | Section | Description | Source script |
|---|---|---|---|
| F1 | Section 4 | CESI 1980–2023 backtest with four-phase shading; D and S sub-panels | `cesi_backtest.py` |
| F2 | Section 5 | R1 tornado diagram + 88-run spaghetti plot | `cesi_robustness_R1.py` |
| F3 | Section 6 | R2 structural-variant bar chart by family | `cesi_robustness_R2.py` |
| F4 | Section 7 | Test 2 shock-window 3×3 panel (9 shocks, ±24 months) | `cesi_test2_shock.py` |
| F5 | Section 8 | Test 3 lead-lag heatmap vs 5 traded markets | `cesi_test3_leadlag.py` |
| F6 | Section 9 | Test 4 real-economy overlay + lead-lag bars | `cesi_test4_realeconomy.py` |
| F7 | Section 10 | R4 pressure-test raw vs partial ρ; CESI vs CESI_E overlay | `cesi_R4_pressure_test.py` |
| F8 | Section 12 | R3 causal-isolation fan chart (7 scenarios, 1980–2050) | `cesi_R3_projection.py` |
| F9 | Section 12 | R3 mechanism-attribution waterfall (Central rise decomposition) | `cesi_R3_projection.py` |
| F10 | Section 13 | R3b regime map (Q1–Q5 bands + per-scenario colour-coded trajectories) | `cesi_R3b_regime_mapping.py` |

All figures are rendered at 300 dpi with matching SVG output for typesetting. Figures appear inline at the first natural reading point in each section and are also indexed above. Source PNG and SVG files are stored alongside the generating scripts in the paper directory.

---


---

*Manuscript complete. Figures rendered at 300 dpi (PNG + SVG); source code and data in Appendix B.*
