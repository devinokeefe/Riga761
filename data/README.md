# Data

All the files are UTF-8 text. Lines beginning with `#` are comments that say what the file is and where it comes
from.

| file | what |
|---|---|
| `telegram761.txt` | the cipher text, transcribed from the scan: 558 letters, one line for each typed line, in groups as typed. The comment gives the heading and signature that stand around it on the sheet. |
| `doubtful_letters.tsv` | the six letters that are hard to make out on the scan, with the other possible reading |
| `key.txt` | the key, as the number over each of the 26 columns |
| `reading.txt` | the text as read, divided into words. Its letters, in order, are the 558 letters of the telegram with 23 corrected. |
| `emendations.tsv` | those 23 letters: where each one is in the text, on the sheet and in the cipher text, what the copy has and what is read |
| `telegram761_first_transcription.txt` | the first transcription, from which the key was originally found. It differs from `telegram761.txt` in 13 letters. |
| `telegram761_check_reading.txt` | a later reading of the scan, made without looking at `telegram761.txt` in order to check it. It agrees in all 558 letters, and its comment lists the 33 letters it was unsure of. |
| `russian_trigrams.tsv` | the language model: counts of three-letter sequences in Russian diplomatic prose of 1920-21 |
| `control_texts.txt` | six passages of 558 letters from the same kind of prose, used to test the search |

## Conventions

- Letters are counted from 1. In `emendations.tsv`, "place" is the place in the deciphered text and "cipher
  place" is the place in the cipher text as transcribed.
- The alphabet has 32 letters: абвгдежзийклмнопрстуфхцчшщъыьэюя. The telegram has no ё, and the model counts ё
  as е.
- In `reading.txt` the clerk's own marks are kept as words: х before and after a proper name, тчк for a full
  stop, зпт for a comma. The capital letters there are editorial.

## Where the telegram comes from

Warsaw, Centralne Archiwum Wojskowe (Wojskowe Biuro Historyczne), Oddział II Naczelnego Dowództwa Wojska
Polskiego, I.301.8.663, "Radiotelegramy zaszyfrowane nadesłane ze Stacji RTG.", part 1. The telegram is leaf 19,
which is page 21 of the PDF that the archive published:
<https://web.archive.org/web/20200703151708/https://wbh.wp.mil.pl/c/pages/atts/2020/6/I_301_8_663_1.pdf>
(139 MB). That page is reproduced in [images/telegram761.jpg](../images/telegram761.jpg).

## Where the language model comes from

*Документы внешней политики СССР*, vol. 3: 1 July 1920 to 18 March 1921 (Moscow, 1959). The volume is online at
<http://militera.lib.ru/docs/da/dvp/03/index.html>, and its text was converted from the Word file offered there.
Only the documents were used, without the preface, notes or indexes. Nos. 1-138 and 175-352 went into the
trigram table. The openings of nos. 143, 159, 160, 161, 162 and 163 became the control texts, so the table has
never seen the texts that the search is tested on. `code/build_model.py` is the program that did this.

The text is a machine reading of the printed book and has misreadings in it (и for н and the like). For counting
three-letter sequences that does not matter much. The control texts are given as they came, misreadings
included.
