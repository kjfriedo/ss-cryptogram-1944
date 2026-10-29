import random, math, zlib, bz2, collections, itertools
random.seed(1)
import argparse, re, pathlib
ap=argparse.ArgumentParser(description="Randomness tests on the SS cryptogram transcription")
ap.add_argument("--data",default=str(pathlib.Path(__file__).resolve().parent.parent/"data"/"ciphertext.txt"))
ap.add_argument("--alt",action="store_true",help="use the second reading of uncertain glyphs ([i|f] -> f)")
ap.add_argument("--out",default=None,help="write results to this file")
args=ap.parse_args()
def load(path,alt):
    lines=[];blocks=[];cur=None
    for raw in open(path,encoding="utf-8"):
        raw=raw.strip()
        if not raw: continue
        if raw.startswith("#"):
            if "Block" in raw: cur=[]; blocks.append(cur)
            elif "Final" in raw: cur=None
            continue
        l=re.sub(r"\[(\w)\|(\w)\]",lambda m:m.group(2 if alt else 1),raw).replace(' ','')
        lines.append(l)
        if cur is not None: cur.append(l)
    return lines,blocks
LINES,(B1,B2,B3)=load(args.data,args.alt)
CT=''.join(LINES)

GER=("""Der Reichsfuehrer hat angeordnet dass die Kunstgegenstaende und Wertsachen aus den gefaehrdeten Gebieten
unverzueglich in die vorbereiteten Stollen in Niederschlesien zu verbringen sind. Die Transporte werden von
zuverlaessigen Maennern der Schutzstaffel begleitet und duerfen keinesfalls ohne schriftlichen Befehl geoeffnet werden.
Ueber die genaue Lage der Verstecke ist strengstes Stillschweigen zu bewahren. Die Listen der eingelagerten Gegenstaende
sind in doppelter Ausfertigung anzulegen und eine Abschrift ist umgehend an das Hauptamt nach Berlin zu senden. Die
Zufahrtswege sind nach Abschluss der Arbeiten zu sprengen und unkenntlich zu machen. Saemtliche beteiligten Arbeitskraefte
sind ueber den Zweck der Arbeiten nicht zu unterrichten. Fuer die Durchfuehrung ist der oertliche Fuehrer persoenlich
verantwortlich. Meldung ueber den Vollzug hat bis spaetestens Ende des Monats zu erfolgen. Weitere Weisungen folgen
durch Kurier. Die Bewachung der Anlagen uebernimmt bis auf weiteres eine Kompanie des Wachbataillons."""
).lower()
GER=''.join(c for c in GER if c.isalpha())[:len(CT)]
KEY='nibelungen'
VIG=''.join(chr((ord(c)-97+ord(KEY[i%len(KEY)])-97)%26+97) for i,c in enumerate(GER))

rows=["qwertzuiop","asdfghjkl","yxcvbnm"]
off=[0,0.25,0.75]; pos={}
for r,row in enumerate(rows):
    for c,ch in enumerate(row): pos[ch]=(r,c+off[r])
def kdist(a,b):
    (r1,c1),(r2,c2)=pos[a],pos[b]; return math.hypot(r1-r2,c1-c2)
LEFT=set("qwertasdfgyxcvb")
A="abcdefghijklmnopqrstuvwxyz"

def mono(t):
    n=len(t); f=collections.Counter(t)
    exp=n/26; chi=sum((f.get(c,0)-exp)**2/exp for c in A)
    ic=sum(v*(v-1) for v in f.values())/(n*(n-1))
    H=-sum(v/n*math.log2(v/n) for v in f.values())
    return chi,ic,H,len(f)
def bigrams(t): return [t[i:i+2] for i in range(len(t)-1)]
def mi(t):
    bg=collections.Counter(bigrams(t)); n=sum(bg.values())
    l=collections.Counter(t[:-1]); r=collections.Counter(t[1:])
    return sum(v/n*math.log2((v/n)/((l[a]/n)*(r[b]/n))) for (a,b),v in ((k,v) for k,v in ((tuple(k),v) for k,v in bg.items())))
def adj(t): return sum(kdist(t[i],t[i+1])<=1.1 for i in range(len(t)-1))/(len(t)-1)
def meand(t): return sum(kdist(t[i],t[i+1]) for i in range(len(t)-1))/(len(t)-1)
def doubles(t): return sum(t[i]==t[i+1] for i in range(len(t)-1))
def handruns(t):
    s=[c in LEFT for c in t]; n1=sum(s); n2=len(s)-n1
    runs=1+sum(s[i]!=s[i-1] for i in range(1,len(s)))
    mu=2*n1*n2/(n1+n2)+1; var=(mu-1)*(mu-2)/(n1+n2-1)
    return n1/len(s),runs,(runs-mu)/math.sqrt(var)
def kappa(t,k): return sum(t[i]==t[i+k] for i in range(len(t)-k))/(len(t)-k)
def repeats(t,n):
    c=collections.Counter(t[i:i+n] for i in range(len(t)-n+1)); return sum(v-1 for v in c.values() if v>1)
def comp(t): return len(bz2.compress(t.encode()))/len(t), len(zlib.compress(t.encode(),9))/len(t)
def pal(t): # back-and-forth: a b a patterns
    return sum(t[i]==t[i+2] for i in range(len(t)-2))
def apen(t,m=2):
    def phi(m):
        c=collections.Counter(t[i:i+m] for i in range(len(t)-m+1)); N=len(t)-m+1
        return sum(v/N*math.log(v/N) for v in c.values())
    return phi(m)-phi(m+1)

def stats(t):
    chi,ic,H,k=mono(t); lf,runs,z=handruns(t)
    return dict(chi2_uniform=chi,IC=ic,entropy=H,alphabet=k,MI_digram=mi(t),adjacent_keys=adj(t),
                key_distance=meand(t),doubles=doubles(t),aba=pal(t),left_hand=lf,runs_z=z,
                rep3=repeats(t,3),rep4=repeats(t,4),bz2=comp(t)[0],ApEn2=apen(t))

def perm_p(t,f,N=2000):
    obs=f(t); L=list(t); ge=0; vals=[]
    for _ in range(N):
        random.shuffle(L); v=f(''.join(L)); vals.append(v); ge+= v>=obs
    m=sum(vals)/N; sd=(sum((x-m)**2 for x in vals)/N)**.5
    return obs,m,sd,(obs-m)/sd if sd else 0,(ge+1)/(N+1)

texts={'cryptogram':CT,'german':GER,'vigenere':VIG}
out=[]
out.append(f"Length: {len(CT)}")
names=list(stats(CT).keys())
out.append("{:16s}".format('metric')+''.join(f"{k:>12s}" for k in texts))
S={k:stats(v) for k,v in texts.items()}
# shuffled baseline averaged
sh=[stats(''.join(random.sample(CT,len(CT)))) for _ in range(300)]
for n in names:
    out.append(f"{n:16s}"+''.join(f"{S[k][n]:12.3f}" for k in texts)+f"   shuffled={sum(s[n] for s in sh)/len(sh):.3f}")

out.append("\nPermutation tests (2000 shuffles of the same letters), z-score and one-sided p-value (greater):")
for nm,f in [('adjacent_keys',adj),('-key_distance',lambda t:-meand(t)),('MI_digram',mi),('aba',pal),('rep3',lambda t:repeats(t,3)),('rep4',lambda t:repeats(t,4)),('-bz2',lambda t:-comp(t)[0])]:
    # ApEn is reported descriptively only: on 575 letters its 2-/3-gram estimates are too sparse to test.
    o,m,sd,z,p=perm_p(CT,f)
    out.append(f"  {nm:16s} obs={o:8.3f} null={m:8.3f}±{sd:6.3f} z={z:7.2f} p={p:.4f}")

out.append("\nKappa (coincidences at shift k); expected for random text = sum p_i^2:")
_,ic,_,_=mono(CT)
out.append("  "+' '.join(f"{k}:{kappa(CT,k):.3f}" for k in range(1,21))+f"   ref={sum((v/len(CT))**2 for v in collections.Counter(CT).values()):.3f}")

# periodic IC
def per_ic(t,p):
    return sum(mono(t[i::p])[1] for i in range(p))/p
out.append("\nMean column IC at period p (detects only simple periodic keys up to p=17 in this reading order):")
out.append("  "+' '.join(f"{p}:{per_ic(CT,p):.3f}" for p in range(1,18)))

# top bigrams/trigrams
bg=collections.Counter(bigrams(CT)).most_common(15)
out.append("\nMost frequent bigrams: "+' '.join(f"{a}{v}" for a,v in bg))
tg=collections.Counter(CT[i:i+3] for i in range(len(CT)-2)).most_common(15)
out.append("Most frequent trigrams: "+' '.join(f"{a}{v}" for a,v in tg))
out.append("Frequencies: "+' '.join(f"{a}{v}" for a,v in collections.Counter(CT).most_common()))

# keyboard random-walk model
def walk(n):
    keys=list(pos); s=[random.choice(keys)]
    while len(s)<n:
        c=s[-1]
        if random.random()<0.68:
            nb=[k for k in keys if 0<kdist(c,k)<=1.1 and k in LEFT|set('zhujnmik')]
            s.append(random.choice(nb or keys))
        else: s.append(random.choice([k for k in keys if k in LEFT] if random.random()<.6 else keys))
    return ''.join(s)
W=[stats(walk(len(CT))) for _ in range(200)]
out.append("\nNaive random-walk model (68 % step to a random adjacent key), mean of 200 runs.\nNOTE: this model does NOT fit (too many adjacent steps and aba patterns); see heldout_model.py for a directional model:")
for n in names: out.append(f"  {n:16s} model={sum(w[n] for w in W)/len(W):8.3f}   cryptogram={S['cryptogram'][n]:8.3f}")

# per-block consistency
out.append("\nConsistency by block (adjacent keys / IC / left hand):")
for nm,b in [('block1',''.join(B1)),('block2',''.join(B2)),('block3',''.join(B3))]:
    out.append(f"  {nm}: {adj(b):.3f} / {mono(b)[1]:.4f} / {handruns(b)[0]:.3f}")
# line-boundary transitions
cross=[(a[-1],b[0]) for a,b in zip(LINES,LINES[1:])]
out.append(f"Adjacent-key transitions across line ends: {sum(kdist(a,b)<=1.1 for a,b in cross)}/{len(cross)} (within lines {sum(sum(kdist(l[i],l[i+1])<=1.1 for i in range(len(l)-1)) for l in LINES)/sum(len(l)-1 for l in LINES):.2f})")
# common-phase boundary test: keep the whole stream, shift the line-end mask through all positions
cyc=[kdist(CT[i],CT[(i+1)%len(CT)])<=1.1 for i in range(len(CT))]
ends=list(itertools.accumulate(len(l) for l in LINES))[:-1]
ends=[e-1 for e in ends]
obs=sum(cyc[e] for e in ends)
ph=[sum(cyc[(e+j)%len(CT)] for e in ends) for j in range(len(CT))]
out.append(f"Common-phase test: {sum(x<=obs for x in ph)} of {len(CT)} shifts of the line-end mask give <= {obs} adjacent pairs (fraction {sum(x<=obs for x in ph)/len(CT):.4f}; mean {sum(ph)/len(ph):.1f})")
if args.out: open(args.out,'w',encoding='utf-8').write('\n'.join(out)+'\n')
print('\n'.join(out))
