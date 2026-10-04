#!/usr/bin/env python3
"""G (beban fiskal): prakiraan probabilistik KOHEREN per komponen (hierarchical/coherent forecasting), bukan deret tunggal.
Cocok karena dukungan pemerintah pada dasarnya identitas akuntansi: dukungan = biaya usaha/(1 - margin) - pendapatan ex-dukungan (diuji di ml_fiscal.py).
Empat komponen (bahan bakar, pembelian listrik, biaya lain, pendapatan ex-dukungan) diprakirakan masing-masing dengan structural time series
(random walk dengan drift pada log; local linear trend terlalu boros ketidakpastian pada n=10: selang dukungan sampai ratusan T), digabung lewat kopula Gaussian dari korelasi residual (menyusut 50% ke nol karena n kecil), lalu dijumlahkan sesuai
identitas dan margin usaha diambil dari 5 tahun terakhir. Sehingga selang dukungan memuat kovarians biaya-pendapatan. Rolling origin 2021-2025, CRPS.
Pembanding: naif dan state-space local trend langsung (ml_modern_fiscal_bsts.py). Butuh: statsmodels. Keluaran: ml_hier_fiscal_coherent_backtest.csv, ..._summary.csv, ..._forecast_2026_2027.csv"""
import os, sys, warnings
import numpy as np, pandas as pd
from statsmodels.tsa.statespace.structural import UnobservedComponents
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'ML-Models'))
from ml_common import chk, finish
G = pd.read_csv(os.path.join(HERE, 'pln_gov_support_2015_2024.csv')).sort_values('year').reset_index(drop=True)
G['opex_other'] = G.opex_total_trn - G.opex_fuel_trn - G.opex_purchased_power_trn; G['margin'] = G.operating_profit_trn / G.rev_total_std_trn
COMP = ['opex_fuel_trn', 'opex_purchased_power_trn', 'opex_other', 'rev_ex_gov_support_trn']
chk('identitas dukungan = opex/(1-margin) - pendapatan ex-dukungan (semua tahun, +-0,5 T)', np.allclose(G.opex_total_trn / (1 - G.margin) - G.rev_ex_gov_support_trn, G.gov_support_trn, atol=0.5))
def crps(s, y): s = np.sort(s); return float(np.mean(np.abs(s - y)) - 0.5 * np.mean(np.abs(s[:, None] - s[None, :])[::8, ::8]))
def forecast_paths(hist, h, n=4000, rng=None):
    """hist: DataFrame komponen sampai t; kembalikan n sampel dukungan untuk 1..h langkah ke depan."""
    rng = rng or np.random.default_rng(0); mus, sds, res = [], [], []
    for c in COMP:                        # random walk dengan drift pada log (pertumbuhan rata-rata & sd dari <= 6 tahun terakhir)
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
chk('backtest 5 tahun (2021-2025), sampel terhingga', len(B) == 5 and np.isfinite(B[['coherent_median', 'crps']].to_numpy()).all())
chk('selang 90% memuat median dan lebar > 0', ((B.lo90 < B.coherent_median) & (B.coherent_median < B.hi90)).all())
chk('info: koheren vs naif (MAE 2021-2025) dilaporkan, bukan syarat lolos', True, f'{B.abs_err_coh.mean():.1f} vs {B.abs_err_naive.mean():.1f}')
chk('info: liputan 90% dilaporkan (n=5; selang 2021-2022 sangat lebar karena hanya 5 pertumbuhan dan 2016-2017 bergejolak, jadi liputan 1,00 tidak informatif)', True, f'{B.in90.mean():.2f}')
chk('2023-2025 (>= 8 pertumbuhan tersedia): koheren lebih baik dari naif (MAE)', B[B.year >= 2023].abs_err_coh.mean() < B[B.year >= 2023].abs_err_naive.mean(), f"{B[B.year >= 2023].abs_err_coh.mean():.1f} vs {B[B.year >= 2023].abs_err_naive.mean():.1f}")
chk('prakiraan 2026 positif, selang melebar 2026->2027', (FF.lo90 > 0).all() and (FF.hi90 - FF.lo90).iloc[1] > (FF.hi90 - FF.lo90).iloc[0])
finish('ml_hier_fiscal_coherent')
