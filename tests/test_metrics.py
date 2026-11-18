import numpy as np
import pandas as pd
import pytest

from daalab.engine import metrics as mt


def _idx(n):
    return pd.date_range("2000-01-31", periods=n, freq="ME")


def test_cagr_constant_growth():
    r = pd.Series([0.01] * 24, index=_idx(24))
    assert mt.cagr(r) == pytest.approx(1.01 ** 12 - 1)


def test_drawdown_and_ulcer():
    r = pd.Series([0.10, -0.50, 0.20], index=_idx(3))
    dd = mt.drawdown(r)
    assert dd.min() == pytest.approx(-0.50)
    assert dd.iloc[-1] == pytest.approx(1.1 * 0.5 * 1.2 / 1.1 - 1)


def test_summary_against_hand_calculation():
    rng = np.random.default_rng(0)
    r = pd.Series(rng.normal(0.006, 0.03, 120), index=_idx(120))
    rf = pd.Series(0.001, index=r.index)
    m = mt.summarize(r, rf)
    ex = r - rf
    assert m["sharpe"] == pytest.approx(ex.mean() * 12 / (ex.std() * np.sqrt(12)))
    assert m["vol"] == pytest.approx(r.std() * np.sqrt(12))
    assert m["pct_pos"] == pytest.approx((r > 0).mean())
    assert m["max_dd"] <= 0


def test_worst_year_uses_full_years_only():
    r = pd.Series([0.01] * 12 + [-0.2], index=_idx(13))   # one bad month in a partial year
    m = mt.summarize(r, pd.Series(0.0, index=r.index))
    assert m["worst_year"] == pytest.approx(1.01 ** 12 - 1)
