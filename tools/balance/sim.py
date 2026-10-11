import numpy as np, itertools, json, sys
rng=np.random.default_rng(7)
import os
W={'fard':dict(draw=0,model='pistol',rof=260,ammo=6,mul=1,reload=1300,spread=20,sway=3,pel=0,fuse=0),
'naqsh':dict(draw=70,model='pistol',rof=300,ammo=5,mul=1.2,reload=1550,spread=12,sway=8,pel=0,fuse=0),
'shotgun':dict(draw=150,model='shot',rof=750,ammo=2,mul=1,reload=1900,spread=44,sway=3,pel=7,fuse=0,pB=(7,9),pH=(12,14)),
'fitil':dict(draw=240,model='fitil',rof=0,ammo=1,mul=2.7,reload=2000,spread=6,sway=10,pel=0,fuse=430)}
P=json.load(open('/home/claude/sim/parts.json'))
for w,o in json.loads(os.environ.get('OV','{}')).items(): W[w].update(o)
if os.environ.get('POV'): P.update(json.loads(os.environ['POV']))
DRAW_BASE=80;HP=150
def stat(w,parts):
    g=dict(W[w]);g['draw']+=DRAW_BASE;g['pdm']=1
    for k in parts:
        if not k: continue
        p=P[k]
        for a,v in p.get('m',{}).items(): g[a]*= (1+(v-1)*0.2) if (g['model']=='shot' and p['s']=='b' and a=='spread') else v
        for a,v in p.get('add',{}).items(): g[a]+=v
        for a,v in p.get('set',{}).items(): g[a]=v
    g['ammo']=max(1,int(round(g['ammo'])));g['draw']=max(0,g['draw'])
    return g
AIM_SD=9.0   # human aim error (px)
RB=23; RH=11; HEAD_Y=-76
def shot_samples(g,n=6000):
    # aim at chest with human error + sway (random phase) + fuse lead error
    err=rng.normal(0,AIM_SD,(n,2))+ (rng.uniform(-1,1,(n,2))*g['sway']*1.3) + rng.normal(0,g['fuse']/100*2.2,(n,2))
    pel=g['pel'] or 1
    a=rng.uniform(0,2*np.pi,(n,pel));r=np.sqrt(rng.uniform(0,1,(n,pel)))*g['spread']
    x=err[:,0:1]+np.cos(a)*r; y=err[:,1:2]+np.sin(a)*r
    head=(x**2+(y-HEAD_Y)**2)<RH**2
    body=((np.abs(x)<RB)&(y>-62)&(y<112))&~head
    if not g['pel']:
        near=(~head)&(~body)&(np.abs(x)<RB+10)&(y>-62-10)&(y<112)
        body=body|near
    if g['pel']:
        dmg=(head*rng.uniform(*W_pel(g,'pH'),(n,pel))+body*rng.uniform(*W_pel(g,'pB'),(n,pel)))*g['mul']*g['pdm']
    else:
        dmg=(head*rng.uniform(40,48,(n,1))+body*rng.uniform(15,22,(n,1)))*g['mul']
    return dmg.sum(1)
def W_pel(g,k): return W['shotgun'][k]
CAD=380
def duel(A,B,sa,sb,N):
    wins=0
    for _ in range(N):
        hp=[HP,HP];t=[rng.normal(380,70)+A['draw']+A['fuse'], rng.normal(380,70)+B['draw']+B['fuse']]
        am=[A['ammo'],B['ammo']];S=[A,B];D=[sa,sb]
        while True:
            i=0 if t[0]<=t[1] else 1;j=1-i;g=S[i]
            hp[j]-=D[i][rng.integers(len(D[i]))]
            if hp[j]<=0: wins+= (i==0);break
            am[i]-=1
            if am[i]<=0: am[i]=g['ammo'];t[i]+=g['reload']+g['fuse']+rng.normal(120,40)
            else: t[i]+=max(g['rof'],CAD)+g['fuse']+rng.normal(60,30)
    return wins/N
def loadouts():
    out=[]
    for w in W:
        md=W[w]['model']
        bs=[None,'b_long','b_short'];gs=[None,'g_sidr','g_bone']
        acs=[None]+[k for k,p in P.items() if p['s']=='a' and p.get('for')==md]
        for b,gr,ac in itertools.product(bs,gs,acs): out.append((w,(b,gr,ac)))
    return out
if __name__=='__main__':
    L=loadouts();ST=[stat(w,p) for w,p in L];SM=[shot_samples(g) for g in ST]
    base=[i for i,(w,p) in enumerate(L) if p==(None,None,None)]
    print('== base weapons head to head ==')
    for i in base:
        row=[duel(ST[i],ST[j],SM[i],SM[j],3000) for j in base]
        print(L[i][0].ljust(8),' '.join('%.2f'%x for x in row), ' avg %.3f'%np.mean(row))
    print('== every loadout vs the whole field ==')
    res=[]
    for i in range(len(L)):
        js=rng.integers(len(L),size=40)
        wr=np.mean([duel(ST[i],ST[j],SM[i],SM[j],120) for j in js])
        res.append((wr,L[i]))
    res.sort(key=lambda x:-x[0])
    for wr,l in res[:8]: print('%.3f'%wr,l)
    print('...');
    for wr,l in res[-5:]: print('%.3f'%wr,l)
    print('max %.3f min %.3f'%(res[0][0],res[-1][0]))
