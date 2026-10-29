"""Held-out block test of a directional keyboard model (suggested by the independent audit of 2026-10-29).

Protocol, fixed before looking at blocks 2-3:
  * Train every model on block 1 only (11 lines, 187 letters). Freeze all parameters.
  * Evaluate on blocks 2-3 (22 lines). Line starts are scored with the unigram model in all
    "reset" variants; cross-line transitions are excluded.
  * Models:
      U   unigram letter frequencies
      B   letter bigram model, add-0.5 smoothing (650 free parameters)
      K0  keyboard model: P(step class) x uniform choice among keys in that class (no memory of direction)
      K1  directional keyboard model: P(step class | previous step class) x uniform choice in class
    Step classes on QWERTZ (row offsets 0 / 0.25 / 0.75): same key, left, right, up-left, up-right,
    down-left, down-right (neighbour = distance <= 1.3), and jump (any non-neighbour, chosen in
    proportion to unigram frequency).
  * Report held-out bits per letter; simulate 2000 texts from frozen K1 with the line lengths of
    blocks 2-3 and compare adjacency, aba patterns, directional run lengths, IC and repeated trigrams.
  * Secondary: the same with each block held out in turn (3-fold).
Standard library only. Seed 20261029.
"""
import math, random, collections, re, pathlib, argparse, itertools

ap = argparse.ArgumentParser()
ap.add_argument("--data", default=str(pathlib.Path(__file__).resolve().parent.parent / "data" / "ciphertext.txt"))
ap.add_argument("--out", default=None)
args = ap.parse_args()

def load(path):
    blocks = []; cur = None
    for raw in open(path, encoding="utf-8"):
        raw = raw.strip()
        if not raw: continue
        if raw.startswith("#"):
            cur = [] if "Block" in raw else None
            if cur is not None: blocks.append(cur)
            continue
        if cur is not None:
            cur.append(re.sub(r"\[(\w)\|(\w)\]", r"\1", raw).replace(" ", ""))
    return blocks

BLOCKS = load(args.data)
A = "abcdefghijklmnopqrstuvwxyz"
rows = ["qwertzuiop", "asdfghjkl", "yxcvbnm"]; off = [0, .25, .75]
POS = {c: (r, k + off[r]) for r, row in enumerate(rows) for k, c in enumerate(row)}
KEYS = [c for c in A if c in POS]          # 'q' is on the keyboard; all 26 letters are
CLASSES = ["same", "L", "R", "UL", "UR", "DL", "DR", "jump"]
NB = 1.3

def cls(a, b):
    if a == b: return "same"
    (r1, x1), (r2, x2) = POS[a], POS[b]
    if math.hypot(r1 - r2, x1 - x2) > NB: return "jump"
    if r1 == r2: return "R" if x2 > x1 else "L"
    v = "U" if r2 < r1 else "D"
    return v + ("R" if x2 > x1 else "L")

TARGETS = {a: {c: [b for b in KEYS if cls(a, b) == c] for c in CLASSES} for a in KEYS}

def unigram(lines, alpha=0.5):
    f = collections.Counter("".join(lines)); n = sum(f.values())
    return {c: (f[c] + alpha) / (n + alpha * 26) for c in A}

def jump_prob(a, b, U):
    tg = TARGETS[a]["jump"]; z = sum(U[x] for x in tg)
    return U[b] / z

class K:
    def __init__(self, lines, order, U, alpha=0.5):
        self.order, self.U = order, U
        cnt = collections.defaultdict(collections.Counter)
        for l in lines:
            prev = "start"
            for a, b in zip(l, l[1:]):
                c = cls(a, b)
                cnt[prev if order else "any"][c] += 1
                prev = c
        self.P = {}
        for ctx in ["start"] + CLASSES + ["any"]:
            row = cnt[ctx]; tot = sum(row.values())
            self.P[ctx] = {c: (row[c] + alpha) / (tot + alpha * len(CLASSES)) for c in CLASSES}
    def step(self, a, b, prev):
        ctx = prev if self.order else "any"
        avail = [c for c in CLASSES if TARGETS[a][c]]
        z = sum(self.P[ctx][c] for c in avail)
        c = cls(a, b)
        pc = self.P[ctx][c] / z
        pb = jump_prob(a, b, self.U) if c == "jump" else 1 / len(TARGETS[a][c])
        return pc * pb, c
    def sample_line(self, n, rng):
        a = rng.choices(A, weights=[self.U[c] for c in A])[0]; s = [a]; prev = "start"
        ctx = lambda p: p if self.order else "any"
        while len(s) < n:
            avail = [c for c in CLASSES if TARGETS[a][c]]
            c = rng.choices(avail, weights=[self.P[ctx(prev)][x] for x in avail])[0]
            tg = TARGETS[a][c]
            b = rng.choices(tg, weights=[self.U[x] for x in tg])[0] if c == "jump" else rng.choice(tg)
            s.append(b); a, prev = b, c
        return "".join(s)

def bits(lines, model, U, B=None):
    tot = 0.0; n = 0
    for l in lines:
        tot -= math.log2(U[l[0]]); n += 1
        prev = "start"
        for a, b in zip(l, l[1:]):
            if model == "U": p = U[b]
            elif model == "B": p = B[a][b]
            else: p, prev = model.step(a, b, prev)
            tot -= math.log2(p); n += 1
    return tot / n

def bigram(lines, alpha=0.5):
    c = collections.defaultdict(collections.Counter)
    for l in lines:
        for a, b in zip(l, l[1:]): c[a][b] += 1
    return {a: {b: (c[a][b] + alpha) / (sum(c[a].values()) + 26 * alpha) for b in A} for a in A}

def stats(lines):
    adj = aba = 0; npairs = 0; runs = []
    for l in lines:
        r = 1
        for i in range(len(l) - 1):
            npairs += 1
            (r1, x1), (r2, x2) = POS[l[i]], POS[l[i + 1]]
            adj += math.hypot(r1 - r2, x1 - x2) <= 1.1
            if i + 2 < len(l): aba += l[i] == l[i + 2]
        # directional runs: consecutive horizontal steps in the same direction
        cs = [cls(a, b) for a, b in zip(l, l[1:])]
        cur = None; k = 0
        for c in cs + [None]:
            if c in ("L", "R") and c == cur: k += 1
            else:
                if cur in ("L", "R"): runs.append(k)
                cur, k = c, 1
    t = "".join(lines); f = collections.Counter(t); n = len(t)
    ic = sum(v * (v - 1) for v in f.values()) / (n * (n - 1))
    tri = collections.Counter(t[i:i + 3] for i in range(n - 2)); rep3 = sum(v - 1 for v in tri.values() if v > 1)
    persist = sum(1 for l in lines for a, b, c in zip(l, l[1:], l[2:]) if cls(a, b) == cls(b, c) and cls(a, b) not in ("same", "jump"))
    return {"adjacent": adj / npairs, "aba": aba, "mean_LR_run": sum(runs) / max(1, len(runs)),
            "same_direction_steps": persist, "IC": ic, "rep3": rep3}

out = []
rng = random.Random(20261029)
def experiment(train, test, label, simulate):
    U = unigram(train); Bm = bigram(train); k0 = K(train, 0, U); k1 = K(train, 1, U)
    res = {m: bits(test, mod, U, Bm) for m, mod in [("U", "U"), ("B", "B"), ("K0", k0), ("K1", k1)]}
    out.append(f"{label}: held-out bits/letter  U={res['U']:.3f}  B={res['B']:.3f}  K0={res['K0']:.3f}  K1={res['K1']:.3f}"
               f"   (uniform = {math.log2(26):.3f})")
    if simulate:
        out.append("\nFrozen K1 parameters P(step | previous step), trained on block 1:")
        out.append("  prev\\next " + " ".join(f"{c:>6s}" for c in CLASSES))
        for ctx in ["start"] + CLASSES:
            out.append(f"  {ctx:9s} " + " ".join(f"{k1.P[ctx][c]:6.3f}" for c in CLASSES))
        obs = stats(test)
        sims = {m: [stats([mod.sample_line(len(l), rng) for l in test]) for _ in range(2000)] for m, mod in [("K0", k0), ("K1", k1)]}
        out.append("\nObserved blocks 2-3 vs 2000 simulations from the frozen models (mean, 95 % range, observed percentile):")
        for key in obs:
            line = f"  {key:22s} observed={obs[key]:8.3f}"
            for m in ("K0", "K1"):
                v = sorted(s[key] for s in sims[m]); mean = sum(v) / len(v)
                pct = sum(x < obs[key] for x in v) / len(v) * 100 + sum(x == obs[key] for x in v) / len(v) * 50
                line += f"   {m}: {mean:7.3f} [{v[50]:.3f}, {v[1949]:.3f}] pct={pct:5.1f}"
            out.append(line)
    return res

out.append("Held-out block test of a directional keyboard model")
out.append("=" * 52)
out.append(f"Block sizes (letters): " + ", ".join(str(len("".join(b))) for b in BLOCKS))
experiment(BLOCKS[0], BLOCKS[1] + BLOCKS[2], "PRIMARY  train block 1 -> test blocks 2-3", True)
out.append("\nSecondary 3-fold check (train on two blocks, test on the third):")
for i in range(3):
    tr = [l for j, b in enumerate(BLOCKS) if j != i for l in b]
    experiment(tr, BLOCKS[i], f"  test block {i+1}", False)
# Residual check: are the repeated trigrams (which the models under-predict) themselves keyboard strokes?
test = BLOCKS[1] + BLOCKS[2]
t = [l[i:i+3] for l in test for i in range(len(l) - 2)]
cnt = collections.Counter(t)
stroke = lambda g: cls(g[0], g[1]) not in ("jump",) and cls(g[1], g[2]) not in ("jump",)
rep_occ = [g for g in t if cnt[g] > 1]
out.append("\nResidual check on blocks 2-3 (trigrams within lines):")
out.append(f"  all trigram positions that are two neighbour steps: {sum(map(stroke, t))}/{len(t)} = {sum(map(stroke, t))/len(t):.2f}")
out.append(f"  occurrences of repeated trigrams that are two neighbour steps: {sum(map(stroke, rep_occ))}/{len(rep_occ)} = {sum(map(stroke, rep_occ))/len(rep_occ):.2f}")
out.append("  most repeated: " + " ".join(f"{g}x{v}" for g, v in cnt.most_common(12)))
res = "\n".join(out); print(res)
if args.out: open(args.out, "w", encoding="utf-8").write(res + "\n")
