import pandas as pd

from daalab.data.macro import _monthly_asof, expanding_z


def test_monthly_series_respects_publication_lag():
    # Norgate-style: value stamped on every day of its reference month
    days = pd.date_range("2020-01-01", "2020-04-30", freq="D")
    s = pd.Series([float(d.month) for d in days], index=days)
    grid = pd.date_range("2020-01-31", "2020-06-30", freq="ME")
    out = _monthly_asof(s, "M", 1, grid)
    assert pd.isna(out.loc["2020-01-31"])           # January data is not known at the end of January
    assert out.loc["2020-02-29"] == 1.0              # ... it is known by the end of February
    assert out.loc["2020-05-31"] == 4.0
    assert out.loc["2020-06-30"] == 4.0              # carried forward until a new release


def test_quarterly_lag():
    days = pd.date_range("2020-01-01", "2020-06-30", freq="D")
    s = pd.Series([float(d.quarter) for d in days], index=days)
    grid = pd.date_range("2020-01-31", "2020-09-30", freq="ME")
    out = _monthly_asof(s, "Q", 2, grid)
    assert pd.isna(out.loc["2020-04-30"])            # Q1 GDP not usable in April
    assert out.loc["2020-05-31"] == 1.0
    assert out.loc["2020-08-31"] == 2.0


def test_expanding_z_uses_past_only():
    x = pd.Series(range(100), dtype=float)
    z1 = expanding_z(x, min_periods=10)
    x2 = x.copy(); x2.iloc[60:] = 1000.0
    z2 = expanding_z(x2, min_periods=10)
    pd.testing.assert_series_equal(z1.iloc[:60], z2.iloc[:60])   # future values never change past scores
