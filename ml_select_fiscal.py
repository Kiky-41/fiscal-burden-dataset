#!/usr/bin/env python3
"""G (beban fiskal): pemilihan metode prakiraan dukungan pemerintah berdasarkan kinerja out-of-sample (rolling origin 2021-2025, min. latih 6 tahun).
Kandidat (semua ditetapkan di muka): naif, rata-rata 3 tahun, drift linear (semua/5 th), drift log (semua/3 th/5 th), Holt teredam, ETS-aditif,
koheren per komponen (identitas dukungan = opex/(1-margin) - pendapatan ex-dukungan; median deterministik), serta rata-rata koheren+drift-log.
Seleksi bersarang: untuk tiap tahun uji, pemenang dipilih hanya dari galat tahun-tahun SEBELUMNYA (2021 memakai naif). Keluaran: ml_select_fiscal_scores.csv, ml_select_fiscal_nested.csv.
Peringatan: n uji = 5, jadi selisih antar-metode hampir pasti tidak signifikan; hasil dilaporkan apa adanya."""
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
best = S.index[0]; print('terbaik:', best, 'nested MAE', round(N.abs_err.mean(), 1), 'naif', round(N.abs_err_naif.mean(), 1))
p26 = CAND[best](G); print('prakiraan 2026 (titik)', round(p26, 1), '2025 aktual', round(G.gov_support_trn.iloc[-1], 1))
pd.DataFrame([dict(model=best, pred_2026=p26)]).to_csv(os.path.join(HERE, 'ml_select_fiscal_pred_2026.csv'), index=False)
chk('backtest 5 tahun x %d kandidat lengkap' % len(CAND), R.shape[0] == 5 * len(CAND) and np.isfinite(R.pred).all())
chk('identitas dukungan (semua tahun, +-0,5 T)', np.allclose(G.opex_total_trn / (1 - G.margin) - G.rev_ex_gov_support_trn, G.gov_support_trn, atol=0.5))
chk('info: MAE terbaik vs naif (statis)', True, f'{S.mae_2021_2025.iloc[0]:.1f} vs {S.loc["naif","mae_2021_2025"]:.1f}')
chk('info: MAE bersarang vs naif (jujur, tanpa pilih-belakangan)', True, f'{N.abs_err.mean():.1f} vs {N.abs_err_naif.mean():.1f}')
finish('ml_select_fiscal')
