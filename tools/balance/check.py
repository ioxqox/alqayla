import json
exec(open('search.py').read().split("best=score(X)")[0])
X=json.loads(open('x.json').read())
s=score(X,N=150,seed=11);print('max dev',round(s[0],3),{k:round(float(v),3) for k,v in s[3].items()})
o=sorted(zip(s[1],s[2]),key=lambda z:-z[0]);print([(round(float(a),3),b) for a,b in o[:3]]);print([(round(float(a),3),b) for a,b in o[-3:]])
apply(X);L=loadouts();ST=[stat(w,p) for w,p in L];SM=[shot_samples(g) for g in ST]
base=[i for i,(w,p) in enumerate(L) if p==(None,None,None)]
for i in base: print(L[i][0].ljust(8),' '.join('%.2f'%duel(ST[i],ST[j],SM[i],SM[j],3000) for j in base))
