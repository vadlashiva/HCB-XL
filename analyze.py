import json,numpy as np
R=json.load(open('res_main.json')); P=dict(Tr=60)
names=list(dict.fromkeys(r['name'] for r in R))
def ci(x): x=np.array(x,float); return x.mean(), 1.96*x.std(ddof=1)/np.sqrt(len(x))
rows={}
for n in names:
    S=[r for r in R if r['name']==n]
    d={k:ci([s[k] for s in S]) for k in ('FND','HND','deliv','EE','EEb','delay','cons','hrf','hpv','lost')}
    d['aliveEnd']=ci([s['alive'][-1] if len(s['alive'])==480 else 0 for s in S])
    d['censHND']=sum(s['HND']>=28800 for s in S)
    rows[n]=d
for n,d in rows.items():
    print(f"{n[:52]:52s} FND {d['FND'][0]:7.0f}±{d['FND'][1]:5.0f}  HND {d['HND'][0]:7.0f}±{d['HND'][1]:5.0f} (cens {d['censHND']})  deliv {d['deliv'][0]/1e6:6.2f}±{d['deliv'][1]/1e6:4.2f}M  EE {d['EE'][0]:6.0f}±{d['EE'][1]:4.0f} kb/J  EEb {d['EEb'][0]:6.2f} Mb/J  delay {d['delay'][0]:5.1f}s  hRF {d['hrf'][0]:6.0f}J hPV {d['hpv'][0]:6.0f}J cons {d['cons'][0]:6.0f}J lost {d['lost'][0]:.0f} aliveEnd {d['aliveEnd'][0]:.1f}")
# paired comparisons
def paired(a,b,k):
    A=np.array([r[k] for r in R if r['name']==a]); B=np.array([r[k] for r in R if r['name']==b])
    d=(B-A)/A*100; m,h=ci(d); 
    from scipy import stats
    t=stats.ttest_rel(B,A); return m,h,t.pvalue
pairs=[('C1','C4'),('C2','C4'),('C3','C4'),('C4','C5'),('C5','C7'),('C6','C7'),('C1','C7')]
full={n[:2]:n for n in names}
for a,b in pairs:
    for k in ('FND','HND','deliv','EE'):
        m,h,p=paired(full[a],full[b],k); print(f"{a}->{b} {k}: {m:+.1f}% ±{h:.1f}  p={p:.2g}")
# alive curves (hourly) mean
curves={n:np.mean([np.pad(r['alive'],(0,480-len(r['alive']))) for r in R if r['name']==n],0) for n in names}
json.dump({n:c.tolist() for n,c in curves.items()},open('curves.json','w'))
