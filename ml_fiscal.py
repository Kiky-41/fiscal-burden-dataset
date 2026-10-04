#!/usr/bin/env python3
"""G (beban fiskal): ML/backtest pada pln_gov_support_2015_2024.csv (sebenarnya 2015-2025, n=11).
1) Backtest rolling-origin (naif, rata2 3 tahun, tren 5 tahun) untuk dukungan pemerintah, porsi thd pendapatan, piutang pemerintah,
   selisih akrual-kas; 2025 = uji luar-sampel (latih 2015-2024).
2) Model 'celah biaya': gov_support ~ (opex_total - rev_ex_gov_support) via OLS leave-one-year-out; sisa = laba usaha yang ditopang.
3) Monte Carlo 2026: bootstrap pertumbuhan tahunan opex & pendapatan ex-dukungan 2016-2025 -> sebaran dukungan yang dibutuhkan agar
   margin laba usaha 2026 = margin 2025; dilaporkan sebagai rentang kondisional, BUKAN prakiraan resmi.
Keluaran: ml_fiscal_macro_realized_link.csv, ml_fiscal_backtest.csv, ml_fiscal_2025_forecast.csv, ml_fiscal_gap_model.csv, ml_fiscal_mc_2026.csv"""
import os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'ML-Models'))
from ml_common import *

G = pd.read_csv(os.path.join(HERE, 'pln_gov_support_2015_2024.csv')).sort_values('year').reset_index(drop=True)
chk('2015-2025 lengkap', list(G.year) == list(range(2015, 2026)))
TG = ['gov_support_trn', 'gov_support_share_rev_pct', 'govt_receivable_trn', 'accrual_minus_cash_trn']
def f_naive(y): return y[-1]
def f_mean3(y): return float(np.mean(y[-3:]))
def f_trend(y):
    yy = y[-5:]; b = np.polyfit(np.arange(len(yy)), yy, 1); return float(np.clip(b[0] * len(yy) + b[1], min(y) - .25 * np.ptp(y), max(y) + .25 * np.ptp(y)))
MODELS = {'naive_last': f_naive, 'mean_last3': f_mean3, 'trend5': f_trend}
rows = []
for t in TG:
    s = G[['year', t]].dropna().reset_index(drop=True)
    for i in range(4, len(s)):
        y = s[t].to_numpy()[:i]
        for m, f in MODELS.items(): rows.append(dict(target=t, model=m, year=int(s.year[i]), actual=float(s[t][i]), pred=float(f(y))))
B = pd.DataFrame(rows); B['abs_err'] = (B.actual - B.pred).abs(); B.to_csv(os.path.join(HERE, 'ml_fiscal_backtest.csv'), index=False)
hist = B[B.year <= 2024].groupby(['target', 'model']).abs_err.mean().rename('mae_hist')
o25 = B[B.year == 2025].set_index(['target', 'model'])[['actual', 'pred', 'abs_err']].rename(columns={'abs_err': 'abs_err_2025'})
F = o25.join(hist).reset_index(); F['error_ratio'] = F.abs_err_2025 / F.mae_hist; F['surprise_flag'] = (F.error_ratio > 2).astype(int)
F.to_csv(os.path.join(HERE, 'ml_fiscal_2025_forecast.csv'), index=False); print(F.round(3).to_string(index=False))

# celah biaya
G['gap'] = G.opex_total_trn - G.rev_ex_gov_support_trn
x, y = G.gap.to_numpy(), G.gov_support_trn.to_numpy()
p = np.full(len(G), np.nan)
for i in range(len(G)):
    k = np.arange(len(G)) != i; b = np.polyfit(x[k], y[k], 1); p[i] = b[0] * x[i] + b[1]
bfull = np.polyfit(x[:-1], y[:-1], 1); pred25 = bfull[0] * x[-1] + bfull[1]
GM = pd.DataFrame(dict(year=G.year, gap_trn=x, gov_support_trn=y, loyo_pred=p, loyo_resid=y - p, operating_profit_trn=G.operating_profit_trn))
GM.to_csv(os.path.join(HERE, 'ml_fiscal_gap_model.csv'), index=False); print(GM.round(2).to_string(index=False))
print('slope/intercept (2015-2024):', np.round(bfull, 3), 'pred 2025:', round(pred25, 2), 'aktual:', round(y[-1], 2))
# identitas: gov = op_profit + gap  (op_profit_ex = rev_ex - opex ; op_profit = rev_ex + gov - opex)
chk('identitas laba usaha = pendapatan ex-dukungan + dukungan - opex (toleransi 0.5 T)', np.allclose(G.operating_profit_trn, G.rev_ex_gov_support_trn + G.gov_support_trn - G.opex_total_trn, atol=0.5),
    f'maks selisih {np.abs(G.operating_profit_trn - (G.rev_ex_gov_support_trn + G.gov_support_trn - G.opex_total_trn)).max():.2f}')
chk('celah biaya: LOYO R2 > 0.8', r2(y, p) > 0.8, f'{r2(y, p):.3f}')
chk('celah biaya memprediksi 2025 dalam 25% (jika tidak, ada perubahan struktur)', abs(pred25 - y[-1]) / y[-1] < .25, f'{pred25:.1f} vs {y[-1]:.1f}')

# Monte Carlo 2026
rng = np.random.default_rng(11)
gO = np.log(G.opex_total_trn).diff().dropna().to_numpy(); gR = np.log(G.rev_ex_gov_support_trn).diff().dropna().to_numpy()
op25, rv25, m25 = G.opex_total_trn.iloc[-1], G.rev_ex_gov_support_trn.iloc[-1], G.operating_profit_trn.iloc[-1] / G.rev_total_std_trn.iloc[-1]
need = []
for _ in range(10000):
    i = rng.integers(0, len(gO)); o, r = op25 * np.exp(gO[i]), rv25 * np.exp(gR[i])   # tahun bootstrap sama -> korelasi biaya-pendapatan terjaga
    need.append(o / (1 - m25) - r)      # (r+g-o)/(r+g) = m25  ->  g = o/(1-m25) - r
need = np.array(need)
MC = pd.DataFrame([dict(stat=k, value=float(v)) for k, v in zip(['p05', 'p25', 'p50', 'p75', 'p95', 'mean', 'gov_support_2025', 'prob_gt_2025'],
     [*np.percentile(need, [5, 25, 50, 75, 95]), need.mean(), y[-1], (need > y[-1]).mean()])])
MC.to_csv(os.path.join(HERE, 'ml_fiscal_mc_2026.csv'), index=False); print(MC.round(3).to_string(index=False))
chk('MC: pertumbuhan nol mereproduksi dukungan 2025 (uji rumus)', abs(op25 / (1 - m25) - rv25 - y[-1]) < 0.5, f'{op25 / (1 - m25) - rv25:.2f} vs {y[-1]:.2f}')
chk('MC: sebaran wajar (p05<p50<p95, positif)', 0 < np.percentile(need, 5) < np.percentile(need, 50) < np.percentile(need, 95))
chk('MC 2026 mendekati 2025 (median dalam 40%)', abs(np.median(need) - y[-1]) / y[-1] < .4, f'median {np.median(need):.1f} vs 2025 {y[-1]:.1f}')
chk('piutang pemerintah 2025 = 110,7 T (lonjakan dicatat)', abs(G.govt_receivable_trn.iloc[-1] - 110.74) < 0.05, f'{G.govt_receivable_trn.iloc[-1]:.2f}')

# makro realisasi (ICP, kurs) vs biaya energi PLN: 2020-2023 dari tabel APBN berstatus LKPP (realisasi), 2024-2025 dari LKPP 2025 (news_updates)
AP = pd.read_csv(os.path.join(HERE, 'apbn_energy_subsidy_2020_2025.csv')).set_index('year')
NU = pd.read_csv(os.path.join(HERE, 'news_updates_2024_2026.csv'))
def nu(item, yr): return float(NU[(NU.item == item) & (NU.year == yr)].value.iloc[0])
icp = {y: float(AP.loc[y, 'icp_usd_bbl']) for y in (2020, 2021, 2022, 2023)}; icp[2024] = nu('macro_realized_icp_usd_bbl', 2024); icp[2025] = nu('macro_realized_icp_usd_bbl', 2025)
fx = {y: float(AP.loc[y, 'usdidr_avg']) for y in (2020, 2021, 2022, 2023)}; fx[2025] = nu('macro_realized_usdidr_avg', 2025)
G2 = G.set_index('year'); G2['energy_cost'] = G2.opex_fuel_trn + G2.opex_purchased_power_trn
yrs = [2020, 2021, 2022, 2023, 2024, 2025]
M = pd.DataFrame(dict(year=yrs, icp_realized=[icp[y] for y in yrs], energy_cost_trn=[G2.energy_cost[y] for y in yrs], gov_support_trn=[G2.gov_support_trn[y] for y in yrs]))
M['d_icp_pct'] = M.icp_realized.pct_change() * 100; M['d_energy_cost_pct'] = M.energy_cost_trn.pct_change() * 100; M['d_gov_support_pct'] = M.gov_support_trn.pct_change() * 100
M.to_csv(os.path.join(HERE, 'ml_fiscal_macro_realized_link.csv'), index=False); print(M.round(1).to_string(index=False))
rho = spearman(M.d_icp_pct[1:], M.d_energy_cost_pct[1:])
chk('ICP realisasi 2025 turun 13.8% tetapi biaya energi PLN 2025 tidak turun (ICP bukan pendorong tunggal; penyebabnya tidak diuji di sini)', M.d_icp_pct.iloc[-1] < -10 and M.d_energy_cost_pct.iloc[-1] > -10,
    f"dICP {M.d_icp_pct.iloc[-1]:.1f}% ; dBiaya {M.d_energy_cost_pct.iloc[-1]:.1f}% ; dDukungan {M.d_gov_support_pct.iloc[-1]:.1f}%")
chk('Spearman dICP vs dBiaya energi (n=5) dilaporkan, bukan syarat', True, f'{rho:.2f} (n=5, tanpa inferensi)')
chk('kurs realisasi 2025 melemah vs asumsi APBN (16.475 > 16.000); 2025 vs 2023: +8%', fx[2025] > 16000 and fx[2025] / fx[2023] > 1.05, f'{fx[2025] / fx[2023] - 1:.3f}')
finish('ml_fiscal')
