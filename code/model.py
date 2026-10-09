"""The Russian alphabet as numbers, the data files, and a trigram model of Russian.

The model is a table of how often each run of three letters occurs in a body of Russian diplomatic prose
(data/russian_trigrams.tsv). A text is scored by the mean natural logarithm of the probability of each letter given
the two before it. Running Russian scores about -2.1 and the same letters in random order about -4.8.
"""
import math
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')        # Cyrillic output, whatever the console's own code page

ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'      # 32 letters; ё is written е
INDEX = {ch: i for i, ch in enumerate(ALPHABET)}
A = len(ALPHABET)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def path(*parts):
    return os.path.join(ROOT, *parts)


def letters(text):
    """the Cyrillic letters of a string as numbers; everything else is dropped"""
    return [INDEX[ch] for ch in text.lower().replace('ё', 'е') if ch in INDEX]


def string(numbers):
    return ''.join(ALPHABET[i] for i in numbers)


def data_lines(name):
    """the lines of a file in data/, without comment lines (those that begin with #) and blank lines"""
    with open(path('data', name), encoding='utf-8') as f:
        return [line.rstrip('\n') for line in f if line.strip() and not line.startswith('#')]


def read_cipher(name='telegram761.txt'):
    return letters(' '.join(data_lines(name)))


def read_key(name='key.txt'):
    return [int(x) for x in ' '.join(data_lines(name)).split()]


def write_result(name, lines):
    os.makedirs(path('results'), exist_ok=True)
    with open(path('results', name), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


class Model:
    def __init__(self, name='russian_trigrams.tsv'):
        self.count3 = {}
        count2 = [[0] * A for _ in range(A)]
        for line in data_lines(name):
            gram, n = line.split('\t')
            a, b, c = (INDEX[ch] for ch in gram)
            self.count3[(a * A + b) * A + c] = int(n)
            count2[a][b] += int(n)
        self.count2 = count2
        count1 = [sum(row) for row in count2]
        total = sum(count1)
        p1 = [(n + 1) / (total + A) for n in count1]
        # probability of b after a, and its logarithm; rare pairs lean on the frequency of b alone
        self.p2 = [[(count2[a][b] + 4 * p1[b]) / (count1[a] + 4) for b in range(A)] for a in range(A)]
        self.log2 = [[math.log(p) for p in row] for row in self.p2]
        self._log3 = {}

    def log3(self, a, b, c):
        """logarithm of the probability of c after a, b; rare trigrams lean on the pair b, c"""
        k = (a * A + b) * A + c
        v = self._log3.get(k)
        if v is None:
            v = math.log((self.count3.get(k, 0) + 4 * self.p2[b][c]) / (self.count2[a][b] + 4))
            self._log3[k] = v
        return v

    def score(self, text):
        """mean log-probability per trigram: nearer zero is more like Russian"""
        return sum(self.log3(text[i], text[i + 1], text[i + 2]) for i in range(len(text) - 2)) / (len(text) - 2)

    def pair_sum(self, text):
        """sum of the pair log-probabilities of a text; the quantity the search maximises"""
        return sum(self.log2[text[i]][text[i + 1]] for i in range(len(text) - 1))
