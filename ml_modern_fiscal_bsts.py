#!/usr/bin/env python3
"""G (beban fiskal), model modern: state-space local linear trend (Unobserved Components, statsmodels state-space + Kalman filter, maximum likelihood; bukan Bayesian -- tanpa prior/posterior)
dengan selang prediksi. Target: dukungan pemerintah (subsidi+kompensasi, Rp T) dan piutang pemerintah, 2015-2025. Rolling origin 2020-2025;
2025 = uji luar-sampel. Ditambah prakiraan 2026-2027 (kondisional, bukan resmi). Dibandingkan dengan naif dan tren dari ml_fiscal.py.
Butuh: statsmodels. Keluaran: ml_modern_fiscal_bsts_backtest.csv, ml_modern_fiscal_bsts_2025.csv, ml_modern_fiscal_bsts_forecast_2026_2027.csv"""
import os, sys, warnings
import numpy as np, pandas as pd
from statsmodels.tsa.statespace.structural import UnobservedComponents
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'ML-Models'))
from ml_common import chk, finish
G = pd.read_csv(os.path.join(HERE, 'pln_gov_support_2015_2024.csv')).sort_values('year').reset_index(drop=True)
chk('2015-2025', list(G.year) == list(range(2015, 2026)))
def fc(y, h=1):
    m = UnobservedComponents(np.asarray(y, float), level='local linear trend').fit(disp=False, maxiter=200)
    f = m.get_forecast(h); ci = f.conf_int(alpha=0.10); return f.predicted_mean, np.sqrt(f.var_pred_mean), ci
rows = []
for tg in ['gov_support_trn', 'govt_receivable_trn', 'accrual_minus_cash_trn']:
    s = G[['year', tg]].dropna().reset_index(drop=True)
    mt = 6 if len(s) >= 11 else 4          # deret pendek (piutang mulai 2020) memakai latih minimal 4
    for i in range(mt, len(s)):
        y = s[tg].to_numpy()[:i]; mu, sd, ci = fc(y); a = float(s[tg][i])
        rows.append(dict(target=tg, year=int(s.year[i]), actual=a, bsts=float(mu[0]), sd=float(sd[0]), lo90=float(ci[0, 0]), hi90=float(ci[0, 1]), naive=float(y[-1]), z=(a - float(mu[0])) / float(sd[0])))
B = pd.DataFrame(rows); B['abs_err_bsts'] = (B.actual - B.bsts).abs(); B['abs_err_naive'] = (B.actual - B.naive).abs(); B['in90'] = ((B.actual >= B.lo90) & (B.actual <= B.hi90)).astype(int)
B.to_csv(os.path.join(HERE, 'ml_modern_fiscal_bsts_backtest.csv'), index=False)
H = B[B.year <= 2024].groupby('target').agg(mae_bsts=('abs_err_bsts', 'mean'), mae_naive=('abs_err_naive', 'mean'), coverage90=('in90', 'mean'), n=('year', 'count')).reset_index()
Y = B[B.year == 2025][['target', 'actual', 'bsts', 'sd', 'lo90', 'hi90', 'z', 'in90']].merge(H, on='target'); Y.to_csv(os.path.join(HERE, 'ml_modern_fiscal_bsts_2025.csv'), index=False); print(Y.round(2).to_string(index=False))
# prakiraan 2026-2027 dari seluruh data 2015-2025
F = []
for tg in ['gov_support_trn', 'govt_receivable_trn']:
    mu, sd, ci = fc(G[tg].to_numpy(), h=2)
    for k in range(2): F.append(dict(target=tg, year=2026 + k, mean=float(mu[k]), sd=float(sd[k]), lo90=float(ci[k, 0]), hi90=float(ci[k, 1])))
F = pd.DataFrame(F); F.to_csv(os.path.join(HERE, 'ml_modern_fiscal_bsts_forecast_2026_2027.csv'), index=False); print(F.round(1).to_string(index=False))
chk('backtest lengkap', B[['bsts', 'sd']].notna().all().all() and len(B) == sum(len(G[['year', t]].dropna()) - (6 if len(G[['year', t]].dropna()) >= 11 else 4) for t in ['gov_support_trn', 'govt_receivable_trn', 'accrual_minus_cash_trn']), str(len(B)))
chk('sd > 0 dan selang mencakup rata-rata', (B.sd > 0).all() and ((B.lo90 <= B.bsts) & (B.bsts <= B.hi90)).all())
chk('info: state-space vs naif (MAE) dilaporkan, bukan syarat lolos', True, f'state-space menang di {(H.mae_bsts < H.mae_naive).sum()}/3 target')
chk('prakiraan 2026 dukungan > 0 dan selang melebar dari 2026 ke 2027', (F[(F.target == 'gov_support_trn')].lo90 > 0).all() and F[(F.target == 'gov_support_trn')].sd.iloc[1] > F[(F.target == 'gov_support_trn')].sd.iloc[0])
d = Y[Y.target == 'govt_receivable_trn'].iloc[0]
chk('info: piutang pemerintah 2025 (110,7 T) di dalam selang 90% state-space karena deret pendek (selang sangat lebar); kejutan tidak terdeteksi model ini', True, f'z={d.z:.1f}, in90={int(d.in90)}, sd={d.sd:.0f}')
finish('ml_modern_fiscal_bsts')
