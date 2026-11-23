# Aktuelle Paketversion

[Cave Diamonds v0.1.16](cave-diamonds-v0.1.16.mcpack) enthält V63 mit zusätzlichen tiefen Höhlenfunden, Ozeanfunden bis Y=+35 und Ausdünnung vollständig eingeschlossener Adern. Der [Testbericht](../experiments/balance-v63/README.md#ergebnis) beschreibt die Ergebnisse aus 384 Chunks und die offenen Spiel- und Realm-Tests.

Erzeugung mit `python3 -m tools.build_v63 --package`. Der Builder überschreibt keine vorhandene Paketdatei. Vor einem Update auf einer bestehenden Welt eine Sicherung erstellen.

Hier liegt genau eine `.mcpack`. Bei jeder neuen festen Version das bisherige Paket nach `data/package-archive/` verschieben, die neue Datei in `.gitignore` freigeben und zusammen mit dem Quellstand committen und pushen. Diesen Verweis, den Verweis in der Projekt-README und die Paketprüfung auf die neue Version umstellen. Bereits veröffentlichte Pakete sind im Git-Verlauf verfügbar. Die Builder früherer Versionen schreiben ins lokale Archiv.
