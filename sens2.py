import hcbxl,json,sys
tag=sys.argv[1]; out=[]
C3,C4,C5,C7='C3 Solar-only LEACH','C4 Hybrid LEACH','C5 Hybrid + CB (layered)','C7 HCB-XL (hybrid + CB + cross-layer)'
if tag.startswith('G'):
    G=float(tag[1:])
    for s in range(10):
        for n in (C3,C4,C5,C7): r=hcbxl.run((n,s,{'Gmax':G})); r.pop('alive'); r['tag']=tag; out.append(r)
else:
    B=int(tag[1:])
    for s in range(10):
        r=hcbxl.run((C7,s,{'B':B,'F':B})); r.pop('alive'); r['tag']=tag; out.append(r)
for r in out:
    for k,v in r.items():
        if hasattr(v,'item'): r[k]=v.item()
json.dump(out,open(f'sens_{tag}.json','w')); print('ok',tag)
