# V52 – eingeschlossene Funde oberhalb −20 auf ungefähr 30 %

Der Nutzer möchte die Zahl vollständig eingeschlossener Diamanterzblöcke oberhalb Y=−20 auf ungefähr 30 % von Vanilla senken. V51 hatte in zwölf zuvor genutzten Referenzgebieten/3.072 Chunks für Y=−19..16 10.874/10.180 = 106,8 % Blöcke und 4.341/4.143 = 104,8 % getrennte eingeschlossene Gruppen. V44 hatte nur 19,4 % Blöcke. V52 ändert gegenüber V51 **nur** den `scatter_chance`-Engine-Wert der oberen vergrabenen Zusatzregel von 45 auf 6. Dieser Wert ist empirisch gewählt, keine bestätigte Prozentwahrscheinlichkeit.

Die sichtbaren Höhlenregeln, normale/große Vanilla-Diamantfeatures, Ausdünnung bis einschließlich −20, tiefe Tunnelbalance und obere Höhlenregel bis geplant +30 bleiben bytegleich zu V51. V51 bewahrte alle 342 luftberührten Vanilla-Erzpositionen und erreichte 354/308 = 114,9 % getrennte sichtbare Gruppen; V52 muss diese Wirkung im Bedrock-Test erneut bestätigen. Die vergrabenen oberen Adern liegen weiterhin nicht an exakt denselben Koordinaten wie in Vanilla.

Die Kandidatenwelt wird gegen die gespeicherten Vanilla-Referenzen gemessen; kein neuer Vanilla-Scan. Beide Referenzserien waren bereits für ältere Varianten genutzt und sind kein unberührter Holdout. Fortsetzen:

```sh
python3 -m tools.balance_followup status --plan experiments/balance-v52/secondary-plan.json
python3 -m tools.balance_followup run --plan experiments/balance-v52/secondary-plan.json
python3 -m tools.balance_followup status --plan experiments/balance-v52/calibration-plan.json
python3 -m tools.balance_followup run --plan experiments/balance-v52/calibration-plan.json
python3 -m tools.buried_height_compare --plan experiments/balance-v52/secondary-plan.json --plan experiments/balance-v52/calibration-plan.json
```

`dist/cave-diamonds-v0.1.7.mcpack` aus V51 wurde lokal erstellt und committed, aber **noch nicht gepusht**. Es bleibt während der V52-Prüfung unverändert; erst ein ausreichend gemessener neuer Stand wird unter einer höheren Version abgelegt und gepusht. Spiel-, Realm- und Konsolenprüfung bleiben offen.
