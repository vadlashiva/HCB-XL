"""Figs. 1, 4 and 5: harvest profile (model equations, Table 4 parameters),
ablation bars (Table 5) and irradiance sensitivity (Table 6).
Run from the repository root: python make_figs.py"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":"serif","font.size":10,"axes.linewidth":0.8,
                     "savefig.dpi":300,"savefig.bbox":"tight"})
# Okabe-Ito colour-blind-safe palette
GREY="#9a9a9a"; ORANGE="#E69F00"; SKY="#56B4E9"; GREEN="#009E73"; BLUE="#0072B2"; VERM="#D55E00"; PURPLE="#CC79A7"

# ---------------- Harvest profile (model, Table 3 parameters) ----------------
c=3e8; f=915e6; lam=c/f; Pt=3.0; Gt=10**(6/10); Gr=10**(2/10)
eta_rf=0.3; Psens=1e-6; eta_pv=0.15; A=1e-4; Gmax=8.0; Tday=12; zmax=0.6; Pc=71.1e-6
def Pbar(d): return Pt*Gt*Gr*lam**2/((4*np.pi)**2*d**2)
def ERF(d): pb=Pbar(d); return eta_rf*(pb+Psens)*np.exp(-Psens/pb)
print("E[P_rf,DC] 15 m = %.2f uW, 60 m = %.3f uW"%(ERF(15)*1e6, ERF(60)*1e6))
t=np.arange(0,48,1/60)               # hours since sunrise, 1-min rounds
td=t%24
G=np.where(td<=Tday, Gmax*np.sin(np.pi*td/Tday),0)
Ppv_mean=eta_pv*A*G*(1-zmax/2)
rng=np.random.default_rng(7)
zeta=rng.uniform(0,zmax,len(t)); h2=rng.exponential(1,len(t))
Ppv_inst=eta_pv*A*G*(1-zeta)
d=15.0
Prf_in=Pbar(d)*h2; Prf_inst=np.where(Prf_in>=Psens, eta_rf*Prf_in,0)
Prf_mean=np.full_like(t,ERF(d))
fig,ax=plt.subplots(figsize=(7,3.2))
for k in range(2): ax.axvspan(12+24*k,24+24*k,color="0.9",lw=0,zorder=0)
ax.plot(t,(Ppv_inst+Prf_inst)*1e6,color=BLUE,lw=0.4,alpha=0.35,label="Hybrid, one realisation (fading + clouds)")
ax.plot(t,Ppv_mean*1e6,color=ORANGE,lw=1.6,ls="-.",label="Solar, expected")
ax.plot(t,Prf_mean*1e6,color=PURPLE,lw=1.6,ls="--",label="RF at 15 m, expected")
ax.plot(t,(Ppv_mean+Prf_mean)*1e6,color=BLUE,lw=1.8,label="Hybrid (RF + solar), expected")
ax.axhline(Pc*1e6,color="k",lw=1,ls=":",label=r"Mean node consumption $P_c$")
ax.set_xlim(0,48); ax.set_ylim(0,None); ax.set_xticks(range(0,49,6))
ax.set_xlabel("Time since sunrise (h)"); ax.set_ylabel(r"Harvested DC power ($\mu$W)")
ax.grid(axis="y",color="0.88",lw=0.6)
ax.legend(fontsize=8,loc="lower center",bbox_to_anchor=(0.5,1.01),ncol=3,frameon=False)
fig.savefig("figures/Fig1_harvest_profile.png"); plt.close(fig)

# ---------------- Ablation bars (Table 4) ----------------
cfg=["C1","C2","C3","C4","C5","C6","C7"]
hnd_r=np.array([1137,1192,1487,1648,4187,4164,4412]); hnd_ci=np.array([4,4,9,31,35,36,138])
hnd_h=hnd_r/60; hci_h=hnd_ci/60
ee=np.array([4570,5315,4617,5367,9118,9125,9294]); ee_ci=np.array([9,121,10,73,39,37,36])
cols=[GREY,SKY,SKY,GREEN,BLUE,BLUE,VERM]
groups=[("Battery only",GREY),("Single-source harvesting",SKY),("Hybrid harvesting",GREEN),
        ("Hybrid + circular buffer",BLUE),("HCB-XL (proposed)",VERM)]
fig,axs=plt.subplots(1,2,figsize=(7.2,3.1))
for ax,val,ci,yl,tag,fmt in [(axs[0],hnd_h,hci_h,"Half-network lifetime (h)","(a)","%.1f"),
                         (axs[1],ee/1000,ee_ci/1000,"Energy efficiency (Mbit/J)","(b)","%.2f")]:
    b=ax.bar(cfg,val,yerr=ci,color=cols,edgecolor="k",lw=0.5,capsize=3,error_kw={"lw":0.8})
    b[-1].set_hatch("///"); b[-1].set_edgecolor("k")
    for i,v in enumerate(val):
        ax.text(i,v+ci[i]+val.max()*0.015,(fmt%v),ha="center",va="bottom",fontsize=7.5)
    ax.set_ylabel(yl); ax.set_ylim(0,val.max()*1.15); ax.grid(axis="y",color="0.88",lw=0.6); ax.set_axisbelow(True)
    ax.text(0.5,-0.22,tag,transform=ax.transAxes,ha="center",fontsize=10)
from matplotlib.patches import Patch
h=[Patch(facecolor=c_,edgecolor="k",lw=0.5,hatch=("///" if n.startswith("HCB") else None),label=n) for n,c_ in groups]
fig.legend(handles=h,loc="upper center",ncol=3,fontsize=8,frameon=False,bbox_to_anchor=(0.5,1.12))
fig.tight_layout(); fig.savefig("figures/Fig4_ablation.png"); plt.close(fig)

# ---------------- Sensitivity (Table 5) ----------------
Gx=[4,8,15]
H={"C3 Solar only":[1309,1485,2399],"C4 Hybrid":[1375,1644,2524],
   "C5 Hybrid + buffer":[2839,4171,21716],"C7 HCB-XL":[2977,4424,26200]}
D={"C3 Solar only":[1.32,1.64,2.46],"C4 Hybrid":[2.26,2.88,4.64],
   "C5 Hybrid + buffer":[4.81,7.35,17.85],"C7 HCB-XL":[5.02,7.75,18.86]}
sty={"C3 Solar only":(SKY,"s","-."),"C4 Hybrid":(GREEN,"^","--"),
     "C5 Hybrid + buffer":(BLUE,"o",":"),"C7 HCB-XL":(VERM,"D","-")}
fig,axs=plt.subplots(1,2,figsize=(7.2,3.0))
for k,(c_,m,ls) in sty.items():
    axs[0].plot(Gx,np.array(H[k])/60,color=c_,marker=m,ls=ls,lw=1.4,ms=5,label=k)
    axs[1].plot(Gx,D[k],color=c_,marker=m,ls=ls,lw=1.4,ms=5,label=k)
for k in ["C5 Hybrid + buffer","C7 HCB-XL"]:   # lower bounds at 15 W/m2
    c_,m,_=sty[k]; axs[0].plot([15],[H[k][2]/60],marker=m,ms=9,mfc="white",mec=c_,mew=1.4,ls="none")
axs[0].set_yscale("log"); axs[0].set_ylabel("Half-network lifetime (h)"); axs[0].set_ylim(15,700)
from matplotlib.ticker import FixedLocator, NullLocator, ScalarFormatter
axs[0].yaxis.set_major_locator(FixedLocator([20,50,100,200,500])); axs[0].yaxis.set_major_formatter(ScalarFormatter()); axs[0].yaxis.set_minor_locator(NullLocator())
axs[1].set_ylabel("Data delivered (M readings)")
for ax,tag in zip(axs,["(a)","(b)"]):
    ax.set_xlabel(r"Peak irradiance $G_{\max}$ (W/m$^2$)"); ax.set_xticks(Gx)
    ax.grid(color="0.88",lw=0.6); ax.text(0.5,-0.32,tag,transform=ax.transAxes,ha="center")
axs[1].legend(fontsize=8,loc="upper left")
axs[0].annotate("open markers:\nlower bounds\n(20-day horizon)",xy=(15,26200/60),xytext=(4.3,180),fontsize=7.5,
                arrowprops=dict(arrowstyle="->",lw=0.6))
fig.tight_layout(); fig.savefig("figures/Fig5_sensitivity.png"); plt.close(fig)
