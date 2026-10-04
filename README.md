# Dataset G — Fiscal burden of the energy transition: subsidies, compensation, and PLN

[![DOI](https://zenodo.org/badge/1403911014.svg)](https://doi.org/10.5281/zenodo.23137075)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](LICENSE)

> **Citation required:** if you use this dataset, please cite it (see `CITATION.cff` or the *Cite this repository* button).

Sources: **APBN Financial Note FY2025** (Appendix Tables 1, 2, 5; Ch. 1 sensitivity; Ch. 3 subsidies; Ch. 6 fiscal risk), **PLN audited financial statements 2015–2024** (via `../PLN-Health-Dataset/pln_financial_panel.csv`), **PLN Statistics 2023** (Figure 11, BPP vs tariffs). Run `python3 build_fiscal.py`; 9 validation checks, all pass.

| File | Contents |
|---|---|
| `news_updates_2024_2026.csv` | Web updates (21 Sep 2026): 2024 electricity subsidy Rp75.8 T (prelim), 2025 electricity subsidy+compensation Rp210 T, all-energy subsidy+compensation Jan–Aug 2025 Rp218 T and Jan–Aug 2026 Rp331.4 T, PLN average selling price 2024 Rp1,153.38/kWh. From news/official statements, not audits; 2025 and 2026 electricity breakdowns unavailable |
| `apbn_energy_subsidy_2020_2025.csv` | Macro assumptions (exchange rate, ICP, etc.), APBN posture, energy/non-energy subsidies; electricity & fuel/LPG subsidies (2020, 2023, 2024 outlook, 2025); ratios to central spending and GDP. Billion Rp |
| `pln_gov_support_2015_2024.csv` | Subsidy and compensation in PLN financial statements (trillion Rp), cash receipts, government receivables, vs APBN |
| `bpp_tariff_gap_2019_2023.csv` | Audited BPP vs average selling price (Rp/kWh) 2019–2023, implied volume, gap cost vs recorded subsidy+compensation |
| `apbn_sensitivity_2025.csv` | APBN 2025 sensitivity (trillion Rp) for exchange rate, ICP, growth, inflation, bonds, lifting |
| `scenario_icp_fx_apbn2025.csv` | ICP (60–120) × exchange-rate (15,500–17,500) grid, linear from Nota sensitivity |
| `scenario_bpp_shock.csv` | BPP increase 0–20% with frozen tariffs, government absorbs 100% or 50% |
| `pln_gov_receivables_bridge_2024_2025.csv` | Bridge reconciling the 2025 receivables increase (million Rp + trillions): compensation, subsidy, Jan–Feb 2025 discount. Increase 67.45 = accrual–cash 53.84 + discount 13.61; each row sourced (LK PLN 2025 Notes 16/37, LKPP 2025, BPK/BPKP) |
| `pln_fiscal_exposure_facts.csv` | Government guarantees, equity injections (PMN), subsidy recipient counts (cited from Ch. 6 and 3) |

## Headline findings
- Government support to PLN (subsidy + compensation) rose from Rp56.6 T (2015) to Rp177.2 T (2024), or 32% of PLN revenue; without it, 2024 operating profit would be negative Rp116.6 T.
- PLN-booked 2023 electricity subsidy (Rp68.64 T) nearly matches APBN (Rp68.70 T); 2020 and 2024 gaps reflect pandemic discounts and outlook status.
- Compensation (not subsidy) is the growing leg: Rp17.9 T (2020) → Rp100.2 T (2024); the Nota carries no separate compensation table, so the figures come only from PLN statements.

## Limitations
1. Nota 2025 reports electricity subsidy only for 2020, 2023, 2024 (outlook), 2025. For 2022 a secondary source is used (BPK/LKPP 2022 via Databoks, Rp56.1 T, +17% over 2021), so 2021 (≈Rp47.9 T) is a derived estimate; both sit in `subsidy_electricity_secondary_bn` and `subsidy_electricity_best_bn`, not the headline column. 2015–2019 subsidies are absent here (use PLN-statement columns).
2. 2024 Nota figures are **outlook**, 2025 is **budget** (not outturn).
3. Nota sensitivity is linear and ceteris paribus, already includes energy compensation, but excludes policy discretion. Grids far from base (ICP 60 or 120) are indicative only.
4. The BPP scenario uses 2023 BPP (Rp1,599/kWh) and 2024 volume derived from electricity revenue ÷ 2023 tariff (estimate, not data). PLN compensation covers more than the BPP–tariff gap (implicit ratio 0.75–1.08 of recorded), so scenarios are orders of magnitude.
5. PLN revenue in Nota Table 6.4 for 2023 (333.2 T) is electricity-sales revenue only; 2019–2022 equal total statement revenue.
6. 2025–2026 figures in `news_updates_2024_2026.csv` come from news and official statements; single-year 2024 BPP remains unfound (only 2021–2024 average Rp1,445/kWh from Databoks). PLN Statistics 2024 could not be downloaded in this environment (web.pln.co.id blocked by proxy), so dataset version F/E for 2024 was not built.

## 2025–2026 updates (`news_updates_2024_2026.csv`, now 15 checks)
Added 2025 LK PLN figures from media (revenue Rp582.68 T; subsidy 87.46; compensation 112.73; government receivables 110.73; profit 7.26; FX loss 12.46), 2026 APBN electricity-subsidy budget Rp104.6 T (2025 outlook Rp89 T), and two BPP markers (RUPTL PSO7 projection Rp1,829/kWh for 2025; PLN CEO statement Rp1,600–1,700/kWh). **Warning**: LK 2025 PDF on IDX was inaccessible (403), so all 2025 figures are news-sourced. Media 2024 profit comparator (Rp21.2 T) differs from panel-E audited 2024 (Rp17.76 T); gap unexplained.
Second search round: 2025 PLN customers 96.2 million, sales 317.69 TWh, Jan–Aug 2025 electricity subsidy+compensation (48.1 + 37.5 + 2.0 arrears = 87.6; ceiling 127.2), 2026 energy-subsidy projection Rp227.26 T. The 2024 profit gap (17.76 vs 21.23 in news) sits below operating costs (comparison cost components match panel E), so likely a tax/other restatement, not a cost revision. Full-year 2025 BPP outturn and full-year 2025 electricity subsidy remain unfound in accessible sources.

Third finding (via Chrome extension, Ministry of Finance): "2025 APBN Subsidy and Compensation" slide (Press Conf. 13 Mar 2025) reports the **should-be price of subsidised 900VA residential electricity at Rp1,800/kWh vs public price Rp600** (APBN bears Rp1,200, 67%), plus 2024 electricity subsidy Rp75.8 T and 2025 allocation Rp89.7 T; 8 Jan 2026 press conference gives provisional 2025 outturn (all-type subsidies Rp281.6 T; subsidy+compensation Rp401.6 T; subsidised electricity customers 42.8 million). This is an official supply-cost proxy for 900VA, **not the national average realised BPP**, still unfound. Full-year 2025 electricity subsidy outturn (ex-fuel/LPG) is likewise absent there.

**LK PLN 2025 audited (added).** 2025 net profit = 7,260,708 million; 2024 profit restated from 17,763,024 to 21,231,284 (Note 58, deferred-tax correction 7,905,235 million). `news_updates_2024_2026.csv` carries `pln_lk_net_profit_restated` and `pln_lk_deferred_tax_overstatement_dec2024` rows; 2025 figures checked against panel E and PLN Statistics 2025 Tables 62–63 (government receivables 110,738, subsidy 87,461, compensation 112,735 million Rp).

**Full 2025 electricity subsidy (LKPP 2025 audited, found via Chrome 21 Sep 2026).** 2025 cash electricity-subsidy spending = Rp81.036 T (ceiling 89.747 T; 2024: 75.817 T); cash electricity tariff compensation 2025 = Rp65.321 T (ceiling 92.411 T). 2025 accrual subsidy expense = Rp87.461 T, equal to subsidy revenue in LK PLN and PLN Statistics 2025 (accrual–cash gap 6.42 T = unpaid subsidy). Rows in `news_updates_2024_2026.csv` (`apbn_electricity_*` items, `subsidized_electricity_gwh_realized` 2020–2024 from the 2025 Ditjen Gatrik performance report).
**National 2025 realised BPP: not found as an official figure.** Only the RUPTL 2025 projection Rp1,829/kWh (secondary source). `derived_bpp_proxy_*` columns are derived proxies (operating [+ financial] expense / kWh sold, PLN Statistics 2025 T63/T46): 2025 = 1,679 (1,757 with financial expense); do not treat as official BPP.

## ML (`ml_fiscal.py`, through 2025)

Numpy+pandas. Outputs: `ml_fiscal_backtest.csv`, `ml_fiscal_2025_forecast.csv`, `ml_fiscal_gap_model.csv`, `ml_fiscal_mc_2026.csv`.

- **2025 backtest (train 2015–2024)**: actual government support 200.2 T; 5-year trend 203.8 (error 3.6), naive 177.2, 3-year mean 147.4. **Government receivables 110.7 T** unpredictable (errors 67–95 T; 3-year mean flagged as surprise), as is the 53.8 T accrual–cash gap.
- **Cost-gap model** (support ~ opex − ex-support revenue; operating-profit identity tested): LOYO R² 0.955; 2025 prediction = 214.4 vs actual 200.2 (residual −14 T).
- **2026 Monte Carlo (annual-growth bootstrap 2016–2025, conditional, not a forecast)**: support needed to hold the 2025 operating margin: p05 182, median 233, p95 282 T; P(above 2025) ≈ 70%. Formula tested: zero growth reproduces 200.2 T.

## 2025 macro outturn (LKPP 2025 via BPK, added to `news_updates_2024_2026.csv`)

Growth 5.11% (assumption 5.2), inflation 2.92% y/y (assumption 2.5), average exchange rate Rp16,475 (assumption 16,000; matches panel-D rate 16,474), 10-year bonds 6.71% (assumption 7.0), **ICP USD 67.38/bbl (assumption 82; 2024: 78.14)**, oil lifting 605.86 kbd. The `apbn_energy_subsidy_2020_2025.csv` 2025 row remains **APBN assumption**, not outturn; use `macro_realized_*` rows for outturn. Also from Ditjen Gatrik: 2025 electricity consumption per capita 1,584 kWh (2024: 1,411), national installed capacity 107.51 GW.

## Realised BPP: follow-up search (21 Sep 2026)

Searched again via Chrome: MEMR decrees/regulations on BPP, DPR Commission XII hearing materials, LK PLN 2025, PLN annual reports and performance reports, RAPBN 2026 Financial Note, plus English-language search (IEEFA/IESR). Result: **no national realised 2024 or 2025 BPP figure**. Found only 2019–2023 BPP (PLN Statistics 2023), the subsidy formula (PMK 20/2025: subsidy = BPP × (1+margin) − selling price, times volume; quoted from a 2026 MDPI article snippet) and the BPP-setting mechanism (Kepmen 169.K/2021). esdm.go.id news pages were unreadable to the extension (domain permission denied) and not pursued otherwise. Dataset 2024–2025 figures remain derived proxies.

- **Macro outturn vs PLN energy cost** (`ml_fiscal_macro_realized_link.csv`): realised 2025 ICP fell 13.8% (67.4 from 78.1) while PLN fuel + power-purchase costs rose 10.0% (393.8 T from 357.9 T) and government support rose 13.0%. Spearman correlation of ICP changes vs energy-cost changes 2021–2025 = −0.30 (n=5, descriptive only). Causes untested.

## Modern ML: state-space local trend (`ml_modern_fiscal_bsts.py`, ML not Bayesian)

Unobserved-components local linear trend, maximum likelihood via Kalman filter (not Bayesian: no priors/posteriors). 2025 government-support test: forecast 205.0 T (90% interval: 170.5–239.4) vs actual 200.2 T; MAE 2021–2024 19.7 vs naive 27.8 (2021–2025: 16.7 vs 26.0 including 2025). 2025 government receivables (110.7 T) **not flagged as a surprise** because the series is only 6 years long so intervals are very wide (forecast 86.6 ± 29). Conditional 2026 forecasts: support 226.5 T (194–259), 2027: 252.5 T (198–307); 2026 receivables: 178 T (132–224) from univariate extrapolation. Not official forecasts. Requires statsmodels.

## Selected headline model: coherent probabilistic component forecast (`ml_hier_fiscal_coherent.py`)

Government support is an identity: opex/(1−margin) − ex-support revenue (tested, every year). Four components (fuel, power purchases, other costs, revenue) forecast as log random walks with drift (last 6 years), joined by a Gaussian copula of residual correlation (50% shrinkage), then aggregated through the identity with margin from the last 5 years. Stochastic rolling-origin backtest (seed 0, 4000 paths): MAE 2021–2025 19.7 vs naive 26.9; **2023–2025: 6.8 vs 25.9**. Deterministic variant in `ml_select_fiscal_scores.csv` (`koheren_komponen`): 20.2/7.4 — simulation noise + median aggregation, not a different model. 2021–2022 are very poor (origins with only 5 volatile growth rates; intervals > 900 T), so only 2023–2025 are evaluable. 2025: median 209.6 T (90%: 151.6–279.9) vs actual 200.2 T. 2023–2025 sharpness: coherent mean width 119 T vs state-space 71 T (both 100% 3/3 coverage) — full coverage bought with wider intervals. Conditional forecasts: 2026 256.6 T (195.5–330.2), 2027 301.6 T (212.9–419.5), using ~15%/year mean growth; more aggressive than state-space (226.5) and Monte Carlo (233) above. The model projects required $G_t$, not cash timing/receivables.
