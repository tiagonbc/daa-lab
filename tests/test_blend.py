"""The blend's yearly selection must depend only on returns known at the selection date."""
import numpy as np
import pandas as pd

from daalab.blend.selection import BlendConfig, select, walk_forward


def _returns(seed=1, n=180, k=12):
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2005-01-31", periods=n, freq="ME")
    base = rng.normal(0.005, 0.02, n)
    data = {f"s{i}": base * (i % 3) / 2 + rng.normal(0.004 + 0.0005 * i, 0.03, n) for i in range(k)}
    return pd.DataFrame(data, index=idx), pd.Series(0.001, index=idx)


def test_selection_ignores_future_returns():
    R, rf = _returns()
    cfg = BlendConfig(n=4)
    asof = R.index[100]
    a = select(R, rf, asof, cfg).chosen
    R2 = R.copy()
    R2.iloc[101:] = R2.iloc[101:] * -5          # scramble everything after the selection date
    b = select(R2, rf, asof, cfg).chosen
    assert a == b


def test_correlation_cap_is_respected():
    R, rf = _returns()
    R["clone"] = R["s11"] + 1e-6               # a near-duplicate of the best strategy
    cfg = BlendConfig(n=4, corr_cap=0.7)
    s = select(R, rf, R.index[-1], cfg)
    assert not {"s11", "clone"} <= set(s.chosen)


def test_walk_forward_returns_start_after_first_selection():
    R, rf = _returns()
    out, sels, _ = walk_forward(R, rf, BlendConfig(n=3))
    assert out.index[0] > sels[0].date
    assert all(s.date.month == 12 for s in sels)
