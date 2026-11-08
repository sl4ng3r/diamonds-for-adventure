# V24 – lokaler Balancekandidat

V24 ergänzt gegenüber V19 eine Höhlenregel für Y=−52 bis −41 mit dem Zahlenwert `scatter_chance: 40`. Die effektive Eintrittswahrscheinlichkeit ist nicht belegt; die ursprüngliche Tunnelregel und übrigen Features bleiben unverändert. Pack-Hash: `de14344d983552f58f5e2f4075e63def5e1ca910d3ef250885268e76e0259832`.

In der Kalibrierung: 32/23 luftberührte Gruppen (139,1 %), 31/118 eingeschlossene Erze Y=−57 (26,3 %). Der separat vorab festgelegte Holdout umfasste sechs Seeds und 1.536 Chunks: 157/144 Gruppen (109,0 %), 114/674 eingeschlossene Erze Y=−57 (16,9 %), 845/5225 überlappende Tunnelkontakte (16,2 %). Gruppengrößen 1/2/3/4/5: 18/48/61/28/2. Gebiets-Bootstrap für die Gruppenquote: 85,6–133,6 %. Luftkontakt ist keine belegte Erreichbarkeit; Tunnelkontakte sind keine Spielrunden.

Die Fundverteilung zeigt einen möglichen X-Chunk-Halbeneffekt, der weitere Prüfungen erfordert. Kontrollierte Proben: je drei Platzierungen an Boden, Wand und Decke erfolgreich; ein per `setblock air` entfernter Erzblock blieb nach Neustart entfernt. Kein echter Werkzeugabbau. Details und Einschränkungen stehen in `TESTREPORT.md`.

```sh
python3 -m tools.balance_batch status --pack experiments/balance-v24/behavior_pack --results experiments/balance-v24/holdout-results --reference reference/balance-holdout-v24-1.26.61.1-2026-11-04.json
python3 -m tools.balance_profiles --results experiments/balance-v24/holdout-results --reference reference/balance-holdout-v24-1.26.61.1-2026-11-04.json
```

Nicht freigegeben: Spieler-, Leistungs- und Realmtests sowie die Untersuchung der Koordinatenverteilung sind offen. Andere weltgenerierende Add-ons und experimentelle Weltoptionen sind nicht unterstützt. Die Variante überschreibt Vanilla-Diamantfeatures und erzeugt Erzpositionen neu.
