# How the telegram was read

All the figures on this page come out of `python code/reproduce.py`.

## Recognising the cipher

Every other telegram in the archive file is in groups of five figures. This one is in groups of five
letters, and the letters occur about as often as they do in ordinary Russian: о makes up 10.0% of the text, а
9.0%, и 7.2% and е 6.8%. If each letter had been swapped for another, those peaks would sit on other letters. So
the telegram is made of the message's own letters in a different order, which is a transposition.

The one letter out of line is х, at 4.3% of the telegram against about 1% in ordinary Russian. That was explained
once the text could be read. The clerk had put an х before and after every proper name except the first
word.

There was outside evidence as well. John Tiltman began work on Soviet diplomatic telegrams for the British in
1920, and of the first system he met he wrote that "All messages were enciphered by simple columnar transposition
of Russian plain text" (see [LITERATURE.md](LITERATURE.md)). In a columnar transposition the text is written in
rows under a key and copied out by columns, so solving one means finding how many columns there were and in what
order they were taken.

## The search

Choose a number of columns and the cipher text falls into that many strips. The program
([code/search.py](../code/search.py)) looks for the arrangement of the strips that makes the rows read most like
Russian. It starts from a random arrangement and makes small changes to it, swapping two strips, moving a block
of them or rotating the whole row. A change that improves the text is always kept. A change that makes it worse
is sometimes kept too, less and less often as the run goes on, which stops the search from settling too early on
a poor arrangement (this is simulated annealing). Every width gets ten runs of 200,000 steps, each from a
different random start.

"Like Russian" is measured with a table of how often each three-letter sequence occurs in about 1.1 million
letters of Soviet diplomatic documents from 1920-21 (1,140,169 sequences, as the header of
[data/russian_trigrams.tsv](../data/README.md) records). During the search an arrangement is judged by the
probability of each letter given the one before it, taken from the same table, because that can be added up
strip by strip. The scores reported here are the average log-probability of each letter given the two before
it, so they are negative and closer to zero is better:

| text | score |
|---|---|
| Russian diplomatic prose the table has not seen (six passages of 558 letters) | -2.116 |
| the same with 23 letters replaced at random | -2.461 |
| the telegram's letters in random order | -5.108 |
| the telegram as it stands | -4.905 |

One complication is that the last row of the clerk's sheet was not full. Some columns are therefore a letter
longer than others, and which ones are longer depends on where they stood on the sheet. The search works this
out as it goes and does not need to be told how long the last row was.

## The result

The search was run at every width from 2 to 35 ([results/width_scan.txt](../results/width_scan.txt)).

| width | best score | runs out of ten that reached it | the text begins |
|---|---|---|---|
| 24 | -4.296 | 1 | нвныиищгимыисчмвенсианох |
| 25 | -4.288 | 1 | хзиовгуиччвхоечрмочрондр |
| 26 | -2.962 | 10 | длянаркомздравахоеиашкох |
| 27 | -4.309 | 1 | уйхнодыаготчиибупучхпнде |
| 28 | -4.312 | 1 | еобтедатьнахиюхнсоатвооа |
| 33 (the best of the other 29) | -4.040 | 1 | звзриховпаниачпрьбеегпрх |

At 26 columns all ten runs finish on the same key, and the text reads from its first words, для Наркомздрава. No
other width gives anything readable.

The telegram scores -2.962, some way short of the -2.116 of clean prose. Correcting the 23 letters of the
Polish copy that do not fit their words ([TEXT.md](TEXT.md)) brings it to -2.708. The rest of the gap is telegraphese: 22 х marks, тчк and
зпт spelled out, and a good many proper names.

## Testing the search

A search like this can miss a key that is there, and it can also turn up something that looks like Russian in a
text that has no key. Each was tested ([results/controls.txt](../results/controls.txt)).

To see whether it misses keys, six passages of 558 letters were taken from Soviet diplomatic documents that had
been kept out of the trigram table. Each had 23 letters replaced at random, to match the state of the telegram,
and was enciphered with random keys at six widths. The search was then run at the correct width. The table shows
how many of the ten runs found the planted key.

| text | width 16 | 21 | 26 | 31 | 36 | 41 |
|---|---|---|---|---|---|---|
| 1 | 10 | 9 | 9 | 7 | 2 | 0 |
| 2 | 10 | 10 | 9 | 8 | 0 | 0 |
| 3 | 10 | 10 | 10 | 10 | 2 | 3 |
| 4 | 10 | 10 | 9 | 10 | 1 | 0 |
| 5 | 10 | 9 | 10 | 10 | 2 | 1 |
| 6 | 10 | 9 | 10 | 10 | 6 | 2 |

Up to 31 columns the key was found for every text, by at least seven runs in ten. Beyond that the search starts
to fail. At 36 columns it missed one text out of six, and at 41 it missed three. That is why the scan of the
telegram stops at 35. A much wider key would not have been found this way, but since the telegram reads in full
at 26 there is nothing left for one to explain.

Three of the planted texts were also searched at every width from 2 to 35, the way the telegram was, without
the program being told the width. The planted width won clearly each time.

| planted width | best width found | its score | next best width | its score |
|---|---|---|---|---|
| 21 | 21 | -2.449 | 28 | -3.718 |
| 26 | 26 | -2.434 | 30 | -4.048 |
| 31 | 31 | -2.496 | 35 | -3.966 |

To see whether it finds keys that are not there, the telegram's letters were shuffled five times and each
shuffle was searched at width 26. The best scores were between -4.396 and -4.291. That is about what the wrong
widths give for the real telegram, and a long way from -2.962.

## Three readings of the scan

The key was first found on 5 October 2026 from a first transcription of the scan, by a compiled search program
that scored four-letter sequences. For this release the scan was transcribed again letter by
letter, and the search was rewritten in plain Python so that anyone can run it.

The second transcription changed 13 letters ([results/decipherment.txt](../results/decipherment.txt) lists
them). In nine of them an н had been taken for и or м, because the typewriter's н has a heavy crossbar that
tends to fill with ink. Every one of the 13 changes turned a garbled word into a correct one, and the number of
letters needing correction fell from 36 to 23. The first transcription is still in
[data/telegram761_first_transcription.txt](../data/telegram761_first_transcription.txt). Searching it at width
26 gives the same key (6 runs out of 10, score -3.091).

Finally the scan was read a third time from enlarged strips, without reference to the other two readings. This
check reading agrees with the final transcription in all 558 letters.

## The key

```
9 8 23 1 13 17 11 24 6 21 7 4 10 15 26 14 18 22 25 12 19 3 20 5 16 2
```

These are the numbers over the columns, from left to right. The column numbered 1 was copied out first.

Keys like this were normally made from a word or phrase by numbering its letters in alphabetical order, with
repeated letters numbered from left to right. If that was done here, the phrase had 26 letters, at least 13 of
them different. It has not been identified.
