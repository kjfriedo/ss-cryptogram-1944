# SS cryptogram (1944/45): transcription and randomness analysis

An analysis of both parts (letters and numbers) of the typed "SS cryptogram" published by Klaus Schmeh on 22 October 2026 in
[Who can decipher this message from World War II?](https://klausschmeh.net/who-can-decipher-this-message-from-world-war-ii/).
Bogusław Wróbel found the document in the archives of the Polish Military Mission in Berlin, and it is said to concern
the hiding of cultural assets in Lower Silesia.

## Conclusion

The letter sequence is strongly non-random, and its dependencies match the geometry of a German **QWERTZ**
keyboard very closely. A sequence produced by moving over the keyboard is currently the most economical
explanation. The statistics cannot determine the document's purpose, origin or date. They make an ordinary cipher
of German text unlikely, but they do not rule out every cipher or key function (see *Limitations* below).
Possible purposes include filler, a decoy, a typing exercise, or carelessly typed key material.

| Test (575 letters) | Cryptogram | Shuffled letters | German text |
|---|---|---|---|
| Adjacent-key pairs | 52 % (300/574) | 17 % (0 exceedances in 100,000) | 18 % |
| Mean key distance | 1.59 | 2.59 | 2.97 |
| Repeated trigrams | 132 | 18 | 190 |
| Index of coincidence | 0.049 | 0.049 (unchanged by shuffling) | 0.083 |
| Left/right-hand runs test | z = −11.6 | z ≈ 0 | z ≈ 0 |

- **Not German, not uniform.** The IC of 0.049 lies between uniform random text (0.038) and German (≈ 0.076).
  The frequencies are clearly not uniform (χ² = 181, 25 df). This rules out plain German and a simple
  substitution of it in the ordinary sense, but it is not evidence of randomness.
- **The geometry is specific.** Assigning the 26 letters to random key positions, while keeping every letter pair,
  never reaches the real QWERTZ score (0 of 100,000). The signal also survives excluding repeated keys, changing
  the distance threshold, and shuffling within each line. QWERTY fits too (43 %), but less well than QWERTZ.
- **The geometry generalizes across blocks.** A small keyboard-step model trained on block 1 alone predicts blocks
  2–3 at 3.68 bits per letter. A letter-bigram model trained on the same data needs 4.11, and frequencies alone
  need 4.55. See *Held-out block test* below.
- **No simple periodicity.** Mean column IC shows no excess for periods 2–17 in either reading order (calibrated
  p ≈ 0.22 block-wise, ≈ 0.10 interleaved). This rules out only simple periodic keys of up to 17 letters in these
  reading orders. It does not rule out autokey or running keys, keys that reset every line, or a prior
  transposition.
- **Line ends are special.** 54 % of steps within lines land on adjacent keys, but only 6 of 33 transitions across
  line ends do. Sliding the line-end positions along the continuous text, only 3 of 575 offsets give so few
  (fraction 0.005, or 0.018 without the final group). This links the pattern to the typed lines. That each line is
  a separate hand movement is an interpretation, not a proof.
- **Robust to the uncertain readings.** All 16 combinations of the four uncertain glyphs give 52.3–52.6 %
  adjacent keys.

## Held-out block test

Following the [independent audit](audit/2026-10-29/), a directional keyboard model was fitted to block 1 only, frozen, and evaluated
on blocks 2–3 (`analysis/heldout_model.py`, `results/heldout_model_results.txt`). Step classes are: same key,
the six neighbour directions, and a jump.

| Model (trained on block 1) | Held-out bits per letter, blocks 2–3 |
|---|---|
| Uniform over 26 letters | 4.70 |
| Letter frequencies (U) | 4.55 |
| Letter bigrams (B, 650 parameters) | 4.11 |
| Keyboard steps, no memory (K0) | 3.68 |
| Keyboard steps with direction memory (K1) | 3.68 |

- **Keyboard geometry predicts unseen blocks better than letter statistics**, with far fewer parameters.
- **Direction memory adds nothing measurable** in this simple form (K1 ≈ K0; mixed in the 3-fold check).
- **The frozen models under-predict the text's regularity.** Blocks 2–3 have more adjacent steps (58 % vs ≈ 43 %
  simulated), more same-direction steps (43 vs ≈ 24) and many more repeated trigrams (82 vs ≈ 22). The aba
  count fits K1.
- **The residue is itself made of keyboard strokes.** 95 % of repeated-trigram occurrences are two neighbour steps
  (*xys, red, cxy, tre, vcv, dcx, tzh*), against 59 % of all trigram positions. The surplus is stereotyped key
  sequences typed again and again, not language-like structure.
- Block 1 is less regular than blocks 2–3 (adjacency 46 % vs 57 %), which partly explains the under-prediction.

## Limitations and alternative explanations

An [independent audit (29 Oct 2026)](audit/2026-10-29/) reproduced all core numbers and pointed out overstatements in the first
version of this README. These have been corrected:

- **The frequencies are not flat.** "Flat frequencies, IC close to random" was wrong wording; see above.
- **A keyboard-designed substitution is possible in principle.** "No substitution can produce this" is too strong.
  A substitution key deliberately designed around the keyboard could place frequent pairs on neighbouring keys.
  No such key and no coherent plaintext are known for this document.
- **The periodicity tests have limited scope.** They do not exclude Vigenère-type ciphers in general (see above).
- **The naive random-walk model does not fit.** It gives about 73 % adjacency and 127 aba patterns against the
  observed 52 % and 31. It is kept in `randomness_tests.py` only for transparency.
- **The ApEn permutation test was oriented the wrong way.** It has been removed; ApEn is reported descriptively only.
- **The p-values are conditional.** They are Monte Carlo values under shuffling, which tests "the letter order
  carries no dependencies", not "this is not a cipher". The tests share bigrams, so their p-values must not be
  multiplied.
- **Several alternatives remain open:**
  - Keyboard-generated key material: badly made key sheets typed mechanically.
  - A homophonic or keyboard-direction cipher with a line reset.
  - Steganography in strokes or jumps.
  
  None has a documented procedure from the period or a compact key. Only the original document and its archival context can
  decide between them.

## Second part of the document: numbers (UHG. Yc. 002)

On 23 October 2026 Bogusław Wróbel sent Klaus Schmeh "the second part of this document". The accompanying
transcription is titled *Szyfr – górna część* (Polish for "cipher – upper part"). It is most likely the upper half
of the same page, whose lower half holds the letter text analysed above. Both images are cropped at the join:
the letter image shows remnants of text above it, and the number image is cut off at the bottom.

The upper part contains 542 typed digits in three blocks and a small "key table" (`Ya. I00`, digit pairs and the
letter pairs `FF ZT AA / RT RE IU`). It shows the same keyboard signature, this time on the typewriter's number row:

| Test (542 digits) | Document | Shuffled digits (3,000×) |
|---|---|---|
| Digit 0 | never occurs | expected ≈ 54 if uniform |
| Steps of ±1 (e.g. `8765`, `2323`) | 43 % | 19 % (z ≈ 15) |
| Runs of four consecutive ±1 steps | 25 | 0.8 (z ≈ 25) |
| Adjacent keys | 56 % | 32 % (z ≈ 12) |
| Adjacent keys across line ends | 28 % (11 of 40) | 32 % |

- The digits cluster in the middle of the row (4–6), and 0, at the far right, is absent.
- An additive cipher with random key digits would give near-uniform digits including 0. A codebook can avoid
  zeros, but it does not explain the long ±1 runs.
- As with the letters, steps across line ends are at chance level.
- The lower part of the second number column and the first four lines of the second letter column have the same
  unusual line lengths: 17, 17, 19 and 17 (Gerry Haynaly's observation). Adding or subtracting the digits from
  the letters gives random-looking text (IC 0.034–0.043). Pure keyboard digits also make a poor one-time pad.
  The shared layout fits both parts having been typed to the same template.
- The typewriter has no `1` key, so 1 is typed as a capital `I`. That fits a period machine and is not evidence of a forgery.

See `data/numeric_transcription.md`, `analysis/numeric_tests.py` and `results/numeric_test_results.txt`.

## Contents

| Path | Description |
|---|---|
| `data/ciphertext.txt` | Machine-readable transcription, block by block; `[a\|b]` marks uncertain glyphs |
| `data/transcription.md` | Annotated transcription and differences from Schmeh's transcript |
| `analysis/randomness_tests.py` | The test battery (Python 3, standard library only) |
| `results/test_results.txt` | Output with the preferred readings |
| `results/test_results_alt_f.txt` | Output with the alternative readings (`f`) |
| `analysis/heldout_model.py` | Held-out block test of keyboard models |
| `results/heldout_model_results.txt` | Its output |
| `data/numeric_transcription.md`, `analysis/numeric_tests.py`, `results/numeric_test_results.txt` | Number part |
| `docs/blog-comment.md`, `docs/blog-comment-numbers.md` | Comments as posted on Schmeh's blog |
| `docs/blog-comment-followup.md` | Follow-up comment with corrections |
| `audit/2026-10-29/` | Independent audit: report (Slovak), English summary, script and results |

## Transcription notes

- The three typed blocks are read **block by block**. Schmeh's transcript interleaves rows across the blocks.
- Readings that differ from Schmeh's transcript: line 2 `was[i|f]tzy`, line 7 `xfr[i|f]ews…`, line 18 `…cxx[i|f]gdfuam`, final group `hgf[m|n]uzzaa`.
- Header: `UHV. Y. Pal. 002`. A handwritten X follows line 32. The final group `eet hgfmuzzaa` is one physical line.

The image of the document is not included here. See Schmeh's article for it.

## Reproducing the results

```bash
python3 analysis/randomness_tests.py                 # preferred readings
python3 analysis/randomness_tests.py --alt           # [i|f] read as f
python3 analysis/randomness_tests.py --out results/test_results.txt
python3 analysis/heldout_model.py --out results/heldout_model_results.txt
python3 analysis/numeric_tests.py
```

The tests use a fixed random seed. The German control text is a 575-letter sample written for this
comparison, and the Vigenère control is that text encrypted with the key `NIBELUNGEN`.

### Tests included

Chi-square against uniform, index of coincidence, Shannon entropy, bigram mutual information, QWERTZ adjacency
and key distance, doubled letters, `aba` patterns, Wald–Wolfowitz runs test on hands, repeated 3- and 4-grams,
bz2 compressibility, approximate entropy (descriptive), kappa at shifts 1–20, periodic IC for periods 1–17, a naive
random-walk model (does not fit), per-block consistency, line-boundary transitions and a common-phase boundary test.

## Author

Jozef Krajčovič — historical cryptology researcher, author of the *katkryptolog* blog.

## License

Code: MIT (see `LICENSE`). Transcription and text: CC BY 4.0.
