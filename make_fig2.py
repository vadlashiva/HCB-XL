"""Fig. 2: HCB-XL cross-layer architecture (schematic).
Run from the repository root: python make_fig2.py"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "dejavuserif",
                     "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.03})
VERM = "#D55E00"

layers = [
    ("Application layer", "Sensing, member circular buffer,\nenergy-adaptive flush (Eq. 8)"),
    ("Transport layer", "Flush-level reliability (ACK / retry)"),
    ("Network layer", "CH-side buffer, fusion, single-hop to BS"),
    ("Data-link layer", "Harvest- & buffer-aware CH election (Eq. 11), TDMA"),
    ("Physical layer", "RF (Eqs. 1–2) + solar (Eqs. 3–4) harvesting,\nenergy store (Eq. 6), radio"),
]
rows = [(r"$E_i$", "residual energy"),
        (r"$\bar{E}_{h,i}$", "harvest rate"),
        (r"$b_i/B_i$", "buffer occupancy"),
        (r"$d_{i,\mathrm{CH}},\ d_{i,\mathrm{BS}}$", "distances")]

fig, ax = plt.subplots(figsize=(7.2, 4.4))
ax.set_xlim(0, 100); ax.set_ylim(0, 60); ax.axis("off")
x0, w, h, gap, top = 1, 55, 10.0, 1.2, 59.5
tx, tw, ty, th = 65, 34, 12, 36
tcx, tcy = tx, ty + th / 2
for k, (title, body) in enumerate(layers):
    y = top - (k + 1) * h - k * gap
    ax.add_patch(FancyBboxPatch((x0, y), w, h, boxstyle="round,pad=0,rounding_size=0.8",
                                fc="#EEF2F7", ec="#2B3A4A", lw=1.0))
    ax.text(x0 + 1.8, y + h - 1.4, title, weight="bold", fontsize=9.5, va="top")
    ax.text(x0 + 1.8, y + h - 4.3, body, fontsize=7.8, va="top", linespacing=1.2)
    ax.add_patch(FancyArrowPatch((x0 + w + 0.6, y + h / 2), (tcx - 0.4, tcy), arrowstyle="<|-|>",
                                 mutation_scale=9, lw=1.0, color="#4A4A4A", shrinkA=0, shrinkB=0))
ax.add_patch(FancyBboxPatch((tx, ty), tw, th, boxstyle="round,pad=0,rounding_size=1.0",
                            fc="#FFF4E8", ec=VERM, lw=1.6))
ax.text(tx + tw / 2, ty + th - 2.5, "Cross-layer\ninformation table", ha="center", va="top",
        weight="bold", fontsize=9.5, linespacing=1.2)
ax.plot([tx + 2.5, tx + tw - 2.5], [ty + th - 10, ty + th - 10], color=VERM, lw=0.7)
for k, (sym, desc) in enumerate(rows):
    yy = ty + th - 14.0 - k * 5.0
    ax.text(tx + 2.0, yy, sym, fontsize=9, va="center")
    ax.text(tx + 15.5, yy, desc, fontsize=7.8, va="center")
fig.savefig("figures/Fig2_architecture.png"); plt.close(fig)
