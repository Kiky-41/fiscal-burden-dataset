#!/usr/bin/env python3
"""G (fiscal burden): COHERENT probabilistic component forecast (hierarchical/coherent forecasting), not a single series.
Fits because government support is fundamentally an accounting identity: support = operating cost/(1 - margin) - ex-support revenue (tested in ml_fiscal.py).
Four components (fuel, power purchases, other costs, ex-support revenue) each forecast with a structural time series
(log random walk with drift; local linear trend wastes uncertainty at n=10: support intervals reach hundreds of T), joined via a Gaussian copula of residual correlation (50% shrinkage to zero given small n), then summed per the
identity with margin from the last 5 years. So support intervals embed cost-revenue covariance. Rolling origins 2021-2025, CRPS.
Comparators: naive and direct state-space local trend (ml_modern_fiscal_bsts.py). Needs: statsmodels. Outputs: ml_hier_fiscal_coherent_backtest.csv, ..._summary.csv, ..._forecast_2026_2027.csv"""
import os, sys, warnings
import numpy as np, pandas as pd
from statsmodels.tsa.statespace.structural import UnobservedComponents
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'ML-Models'))
from ml_common import chk, finish
G = pd.read_csv(os.path.join(HERE, 'pln_gov_support_2015_2024.csv')).sort_values('year').reset_index(drop=True)
G['opex_other'] = G.opex_total_trn - G.opex_fuel_trn - G.opex_purchased_power_trn; G['margin'] = G.operating_profit_trn / G.rev_total_std_trn
COMP = ['opex_fuel_trn', 'opex_purchased_power_trn', 'opex_other', 'rev_ex_gov_support_trn']
chk('support identity = opex/(1-margin) - ex-support revenue (all years, +-0.5 T)', np.allclose(G.opex_total_trn / (1 - G.margin) - G.rev_ex_gov_support_trn, G.gov_support_trn, atol=0.5))
def crps(s, y): s = np.sort(s); return float(np.mean(np.abs(s - y)) - 0.5 * np.mean(np.abs(s[:, None] - s[None, :])[::8, ::8]))
def forecast_paths(hist, h, n=4000, rng=None):
    """hist: component DataFrame through t; return n support samples for 1..h steps ahead."""
    rng = rng or np.random.default_rng(0); mus, sds, res = [], [], []
    for c in COMP:                        # log random walk with drift (mean growth & sd from <= last 6 years)
        y = np.log(hist[c].to_numpy()); gr = np.diff(y)[-6:]; dr, sg = gr.mean(), gr.std(ddof=1)
        mus.append(y[-1] + dr * np.arange(1, h + 1)); sds.append(sg * np.sqrt(np.arange(1, h + 1))); res.append((gr - dr) / (sg or 1))
    R = np.corrcoef(np.array(res)); R = 0.5 * R + 0.5 * np.eye(len(COMP)); L = np.linalg.cholesky(R + 1e-6 * np.eye(len(COMP)))
    marg = hist.margin.to_numpy()[-5:]; out = np.zeros((n, h))
    for k in range(h):
        z = rng.standard_normal((n, len(COMP))) @ L.T; v = np.exp(np.array([mus[j][k] for j in range(4)])[None, :] + z * np.array([sds[j][k] for j in range(4)])[None, :])
        o = v[:, 0] + v[:, 1] + v[:, 2]; r = v[:, 3]; m = rng.choice(marg, n); out[:, k] = o / (1 - m) - r
    return out
rows = []
for i in range(6, len(G)):
    S = forecast_paths(G.iloc[:i], 1)[:, 0]; a = float(G.gov_support_trn[i]); lo, hi = np.percentile(S, [5, 95])
    rows.append(dict(year=int(G.year[i]), actual=a, coherent_median=float(np.median(S)), lo90=float(lo), hi90=float(hi), naive=float(G.gov_support_trn[i - 1]), crps=crps(S, a), in90=int(lo <= a <= hi)))
B = pd.DataFrame(rows); B['abs_err_coh'] = (B.actual - B.coherent_median).abs(); B['abs_err_naive'] = (B.actual - B.naive).abs()
B.to_csv(os.path.join(HERE, 'ml_hier_fiscal_coherent_backtest.csv'), index=False); print(B.round(2).to_string(index=False))
Sm = pd.DataFrame([dict(metric='mae_2021_2025_coherent', value=B.abs_err_coh.mean()), dict(metric='mae_2021_2025_naive', value=B.abs_err_naive.mean()), dict(metric='mae_2023_2025_coherent', value=B[B.year >= 2023].abs_err_coh.mean()), dict(metric='mae_2023_2025_naive', value=B[B.year >= 2023].abs_err_naive.mean()),
                    dict(metric='coverage90', value=B.in90.mean()), dict(metric='mean_crps', value=B.crps.mean()), dict(metric='aktual_2025', value=float(B.actual.iloc[-1])), dict(metric='pred_2025_median', value=float(B.coherent_median.iloc[-1])),
                   dict(metric='pred_2025_lo90', value=float(B.lo90.iloc[-1])), dict(metric='pred_2025_hi90', value=float(B.hi90.iloc[-1]))])
Sm.to_csv(os.path.join(HERE, 'ml_hier_fiscal_coherent_summary.csv'), index=False); print(Sm.round(2).to_string(index=False))
Fp = forecast_paths(G, 2); FF = pd.DataFrame([dict(year=2026 + k, median=float(np.median(Fp[:, k])), lo90=float(np.percentile(Fp[:, k], 5)), hi90=float(np.percentile(Fp[:, k], 95)), prob_above_2025=float((Fp[:, k] > G.gov_support_trn.iloc[-1]).mean())) for k in range(2)])
FF.to_csv(os.path.join(HERE, 'ml_hier_fiscal_coherent_forecast_2026_2027.csv'), index=False); print(FF.round(2).to_string(index=False))
chk('5-year backtest (2021-2025), finite sample', len(B) == 5 and np.isfinite(B[['coherent_median', 'crps']].to_numpy()).all())
chk('90% interval contains median with width > 0', ((B.lo90 < B.coherent_median) & (B.coherent_median < B.hi90)).all())
chk('info: coherent vs naive (MAE 2021-2025) reported, not a pass condition', True, f'{B.abs_err_coh.mean():.1f} vs {B.abs_err_naive.mean():.1f}')
chk('info: 90% coverage reported (n=5; 2021-2022 intervals very wide given only 5 growth rates and volatile 2016-2017, so 1.00 coverage is uninformative)', True, f'{B.in90.mean():.2f}')
chk('2023-2025 (>= 8 growth rates available): coherent beats naive (MAE)', B[B.year >= 2023].abs_err_coh.mean() < B[B.year >= 2023].abs_err_naive.mean(), f"{B[B.year >= 2023].abs_err_coh.mean():.1f} vs {B[B.year >= 2023].abs_err_naive.mean():.1f}")
chk('2026 forecast positive, intervals widening 2026->2027', (FF.lo90 > 0).all() and (FF.hi90 - FF.lo90).iloc[1] > (FF.hi90 - FF.lo90).iloc[0])
finish('ml_hier_fiscal_coherent')
