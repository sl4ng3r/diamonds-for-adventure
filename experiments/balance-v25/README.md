# V25 – Adergrößen und Höhlenfundstellen

V25 ist ein nicht freigegebener Bedrock-Behavior-Pack-Teststand auf Basis von V24. Gegenüber V24 wurde ausschließlich die gewichtete Auswahl der versuchten Höhlenerzgröße geändert:

| versuchte Größe | Gewicht |
| ---: | ---: |
| 1 | 1 |
| 2 | 2 |
| 3 | 35 |
| 4 | 52 |
| 5 | 10 |

Richtungswahl, Höhenregeln, Platzierungshäufigkeit und die tiefe Zusatzregel bleiben V24 entsprechend. Die tatsächlich sichtbaren Gruppen können wegen Hohlraumform, Chunk-Grenzen, Aggregat-Reihenfolge und zusammenfallenden Versuchen von diesen Gewichten abweichen. Der Pack-Hash lautet `5b4e7b84e8bf5a35b21d3db0544ed0017f83f2e99822c9459694242f0ff21206`.

## Kalibrierung

Die 20 kleinen Referenzgebiete ergaben 32 gegenüber 23 Vanilla-Luftkontaktgruppen (139,1 %), 31 gegenüber 118 eingeschlossene Erze auf Y=-57 (26,3 %) und 202 gegenüber 1.103 Tunnelkontakte (18,3 %). Die gemessenen Gruppengrößen 1/2/3/4/5 waren 1/8/16/6/1.

Die 15 großen V24-Gebiete wurden nur zur Kalibrierung wiederverwendet, nicht als unabhängiger Nachweis: 1.729 gegenüber 1.630 Gruppen (106,1 %), 906 gegenüber 6.564 Erze auf Y=-57 (13,8 %) und 7.968 gegenüber 52.810 Tunnelkontakte (15,1 %). Gruppengrößen 1/2/3/4/5/7: 92/453/754/382/42/6.

## Unabhängiger Holdout

Der Holdoutplan `reference/balance-holdout-plan-2026-11-06-v25.json` wurde vor der Messung festgelegt. Er umfasst 15 neue Seeds mit jeweils 32×32 Chunks. Vanilla wurde zuerst unter `reference/balance-holdout-v25-1.26.61.1-2026-11-06.json` eingefroren; V25 wurde anschließend in denselben Gebieten gemessen. Ergebnisse liegen atomar unter `holdout-results/`.

| Kennzahl | Vanilla | V25 | V25/Vanilla |
| --- | ---: | ---: | ---: |
| Luftkontakt-Fundstellen | 1.509 | 1.629 | **108,0 %** |
| eingeschlossene Erze Y=-57 | 6.683 | 1.045 | **15,6 %** |
| eingeschlossene Erze Y=-59..-55 | 33.087 | 4.977 | **15,0 %** |
| überlappende Tunnelkontakte | 52.884 | 8.107 | **15,3 %** |

Die gebietsweise Bootstrap-Auswertung in `holdout-uncertainty.json` behandelt vollständige Seeds als Einheiten. Die 2,5–97,5-%-Intervalle betragen 99,3–117,0 % für Fundstellen, 14,0–17,4 % für Y=-57 und 14,5–16,1 % für das Tunnelmodell.

Die Holdout-Gruppengrößen 1/2/3/4/5/6 betragen 113/394/722/364/34/2. Dreier- und Vierergruppen bilden 1.086 von 1.629 Gruppen (66,7 %). Einergruppen sind deutlich reduziert; Fünfergruppen bleiben selten. Siebenergruppen wurden in diesem Holdout nicht gemessen. Luftkontakt ist weiterhin nur eine technische Näherung und beweist weder Erreichbarkeit noch vollständige natürliche Adern.

## Kontrolltests

- Boden, Decke und Wand wurden im kontrollierten Hohlraum jeweils in 3/3 Versuchen platziert.
- Die simulierte Entfernung eines Erzes per `setblock air` blieb nach Neustart entfernt; dies ist kein echter Spielerabbau.
- Die ausgewählte Erzpositionsprobe fand für die geprüften anderen Erztypen keine V25-Abweichung gegenüber Vanilla; sie ist keine vollständige Block- oder Weltprüfung.
- Höhen, Biome, Grenzgruppen und Seed-Streuung sind in den gespeicherten Einzelresultaten enthalten. Im Holdout wurden keine V25-Erze auf Y=17..40 gemessen.

## Reproduktion

```bash
python3 -m unittest discover -s tests -v
python3 -m tools.balance_batch status --pack experiments/balance-v25/behavior_pack --results experiments/balance-v25/holdout-results --reference reference/balance-holdout-v25-1.26.61.1-2026-11-06.json
python3 -m tools.balance_profiles --results experiments/balance-v25/holdout-results --reference reference/balance-holdout-v25-1.26.61.1-2026-11-06.json
```

V25 bleibt eine lokal geprüfte Testversion. Echte Spieler-Spielzeitvergleiche, Werkzeug-/Verzauberungs-/Explosionsfälle, Mehrspielerleistung, Versionsabgleich sowie Test-Realm- und Konsolenprüfungen stehen noch aus. Es darf daraus noch kein Produktions-`.mcpack` oder Realm-Einsatz abgeleitet werden.
