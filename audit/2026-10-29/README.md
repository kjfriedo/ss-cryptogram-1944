# Independent audit, 29 October 2026

An independent review of this repository, carried out with ChatGPT at the author's request and added here unchanged.
The report is in Slovak (`audit_report_sk.md`); a summary in English follows.

| File | Description |
|---|---|
| `audit_report_sk.md` | The audit report (Slovak), unchanged |
| `independent_audit.py` | The audit's own computation (Python 3, numpy, scipy; seed 20261029) |
| `audit_results.json` | Its full numerical output |
| `data/ciphertext.txt` | The frozen input: the transcription at commit `1eac579`, which the script reads |

The audit was based on commit `1eac5795a712322331e76ba1b82f71291cf1ea48`. The other input files it used
(`data/transcription.md`, `analysis/randomness_tests.py`) are identical to that commit and can be viewed there.

## Reproduction

```bash
pip install numpy scipy
python3 audit/2026-10-29/independent_audit.py
```

Rerunning it with numpy 2.5.3 and scipy 1.18.1 reproduced `audit_results.json` exactly. (The report lists numpy
2.3.5 and scipy 1.17.0.)

## Summary in English

**Verdict.** The sequence is very strongly tied to QWERTZ keyboard geometry, and keyboard-generated text is the
most economical working explanation. "Definitively proven not to be a cipher" goes beyond the evidence: the
statistics do not determine the document's purpose, origin, date or the author's intent.

**Confirmed:**
- Adjacent keys: 300 of 574 pairs against about 17 % expected, with 0 exceedances in 100,000 shuffles.
- The signal survives excluding repeated keys, horizontal-only adjacency, wider distance thresholds, and shuffling
  within each line.
- Random relabelling of the 26 letters to key positions, keeping every bigram, never reached the QWERTZ score.
- QWERTZ fits better than QWERTY (43 %).
- All 16 combinations of the uncertain glyphs give 52.3–52.6 % adjacency.

**Corrections requested (all made in the main README):**
- Frequencies are not flat (χ² = 181, 25 df). The IC of 0.049 is not "close to random".
- "No substitution can produce this" is invalid: a keyboard-designed substitution key could.
- The periodic-IC test (calibrated p ≈ 0.22 block-wise, ≈ 0.10 interleaved) does not exclude Vigenère variants in
  general, such as autokey or running keys, a key that resets every line, or a prior transposition.
- The naive random-walk model does not fit (about 73 % adjacency and 127 aba patterns against 52 % and 31).
- The ApEn test was oriented the wrong way.
- The final group `eet hgfmuzzaa` is one physical line, so 6 of 33 transitions cross line ends, not 6 of 34.
- The p-values are conditional Monte Carlo values; tests sharing bigrams must not be multiplied.

**Line boundaries.** A common-phase test (only 3 of 575 shifts give so few adjacent pairs) links the pattern to
the typed lines. A cyclic-cut null (p ≈ 0.47) shows that the exact line starts and ends are not unusual given
line-wise units. The boundaries alone do not prove that each line is one hand movement.

**Alternatives kept open:**
- Keyboard-generated key material (rated a realistic functional alternative)
- A keyboard-designed or homophonic cipher with a line reset
- Transposition of a special short text
- Steganography

The audit did not independently test the number part.

**Recommended next steps:**
1. The original document and its archival context
2. A blind second transcription and more control material
3. A held-out block test of a directional typing model, now done: see `analysis/heldout_model.py`
4. A pre-registered, constrained test of any letter–digit pairing
