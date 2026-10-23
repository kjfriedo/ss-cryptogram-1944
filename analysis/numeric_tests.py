import random, math, collections
random.seed(2)
TOP=['56543487899729654567467895453327','85847334927535622768936487783252']
B1=['II86543543434','834I9II434229','65674I34II545','456387II9924I','2626547II47II','545457II7II62','6II8656451922','6547I98II3367','II5678537I133',
    '7898765II54576568','76II989658II32844','88I9I4354622II266','5643876II53II2983']
B2=['843686II964I2','354678965432I','87II453792388','654396II767II','5I6543367I7II','I876543456567','98987873I6II3','547652II8II8654','7564I332I8784',
    '654365343879II86I','II436576936I543I4','98789895II45343II87','23II8657434III432']
B3=['8765439I','II956436','87654II5','II546532','545222I9','5456I3II','I8765893','54643I8I','76567878',
    '6565467I','23232589','67565477','65742II9']
B1=[l.replace('1','I') for l in B1]  # the typewriter has no '1'; every one is a capital I
LINES=TOP+B1+B2+B3
for l in LINES: assert set(l)<=set('23456789I0'),l
D='I234567890'
# key geometry: number row x positions 2..9,0 ; I on QWERTZ upper letter row
NUMX={str(d):i for i,d in enumerate('1234567890')}  # '1' at x=0
def pos(c,mode):
    if c=='I':
        return (0,0.0) if mode=='digit1' else (1,7.25)   # key i: upper row, between 8 and 9 (+0.25 stagger)
    return (0,float(NUMX[c]))
def dist(a,b,mode): (r1,x1),(r2,x2)=pos(a,mode),pos(b,mode); return math.hypot(r1-r2,x1-x2)
def pairs(lines): return [(l[i],l[i+1]) for l in lines for i in range(len(l)-1)]
def adj_rate(lines,mode): P=pairs(lines); return sum(dist(a,b,mode)<=1.1 for a,b in P)/len(P)
def mean_d(lines,mode): P=pairs(lines); return sum(dist(a,b,mode) for a,b in P)/len(P)
def step1(lines): # numeric |Δ|==1 with I as 1
    v=lambda c:1 if c=='I' else int(c)
    P=pairs(lines); return sum(abs(v(a)-v(b))==1 for a,b in P)/len(P)
def runs3(lines): # monotonic runs of length>=4 with step ±1 (I=1)
    v=lambda c:1 if c=='I' else int(c); n=0
    for l in lines:
        x=[v(c) for c in l]
        for i in range(len(x)-3):
            d=[x[i+k+1]-x[i+k] for k in range(3)]
            if all(e==1 for e in d) or all(e==-1 for e in d): n+=1
    return n
def shuffle_lines(lines):
    s=list(''.join(lines)); random.shuffle(s); out=[];i=0
    for l in lines: out.append(''.join(s[i:i+len(l)])); i+=len(l)
    return out
def perm(f,N=3000):
    obs=f(LINES); vals=[f(shuffle_lines(LINES)) for _ in range(N)]
    m=sum(vals)/N; sd=(sum((x-m)**2 for x in vals)/N)**.5
    p=(sum(x>=obs for x in vals)+1)/(N+1); return obs,m,sd,(obs-m)/sd,p
S=''.join(LINES); n=len(S); f=collections.Counter(S)
out=[]
out.append(f"Digits: {n} in {len(LINES)} lines; '0' occurs {f.get('0',0)} times")
out.append("Frequencies: "+' '.join(f"{d}:{f.get(d,0)}" for d in D))
chi=sum((f.get(d,0)-n/10)**2/(n/10) for d in D); ic=sum(v*(v-1) for v in f.values())/(n*(n-1))
out.append(f"Chi2 vs uniform over 10 digits (df=9): {chi:.1f}   IC={ic:.4f} (uniform 0.100)")
out.append("\nPermutation tests (3000 shuffles of the same digits, line lengths kept):")
for name,fn in [("adjacent keys, I = key 'i' (under 8/9)",lambda L:adj_rate(L,'ikey')),
                ("adjacent keys, I = digit 1",lambda L:adj_rate(L,'digit1')),
                ("-mean key distance, I = key 'i'",lambda L:-mean_d(L,'ikey')),
                ("numeric step |d|=1 (I=1)",step1),
                ("runs of 4 consecutive +-1 steps",runs3)]:
    o,m,sd,z,p=perm(fn); out.append(f"  {name:42s} obs={o:7.3f} null={m:7.3f}±{sd:6.3f} z={z:6.2f} p={p:.4f}")
# line breaks
def cross(mode):
    c=[(a[-1],b[0]) for a,b in zip(LINES,LINES[1:])]; return sum(dist(a,b,mode)<=1.1 for a,b in c),len(c)
a,b=cross('ikey'); out.append(f"\nAdjacent across line ends (I=key i): {a}/{b} = {a/b:.2f}  vs within lines {adj_rate(LINES,'ikey'):.2f}")
# what follows/precedes I
nb=collections.Counter()
for x,y in pairs(LINES):
    if x=='I' and y!='I': nb[y]+=1
    if y=='I' and x!='I': nb[x]+=1
out.append("Neighbours of I (excluding I): "+' '.join(f"{d}:{nb[d]}" for d in '234567890'))
exp={d:f[d] for d in '234567890'}; tot=sum(exp.values())
out.append("  expected share if random:     "+' '.join(f"{d}:{sum(nb.values())*exp[d]/tot:.1f}" for d in '234567890'))
out.append("Doubled I ('II') count: "+str(sum(l.count('II') for l in LINES)))
out.append("\nPer-part adjacency (I=key i): "+', '.join(f"{nm} {adj_rate(L,'ikey'):.2f}" for nm,L in [('top',TOP),('block1',B1),('block2',B2),('block3',B3)]))
res='\n'.join(out); print(res)
open(__import__('pathlib').Path(__file__).resolve().parent.parent/'results'/'numeric_test_results.txt','w').write(res+'\n')
