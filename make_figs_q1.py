#!/usr/bin/env python3
"""Q1 redesign for Fiscal-Burden figures (5 panels)."""
import os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "LaTeX", "figs")
os.makedirs(FIG, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 300, "savefig.dpi": 300,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.10,
    "font.family": "serif", "font.serif": ["STIX Two Text", "Times New Roman", "DejaVu Serif"],
    "font.size": 8, "axes.titlesize": 9, "axes.labelsize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
    "axes.linewidth": 0.7, "grid.linewidth": 0.4, "lines.linewidth": 1.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.22, "grid.linestyle": "--",
})

C_SUB = "#3B6EA5"
C_COMP = "#D67E2C"
C_SHARE = "#1A1A1A"
C_BPP = "#B23C17"
C_TAR = "#2C3E50"
C_GAPFILL = "#F5D7C8"
C_ACT = "#0F0F0F"
C_MED = "#2A6FA0"
C_BAND = "#D4E6F1"
C_NAIVE = "#95A5A6"
C_DEF = "#2A6FA0"
C_CAP = "#C0392B"
C_BPP100 = "#2A5A8C"
C_BPP50 = "#AAB7B8"
C_ICP = "#2E86AB"
C_COST = "#8E2F2F"
C_SUPP = "#1A6B4A"

REPORT=[]

def audit(fig,name):
    fig.canvas.draw()
    seen=set(); texts=[]
    for o in list(fig.texts):
        if id(o) not in seen:
            seen.add(id(o)); texts.append(o)
    for ax in fig.axes:
        for o in list(ax.texts)+[ax.title,ax.xaxis.label,ax.yaxis.label]+list(ax.get_xticklabels())+list(ax.get_yticklabels()):
            if id(o) not in seen:
                seen.add(id(o)); texts.append(o)
    for leg in fig.findobj(lambda o: isinstance(o, Legend)):
        for o in leg.get_texts():
            if id(o) not in seen:
                seen.add(id(o)); texts.append(o)
    boxes=[(t.get_text()[:26],t.get_window_extent()) for t in texts if t.get_visible() and t.get_text().strip()]
    pairs=[]
    for i in range(len(boxes)):
        for j in range(i+1,len(boxes)):
            if boxes[i][1].overlaps(boxes[j][1]): pairs.append((boxes[i][0],boxes[j][0]))
    REPORT.append((name,len(boxes),pairs))

# ---------- load ----------
G=pd.read_csv(os.path.join(HERE,"pln_gov_support_2015_2024.csv")).sort_values("year")
B=pd.read_csv(os.path.join(HERE,"bpp_tariff_gap_2019_2023.csv"))
SC_ICP=pd.read_csv(os.path.join(HERE,"scenario_icp_fx_apbn2025.csv"))
SC_BPP=pd.read_csv(os.path.join(HERE,"scenario_bpp_shock.csv"))
BT=pd.read_csv(os.path.join(HERE,"ml_hier_fiscal_coherent_backtest.csv"))
FC=pd.read_csv(os.path.join(HERE,"ml_hier_fiscal_coherent_forecast_2026_2027.csv"))
MLNK=pd.read_csv(os.path.join(HERE,"ml_fiscal_macro_realized_link.csv"))

# ===== Fig1: Govt support stacked + share =====
years=G.year.values
sub=G.subsidy_trn.values
comp=np.where(np.isnan(G.compensation_trn.values),0,G.compensation_trn.values)
tot=G.gov_support_trn.values
share=G.gov_support_share_rev_pct.values

fig, ax1 = plt.subplots(figsize=(7.4,4.2))
x=np.arange(len(years))
w=0.62
b1=ax1.bar(x, sub, width=w, color=C_SUB, edgecolor="white", linewidth=0.7, label="Subsidy (accrued)")
b2=ax1.bar(x, comp, bottom=sub, width=w, color=C_COMP, edgecolor="white", linewidth=0.7, label="Compensation (accrued)")
# totals on top
for i, (t, y) in enumerate(zip(tot, x)):
    ax1.text(y, t+4, f"{t:.0f}", ha="center", va="bottom", fontsize=6.2, color="#2C3E50")
ax1.set_xticks(x); ax1.set_xticklabels([str(int(y)) for y in years], rotation=0)
ax1.set_ylabel("Government support (Rp trillion)")
ax1.set_title("Government support to PLN: level and composition", loc="left", pad=10)
ax1.set_ylim(0, 250)
# missing label for early years
ax1.text(0.5, 18, "Comp. n.a.", fontsize=6, color="white", ha="center", va="center", style="italic")
# right axis share
ax2=ax1.twinx()
ax2.plot(x, share, color=C_SHARE, marker="o", markersize=3.5, lw=1.4, markerfacecolor="white", markeredgewidth=0.9, markeredgecolor=C_SHARE)
ax2.set_ylabel("Share of PLN revenue (%)")
ax2.set_ylim(8, 42)
ax2.grid(False)
ax2.spines["top"].set_visible(False)
ax2.tick_params(labelbottom=False)
ax2.set_xticks([])
# annotate 2025 composition
ax1.annotate("56.3% compensation\n110.7 T receivables", xy=(10,200), xytext=(5.2,218),
            fontsize=6.8, color="#2C3E50", ha="left",
            arrowprops=dict(arrowstyle="->", color="#2C3E50", lw=0.9, shrinkB=4),
            bbox=dict(boxstyle="round,pad=0.32", fc="white", ec="#BDC3C7"))
h1,l1=ax1.get_legend_handles_labels()
# need line handle for share
share_h=Line2D([0],[0], color=C_SHARE, marker="o", markerfacecolor="white", markersize=4, lw=1.3)
fig.legend(handles=[h1[0],h1[1],share_h], labels=["Subsidy (accrued)","Compensation (accrued)","Share of PLN revenue (%)"],
           loc="lower center", ncol=3, frameon=True, facecolor="white", edgecolor="#BDC3C7", bbox_to_anchor=(0.5, -0.02))
fig.subplots_adjust(left=0.09, right=0.92, top=0.88, bottom=0.20)
audit(fig,"fig1"); fig.savefig(os.path.join(FIG,"fig1_gov_support.png")); fig.savefig(os.path.join(FIG,"fig1_gov_support.pdf")); plt.close(fig)

# ===== Fig2: BPP vs tariff gap =====
fig, ax = plt.subplots(figsize=(7.0,3.9))
yrs=B.year.values
bpp=B.bpp_rp_kwh.values
tar=B.avg_price_rp_kwh.values
gap=B.gap_rp_kwh.values
ax.plot(yrs, bpp, color=C_BPP, marker="s", markersize=4, lw=1.6, label="BPP (audited cost)")
ax.plot(yrs, tar, color=C_TAR, marker="o", markersize=4, lw=1.6, label="Average tariff")
ax.fill_between(yrs, bpp, tar, color=C_GAPFILL, alpha=0.55, step=None, zorder=1)
# gap labels centred
for yy, bb, tt, gg in zip(yrs, bpp, tar, gap):
    mid=(bb+tt)/2
    ax.text(yy, mid, f"{gg:.0f}", ha="center", va="center", fontsize=6.5, color="#6E2C00",
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="#EDBB99", alpha=0.92))
# annotations for widening
ax.annotate("", xy=(2023,1599), xytext=(2019,1385), arrowprops=dict(arrowstyle="<->", color="#7F8C8D", lw=0.9))
ax.text(2021, 1620, "BPP +15% (2019-23)", fontsize=6.5, ha="center", color="#7F8C8D")
ax.set_xlabel("Year")
ax.set_ylabel("Rp / kWh")
ax.set_title("Audited BPP versus average tariff and cost-recovery gap", loc="left", pad=10)
ax.set_xticks(yrs); ax.set_xlim(2018.7,2023.3); ax.set_ylim(1000,1700)
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
fig.legend(loc="lower center", ncol=2, frameon=True, facecolor="white", edgecolor="#BDC3C7", bbox_to_anchor=(0.5,-0.06))
fig.subplots_adjust(left=0.11, right=0.97, top=0.88, bottom=0.22)
audit(fig,"fig2"); fig.savefig(os.path.join(FIG,"fig2_bpp_gap.png")); fig.savefig(os.path.join(FIG,"fig2_bpp_gap.pdf")); plt.close(fig)

# ===== Fig3: Forecast coherent =====
# combine BT+FC
years_bt=BT.year.values
actual_bt=BT.actual.values
med_bt=BT.coherent_median.values
lo_bt=BT.lo90.values
hi_bt=BT.hi90.values
years_fc=FC["year"].values
med_fc=FC["median"].values
lo_fc=FC["lo90"].values
hi_fc=FC["hi90"].values

# also include naive for context but faint
naive_bt=BT.naive.values

fig, ax = plt.subplots(figsize=(7.8,4.4))
mask = years_bt >= 2023
ax.fill_between(years_bt[mask], lo_bt[mask], hi_bt[mask], color=C_BAND, alpha=0.92, linewidth=0, label="90% interval (coherent)")
ax.fill_between(years_fc, lo_fc, hi_fc, color=C_BAND, alpha=0.62, linewidth=0)
for xb, yb in [(2021, hi_bt[years_bt==2021][0]), (2022, hi_bt[years_bt==2022][0])]:
    ax.annotate("", xy=(xb, 465), xytext=(xb, 430), arrowprops=dict(arrowstyle="-|>", color="#B0B0B0", lw=0.8))
ax.plot(np.concatenate([years_bt, years_fc]), np.concatenate([med_bt, med_fc]), color=C_MED, lw=1.9, marker="o", markersize=3.6, label="Coherent median")
ax.plot(years_bt, actual_bt, color=C_ACT, lw=1.6, marker="s", markersize=4.4, markerfacecolor="white", markeredgewidth=0.9, label="Actual support")
ax.plot(years_bt, naive_bt, color=C_NAIVE, lw=1.0, ls="--", marker="x", markersize=3.5, label="Naive")
ax.set_ylim(30, 485)
ax.set_xlim(2020.6, 2027.6)
ax.axvline(2025.5, color="#BDC3C7", lw=0.9, ls=":")
ax.text(2025.5, 467, "forecast \u2192", fontsize=6.5, ha="center", va="bottom", color="#7F8C8D",
        bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="#BDC3C7"))
ax.text(2023.8, 275, "90% band", fontsize=6.5, color=C_MED, ha="center", bbox=dict(boxstyle="round,pad=0.16", fc="white", ec=C_MED))
ax.text(2021.5, 405, "2021\u201322 intervals >Rp900T\ntruncated", fontsize=5.8, color="#5D6D7E", ha="center", va="center",
        bbox=dict(boxstyle="round,pad=0.24", fc="#FDF2E9", ec="#EDBB99"))
ax.set_xticks([2021,2022,2023,2024,2025,2026,2027])
ax.set_xlabel("Year")
ax.set_ylabel("Required support (Rp trillion)")
ax.set_title("Coherent probabilistic forecast: backtest and conditional outlook", loc="left", pad=10)
fig.legend(loc="lower center", ncol=3, frameon=True, facecolor="white", edgecolor="#BDC3C7", bbox_to_anchor=(0.5,-0.06))
fig.subplots_adjust(left=0.10, right=0.97, top=0.88, bottom=0.20)
audit(fig,"fig3"); fig.savefig(os.path.join(FIG,"fig3_forecast.png")); fig.savefig(os.path.join(FIG,"fig3_forecast.pdf")); plt.close(fig)

# ===== Fig4: scenarios 2 panels =====
icp16=SC_ICP[SC_ICP.usdidr==16000].sort_values("icp")
bpp100=SC_BPP[SC_BPP.govt_absorbs_share==1.0].sort_values("bpp_shock_pct")
bpp50=SC_BPP[SC_BPP.govt_absorbs_share==0.5].sort_values("bpp_shock_pct")
fig, (a1,a2)=plt.subplots(1,2, figsize=(8.4,4.2), gridspec_kw={"width_ratios":[1,1]})
a1.plot(icp16.icp, icp16.deficit_pct_gdp, color=C_DEF, lw=1.7, marker="o", markersize=3.2)
a1.axhline(3.0, color=C_CAP, lw=1.0, ls="--", dashes=(4,3))
a1.fill_between(icp16.icp, icp16.deficit_pct_gdp, 3.0, where=(icp16.deficit_pct_gdp>=3.0), color="#FADBD8", alpha=0.55, step="mid")
a1.scatter([100],[3.04], s=46, color=C_CAP, edgecolor="white", linewidth=0.8, zorder=5)
a1.set_xlabel("ICP (USD / bbl)")
a1.set_ylabel("Deficit (% of GDP)")
a1.set_title("(a) Deficit at Rp 16,000 / USD", loc="left", pad=8)
a1.set_xlim(58,122); a1.set_ylim(1.6,3.98)
a2.plot(bpp100.bpp_shock_pct, bpp100.extra_govt_burden_trn, color=C_BPP100, lw=1.8, marker="s", markersize=3.4, label="Govt absorbs 100%")
a2.plot(bpp50.bpp_shock_pct, bpp50.extra_govt_burden_trn, color=C_BPP50, lw=1.4, ls="--", dashes=(4,2), marker="o", markersize=3.2, label="Govt absorbs 50%")
a2.scatter([10],[48.9], s=36, color=C_BPP100, edgecolor="white", linewidth=0.7, zorder=5)
a2.set_xlabel("BPP shock (%)")
a2.set_ylabel("Extra burden (Rp trillion)")
a2.set_title("(b) BPP shock (2024 volume)", loc="left", pad=8)
a2.set_xlim(-0.5,20.5); a2.set_ylim(0,108)
fig.suptitle("Calibrated fiscal stress tests  (linear, ceteris paribus, official sensitivities)", fontsize=7.4, y=0.99, color="#2C3E50")
lh = [Line2D([0],[0], color=C_BPP100, lw=1.8, marker="s", markersize=4, markerfacecolor=C_BPP100, markeredgecolor="white"),
      Line2D([0],[0], color=C_BPP50, lw=1.4, ls="--", dashes=(4,2), marker="o", markersize=4, markerfacecolor=C_BPP50, markeredgecolor="white")]
fig.legend(handles=lh, labels=["Govt absorbs 100%", "Govt absorbs 50%"], loc="lower center", ncol=2,
           frameon=True, facecolor="white", edgecolor="#BDC3C7", bbox_to_anchor=(0.5, -0.03))
fig.subplots_adjust(left=0.08, right=0.98, top=0.86, bottom=0.22, wspace=0.30)
audit(fig,"fig4"); fig.savefig(os.path.join(FIG,"fig4_scenarios.png")); fig.savefig(os.path.join(FIG,"fig4_scenarios.pdf")); plt.close(fig)

# ===== Fig5: 2025 macro divergence =====
row2025=MLNK[MLNK.year==2025].iloc[0]
cats=["ICP", "PLN energy cost", "Govt support"]
levels=["67.4 vs 78.1 USD/bbl", "393.8T vs 357.9T", "200.2T vs 177.2T"]
vals=[row2025.d_icp_pct, row2025.d_energy_cost_pct, row2025.d_gov_support_pct]
cols=[C_ICP, C_COST, C_SUPP]
fig, ax = plt.subplots(figsize=(7.6,3.0))
y=np.arange(len(cats))
ax.barh(y, vals, color=cols, edgecolor="white", height=0.42, zorder=3)
ax.axvline(0, color="black", lw=0.9, zorder=4)
for i, v in enumerate(vals):
    lab=f"{v:+.1f}%"
    ha="left" if v>0 else "right"
    off=0.7 if v>0 else -0.7
    ax.text(v+off, y[i], lab, va="center", ha=ha, fontsize=8, color="#1A1A1A", weight="bold",
            bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="#BDC3C7"), zorder=6)
ax.set_yticks(y)
ax.set_yticklabels(cats, fontsize=8, color="#1A1A1A", weight="bold", va="center")
ax.tick_params(axis="y", length=0, pad=8)
for i, lv in enumerate(levels):
    ax.text(-19.8, y[i]-0.30, lv, fontsize=5.8, color="#5D6D7E", ha="left", va="top", style="italic")
ax.set_xlabel("Year-on-year change, 2024 \u2192 2025 (%)", fontsize=7.5)
ax.set_xlim(-20, 19)
ax.set_ylim(-0.8, 2.8)
ax.set_xticks([-15,-10,-5,0,5,10,15])
ax.set_xticklabels(["-15%","-10%","-5%","0","5%","10%","15%"], fontsize=7)
fig.subplots_adjust(left=0.20, right=0.97, top=0.88, bottom=0.20)
audit(fig,"fig5"); fig.savefig(os.path.join(FIG,"fig5_macro_link.png")); fig.savefig(os.path.join(FIG,"fig5_macro_link.pdf")); plt.close(fig)

print("=== overlap audit ===")
for n,nt,pairs in REPORT:
    print(f"{n}: {nt} texts, {len(pairs)} overlaps")
    for a,b in pairs[:10]:
        print("  ",a," x ",b)
print("Q1 figs written to",FIG)
