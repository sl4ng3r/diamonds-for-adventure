# V55 – anteilige Ausdünnung oberhalb −20

Neues Nutzerziel: Zwischen Y=−19 und +16 sollen vollständig eingeschlossene Diamanterzblöcke ungefähr **30 % der Vanilla-Menge** erreichen; direkt luftberührte Höhlenfunde sollen erhalten bleiben. V51 hatte oben 106,8 % eingeschlossene Blöcke. V52 mit oberem `scatter_chance`-Wert 6 ergab im ersten Gebiet noch 474/931 = 50,9 %, V53 mit Wert 2 noch 455/931 = 48,9 %, V54 mit kleineren Zusatzadern 421/931 = 45,2 %. Diese drei Versuche wurden nach je einem Gebiet gestoppt. Die Chance-Werte nicht als gemessene Prozentwahrscheinlichkeiten behandeln.

V55 entfernt die obere vergrabene Zusatzregel ganz. Die tiefe V51-Ausdünnung bleibt auf Y=−64..−20 begrenzt; zusätzlich scannt eine eigene `final_pass`-Regel Y=−19..16 und versucht bei vollständig eingeschlossenen normalen und Tiefenschiefer-Diamanterzen eine gewichtete Auswahl: Wirtsgestein mit Gewicht 1, Erz mit Gewicht 2. Das ist ein **Startparameter**, keine nachgewiesene 33-%-Entfernung. Luft- oder flüssigkeitsberührte Erze sind von der Ersatzregel ausgenommen. Normale/große Vanilla-Features, sparsame Höhlenregeln und obere Möglichkeit bis geplant +30 bleiben erhalten. Die vergrabene Vanilla-Quelle bleibt unterdrückt.

Kandidatenwelten werden ausschließlich gegen vorhandene Vanilla-Rohscans verglichen. Pläne und Ergebnisse sind einzeln fortsetzbar:

```sh
python3 -m tools.balance_followup status --plan experiments/balance-v55/secondary-plan.json
python3 -m tools.balance_followup run --plan experiments/balance-v55/secondary-plan.json
python3 -m tools.balance_followup status --plan experiments/balance-v55/calibration-plan.json
python3 -m tools.balance_followup run --plan experiments/balance-v55/calibration-plan.json
python3 -m tools.buried_height_compare --plan experiments/balance-v55/secondary-plan.json --plan experiments/balance-v55/calibration-plan.json
```

Die beiden Referenzserien waren bereits für frühere Varianten verwendet und sind kein unabhängiger Holdout. Die lokal committete v0.1.7 aus V51 wurde nach der neuen Nutzerpräferenz **nicht gepusht**. Erst nach Bedrock-Prüfung eine neue feste Version unter `dist/` bauen und pushen.
