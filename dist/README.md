# Aktuelle Paketversion

`cave-diamonds-v0.1.10.mcpack` ist die aktuelle feste Version von Cave Diamonds. Gegenüber `v0.1.9` ändert sich nur die Manifest-Version von 0.1.9 auf 0.1.10. Sämtliche Generierungsdateien, Paketname, Beschreibung, Icon und UUIDs bleiben bytegleich. Erzeugung: `python3 -m tools.build_v57_dist --version 0.1.10`. Der Builder überschreibt eine vorhandene Version nicht. `v0.1.9` (ebenfalls V57), `v0.1.8` (V56), `v0.1.7` (V51), `v0.1.6` (V44), `v0.1.5` (V33) und `v0.1.4` (V29) bleiben erhalten.

Bei künftigen Kandidaten die neue versionierte `.mcpack` unter `dist/` ablegen und diesen Verweis aktualisieren. Forschungs- und Testpakete bleiben unter `experiments/`. Die Paketversion kennzeichnet den Stand; sie belegt keine erfolgreiche Realm- oder Konsolenprüfung. Vor Einsatz in einer bestehenden Welt eine Sicherung erstellen. Die Messergebnisse und offenen Prüfungen stehen in [`experiments/balance-v57/README.md`](../experiments/balance-v57/README.md).
