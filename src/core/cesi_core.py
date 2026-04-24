"""Shared primitives for the CESI construction.

Every script in src/ should import from this module rather than re-deriving
the demand composite, supply composite, or threshold penalty locally.
"""
from __future__ import annotations
import numpy as np


RP_CRIT   = 20.0     # reserves-to-production critical value (years)
EROI_CRIT = 7.0      # EROI critical value
DEMAND_WEIGHTS = {"E": 0.40, "X": 0.30, "I": 0.20, "P": 0.10}


def threshold_penalty(x: float, x_crit: float) -> float:
    """Super-linear penalty applied to a supply input below its critical value.

    Continuous at x = x_crit; reduces to x when x > x_crit.
    """
    if x > x_crit:
        return x
    return x * (x / x_crit) ** 1.5


def demand_composite(e: float, x: float, i: float, p: float,
                     e0: float, x0: float, i0: float, p0: float,
                     weights: dict[str, float] = DEMAND_WEIGHTS) -> float:
    """Weighted aggregate of four sub-series each normalised to its 1980 value."""
    e_t, x_t, i_t, p_t = e / e0, x / x0, i / i0, p / p0
    return 100.0 * (weights["E"] * e_t
                    + weights["X"] * x_t
                    + weights["I"] * i_t
                    + weights["P"] * p_t)


def supply_composite(rp: float, eroi: float,
                     rp_1980: float, eroi_1980: float) -> float:
    """Product of R/P and EROI, each normalised to 1980 and passed through
    the threshold penalty."""
    rp_eff     = threshold_penalty(rp, RP_CRIT)
    eroi_eff   = threshold_penalty(eroi, EROI_CRIT)
    rp_eff_0   = threshold_penalty(rp_1980, RP_CRIT)
    eroi_eff_0 = threshold_penalty(eroi_1980, EROI_CRIT)
    return 100.0 * (rp_eff / rp_eff_0) * (eroi_eff / eroi_eff_0)


def cesi(demand: float, supply: float) -> float:
    """CESI is the ratio of the demand composite to the supply composite, rebased."""
    return 100.0 * demand / supply
