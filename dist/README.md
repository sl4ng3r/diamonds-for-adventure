# Aktuelle Paketversion

`cave-diamonds-v0.1.5.mcpack` ist die aktuelle feste Version von Cave Diamonds. Sie enthält die Generierungsdateien des V33-Kandidaten bytegleich; geändert wurden nur Paketname, Beschreibung, Icon und Manifest-Version. Erzeugung: `python3 -m tools.build_v33_dist`. Der Builder überschreibt eine vorhandene Version nicht. `cave-diamonds-v0.1.4.mcpack` bleibt als vorheriger V29-Stand erhalten.

Bei künftigen Kandidaten die neue versionierte `.mcpack` unter `dist/` ablegen und diesen Verweis aktualisieren. Forschungs- und Testpakete bleiben unter `experiments/`. Die Paketversion kennzeichnet den Stand; sie belegt keine erfolgreiche Realm- oder Konsolenprüfung. Vor Einsatz in einer bestehenden Welt eine Sicherung erstellen. Die Messergebnisse und offenen Prüfungen stehen in [`experiments/balance-v33/README.md`](../experiments/balance-v33/README.md).
