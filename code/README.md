# Code

The scripts need Python 3.9 or later and only the standard library. Run them from the top folder of the
repository. They read from data/ and write to results/, and the two that search use every processor core.

## Everything at once

```
python code/reproduce.py            # run all steps, then print each documented figure next to the recomputed one
python code/reproduce.py --check    # print the comparison from the result files already present
python code/reproduce.py --only decipher solve    # run only some steps
```

A full run took four to seven minutes on the desktop used for this release, which has 32 threads. That is about
an hour and a half of work for a single core, so allow half an hour on a four-core laptop. The comparison table
is also written to results/reproduce_summary.txt, and the exit status is 1 if any figure differs.

## The steps one by one

| command | what it does | writes | time |
|---|---|---|---|
| `python code/decipher.py` | deciphers the telegram with data/key.txt, prints the sheet of 26 columns, lists the letters where the reading differs and checks them against data/emendations.tsv, counts letters and compares the other two readings of the scan | results/decipherment.txt | 1 s |
| `python code/solve.py` | finds the key from the cipher text alone, trying every width from 2 to 35 with ten runs each | results/width_scan.txt | 1 min |
| `python code/solve.py --widths 26 26` | the same for one width or any range of widths; `--restarts` and `--steps` change the effort | prints only | 10 s |
| `python code/solve.py --file NAME` | the same for another cipher text, given as a file of Russian letters in data/ | prints only | 1 min |
| `python code/controls.py` | runs the search on six other texts with planted keys, on the telegram's letters in random order, and on the first transcription | results/controls.txt | 3 min |

The result files from the last run are in results/, so any one script can be run without the others.

## Modules

- `transposition.py` is the cipher itself, in both directions. A key is the row of numbers as the clerk would
  have written it over the columns.
- `model.py` has the alphabet, the readers for the data files, and the trigram model that scores how much a text
  looks like Russian.
- `search.py` is the search for a key at a given width (simulated annealing over the order of the columns).

## Repeatability

Each run of the search takes its random numbers from a seed made of the width and the number of the run, so the
results do not depend on how many cores there are. Repeated runs on the same machine gave identical output. A
Python build whose floating-point library rounds differently could change a last digit somewhere, and the
comparison in reproduce.py is on the printed digits.

## What reproduce.py leaves out

`build_model.py` shows how the trigram table and the control texts in data/ were made. It needs the text of the
source volume, which is not in the repository (see data/README.md), so reproduce.py does not run it.

The compiled program that first found the key is not in the repository, nor are the scripts used along the way
for cutting up the scan and comparing readings of single letters. The search in this folder is a plain rewrite
that gives the same key.
