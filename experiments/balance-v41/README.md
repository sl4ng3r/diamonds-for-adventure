# V41 – Vanilla-Höhlenadern als Ausgangspunkt

V29 bis V40 ersetzen die normalen Vanilla-Diamantfeatures und setzen neue Erze an Höhlenflächen. In einer großen Höhle kann das zu vielen separaten Fundstellen führen. V41 lässt `minecraft:diamond_ore_feature` und `minecraft:diamond_ore_large_feature` deshalb unverändert. Sie unterdrückt nur `minecraft:diamond_ore_buried_feature`, entfernt alle eigenen normalen Höhlen- und vergrabenen Zusatzregeln und behält die obere Regel mit geplantem Maximum Y=+30. V41 ist ein Diagnosepack, keine feste Version.

Im auffälligen wiederverwendeten V19-Referenzgebiet (Seed 919001, 16×16 Chunks) hat V41 **38/38 luftberührte Erzgruppen** und **40/40 luftberührte Blöcke** gegenüber Vanilla. Die 40 luftberührten Erzblöcke liegen an exakt denselben Positionen. Im Band Y=−47..−32 sind es **10/10 Gruppen** und **11/11 luftberührte Blöcke**. Damit zeigt dieser Engine-Test, dass die eigenen Höhlenregeln die zuvor beobachtete Häufung verursachten; er beweist keine allgemeine Identität in allen Welten.

Der Nachteil: Auf Y=−57 bleiben **57/111 = 51,4 %** der vergrabenen Vanilla-Erzblöcke, alle 57 an Vanilla-Positionen. Das überlappende Tunnelmodell liefert 492/919 = 53,5 % Kontakte. V41 verfehlt damit den früheren Arbeitswert von etwa 15 % und erzeugt im getesteten Untergrund keine 10–15 % zusätzlichen Höhlenfundstellen. V42 prüft eine ergänzende späte Ausdünnung; deren Wirksamkeit und Erhalt der Höhlenadern sind offen.

Reproduktion ohne neuen Vanilla-Scan:

```sh
python3 -m tools.balance_followup status --plan experiments/balance-v41/secondary-plan.json
python3 -m tools.cave_spatial_compare --plan experiments/balance-v41/secondary-plan.json
```

Rohscans und Testwelten liegen lokal unter `data/research/`; die Ergebnisse enthalten Pack- und Referenzprüfsummen. Luftkontakt beweist keine Sichtbarkeit oder Erreichbarkeit. Import, alte Welten, Spiel, Realm und Konsolen sind nicht geprüft.
