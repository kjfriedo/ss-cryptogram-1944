# SS cryptogram (1944/45): transcription and randomness analysis

An analysis of the typed "SS cryptogram" published by Klaus Schmeh on 22 October 2026 in
[Who can decipher this message from World War II?](https://klausschmeh.net/who-can-decipher-this-message-from-world-war-ii/).
Bogusław Wróbel found the document in the archives of the Polish Military Mission in Berlin, and it is said to concern
the hiding of cultural assets in Lower Silesia.

## Conclusion

The text is very unlikely to be a cipher. Its letter sequence is strongly non-random, but all of that structure
comes from the geometry of a German **QWERTZ** keyboard rather than from language or a key. The most likely
explanation is keyboard mashing on a typewriter: filler, a decoy or a typing test.

| Test (575 letters) | Cryptogram | Shuffled letters (2,000×) | German text |
|---|---|---|---|
| Adjacent-key pairs | 52 % | 17 % (z ≈ 22) | 18 % |
| Mean key distance | 1.59 | 2.59 (z ≈ 19) | 2.97 |
| Repeated trigrams | 132 | 18 (z ≈ 27) | 190 |
| Index of coincidence | 0.049 | 0.049 | 0.083 |
| Left/right-hand runs test | z = −11.6 | z ≈ 0 | z ≈ 0 |

- **No language signal.** Letter frequencies are flat, with an IC close to random.
- **No periodicity.** Mean column IC is flat for periods 1–17 and the kappa test shows no peak, which excludes Vigenère-type ciphers.
- **Line breaks reset the pattern.** Adjacent-key pairs make up 54 % within lines but only 6 of 34 (≈ 18 %) across line ends, so each line is a separate hand movement.
- **Robust to the uncertain readings.** Reading the uncertain `[i|f]` glyphs as `f` does not change the result (52.6 % adjacent keys, z ≈ 22.5).

## Second document: numeric "cipher" (UHG. Yc. 002)

Bogusław Wróbel supplied a second sheet from the same series: 542 typed digits in three blocks, plus a small
"key table" (`Ya. I00`, digit pairs and the letter pairs `FF ZT AA / RT RE IU`). It shows the same keyboard
signature, this time on the typewriter's number row:

| Test (542 digits) | Document | Shuffled digits (3,000×) |
|---|---|---|
| Digit 0 | never occurs | expected ≈ 54 if uniform |
| Steps of ±1 (e.g. `8765`, `2323`) | 43 % | 19 % (z ≈ 15) |
| Runs of four consecutive ±1 steps | 25 | 0.8 (z ≈ 25) |
| Adjacent keys | 56 % | 32 % (z ≈ 12) |
| Adjacent keys across line ends | 28 % (11 of 40) | 32 % |

- The digits cluster in the middle of the row (4–6), and 0, at the far right, is absent.
- A numeric additive cipher or code would give near-uniform digits including 0.
- As with the letters, the pattern resets at every line break.
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
| `docs/blog-comment.md` | Comment submitted to Schmeh's blog |

## Transcription notes

- The three typed blocks are read **block by block**. Schmeh's transcript interleaves rows across the blocks.
- Readings that differ from Schmeh's transcript: line 2 `was[i|f]tzy`, line 7 `xfr[i|f]ews…`, line 18 `…cxx[i|f]gdfuam`, final group `hgf[m|n]uzzaa`.
- Header: `UHV. Y. Pal. 002`. A handwritten X follows line 32.

The image of the document is not included here. See Schmeh's article for it.

## Reproducing the results

```bash
python3 analysis/randomness_tests.py                 # preferred readings
python3 analysis/randomness_tests.py --alt           # [i|f] read as f
python3 analysis/randomness_tests.py --out results/test_results.txt
```

The tests use a fixed random seed. The German control text is a 575-letter sample written for this
comparison, and the Vigenère control is that text encrypted with the key `NIBELUNGEN`.

### Tests included

Chi-square against uniform, index of coincidence, Shannon entropy, bigram mutual information, QWERTZ adjacency
and key distance, doubled letters, `aba` patterns, Wald–Wolfowitz runs test on hands, repeated 3- and 4-grams,
bz2 compressibility, approximate entropy, kappa at shifts 1–20, periodic IC for periods 1–17, a random-walk
keyboard-mashing model, per-block consistency and line-boundary transitions.

## Author

Jozef Krajčovič — historical cryptology researcher, author of the *katkryptolog* blog.

## License

Code: MIT (see `LICENSE`). Transcription and text: CC BY 4.0.
