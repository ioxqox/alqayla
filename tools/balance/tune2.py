import os,json,sys
exec(open('sim.py').read().split("if __name__")[0])
cfg=json.loads(sys.argv[1]);pov=json.loads(sys.argv[2]) if len(sys.argv)>2 else {}
for w,o in cfg.items():
    for k,v in o.items(): W[w][k]=tuple(v) if isinstance(v,list) else v
for k,o in pov.items(): P[k].update(o)
L=loadouts();ST=[stat(w,p) for w,p in L];SM=[shot_samples(g) for g in ST]
N=int(os.environ.get('N','24'))
res=[]
for i in range(len(L)):
    wr=np.mean([duel(ST[i],ST[j],SM[i],SM[j],N) for j in range(len(L))]);res.append((wr,L[i]))
res.sort(key=lambda x:-x[0])
for wr,l in res[:6]: print('%.3f'%wr,l)
print('...')
for wr,l in res[-5:]: print('%.3f'%wr,l)
# per weapon average across its loadouts
for w in W: print(w, '%.3f'%np.mean([r for r,l in res if l[0]==w]))
# per part average effect
for k in P: 
    a=[r for r,l in res if k in l[1]];print(k,'%.3f'%np.mean(a))
