"""Independent audit, Python 3 + numpy + scipy. Seed 20261029.
Input frozen from repo main commit 1eac5795a712322331e76ba1b82f71291cf1ea48.
No fitted language/key search is used. Nulls are explicitly conditional models.
"""
import re, json, itertools, hashlib
from pathlib import Path
import numpy as np
from scipy.stats import chi2, beta

ROOT=Path(__file__).resolve().parent
raw=(ROOT/'data/ciphertext.txt').read_text()
rawlines=[s for s in raw.splitlines() if s and not s.startswith('#')]
lines=[re.sub(r'\[(\w)\|(\w)\]',r'\1',s) for s in rawlines]
enc=lambda s: np.array([ord(c)-97 for c in s],dtype=np.int16)
parsed_lines=lines[:]
# Photograph: final 'eet hgfmuzzaa' occupies one physical line, not two.
lines=lines[:33]+[''.join(lines[33:])]
ls=list(map(enc,lines)); t=np.concatenate(ls); n=len(t)
freq=np.bincount(t,minlength=26)
rng=np.random.default_rng(20261029)
R={'input_sha256':hashlib.sha256(raw.encode()).hexdigest(),'n':n,'line_lengths':list(map(len,lines)), 'seed':20261029}
def graph(layout='qwertz',threshold=1.1,repeat=True,horizontal=False):
    rows=['qwertzuiop','asdfghjkl','yxcvbnm'] if layout=='qwertz' else ['qwertyuiop','asdfghjkl','zxcvbnm']
    pos=np.zeros((26,2))
    for j,row in enumerate(rows):
        for k,c in enumerate(row): pos[ord(c)-97]=(k+[0,.25,.75][j],j)
    d=np.sqrt(((pos[:,None]-pos[None,:])**2).sum(axis=2))
    a=(d<=threshold)
    if horizontal:a &= (pos[:,1,None]==pos[None,:,1])
    if not repeat:np.fill_diagonal(a,False)
    return a.astype(np.int16)
def summary(v,obs,tail='high'):
    k=int(np.sum(v>=obs) if tail=='high' else np.sum(v<=obs))
    return {'observed':float(obs),'null_mean':float(v.mean()),'null_sd':float(v.std()),'z_descriptive':float((obs-v.mean())/v.std()),'exceedances':k,'B':len(v),'p_MC_plus1':(k+1)/(len(v)+1),'p_upper95_if_zero':float(beta.ppf(.95,1,len(v))) if k==0 else None}
A=graph(); within=np.concatenate([A[x[:-1],x[1:]] for x in ls]); cross=A[np.array([x[-1] for x in ls[:-1]]),np.array([x[0] for x in ls[1:]])]
R['counts']={'all_adj':int(A[t[:-1],t[1:]].sum()),'all_pairs':n-1,'within_adj':int(within.sum()),'within_pairs':len(within),'cross_adj':int(cross.sum()),'cross_pairs':len(cross),'same_key_pairs':int((t[:-1]==t[1:]).sum())}
R['IC']=float((freq*(freq-1)).sum()/(n*(n-1)))
R['uniform_chi2']={'stat':float(((freq-n/26)**2/(n/26)).sum()),'df':25}
R['uniform_chi2']['p']=float(chi2.sf(R['uniform_chi2']['stat'],25))
graphs={'original':A,'distinct_only':graph(repeat=False),'horizontal_distinct':graph(repeat=False,horizontal=True),'radius1.3_distinct':graph(threshold=1.3,repeat=False),'radius1.5_distinct':graph(threshold=1.5,repeat=False),'qwerty_original':graph(layout='qwerty')}
B=100000; nulls={k:[] for k in graphs}; perline=[]; labelnull=[]; cutnull=[]
bg=np.zeros((26,26),dtype=np.int32); np.add.at(bg,(t[:-1],t[1:]),1)
for start in range(0,B,1000):
    b=min(1000,B-start)
    sh=rng.permuted(np.tile(t,(b,1)),axis=1)
    for k,g in graphs.items():nulls[k].extend(g[sh[:,:-1],sh[:,1:]].sum(axis=1).tolist())
    w=np.zeros(b,dtype=int)
    for x in ls:
        q=rng.permuted(np.tile(x,(b,1)),axis=1)
        w+=A[q[:,:-1],q[:,1:]].sum(axis=1)
    perline.extend(w.tolist())
    # Relabel all 26 letters to randomly chosen keyboard locations, preserving every ngram.
    maps=rng.permuted(np.tile(np.arange(26),(b,1)),axis=1)
    labelnull.extend((A[maps[:,:,None],maps[:,None,:]]*bg[None,:,:]).sum(axis=(1,2)).tolist())
    # Each typed line is viewed as a cycle; choose an independent cut in each cycle.
    # Tests unusual ends conditional on cycles, NOT a generic cipher null.
    starts=[]; ends=[]; kept=np.zeros(b,dtype=int)
    for x in ls:
        cuts=rng.integers(len(x),size=b)
        starts.append(x[cuts]); ends.append(x[(cuts-1)%len(x)])
        cyc=A[x,np.roll(x,-1)].sum()
        kept+=cyc-A[x[(cuts-1)%len(x)],x[cuts]]
    starts=np.array(starts).T;ends=np.array(ends).T
    cr=A[ends[:,:-1],starts[:,1:]].sum(axis=1)
    cutnull.extend((kept/len(within)-cr/len(cross)).tolist())
R['geometry']={k:summary(np.array(nulls[k]),int(g[t[:-1],t[1:]].sum())) for k,g in graphs.items()}
R['line_conditioned_shuffle']=summary(np.array(perline),int(within.sum()))
R['random_label_layout']=summary(np.array(labelnull),int(A[t[:-1],t[1:]].sum()))
R['random_circular_line_cuts']=summary(np.array(cutnull),float(within.mean()-cross.mean()))
# Exact common phase shift: preserve the entire stream and shift boundary mask.
# This null assumes a stationary stream with arbitrary display-line phase.
ends=np.cumsum([len(x) for x in ls])[:-1]-1
cyclic=A[t,np.roll(t,-1)]
phase_counts=np.array([cyclic[(ends+j)%n].sum() for j in range(n)])
R['boundary_common_phase']={'observed':int(cross.sum()),'phase_mean':float(phase_counts.mean()),'phase_count_le_observed':int((phase_counts<=cross.sum()).sum()),'phases':n,'exact_fraction_le':float((phase_counts<=cross.sum()).mean())}
main=ls[:33];mt=np.concatenate(main);me=np.cumsum([len(x) for x in main])[:-1]-1
mc=A[mt,np.roll(mt,-1)];obs=int(mc[me].sum())
pv=np.array([mc[(me+j)%len(mt)].sum() for j in range(len(mt))])
R['boundary_main33_phase']={'observed':obs,'pairs':len(me),'phase_mean':float(pv.mean()),'phase_count_le_observed':int((pv<=obs).sum()),'phases':len(mt),'exact_fraction_le':float((pv<=obs).mean())}
# Exact permutation expectation, sampling without replacement.
R['exact_null_adjacency']=float((freq[:,None]*freq[None,:]*A).sum()-np.dot(freq,np.diag(A)))/(n*(n-1))
variants=[]
for choices in itertools.product((0,1),repeat=4):
    ci=iter(choices)
    vv=[re.sub(r'\[(\w)\|(\w)\]',lambda m:m.group(next(ci)+1),s) for s in rawlines]
    x=enc(''.join(vv));f=np.bincount(x,minlength=26)
    variants.append({'choices':choices,'adj_count':int(A[x[:-1],x[1:]].sum()),'IC':float((f*(f-1)).sum()/(n*(n-1)))})
R['all_16_glyph_variants']=variants
# Periodic column IC: original order and interleaved visual rows, without final split effect.
interleaved=[lines[j*11+i] for i in range(11) for j in range(3)]+lines[33:]
orders={'block':t,'interleaved':enc(''.join(interleaved))}
def pic(x,p):
    x=np.atleast_2d(x);z=np.zeros(len(x))
    for j in range(p):
        col=x[:,j::p]; counts=(col[:,:,None]==np.arange(26)).sum(axis=1)
        z+=(counts*(counts-1)).sum(axis=1)/(col.shape[1]*(col.shape[1]-1))
    return z/p
P=10000
pn=[]
for start in range(0,P,200):
    sh=rng.permuted(np.tile(t,(min(200,P-start),1)),axis=1)
    pn.append(np.column_stack([pic(sh,p) for p in range(2,18)]))
pn=np.concatenate(pn);mu=pn.mean(axis=0);sd=pn.std(axis=0)
maxz=((pn-mu)/sd).max(axis=1)
R['periods']={}
for name,x in orders.items():
    obs=np.array([pic(x,p)[0] for p in range(2,18)])
    R['periods'][name]={'periods':list(range(2,18)),'ICs':obs.tolist(),'max_standardized_IC_test':summary(maxz,float(((obs-mu)/sd).max())),'all_adj':int(A[x[:-1],x[1:]].sum())}
# Potential artifact: excluded q and duplicates are explicit, no alphabet renormalization.
(ROOT/'audit_results.json').write_text(json.dumps(R,indent=2)+'\n')
print(json.dumps(R,indent=2))
