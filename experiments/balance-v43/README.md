# V43 – Vanilla-Höhlenadern mit später Ausdünnung

V41 erhält normale und große Vanilla-Diamantfeatures und unterdrückt die vergrabene Vanilla-Quelle. Im auffälligen Seed 919001 blieben alle 40 luftberührten Erzblöcke an exakt denselben Positionen, aber noch 57/111 vergrabene Erze auf Y=−57. V42 ergänzt den alten `final_pass`-Ausdünner und senkte dort auf 21/111, ohne Luftkontaktpositionen zu verlieren. V43 ersetzt jeden vom Ausdünner erreichten, vollständig eingeschlossenen Erzblock sicher durch Stein beziehungsweise Tiefenschiefer; die sechsseitige Luft-/Flüssigkeitssperre bleibt unverändert.

Im ersten isolierten 16×16-Chunk-Gebiet (Seed 919001) hatte V43 **38/38 luftberührte Erzgruppen**, alle **40/40 luftberührten Erzblöcke an exakt denselben Koordinaten** und bei Y=−47..−32 **10/10 Gruppen** (11/11 luftberührte Blöcke). Auf Y=−57 blieben **16/111 = 14,4 %** vergrabene Erze; das überlappende Tunnelmodell ergab **127/919 = 13,8 %** Kontakte. Die verbleibenden Erze liegen an Vanilla-Positionen. Das ist ein einzelner ausgewählter Seed und noch keine allgemeine Freigabe.

In drei Gebieten der zweiten wiederverwendeten Referenzserie blieben zusammen **101/101 luftberührte Vanilla-Erzblöcke an denselben Positionen**, ohne verlorene oder neue Luftkontaktposition. Die technische Gruppenzahl ist 94/93: Das Entfernen eines eingeschlossenen Verbindungsblocks trennte eine Gruppe. Auf Y=−57 blieben **55/357 = 15,4 %** vergrabene Erze. Das bestätigt die Wirkung in drei Seeds, ist aber kein unabhängiger Holdout und beweist keine allgemeine Positionssicherheit.

Die obere Regel bis geplant Y=+30 bleibt gegenüber V37 bytegleich. V43 erzeugt im normalen Untergrund keine zusätzlichen Höhlenfundstellen; V44 testet deshalb wenige neue Fundstellen zusätzlich zu den erhaltenen Vanilla-Adern. Die `final_pass`-Ausdünnung wurde in älteren Versuchen allein als unzuverlässig befunden. Weitere Seeds und praktische Spiel-/Realmtests bleiben erforderlich.

Reproduktion ohne erneuten Vanilla-Scan:

```sh
python3 -m tools.balance_followup status --plan experiments/balance-v43/secondary-plan.json
python3 -m tools.cave_spatial_compare --plan experiments/balance-v43/secondary-plan.json
```

Rohscans und Testwelten liegen lokal unter `data/research/`. Luftkontakt beweist keine tatsächliche Sichtbarkeit oder Erreichbarkeit; Weltübernahme, Spiel, Realm, Konsolen und Leistung bleiben offen. V43 ist ein Forschungspack, `dist/` bleibt unverändert.
