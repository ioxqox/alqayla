import os,json,sys,copy,time
exec(open('sim.py').read().split("if __name__")[0])
W0=copy.deepcopy(W);P0=copy.deepcopy(P)
X={'fard_rl':1200,'naqsh_mul':1.12,'shot_pb':7.6,'shot_rl':1650,'fitil_rl':1900,'fitil_mul':4.1,'light_rl':.92,'coarse_pdm':1.1,'soft_pdm':.85,'wide_draw':30,'bone_draw':-30,'sidr_draw':35,'fuse_f':.9,'powder_rl':.88}
STEP={'fard_rl':60,'naqsh_mul':.03,'shot_pb':.2,'shot_rl':80,'fitil_rl':80,'fitil_mul':.1,'light_rl':.03,'coarse_pdm':.05,'soft_pdm':.04,'wide_draw':15,'bone_draw':10,'sidr_draw':10,'fuse_f':.04,'powder_rl':.03}
def apply(x):
    global W,P
    W=copy.deepcopy(W0);P=copy.deepcopy(P0)
    W['naqsh'].update(mul=x['naqsh_mul'],sway=9,rof=340);W['fard'].update(rof=250,reload=x['fard_rl'])
    W['shotgun'].update(rof=700,reload=x['shot_rl'],pB=(x['shot_pb'],x['shot_pb']+2),pH=(x['shot_pb']+5,x['shot_pb']+7))
    W['fitil'].update(mul=x['fitil_mul'],reload=x['fitil_rl'])
    P['a_light']['m']={'reload':x['light_rl']};P['a_light']['add']={'ammo':-1}
    P['a_wide']['m']={};P['a_wide']['add']={'ammo':1,'draw':x['wide_draw']}
    P['a_coarse']['m']={'spread':.75,'pdm':x['coarse_pdm']};P['a_soft']['m']={'spread':1.1,'pdm':x['soft_pdm']}
    P['b_long']['m']={'spread':.9,'sway':1.2};P['b_short']['m']={'sway':.75,'spread':1.1}
    P['g_sidr']['m']={'sway':.8};P['g_sidr']['add']={'draw':x['sidr_draw']};P['g_bone']['m']={'sway':1.2};P['g_bone']['add']={'draw':x['bone_draw']}
    P['a_fuse']['m']={'fuse':x['fuse_f'],'sway':1.35};P['a_powder']['m']={'reload':x['powder_rl'],'fuse':1.2}
    globals()['W']=W;globals()['P']=P
def score(x,N=30,seed=1):
    apply(x);rng2=np.random.default_rng(seed);globals()['rng']=rng2
    L=loadouts();ST=[stat(w,p) for w,p in L];SM=[shot_samples(g) for g in ST]
    wr=[np.mean([duel(ST[i],ST[j],SM[i],SM[j],N) for j in range(len(L))]) for i in range(len(L))]
    wa={w:np.mean([wr[i] for i,(ww,_) in enumerate(L) if ww==w]) for w in W}
    return max(abs(np.array(wr)-.5)),wr,L,wa
best=score(X);print('start',round(best[0],3),flush=True)
rs=np.random.default_rng(3);t0=time.time()
while time.time()-t0<500:
    y=dict(X)
    for k in rs.choice(list(X),size=3,replace=False): y[k]=float(round(y[k]+float(rs.choice([-1,1]))*STEP[k],3))
    s=score(y)
    if s[0]<best[0]: X=y;best=s;print('better',round(s[0],3),json.dumps(X),flush=True)
json.dump(X,open('best_x.json','w'))
s=score(X,N=120,seed=9);print('final max dev',round(s[0],3));print({k:round(v,3) for k,v in s[3].items()})
o=sorted(zip(s[1],s[2]),key=lambda z:-z[0]);print(o[:4]);print(o[-4:]);print(X)
