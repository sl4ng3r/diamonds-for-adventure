# V63 – Tiefe Höhlenfunde mit einem Zusatzversuch

V63 setzt höchstens einen zusätzlichen Startpunkt pro Chunk auf Y=−54 bis −52. Der Stellwert für den Platzierungsversuch beträgt 65. Vier Blöcke Suchweite begrenzen diese Funde auf Y=−48 oder tiefer. V62 setzte zwei Startpunkte und erzeugte im Gebiet 920027 sechs zusätzliche Funde bei acht Vanilla-Fundstellen. Diese Häufung war der Grund für die Reduktion.

Der V61-Filter erhält freiliegende Adern vollständig und kann eingeschlossene Adern über Chunkgrenzen prüfen, wenn alle betroffenen Chunks geladen und markiert sind. Andere Höhlenregeln, die geplante Obergrenze +30 und die Ozeanregel bis +35 entsprechen V60.

Lokales Spieltestpaket: [Cave Diamonds 0.1.16](../../dist/cave-diamonds-v0.1.16.mcpack). Erzeugung mit `python3 -m tools.build_v63 --package`.

## Ergebnis

Bedrock Dedicated Server 1.26.61.1, sechs Gebiete mit je 8×8 Chunks. Vier davon waren die direkten Vergleichsgebiete von V60. Das fünfte (920027) war vorher für V62 ausgewertet und hat die Wahl eines Zusatzversuchs beeinflusst. Das sechste (920039) war für die Einstellung von V61 bis V63 unbenutzt. Vanilla und Kandidat wurden an denselben Orten verglichen.

| Kennzahl | V60 in denselben 256 Chunks | V63 in denselben 256 Chunks | V63 in allen 384 Chunks |
| --- | ---: | ---: | ---: |
| Luftberührte Fundstellen bis Y=+16 | 27/26 (+3,8 %) | 29/26 (+11,5 %) | 52/44 (+18,2 %) |
| Luftberührte Fundstellen auf Y=−64 bis −48 | 2/2 | 4/2 | 10/3 |
| Luftberührte Fundstellen auf Y=−47 bis −32 | 8/8 | 8/8 | 13/13 |
| Eingeschlossene Erzblöcke auf Y=−57 | 40/107 (37,4 %) | 14/107 (13,1 %) | 21/162 (13,0 %) |
| Eingeschlossene Erzblöcke auf Y=−59 bis −55 | 184/538 (34,2 %) | 63/538 (11,7 %) | 99/799 (12,4 %) |
| Eingeschlossene Erzblöcke auf Y=−54 bis −20 | 749/2.828 (26,5 %) | 481/2.828 (17,0 %) | 646/3.762 (17,2 %) |
| Eingeschlossene Erzblöcke auf Y=−19 bis +16 | 383/866 (44,2 %) | 222/866 (25,6 %) | 285/1.175 (24,3 %) |

Die Spalten zeigen jeweils Kandidat/Vanilla. Im ungeprüften Gebiet 920039 wurden bis +16 zwölf statt zehn luftberührte Gruppen gefunden. Auf Y=−57 blieben 4/28 eingeschlossene Erzblöcke (14,3 %), im oberen Band 45/238 (18,9 %). Gebiet 920027 sank von den 14 V62-Fundstellen auf 11 (Vanilla acht). Die Zusatzfunde häufen sich im tiefsten Band. Die Gesamtzahl der Fundstellen steigt über die gemessenen Höhenbänder trotzdem nicht durchgehend in Richtung Tiefe. Im frischen Gebiet gab es einen luftberührten Fund auf Y=+19. Funde nahe +30 oder +35 wurden in dieser Serie nicht beobachtet.

Alle 84 Adern mit Luft- oder Flüssigkeitskontakt blieben vollständig erhalten, davon 39 mit mehreren Blöcken. Die 49 luftberührten Vanilla-Erzpositionen blieben alle erhalten. Im gescannten Gebiet wurden 1.472 ganze eingeschlossene Gruppen entfernt, 116 davon über Chunkgrenzen. Keine beobachtete Gruppe wurde geteilt. Die Weltdateien enthielten nach dem Speichern dieselben Erzpositionen wie die Abschlussscans, und an allen 768 Markerpositionen lag wieder Grundgestein.

Die Ausdünnung wurde für die Messung direkt im Server ausgelöst. Spielerbetrieb und Realm-Leistung wurden damit nicht geprüft. Alle 197 automatisierten Tests bestanden. Rohdaten, Paketprüfsumme und die Ergebnisse pro Gebiet stehen unter `data/research/v63-balance-2026-11-22/`.
