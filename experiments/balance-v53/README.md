# V53 – Oberes vergrabenes Erz bei ungefähr 30 %

Der Nutzer möchte zwischen Y=−19 und +16 nur noch ungefähr 30 % der **vollständig eingeschlossenen Diamanterzblöcke** gegenüber Vanilla. Sichtbare Höhlenfunde sollen wie bei V51 erhalten bleiben. V51 hatte über zwölf bereits verwendete Referenzgebiete 10.874/10.180 = 106,8 % eingeschlossene Blöcke, 4.341/4.143 = 104,8 % getrennte eingeschlossene Gruppen und 354/308 = 114,9 % sichtbare Gruppen. V44 hatte oben nur 19,4 % eingeschlossene Blöcke.

V52 änderte gegenüber V51 nur den oberen `scatter_chance`-Engine-Wert von 45 auf 6. Im ersten V19-Gebiet ergaben sich dennoch 474/931 = 50,9 % eingeschlossene Blöcke, 247/353 = 70,0 % eingeschlossene Gruppen. Sichtbar blieben alle 40 Vanilla-Erzpositionen erhalten, mit 43/38 sichtbaren Gruppen; auf Y=−57 blieben 16/111 vergrabene Erze. V52 wurde nicht weitergemessen. V53 setzt denselben oberen Wert auf 2; **das ist keine garantierte 2-%-Wahrscheinlichkeit**. Alle übrigen Generierungsdateien bleiben bytegleich zu V52/V51.

Die ersten Tests laufen gegen bereits gespeicherte Vanilla-Rohscans, ohne neue Vanilla-Welt. Pläne und Ergebnisse sind einzeln fortsetzbar:

```sh
python3 -m tools.balance_followup status --plan experiments/balance-v53/secondary-plan.json
python3 -m tools.balance_followup run --plan experiments/balance-v53/secondary-plan.json
python3 -m tools.balance_followup status --plan experiments/balance-v53/calibration-plan.json
python3 -m tools.balance_followup run --plan experiments/balance-v53/calibration-plan.json
python3 -m tools.buried_height_compare --plan experiments/balance-v53/secondary-plan.json --plan experiments/balance-v53/calibration-plan.json
```

Der neue obere Zielwert bezieht sich auf Erzblöcke; die Zahl getrennter Gruppen wird gesondert berichtet. Beide Referenzserien waren bereits für frühere Varianten verwendet und sind kein unabhängiger Holdout. Das lokal committete Paket v0.1.7 aus V51 wurde **nicht gepusht**; ein neuer fester Stand wird erst nach Messung und Prüfung gebaut.
