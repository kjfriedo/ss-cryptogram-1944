An independent audit of my analysis reproduced all the core numbers, but it also caught overstatements in my earlier comments. I'd like to correct them here:

1. **"Flat letter frequencies, IC close to random"** was wrong. The IC of 0.049 lies between random text (0.038) and German (≈ 0.076), and the frequencies are clearly not uniform. The text is not plain German, but it isn't random either.
2. **"No substitution can produce this"** is too strong. A substitution key deliberately designed around the keyboard could do it. However, giving the 26 letters random key positions never reproduces the real QWERTZ score (0 of 100,000 trials), so such a key would itself have to be a keyboard-based construction.
3. **The periodicity test does not exclude Vigenère-type ciphers in general.** It only shows no simple periodic key of up to 17 letters in the assumed reading order. Autokey or running keys, a key that resets every line, or a prior transposition remain untested.
4. In my comment on the number part, **"a code would give roughly equal digits"** also overstates it. An additive cipher with random key digits would, but a codebook can avoid zeros. Codes do not, however, explain the long ±1 runs.

One new test supports the keyboard explanation. A small keyboard-step model trained on block 1 alone predicts the unseen blocks 2–3 better than a letter-bigram model trained on the same data: 3.68 against 4.11 bits per letter. What the model misses consists of the same short key strokes typed again and again (*xys, red, cxy, tre*). It does not look like language.

So my position is now this: a sequence typed by moving over a QWERTZ keyboard is the most economical explanation, and an ordinary cipher of German text is unlikely. The statistics cannot tell us what the document was for. Carelessly typed key material is a real alternative to filler or a typing exercise. Only the original and its archival context can decide.

Updated analysis: https://github.com/kjfriedo/ss-cryptogram-1944

Jozef Krajčovič
