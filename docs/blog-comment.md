> As posted on Klaus Schmeh's blog. Some statements were corrected later; see `docs/blog-comment-followup.md` and the *Limitations* section of the README.

I looked at this cryptogram and I believe it is not a cipher at all but keyboard mashing on a German QWERTZ typewriter.

**Transcript.** The three typed blocks should be read one after another (column by column), not row by row across the blocks. My reading from the high-resolution image differs in three or four places: row 2 *was[i/f]tzy*, row 7 *xfr[i/f]ews…*, row 18 *…cxx[i/f]gdfuam*, and the final group, which is *hgfmuzzaa* rather than *hgfnuzzaa*. In the three i/f cases the glyph lacks both the hook of every other "f" and the dot of the other "i"s. With this transcript the index of coincidence comes out at 4.9 %, not 6.8 %.

**Tests** (each compared with 2,000 shuffles of the same letters):
- Successive letters sit on adjacent keys in 52 % of cases, against 17 % expected (z ≈ 22). The pairs *tz, zh, cx, xy* only make sense on a QWERTZ layout.
- Trigram repeats number 132 against 18 expected; the strongest structure appears in runs such as *sdfg, ztre, cxys*.
- A runs test on left/right hand gives z = −11.6, so there are long stretches typed with one hand.
- Letter frequencies are flat, with an IC close to random and far from German, and periodic IC and kappa tests show no period from 1 to 17. This excludes Vigenère-type and other periodic ciphers.
- The keyboard pattern stops at line breaks: 54 % of adjacent pairs within lines, but only 6 of 34 (≈ 18 %) across line ends. Each line is a separate hand movement. A real ciphertext merely split into lines would show no such effect.

No substitution or polyalphabetic encryption of German text can produce keyboard adjacency at this level. My guess is filler, a decoy, or a typing test. The header "UHV. Y. Pal. 002" and the handwritten X next to row 32 may help identify what the document actually is.

Jozef Krajčovič
