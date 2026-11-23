# V59 – Diamanten in Unterwasserhöhlen

V59 ergänzt V57 (Paket 0.1.10) um eine seltene Platzierung im Ozean bis zur absoluten Höhe **Y=+35 einschließlich**. Startpunkte reichen von Y=−40 bis +31. Beim Einbetten an der Decke liegt die Erzposition in Bedrock höchstens vier Blöcke über dem Startpunkt.

Die Regel sucht an Boden, Wand oder Decke im Wasser nach Stein und Tiefenschiefer. Auch freiliegende Felsflächen am Meeresgrund können passen. Pro erfolgreichem Versuch kommt genau ein Erzblock hinzu. Die Regel erzeugt selbst keine größeren Adern. In unmittelbarer Nähe können bereits vorhandene Erze liegen. Alle Generierungsdateien von V57 sind bytegleich übernommen. Bedrock kann bei erneuter Generierung dennoch einzelne Positionen anders setzen.

## Bedrock-Prüfung

- Bedrock Dedicated Server 1.26.61.1 platzierte bei direkten Versuchen in einem gefüllten Testhohlraum je einen Block am Boden, an der Wand und an der Decke. Die entsprechenden neun Versuche in Luft, Lava und massivem Stein platzierten keinen.
- Bei einem direkten Test mit Startpunkt Y=+31 entstand ein Erzblock an einer Unterwasserdecke bei Y=+35. Bei einer Decke auf Y=+36 entstand kein Erzblock. Alle 191 automatisierten Tests bestanden. Der Paketvergleich mit 0.1.11 ergab nur Änderungen an der Obergrenze der Ozeanregel und an der Manifest-Version.
- Natürlicher Scan des Vorgängerpakets 0.1.11 im Ozean mit Seed `919033`, 8×8 Chunks ab `−2900/−5300`, verglichen mit dem gespeicherten V57-Scan derselben Fläche. V57 hatte zwei wasserberührte Erzblöcke, V59 drei. Der einzelne neue Block lag auf Y=+17 mit Wasser direkt darunter. Das nächste Diamanterz lag 32 Blockschritte entfernt. Alle fünf bestehenden luft- bzw. wasserberührten Erzpositionen blieben erhalten. Eine eingeschlossene Position auf Y=−19 fehlte im neuen Lauf. Rohscans unter `data/research/cavediamonds-research-0342d08d1f/` (V59) und `data/research/cavediamonds-research-9ea22d41df/` (V57).
- Die 64 Chunks zeigen natürliche Platzierung. Sie reichen nicht aus, um Fundhäufigkeit, das Verhalten in anderen Ozeanen, die globale Balance oder Realm-Kompatibilität zu bestätigen.

Lokales Spieltestpaket: `dist/cave-diamonds-v0.1.12.mcpack`. Erzeugung mit `python3 -m tools.build_v59 --package`. Für den Spieltest neue Chunks in einer Kopie oder einer neuen Welt erkunden.
