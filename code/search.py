"""Search for the key of a columnar transposition when only the cipher text is known.

For a given width the cipher text falls into that many strips, one for each column, in the order in which the clerk
copied the columns out. The search looks for the arrangement of the strips, left to right, that makes the rows read
most like Russian. It is a simulated annealing: swap two strips, move a block of neighbouring strips, or rotate the
whole row; keep every change for the better and, less and less often as the search cools, a change for the worse.

What makes this fast enough for plain Python is that the fit of an arrangement is a sum over neighbouring columns:
how well does this strip read when it stands directly to the left of that one? Each such sum is worked out once and
remembered. Because the last row is incomplete, a strip is one letter longer when it stands in one of the left-hand
columns, so the place where a strip begins in the cipher text depends on the arrangement. The sums are therefore
remembered by the starting places of the two strips.

With 558 letters the search finds a planted key at almost every start up to a width of about 31, at some starts at
36, and hardly ever above 40 (see controls.py). That is a limit of this search, not of the cipher.
"""
import math
import multiprocessing
import random

from model import Model
from transposition import decipher


class Search:
    def __init__(self, cipher, width, model):
        self.cipher = cipher
        self.width = width
        self.log2 = model.log2
        self.rows, self.extra = divmod(len(cipher), width)
        self.beside = {}      # (start of left strip, start of right strip, rows) -> sum of pair scores
        self.around = {}      # the same for the end of one row running on into the next

    def _sum(self, memo, s1, s2, m, down):
        k = (s1, s2, m)
        v = memo.get(k)
        if v is None:
            cipher, log2 = self.cipher, self.log2
            v = 0.0
            for i in range(m):
                v += log2[cipher[s1 + i]][cipher[s2 + i + down]]
            memo[k] = v
        return v

    def fit(self, key):
        """sum of the pair log-probabilities of the text that `key` gives (key[c] counted from 0 here)"""
        width, rows, extra = self.width, self.rows, self.extra
        longer = [0] * width
        for c in range(extra):
            longer[key[c]] = 1
        start = [0] * width
        pos = 0
        for strip in range(width):
            start[strip] = pos
            pos += rows + longer[strip]
        total = 0.0
        for c in range(width - 1):
            total += self._sum(self.beside, start[key[c]], start[key[c + 1]], rows + (1 if c + 1 < extra else 0), 0)
        if width > 1:
            total += self._sum(self.around, start[key[width - 1]], start[key[0]], rows if extra else rows - 1, 1)
        return total

    def anneal(self, rng, steps, hot=8.0, cold=1.0):
        width = self.width
        key = list(range(width))
        rng.shuffle(key)
        now = self.fit(key)
        best, best_key = now, key[:]
        temperature = hot
        cooling = (cold / hot) ** (1.0 / steps)
        for _ in range(steps):
            temperature *= cooling
            move = rng.random()
            if move < 0.4:                                   # swap two strips
                i, j = rng.randrange(width), rng.randrange(width)
                if i == j:
                    continue
                new = key[:]
                new[i], new[j] = new[j], new[i]
            elif move < 0.9:                                 # move a block of up to eight neighbouring strips
                i = rng.randrange(width)
                size = 1 + rng.randrange(min(width - 1, 8))
                if i + size > width:
                    continue
                rest = key[:i] + key[i + size:]
                j = rng.randrange(len(rest) + 1)
                new = rest[:j] + key[i:i + size] + rest[j:]
            else:                                            # rotate the row
                j = 1 + rng.randrange(width - 1)
                new = key[j:] + key[:j]
            then = self.fit(new)
            if then >= now or rng.random() < math.exp((then - now) / temperature):
                key, now = new, then
                if now > best:
                    best, best_key = now, key[:]
        return best, best_key


def solve(cipher, width, model, restarts=10, steps=200000, seed=1):
    """the best key found for one width, as (score, key as the clerk would write it, restarts that ended on it)"""
    if width == 1:
        return model.score(cipher), [1], restarts
    search = Search(cipher, width, model)
    runs = [search.anneal(random.Random('%d %d %d' % (seed, width, r)), steps) for r in range(restarts)]
    best, key = max(runs, key=lambda run: run[0])
    same = sum(1 for run in runs if run[1] == key)
    key = [k + 1 for k in key]
    plain = decipher(cipher, key)
    assert abs(best - model.pair_sum(plain)) < 1e-6
    return model.score(plain), key, same


_model = None


def _solve(task):
    global _model
    if _model is None:
        _model = Model()
    return solve(task[0], task[1], _model, *task[2:])


def solve_many(tasks):
    """solve() for each task (cipher, width, restarts, steps, seed), on all processor cores; results in the same order"""
    with multiprocessing.Pool() as pool:
        return pool.map(_solve, tasks, chunksize=1)
