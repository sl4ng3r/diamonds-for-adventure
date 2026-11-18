# V51 – Vanilla-ähnliche Grabfunde oberhalb −20

V44 (Paket 0.1.6) ließ zwischen Y=−19 und +16 nur 19,4 % der eingeschlossenen Vanilla-Erzblöcke übrig. Der Nutzer möchte dort weiterhin gelegentliche Grabfunde ungefähr wie in Vanilla und die Ausdünnung bis einschließlich Y=−20 begrenzen. V51 bewahrt V44s sichtbare Höhlenregeln, die geplante obere Reichweite +30 und die tiefe Reduktion. Die ursprüngliche vergrabene Vanilla-Quelle bleibt unterdrückt; stattdessen erzeugt eine eigene Regel nur oberhalb −20 vergrabene Adern. Ihre Positionen sind deshalb nicht identisch mit Vanilla. V45–V50 waren Vorversuche; Einzelwerte und Gründe stehen in `experiments/balance-v50/README.md`.

V51 senkt gegenüber V50 nur den oberen `scatter_chance`-Engine-Wert von 50 auf 45. V50 hatte in sechs zuvor verwendeten V24-Referenzgebieten zwischen −19 und +16 6.017/5.365 = 112,2 % eingeschlossene Blöcke und 2.361/2.159 = 109,4 % getrennte eingeschlossene Gruppen. Das war höher als gewünscht. V51 wird in zwei Serien mit je sechs bereits verwendeten 16×16-Chunk-Gebieten geprüft; **keine neue Vanilla-Generierung**. Beide Serien sind keine unberührten Holdouts.

Beide V51-Serien sind vollständig (zwölf Gebiete/3.072 Chunks). Oberhalb −20 ergeben sich **10.874/10.180 = 106,8 %** eingeschlossene Erzblöcke und **4.341/4.143 = 104,8 %** getrennte eingeschlossene Gruppen. Die V19-Serie liegt bei 5.107/4.815 Blöcken und 2.043/1.984 Gruppen; die V24-Serie bei 5.767/5.365 Blöcken und 2.298/2.159 Gruppen. Nur 5.221 der 10.180 Vanilla-Positionen bleiben exakt erhalten: Die obere vergrabene Quelle wird durch eine neu platzierte, mengenmäßig angenäherte Regel ersetzt. „Vanilla-ähnlich“ meint daher die gemessene Häufigkeit, nicht identische Adern.

Sichtbare Höhlengruppen: **354/308 = 114,9 %**, im kritischen Band Y=−47..−32 **108/100 = 108 %**. Alle 342 direkt luftberührten Vanilla-Erzpositionen blieben erhalten; 53 neue kamen hinzu. Die maximale Gruppenzahl pro 64×64-Kachel im kritischen Band war bei Vanilla und V51 jeweils vier. Das ist keine Messung pro zusammenhängender Höhle. Auf Y=−57 blieben **225/1.334 = 16,9 %** eingeschlossene Erze; das überlappende Tunnelmodell ergab **1.808/10.823 = 16,7 %** Kontakte. Oberhalb +16 wurden zehn Erzblöcke bis maximal +24 beobachtet; +30 ist weiterhin nur eine geplante Obergrenze.

Eine isolierte `setblock air`-Probe (`verification/mining-00.json`) blieb nach Neustart entfernt, ohne weitere gemessene Erzpositionsänderungen. Sie simuliert keinen echten Spielerabbau. `combined-summary.json`, `secondary-spatial-summary.json` und `calibration-spatial-summary.json` enthalten die prüfbaren Zahlen.

Die oberen eingeschlossenen Gruppen haben Größen 1/2/3/4/5/6/7/8/>8: Vanilla 1.686/1.357/160/314/205/210/18/157/36, V51 1.714/1.442/178/303/233/243/24/149/55. Die größte technische Gruppe umfasst in beiden Varianten 15 Blöcke; benachbarte Adern können zusammenfallen und diagonale Verbindungen werden getrennt.

Fortsetzbare, prüfsummengeschützte Messung:

```sh
python3 -m tools.balance_followup status --plan experiments/balance-v51/secondary-plan.json
python3 -m tools.balance_followup run --plan experiments/balance-v51/secondary-plan.json
python3 -m tools.balance_followup status --plan experiments/balance-v51/calibration-plan.json
python3 -m tools.balance_followup run --plan experiments/balance-v51/calibration-plan.json
python3 -m tools.buried_height_compare --plan experiments/balance-v51/secondary-plan.json --plan experiments/balance-v51/calibration-plan.json
```

`tools.buried_height_compare` zählt eingeschlossene Blöcke und flächenweise verbundene Gruppen zwischen −19 und +16 aus den gespeicherten Rohscans. Die feste Paketversion `dist/cave-diamonds-v0.1.7.mcpack` enthält die V51-Generierung bytegleich; nur Manifest-Metadaten und Icon wurden für das Paket ergänzt. Paket, Spiel, Realm und Konsolen sind verschiedene Prüfungen: Import und Spiel wurden nicht praktisch verifiziert. Vor Einsatz in einer bestehenden Welt eine Sicherung erstellen; bereits generierte Chunks können abweichen oder unverändert bleiben.
