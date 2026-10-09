"""Find the key of telegram no. 761 from the cipher text alone.

    python code/solve.py                     every width from 2 to 35; writes results/width_scan.txt
    python code/solve.py --widths 26 26      one width only; prints the result
    python code/solve.py --file NAME         another cipher text (a file of Russian letters in data/); prints the result

For each width the search (search.py) is started ten times from a random arrangement. The table gives the score of
the best arrangement found and how many of the ten starts ended on it. Uses all processor cores.
"""
import argparse

from model import Model, data_lines, letters, read_cipher, read_key, string, write_result
from search import solve_many
from transposition import decipher

TELEGRAM = 'telegram761.txt'
WIDTHS = [2, 35]
RESTARTS = 10
STEPS = 200000


def scan(cipher, widths, restarts=RESTARTS, steps=STEPS, seed=1):
    """[(width, score, key, starts that ended on that key)] for each width"""
    found = solve_many([(cipher, width, restarts, steps, seed) for width in widths])
    return [(width,) + result for width, result in zip(widths, found)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--file', default=TELEGRAM, help='a file in data/ (default: %(default)s)')
    ap.add_argument('--widths', nargs=2, type=int, default=WIDTHS, metavar=('FROM', 'TO'))
    ap.add_argument('--restarts', type=int, default=RESTARTS)
    ap.add_argument('--steps', type=int, default=STEPS)
    a = ap.parse_args()

    cipher = read_cipher(a.file)
    model = Model()
    controls = [model.score(letters(line)) for line in data_lines('control_texts.txt')]
    table = scan(cipher, range(a.widths[0], a.widths[1] + 1), a.restarts, a.steps)

    out = ['data/%s, %d letters: the best arrangement found for each width' % (a.file, len(cipher)),
           '%d starts of %d steps for each width. The score is the mean log-probability per trigram of the text that'
           % (a.restarts, a.steps),
           'the arrangement gives. For comparison: the six control texts score %.3f on average, and the cipher text'
           % (sum(controls) / len(controls)),
           'as it stands %.3f.' % model.score(cipher),
           '',
           'width   score  starts  the text begins']
    for width, score, key, same in table:
        out.append('%5d  %6.3f  %6d  %s' % (width, score, same, string(decipher(cipher, key))[:40]))
    ranked = sorted(table, key=lambda row: -row[1])
    width, score, key, same = ranked[0]
    out += ['', 'best: width %d, score %.3f, found by %d of %d starts' % (width, score, same, a.restarts)]
    if len(ranked) > 1:
        out.append('next best: width %d, score %.3f' % (ranked[1][0], ranked[1][1]))
    out.append('key at width %d: %s' % (width, ' '.join(str(k) for k in key)))
    if a.file == TELEGRAM:
        out.append('the same as data/key.txt: %s' % ('yes' if key == read_key() else 'no'))
    if (a.file, a.widths, a.restarts, a.steps) == (TELEGRAM, WIDTHS, RESTARTS, STEPS):
        write_result('width_scan.txt', out)
    else:
        print('\n'.join(out))


if __name__ == '__main__':
    main()
