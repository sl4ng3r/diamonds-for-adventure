# Aktuelle Paketversion

`cave-diamonds-v0.1.6.mcpack` ist die aktuelle feste Version von Cave Diamonds. Sie enthält die Generierungsdateien des V44-Kandidaten bytegleich; geändert wurden nur Paketname, Beschreibung, Icon und Manifest-Version. Erzeugung: `python3 -m tools.build_v44_dist`. Der Builder überschreibt eine vorhandene Version nicht. `v0.1.5` (V33) und `v0.1.4` (V29) bleiben erhalten.

Bei künftigen Kandidaten die neue versionierte `.mcpack` unter `dist/` ablegen und diesen Verweis aktualisieren. Forschungs- und Testpakete bleiben unter `experiments/`. Die Paketversion kennzeichnet den Stand; sie belegt keine erfolgreiche Realm- oder Konsolenprüfung. Vor Einsatz in einer bestehenden Welt eine Sicherung erstellen. Die Messergebnisse und offenen Prüfungen stehen in [`experiments/balance-v44/README.md`](../experiments/balance-v44/README.md).
