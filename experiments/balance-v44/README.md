# V44 – Vanilla-Höhlenadern mit sparsamem Zuschlag

Der Spieler fand V29 in einer großen Höhle um Y=−40 zu reichhaltig. Die Ursache lag nicht bloß in der Größe der Adern: Im untersuchten V19-Referenzgebiet hatte V39 trotz passender globaler Kalibrierung **29 statt 10 getrennte Luftkontaktgruppen** im Höhenband Y=−47..−32. V38 ohne schmale Zusatzregel hatte dort ebenfalls 29, V40 mit kürzerer tiefer Oberflächensuche noch 27. Die eigenen Höhlenregeln ersetzten die natürliche Vanilla-Verteilung durch Oberflächentreffer.

V44 baut stattdessen auf V43 auf: Normale und große Vanilla-Diamantfeatures bleiben aktiv, die vergrabene Vanilla-Quelle wird unterdrückt, und ein später `final_pass`-Schritt ersetzt geeignete vollständig eingeschlossene Erze durch Stein oder Tiefenschiefer. Eine tiefe und eine mittlere eigene Höhlenregel ergänzen nur wenige Funde (`scatter_chance` 10 und 15 als Engine-Werte, nicht als bewiesene Prozentwahrscheinlichkeiten). Die zwei zusätzlichen tiefen Regeln entfallen. Die obere Regel mit geplantem Maximum Y=+30 bleibt bytegleich zu V37. V44 ist noch ein Forschungspack.

Im ersten gezielt gewählten 16×16-Chunk-Gegenfall (Seed 919001):

| Messwert | Vanilla | V44 |
| --- | ---: | ---: |
| Getrennte Luftkontaktgruppen, Y=−64..40 | 38 | 43 (+13,2 %) |
| Getrennte Luftkontaktgruppen, Y=−47..−32 | 10 | 11 (+10 %) |
| Luftberührte Erzblöcke | 40 | 45; alle 40 Vanilla-Positionen erhalten |
| Höchste Gruppenzahl pro 64×64-Kachel im kritischen Band | 2 | 2 |
| Vergrabene Erze auf Y=−57 | 111 | 16 (14,4 %) |
| Kontakte im überlappenden Tunnelmodell | 919 | 127 (13,8 %) |

Beide bereits früher verwendeten Referenzserien sind vollständig (zwölf Gebiete, 3.072 Chunks): **354/308 = 114,9 %** luftberührte Gruppen insgesamt; V19-Serie **188/164 = 114,6 %**, V24-Serie **166/144 = 115,3 %**. Im für den Spieler auffälligen Band Y=−47..−32 sind es **108/100 = 108 %**. Die höchste Gruppenzahl pro 64×64-Kachel in diesem Band ist für Vanilla und V44 jeweils vier. Alle **342 luftberührten Vanilla-Erzblöcke** blieben an denselben Positionen; 53 neue Luftkontaktblöcke kamen hinzu. Auf Y=−57 blieben **225/1.334 = 16,9 %** vergrabene Erze; das überlappende Tunnelmodell ergab **1.808/10.823 = 16,7 %** Kontakte. Der gebietsweise Bootstrap-Bereich für die Gruppenquote ist 111,7–117,8 %. Diese Serien dienten schon früheren Varianten und sind **keine unberührten Holdouts**.

Im Höhenband −15..−1 liegt die Gruppenquote bei 56/46 = 121,7 %, in 0..16 bei 19/14 = 135,7 %; die zweite Basis ist klein. Oberhalb +16 wurden zehn Erzblöcke bis maximal +24 gemessen. Die obere Regel plant Startpunkte bis +30, aber Funde nahe +30 sind nicht nachgewiesen. Die lokale Kachelmetrik zeigt eine begrenzte räumliche Häufung, kann die Zahl in einer tatsächlich zusammenhängenden großen Höhle aber nicht messen. Ergebnisse und Prüfsummen: `combined-summary.json`, `combined-spatial-summary.json`, `calibration-summary.json` und die beiden Pläne.

Eine isolierte Abbauprobe in Gebiet 0 entfernte ein luftberührtes Erz per `setblock air`. Nach Serverneustart war es weiter entfernt; im gemessenen geänderten Chunk und den übrigen untersuchten Chunks gab es keine weiteren Erzpositionsänderungen (`verification/mining-00.json`). Dies simuliert keinen echten Spielerabbau oder Drops.

Eine Kachel ist keine zusammenhängende oder zugängliche Höhle. Die erste Messung ist gezielt auf einen zuvor gescheiterten Seed gewählt, keine unabhängige Bestätigung. Die Rohscans liegen lokal unter `data/research/` und werden nicht committed. Die beiden Pläne frieren Pack, Referenz, Seed und Chunkbereiche per Prüfsumme ein:

```sh
python3 -m tools.balance_followup status --plan experiments/balance-v44/secondary-plan.json
python3 -m tools.cave_spatial_compare --plan experiments/balance-v44/secondary-plan.json
python3 -m tools.balance_followup status --plan experiments/balance-v44/calibration-plan.json
```

Aus der isolierten Servermessung folgen weder Spielertrag noch Erreichbarkeit, Realm-/Konsolenkompatibilität, alte-Welt-Sicherheit oder Mehrspielerleistung. Die feste Paketversion liegt gemäß Nutzerentscheidung unter `dist/cave-diamonds-v0.1.6.mcpack`; sie ist noch kein praktischer Spieltest.
