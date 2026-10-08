# HCB-XL: Buffer-Aware Cross-Layer Clustering with Hybrid RF–Solar Harvesting

Simulation code and raw results for the paper:

> Shiva Kumar V and Choupiri Shivakeshi, "Buffer-Aware Cross-Layer Clustering with Hybrid RF–Solar Harvesting for Energy-Efficient Wireless Sensor Network," submitted to *Internet of Things* (Elsevier), 2026.

HCB-XL is a clustering protocol for wireless sensor networks whose nodes harvest both RF and solar energy. A shared cross-layer information table carries residual energy, smoothed harvesting rate and buffer occupancy to every layer; cluster heads are elected by energy, harvesting rate and free buffer space, and an energy-adaptive circular buffer aggregates readings.

## Contents
| File | Purpose |
|---|---|
| `hcbxl.py` | Network, harvesting, radio and buffer models; protocol; configurations C1–C7 and external baseline C8, EECHS (parameters in dict `P`, Table 4 of the paper) |
| `chunk.py` | Runs all seven configurations for a range of seeds |
| `analyze.py` | Builds Table 5, paired t-tests, and alive-node curves |
| `sens2.py` | Sensitivity runs for Table 6 (`G4`, `G15`, `B5`, `B20`) |
| `make_figs.py` | Generates Figs. 1, 5 and 6 |
| `make_fig2.py` | Generates Fig. 2 (system model: one HCB-XL clustering round taken from the simulation) |
| `make_fig3.py` | Generates Fig. 3 (cross-layer architecture schematic) |
| `make_fig4.py` | Generates Fig. 4 from `results/res_main.json` |
| `results/res_main.json` | Raw results (30 seeds × 7 configurations) used in the paper |
| `results/res_c8.json` | Raw results for C8 (EECHS re-implementation, 30 seeds), Section 5.7 |
| `figures/` | Figures 1–6 of the paper (300 dpi PNG) |

## Requirements
Python 3.9+, `pip install -r requirements.txt`

## Reproducing the results
```bash
python chunk.py 0 10
python chunk.py 10 20
python chunk.py 20 30
python -c "import json,glob; R=sum([json.load(open(f)) for f in sorted(glob.glob('chunk_*.json'))],[]); json.dump(R,open('res_main.json','w'))"
python analyze.py          # Table 5 and significance tests
python -c "import hcbxl,json; json.dump([hcbxl.run(('C8 EECHS (hybrid + CB)',s,{})) for s in range(30)],open('res_c8.json','w'),default=float)"   # C8 row of Table 5
python sens2.py G4; python sens2.py G15; python sens2.py B5; python sens2.py B20   # Table 6
```
Seeds are fixed, so results are exactly reproducible.

## Reproducing the figures
```bash
python make_figs.py        # Fig. 1 (harvest profile), Fig. 5 (ablation), Fig. 6 (sensitivity)
python make_fig2.py        # Fig. 2 (system model, seed 0, round 2200)
python make_fig3.py        # Fig. 3 (cross-layer architecture)
python make_fig4.py        # Fig. 4 (alive nodes), from results/res_main.json
```

## Citation
See `CITATION.cff`.

## License
MIT — see `LICENSE`.
