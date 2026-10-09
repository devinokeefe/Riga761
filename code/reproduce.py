"""Regenerate the figures quoted in README.md and docs/ from the data, and compare them with the documented values.

    python code/reproduce.py            run every step (a few minutes on a desktop computer), then compare
    python code/reproduce.py --check    compare only, from the result files already in results/
    python code/reproduce.py --only decipher solve      run only the named steps, then compare

Steps (each is an ordinary script that can also be run by itself; see code/README.md):
    decipher   decipher.py    the telegram deciphered with its key, and compared with the reading
    solve      solve.py       the key found from the cipher text alone, every width from 2 to 35
    controls   controls.py    the same search on texts with a planted key, and on shuffled letters

The table printed at the end is also written to results/reproduce_summary.txt. Exit status 1 if a figure differs.
"""
import argparse
import os
import re
import subprocess
import sys
import time

from model import ROOT, path

STEPS = [('decipher', 'decipher.py'), ('solve', 'solve.py'), ('controls', 'controls.py')]


def rx(pattern, fmt=None):
    def f(text):
        m = re.search(pattern, text, re.S)
        if not m:
            return 'not found'
        return fmt.format(*m.groups()) if fmt else ' / '.join(m.groups())
    return f


def each(*patterns):
    """one figure made of several, each found by its own pattern"""
    return lambda text: ' / '.join(rx(p)(text) for p in patterns)


D, W, C = 'results/decipherment.txt', 'results/width_scan.txt', 'results/controls.txt'
BLIND = r'\n\s+{}\s+(\d+)\s+(\d+)\s+(-[\d.]+)\s+(\d+)\s+(-[\d.]+)'
# (figure, value quoted in the documentation, result file, how to read it from the file)
FIGURES = [
    ('THE TELEGRAM', None, None, None),
    ('letters / columns / full rows / letters in the last row', '558 / 26 / 21 / 12', D,
     rx(r'(\d+) letters in (\d+) columns: (\d+) full rows and (\d+) letters')),
    ('letters corrected in the reading', '23 of 558 (4.1%)', D,
     rx(r'(\d+) of (\d+) letters differ \(([\d.]+%)\)', '{0} of {1} ({2})')),
    ('the corrections are those of data/emendations.tsv', 'yes', D, rx(r'the same as data/emendations\.tsv: (\w+)')),
    ('words in the reading / marks х / тчк and зпт', '114 / 22 / 4', D,
     rx(r'(\d+) words, of which (\d+) are the mark х and (\d+) are')),
    ('score: cipher text / its letters in random order', '-4.905 / -5.108', D,
     each(r'cipher text as it stands\s+(-[\d.]+)', r'random order \(20 times\)\s+(-[\d.]+)')),
    ('score: deciphered / the reading / control texts', '-2.962 / -2.708 / -2.116', D,
     each(r'deciphered with the key\s+(-[\d.]+)', r'the reading\s+(-[\d.]+)', r'six control texts\s+(-[\d.]+)')),
    ('rising runs in the key', '13', D, rx(r'Rising runs in the key: (\d+)')),
    ('commonest letters', 'о 10.0%, а 9.0%, и 7.2%, е 6.8%', D, rx(r'Commonest letters of the telegram: (.+?)\n')),
    ('the letter х: share of the telegram / of the model text', '4.3% / 1.1%', D,
     rx(r'The letter х: ([\d.]+%) of the telegram, ([\d.]+%) of the text')),
    ('first transcription: letters changed / letters to correct', '13 / 36', D,
     each(r'first transcription \([^)]*\) differs in (\d+) letters', r'differs from the reading in (\d+) letters')),
    ('check reading: letters / letters that differ', '558 / 0', D,
     rx(r'check reading \([^)]*\) has (\d+) letters and differs in (\d+)')),
    ('THE SEARCH', None, None, None),
    ('best width; score; starts that found it', '26; -2.962; 10 of 10', W,
     rx(r'best: width (\d+), score (-[\d.]+), found by (\d+ of \d+) starts', '{0}; {1}; {2}')),
    ('next best width; score', '33; -4.040', W, rx(r'next best: width (\d+), score (-[\d.]+)', '{0}; {1}')),
    ('the key found is that of data/key.txt', 'yes', W, rx(r'the same as data/key\.txt: (\w+)')),
    ('CONTROLS', None, None, None),
    ('control texts: score as they stand / with 23 letters replaced', '-2.116 / -2.461', C,
     rx(r'score (-[\d.]+) on average as they stand \(mean log-probability per trigram\) and (-[\d.]+)')),
    ('texts whose planted key was found, widths 16 / 21 / 26 / 31 / 36 / 41', '6/6 / 6/6 / 6/6 / 6/6 / 5/6 / 3/6', C,
     rx(r'texts\s+(\d+/\d+)\s+(\d+/\d+)\s+(\d+/\d+)\s+(\d+/\d+)\s+(\d+/\d+)\s+(\d+/\d+)')),
    ('width not known, text 1: planted; best, score; next best, score', '21; 21, -2.449; 28, -3.718', C,
     rx(BLIND.format(1), '{0}; {1}, {2}; {3}, {4}')),
    ('width not known, text 3: planted; best, score; next best, score', '26; 26, -2.434; 30, -4.048', C,
     rx(BLIND.format(3), '{0}; {1}, {2}; {3}, {4}')),
    ('width not known, text 5: planted; best, score; next best, score', '31; 31, -2.496; 35, -3.966', C,
     rx(BLIND.format(5), '{0}; {1}, {2}; {3}, {4}')),
    ('telegram in random order, width 26: best / worst score', '-4.291 / -4.396', C,
     rx(r'best score (-[\d.]+), worst (-[\d.]+)')),
    ('first transcription, width 26: score; starts; same key', '-3.091; 6 of 10; yes', C,
     rx(r'width 26: score (-[\d.]+), found by (\d+ of \d+) starts; the key is the same as data/key\.txt: (\w+)',
        '{0}; {1}; {2}')),
]


def compare():
    rows, bad = [], 0
    cache = {}
    for name, documented, file, read in FIGURES:
        if documented is None:
            rows.append((name, '', '', ''))
            continue
        if file not in cache:
            cache[file] = open(path(file), encoding='utf-8').read() if os.path.exists(path(file)) else None
        got = 'file missing: ' + file if cache[file] is None else read(cache[file])
        ok = got == documented
        bad += not ok
        rows.append(('  ' + name, documented, got, 'ok' if ok else 'DIFFERS'))
    w = [max(len(r[i]) for r in rows) for i in range(3)]
    lines = ['%-*s  %-*s  %s' % (w[0], 'figure', w[1], 'documented', 'reproduced'), '-' * (sum(w) + 12)]
    lines += [('%-*s  %-*s  %-*s  %s' % (w[0], a, w[1], b, w[2], c, d)).rstrip() for a, b, c, d in rows]
    n = sum(1 for f in FIGURES if f[1] is not None)
    lines += ['', '%d of %d figures reproduce' % (n - bad, n) + ('; %d differ' % bad if bad else '')]
    return lines, bad


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true', help='compare only; run nothing')
    ap.add_argument('--only', nargs='+', choices=[name for name, _ in STEPS], help='run only these steps')
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    if not a.check:
        for name, script in STEPS:
            if a.only and name not in a.only:
                continue
            t0 = time.time()
            print('--- %s: python code/%s' % (name, script), flush=True)
            r = subprocess.run([sys.executable, os.path.join(here, script)], cwd=ROOT, stdout=subprocess.DEVNULL)
            print('    exit status %d, %.0f s' % (r.returncode, time.time() - t0), flush=True)
            if r.returncode:
                sys.exit('step %s failed' % name)
    lines, bad = compare()
    with open(path('results', 'reproduce_summary.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
