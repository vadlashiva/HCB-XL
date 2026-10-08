# HCB-XL: Buffer-Aware Cross-Layer Clustering with Hybrid RF–Solar Harvesting

Simulation code and raw results for the paper:

> Shiva Kumar V and Choupiri Shivakeshi, "Buffer-Aware Cross-Layer Clustering with Hybrid RF–Solar Harvesting for Energy-Efficient Wireless Sensor Network," submitted to *Internet of Things* (Elsevier), 2026.

HCB-XL is a clustering protocol for wireless sensor networks whose nodes harvest both RF and solar energy. A shared cross-layer information table carries residual energy, smoothed harvesting rate and buffer occupancy to every layer; cluster heads are elected by energy, harvesting rate and free buffer space, and an energy-adaptive circular buffer aggregates readings.

## Contents
| File | Purpose |
|---|---|
| `hcbxl.py` | Network, harvesting, radio and buffer models; protocol; configurations C1–C7 (parameters in dict `P`, Table 4 of the paper) |
| `chunk.py` | Runs all seven configurations for a range of seeds |
| `analyze.py` | Builds Table 5, paired t-tests, and alive-node curves |
| `sens2.py` | Sensitivity runs for Table 6 (`G4`, `G15`, `B5`, `B20`) |
| `make_figs.py` | Generates Figs. 1, 4 and 5 |
| `make_fig2.py` | Generates Fig. 2 (architecture schematic) |
| `make_fig3.py` | Generates Fig. 3 from `results/res_main.json` |
| `results/res_main.json` | Raw results (30 seeds × 7 configurations) used in the paper |
| `figures/` | Figures 1–5 of the paper (300 dpi PNG) |

## Requirements
Python 3.9+, `pip install -r requirements.txt`

## Reproducing the results
```bash
python chunk.py 0 10
python chunk.py 10 20
python chunk.py 20 30
python -c "import json,glob; R=sum([json.load(open(f)) for f in sorted(glob.glob('chunk_*.json'))],[]); json.dump(R,open('res_main.json','w'))"
python analyze.py          # Table 5 and significance tests
python sens2.py G4; python sens2.py G15; python sens2.py B5; python sens2.py B20   # Table 6
```
Seeds are fixed, so results are exactly reproducible.

## Reproducing the figures
```bash
python make_figs.py        # Fig. 1 (harvest profile), Fig. 4 (ablation), Fig. 5 (sensitivity)
python make_fig2.py        # Fig. 2 (architecture schematic)
python make_fig3.py        # Fig. 3 (alive nodes), from results/res_main.json
```

## Citation
See `CITATION.cff`.

## License
MIT — see `LICENSE`.
