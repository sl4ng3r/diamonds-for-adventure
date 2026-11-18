# V56 – etwa 30 % eingeschlossene Erze oberhalb −20

Nutzerziel: Für vollständig eingeschlossene Diamanterzblöcke zwischen Y=−19 und +16 ungefähr 30 % von Vanilla, während direkt luftberührte Höhlenfunde erhalten bleiben und die tiefe Tunnelhöhe selten bleibt. V51 hatte über zwölf früher verwendete Referenzgebiete 106,8 % eingeschlossene Blöcke; V52–V54 blieben nach je einem Gebiet bei 45–51 %. V55 führte einen eigenen oberen `final_pass`-Filter mit Ersetzen/Behalten-Gewichten 1:2 ein und erreichte im ersten V19-Gebiet 335/931 = 36,0 %. V56 ändert ausschließlich diese Gewichte auf **2:1** für normale und Tiefenschiefer-Diamanterze. Das ist ein Engine-Startparameter, keine garantierte Ersetzungswahrscheinlichkeit.

Die erste V19-Serie mit sechs Gebieten/1.536 Chunks ist vollständig: oben eingeschlossen **1.442/4.815 = 29,9 % Blöcke**, **960/1.984 = 48,4 % getrennte eingeschlossene Gruppen**. Sichtbare Höhlengruppen **188/164 = 114,6 %**; vergraben auf Y=−57 **109/660 = 16,5 %**. Alle **181 direkt luftberührten Vanilla-Erzpositionen** blieben erhalten; 32 neue kamen hinzu. Im kritischen Band −47..−32 ergaben sich 57/52 = 109,6 % luftberührte Gruppen. Die obere Grenze +30 der Höhlenregel bleibt geplant; in dieser V56-Serie wurde oberhalb +16 kein Erz gefunden. Funde nahe +30 sind nicht nachgewiesen.

Die zweite V24-Serie mit sechs ebenfalls bereits früher verwendeten Gebieten ist **nicht abgeschlossen**. Das erste 16×16-Gebiet scheiterte zweimal mit `LocationInUnloadedChunkError` beim ersten Scanblock, obwohl alle vier Ticking Areas angelegt waren. Nach Erhöhung der Wartezeit vor großen Scans von 30 auf 120 Sekunden trat dieser Fehler nicht erneut auf, aber das Diagnoseskript lieferte innerhalb seiner 768-Sekunden-Grenze kein Ergebnis. Der Server nutzte währenddessen CPU. Ein V19-Gebiet benötigte bis zum fertigen Scan 541 Sekunden nach Serverstart, die übrigen 126–152 Sekunden. Die Ursache der starken Laufzeitstreuung und die Mehrspieler- und Realm-Leistung bleiben offen. Keine Ergebnisse der gescheiterten V24-Läufe wurden in die Kennzahlen eingerechnet.

V56 übernimmt V55s Architektur: normales/großes Vanilla-Diamantfeature aktiv; vergrabene Vanilla-Quelle unterdrückt; tiefe Ausdünnung bis einschließlich −20; separater anteiliger Filter oberhalb −20 nur für Erze ohne direkten Luft- oder Flüssigkeitskontakt. Zwei sparsame Höhlenregeln plus obere Regel bleiben bytegleich zu V51. Die höher gelegenen vergrabenen Adern sind nicht an denselben Positionen wie in Vanilla zu garantieren.

Nur Kandidatenwelten werden neu gemessen, gegen die gespeicherten Vanilla-Rohscans. Die zwei Referenzserien wurden bereits für andere Varianten verwendet und sind keine unabhängigen Holdouts. Fortsetzbare Läufe:

```sh
python3 -m tools.balance_followup status --plan experiments/balance-v56/secondary-plan.json
python3 -m tools.balance_followup run --plan experiments/balance-v56/secondary-plan.json
python3 -m tools.balance_followup status --plan experiments/balance-v56/calibration-plan.json
python3 -m tools.balance_followup run --plan experiments/balance-v56/calibration-plan.json
python3 -m tools.buried_height_compare --plan experiments/balance-v56/secondary-plan.json --plan experiments/balance-v56/calibration-plan.json
```

Das feste Paket `dist/cave-diamonds-v0.1.8.mcpack` entspricht V56 bis auf Manifestname, Beschreibung, Version und Icon. Die Zahlen stammen ausschließlich aus der abgeschlossenen V19-Serie, nicht aus einem unabhängigen Holdout. Vor Einsatz in einer wichtigen Welt sind Sicherung und praktischer Spieltest nötig; die festen Pakete sind kein Nachweis für Realm- oder Konsolenkompatibilität.
