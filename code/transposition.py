"""Columnar transposition, the cipher of telegram no. 761.

The clerk writes the text in rows under a row of key numbers and then copies the columns out one after another,
beginning with the column numbered 1. Nothing is added to fill the last row, so the columns on the left are one
letter longer than those on the right.

A key is the row of numbers as the clerk would have it on paper: key[c] is the number over column c (counted from the
left, from 0), and the numbers 1 to len(key) each occur once. Texts are lists (of letters or of numbers).
"""


def column_lengths(n, width):
    """lengths of the columns, left to right, when n letters are written in rows of `width`"""
    rows, extra = divmod(n, width)
    return [rows + (1 if c < extra else 0) for c in range(width)]


def reading_order(key):
    """the columns in the order in which they are copied out"""
    return sorted(range(len(key)), key=lambda c: key[c])


def encipher(plain, key):
    width = len(key)
    cipher = []
    for c in reading_order(key):
        cipher.extend(plain[c::width])
    return cipher


def decipher(cipher, key):
    width = len(key)
    lengths = column_lengths(len(cipher), width)
    plain = [None] * len(cipher)
    start = 0
    for c in reading_order(key):
        plain[c::width] = cipher[start:start + lengths[c]]
        start += lengths[c]
    return plain


def rows(plain, width):
    """the text as it stood on the clerk's sheet, one string or list per row"""
    return [plain[i:i + width] for i in range(0, len(plain), width)]


def check_key(key):
    if sorted(key) != list(range(1, len(key) + 1)):
        raise ValueError('a key must hold each of the numbers 1 to %d once' % len(key))
    return key
