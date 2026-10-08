"""Fig. 2: system model - one clustering round of HCB-XL (C7), taken from the actual simulation.
Run from the repository root: python make_fig2.py

The snapshot is read out of hcbxl.run() without changing it: a copy of its source gets one
extra line that records the network state at round SNAP and stops. All the models, the seed
and the CH election are exactly those used for the paper's results."""
import inspect, textwrap, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle, Circle
import hcbxl

SEED, SNAP = 0, 2200             # seed 0, round 2200 = 36.7 h (day 2, just after sunset): energies have spread out, all nodes alive
CFG = "C7 HCB-XL (hybrid + CB + cross-layer)"
plt.rcParams.update({"font.family": "serif", "font.size": 9, "mathtext.fontset": "dejavuserif",
                     "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.03})
VERM = "#D55E00"; BLUE = "#0072B2"; GREY = "#555555"


class _Snap(Exception):
    pass


def snapshot():
    src = textwrap.dedent(inspect.getsource(hcbxl.run))
    hook = "direct=dbs[mem]<=dmin; dist=np.where(direct,dbs[mem],dmin)"
    assert hook in src, "hcbxl.run changed - update the hook line"
    grab = ("\n        if r==__SNAP: raise __Snap(dict(xy=xy,bs=bs,alive=alive.copy(),ch=ch.copy(),mem=mem,"
            "cid=cid,j=j,direct=direct,E=E.copy(),Eh=Eh_bar.copy(),shade=shade,dbs=dbs))")
    src = src.replace(hook, hook + grab)
    ns = dict(vars(hcbxl)); ns.update(__SNAP=SNAP, __Snap=_Snap)
    exec(src, ns)
    try:
        ns["run"]((CFG, SEED, {}))
    except _Snap as s:
        return s.args[0]
    raise RuntimeError("network died before the snapshot round")


S = snapshot()
P = hcbxl.P
xy, bs, ch, mem, cid, j, direct = S["xy"], S["bs"], S["ch"], S["mem"], S["cid"], S["j"], S["direct"]
Erel = S["E"] / P["Emax"]

fig, ax = plt.subplots(figsize=(6.4, 5.4))
ax.set_xlim(-2, 102); ax.set_ylim(-2, 102); ax.set_aspect("equal")
ax.add_patch(Rectangle((0, 0), 100, 100, fc="none", ec="0.6", lw=0.8, ls="--"))

# RF field from the co-located power beacon (received power falls as 1/d^2)
for r_ in (15, 30, 45, 60):
    ax.add_patch(Circle(bs, r_, fc="none", ec=BLUE, lw=0.6, ls=(0, (2, 3)), alpha=0.55))
    ax.text(bs[0] + r_ * 0.707 + 0.8, bs[1] + r_ * 0.707 + 0.8, f"{r_} m", fontsize=6.5, color=BLUE, alpha=0.8)

# links: member -> CH (thin), member -> BS directly (dotted), CH -> BS (thick)
for k, i in enumerate(mem):
    if direct[k]:
        ax.plot(*zip(xy[i], bs), color="0.55", lw=0.6, ls=":", zorder=1)
    else:
        ax.plot(*zip(xy[i], xy[cid[j[k]]]), color="0.6", lw=0.6, zorder=1)
for c in cid:
    ax.annotate("", xy=bs, xytext=xy[c], zorder=2,
                arrowprops=dict(arrowstyle="-|>", color=VERM, lw=1.2, shrinkA=6, shrinkB=9, mutation_scale=8))

# nodes: colour = residual energy, size = canopy shading factor (sunlit nodes are bigger)
cmap = plt.get_cmap("viridis")
sz = 14 + 34 * (S["shade"] - P["shade_min"]) / (1 - P["shade_min"])
sc = ax.scatter(xy[mem, 0], xy[mem, 1], c=Erel[mem], cmap=cmap, vmin=0, vmax=1, s=sz[mem],
                edgecolors="k", linewidths=0.4, zorder=3)
ax.scatter(xy[cid, 0], xy[cid, 1], c=Erel[cid], cmap=cmap, vmin=0, vmax=1, s=150, marker="*",
           edgecolors=VERM, linewidths=1.0, zorder=4)
ax.scatter(*bs, s=230, marker="s", c="white", edgecolors="k", linewidths=1.2, zorder=5)
ax.text(bs[0], bs[1], "BS", ha="center", va="center", fontsize=6.5, weight="bold", zorder=6)
ax.text(bs[0] + 3.5, bs[1] - 3.5, "BS + RF beacon\n(915 MHz, 3 W)", ha="left", va="top", fontsize=6.8, zorder=6,
        bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.6))
dead = ~S["alive"]
if dead.any():
    ax.scatter(xy[dead, 0], xy[dead, 1], marker="x", c="0.5", s=18, lw=0.8, zorder=3)

ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
ax.set_xticks(range(0, 101, 20)); ax.set_yticks(range(0, 101, 20))
cb = fig.colorbar(sc, ax=ax, fraction=0.04, pad=0.02)
cb.set_label(r"Residual energy $E_i/E_{\max}$")

h = [Line2D([], [], marker="*", ls="none", ms=11, mfc="white", mec=VERM, label="Cluster head (CH)"),
     Line2D([], [], marker="o", ls="none", ms=6, mfc="white", mec="k", mew=0.4, label="Member node (circular buffer)"),
     Line2D([], [], color="0.6", lw=0.8, label="Member → CH"),
     Line2D([], [], color="0.55", lw=0.8, ls=":", label="Member → BS (BS closer than CH)"),
     Line2D([], [], color=VERM, lw=1.2, marker=">", ms=4, label="CH → BS (single hop, fused)"),
     Line2D([], [], color=BLUE, lw=0.8, ls=(0, (2, 3)), label="RF beacon range rings"),
     Line2D([], [], marker="o", ls="none", ms=3.5, mfc="white", mec="k", mew=0.4,
            label="Marker size ∝ solar exposure (shading)")]
if dead.any():
    h.append(Line2D([], [], marker="x", ls="none", color="0.5", label="Dead node"))
ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=2, fontsize=7.2, frameon=False)
fig.savefig("figures/Fig2_system_model.png"); plt.close(fig)
print("CHs:", len(cid), "alive:", int(S["alive"].sum()), "direct members:", int(direct.sum()))
