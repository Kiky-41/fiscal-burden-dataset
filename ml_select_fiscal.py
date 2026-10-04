#!/usr/bin/env python3
"""G (fiscal burden): selecting a government-support forecasting method on out-of-sample performance (rolling origins 2021-2025, min. training 6 years).
Candidates (all pre-specified): naive, 3-year mean, linear drift (full/5y), log drift (full/3y/5y), damped Holt, level ETS,
component-coherent (support identity = opex/(1-margin) - ex-support revenue; deterministic median), and coherent+log-drift mean.
Nested selection: for each test year, the winner is chosen only from PRIOR years' errors (2021 uses naive). Outputs: ml_select_fiscal_scores.csv, ml_select_fiscal_nested.csv.
Warning: n_test = 5, so method differences are almost surely insignificant; results reported as-is."""
import os, sys, warnings
import numpy as np, pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'ML-Models'))
from ml_common import chk, finish
G = pd.read_csv(os.path.join(HERE, 'pln_gov_support_2015_2024.csv')).sort_values('year').reset_index(drop=True)
G['opex_other'] = G.opex_total_trn - G.opex_fuel_trn - G.opex_purchased_power_trn; G['margin'] = G.operating_profit_trn / G.rev_total_std_trn
COMP = ['opex_fuel_trn', 'opex_purchased_power_trn', 'opex_other', 'rev_ex_gov_support_trn']
def logdrift(s, k=None):
    y = np.log(np.asarray(s, float)); g = np.diff(y); g = g[-k:] if k else g; return float(np.exp(y[-1] + g.mean()))
def lindrift(s, k=None):
    y = np.asarray(s, float); g = np.diff(y); g = g[-k:] if k else g; return float(y[-1] + g.mean())
def holt(s):
    try: return float(ExponentialSmoothing(np.asarray(s, float), trend='add', damped_trend=True).fit().forecast(1)[0])
    except Exception: return float(s[-1])
def ets(s):
    try: return float(ExponentialSmoothing(np.asarray(s, float), trend=None).fit().forecast(1)[0])
    except Exception: return float(s[-1])
def coherent(h, k=6):
    v = {c: logdrift(h[c], k) for c in COMP}; m = float(np.median(h.margin.to_numpy()[-5:]))
    return (v[COMP[0]] + v[COMP[1]] + v[COMP[2]]) / (1 - m) - v[COMP[3]]
CAND = {'naif': lambda h: float(h.gov_support_trn.iloc[-1]), 'rata3': lambda h: float(h.gov_support_trn.iloc[-3:].mean()),
        'drift_lin_all': lambda h: lindrift(h.gov_support_trn), 'drift_lin_5': lambda h: lindrift(h.gov_support_trn, 5),
        'drift_log_all': lambda h: logdrift(h.gov_support_trn), 'drift_log_3': lambda h: logdrift(h.gov_support_trn, 3), 'drift_log_5': lambda h: logdrift(h.gov_support_trn, 5),
        'holt_teredam': lambda h: holt(h.gov_support_trn), 'ets_level': lambda h: ets(h.gov_support_trn), 'koheren_komponen': coherent}
CAND['ens_koheren+drift_log_5'] = lambda h: 0.5 * coherent(h) + 0.5 * logdrift(h.gov_support_trn, 5)
rows = []
for i in range(6, len(G)):
    h = G.iloc[:i]; a = float(G.gov_support_trn[i])
    for n, f in CAND.items(): p = f(h); rows.append(dict(year=int(G.year[i]), model=n, pred=p, actual=a, abs_err=abs(p - a)))
R = pd.DataFrame(rows); W = R.pivot(index='year', columns='model', values='abs_err')
S = pd.DataFrame(dict(mae_2021_2025=W.mean(), mae_2023_2025=W.loc[2023:].mean(), max_err=W.max())).sort_values('mae_2021_2025'); S['rank'] = range(1, len(S) + 1)
S.to_csv(os.path.join(HERE, 'ml_select_fiscal_scores.csv')); print(S.round(1).to_string())
nest = []
for y in W.index:
    prev = W.loc[:y - 1]; ch = 'naif' if len(prev) == 0 else prev.mean().idxmin(); nest.append(dict(year=y, chosen=ch, abs_err=W.loc[y, ch], abs_err_naif=W.loc[y, 'naif'], abs_err_best_static=W.loc[y, S.index[0]]))
N = pd.DataFrame(nest); N.to_csv(os.path.join(HERE, 'ml_select_fiscal_nested.csv'), index=False); print(N.round(1).to_string(index=False))
best = S.index[0]; print('best:', best, 'nested MAE', round(N.abs_err.mean(), 1), 'naive', round(N.abs_err_naif.mean(), 1))
p26 = CAND[best](G); print('2026 forecast (point)', round(p26, 1), '2025 actual', round(G.gov_support_trn.iloc[-1], 1))
pd.DataFrame([dict(model=best, pred_2026=p26)]).to_csv(os.path.join(HERE, 'ml_select_fiscal_pred_2026.csv'), index=False)
chk('5-year x %d-candidate backtest complete' % len(CAND), R.shape[0] == 5 * len(CAND) and np.isfinite(R.pred).all())
chk('support identity (all years, +-0.5 T)', np.allclose(G.opex_total_trn / (1 - G.margin) - G.rev_ex_gov_support_trn, G.gov_support_trn, atol=0.5))
chk('info: best vs naive MAE (static)', True, f'{S.mae_2021_2025.iloc[0]:.1f} vs {S.loc["naif","mae_2021_2025"]:.1f}')
chk('info: nested vs naive MAE (honest, no look-ahead)', True, f'{N.abs_err.mean():.1f} vs {N.abs_err_naif.mean():.1f}')
finish('ml_select_fiscal')
