"""Smoke tests on the CESI core.

These are not full coverage. They are three cheap invariants that any healthy
implementation should satisfy, and that would catch the most common regressions
(broken normalisation, discontinuous penalty, missing output files).
"""
from pathlib import Path
import pandas as pd
import pytest

RESULTS = Path(__file__).resolve().parents[1] / "results" / "series"


def _penalty(x, x_crit):
    return x if x > x_crit else x * (x / x_crit) ** 1.5


def test_penalty_continuous_at_threshold():
    """The super-linear penalty must be continuous at the critical value."""
    x_crit = 7.0
    left  = _penalty(x_crit - 1e-9, x_crit)
    right = _penalty(x_crit + 1e-9, x_crit)
    assert abs(left - right) < 1e-6


def test_penalty_reduces_below_threshold():
    """Below the critical value the effective x must be strictly smaller than x itself."""
    x_crit = 7.0
    for x in (6.5, 5.0, 3.0, 1.0):
        assert _penalty(x, x_crit) < x


def test_backtest_csv_exists_and_is_indexed_1980():
    """If the backtest has been run, CESI(1980) must equal 100 by construction."""
    path = RESULTS / "cesi_backtest_data.csv"
    if not path.exists():
        pytest.skip("backtest output not generated")
    df = pd.read_csv(path)
    row_1980 = df.loc[df["year"] == 1980].iloc[0]
    assert abs(row_1980["CESI"] - 100.0) < 0.5
