"""Dataset G: fiscal burden of the energy transition / PLN support.
Sources: APBN Financial Note 2025 (Appendix Tables 1,2,5; Ch. 3; Ch. 1 sensitivity; Ch. 6 risk), PLN statements 2015-2024 (PLN-Health-Dataset panel),
PLN Statistics 2023 (Figure 11 BPP vs tariffs, Table 6 GWh).  Run: python3 build_fiscal.py   (needs pdftotext)"""
import os, re, subprocess, tempfile, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.dirname(HERE)
NOTA = os.path.join(DATA,'NOTA KEUANGAN APBN TA 2025.pdf')
PANEL = os.path.join(DATA,'PLN-Health-Dataset','pln_financial_panel.csv')
YEARS = [2020,2021,2022,2023,2024,2025]; STATUS = ['LKPP','LKPP','LKPP','LKPP','Outlook','APBN']
checks=[]
def chk(n,ok,d=''):
    checks.append(bool(ok)); print(('PASS ' if ok else 'FAIL ')+n,d)
def txt():
    out=os.path.join(tempfile.gettempdir(),'nota2025.txt')
    if not os.path.exists(out): subprocess.run(['pdftotext','-layout',NOTA,out],check=True)
    return open(out,encoding='utf-8',errors='ignore').read().split('\n')
NUMRE=re.compile(r'\(?-?\d{1,3}(?:\.\d{3})*(?:,\d+)?\)?|\s-\s')
def num(t):
    neg=t.startswith('('); t=t.strip('()').replace('.','').replace(',','.')
    v=float(t); return -v if neg else v
def rowvals(line,n):
    toks=re.findall(r'\(?-?\d{1,3}(?:\.\d{3})*(?:,\d+)?\)?',line.split('  ',1)[-1] if False else line)
    vals=[num(t) for t in toks]
    return vals[-n:] if len(vals)>=n else None
def find(lines, pattern, n, lo, hi):
    for i in range(lo,hi):
        if re.search(pattern,lines[i]):
            l=re.sub(r'^.*?(?=[A-Za-z%])','',lines[i]) ; v=rowvals(re.sub(r'^\s*[\dIVX]+\.\s+','',lines[i]) if False else lines[i][lines[i].find(re.search(pattern,lines[i]).group(0))+len(re.search(pattern,lines[i]).group(0)):],n)
            if v: return v
    raise ValueError(pattern)
def build_apbn(L):
    lo=next(i for i,l in enumerate(L) if 'ASUMSI DASAR EKONOMI MAKRO, 2020-2025' in l)
    hi=lo+170
    g=lambda p,n=6: find(L,p,n,lo,hi)
    d={'year':YEARS,'status':STATUS,
       'gdp_growth_pct':g(r'Pertumbuhan Ekonomi \(%,yoy\)'),'inflation_pct':g(r'Inflasi \(%,yoy\)'),
       'usdidr_avg':g(r'Nilai Tukar \(Rp/US\$\)'),'sbn10y_pct':g(r'Tingkat Suku Bunga SBN 10 Tahun \(%\)'),
       'icp_usd_bbl':g(r'Harga Minyak Mentah Indonesia \(US\$/barel\)'),
       'revenue_bn':g(r'PENDAPATAN NEGARA'),'spending_bn':g(r'B\.\s+BELANJA NEGARA'),'central_spending_bn':g(r'I\.\s+BELANJA PEMERINTAH PUSAT'),
       'deficit_bn':g(r'SURPLUS/ \(DEFISIT\) ANGGARAN \(A - B\)'),'deficit_pct_gdp':g(r'% Surplus/ \(Defisit\) Anggaran terhadap PDB'),
       'interest_bn':g(r'Pembayaran Bunga Utang'),'subsidy_total_bn':g(r'5\.\s+Subsidi\s'),'subsidy_energy_bn':g(r'a\. Subsidi Energi'),
       'subsidy_nonenergy_bn':g(r'b\. Subsidi Non Energi'),'other_spending_bn':g(r'8\.\s+Belanja Lain-Lain')}
    df=pd.DataFrame(d)
    # narrative values (Nota Ch. 3 pp. 3-22/3-23; 2021-2022 unavailable in this document)
    lis={2020:61103.5,2023:68702.3,2024:80724.3,2025:89746.5}; bbm={2020:47737.0,2023:95590.0,2024:112027.1,2025:113665.7}
    df['subsidy_electricity_bn']=df.year.map(lis); df['subsidy_fuel_lpg_bn']=df.year.map(bbm)
    # secondary source (browser): Databoks/Katadata citing BPK audit of LKPP 2022: electricity subsidy 2022 = Rp56.1 trn, +17% vs 2021 (2021 derived, approx.)
    sec={2022:56100.0,2021:56100.0/1.17}
    df['subsidy_electricity_secondary_bn']=df.year.map(sec); df['subsidy_electricity_secondary_source']=df.year.map({2021:'derived: 56.1 trn / 1.17 (approx.)',2022:'BPK LKPP 2022 via Databoks 23-Jun-2023'})
    df['subsidy_electricity_best_bn']=df.subsidy_electricity_bn.fillna(df.subsidy_electricity_secondary_bn)
    df['gdp_bn']=(df.deficit_bn/(df.deficit_pct_gdp/100)).abs()
    ok=df.dropna(subset=['subsidy_electricity_bn'])
    chk('elec + fuel/LPG subsidy = energy subsidy (4 yrs)', (abs(ok.subsidy_electricity_bn+ok.subsidy_fuel_lpg_bn-ok.subsidy_energy_bn)<0.2).all())
    chk('energy + non-energy = total subsidy', (abs(df.subsidy_energy_bn+df.subsidy_nonenergy_bn-df.subsidy_total_bn)<0.2).all())
    chk('revenue - spending = deficit', (abs(df.revenue_bn-df.spending_bn-df.deficit_bn)<0.2).all())
    chk('deficit/GDP matches implied GDP ~ 15-25 quadrillion? (GDP 2025 bn)', 2.3e7<df.gdp_bn.iloc[-1]<2.6e7, f"{df.gdp_bn.iloc[-1]:.0f}")
    df['electricity_subsidy_share_of_energy_pct']=df.subsidy_electricity_bn/df.subsidy_energy_bn*100
    df['energy_subsidy_pct_central_spending']=df.subsidy_energy_bn/df.central_spending_bn*100
    df['energy_subsidy_pct_gdp']=df.subsidy_energy_bn/df.gdp_bn*100
    return df
def build_sens(L):
    lo=next(i for i,l in enumerate(L) if 'Sensitivitas Belanja Pemerintah termasuk' in l)-30
    cols=['gdp_growth_+0.1pp','inflation_+0.1pp','sbn10y_+0.1pp','usdidr_+Rp100','icp_+1usd','oil_lifting_+10k_bpd','gas_lifting_+10k_boepd']
    items=[('State revenue',r'A\. Pendapatan Negara'),('Tax revenue',r'1\. Penerimaan Perpajakan'),('Non-tax revenue (PNBP)',r'2\. PNBP'),('State spending (incl. energy compensation)',r'B\. Belanja Negara'),('Central government spending',r'I\. Belanja Pemerintah Pusat'),('Transfers to regions',r'II\. Transfer ke Daerah'),('Surplus/(Deficit)',r'C\. Surplus/\(Defisit\) Anggaran')]
    rows=[]
    for name,p in items:
        v=find(L,p,7,lo,lo+40); rows.append([name]+v)
    s=pd.DataFrame(rows,columns=['apbn_item_trn_rp']+cols)
    chk('sensitivity: revenue - spending = deficit (per column)', all(abs(s.iloc[0,i]-s.iloc[3,i]-s.iloc[6,i])<0.25 for i in range(1,8)))
    return s
def build_pln(apbn):
    p=pd.read_csv(PANEL); tn=1e6      # million Rp -> trillion
    o=pd.DataFrame({'year':p.year})
    for c in ['rev_total_std','rev_ex_gov_support','opex_total','opex_fuel','opex_purchased_power','operating_profit','subsidy','compensation','gov_support','cf_receipt_subsidy','cf_receipt_compensation','govt_receivable','cf_govt_equity','cfo','cf_capex','ebitda']:
        o[c+'_trn']=p[c]/tn
    o['gov_support_share_rev_pct']=p.gov_support_share_rev*100
    o['op_profit_ex_gov_support_trn']=p.op_profit_ex_gov_support/tn
    o['cash_received_support_trn']=(p.cf_receipt_subsidy.fillna(0)+p.cf_receipt_compensation.fillna(0))/tn
    o['support_accrued_trn']=o.gov_support_trn
    o['accrual_minus_cash_trn']=o.support_accrued_trn-o.cash_received_support_trn   # ignores 2015-17 where compensation is not reported separately
    a=apbn.set_index('year')
    o['apbn_subsidy_electricity_trn']=o.year.map(a.subsidy_electricity_bn/1000)
    o['apbn_subsidy_energy_trn']=o.year.map(a.subsidy_energy_bn/1000)
    o['apbn_central_spending_trn']=o.year.map(a.central_spending_bn/1000)
    o['apbn_subsidy_electricity_trn']=o.year.map(a.subsidy_electricity_best_bn/1000)
    o['pln_subsidy_over_apbn_elec_subsidy']=o.subsidy_trn/o.apbn_subsidy_electricity_trn
    o['pln_gov_support_pct_central_spending']=o.gov_support_trn/o.apbn_central_spending_trn*100
    o['pln_compensation_pct_central_spending_other']=o.compensation_trn/o.year.map(a.other_spending_bn/1000)*100
    return o
def bpp_table(pln):
    # PLN Statistics 2023, Figure 11 (audited BPP vs average selling price, Rp/kWh); 2023 tariff cross-checked to Table 9 (1,155.47)
    b=pd.DataFrame({'year':[2019,2020,2021,2022,2023],'bpp_rp_kwh':[1385,1348,1333,1473,1599],'avg_price_rp_kwh':[1130,1071,1083,1137,1155]})
    b['gap_rp_kwh']=b.bpp_rp_kwh-b.avg_price_rp_kwh
    m=pln.set_index('year')
    b['implied_twh_sold']=b.year.map(pd.read_csv(PANEL).set_index('year').rev_electricity)*1e6/b.avg_price_rp_kwh/1e9   # electricity revenue (juta Rp) / average price -> TWh (approximation)
    b['implied_gap_cost_trn']=b.gap_rp_kwh*b.implied_twh_sold/1000
    b['recorded_subsidy_plus_comp_trn']=b.year.map(m.gov_support_trn)
    b['implied_over_recorded']=b.implied_gap_cost_trn/b.recorded_subsidy_plus_comp_trn
    return b
if __name__=='__main__':
    L=txt(); apbn=build_apbn(L); sens=build_sens(L); pln=build_pln(apbn); bpp=bpp_table(pln)
    apbn.to_csv(f'{HERE}/apbn_energy_subsidy_2020_2025.csv',index=False); sens.to_csv(f'{HERE}/apbn_sensitivity_2025.csv',index=False)
    pln.to_csv(f'{HERE}/pln_gov_support_2015_2024.csv',index=False); bpp.to_csv(f'{HERE}/bpp_tariff_gap_2019_2023.csv',index=False)
    # cross-checks vs Nota Ch. 6 Table 6.4 (PLN revenue 2019-2022 trn; 2023 = electricity revenue only)
    nota_rev={2019:285.6,2020:345.4,2021:368.2,2022:441.1}
    pr=pd.read_csv(PANEL).set_index('year').rev_total_reported/1e6
    chk('PLN revenue as reported (LK) matches Nota Table 6.4 for 2019-2022 (+-0.1)', all(abs(pr[y]-v)<0.1 for y,v in nota_rev.items()))
    chk('PLN 2023 electricity revenue 333.2 = Nota Table 6.4', abs(pd.read_csv(PANEL).set_index('year').rev_electricity[2023]/1e6-333.2)<0.1)
    chk('BPP-gap implied 2023 volume close to PLN Statistics Table 6 (288.4 TWh)', abs(bpp.set_index('year').implied_twh_sold[2023]-288.4)/288.4<0.03, f"{bpp.set_index('year').implied_twh_sold[2023]:.1f}")

    # ---- exposure facts (Nota Ch. 6, pp. 6-x; values quoted from text) ----
    facts=pd.DataFrame([
     ('Government loan guarantees for PLN borrowing (4 letters, Perpres 4/2016 and 14/2017)','Rp15,173.8 billion total loan value','Jun 2024','Financial Note 2025 Ch. 6 (Government Guarantees for the 35,000 MW programme)'),
     ('Business-viability guarantee for Jawa 1 & Jawa 4 coal plants (IPP)','US$6.6 billion total project value','Jun 2024','Financial Note 2025 Ch. 6'),
     ('Cumulative PMN equity into PLN 2015-Q4 2023','Rp50.1 trillion','2023','Financial Note 2025 Table 6.5'),
     ('PLN asset growth 2015-Q4 2023','Rp332.2 trillion (7.1x PMN leverage; DER 0.6)','2023','Financial Note 2025 Table 6.5'),
     ('Residential subsidy recipients (450/900 VA)','53.0 million (2017) -> 40.9 million customers (2024 APBN)','2017-2024','Financial Note 2025 Ch. 3'),
     ('Compensation disbursement cushioning SOE energy cash-flow stress','Cited as the main mitigant of SOE energy risk','2025','Financial Note 2025 Ch. 6'),
     ('Energy-subsidy shift to beneficiary basis','Gradual; 2025 APBN still commodity-based','2025','Financial Note 2025 Ch. 3')],
     columns=['item','value','as_of','source'])
    facts.to_csv(f'{HERE}/pln_fiscal_exposure_facts.csv',index=False)
    # ---- scenarios (illustrative, linear, ceteris paribus) ----
    base_icp,base_fx=82.0,16000.0; ss=sens.set_index('apbn_item_trn_rp'); A=apbn.set_index('year').loc[2025]
    rows=[]
    for icp in [60,70,82,90,100,110,120]:
        for fx in [15500,16000,16500,17000,17500]:
            di=icp-base_icp; df_=(fx-base_fx)/100
            dr=ss.loc['State revenue','icp_+1usd']*di+ss.loc['State revenue','usdidr_+Rp100']*df_
            ds=ss.loc['State spending (incl. energy compensation)','icp_+1usd']*di+ss.loc['State spending (incl. energy compensation)','usdidr_+Rp100']*df_
            dd=ds-dr; rows.append(dict(icp=icp,usdidr=fx,d_revenue_trn=dr,d_spending_trn=ds,d_deficit_trn=dd,deficit_trn=-A.deficit_bn/1000+dd,deficit_pct_gdp=(-A.deficit_bn/1000+dd)/(A.gdp_bn/1000)*100))
    g=pd.DataFrame(rows); g.to_csv(f'{HERE}/scenario_icp_fx_apbn2025.csv',index=False)
    chk('scenario base case reproduces APBN 2025 deficit (2.53% GDP)', abs(g[(g.icp==82)&(g.usdidr==16000)].deficit_pct_gdp.iloc[0]-2.53)<0.01)
    print('info: ICP 100 / Rp16,000 -> deficit', round(g[(g.icp==100)&(g.usdidr==16000)].deficit_pct_gdp.iloc[0],2), '% of GDP (linear approx.; statutory cap 3%)')
    # BPP shock: tariff frozen, share passed to Government as extra compensation
    bq=bpp.set_index('year'); vol=pd.read_csv(PANEL).set_index('year').rev_electricity[2024]*1e6/bq.avg_price_rp_kwh[2023]/1e9   # TWh, assumes 2023 tariff still in force
    rows=[]
    for shock in [0,2.5,5,10,15,20]:
        for absorb in [1.0,0.5]:
            extra=bq.bpp_rp_kwh[2023]*shock/100*vol/1000*absorb
            rows.append(dict(bpp_shock_pct=shock,govt_absorbs_share=absorb,base_bpp_rp_kwh=bq.bpp_rp_kwh[2023],volume_twh_2024_est=vol,extra_govt_burden_trn=extra,
              pct_of_apbn2025_energy_subsidy=extra/(A.subsidy_energy_bn/1000)*100,pct_of_apbn2025_deficit=extra/(-A.deficit_bn/1000)*100,extra_deficit_pct_gdp=extra/(A.gdp_bn/1000)*100))
    pd.DataFrame(rows).to_csv(f'{HERE}/scenario_bpp_shock.csv',index=False)
    print(g[(g.usdidr==16000)].round(2).to_string()); print(pd.DataFrame(rows).round(2).to_string())
    print(apbn.T.to_string()); print(sens.to_string()); print(bpp.round(2).to_string()); print(pln[['year','subsidy_trn','compensation_trn','gov_support_trn','cash_received_support_trn','pln_subsidy_over_apbn_elec_subsidy','pln_gov_support_pct_central_spending']].round(2).to_string())
    print(f'{sum(checks)}/{len(checks)} checks passed')
