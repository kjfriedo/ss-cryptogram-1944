> As posted on Klaus Schmeh's blog. Some statements were corrected later; see `docs/blog-comment-followup.md` and the *Limitations* section of the README.

The number part shows the same signature as the letter part: keyboard mashing, this time on the typewriter's number row. (Note that the machine had no "1" key, so every 1 is a typed capital I.)

**Tests** (542 digits, each compared with 3,000 shuffles of the same digits):
- The digit 0 never occurs. A code or an additive cipher would give roughly equal digits, so about 54 zeros would be expected. The 0 key sits at the far right of the row, and the digits cluster around 4–6, in the middle.
- 43 % of steps go to a neighbouring digit, as in 8765… or 2323…, against 19 % for shuffled digits (z ≈ 15). There are 25 runs of four such steps in a row, against fewer than 1 expected.
- As in the letter part, the pattern stops at line breaks: 56 % of steps within lines land on adjacent keys, but only 11 of 40 (28 %) across line ends, which is chance level.
- The letter pairs in the small table (FF ZT AA / RT RE IU) are themselves doubled letters or adjacent keys.

**Gerry's one-time pad idea.** The layout match is real: the lower part of the second number column and the first four lines of the second letter column both run 17, 17, 19 and 17 characters. Even so, I don't think the numbers are a key:
1. A one-time pad has to be random, and these digits are not (no zeros, long ±1 runs).
2. Adding or subtracting them from the letters gives random-looking text (IC 0.034–0.043 for every pairing I tried), as Gerry found.
3. If German plaintext had been enciphered with any additive key, the keyboard adjacency in the letter part (52 % against 17 % expected) would have been destroyed, not created.

I read the identical line lengths, including the odd 19, as a sign that both parts were typed to the same layout. That fits a typing exercise or prepared filler better than a message and its key.

My transcription differs from the Word transcript in three places: line 2 of the lower part of column 1 reads …32844 rather than …32884, and two digits in column 2 are uncertain (3 or 8). None of this affects the results. Transcriptions, script and results: https://github.com/kjfriedo/ss-cryptogram-1944

Jozef Krajčovič
