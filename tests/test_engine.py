"""The engine must only use data up to each rebalance date, and apply weights to the NEXT month."""
import numpy as np
import pandas as pd
import pytest

from daalab.engine.core import Context, Strategy, run


class FakePanel:
    def __init__(self, monthly: pd.DataFrame):
        self._m = monthly
        self.trade_dates = pd.Series(monthly.index, index=monthly.index)
        self.month_ends = monthly.index
        self.calendar = monthly.index
        self.partial_month = False

    def monthly_frame(self, tickers):
        return self._m[tickers]

    def daily_frame(self, tickers):
        return self._m[tickers]


def _panel():
    idx = pd.date_range("1999-01-31", periods=40, freq="ME")
    # A gains 10% in even months and B in odd months, so "last month's winner" is always wrong next month
    a = np.where(np.arange(40) % 2 == 0, 0.10, 0.0)
    b = np.where(np.arange(40) % 2 == 1, 0.10, 0.0)
    lv = pd.DataFrame({"A": np.cumprod(1 + a), "B": np.cumprod(1 + b), "BIL": np.ones(40)}, index=idx)
    return FakePanel(lv), lv


def test_weights_apply_to_next_month_only():
    panel, lv = _panel()
    s = Strategy(id="t", name="t", author="t", family="other", year=2000, source_title="", source_url="",
                 assets=["A", "B"], lookback_months=1, fn=lambda ctx: {ctx.ret(["A", "B"], 1).idxmax(): 1.0})
    res = run(s, panel, first_date="2000-01-31")
    # chasing last month's winner earns 0% every month (minus costs) in this alternating world
    assert (res.returns <= 1e-12).all()
    assert res.returns.min() > -0.0021


def test_context_sees_only_current_row():
    _, lv = _panel()
    ctx = Context(lv, None, None, pd.Series(lv.index, index=lv.index))
    ctx.i = 5
    assert ctx.px(["A"])["A"] == pytest.approx(lv["A"].iloc[5])
    assert ctx.ret(["A"], 1)["A"] == pytest.approx(lv["A"].iloc[5] / lv["A"].iloc[4] - 1)
    w = ctx.mom13612w(["A"])["A"]
    r = lambda n: lv["A"].iloc[5] / lv["A"].iloc[5 - n] - 1 if 5 - n >= 0 else np.nan
    assert np.isnan(w)  # 12-month history not available yet -> no silent look-ahead
    ctx.i = 20
    r = lambda n: lv["A"].iloc[20] / lv["A"].iloc[20 - n] - 1
    assert ctx.mom13612w(["A"])["A"] == pytest.approx(12 * r(1) + 4 * r(3) + 2 * r(6) + r(12))
    assert ctx.sma_rel(["A"], 10)["A"] == pytest.approx(lv["A"].iloc[20] / lv["A"].iloc[11:21].mean() - 1)


def test_weights_must_sum_to_one():
    panel, _ = _panel()
    s = Strategy(id="bad", name="bad", author="t", family="other", year=2000, source_title="", source_url="",
                 assets=["A"], lookback_months=1, fn=lambda ctx: {"A": 0.5})
    with pytest.raises(ValueError):
        run(s, panel, first_date="2000-01-31")
