# The text

## The sheet

The telegram survives as one typed page, a copy that the Polish Cipher Bureau made from what its radio operators
had taken down. It is in Warsaw, Centralne Archiwum Wojskowe, Oddział II NDWP, I.301.8.663, part 1, on page 21 of
the archive's PDF ([picture](../images/telegram761.jpg)). The page is headed "I." and has the cipher text in
groups of five letters, with a heading and a signature in plain Russian:

```
                                        I.
Изъ  Риги М.Д. 267 5/II 10-15 Тов.Чичерину.Перекопъ одинъ
ноль пять восемь стопъ нодве рдвов еафот усьхд неррм пнйтп
итчиа патих очоко ласск илккр иаосч дденр иивок гмчнг
ееясо оустр ехмди обзнс масоз еипан ажмюа ивутв квсем
юкуту уымад иихрч иемйо ижочщ сбвад илчор рувык ваахе
локяб хтода ниенд беарк юносч нибев асхыз оояаы онттс
ггвль акзеф тотом инедч етщси окгаи йепзт нонув тлели
мента леиха усррз зррив онфиа схроз юмпак чеыла оссаа
дхвог рсндв тнхап отолх упвви иеяоп стхтс закхр веснр
ьлчаб авоеу риучс бармр ооури херчо ааеуо гонре ьншкв
лоаиы влнхь клаез зыоов антои иаото бквто разуз щщдхт
рраок нотию ежхдз седгл неаей лкзчи обыкв еаяпй оеюал
топрх гичст оохшо угрьт ьехяд шхасв илдво линиж аткбх
ьпдищ чвлсы мчате аииар саево внхан чоа 50558 Іоффе
4/II 1921 года № 761.
```

The heading reads: from Riga, M.D. 267, 5 February, 10:15, to Comrade Chicherin, "Perekop", one zero five eight,
stop. The signature is 50558, Joffe, 4 February 1921, no. 761. Joffe dated the telegram on the 4th, then, and it
went out on the radio the next morning.

Some notes on the heading:

- М.Д. stands for мирная делегация, the peace delegation, as the office where the telegram was handed in, and
  267 is its serial number there. Another telegram in the file, of 24 January, is headed "М.Д. № 189 165 сл.",
  where 165 сл. is the word count. The delegation's telegrams that have been printed from the Russian archives
  are headed in the same way, and their numbers fit the sequence: "Из Риги мир дел № 4" on 2 January 1921 and
  "Мир. Дел нр. 54" on 7 January.
- № 761 is the delegation's own outgoing number. A telegram of 9 February in the same printed collection ends
  "нр 784". (*Советско-польские отношения в 1918-1945 гг.*, vol. 1, Moscow 2017, pp. 356, 359 and 365-366.)
- Перекоп is the name of the cipher, or of its key. Perekop is the isthmus leading into the Crimea, which the
  Red Army had stormed in November 1920. The other Riga telegrams in the file are marked Победа ("victory") and
  are in figures.
- The plain-language parts are in the old spelling (Изъ, одинъ, Іоффе). The cipher text is in the new, with no ъ
  at the ends of words and no ѣ or і.

The cipher text has 558 letters. Six of them are hard to read on the scan. In each case the word the letter
belongs to is clear whichever way it is taken.

| cipher place | line, group | read as | could be | on the scan | falls in |
|---|---|---|---|---|---|
| 31 | 2, 1 | и | н | faint; the diagonal stroke shows only under strong magnification | области |
| 74 | 2, 9 | н | и | smudged | войны |
| 94 | 3, 4 | н | и | heavily inked | инспектором |
| 344 | 8, 9 | н | и | pen strokes across the letter | нужно |
| 383 | 9, 8 | н | и | pen strokes across the letter | согласны |
| 500 | 12, 4 | т | | a horizontal stroke runs through the letter | работу |

To check the transcription, the scan was read once more from enlarged strips, one typed line at a time, without
looking at the transcription. The two agree in all 558 letters. The check reading was unsure of 33 letters,
including the six above, and nearly all of them are a choice between и and н. None of the 33 is one of the
letters corrected further down ([data/telegram761_check_reading.txt](../data/telegram761_check_reading.txt)).

## Deciphered

The cipher clerk wrote the message in rows of 26 letters under the key and copied the columns out in the order
of the key numbers. Writing the columns back in under their numbers gives the sheet he worked from:

```
     9  8 23  1 13 17 11 24  6 21  7  4 10 15 26 14 18 22 25 12 19  3 20  5 16  2

 1   д  л  я  н  а  р  к  о  м  з  д  р  а  в  а  х  о  е  и  а  ш  к  о  х  в  р
 2   а  ч  п  о  л  ь  з  у  ю  щ  и  и  с  о  т  р  у  д  н  и  к  о  в  м  и  р
 3   н  о  й  д  е  л  е  г  а  щ  и  и  х  г  е  о  р  г  и  й  в  л  а  д  и  м
 4   и  р  о  в  и  ч  ф  р  и  д  х  в  ы  р  а  з  и  л  ж  е  л  а  н  и  е  п
 5   е  р  е  е  х  а  т  ь  в  х  р  о  з  с  и  ю  х  н  а  п  о  с  т  о  я  н
 6   н  у  ю  р  а  б  о  т  у  т  ч  к  о  н  и  м  е  е  т  з  а  с  о  б  о  й
 7   д  в  а  д  у  а  т  ь  т  р  и  г  о  д  а  п  р  а  к  т  и  к  и  з  п  т
 8   б  ы  л  в  с  в  о  е  в  р  е  м  я  в  р  а  ч  е  б  н  ы  и  и  н  с  п
 9   е  к  т  о  р  о  м  х  к  а  м  ч  а  т  с  к  о  й  х  о  в  л  а  с  т  и
10   а  в  о  в  р  е  и  я  в  о  й  н  ы  н  а  ч  а  л  ь  н  л  к  о  м  х  т
11   р  а  п  е  з  у  н  д  с  к  о  г  о  х  е  е  а  к  п  у  н  к  т  а  т  ч
12   к  а  р  а  з  р  е  ш  е  н  и  е  н  а  в  ы  е  з  д  в  х  р  о  с  с  и
13   ю  х  х  ф  р  и  д  х  м  о  ж  е  т  п  о  л  у  ч  и  т  ь  и  б  о  з  а
14   н  е  г  о  р  у  ч  а  ю  т  о  я  т  о  в  а  о  и  щ  л  к  а  к  з  а  п
15   о  л  и  т  и  ч  е  с  к  и  ч  с  с  т  н  о  г  о  ч  е  л  о  в  е  к  а
16   с  о  ч  у  в  с  т  в  у  ю  щ  о  г  о  х  с  о  б  в  л  а  с  т  и  х  т
17   ч  к  с  с  о  б  щ  и  т  е  с  о  г  л  а  с  н  ы  л  и  е  ч  о  п  р  и
18   н  я  т  ь  н  а  с  л  у  ж  б  у  в  х  н  а  р  к  с  м  з  д  р  а  в  х
19   и  б  о  х  ф  р  и  д  у  х  в  с  л  у  ч  а  е  в  ы  е  з  д  а  н  е  о
20   б  х  о  д  и  м  о  в  ы  д  а  т  ь  п  о  д  ь  е  м  н  ы  е  з  а  с  ч
21   е  т  х  н  а  р  к  о  м  з  д  р  а  в  а  х  н  а  ч  т  о  н  у  ж  н  о
22   в  о  ш  е  с  о  г  л  а  с  и  е
```

The column under the 1 reads н о д в е р д в о в ..., which is how the telegram begins. The last row has only
12 letters, so the first 12 columns are a letter longer than the other 14.

## The reading

Here is the text divided into words, with 23 letters corrected (see the next section). The clerk's own marks are
left in: х before and after a proper name, тчк for a full stop, зпт for a comma.

> для наркомздрава х семашко х врач пользующий сотрудников мирной делегации х георгий владимирович фрид х выразил
> желание переехать в х россию х на постоянную работу тчк он имеет за собой двадцать три года практики зпт был в
> свое время врачебным инспектором х камчатской х области а во время войны начальником х трапезундского х
> эвакпункта тчк а разрешение на выезд в х россию х х фрид х может получить ибо за него ручаются товарищи как за
> политически честного человека сочувствующего х соввласти х тчк сообщите согласны ли его принять на службу в х
> наркомздрав х ибо х фриду х в случае выезда необходимо выдать подъемные за счет х наркомздрава х на что нужно
> ваше согласие

With capitals and punctuation:

> Для Наркомздрава, Семашко. Врач, пользующий сотрудников мирной делегации, Георгий Владимирович Фрид выразил
> желание переехать в Россию на постоянную работу. Он имеет за собой двадцать три года практики, был в свое время
> врачебным инспектором Камчатской области, а во время войны начальником Трапезундского эвакпункта. А разрешение
> на выезд в Россию Фрид может получить, ибо за него ручаются товарищи как за политически честного человека,
> сочувствующего Соввласти. Сообщите, согласны ли его принять на службу в Наркомздрав, ибо Фриду в случае выезда
> необходимо выдать подъемные за счет Наркомздрава, на что нужно Ваше согласие.

In English:

> For the People's Commissariat of Health, Semashko. The doctor who attends the staff of the peace delegation,
> Georgy Vladimirovich Frid, has expressed a wish to move to Russia for permanent work. He has twenty-three years
> of practice behind him, was at one time medical inspector of the Kamchatka region and, during the war, head of
> the Trebizond evacuation point. Frid can get permission to leave for Russia, since comrades vouch for him as a
> politically honest man who sympathises with Soviet power. Let us know whether you agree to take him into the
> service of the Commissariat of Health, since if he leaves Frid must be paid a removal allowance at the
> Commissariat's expense, and for that your consent is needed.

Some notes on the wording:

- Наркомздрав is the People's Commissariat of Health, and Nikolai Semashko was its commissar. The telegram is
  sent to Chicherin's commissariat to be passed on to him.
- пользующий is an old word for "treating", as in пользовать больного, to attend a patient.
- A врачебный инспектор was the head of the government medical service in a province or region before 1917.
- эвакпункт is short for эвакуационный пункт. In the war of 1914-18 this was an army medical establishment that
  took in the sick and wounded and sent them on to hospitals in the rear. Trebizond, on the Black Sea coast of
  Turkey, was in Russian hands from April 1916 to early 1918.
- подъемные is the lump sum paid to someone taking up a post, to cover the cost of moving.
- In "в х россию х х фрид х" the first two х enclose Россию and the next two enclose Фрид.
- The telegram does not say where Frid was living or what his position was. It reads as though he was not in
  Soviet service, since he needs a permit to go to Russia, comrades have to vouch for him, and the Commissariat
  has to agree to take him.

## The 23 corrections

Twenty-three letters of the deciphered text are wrong. They fall in 20 words, none of which is in any doubt. All
23 letters are clear on the scan, so these are mistakes on the sheet itself and not misreadings of it.

| place | as typed | read as | letter |
|---|---|---|---|
| 17 | оеиашко | семашко | о for с, и for м |
| 29 | пользующии | пользующий | и for й |
| 56 | делегащии | делегации | щ for ц |
| 115 | розсию | россию | з for с |
| 157 | двадуать | двадцать | у for ц |
| 196 | врачебныи | врачебным | и for м |
| 228 | овласти | области | в for б |
| 238 | вреия | время | и for м |
| 248 | начальнлком | начальником | л for и |
| 275 | ееакпункта | эвакпункта | е for э, е for в |
| 343 | ручаютоя | ручаются | о for с |
| 351 | товаоищл | товарищи | о for р, л for и |
| 375 | чсстного | честного | с for е |
| 391 | сочувствующого | сочувствующего | о for е |
| 406 | собвласти | соввласти | б for в |
| 419 | ссобщите | сообщите | с for о |
| 437 | ечо | его | ч for г |
| 457 | нарксмздрав | наркомздрав | с for о |
| 508 | подьемные | подъемные | ь for ъ |
| 547 | воше | ваше | о for а |

"Place" is where the word begins in the deciphered text, counting letters from 1.
[data/emendations.tsv](../data/emendations.tsv) gives each of the 23 letters with its row and column on the sheet
and its place in the cipher text.

Most of these are pairs of letters that look alike in Russian handwriting: и and м, о and с and е, ч and г, щ
and ц, л and и. That would fit a typist copying from a radio operator's pencilled log, although nothing on the
sheet shows who made them. Two may not be mistakes at all. The ь for ъ in подъемные and the и for й in
пользующий could simply be how the Soviet clerk spelled the words.

## Not explained

"One zero five eight" comes before the cipher text and 50558 after it. 558 is the number of letters, but what
1058 and the 50 in front of 558 mean is not known.

The key phrase, if there was one, has not been found (see [METHOD.md](METHOD.md)).
