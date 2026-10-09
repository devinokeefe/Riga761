"""How data/russian_trigrams.tsv and data/control_texts.txt were made. Not part of reproduce.py.

    python code/build_model.py path/to/dvp03.txt

The text is volume 3 of "Документы внешней политики СССР" (Moscow, 1959): Soviet diplomatic documents from 1 July
1920 to 18 March 1921. The volume is distributed as a Word file by militera.lib.ru; it was converted to plain text
(UTF-8) and is not included here. Only the documents are used, not the preface, the editors' notes or the indexes.
Documents 139 to 174 are left out of the table, and the control texts are taken from them, so that the model has
not seen the texts on which the search is tested.
"""
import re
import sys

from model import ALPHABET, letters, path, string

FIRST = '1. Нота Председателя Совета Народных Комиссаров'       # heading of document 1
NOTES = '1 В августе 1918 г. правительство Финляндии'          # the first of the editors' notes
HELD_FROM = '139. Нота Народного Комиссара Иностранных Дел РСФСР Министру Иностранных Дел Франции'
HELD_TO = '175. Нота Народного Комиссара Иностранных Дел РСФСР Министру Иностранных Дел Великобритании'
CONTROLS = [143, 159, 160, 161, 162, 163]      # documents whose first 558 letters serve as control texts
LENGTH = 558


def main():
    raw = open(sys.argv[1], encoding='utf-8').read()
    first, notes = raw.index(FIRST), raw.index(NOTES)
    held_from, held_to = raw.index(HELD_FROM), raw.index(HELD_TO)
    assert first < held_from < held_to < notes

    count = {}
    for part in (raw[first:held_from], raw[held_to:notes]):
        text = letters(part)
        for i in range(len(text) - 2):
            gram = string(text[i:i + 3])
            count[gram] = count.get(gram, 0) + 1
    with open(path('data', 'russian_trigrams.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Trigram counts of Russian diplomatic prose of 1920-21: how often each run of three letters occurs.\n'
                '# From the documents of "Документы внешней политики СССР", vol. 3 (Moscow, 1959), nos. 1-138 and\n'
                '# 175-352; letters only, in the %d-letter alphabet %s (ё counted as е);\n'
                '# %d trigrams in all, %d different. Made by code/build_model.py. The text is a machine reading of\n'
                '# the printed volume and has its misreadings.\n'
                % (len(ALPHABET), ALPHABET, sum(count.values()), len(count)))
        for gram in sorted(count):
            f.write('%s\t%d\n' % (gram, count[gram]))
    print('%d trigrams, %d different' % (sum(count.values()), len(count)))

    held = raw[held_from:held_to]
    with open(path('data', 'control_texts.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Control texts: the first %d letters (after the date line) of six documents of "Документы внешней\n'
                '# политики СССР", vol. 3, that were left out of the trigram table. One text per line, after a comment\n'
                '# line with the number and heading of the document. Made by code/build_model.py.\n' % LENGTH)
        for number in CONTROLS:
            m = re.search(r'\n\s*%d\. ([^\n]+)\n' % number, held)
            date_line, body = held[m.end():].split('\n', 1)
            body = letters(body)[:LENGTH]
            assert len(body) == LENGTH
            f.write('# %d. %s\n%s\n' % (number, m.group(1).strip(), string(body)))
            print(number, m.group(1).strip()[:90])


if __name__ == '__main__':
    main()
