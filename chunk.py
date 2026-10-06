import hcbxl,json,sys,os
a,b=int(sys.argv[1]),int(sys.argv[2])
out=[hcbxl.run((n,s,{})) for s in range(a,b) for n in hcbxl.CFG]
for r in out:
    for k,v in r.items():
        if hasattr(v,'item'): r[k]=v.item()
json.dump(out,open(f'chunk_{a}_{b}.json','w'))
print('ok',a,b)
