"""Does the search find a key when there is one, and only then? Writes results/controls.txt.

    python code/controls.py

Four tests, all with the settings of solve.py (ten starts of 200,000 steps):

1. Planted keys, width known. Each of the six control texts (558 letters of Russian that the trigram table has not
   seen) gets 23 letters replaced at random, as many as are corrected in the telegram, and is enciphered with a
   random key at each of six widths. The search is run at that width.
2. Planted keys, width not known. Three of those cipher texts are searched at every width from 2 to 35, as the
   telegram is.
3. Nothing to find. The letters of the telegram are put in random order and searched at width 26.
4. The first transcription of the telegram, which differs from the final one in 13 letters, searched at width 26.

Uses all processor cores.
"""
import random

from model import A, Model, data_lines, letters, read_cipher, read_key, write_result
from search import solve_many
from solve import RESTARTS, STEPS, WIDTHS
from transposition import encipher

PLANTED_WIDTHS = [16, 21, 26, 31, 36, 41]
BLIND = [(0, 21), (2, 26), (4, 31)]       # (control text, planted width) for test 2
GARBLED = 23
SHUFFLES = 5


def garble(text, number):
    """control text `number` with 23 letters replaced by other letters"""
    rng = random.Random('garble %d' % number)
    text = text[:]
    for place in rng.sample(range(len(text)), GARBLED):
        text[place] = rng.choice([x for x in range(A) if x != text[place]])
    return text


def random_key(number, width):
    key = list(range(1, width + 1))
    random.Random('key %d %d' % (number, width)).shuffle(key)
    return key


def main():
    model = Model()
    plain = [letters(line) for line in data_lines('control_texts.txt')]
    texts = [garble(text, number) for number, text in enumerate(plain)]
    telegram = read_cipher()
    scan_widths = list(range(WIDTHS[0], WIDTHS[1] + 1))

    # every search to be run, by name
    ciphers = {}
    for number, text in enumerate(texts):
        for width in PLANTED_WIDTHS:
            ciphers['planted', number, width] = (encipher(text, random_key(number, width)), width)
    for number, planted_width in BLIND:
        for width in scan_widths:
            ciphers['blind', number, width] = (ciphers['planted', number, planted_width][0], width)
    for n in range(SHUFFLES):
        shuffled = telegram[:]
        random.Random('shuffle %d' % n).shuffle(shuffled)
        ciphers['shuffled', n] = (shuffled, 26)
    ciphers['first'] = (read_cipher('telegram761_first_transcription.txt'), 26)
    names = list(ciphers)
    found = solve_many([ciphers[name] + (RESTARTS, STEPS, 1) for name in names])
    result = dict(zip(names, found))

    def mean_score(some):
        return sum(model.score(t) for t in some) / len(some)

    out = ['Controls for the search (%d starts of %d steps each time)' % (RESTARTS, STEPS),
           '',
           '== 1. Planted keys, width known',
           'The six control texts score %.3f on average as they stand (mean log-probability per trigram) and %.3f'
           % (mean_score(plain), mean_score(texts)),
           'with %d letters replaced. Entries: how many of the %d starts ended on the planted key.'
           % (GARBLED, RESTARTS),
           '',
           'text  ' + ''.join('  width %2d' % w for w in PLANTED_WIDTHS)]
    texts_found = [0] * len(PLANTED_WIDTHS)
    for number in range(len(texts)):
        row = '%4d  ' % (number + 1)
        for i, width in enumerate(PLANTED_WIDTHS):
            score, key, same = result['planted', number, width]
            hits = same if key == random_key(number, width) else 0
            texts_found[i] += hits > 0
            row += '%10d' % hits
        out.append(row)
    out.append('texts ' + ''.join('%8d/%d' % (n, len(texts)) for n in texts_found))

    out += ['',
            '== 2. Planted keys, width not known (every width from %d to %d searched)' % tuple(WIDTHS),
            'text  planted width  best width   score  next best width   score']
    for number, planted_width in BLIND:
        ranked = sorted(scan_widths, key=lambda w: -result['blind', number, w][0])
        out.append('%4d  %13d  %10d  %6.3f  %15d  %6.3f'
                   % (number + 1, planted_width, ranked[0], result['blind', number, ranked[0]][0],
                      ranked[1], result['blind', number, ranked[1]][0]))

    scores = [result['shuffled', n][0] for n in range(SHUFFLES)]
    out += ['',
            '== 3. Nothing to find',
            'The letters of the telegram in random order, searched at width 26, %d times:' % SHUFFLES,
            'best score %.3f, worst %.3f' % (max(scores), min(scores))]

    score, key, same = result['first']
    out += ['',
            '== 4. The first transcription',
            'width 26: score %.3f, found by %d of %d starts; the key is the same as data/key.txt: %s'
            % (score, same, RESTARTS, 'yes' if key == read_key() else 'no')]
    write_result('controls.txt', out)


if __name__ == '__main__':
    main()
