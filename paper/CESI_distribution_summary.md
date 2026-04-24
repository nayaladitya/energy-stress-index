# CESI, Distribution Summary

*Companion document to the full paper:* **EROI Dominance over Reserve Scarcity in a Thermodynamic Decomposition of Long-Run Energy Constraint (CESI)**

---

## 1. Short abstract (200 words, general-audience)

For fifty years the question of whether industrial civilisation faces a hard energy ceiling has been answered two different ways. One camp counts barrels in the ground and warns of exhaustion. The other points to technology and price signals and concludes that substitution will always find a way. Both answers have run into the evidence repeatedly and in opposite directions.

This paper proposes that neither framing is the useful one. The binding constraint on industrial energy is not how much oil remains; it is how much energy must be spent to get the next unit of energy out of the ground. The ratio of energy returned to energy invested, EROI, has fallen from roughly 25-to-1 in 1980 to around 9-to-1 today.

We build a single index, the Civilisational Energy Stress Index (CESI), that combines this efficiency decline with reserve and demand dynamics on a common scale. CESI has risen six-fold since 1980. When we simulate what would happen if EROI stopped falling, nearly 90% of the projected stress rise to 2050 disappears. Reserves and demand matter much less. The conclusion is that long-run energy constraint is a thermodynamic problem, not a volumetric one, and that is a different kind of problem to solve.

---

## 2. Executive summary (one page)

### The question

Does industrial civilisation face a binding long-run energy constraint, and if so, what mechanism is driving it?

### The framework

The Civilisational Energy Stress Index (CESI) is a ratio of an aggregate energy-demand composite to a thermodynamic supply capacity built from two variables: reserves-to-production years (adjusted for documented post-1987 OPEC overstatement) and energy return on energy invested (EROI). CESI is indexed to 1980 = 100.

### The main finding

Within the CESI decomposition, declining EROI accounts for approximately **88%** of the projected 2024–2050 rise in energy-system stress under central assumptions. Demand growth contributes approximately **56%**. Reserve dynamics contribute negligibly. The result is robust to 88 parameter-sensitivity runs (97.7% pass rate), to structural variants including a per-capita reformulation, and to a control scenario in which all mechanisms are frozen (which correctly produces a flat trajectory).

### What the paper does not claim

CESI is not a forecasting model, not a tradable signal, and not a statistically superior predictor of macroeconomic outcomes. Simpler variables, primary energy consumption, energy intensity, labour productivity, match or beat CESI on standard fit criteria. This is reported in full. The framework's contribution is mechanism separation, not prediction: it is the simplest construction we have found that lets reserve drag, EROI decline, and demand expansion be attributed separately.

### The boundary

Under any non-benign projection scenario, CESI exits the 1980–2023 historical operating envelope within roughly ten to twelve years. Beyond that boundary the model serves as a regime-severity indicator, not as a source of quantitative point estimates. The paper uses quintile-based regime mapping rather than elasticity extrapolation to report this explicitly.

### Falsification

Four explicit falsification conditions are stated. If any one is observed in subsequent decades, the corresponding claim is refuted. The most important is F1: if civilisational EROI stabilises or rises over a decade while CESI continues to rise materially, the framework's EROI-dominance claim is refuted.

### The reframing

If the result holds, the productive policy question is no longer "how many barrels remain" but "what is the EROI floor of the substitute energy system, and is that floor compatible with the structural energy intensity of complex industrial society?"

---

## 3. At-a-glance numbers

| Metric | Value |
|---|---|
| CESI, 1980 → 2023 | 100 → 612 (6.1×, CAGR 4.3%) |
| EROI, civilisational-scale, 1980 → 2023 | ~25:1 → ~9:1 |
| R1 robustness pass rate | 97.7% (86 of 88 runs) |
| Baseline percentile in robustness distribution | 35.6th (rules out cherry-picking) |
| Path correlation, CESI vs primary energy (log) | +0.98 |
| Horse-race R², real wages: productivity | 0.916 |
| Horse-race R², real wages: CESI | 0.829 (5th of 5 candidates) |
| P1 partial ρ, Real Wages \| GDP, M2 | −0.31 (only surviving channel) |
| P3 E-only null path correlation | ρ = 0.999 |
| 2050 CESI, Central scenario | 2,529 (regime-ordinal) |
| 2050 CESI, Optimistic scenario | 348 (the only falling trajectory) |
| % of Central 2024–2050 rise attributed to EROI | 88% |
| Year Central scenario exits historical envelope | ~2030–2032 |

---

## 4. Target audiences and framing

| Audience | Likely point of entry | Key tension to flag |
|---|---|---|
| Energy economists | Sections 3, 6, 10 (construction, robustness, pressure test) | CESI ≈ E/S at ρ=0.999, is the supply construction doing real work? |
| Policy / long-horizon planning | Sections 12–14 (projection, regime map, falsifiers) | Central scenario goes OFF-CHART by early 2030s; what does that mean operationally? |
| Macro / finance | Section 8 (Test 3 null), Section 11 (horse race) | Not a tradable signal; productivity beats it for wage prediction |
| Thermodynamics / physical-economy | Sections 2–3 (definition, EROI step function), Section 15.4 (literature position) | Formalises a hypothesis Hall & Klitgaard and the net-energy school have argued qualitatively for decades |
| Critics / referees | Sections 10, 11, 15.3 (pressure test, concession, vulnerabilities) | Paper concedes everything a hostile reviewer would raise; defence is structural, not statistical |

---

## 5. One-sentence versions (for different channels)

- **Technical (journal abstract):** Within a thermodynamic decomposition of the post-1980 energy-economy constraint surface, declining EROI accounts for approximately 88% of attributable long-run stress, with reserve and demand dynamics as secondary or negligible contributors.
- **Policy brief:** The binding constraint on long-run industrial energy is the falling efficiency of extraction, not the quantity of resource remaining, and the policy implications are different.
- **General:** We are running out of cheap energy before we run out of energy.
- **Adversarial / short:** Peak oil was the wrong question. Peak EROI is the right one.

---

## 6. Deliverables available

| File | Purpose |
|---|---|
| `CESI_paper_draft.md` | Full manuscript, 10,476 words, 10 embedded figures, 32-reference bibliography |
| `CESI_paper_draft.docx` | Styled Word version, 3.78 MB, ready for circulation |
| `CESI_distribution_summary.md` | This document |
| `CESI_*.png` / `.svg` (×10) | All figures at 300 dpi, matched SVG for typesetting |
| `cesi_*.py` (×10) | All analysis and figure-generating scripts |
| `cesi_*.csv` (×13) | All intermediate and output data series |

---

*Summary prepared to accompany the full paper. Numerical claims reproduce those in the full manuscript; any divergence between this summary and the paper should be resolved in favour of the paper.*
