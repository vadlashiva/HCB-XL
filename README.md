# HCB-XL: Hybrid RF–Solar Energy Harvesting WSN with Cross-Layer Design and Adaptive Circular Buffering

Simulation code for the paper:

> Shiva Kumar V and Choupiri Shivakeshi, "HCB-XL: Energy-Efficient Clustering for Wireless Sensor Networks with Hybrid RF–Solar Energy Harvesting, Cross-Layer Design and Adaptive Circular Buffering," (under review).

## Contents
| File | Purpose |
|---|---|
| `hcbxl.py` | Network, harvesting, radio and buffer models; protocol; configurations C1–C7 (parameters in dict `P`, Table 3) |
| `chunk.py` | Runs all seven configurations for a range of seeds |
| `analyze.py` | Builds Table 4, paired t-tests, and alive-node curves |
| `sens2.py` | Sensitivity runs for Table 5 (`G4`, `G15`, `B5`, `B20`) |
| `results/res_main.json` | Raw results (30 seeds × 7 configurations) used in the paper |
| `figures/` | Figures 1–3 of the paper |

## Requirements
Python 3.9+, `pip install -r requirements.txt`

## Reproducing the results
```bash
python chunk.py 0 10
python chunk.py 10 20
python chunk.py 20 30
python -c "import json,glob; R=sum([json.load(open(f)) for f in sorted(glob.glob('chunk_*.json'))],[]); json.dump(R,open('res_main.json','w'))"
python analyze.py          # Table 4 and significance tests
python sens2.py G4; python sens2.py G15; python sens2.py B5; python sens2.py B20   # Table 5
```
Seeds are fixed, so results are exactly reproducible.

## Citation
See `CITATION.cff`.

## License
MIT — see `LICENSE`.
