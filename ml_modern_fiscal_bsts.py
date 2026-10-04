#!/usr/bin/env python3
"""G (fiscal burden), modern model: state-space local linear trend (Unobserved Components, statsmodels state-space + Kalman filter, maximum likelihood; not Bayesian -- no priors/posteriors)
with prediction intervals. Targets: government support (subsidy+compensation, Rp T) and government receivables, 2015-2025. Rolling origins 2020-2025;
2025 = out-of-sample test. Plus 2026-2027 forecasts (conditional, not official). Compared against naive and trend from ml_fiscal.py.
Needs: statsmodels. Outputs: ml_modern_fiscal_bsts_backtest.csv, ml_modern_fiscal_bsts_2025.csv, ml_modern_fiscal_bsts_forecast_2026_2027.csv"""
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
    mt = 6 if len(s) >= 11 else 4          # short series (receivables start 2020) use min training 4
    for i in range(mt, len(s)):
        y = s[tg].to_numpy()[:i]; mu, sd, ci = fc(y); a = float(s[tg][i])
        rows.append(dict(target=tg, year=int(s.year[i]), actual=a, bsts=float(mu[0]), sd=float(sd[0]), lo90=float(ci[0, 0]), hi90=float(ci[0, 1]), naive=float(y[-1]), z=(a - float(mu[0])) / float(sd[0])))
B = pd.DataFrame(rows); B['abs_err_bsts'] = (B.actual - B.bsts).abs(); B['abs_err_naive'] = (B.actual - B.naive).abs(); B['in90'] = ((B.actual >= B.lo90) & (B.actual <= B.hi90)).astype(int)
B.to_csv(os.path.join(HERE, 'ml_modern_fiscal_bsts_backtest.csv'), index=False)
H = B[B.year <= 2024].groupby('target').agg(mae_bsts=('abs_err_bsts', 'mean'), mae_naive=('abs_err_naive', 'mean'), coverage90=('in90', 'mean'), n=('year', 'count')).reset_index()
Y = B[B.year == 2025][['target', 'actual', 'bsts', 'sd', 'lo90', 'hi90', 'z', 'in90']].merge(H, on='target'); Y.to_csv(os.path.join(HERE, 'ml_modern_fiscal_bsts_2025.csv'), index=False); print(Y.round(2).to_string(index=False))
# 2026-2027 forecasts from full 2015-2025 data
F = []
for tg in ['gov_support_trn', 'govt_receivable_trn']:
    mu, sd, ci = fc(G[tg].to_numpy(), h=2)
    for k in range(2): F.append(dict(target=tg, year=2026 + k, mean=float(mu[k]), sd=float(sd[k]), lo90=float(ci[k, 0]), hi90=float(ci[k, 1])))
F = pd.DataFrame(F); F.to_csv(os.path.join(HERE, 'ml_modern_fiscal_bsts_forecast_2026_2027.csv'), index=False); print(F.round(1).to_string(index=False))
chk('complete backtest', B[['bsts', 'sd']].notna().all().all() and len(B) == sum(len(G[['year', t]].dropna()) - (6 if len(G[['year', t]].dropna()) >= 11 else 4) for t in ['gov_support_trn', 'govt_receivable_trn', 'accrual_minus_cash_trn']), str(len(B)))
chk('sd > 0 and intervals contain mean', (B.sd > 0).all() and ((B.lo90 <= B.bsts) & (B.bsts <= B.hi90)).all())
chk('info: state-space vs naive (MAE) reported, not a pass condition', True, f'state-space wins in {(H.mae_bsts < H.mae_naive).sum()}/3 targets')
chk('2026 support forecast > 0 with intervals widening 2026 to 2027', (F[(F.target == 'gov_support_trn')].lo90 > 0).all() and F[(F.target == 'gov_support_trn')].sd.iloc[1] > F[(F.target == 'gov_support_trn')].sd.iloc[0])
d = Y[Y.target == 'govt_receivable_trn'].iloc[0]
chk('info: 2025 government receivables (110.7 T) inside state-space 90% interval due to short series (very wide interval); surprise not detected by this model', True, f'z={d.z:.1f}, in90={int(d.in90)}, sd={d.sd:.0f}')
finish('ml_modern_fiscal_bsts')
