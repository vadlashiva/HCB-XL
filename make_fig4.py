"""Fig. 4: alive nodes versus time, from the raw results in results/res_main.json.
Run from the repository root: python make_fig4.py"""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":"serif","font.size":10,"savefig.dpi":300,"savefig.bbox":"tight"})
R=json.load(open("results/res_main.json"))
names=list(dict.fromkeys(r["name"] for r in R))
cur={n:np.mean([np.pad(r["alive"],(0,480-len(r["alive"]))) for r in R if r["name"]==n],0) for n in names}
t=np.arange(480)/24  # hourly samples -> days
lab={"C1":"C1 Battery only","C2":"C2 RF only","C3":"C3 Solar only","C4":"C4 Hybrid",
     "C5":"C5 Hybrid + circular buffer","C6":"C6 Hybrid + buffer + energy-aware election","C7":"C7 HCB-XL (proposed)"}
sty={"C1":("#000000",":","x"),"C2":("#56B4E9","--","s"),"C3":("#E69F00","-.","^"),"C4":("#009E73","-","v"),
     "C5":("#0072B2","--","o"),"C6":("#CC79A7",(0,(3,1,1,1)),"P"),"C7":("#D55E00","-","D")}
fig,axs=plt.subplots(1,2,figsize=(7.4,3.3),gridspec_kw={"width_ratios":[1.15,1]})
for ax,xmax,ymax,me in [(axs[0],6,105,6),(axs[1],20,25,24)]:
    for k in range(int(xmax)+1): ax.axvspan(k+0.5,k+1,color="0.9",lw=0,zorder=0)
    for n in names:
        k=n[:2]; c,ls,m=sty[k]
        ax.plot(t,cur[n],color=c,ls=ls,lw=1.8 if k=="C7" else 1.3,marker=m,ms=4,markevery=(3,me),
                label=lab[k],zorder=3 if k=="C7" else 2)
    ax.set_xlim(0,xmax); ax.set_ylim(0 if ymax<50 else -2,ymax); ax.grid(axis="y",color="0.88",lw=0.6)
    ax.set_xlabel("Time (days)")
axs[0].set_ylabel("Alive nodes"); axs[1].set_xticks(range(0,21,4)); axs[1].set_ylabel("Alive nodes (zoom, 0\u201325)")
axs[0].text(0.5,-0.27,"(a)",transform=axs[0].transAxes,ha="center")
axs[1].text(0.5,-0.27,"(b)",transform=axs[1].transAxes,ha="center")
h,l=axs[0].get_legend_handles_labels()
fig.legend(h,l,loc="lower center",bbox_to_anchor=(0.5,1.0),ncol=2,fontsize=8,frameon=False)
fig.tight_layout(); fig.savefig("figures/Fig4_alive_nodes.png")
for n in names: print(n[:2], "alive after 3rd night (day 3): %.1f"%cur[n][72], " end: %.1f"%cur[n][-1])
