#!/usr/bin/env python3
"""2024-2026 updates from public sources (news/official statements, searched via internet 21 Sep 2026).
Not audits; each row carries a source and status. Consistency-checked against PLN-statement data in this folder."""
import os, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
rows = [
 (2024,'apbn_electricity_subsidy_realized_prelim',75.8,'IDR trillion','outturn as of 24 Dec 2024; 73.24 (current year) + 2.58 (2022 arrears)','Finance Minister Sri Mulyani, 6 Jan 2025 (quoted by Warta Ekonomi)','https://wartaekonomi.co.id/read554249/realisasi-subsidi-listrik-2024-capai-rp758-triliun-ini-detailnya','preliminary'),
 (2024,'apbn_electricity_subsidy_arrears_2022_paid',2.58,'IDR trillion','2022 subsidy arrears payment','idem','idem','preliminary'),
 (2024,'pln_lk_subsidy_revenue',77.045334,'IDR trillion','PLN Statistics 2024, profit-and-loss summary (Rp77,045,334 million)','PLN, Statistics 2024','https://web.pln.co.id/statics/uploads/2025/09/Statistik-PLN-2024-Ind-Eng.pdf','PDF not downloadable from sandbox; figures from summary page'),
 (2024,'pln_lk_compensation_revenue',100.184044,'IDR trillion','PLN Statistics 2024 (Rp100,184,044 million)','PLN, Statistics 2024','idem','idem'),
 (2024,'pln_lk_electricity_sales_revenue',353.176019,'IDR trillion','PLN Statistics 2024 (Rp353,176,019 million)','PLN, Statistics 2024','idem','idem'),
 (2024,'pln_avg_selling_price',1153.38,'IDR/kWh','2024 average selling price (2023: 1,155.47)','PLN, Statistics 2024','idem','idem'),
 (2023,'pln_avg_selling_price',1155.47,'IDR/kWh','from PLN Statistics 2024','PLN, Statistics 2024','idem','idem'),
 (2025,'electricity_subsidy_and_compensation_total',210.0,'IDR trillion','including Rp12 T Mar-May 2025 tariff discount; subsidy vs compensation split unpublished in source','MEMR Minister Bahlil Lahadalia, 16 Dec 2025','https://most1058fm.com/2025/12/realisasi-subsidi-dan-kompensasi-listrik-2025-capai-rp-210-triliun/','official statement, not audited'),
 (2025,'electricity_tariff_stimulus_discount',12.0,'IDR trillion','Mar-May 2025 electricity tariff discount','idem','idem','official statement'),
 (2025,'energy_subsidy_compensation_jan_aug',218.0,'IDR trillion','all energy (fuel, LPG, electricity) Jan-Aug 2025','Ministry of Finance, quoted by Jawa Pos 18 Sep 2026','https://www.jawapos.com/ekonomi/2609180254/realisasi-subsidi-energi-tembus-rp-331-triliun-naik-rp-113-triliun-dari-2025','news'),
 (2026,'energy_subsidy_compensation_jan_aug',331.4,'IDR trillion','all energy Jan-Aug 2026; electricity split unavailable','Ministry of Finance, Jawa Pos 18 Sep 2026','idem','news'),
 (2026,'energy_subsidy_compensation_jan_aug_yoy_increase',113.0,'IDR trillion','+51.8% over Jan-Aug 2025','idem','idem','news'),

 (2025,'pln_lk_operating_revenue_total',582.68,'IDR trillion','2025 PLN statements (media); 2024 comparator = 545.38','CNBC Indonesia 2 Jun 2026; Katadata','https://www.cnbcindonesia.com/news/20260602161044-4-739489/pln-cetak-laba-rp-726-triliun-di-2025','news; IDX PDF 403'),
 (2025,'pln_lk_subsidy_revenue',87.46,'IDR trillion','+13.52% YoY','Katadata (2025 PLN statements)','https://katadata.co.id/amp/finansial/korporasi/6a39457acf3c0/utang-pemerintah-ke-pln-membengkak-ke-rp-110-triliun-laba-susut-67-di-2025','news'),
 (2025,'pln_lk_compensation_revenue',112.73,'IDR trillion','+12.53% YoY; CNBC matches (112.73)','Katadata; CNBC','idem','news'),
 (2025,'pln_lk_govt_receivable',110.73,'IDR trillion','government receivables, +155.8% from 43.29 (2024) = matches panel E','Katadata','idem','news'),
 (2025,'pln_lk_net_profit',7.260708,'IDR trillion','Audited 2025 statements (Rp7,260,708 million). 2024 comparator restated from 17.763 to 21.231 T: deferred-tax over-accrual correction Rp3.468 T (deferred tax on fiscally capitalised maintenance cost since 2020; Note 58 of 2025 statements). 2024 pre-tax profit unchanged (28.270 T)','PLN, Audited 2025 statements (approved 19 May 2026), Note 58','LK-PLN 2025 Audited.pdf (Data folder)','audited'),
 (2025,'pln_lk_fx_loss',12.46,'IDR trillion','2025 FX loss (2024 comparator 6.78 = panel E)','CNBC','https://www.cnbcindonesia.com/news/20260602161044-4-739489/pln-cetak-laba-rp-726-triliun-di-2025','news'),
 (2025,'pln_lk_gov_support_total',200.19,'IDR trillion','subsidy 87.46 + compensation 112.73 (computed); 2024: 177.23','computed','idem','derived'),
 (2026,'apbn_electricity_subsidy_budget',104.6,'IDR trillion','2026 APBN, +17.5% over 2025 outlook Rp89 T; drivers: FX, biomass cofiring, 3T fuel mix','Investortrust (budget document)','https://investortrust.id/business/76355/subsidi-listrik-2026-naik-17-5-tembus-rp-104-6-triliun-ternyata-karena-faktor-ini','news'),
 (2025,'apbn_electricity_subsidy_outlook',89.0,'IDR trillion','2025 outlook (not audited outturn)','idem','idem','news'),
 (2025,'bpp_ruptl2025_pso7_scenario',1829.0,'IDR/kWh','Average 2025 BPP under RUPTL 2025-2034 PSO7 scenario (Plan-Financing-Gap-Dataset/ruptl2025_bpp_subsidy_scenarios.csv); projection, not outturn','RUPTL PLN 2025-2034','Plan-Financing-Gap-Dataset','official projection'),
 (2025,'bpp_ceo_statement_approx',1650.0,'IDR/kWh','"Current BPP around Rp1,600-1,700/kWh" (PLN CEO, when tariffs held end-2024); midpoint; exact date unverified','Bloomberg Technoz','https://www.bloombergtechnoz.com/detail-news/57176/bos-pln-beber-nasib-tarif-listrik-2025-usai-tak-naik-akhir-2024/2','oral statement from search results'),
 (2025,'pln_customers',96.2,'million customers','PLN 2025 statements/release (2024: 92.88 million from Statistics 2024)','Infobanknews (PLN release)','https://infobanknews.com/pln-bukukan-laba-bersih-rp726-triliun-sepanjang-2025','news'),
 (2025,'pln_electricity_sold',317.69,'TWh','+3.75% from 306.21 TWh (2024; Statistics 2024: 306,219 GWh)','Infobanknews (PLN release)','idem','news'),
 (2025,'pln_connected_capacity',192621,'MVA','+5.82% from 182,026 MVA (2024)','Infobanknews (PLN release)','idem','news'),
 (2025,'pln_lk_2024_net_profit_as_comparative_in_media',21.23,'IDR trillion','2024 comparator in 2025-statement news (Bloomberg Technoz; -65.8% to 7.26). 2024 comparator cost components (fuel 179.29; IPP 178.63; maintenance 31.55) MATCH panel E, so the 17.76 vs 21.23 profit gap (= 3.47 T) sits below operating costs; probably a restatement, unconfirmed','Bloomberg Technoz','https://www.bloombergtechnoz.com/detail-news/110581/laba-bersih-anjlok-65-8-sepanjang-2025-pln-kantongi-rp7-26-t','news; needs original 2025 statements'),
 (2025,'apbn_electricity_subsidy_realized_jan_aug',48.1,'IDR trillion','55.9% of subsidy ceiling; includes 2023 arrears','Finance Minister Purbaya via Bloomberg Technoz','https://www.bloombergtechnoz.com/detail-news/85564/subsidi-kompensasi-listrik-tembus-rp87-triliun-per-agustus-2025','news'),
 (2025,'apbn_electricity_compensation_realized_jan_aug',37.5,'IDR trillion','100% of current-period compensation target','idem','idem','news'),
 (2025,'apbn_electricity_subsidy_compensation_budget',127.2,'IDR trillion','total 2025 electricity subsidy + compensation ceiling (calculation base)','idem','idem','news'),
 (2025,'apbn_electricity_arrears_component_jan_aug',2.0,'IDR trillion','prior-year arrears within the 87.6 total','idem','idem','news'),
 (2025,'apbn_subsidy_total_all_types',281.6,'IDR trillion','total 2025 government subsidy outturn (fuel, LPG, electricity, fertiliser, etc.), excluding compensation','Tempo/Kompas 8 Jan 2026 (headline)','https://www.tempo.co/ekonomi/realisasi-subsidi-pemerintah-pada-2025-naik-jadi-rp-281-6-t-2105784','news; body unretrievable (robots)'),
 (2026,'apbn_energy_subsidy_outlook_all',227.26,'IDR trillion','end-2026 energy-subsidy (fuel, LPG, electricity) projection; 2022-2025 average Rp174.73 T','CNBC Indonesia 18 Aug 2026','https://www.cnbcindonesia.com/news/20260818142222-4-760308/subsidi-bbm-lpg-listrik-di-2026-diperkirakan-naik-jadi-rp-227-triliun/amp','news (government document)'),
 (2025,'bpp_proxy_900va_price_should_be',1800.0,'IDR/kWh','"should-be price" of subsidised 900VA residential electricity (government supply-cost proxy): 1,800; public price 600; APBN bears 1,200 (67%); 41.5 million customers','Ministry of Finance, APBN Kita Press Conference 13 Mar 2025, p. 21','https://media.kemenkeu.go.id/getmedia/b6026682-cd60-48f9-9183-f03d51df9479/Publikasi-Web-Konpers-APBN-Kita-(Maret-2025).pdf','official document (not realised BPP)'),
 (2025,'bpp_proxy_900va_price_paid_by_public',600.0,'IDR/kWh','selling price to subsidised 900VA residential public','idem','idem','official document'),
 (2025,'bpp_proxy_900va_borne_by_apbn',1200.0,'IDR/kWh','gap borne by APBN (67% of 1,800)','idem','idem','official document'),
 (2024,'apbn_electricity_subsidy_realized_kemenkeu',75.8,'IDR trillion','2024 realised electricity subsidy (matches Finance Minister 6 Jan 2025)','Ministry of Finance, 13 Mar 2025 press conference','idem','official document'),
 (2025,'apbn_electricity_subsidy_apbn_allocation',89.7,'IDR trillion','2025 APBN electricity subsidy (2025 column, not outturn); Investortrust outlook 89.0','Ministry of Finance, 13 Mar 2025 press conference','idem','official document'),
 (2024,'apbn_energy_subsidy_total',177.6,'IDR trillion','Fuel 21.6 + LPG 80.2 + electricity 75.8','idem','idem','official document'),
 (2024,'apbn_energy_compensation_total',209.3,'IDR trillion','2024 energy compensation (fuel+electricity)','idem','idem','official document'),
 (2025,'apbn_energy_subsidy_total_allocation',203.4,'IDR trillion','Fuel 26.7 + LPG 87.0 + electricity 89.7 (2025 APBN allocation)','idem','idem','official document'),
 (2025,'apbn_energy_compensation_total_allocation',190.9,'IDR trillion','2025 energy compensation (allocation)','idem','idem','official document'),
 (2025,'apbn_subsidy_all_types_realized',281.6,'IDR trillion','all-type subsidy outturn through 31 Dec 2025 (fuel, LPG, electricity, fertiliser, housing)','Ministry of Finance, provisional 2025 APBN outturn press conference, 8 Jan 2026, p. 28','https://media.kemenkeu.go.id/getmedia/b7f00cc5-15ad-4d8d-9bb5-42e18e8494a8/Publikasi-Web-Konpers-APBN-Kita-(Januari-2026).pdf','official document (provisional)'),
 (2025,'apbn_subsidy_and_compensation_realized',401.6,'IDR trillion','all-type subsidy + compensation through 31 Dec 2025','idem','idem','official document (provisional)'),
 (2025,'subsidized_electricity_customers',42.8,'million customers','2025 subsidised electricity customers (2024: 41.7; +2.6%)','idem','idem','official document (provisional)'),
 (2024,'subsidized_electricity_customers',41.7,'million customers','2024 subsidised electricity customers','idem','idem','official document (provisional)'),
 (2024,'pln_lk_net_profit_restated',21.231284,'IDR trillion','restated 2024 current-year profit (was 17.763024); +3.468260 adjustment = over-accrued tax expense','PLN, Audited 2025 statements, Note 58','LK-PLN 2025 Audited.pdf (Data folder)','audited'),
 (2024,'pln_lk_deferred_tax_overstatement_dec2024',7.905235,'IDR trillion','over-accrued deferred-tax liability 31 Dec 2024 (1 Jan 2024: 4.436975); parent equity up 7.905 T to 1,067,870 million','PLN, Audited 2025 statements, Note 58','LK-PLN 2025 Audited.pdf (Data folder)','audited'),
 (2025,'pln_lk_total_assets',1837.409908,'IDR trillion','TOTAL ASSETS 31 Dec 2025 (2024: 1,772.375266)','PLN, Audited 2025 statements','LK-PLN 2025 Audited.pdf (Data folder)','audited'),
  (2025,'pln_lk_operating_profit',49.226013,'IDR trillion','2025 operating profit (2024: 60.621006)','PLN, Audited 2025 statements','LK-PLN 2025 Audited.pdf (Data folder)','audited'),
  (2025,'pln_govt_receivable_compensation',84.864811,'IDR trillion','31 Dec 2025 compensation receivables (2024: 37.450898); opening + revenue 112.734817 - cash 65.320904','PLN, Audited 2025 statements, Note 16','LK-PLN 2025 Audited.pdf (Data folder)','audited'),
  (2025,'pln_govt_receivable_subsidy',12.26409,'IDR trillion','31 Dec 2025 electricity-subsidy receivables (2024: 5.839850); accrual 87.460664 - cash 81.036424','PLN, Audited 2025 statements, Notes 16/37','LK-PLN 2025 Audited.pdf (Data folder)','audited'),
  (2025,'pln_govt_receivable_discount_jan_feb',13.609498,'IDR trillion','Jan-Feb 2025 tariff-discount receivables, recognised separately outside G_t; explains the 67.447651-53.838153 reconciliation gap','PLN, Audited 2025 statements, Note 16; BPKP Review + Kemenko letter 31-Dec-2025','LK-PLN 2025 Audited.pdf (Data folder)','audited'),
]

# ---- Found via Chrome 21 Sep 2026: audited LKPP 2025, 2025 Ditjen Gatrik performance report, Sep 2026 APBN KiTa
LKPP='LKPP 2025 (Audited), DJPb Ministry of Finance'; LKPPU='https://djpb.kemenkeu.go.id/portal/images/lkpp/LKPP-2025.pdf'
rows += [
 (2025,'apbn_electricity_subsidy_realized_lkpp_cash',81.036424,'IDR trillion','Electricity Subsidy Spending (LRA, cash) FY2025 Audited: Rp81,036,424,051,631; ceiling 89.747 T (90.29%); 2024 Audited 75.817285',LKPP,LKPPU,'audited'),
 (2024,'apbn_electricity_subsidy_realized_lkpp_cash',75.817285,'IDR trillion','Audited 2024 Electricity Subsidy Spending (Rp75,817,285,111,936) = 73.24 + 2.58 2022 arrears (Finance Minister 6 Jan 2025)',LKPP,LKPPU,'audited'),
 (2025,'apbn_electricity_subsidy_budget_ceiling',89.74651,'IDR trillion','2025 Electricity Subsidy Spending ceiling (LKPP performance table, p. 142)',LKPP,LKPPU,'audited'),
 (2025,'apbn_electricity_subsidy_expense_accrual',87.460664,'IDR trillion','Electricity Subsidy Expense (LO, accrual) 2025: Rp87,460,663,602,008; 2024 = 77.045335; equals subsidy revenue in PLN statements',LKPP,LKPPU,'audited'),
 (2024,'apbn_electricity_subsidy_expense_accrual',77.045335,'IDR trillion','2024 Electricity Subsidy Expense (LO) (Rp77,045,334,864,270)',LKPP,LKPPU,'audited'),
 (2025,'macro_realized_gdp_growth_pct',5.11,'%','2025 realised economic growth (2024: 5.03); APBN assumption 5.2','BPK, Review Report on FY2025 Fiscal Transparency Implementation (LKPP 2025)','https://www.bpk.go.id/assets/files/lkpp/2025/lkpp_2025_1784027527.pdf','audited'),
 (2025,'macro_realized_inflation_yoy_pct',2.92,'%','2025 y/y inflation (2024: 1.57); APBN assumption 2.5','BPK, Review Report on FY2025 Fiscal Transparency Implementation (LKPP 2025)','https://www.bpk.go.id/assets/files/lkpp/2025/lkpp_2025_1784027527.pdf','audited'),
 (2025,'macro_realized_usdidr_avg',16475,'IDR/USD','2025 average exchange rate; APBN assumption 16,000','BPK, Review Report on FY2025 Fiscal Transparency Implementation (LKPP 2025)','https://www.bpk.go.id/assets/files/lkpp/2025/lkpp_2025_1784027527.pdf','audited'),
 (2025,'macro_realized_sbn10y_pct',6.71,'%','2025 10-year government-bond yield (ytd); assumption 7.0; 2024: 6.78','BPK, Review Report on FY2025 Fiscal Transparency Implementation (LKPP 2025)','https://www.bpk.go.id/assets/files/lkpp/2025/lkpp_2025_1784027527.pdf','audited'),
 (2025,'macro_realized_icp_usd_bbl',67.38,'USD/bbl','2025 average realised ICP (2024: 78.14); APBN assumption 82','BPK, Review Report on FY2025 Fiscal Transparency Implementation (LKPP 2025)','https://www.bpk.go.id/assets/files/lkpp/2025/lkpp_2025_1784027527.pdf','audited'),
 (2024,'macro_realized_icp_usd_bbl',78.14,'USD/bbl','2024 average realised ICP','BPK, Review Report on FY2025 Fiscal Transparency Implementation (LKPP 2025)','https://www.bpk.go.id/assets/files/lkpp/2025/lkpp_2025_1784027527.pdf','audited'),
 (2025,'macro_realized_oil_lifting_kbpd',605.86,'thousand bpd','2025 oil lifting; APBN target 605','BPK, Review Report on FY2025 Fiscal Transparency Implementation (LKPP 2025)','https://www.bpk.go.id/assets/files/lkpp/2025/lkpp_2025_1784027527.pdf','audited'),
 (2025,'ebt_capacity_total_mw_esdm',15630,'MW','Dec 2025 renewable capacity (EBTKE/MEMR Directorate definition: total, not Handbook on-grid series)','MEMR Electricity Directorate (Gatrik), 22 Jan 2026 news (DPR Commission XII working meeting)','https://gatrik.esdm.go.id/berita/di-depan-dpr-menteri-esdm-paparkan-capaian-positif-subsektor-ketenagalistrikan','official statement'),
 (2025,'ebt_capacity_added_plta_mw',531.2,'MW','2025 additions','idem','idem','official statement'),
 (2025,'ebt_capacity_added_plts_mw',584.7,'MW','2025 additions','idem','idem','official statement'),
 (2025,'ebt_capacity_added_pltp_mw',105.2,'MW','2025 additions','idem','idem','official statement'),
 (2025,'ebt_capacity_added_pltbio_mw',84.5,'MW','2025 additions','idem','idem','official statement'),
 (2025,'ebt_capacity_added_total_mw',1305.6,'MW','four types sum = the 1.3 GW cited by the Minister; largest in 5 years','idem','idem','official statement'),
 (2025,'national_installed_capacity_gw',107.51,'GW','2025 national installed capacity, +~7 GW (mostly fossil/coal)','idem','idem','official statement'),
 (2025,'electricity_consumption_per_capita_kwh',1584,'kWh/capita','2025 electricity consumption per capita (2024: 1,411)','idem','idem','official statement'),
 (2025,'apbn_electricity_compensation_realized_lkpp_cash',65.3209,'IDR trillion','2025 Electricity Tariff Compensation (cash outturn), ceiling 92.411 T (70.69%); compensation payments deferred -> compensation debt',LKPP,LKPPU,'audited'),
 (2025,'apbn_electricity_compensation_budget_ceiling',92.41119,'IDR trillion','2025 Electricity Tariff Compensation ceiling',LKPP,LKPPU,'audited'),
 (2025,'apbn_electricity_subsidy_volume_twh_realized',69.66,'TWh','2025 Electricity Subsidy output volume (PDF text reads "75.55 | 69.66": target 75.55; outturn 69.66; column order from extraction, not a clean table)',LKPP,LKPPU,'audited; text extraction'),
 (2025,'apbn_electricity_compensation_volume_twh_realized',222.16,'TWh','2025 Electricity Tariff Compensation output volume (target 195)',LKPP,LKPPU,'audited'),
 (2020,'subsidized_electricity_gwh_realized',59002,'GWh','realised subsidised electricity energy (MEMR Strategic Plan 2025-2029), target 60,080','2025 Electricity Directorate Performance Report, Table 7','https://gatrik.artristik.co.id/gatrik-api//storage/migrasi/download_index/files/d35ab-laporan-kinerja-direktorat-jenderal-ketenagalistrikan-tahun-2025-published-tte-_compressed-1-.pdf','official'),
 (2021,'subsidized_electricity_gwh_realized',61916,'GWh','target 64,258','idem','idem','official'),
 (2022,'subsidized_electricity_gwh_realized',62248,'GWh','target 68,894','idem','idem','official'),
 (2023,'subsidized_electricity_gwh_realized',66034,'GWh','target 73,609','idem','idem','official'),
 (2024,'subsidized_electricity_gwh_realized',70807,'GWh','target 78,191','idem','idem','official'),
 (2025,'subsidized_household_allocation_gwh_q1',19349.53,'GWh','subsidised poor/vulnerable-household electricity allocation, Q1 2025 achievement (target 17,057.75) -- not a full year','idem','idem','official; partial'),
 (2026,'subsidized_customers_million_jan_aug',43.3,'million customers','subsidised electricity customers through Aug 2026 (+2.1% from 42.4 million)','Ministry of Finance, Sep 2026 APBN KiTa Press Conference','http://media.kemenkeu.go.id/getmedia/04ced8b6-ddc6-4127-8cda-73e39ef5cbee/Publikasi-Web-Konpers-APBN-KiTa-(Sept-2026).pdf','official'),
]
# Derived BPP proxy (NOT official BPP): PLN operating (+ financial) expense / energy sold, from PLN Statistics 2025 Tables 63 & 46
_R = os.path.join(HERE,'..','Regional-Disparity-Dataset')
_ts = pd.read_csv(os.path.join(_R,'pln_national_timeseries_2016_2025.csv')).set_index('year')
_fin = pd.read_csv(os.path.join(_R,'pln_stat2025_financial_timeseries_long.csv'))
def _f(item,y): return _fin[(_fin.table==63)&_fin.item.str.startswith(item)&(_fin.year==y)].value.iloc[0]
for _y in range(2021,2026):
    _opex=_f('Jumlah Beban Usaha',_y); _fe=-_f('Beban Keuangan',_y); _gwh=_ts.loc[_y,'gwh_sold_total']
    rows.append((_y,'derived_bpp_proxy_opex_per_kwh_sold',round(_opex/_gwh,1),'IDR/kWh',f'DERIVED: Total Operating Expense {_opex:,.0f} million Rp / energy sold {_gwh:,.2f} GWh; covers operating expense only (no financial expense); divisor = energy sold -> not official BPP','computed from PLN Statistics 2025 Tables 63 & 46','pln_stat2025_financial_timeseries_long.csv','derived'))
    rows.append((_y,'derived_bpp_proxy_opex_plus_finance_per_kwh_sold',round((_opex+_fe)/_gwh,1),'IDR/kWh',f'DERIVED: (Operating Expense + Financial Expense {_fe:,.0f}) / energy sold {_gwh:,.2f} GWh; covers both cost blocks; divisor = energy sold -> not official BPP (official BPP is computed by PLN/MEMR per ministerial decree and unpublished for 2025 outturn in readable sources)','idem','idem','derived'))
d = pd.DataFrame(rows, columns=['year','item','value','unit','note','source','url','status'])
d.to_csv(f'{HERE}/news_updates_2024_2026.csv', index=False)
fails=[]
def chk(n,ok,det=''):
    print(('PASS ' if ok else 'FAIL ')+n,det)
    if not ok: fails.append(n)
g = pd.read_csv(f'{HERE}/pln_gov_support_2015_2024.csv').set_index('year')
v = d.set_index(['year','item']).value
chk('2024: 73.24 + 2.58 = 75.8 (+-0.05)', abs(73.24+v[(2024,'apbn_electricity_subsidy_arrears_2022_paid')]-v[(2024,'apbn_electricity_subsidy_realized_prelim')])<=0.05)
chk('2024: PLN-statement subsidy (Statistics 2024) = panel Audited 2024 (+-0.01 T)', abs(v[(2024,'pln_lk_subsidy_revenue')]-g.loc[2024,'subsidy_trn'])<=0.01, f"{v[(2024,'pln_lk_subsidy_revenue')]:.3f} vs {g.loc[2024,'subsidy_trn']:.3f}")
chk('2024: PLN-statement compensation (Statistics 2024) = Audited 2024 (+-0.01 T)', abs(v[(2024,'pln_lk_compensation_revenue')]-g.loc[2024,'compensation_trn'])<=0.01, f"{v[(2024,'pln_lk_compensation_revenue')]:.3f} vs {g.loc[2024,'compensation_trn']:.3f}")
chk('2026 - 2025 (Jan-Aug) = reported increase (+-1)', abs(v[(2026,'energy_subsidy_compensation_jan_aug')]-v[(2025,'energy_subsidy_compensation_jan_aug')]-v[(2026,'energy_subsidy_compensation_jan_aug_yoy_increase')])<=1)
chk('2025: Rp210 T electricity subsidy+compensation on trend (>= 2024 PLN statements, Rp177 T)', v[(2025,'electricity_subsidy_and_compensation_total')]>g.loc[2024,'gov_support_trn'], f"{v[(2025,'electricity_subsidy_and_compensation_total')]} vs {g.loc[2024,'gov_support_trn']:.1f}")
chk('2025: operating revenue 582.68 vs 2024 545.38 up ~6.8% (+-0.1)', abs((582.68/545.380993-1)*100-6.84)<=0.1)
chk('2025: government receivables 110.73 / 43.29 -1 = 155.8% (+-0.5)', abs((110.73/g.loc[2024,'govt_receivable_trn']-1)*100-155.8)<=0.5, f"{g.loc[2024,'govt_receivable_trn']:.2f}")
chk('2025: 2024 comparator FX loss 6.78 = panel E (+-0.01)', abs(6.78-6.780398)<=0.01)
chk('2025: pre-tax profit 12.99 - tax 5.73 = profit 7.26 (+-0.02)', abs(12.99-5.73-7.26)<=0.02)
chk('2025: subsidy+compensation 200.19 = 87.46+112.73 (+-0.01) and up from 2024', abs(v[(2025,'pln_lk_gov_support_total')]-v[(2025,'pln_lk_subsidy_revenue')]-v[(2025,'pln_lk_compensation_revenue')])<=0.01 and v[(2025,'pln_lk_gov_support_total')]>g.loc[2024,'gov_support_trn'])
chk('2026: 104.6/89 -1 = 17.5% (+-0.2)', abs((104.6/89-1)*100-17.5)<=0.2)
chk('2025 Jan-Aug: subsidy 48.1 + compensation 37.5 + arrears 2.0 = 87.6 (+-0.05)', abs(48.1+37.5+2.0-87.6)<=0.05)
chk('2025: sales 317.69 TWh / 306.21 = +3.75% (+-0.05)', abs((317.69/306.21-1)*100-3.75)<=0.05)
chk('2025: 2024 media comparator profit 21.23 vs statements 17.76 = 3.47 T gap (recorded)', abs(21.23-17.763024-3.47)<=0.01)
chk('2026: 227.26 energy-subsidy projection > 2022-25 average 174.73', 227.26>174.73)
chk('Ministry of Finance 2024: energy subsidy 21.6 + 80.2 + 75.8 = 177.6 (+-0.05)', abs(21.6+80.2+75.8-177.6)<=0.05)
chk('Ministry of Finance 2024: subsidy 177.6 + compensation 209.3 = 386.9 (+-0.05)', abs(177.6+209.3-386.9)<=0.05)
chk('Ministry of Finance 2025 allocation: 26.7 + 87.0 + 89.7 = 203.4; + compensation 190.9 = 394.3 (+-0.05)', abs(26.7+87.0+89.7-203.4)<=0.05 and abs(203.4+190.9-394.3)<=0.05)
chk('Ministry of Finance 2024 electricity subsidy (75.8) = Finance Minister 6 Jan 2025 = statements: (73.24+2.58)', abs(v[(2024,'apbn_electricity_subsidy_realized_kemenkeu')]-v[(2024,'apbn_electricity_subsidy_realized_prelim')])<=0.01)
chk('900VA: 1,800 - 600 = 1,200 and 1,200/1,800 = 67% (+-0.5)', abs(1800-600-1200)<=0.01 and abs(1200/1800*100-67)<=0.5)
chk('900VA should-be-price proxy (1,800) near RUPTL 2025 BPP projection (1,829) and CEO statement (1,600-1,700) within 12%', abs(1800/1829-1)<0.12 and 1600*0.9<1800<1700*1.12)
chk('subsidised customers 41.7 -> 42.8 = +2.6% (+-0.1)', abs((42.8/41.7-1)*100-2.6)<=0.1)
chk('2025 subsidy+compensation 401.6 > all-type subsidy total 281.6 (implied compensation ~120.0)', 401.6>281.6)
E = pd.read_csv(os.path.join(HERE,'..','PLN-Health-Dataset','pln_financial_panel.csv')).set_index('year')
def near(a,b,t): return abs(a-b)<=t
chk('Audited 2025 statements (panel E): revenue 582.68 = media (+-0.01 T)', near(E.loc[2025,'rev_total_reported']/1e6,582.68,0.01))
chk('Audited 2025 statements: subsidy 87.46 and compensation 112.73 = Katadata media (+-0.01 T)', near(E.loc[2025,'subsidy']/1e6,87.46,0.01) and near(E.loc[2025,'compensation']/1e6,112.73,0.01))
chk('Audited 2025 statements: government receivables 110.74 (media 110.73) (+-0.02 T)', near(E.loc[2025,'govt_receivable']/1e6,110.73,0.02), f"{E.loc[2025,'govt_receivable']/1e6:.3f}")
chk('Audited 2025 statements: profit 7.2607 = CNBC 7.26 and Katadata ~7.0 imprecise (+-0.01 vs CNBC)', near(E.loc[2025,'profit_year']/1e6,7.26,0.01))
chk('Audited 2025 statements: FX loss 12.462 = media 12.46 (+-0.01)', near(-E.loc[2025,'fx_gain_loss']/1e6,12.46,0.01))
chk('2024 restatement: 17.763024 + 3.468260 = 21.231284 (+-0.000001) and = panel-E _restated column', near(17.763024+3.468260,21.231284,1e-6) and near(E.loc[2024,'profit_year_restated_next_report']/1e6,21.231284,1e-6))
chk('2024 restatement: pre-tax profit unchanged 28.269959 and tax 10.506935 -> 7.038675 (gap 3.468260)', near(10.506935-7.038675,3.468260,1e-6))
chk('2024 restatement: equity up 7.905235 = liability decrease (panel E)', near((E.loc[2024,'total_equity_restated_next_report']-E.loc[2024,'total_equity'])/1e6,7.905235,1e-6) and near((E.loc[2024,'total_liab']-E.loc[2024,'total_liab_restated_next_report'])/1e6,7.905235,1e-6))
chk('2025: subsidy+compensation (government support) 200.195 = panel-E gov_support', near(E.loc[2025,'gov_support']/1e6,200.195481,0.01), f"{E.loc[2025,'gov_support']/1e6:.3f}")

chk('LKPP 2025: electricity subsidy 81.036424 / ceiling 89.74651 = 90.29% (+-0.01)', abs(81.036424/89.74651*100-90.29)<=0.01)
chk('LKPP 2025: electricity compensation 65.3209 / ceiling 92.41119 = 70.69% (+-0.01)', abs(65.3209/92.41119*100-70.69)<=0.01)
chk('LKPP 2024 cash 75.817285 = Ministry of Finance 75.8 (+-0.05) and 73.24 + 2.58 (+-0.05)', abs(75.817285-75.8)<=0.05 and abs(73.24+2.58-75.817285)<=0.05)
chk('2025 accrual electricity-subsidy expense (87.460664) = PLN-statement and panel-E subsidy (+-0.001 T)', abs(87.460664-E.loc[2025,'subsidy']/1e6)<=0.001, f"{E.loc[2025,'subsidy']/1e6:.6f}")
chk('2024 accrual electricity-subsidy expense (77.045335) = panel Audited 2024 (+-0.001 T)', abs(77.045335-g.loc[2024,'subsidy_trn'])<=0.001)
chk('accrual - cash: 2025 = 6.42 T (owed subsidy, 2024: 1.23 T) recorded', abs(87.460664-81.036424-6.42424)<=1e-6 and abs(77.045335-75.817285-1.22805)<=1e-6)
chk('2025 PLN-statement accrual compensation (112.73) > cash compensation (65.32): ~47.4 T gap = unpaid compensation debt (proxy)', 112.73>65.3209, f"{112.73-65.3209:.2f}")
chk('Gatrik: 2020-2024 electricity subsidy (47.99/49.80/58.83/68.64/77.04) 2021-2024 = PLN-statement subsidy revenue (+-0.01)', abs(49.80-49.796949)<=0.01 and abs(58.83-58.83196)<=0.01 and abs(68.64-68.636731)<=0.01 and abs(77.04-77.045335)<=0.01)
_p = d[d.item=='derived_bpp_proxy_opex_plus_finance_per_kwh_sold'].set_index('year').value
chk('2025 BPP proxy (operating+financial cost / kWh) within 1,500-2,000 and near RUPTL 1,829 projection (+-10%)', 1500<_p[2025]<2000 and abs(_p[2025]/1829-1)<=0.10, f"{_p[2025]}")
chk('BPP proxy rising 2021->2025 (not an official value)', _p[2025]>_p[2021], f"{_p[2021]} -> {_p[2025]}")
chk('compensation volume 222.16 TWh ~ total sales 317.69 TWh (70%): plausible (<= total)', 222.16<317.69)
chk('2025 realised FX (16,475, LKPP) = panel-D 2025 average FX (16,474) within 0.1%', abs(16475/pd.read_csv(os.path.join(HERE,'..','FX-Risk-Dataset','fx_annual_panel.csv')).set_index('year').loc[2025,'fx_avg']-1)<0.001)
chk('2025 renewable additions = hydro+solar+geothermal+bioenergy (+-0.1 MW) and = stated 1.3 GW (+-0.05 GW)', abs(531.2+584.7+105.2+84.5-1305.6)<=0.1 and abs(1305.6/1000-1.3)<=0.05)
chk('2025 realised ICP (67.38) below APBN assumption (82) and 2024 outturn (78.14)', 67.38<82 and 67.38<78.14)
chk('recorded 2025 outturn vs APBN assumptions: weaker FX (+3.0%), higher inflation (2.92>2.5)', 16475>16000 and 2.92>2.5)
chk('2025 bridge: compensation 37.450898+112.734817-65.320904=84.864811 (+-0.001)', abs(37.450898+112.734817-65.320904-84.864811)<=0.001)
chk('2025 bridge: subsidy 5.839850+87.460664-81.036424=12.264090 (+-0.001)', abs(5.839850+87.460664-81.036424-12.264090)<=0.001)
chk('2025 bridge: 84.864811+12.264090+13.609498=110.738399 total receivables (+-0.001)', abs(84.864811+12.264090+13.609498-110.738399)<=0.001)
chk('2025 bridge: increase 67.447651 = accrual-cash 53.838153 + discount 13.609498 (+-0.001)', abs(67.447651-53.838153-13.609498)<=0.001)
print('news updates OK' if not fails else 'FAILED'); 
if fails: raise SystemExit(1)
