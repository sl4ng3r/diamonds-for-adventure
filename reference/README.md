# Vanilla-Referenz vom 3. November 2026

Die Datei `vanilla-1.26.61.1-2026-11-03.json` hält die Ausgangsmessung für spätere Balancing-Vergleiche fest. Getestet wurden 20 ausgewählte 4×4-Chunk-Ausschnitte in 19 Seeds auf Bedrock Dedicated Server 1.26.61.1. Sie waren ohne das Forschungs-Add-on; das separate Diagnosepack liest die Blöcke aus. Insgesamt wurden 320 Chunks im Bereich Y=−64 bis einschließlich 16 untersucht. Die Bereiche sind keine zufällige oder repräsentative Stichprobe der ganzen Minecraft-Welt.

Die Nutzerziele sind circa 15 % mehr **getrennte Höhlenfundstellen**, ohne größere Adern, und im Umfeld von Y=−57 circa 30 % des Vanilla-Erzbestands. Die konkrete Höhenkurve ist noch offen. Die Referenz umfasst keine tatsächlichen Spielzeiten oder Tests des Add-ons.

## Bedeutung der Messwerte

- `blocks.air`: mindestens ein direkt benachbarter Luftblock. Ein Hohlraum kann winzig, verdeckt oder unerreichbar sein; dies ist nur ein Näherungswert für Höhlenfunde.
- `blocks.fluid_only`: Kontakt zu Wasser oder Lava, aber kein Luftkontakt. `buried`: weder Luft- noch Wasserkontakt noch Lavakontakt. Diese drei Kategorien schließen sich gegenseitig aus.
- `water_adjacent`, `lava_adjacent` und `air_and_fluid` sind zusätzliche, überlappende Kontaktzahlen, keine weiteren Kategorien zur Summe.
- `y_minus57` erfasst genau diese Blockhöhe; `tunnel_band` erfasst −59 bis einschließlich −55. Beides zählt Erzblöcke, keine Spielerausbeute. Ein zweiblöckiger Tunnel legt auch Boden, Decke und Seiten frei.
- `deepslate_ore` zählt den Erzblocktyp, unabhängig von der Höhe. `below_zero` zählt die Höhe, unabhängig vom Blocktyp. Beide Gruppen sind nicht identisch.
- `deposits` sind Gruppen von Erzblöcken mit direktem Flächenkontakt. Diagonal benachbarte oder getrennte Teile derselben natürlich generierten Ader können als mehrere Gruppen gezählt werden; benachbarte natürliche Adern können zusammenfallen. Gruppen an der Scan-Grenze können unvollständig sein. Das ist keine vollständige Erkennung echter Adern oder erreichbarer Fundstellen.
- Verschiedene Höhen und Biome wurden nur punktuell erfasst. Weltgenerierung, unbeeinflusste Chunks und Flüssigkeiten können sich unter anderem beim Laden verändern. Die 23 beobachteten luftseitigen Gruppen sind zu wenige, um eine 15-%-Änderung präzise abzusichern.

## Reproduktion

Die Quellliste verweist auf die tatsächlich für diese Messung verwendeten Dateien unter `data/research/`. Solange diese lokalen Testdaten vorhanden sind, lässt sich die Auswertung ohne Serverstart neu erzeugen:

```sh
xargs python3 -m tools.aggregate_vanilla_reference --server-version 1.26.61.1 --measurement-date 2026-11-03 --output reference/vanilla-rebuilt.json < reference/vanilla-1.26.61.1-2026-11-03-inputs.txt
```

Das Werkzeug verweigert standardmäßig das Überschreiben vorhandener Ausgaben. Sind die lokalen Rohscans nicht mehr vorhanden, können die einzelnen Gebiete anhand ihrer Seeds und Chunk-Koordinaten aus der JSON-Datei mit `python3 -m tools.vanilla_reference --seed SEED --chunks 4 --chunk-x X --chunk-z Z` neu erzeugt werden. Wegen Bedrock-Ladeverhalten und Veränderungen bei Updates sind identische Ergebnisse nicht garantiert. Der Server startet nur nach ausdrücklicher EULA-Zustimmung in `.env`; reale Welten werden nicht verwendet.
