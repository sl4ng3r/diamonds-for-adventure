# V60 – Ganze Höhlenadern erhalten

V60 ersetzt die blockweise Ausdünnung von V59. Die übrigen Höhlenregeln einschließlich der Ozeanregel bis Y=+35 werden übernommen. Die Vanilla-Regel für vergrabene Adern ist wieder aktiv, damit der Filter auch diese Adern im Originalzustand prüfen kann.

Zwei unsichtbare, unzerstörbare Barriereblöcke in der untersten Grundgesteinsschicht kennzeichnen frisch generierte Chunks. Sobald ein Spieler in die Nähe kommt, prüft das Verhalten pro Durchlauf höchstens einen markierten Chunk und setzt nach der Prüfung beide Marker zu Grundgestein zurück. Direkt vom Spieler bearbeitete markierte Chunks werden von der Ausdünnung ausgenommen. Chunks ohne das Markerpaar werden nicht bearbeitet.

Das Skript fasst normale Diamanterze und Tiefenschiefer-Diamanterze zu Gruppen zusammen. Es zählt auch Kanten- und Eckverbindungen, um diagonal verlaufende Adern zu schonen. Sobald ein Block der Gruppe flächig an Luft, Wasser oder Lava grenzt, bleibt die ganze Gruppe erhalten. Wenn Nachbarn nicht geladen sind, die Ader in einen anderen Chunk reicht oder oberhalb der bisherigen Ausdünnungsgrenze Y=+16 weitergeht, bleibt sie ebenfalls erhalten. Nur vollständig eingeschlossene Gruppen im geprüften Chunk kommen für eine Entfernung infrage. Für diese Gruppen ist der Sollwert für den Erhalt 15 % bei tiefster Position bis Y=−20 und 30 % darüber. Weil sichere Ausnahmefälle zusätzlich erhalten bleiben und Adern unterschiedlich groß sind, sind das keine Sollwerte für alle eingeschlossenen Erzblöcke.

Die JavaScript-Laufzeit benötigt das stabile Modul `@minecraft/server` in Version 2.11.0. Erst in einer neuen Testwelt oder einer Kopie einspielen. Die Ausdünnung wird beim Erkunden ausgeführt. Ein Update kann bereits entfernte Erze in alten Chunks nicht rekonstruieren.

## Bedrock-Prüfung

Im Bedrock Dedicated Server 1.26.61.1 wurden vor und nach der Ausdünnung dieselben 16 Chunks von Seed 919001 (Chunkstart 2300/−3200) gescannt. Die Teststeuerung rief dieselbe Chunk-Funktion auf, die das Paket beim Erkunden verwendet. Sie fand alle 16 Markerpaare. Ein zweiter Aufruf für jeden bearbeiteten Chunk erkannte keine Marker mehr.

- Alle vier Adern mit Luft- oder Flüssigkeitskontakt blieben an denselben Positionen vollständig erhalten. Zwei bestanden jeweils aus drei Erzblöcken.
- 50 von 69 eingeschlossenen Gruppen wurden als ganze Gruppen entfernt. Insgesamt blieben 63 von 240 Erzblöcken übrig. Keine Ader im Vorher-Nachher-Vergleich wurde geteilt.
- Im Band Y=−59 bis −55 blieben 6 von 40 eingeschlossenen Erzblöcken (15 %). Auf Y=−57 blieben in dieser Stichprobe 0 von 10, oberhalb Y=−20 13 von 46 (28,3 %). Der Vergleich misst die Ausdünnung im selben V60-Gebiet vor und nach dem Aufruf. Eine unabhängige Balanceprüfung gegen Vanilla, die automatische Ausführung mit echten Spielern, Mehrspielerleistung und Realm-Kompatibilität stehen noch aus.

Lokales Spieltestpaket: `data/package-archive/cave-diamonds-v0.1.13.mcpack`. Erzeugung mit `python3 -m tools.build_v60 --package`. Rohscans und Chunk-Ergebnisse liegen unter `data/research/cavediamonds-research-d7f2e6598c/`.
