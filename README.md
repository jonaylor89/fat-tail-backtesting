# Convex Risk Notebook

Companion notebook for the post “Algo Backtests Are Lying to You.” It recreates the article’s synthetic experiments, then reruns the same ideas on live SPY and BTC-USD candles via `backtesting.py`.

## Quick start
- Install deps with `uv sync` (or `uv pip install -r pyproject.toml`).
- Launch Jupyter: `uv run --frozen jupyter lab` (or `uv run --frozen jupyter notebook`).
- Open `python/convex.ipynb` and run cells top-down. Section 6 fetches real data; you’ll need network access for the `yfinance` pulls.

## Notebook map
1. Gaussian comfort zone — deterministic SMA edges in a tidy world.
2. Fat tails, shocks, quantile payoffs, and Monte Carlo convex/concave contrasts.
3. Regime-shift stress test synthesizer.
4. Real-data sanity check with `backtesting.py` across SPY and BTC regimes.

Feel free to adjust the RNG seed, regime definitions, or add your own instruments to falsify strategies faster.
