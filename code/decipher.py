"""Decipher telegram no. 761 with its key and compare the result with the reading. Writes results/decipherment.txt.

    python code/decipher.py

Reads data/telegram761.txt, key.txt, reading.txt, emendations.tsv, doubtful_letters.tsv, the first
transcription and the check reading.
"""
import random

from model import Model, data_lines, letters, path, read_cipher, read_key, string, write_result
from transposition import check_key, column_lengths, decipher, reading_order, rows


def cipher_places(n, key):
    """for each place in the plain text (from 0), its place in the cipher text (from 0)"""
    return decipher(list(range(n)), key)


def words_by_place(lines):
    """the word of the reading in which each letter stands"""
    out = []
    for line in lines:
        for word in line.split():
            out += [word] * len(letters(word))
    return out


def runs(key):
    """Number of rising runs in the places of the key numbers 1, 2, 3, ... A key made by numbering the letters of a
    phrase in alphabetical order, equal letters from left to right, has no more runs than the phrase has different
    letters."""
    place = reading_order(key)
    return 1 + sum(1 for a, b in zip(place, place[1:]) if b < a)


def table(name):
    with open(path('data', name), encoding='utf-8') as f:
        return [line.rstrip('\n').split('\t') for line in f if line.strip() and not line.startswith('#')][1:]


def main():
    cipher, key = read_cipher(), check_key(read_key())
    n, width = len(cipher), len(key)
    plain = decipher(cipher, key)
    lengths = column_lengths(n, width)
    model = Model()

    out = ['Telegram no. 761 deciphered with data/key.txt',
           '%d letters in %d columns: %d full rows and %d letters; columns 1-%d have %d letters, the others %d'
           % (n, width, n // width, n % width, n % width, lengths[0], lengths[-1]),
           '',
           '     ' + ''.join('%3d' % k for k in key)]
    for i, row in enumerate(rows(plain, width)):
        out.append('%3d  ' % (i + 1) + ''.join('  ' + ch for ch in string(row)))

    reading_lines = data_lines('reading.txt')
    reading = letters(' '.join(reading_lines))
    assert len(reading) == n
    word = words_by_place(reading_lines)
    place = cipher_places(n, key)
    differ = [i for i in range(n) if plain[i] != reading[i]]
    out += ['',
            'Against the reading (data/reading.txt): %d of %d letters differ (%.1f%%)'
            % (len(differ), n, 100.0 * len(differ) / n),
            '',
            'place  row  column  cipher place  typed  read  word']
    found = []
    for i in differ:
        entry = [str(i + 1), str(i // width + 1), str(i % width + 1), str(place[i] + 1),
                 string([plain[i]]), string([reading[i]]), word[i]]
        found.append(entry)
        out.append('%5s  %3s  %6s  %12s  %5s  %4s  %s' % tuple(entry))
    out.append('the same as data/emendations.tsv: %s' % ('yes' if found == table('emendations.tsv') else 'no'))

    back = dict((c, p) for p, c in enumerate(place))
    out += ['',
            'Doubtful letters (data/doubtful_letters.tsv) and where they fall',
            '',
            'cipher place  as read  could be  place  word in the reading']
    for row in table('doubtful_letters.tsv'):
        c = int(row[0]) - 1
        assert string([cipher[c]]) == row[3]
        out.append('%12s  %7s  %8s  %5d  %s' % (row[0], row[3], row[4], back[c] + 1, word[back[c]]))

    first = read_cipher('telegram761_first_transcription.txt')
    changed = ['%d %s>%s' % (i + 1, string([first[i]]), string([cipher[i]])) for i in range(n) if first[i] != cipher[i]]
    out += ['',
            'The first transcription (data/telegram761_first_transcription.txt) differs in %d letters' % len(changed),
            '(cipher place, first reading > final reading): ' + ', '.join(changed),
            'Deciphered with the key, it differs from the reading in %d letters'
            % sum(1 for a, b in zip(decipher(first, key), reading) if a != b)]
    check = read_cipher('telegram761_check_reading.txt')
    out += ['',
            'The check reading (data/telegram761_check_reading.txt) has %d letters and differs in %d'
            % (len(check), sum(1 for a, b in zip(check, cipher) if a != b) + abs(len(check) - n))]

    share = sorted(((100.0 * cipher.count(x) / n, string([x])) for x in set(cipher)), reverse=True)
    in_table = [sum(row) for row in model.count2]
    x = letters('х')[0]
    out += ['',
            'Commonest letters of the telegram: ' + ', '.join('%s %.1f%%' % (ch, v) for v, ch in share[:4]),
            'The letter х: %.1f%% of the telegram, %.1f%% of the text behind the trigram table'
            % (100.0 * cipher.count(x) / n, 100.0 * in_table[x] / sum(in_table))]

    marks = sum(1 for line in reading_lines for w in line.split() if w == 'х')
    stops = sum(1 for line in reading_lines for w in line.split() if w in ('тчк', 'зпт'))
    shuffled = []
    for seed in range(20):
        text = cipher[:]
        random.Random(seed).shuffle(text)
        shuffled.append(model.score(text))
    controls = [model.score(letters(line)) for line in data_lines('control_texts.txt')]
    out += ['',
            'In the reading: %d words, of which %d are the mark х and %d are тчк or зпт'
            % (sum(len(line.split()) for line in reading_lines), marks, stops),
            '',
            'Mean log-probability per trigram (nearer zero is more like Russian)',
            '  the cipher text as it stands             %.3f' % model.score(cipher),
            '  its letters in random order (20 times)   %.3f' % (sum(shuffled) / len(shuffled)),
            '  deciphered with the key                  %.3f' % model.score(plain),
            '  the reading                              %.3f' % model.score(reading),
            '  six control texts                        %.3f (from %.3f to %.3f)'
            % (sum(controls) / len(controls), min(controls), max(controls)),
            '',
            'Rising runs in the key: %d' % runs(key)]
    write_result('decipherment.txt', out)


if __name__ == '__main__':
    main()
