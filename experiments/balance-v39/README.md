# V39 – räumlich kalibrierte Höhlenfundstellen

Der Spieler fand V29 in einer großen Höhle um Y=−40 zu reichhaltig. Ziel sind 10–15 % mehr getrennte Erzgruppen mit mindestens einem direkt luftberührten Block gegenüber Vanilla, ohne eine Häufung um −40. Ein oder mehrere sichtbare Blöcke derselben Gruppe zählen als eine Fundstelle. Luftkontakt ist nur ein Messproxy für Sichtbarkeit und Erreichbarkeit.

V35 und V36 untersuchten `minecraft:ore_feature` für natürlichere Adern; V35 platzierte in kontrollierten Oberflächentests 0/9 Erze direkt an der Höhlenfläche, V36 mit Oberflächenanker 9/9, aber im ersten natürlichen Gebiet nur luftberührte Einzelgruppen. V37 bettet bei Boden und Decke weitere Aderblöcke hinter dem luftberührten Anker ein. V38 entfernte die schmale tiefe Zusatzregel ganz; V39 reduziert allein deren `scatter_chance` von 40 auf 30. Der Bedrock-Zahlenwert wird nicht als exakte Wahrscheinlichkeit interpretiert. Die obere Regel mit geplantem Maximum Y=+30 und die vergrabenen Regeln bleiben bytegleich zu V37.

| Variante | Luftkontaktgruppen, sechs wiederverwendete V24-Gebiete | Gruppen Y=−47..−32 | Direkt luftberührte Blöcke Y=−47..−32 |
| --- | ---: | ---: | ---: |
| Vanilla | 144 | 48 | 54 |
| V37 | 165 (114,6 %) | 57 (118,8 %) | 60 |
| V38 | 145 (100,7 %) | 45 (93,8 %) | 47 |
| V39 | 161 (111,8 %) | 55 (114,6 %) | 58 |

Die höchste Zahl von Gruppen im kritischen Höhenband pro 64×64-Block-Teilgebiet beträgt in **diesen sechs Gebieten** bei V39 und Vanilla je vier. Eine solche Kachel ist **keine** zusammenhängende Höhle. V39 hatte 119/674 (17,7 %) vergrabene Erzblöcke auf Y=−57 und 903/5225 (17,3 %) Kontakte im überlappenden Tunnelmodell. Über Y=+16 wurden zehn Erzblöcke bis Y=+24 gemessen; Y=+30 ist als mögliche Obergrenze konstruiert, aber nicht beobachtet. Die Gebiets-Bootstrap-Spanne der gesamten Fundstellenquote ist 87,2–140,0 %. Diese früher verwendeten Gebiete sind eine Kalibrierung, keine unabhängige Bestätigung.

**Gegenbefund aus der zweiten Referenzserie:** Im ersten V19-Gebiet entstanden im Band Y=−47..−32 **29 statt 10** Vanilla-Fundstellen; in einer 64×64-Kachel fünf statt null. Der restliche V39-Lauf wurde daraufhin gestoppt. V39 ist wegen dieser lokalen Häufung verworfen, auch wenn die erste Gesamtquote passt. V38 ohne die schmale tiefe Regel hatte im selben Gebiet ebenfalls 29 statt 10 Fundstellen; diese Regel ist dort nicht die Hauptursache. V40 mit halbiertem Suchradius der tiefen Regeln hatte noch 27 statt 10 Gruppen. V41 prüft deshalb einen Ansatz, der Vanilla-Normaladern erhält und zunächst auf unsere regulären Höhlenregeln verzichtet.

Reproduzieren, ohne Vanilla neu zu scannen:

```sh
python3 -m tools.balance_followup status --plan experiments/balance-v39/calibration-plan.json
python3 -m tools.cave_spatial_compare --plan experiments/balance-v39/calibration-plan.json
```

Die gespeicherten Resultate prüfen Pack- und Referenzhash, Seed und Chunkbereich. Rohscans und Testwelten liegen lokal unter `data/research/` und werden nicht committed. Spielertrag, tatsächliche Höhlenzugänglichkeit, alte Welten, Realm und Konsolen bleiben praktische Prüfungen. V39 ist nicht freigegeben; `dist/` bleibt unverändert.
