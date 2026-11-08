# Testbericht – Machbarkeitsprototyp

Die separate Vanilla-Balancingreferenz vom 3. November 2026 umfasst 320 Chunks in 20 ausgewählten Gebieten und 19 Seeds. Ergebnisse und Auswertungsgrenzen stehen in `AGENTS.md` und `reference/README.md`, die einzelnen Werte in `reference/vanilla-1.26.61.1-2026-11-03.json`. Sie misst keine Add-on-Wirkung oder Diamanten pro Spielstunde.

Stand: 3. November 2026. Server: offizieller Bedrock Dedicated Server 1.26.61.1 unter Docker linux/amd64. Die Testwelt ist entbehrlich und liegt in `data/`. Das Pack wurde laut Serverlog in den Pack-Stack geladen, Inhalt-Meldungen waren aktiviert.

- Statische Prüfungen: vier Prüfungen erfolgreich. Sie bestätigen Struktur und gewünschte Konfiguration, nicht das Engine-Verhalten.
- Manuelle Engine-Probe im vorbereiteten Bereich: Ein an Luft grenzendes Diamanterz blieb erhalten; der einzelne Feature-Aufruf wurde dort abgelehnt. Ein von Stein umschlossenes Diamanterz wurde beim Feature-Aufruf zu Stein.
- Manuelle Rasterprobe: 11.760 künstlich gesetzte Diamanterzblöcke innerhalb einer Steinhülle. Ein direkter Aufruf von `cavediamonds:scan_chunk` ließ 1.149 Erze übrig. Dies entspricht 10.611 ersetzten Blöcken beziehungsweise 90,23 %. Die Zählung verwendete `fill ... gold_block replace diamond_ore` und veränderte ausschließlich den Testbereich.
- Dieser direkte Feature-Aufruf belegt weder die automatische Ausführung bei natürlicher Weltgenerierung noch die Einmaligkeit aller 20.736 Positionen. Die Probe ist nicht automatisiert und ersetzt keine Mehrfach-, Rand-, Biom- oder Seed-Tests.
- Offen: alle sechs Seiten und Flüssigkeiten, Tiefenschiefer, vollständige Rasterprüfung, natürliche Generierung, Chunk- und Biomgrenzen, Persistenzprüfung, drei Seeds, Spielbalance, Zwei-Spieler-Last, Realm- und Konsolenprüfung sowie Deploy-Cockpit-Erkennung. Kein freigegebenes `.mcpack`.
- Deploy-Cockpit-Scanner lokal gegen dieses Verzeichnis ausgeführt: `minceaftPlugin` mit Service `bedrock-test` und erkanntem Healthcheck gefunden. Dies bestätigt die Erkennung, keine Installation oder Aktualisierung auf einem Server.
- Nach Container-Neuerstellung: Compose meldet `healthy`; ein Prozess-Healthcheck beweist nicht die Funktionsfähigkeit des Packs.

Die manuelle Rasterprobe wurde über die Bedrock-Serverkonsole ausgeführt:

```text
fill 0 -64 0 15 16 15 stone
fill 1 -63 1 14 -4 14 diamond_ore
place feature cavediamonds:scan_chunk 0 -64 0
fill 1 -63 1 14 -4 14 gold_block replace diamond_ore
```

## Eingrenzung der Neustartabweichung

Alle folgenden Experimente verwenden getrennte Forschungskopien. Das ursprüngliche Prototyp-Pack und die Welt eines Spielers wurden nicht verändert.

Im Tropfsteinhöhlen-Ausschnitt (Seed 98765, Chunk −500/300, vier Chunks) wurden Höhlen- und Gesteinserzeugung getrennt. Nur mit Höhlenplatzierung änderte sich nach Neustart je ein Erz an zwei Positionen; nur mit vereinzelten vergrabenen Erzen blieb das eine gefundene Erz erhalten. Bei der Höhlenvariante mit je einer künstlichen Chunkmarkierung blieb sie unverändert. Die Gesteinsstichprobe ist zu klein für einen Zuverlässigkeitsnachweis.

Der bisherige Höhlenversuch nutzt `aggregate_feature` mit `early_out: first_success`, um Boden oder Decke auszuwählen. Microsoft dokumentiert für Aggregate keine feste Reihenfolge: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftaggregate_feature?view=minecraft-bedrock-stable. Ein Einmaltest nur mit Boden und ein Einmaltest nur mit Decke blieb nach Neustart unverändert; ein Gegenversuch mit beiden Oberflächen und ohne frühzeitigen Abbruch hatte drei entfernte und drei hinzugekommene Erze. Dies stützt die Hypothese einer Reihenfolgeabhängigkeit, beweist sie aber nicht.

Als zweite unabhängige Änderung wurde die Phase der Höhlengenerierung untersucht. Bei jeweils einem Test nur mit Höhlenplatzierung blieben `underground_pass` und `after_underground_pass` stabil; `after_surface_pass` änderte je ein Erz an zwei Positionen. Drei weitere kombinierte Tests mit `after_underground_pass` und zwei Seeds zeigten ebenfalls keine Änderung nach Neustart. Frühere Platzierung änderte jedoch auch die Zahl und zum Teil die Freilegung der Erze. Weil die Tests Gebiete, Zeitabläufe und nur eine Stichprobe abdecken, ist sie noch keine freigegebene Lösung.

Eine kombinierte Variante nur mit Bodenplatzierung wurde in vier weiteren Ausschnitten à vier Chunks und zwei weiteren à 16 Chunks untersucht. Bei diesen sechs Neustarts waren Erzpositionen, Typen und die Feststellung Luft-/Flüssigkeitskontakt unverändert. Ein weiterer Test entfernte in einer Wegwerfwelt ein freiliegendes Erz per `setblock ... air`: Der entfernte Block erschien nach dem Neustart nicht wieder, allerdings entstand in einem anderen Chunk ein zusätzliches Erz. Ein gleicher Test der früheren Generierungsphase zeigte dasselbe Muster. Das ist kein echter Werkzeugabbau und testet weder Drops noch Glück oder Behutsamkeit. Auch Bodenplatzierung allein beseitigt die offene Frage somit noch nicht sicher.

Ein Gegenversuch ersetzte die zufälligen Höhlenplatzierungspositionen durch ein festes Raster mit Abständen von vier Blöcken horizontal und acht vertikal, weiterhin nur mit Bodenplatzierung. In drei von vier Bereichen blieben die Erze nach Neustart gleich, im vierten entfielen zwei und drei kamen hinzu. Das Raster löst das Problem damit nicht zuverlässig. Zudem lagen in einem Test alle 23 freiliegenden Erze auf durch vier teilbaren X- und Z-Koordinaten: Das ist ein erkennbares Muster und keine geeignete Freigabekonfiguration.

Eine weitere Kombination aus festem Raster, Bodenplatzierung und `after_underground_pass` wurde im gleichen Tropfsteinhöhlengebiet viermal getestet. Zwei unveränderte Welten blieben nach Neustart stabil. In zwei Welten wurde je ein Erz mit `setblock` entfernt: Beide entfernten Erze blieben weg; in einem dieser Versuche verschwanden aber zusätzlich zwei andere Erze nach dem Neustart. Damit besteht die Abweichung auch bei dieser Kombination fort.

Zur Unterscheidung zwischen Erz- und Umgebungsänderungen wurde anschließend für jeden Chunk ein Fingerabdruck der Blocktypen im Bereich Y=−64 bis 16 gemessen; Diamanterze werden dafür auf ihren jeweiligen Grundblock normalisiert. Ergänzend wurden die Blocktypen gezählt. In zwei separaten Vanilla-Kontrollwelten blieben zwar alle Diamanterze an ihren Positionen, aber in je drei der vier Chunks änderten sich die Fingerabdrücke. In einem Chunk nahm beispielsweise die Anzahl Tiefenschieferblöcke um 65 zu und die Anzahl Tropfsteinblöcke um 53 ab; außerdem änderten sich Luft- und Wassermengen. Dies sind Nettoänderungen pro Typ, kein vollständiger Positionsnachweis. Der Fingerabdruck ist nicht kollisionsfrei und berücksichtigt keine Blockzustände. Er zeigt, dass die untersuchte Umgebung auch ohne Add-on zwischen den Scans unterschiedlich war; ob dies durch Chunk-Neugenerierung, nachlaufende Platzierungen oder den Messaufbau entsteht, bleibt offen. Höhlenplatzierung kann davon beeinflusst werden, aber der genaue kausale Zusammenhang ist nicht belegt.

Microsoft dokumentiert inzwischen ausdrücklich, dass Bedrock nahe Chunks erzeugt, aber nur bei relevanten Änderungen speichert; beim erneuten Betreten können manche daher neu erzeugt werden: https://learn.microsoft.com/en-us/minecraft/creator/documents/biomes/custompartialbiomereplacement?view=minecraft-bedrock-stable. Das stützt die Neugenerierung als Erklärung des beobachteten Verhaltens, beweist aber nicht den Ablauf jedes einzelnen Blocks. In allen vier bisherigen `setblock ... air`-Abbauproben blieb der entfernte Diamantblock nach Neustart weg; im jeweils veränderten Chunk gab es darüber hinaus keine Änderungen an den gemessenen Diamanterzpositionen. In zwei Proben erschien je ein Erz in einem anderen Chunk, in einer weiteren verschwanden zwei Erze in einem anderen Chunk, in einer gab es keine solche Änderung. Dies ist eine kleine Stichprobe, kein tatsächlicher Abbau durch einen Spieler und kein Realm-Test.

Ein weiterer Paarvergleich mit Blockfingerabdrücken zeigte in der unveränderten Vanilla-Kontrolle Änderungen in zwei Chunks. In der Add-on-Welt, in der vor dem Neustart in jedem der vier Chunks eine Markierung gesetzt wurde, blieben alle vier normalisierten Fingerabdrücke und alle Diamanterzpositionen gleich. Dies passt zum dokumentierten Speichermodell; ein Fingerabdruck ist dennoch kein kollisionsfreier Nachweis für alle Blockdaten.

### Aktivierung in einer bereits erkundeten Testwelt

Zwei Vanilla-Welten mit Seed 98765 wurden im selben Bereich erzeugt und gescannt. Anschließend wurde das kombinierte Testpack aktiviert und derselbe Bereich nach Serverneustart erneut gescannt. In der unmarkierten Welt waren von zuvor 41 Diamanterzpositionen 29 nicht mehr vorhanden; 23 neue Positionen kamen hinzu (35 insgesamt). In der Kontrollwelt mit zuvor je einem gesetzten Goldblock pro Chunk blieben alle 41 Positionen, Typen und Freilegungszustände gleich. Dies betrifft nur vier Chunks je Welt und ist keine globale Aussage, belegt aber: „Alle zuvor einmal gesehenen Gebiete bleiben nach Aktivierung unverändert“ kann mit diesem Ansatz nicht zugesichert werden. Microsofts dokumentierte Behandlung nicht gespeicherter Chunks liefert eine plausible Erklärung. Gespeicherte und nur betrachtete, erneut generierbare Chunks sind auseinanderzuhalten.

Zwei weitere Aktivierungsversuche ohne Markierung bestätigten das Muster: Bei Seed 42 wurden von 38 vorherigen Positionen acht entfernt und elf neue erzeugt; bei Seed 12345 wurden von 70 vorherigen Positionen 56 entfernt und 26 neue erzeugt. Bei einer zweiten markierten Kontrollwelt mit Seed 42 blieben alle 38 Positionen, Typen und Freilegungszustände gleich. Jeweils vier Chunks; keine Aussage zu allen möglichen Welten und kein Realm-Test. Reproduktion nach EULA-Zustimmung:

```sh
python3 tools/compare_worlds.py --diagnose --combined-test --activation-check --chunks 2 --seed 98765 --chunk-x -500 --chunk-z 300
python3 tools/compare_worlds.py --diagnose --combined-test --activation-check --mark-baseline-chunks --chunks 2 --seed 98765 --chunk-x -500 --chunk-z 300
```

Die Befehle überschreiben den angegebenen Bereich vollständig und sind ausschließlich in einer wegwerfbaren Testwelt auszuführen. Die letzte Zeile zählt und ersetzt die verbliebenen Erze.

## Ergänzende direkte Engine-Tests

- Für beide Erztypen wurden je sechs Einzeltests mit Luft an den sechs Nachbarseiten durchgeführt. In allen zwölf Fällen blieb das Erz erhalten; der direkte Feature-Aufruf meldete erwartungsgemäß, dass dort kein Ersatz platziert werden konnte.
- Zusätzlich wurden für beide Erztypen je vier Tests mit den über `setblock` gesetzten Blocktypen `water`, `flowing_water`, `lava` und `flowing_lava` an einer Nachbarseite durchgeführt. Alle acht Erze blieben erhalten. Ob Minecraft fließende Flüssigkeiten zwischen Setzen und Test verändert hat, wurde nicht gesondert überprüft; dies sind daher keine vollständigen Flüssigkeitstests.
- Die vollständige Feature-Regel `cavediamonds:thin_overworld` wurde mit `/place featurerule` direkt aufgerufen. Von 11.760 künstlich eingeschlossenen Tiefenschiefer-Diamanterzen blieben 1.193 übrig: 10.567 ersetzt, 89,855 %. Das entspricht dem vereinbarten Bereich. Ein direkter Befehlsaufruf weist weiterhin nicht nach, dass die Regel in allen natürlichen Biomen automatisch ausgelöst wird.

## Automatisierter Vergleich natürlich generierter Welten

Für jeden Seed wurden zwei eigenständige neue Testwelten mit identischer Serverversion und identischem Seed erzeugt. Ein separates reines Diagnose-Behavior-Pack liest nach der Generierung Erzkoordinaten und die sechs Nachbarn aus. Es verändert keine Blöcke und gehört nicht zum Produktionsprototyp. Gemessen wurden pro Welt 16 Chunks (64 × 64 Blöcke) im Höhenbereich −64 bis 16. Der durch den Seed bedingte Weltbereich ist klein; keine Hochrechnung auf alle Biome oder das Spielerlebnis.

| Seed | Erze Vanilla | Davon eingeschlossen | Erze mit Add-on | Eingeschlossene Erze entfernt | Freiliegende Vanilla-Erze erhalten |
| --- | ---: | ---: | ---: | ---: | ---: |
| 42 | 201 | 199 | 111 | 90 (45,2 %) | 2 von 2 |
| 98765 | 244 | 241 | 107 | 137 (56,8 %) | 3 von 3 |
| 12345 | 316 | 312 | 146 | 170 (54,5 %) | 4 von 4 |

Bei den 761 ursprünglich gefundenen Erzpositionen sind in den jeweiligen Add-on-Welten keine neuen Erzpositionen festgestellt worden. Die neun freiliegenden Vanilla-Erze blieben an ihren Positionen bestehen; die Stichprobe ist für eine weitreichende Aussage zu klein.

Ein wiederholter Durchlauf von Seed 42 ergab in der Vanilla-Welt erneut dieselben 201 Positionen. Mit Add-on wurden 108 statt 111 Erze gezählt; 13 Positionen unterschieden sich zwischen beiden Add-on-Läufen. Ursache unbekannt. Auch deshalb darf aus einem einzelnen Testlauf keine Garantie abgeleitet werden.

Zum Eingrenzen der Ursache wurde das Raster auf einer weiteren bereits fertig generierten Add-on-Testwelt (Seed 42) einmal manuell pro Chunk erneut angewendet. Von 109 verbliebenen eingeschlossenen Erzen wurden dabei 96 entfernt (88,1 %); beide freiliegenden Erze blieben erhalten. Damit kann der Filter die meisten später verbliebenen Erze nachträglich erreichen. **Warum der automatische Durchlauf sie zunächst nicht erfasst, ist noch ungeklärt**; Generierungszeitpunkt, Reihenfolge und Abdeckung sind mögliche Ursachen, aber nicht bewiesen.

### Modell für gerade Tunnel auf Y=−57

Als zusätzliche Auswertung wurden pro Seed 62 alternative, jeweils 64 Blöcke lange und zwei Blöcke hohe gerade Tunnel durch die erfassten Positionen modelliert. Gezählt wurden Erze im Tunnel oder direkt an Wänden, Boden und Decke. Die alternativen Tunnel überlappen; ein Erz kann in mehreren Varianten gezählt werden. Dies sind keine unabhängigen Spielrunden und keine Diamanten-pro-Stunde-Messung.

| Seed | Erz-Kontakte Vanilla | Erz-Kontakte Add-on |
| --- | ---: | ---: |
| 42 | 33 | 15 |
| 98765 | 32 | 22 |
| 12345 | 68 | 22 |

Das Modell berücksichtigt insbesondere keine Aderausbeutung, Höhleneingänge, Lava, Bewegung, Werkzeuge oder Höhlensuche. Aus diesen Zahlen lässt sich nicht ableiten, ob Höhlen pro Spielstunde doppelt so ergiebig sind.

### Neue Zielvorgabe und Status

Die 90-%-Ausdünnung war ein Ausgangswert und ist keine nachgewiesene Voraussetzung für die gewünschte Balance. Die neue Zielvorgabe lautet: **Höhlenerkundung soll ungefähr doppelt so ergiebig pro Zeit wie Tiefenschiefer-Tunnelbau sein.** Dazu fehlt eine belastbare Vergleichsmessung beider Spielweisen. Ob 90 % dafür zu viel oder zu wenig sind, ist offen.

Die aktuelle technische Konfiguration erzielt bei natürlicher Generierung nicht die eingestellten 90 % und ist in ihrer Wirkung noch nicht hinreichend verstanden. Kein Produktionspaket oder Realm-Freigabe. Direkte Nachbearbeitung ganzer Chunks nach dem Laden ist nur ein diagnostischer Test, keine freigegebene Lösung für bestehende Spielwelten.

Reproduzierbarer Test, nach Docker-Start und EULA-Zustimmung, erzeugt ausschließlich neue Testwelten unter `data/research/`:

```sh
python3 tools/compare_worlds.py --seed 42 --chunks 4 --diagnose
python3 tools/compare_worlds.py --seed 42 --chunks 4 --diagnose --reapply
```

`ore_scan.json` enthält Positionen, Erztypen und Nachbarblöcke; beim zweiten Befehl wird zusätzlich `ore_scan_after_reapply.json` abgelegt. Die Testwelten sind nicht zur Nutzung als Spielwelt bestimmt.

## Weiterführende Ursachenanalyse und alternativer Forschungsansatz

Alle folgenden Varianten sind ausschließlich temporäre Forschungspacks unter `data/research/`; das ursprüngliche Pack unter `prototype/behavior_pack` wurde dadurch nicht zur freigegebenen Lösung. Alle Angaben beziehen sich auf Bedrock Dedicated Server 1.26.61.1 und die untersuchten kleinen Ausschnitte.

### Automatische Nachbearbeitung

Bei einer Diagnosevariante, die alle geeigneten vergrabenen Erze statt 90 % ersetzen sollte, wurden bei Seed 42 zunächst 97 von 199, bei Seed 98765 147 von 241 erfasst. Ein erneuter direkter Aufruf auf der fertig erzeugten Welt entfernte die jeweils verbleibenden 102 beziehungsweise 94 Erze. Auch ohne Nachbarschaftsfilter blieb das automatische Ergebnis unvollständig.

Marker zeigten in einem untersuchten Bereich jeweils einen Regelursprung in allen 16 Chunks. Ein separater Rastertest im Himmel erfasste in vier Chunks alle 82.944 vorgesehenen Positionen (4 × 20.736). Das belegt weder identisches Verhalten unterirdisch noch die Generierungsreihenfolge an Chunkgrenzen. Ein weiterer Versuch markierte Gestein unterirdisch; dabei änderten sich auch Erzvorkommen, obwohl der Marker nur Gestein ersetzen sollte. Das spricht für Wechselwirkungen mit weiteren Generierungsschritten; der Marker kann diese Schritte selbst beeinflussen. Eine konkrete interne Ursache ist nicht nachgewiesen. Die Dokumentation nennt `final_pass` als letzten Feature-Pass, garantiert aber nicht, dass zu diesem Zeitpunkt in benachbarten Chunks bereits alle später wirksamen Änderungen abgeschlossen sind: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/featuresintroduction?view=minecraft-bedrock-stable

### Erforschtes Ersetzen der Erzgenerierung

Minecraft dokumentiert das Überschreiben gleich benannter Features durch höher priorisierte Behavior-Packs. Eine Testvariante ersetzte die drei eingebauten Features `minecraft:diamond_ore_feature`, `minecraft:diamond_ore_large_feature` und `minecraft:diamond_ore_buried_feature` durch wirkungslose Versionen. In jeweils 16 Chunks entstanden bei den Seeds 42, 98765 und 12345 keine Diamanterze, gegenüber 201, 244 und 315 in den jeweiligen Referenzwelten. Dies belegt nicht, dass damit weltweit jede andere Quelle ausgeschaltet ist; insbesondere Fossilien, weitere Biome und zukünftige Versionen sind offen. Das Überschreiben kann außerdem mit anderen Add-ons kollidieren.

Eine weitere Testvariante erzeugte vereinzelt normale Diamanterze im Gestein. Ein separater Versuch mit `minecraft:snap_to_surface_feature` platzierte in drei Bereichen mit je 16 Chunks 157, 173 und 51 Erze; bei der abschließenden Messung grenzten alle 381 an Luft oder Flüssigkeit. Ein angrenzender Hohlraum kann jedoch klein, unzugänglich oder mit Flüssigkeit gefüllt sein; damit ist eine spielerisch erreichbare Höhle noch nicht nachgewiesen. Die Versuchsmenge war bewusst hoch und ist keine Balanceempfehlung. Das in diesen Versuchen verwendete `embed_in_surface` ist laut Microsoft erst seit Formatversion 1.26.20 verfügbar: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_snap_to_surface_feature?view=minecraft-bedrock-stable

Die Kombination beider Bausteine erzeugte in drei Gebieten mit je 16 Chunks bei Seed 42 insgesamt 179 Erze (157 freiliegend, 22 vergraben), bei Seed 98765 195 (167 freiliegend, 28 vergraben), bei Seed 12345 78 (52 freiliegend, 26 vergraben). Die Referenz hatte jeweils 201, 244 und 315 Erze. Diese Erze entstehen an neuen Positionen: Vorhandene natürlich generierte Höhlenerze und vollständige Adern werden mit diesem Ansatz nicht garantiert erhalten. Die unterschiedlichen Erzmengen belegen keine Erträge pro Spielstunde.

Ein zusätzlicher Bereich an den Chunk-Koordinaten −12/−9 mit jeweils 16 Chunks lieferte für Seed 42 in Vanilla 204 Diamanterze, mit der Kombination 166 (148 freiliegend, 18 vergraben). Für Seed 98765 waren es 294 gegenüber 85 (54 freiliegend, 31 vergraben). Damit wurden beide Bausteine auch bei negativen Koordinaten beobachtet; dies ist noch kein Nachweis für alle Chunk-Grenzen oder Erkundungsrichtungen.

Weitere Kontrollen: Bei Seed 42 und Chunk −12/−9 enthielt eine eigene Welt mit ausschließlich abgeschalteten Vanilla-Diamantfeatures kein Diamanterz, die Referenz 204. In einem anderen Bereich bei Chunk 100/80 und Seed 12345 enthielt die kombinierte Variante 194 Diamanterze (170 freiliegend, 24 vergraben), die Referenz 298. Ein ergänzender Zähler für Blocktypen mit Endung `_ore`, ohne Diamanterze, fand beim ersten Vergleich gleiche Anzahlen für alle erfassten Erztypen; beim zweiten Unterschied lediglich bei Tiefenschiefer-Lapiserz (203 Vanilla, 204 Testvariante). Dies sind Anzahlen ohne Positionsabgleich und keine Garantie, dass andere Erze oder Strukturen unverändert sind; auch natürliche Streuung beziehungsweise Generierungsreihenfolge ist nicht ausgeschlossen.

Ein Test der vermeintlichen Nachbarschaftsprüfung `may_attach_to` wurde verworfen: Bei einem direkten Negativtest platzierte die untersuchte Richtungsvariante auch ohne benachbarte Luft Erz; ein natürlicher Test produzierte überwiegend vergrabene statt freiliegende Erze. Dies darf nicht als funktionsfähiger Höhlenfilter verwendet werden.

Reproduktion der Kombination, nach ausdrücklicher Zustimmung in `.env`:

```sh
python3 tools/compare_worlds.py --diagnose --combined-test --seed 42 --chunks 4
python3 tools/compare_worlds.py --diagnose --combined-test --seed 42 --chunks 4 --chunk-x -12 --chunk-z -9
```

Die Vergleichszahlen für erhaltene frühere Positionen im Werkzeug sind für diese neu generierende Variante nicht als Erhaltungsquote zu interpretieren. Offen bleiben insbesondere Generierungsreihenfolge und Chunkgrenzen, andere Erzarten und Strukturen, viele Biome, Versionen, Verhalten nach Speichern und Neustart, Leistung, tatsächlich erreichbare Höhlen und Spielbalance sowie Realm- und Konsolentest. Keine Freigabe und kein `.mcpack`.

## Erweiterte Engine-Prüfung: Biome, Hohlräume, Reihenfolge und Neustart

Die folgenden Untersuchungen verwenden ebenfalls ausschließlich den lokalen Testserver 1.26.61.1 und neue Testwelten. Die Biome wurden durch die Diagnose-Script-API an vier Höhen und im Abstand von vier Blöcken sowie an jeder Erzposition ermittelt. Das Testscript wird nicht Teil des Produktionspakets. Ein Biomeintrag bedeutet nur, dass dieses Biom im jeweiligen Ausschnitt vertreten war, nicht dass das gesamte Biom oder alle Vorkommen untersucht wurden.

| Seed und Startchunk | Untersuchte Biome unter anderem | Diamanterze Vanilla | Eigene Erze insgesamt | Davon an Luft/Flüssigkeit |
| --- | --- | ---: | ---: | ---: |
| 42, 0/0 | Üppige Höhlen, dunkler Wald, Fluss, Strand | 38 | 27 | 23 |
| 42, 500/−500 | Steinstrand, Fluss | 92 | 44 | 37 |
| 98765, −500/300 | Tropfsteinhöhlen, Blumenwald | 41 | 33 | 32 |
| 12345, 1000/1000 | kalter Ozean, Strand | 81 | 18 | 15 |
| 24680, −1000/1000 | tiefer kalter Ozean, üppige Höhlen | 236 | 282 | 269 |
| 42, 1/−35 | Deep Dark, Birkenwald, dunkler Wald | 295 | 72 | 38 |

Die ersten vier Bereiche umfassen je 2 × 2, die letzten beiden je 4 × 4 Chunks. In den untersuchten Gebieten wurden in üppigen Höhlen 22 und in Tropfsteinhöhlen 30 eigene Erze an diesen Biompositionen gefunden. Im Deep-Dark-Ausschnitt wurden sieben Erze im eigentlichen Deep-Dark-Biom gefunden, alle ohne direkten Luft- oder Flüssigkeitskontakt. Auch im Vanilla-Vergleich gab es in dem gesamten Ausschnitt kein freiliegendes Erz. Ob die Höhlenbeschaffenheit dort keine Platzierung erlaubte oder ein systematisches Problem vorliegt, ist offen und braucht gezielte Tests an Höhlenoberflächen, insbesondere mit Sculk. Für die übrigen Gebiete ist die Biomverteilung in den jeweiligen `ore_scan.json` gespeichert. Die Mengen sind Testparameter, keine Balancevorschläge.

Bei einer nachträglichen Oberflächenzählung im gleichen Deep-Dark-Ausschnitt fanden sich nur 14 Luftkontakte zu Tiefenschiefer und überwiegend zu Amethystblöcken beziehungsweise Knospen; der Test sah dort keine Sculk-Luftkontakte. Somit enthält dieser Ausschnitt wenig nach aktuellem Testpack erlaubte Höhlenoberfläche. Das erklärt plausibel die geringe Zahl möglicher Platzierungen, ist aber kein Beweis für korrektes Verhalten in einem größeren, tatsächlich zugänglichen Deep-Dark-Höhlensystem. Die Testvariante lässt aktuell nur Stein und Tiefenschiefer als Einbettungsflächen zu, keinen Sculk.

Die Diagnose betrachtet nun außerdem benachbarte zusammenhängende Luftblöcke, begrenzt auf den Messbereich und mindestens 64 Blöcke für die Klassifikation „groß“. In den Gebieten Seed 42 bei 0/0 und Seed 98765 bei −500/300 traf das auf alle 12 beziehungsweise 28 Erze mit Luftkontakt zu. Von den 23 freiliegenden Erzen im ersten Gebiet hatten 10 Wasserkontakt und eines Lavakontakt. Im Tropfsteingebiet hatten 6 Wasserkontakt; einzelne Erze können mehrere Kontaktarten haben. Auch ein größerer Luftraum beweist keine Erreichbarkeit durch einen Spieler oder eine Verbindung zur Oberfläche. Wasserkontakt bedeutet nicht zwingend eine unzugängliche Stelle.

Andere Blocktypen mit der Endung `_ore` wurden in fünf Vergleichen gezählt. In vier stimmten alle erfassten Anzahlen überein; im fünften gab es bei Eisen und Tiefenschiefereisen je einen Block Unterschied (264/263 und 571/570). Positionen und alle anderen Blöcke wurden nicht vollständig abgeglichen. Dies beweist weder eine direkte Ursache noch allgemeine Unveränderlichkeit.

Bei Seed 24680, Chunk −1000/1000, wurden zwei Welten mit versuchsweise umgekehrter Reihenfolge der chunkspaltenweisen Vorladung erzeugt. Beide Add-on-Welten enthielten 283 Erze an denselben Positionen und mit denselben direkten Nachbarblöcken; die jeweiligen Vanilla-Vergleiche enthielten 236 Erze. Die Zeit zum Vorladen wurde begrenzt abgewartet, ohne einen expliziten Abschluss jeder einzelnen Chunkgenerierung nachzuweisen. Es handelt sich deshalb um ein positives Beispiel, nicht um einen vollständigen Test sämtlicher Erkundungsrichtungen oder Chunkgrenzen. In älteren 4×4-Tests variierte der Anteil der Erze an Chunk-Rändern; ob das auf die Höhlenverteilung oder ein systematisches Platzierungsmuster zurückgeht, ist offen.

Bei zwei Neustartprüfungen nach 15 Sekunden Wartezeit war ein Fall unverändert, in einem anderen fehlte nach dem Neustart ein Erz. Zwei Wiederholungen desselben zweiten Seeds zeigten erneut Veränderungen von je einem entfernten und in einem Fall zusätzlich einem hinzugekommenen Erz, jeweils an unterschiedlichen Positionen. Die Ursache ist unbekannt: Neben Persistenz kommt insbesondere eine vor dem ersten Scan nicht abgeschlossene Generierung oder Blockaktualisierung infrage. Die Ergebnisse rechtfertigen keine Freigabe. Der erste Versuch des Neustartwerkzeugs scheiterte zunächst an einer eigenen zeitgleichen Ticking-Area-Änderung; dieser Testfehler wurde behoben und ist nicht als Minecraft-Befund gewertet.

Auch längeres Warten löste den Befund nicht: Bei zwei weiteren Durchläufen desselben Tropfsteinhöhlen-Ausschnitts mit 60 Sekunden Wartezeit vor jedem Scan kam nach dem Neustart in einem Fall ein Erz hinzu; im anderen fehlten vier und drei kamen hinzu. Die Unterschiede betreffen einzelne Positionen, nicht alle Erze. Daraus lässt sich nicht ablesen, ob der Neustart selbst, fortgesetzte Generierung, Speichern nicht veränderter Chunks, natürliche Blockupdates oder eine Eigenart des Diagnoseverfahrens verantwortlich ist. Ein bloßes Zeitlimit belegt keinen Abschluss der Generierung. Insbesondere ist **Stabilität nach Neustart bislang nicht nachgewiesen**.

In zwei anschließenden Paarvergleichen wurden sowohl Vanilla- als auch Add-on-Welt neu gestartet: Die beiden Vanilla-Welten zeigten keine hinzugekommenen oder entfernten Diamanterze; bei den zwei Add-on-Welten verschwand je ein Erz und an anderer Stelle kam je eines hinzu. Das ist ein Hinweis auf eine Interaktion mit der Testvariante oder deren Testablauf, aber keine vollständige Ursachenanalyse und kein Beweis, dass alle Vanilla-Welten unverändert bleiben.

Zwei zusätzliche Add-on-Welten desselben Tropfsteinhöhlen-Seeds wurden zunächst nach 30 Sekunden ohne Neustart erneut gescannt: Beide hatten dabei dieselben Erzpositionen, Typen und Freilegungszustände. Nach anschließendem Neustart blieb eine dieser Welten bei dieser Messung unverändert; in der anderen kam ein Erz hinzu. Dieser begrenzte Vergleich verstärkt den Verdacht, dass das Laden beziehungsweise Speichern in Verbindung mit der Testvariante relevant ist. Er beweist weder die genaue technische Ursache noch, wie sich ein Realm mit echten Spielern verhält.

In zwei weiteren Wegwerfwelten wurde nach dem ersten Scan je ein Goldblock auf Y=300 in jedem der vier Test-Chunks gesetzt, um diese Chunks ausdrücklich zu verändern. Nach dem Neustart waren in beiden Fällen alle vier Markierungen vorhanden und die Diamanterzpositionen, Typen und Freilegungszustände unverändert. Dies ist ein Hinweis auf einen möglichen Zusammenhang mit dem Speichern beziehungsweise Neugenerieren zuvor nicht veränderter Chunks; er ist nicht bewiesen. Insbesondere darf daraus nicht geschlossen werden, dass die Produktion künstliche Markierungen platzieren soll oder dass echte Spieler beziehungsweise Realms dasselbe Verhalten zeigen.

Reproduktion nach EULA-Zustimmung:

```sh
python3 tools/compare_worlds.py --diagnose --combined-test --air-probe --restart-check --chunks 2 --seed 98765 --chunk-x -500 --chunk-z 300
python3 tools/compare_worlds.py --diagnose --combined-test --preload-direction east --chunks 4 --seed 24680 --chunk-x -1000 --chunk-z 1000
python3 tools/compare_worlds.py --diagnose --combined-test --preload-direction west --chunks 4 --seed 24680 --chunk-x -1000 --chunk-z 1000
```

## Nachjustierung V20–V23 (4. November 2026)

V20 änderte nur `scatter_chance` der tiefen V19-Feature-Regel von 50 auf 70. V21 ergänzte eine tiefe Regel mit `scatter_chance` 0.3. Beide ergaben in je 20 Kalibriergebieten dieselben Gesamtwerte wie V19: 29/23 Luftkontaktgruppen, 31/118 eingeschlossene Erze auf Y=−57 und 202/1103 Tunnelkontakte; 19/20 Gebietsanalysen waren identisch. Der Grund ist nicht geklärt. Laut [Microsofts Feature-Regel-Referenz](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/feature_rule_definition?view=minecraft-bedrock-stable) liegen solche Wahrscheinlichkeiten zwischen 0 und 1; frühere Werte 50 und 70 dürfen daher nicht als gesicherte Prozentwerte ausgegeben werden. Die Engine-Wirkung bleibt separat zu prüfen.

V22 ergänzt eine Regel im Höhenband −52..−41 ohne gesetztes `scatter_chance`. Die 20 Gebiete enthalten 34/23 Luftkontaktgruppen (147,8 %), 31/118 eingeschlossene Erze auf −57 (26,3 %) und 202/1103 Tunnelkontakte (18,3 %). V22 verändert damit mindestens im untersuchten Vergleich die Höhlenfundzahl, liegt aber in dieser kleinen Kalibrierstichprobe über dem Arbeitskorridor. Pack-Hash: `e1548ddfcb9e2f57afa3211ccc2a19aa3853f31c87601608e3271127861a978f`.

V23 verwendet denselben Zusatzbereich mit `scatter_chance: 0.4` und ergab 20/20 dieselben Gesamtwerte wie V19. V24 verwendet stattdessen den Zahlenwert `40`: In 20 Kalibriergebieten 32/23 Gruppen (139,1 %), 31/118 eingeschlossene Y=−57-Erze (26,3 %), 202/1103 Tunnelkontakte (18,3 %); Gruppengrößen 1/2/3/4/5 = 4/6/16/5/1. Die Wirkung ist empirisch, keine Bestätigung einer exakten Prozentwahrscheinlichkeit. V24 wurde trotz der hohen Kalibrierquote als Kandidat für einen neuen Holdout eingefroren, da V19 auf derselben kleinen Kalibrierung ebenfalls hoch lag und im großen Holdout nur 101,2 % erreichte. Diese frühere Messung hat die Auswahl beeinflusst und ist keine unabhängige Bestätigung von V24.

Der vorab festgelegte V24-Holdout (`reference/balance-holdout-plan-2026-11-04-v24.json`, Pack-Hash `de14344d983552f58f5e2f4075e63def5e1ca910d3ef250885268e76e0259832`) umfasste sechs neue Seeds und 1.536 Chunks. Vanilla zuerst: 144 Luftkontaktgruppen; V24: 157 (109,0 %). Eingeschlossenes Erz Y=−57: 114/674 (16,9 %); überlappendes Tunnelmodell 845/5225 (16,2 %). V24-Gruppen 1/2/3/4/5 = 18/48/61/28/2. Verhältnis der Gruppen je Seed in Planreihenfolge: 26/20, 37/31, 35/33, 25/14, 29/32, 5/14. Das sind keine Spielzeiterträge oder Erreichbarkeitsnachweise.

Gebiets-Bootstrap (10.000 Wiederholungen, sechs vollständige Gebiete als Einheiten): 2,5–97,5-%-Perzentile 85,6–133,6 % für Gruppen, 11,6–24,1 % für Y=−57 und 12,4–21,3 % für Tunnelkontakte. Der große Bereich erlaubt keine präzise Aussage, dass das tatsächliche Plus genau 9 % beträgt. Von 327 luftberührten V24-Blöcken lagen 196 bei X modulo 16 = 0–7 und 131 bei 8–15; bei Vanilla 72/89 von 161. Zusammenhängende Erzblöcke sind nicht unabhängig, daher ist das kein Nachweis eines ausnutzbaren Musters. Gruppenbasierte zusätzliche Untersuchung ist offen.

Auf Gruppenebene haben 92 V24-Luftkontaktgruppen ihre luftberührten Blöcke ausschließlich bei X modulo 16 = 0–7, 57 ausschließlich bei 8–15 und acht auf beiden Seiten; Vanilla 66/77/1. Die Gruppen sind flächig verbundene Komponenten innerhalb des Scanbereichs, keine sicheren natürlichen Adern. Die Beobachtung ist ein Hinweis auf eine mögliche Chunk-Koordinatenpräferenz und muss mit zusätzlichen unabhängigen Gebieten geprüft werden.

Kontrollierte Oberflächenproben ergaben bei Boden, Wand und Decke jeweils 3/3 erfolgreiche Platzierungen. Eine simulierte Entfernung per `setblock air` blieb nach Neustart entfernt; es traten keine weiteren Diamantpositionsänderungen in dieser Probe auf. Das testet keinen echten Spielerabbau. Alle Varianten bleiben Teststände; Realm, Spielzeiten, Mehrspielerlast, Werkzeuge und Verzauberungen sind offen. Der Nutzer akzeptiert ungefähr 10 % zusätzliche Höhlenfundstellen als Richtwert.

## Balancevarianten V9–V19 und Holdouts (4. November 2026)

Die Varianten V9 bis V19 wurden jeweils in einem eigenen Behavior-Pack und Ergebnisordner erzeugt. Kein Ergebnis überschreibt eine ältere Variante. Die Sammeltests verwenden dieselbe Vanilla-Referenz mit 20 Kalibriergebieten, 320 Chunks und Bedrock Dedicated Server 1.26.61.1.

| Variante | Luftkontaktgruppen Kandidat/Vanilla | Y=-57 Kandidat/Vanilla | Tunnelkontakte Kandidat/Vanilla | Gruppengrößen 1/2/3/4/5 | Befund |
| --- | ---: | ---: | ---: | ---: | --- |
| V9 | 42/23 (182,6 %) | 21/118 (17,8 %) | 125/1103 (11,3 %) | 1/17/11/9/4 | zu viele Fundstellen |
| V10 | 14/23 (60,9 %) | 21/118 (17,8 %) | 125/1103 (11,3 %) | 2/6/4/2/0 | zu wenige; Richtungshypothese unbewiesen |
| V11 | 14/23 (60,9 %) | 21/118 (17,8 %) | 125/1103 (11,3 %) | 3/3/5/3/0 | zu wenige |
| V12 | 16/23 (69,6 %) | 21/118 (17,8 %) | 125/1103 (11,3 %) | 3/5/5/3/0 | zu wenige |
| V13 | 32/23 (139,1 %) | 21/118 (17,8 %) | 125/1103 (11,3 %) | 2/6/15/7/2 | zu viele |
| V14 | 21/23 (91,3 %) | 21/118 (17,8 %) | 125/1103 (11,3 %) | 1/9/6/4/1 | knapp zu wenige, zu viele Zweier |
| V15 | 25/23 (108,7 %) | 21/118 (17,8 %) | 125/1103 (11,3 %) | 1/10/8/5/1 | Kalibrierung passend |
| V16 | 58/23 (252,2 %) | 21/118 (17,8 %) | 125/1103 (11,3 %) | nicht separat im Bericht | verworfen; `scatter_chance: 0` schaltet nicht sicher aus |
| V17 | 42/23 (182,6 %) | 21/118 (17,8 %) | 125/1103 (11,3 %) | nicht separat im Bericht | verworfen; obere Regel weiterhin aktiv |
| V18 | 25/23 (108,7 %) | 21/118 (17,8 %) | 125/1103 (11,3 %) | 3/5/11/5/1 | obere Regel entfernt |
| V19 | 29/23 (126,1 %) | 31/118 (26,3 %) | 202/1103 (18,3 %) | 3/7/13/5/1 | aktueller lokaler Kandidat |

V15-Holdout: sechs neue vorab festgelegte Gebiete, 1.536 Chunks, 159 Vanilla-Gruppen. V15 erzeugte 135 Gruppen (84,9 %), 74/644 Y=-57-Erze (11,5 %) und 620/5207 Tunnelkontakte (11,9 %). V18-Holdout: 176 Vanilla-Gruppen; V18 erzeugte 123 (69,9 %), 51/715 Y=-57-Erze (7,1 %) und 458/5790 Tunnelkontakte (7,9 %). Beide Holdouts sind in separaten Referenz- und Ergebnisdateien gespeichert und bleiben als Negativbefunde erhalten.

V19-Holdout: `reference/balance-holdout-plan-2026-11-04-v19.json` wurde vorab mit sechs neuen Seeds festgelegt. Vanilla und V19 wurden danach in denselben 1.536 Chunks erzeugt. Vanilla: 164 luftberührte Gruppen, 660 eingeschlossene Y=-57-Erze, 5.598 Tunnelkontakte. V19: 166 Gruppen (101,2 %), 112 Y=-57-Erze (17,0 %), 803 Tunnelkontakte (14,3 %). Gruppengrößen im Holdout waren für V19 25/44/66/27/4 (1/2/3/4/5). Die Fundstellenquote liegt leicht unter dem vorläufigen Korridor 105–125 %, aber nahe am Vanilla-Mittel; zusammen mit der Kalibrierung ergibt sich 195/187 = 104,3 %. Das ist kein Beleg für 15 % pro Welt und keine Freigabe.

`tools/holdout_uncertainty.py` resampelt vollständige Gebiete/Seeds als Einheiten (10.000 Wiederholungen, fester Seed 0). Für V19 liegen die 2,5–97,5-%-Intervalle bei 82,1–123,2 % der Gruppen, 11,3–22,7 % Y=-57 und 11,3–17,8 % Tunnelkontakten. Die große Streuung ist ein wesentlicher offener Balancepunkt.

### Scanner- und technische Kontrollen

Der große Scanner wurde repariert: `ticking_area_windows()` lädt Kernfläche plus horizontale Nachbarn in Fenstern mit höchstens 100 Chunks. Automatisierte Tests prüfen 4, 8, 9, 10 und 16 Chunks, negative Koordinaten und Randabdeckung. Ein 16×16-Vanilla-Lauf sowie alle großen Holdouts liefen vollständig und ohne abgeschnittene Scanantwort. Die Diagnose bricht bei Serverabbruch statt stillschweigend unvollständige Blöcke zu verwenden.

Für V19 wurden in `experiments/balance-v19/verification/` direkte Boden-, Decken- und Wandproben, zwei simulierte Abbau-/Neustartproben, ein Ost-/West-Vorladevergleich sowie ein gezielter Erzpositionsvergleich gespeichert. Der Vorladevergleich fand in einer negativen 4×4-Region identische 83 Erzpositionen. Der Erzvergleich zeigte eine zusätzliche Tiefenschiefer-Lapisposition; die Zusicherung unveränderter anderer Erze bleibt daher offen. `setblock air` ist kein echter Spielerabbau. Werkzeuge, Verzauberungen, Explosionen, Leistung, gleichzeitige Spieler und Realm/Konsolen sind nicht automatisiert bestätigt.

### Freigabestatus

V19 ist ein lokal geprüfter Kandidat, kein freigegebenes Add-on. Es existiert kein importierbares Produktions-`.mcpack`. Vor einer Veröffentlichung fehlen mindestens echte Spielvergleiche (Tunnel Y=-57 gegen Höhle, je Seed zwei 30-Minuten-Runden), Stabilitäts-/Leistungstests mit zwei Spielern, Versionsabgleich sowie Test-Realm-, PC- und Konsolenprüfung. Andere weltgenerierende Add-ons und experimentelle Weltoptionen bleiben nicht unterstützt.

## Balance-V6: unabhängige Gegenprobe

Am 4. November 2026 wurden zehn vorab festgelegte neue Gebiete mit je 16 Chunks auf Bedrock Dedicated Server 1.26.61.1 sowohl in Vanilla als auch mit dem unveränderten V6-Testpack verglichen. Plan und Baseline liegen unter `reference/balance-holdout-*`, Einzelmessungen und Aggregat unter `experiments/balance-v6/holdout-results/` und `holdout-summary.json`.

Vanilla hatte 23 luftberührte, flächig zusammenhängende Diamanterzgruppen; V6 hatte 15 (65,2 %), obwohl rund 115 % angestrebt waren. Vanilla hatte 13 Einzel-, sieben Zweier-, zwei Vierer- und eine Neunergruppe, V6 zehn Einzel- und fünf Zweiergruppen. Die Gruppen sind nur eine Näherung für Fundstellen, nicht zwingend erreichbare Höhlen oder vollständige natürliche Adern. Auf Y=−57 gab es sieben gegenüber 104 vollständig eingeschlossenen Erzblöcken (6,7 %); ein Modell gerader Tunnel erfasste 47 statt 640 überlappende Erzblockkontakte (7,3 %). Die Stichprobe ist klein und kein Spielzeitvergleich. Der unabhängige Befund stützt die vorherige Kalibrierung nicht; V6 ist nicht freigegeben.

Drei weitere V6-Testwelten wurden per `setblock air` an jeweils einem Erz verändert und neu gestartet. Die entfernten Blöcke erschienen nicht wieder, und die übrigen Diamanterzpositionen der untersuchten Gebiete blieben gleich. Ergebnisdateien: `experiments/balance-v6/verification/mining-*.json`. Das ist kein echter Abbau und keine Bestätigung von Werkzeugen, Verzauberungen, Explosionen oder Realm-Persistenz.

In zwei Gebieten wurden Positionen ausgewählter anderer Erztypen jeweils zwischen zwei unabhängig erzeugten Vanilla-Welten und einer V6-Welt verglichen. Die beiden Vanilla-Scans pro Gebiet waren identisch; im V6-Scan fand sich jeweils ein zusätzliches Tiefenschiefer-Lapiserz an einer Position, die im Vanilla-Scan Diamanterz enthielt. Die Änderung der Diamantgenerierung ist ein plausibler Auslöser, die genaue Engine-Reihenfolge bleibt offen. Das ist ein messbarer Unterschied bei anderen Erztypen und widerspricht dem ursprünglichen Ziel, diese unverändert zu lassen. Die Untersuchung beschränkt sich auf fünf Erztypen und Höhen −64 bis 16. Ergebnisdateien: `experiments/balance-v6/verification/ore-trace-{02,04}.json`.

## V8: Höhen und Höhlenflächen

20 zuvor für die Kalibrierung ausgewählte Referenzgebiete (320 Chunks, Bedrock 1.26.61.1): 42 luftberührte Gruppen gegenüber 23 in Vanilla, 21 gegenüber 118 eingeschlossene Erze auf Y=−57, Tunnelmodell 125 gegenüber 1.103 Kontakten. Das Höhlenziel von rund 115 % ist mit 182,6 % verfehlt. Es handelt sich nicht um einen unabhängigen oder repräsentativen Nachweis. `experiments/balance-v8/status.json` enthält die Höhen- und Flächenzählung; das tiefste Höhenband enthielt trotz stärker gewichteter Startpunkte nur einen sichtbaren Testblock. Kein Diamanterz wurde auf Y=17..40 gefunden, andere Höhen wurden hier nicht untersucht.

In einem künstlichen Hohlraum funktionierte die gezielte Erzplatzierung an Boden, Decke und Wand bei je drei von drei Versuchen. Die gezählte Fläche und die bei natürlicher Generierung luftberührten Erze belegen weder Erreichbarkeit noch einen Realm-Einsatz. Ergebnis `experiments/balance-v8/verification/surface-probes.json`; V8 bleibt nicht freigegeben.

## V24 großer Holdout und technische Nachtests (6. November 2026)

### Unabhängiger 15-Seed-Vergleich

Der große Holdout wurde vorab im Plan `reference/balance-large-plan-2026-11-04-v24.json` festgelegt: 15 Seeds, je 32×32 Kern-Chunks (512×512 Blöcke), insgesamt 15.360 Chunks. Die Vanilla-Referenz wurde zuerst erzeugt und unveränderlich unter `reference/balance-large-v24-1.26.61.1-2026-11-05.json` gespeichert. Danach lief V24 mit exakt denselben Seeds und Koordinaten. Paket-Hash: `de14344d983552f58f5e2f4075e63def5e1ca910d3ef250885268e76e0259832`. Alle Gebiete wurden atomar unter `experiments/balance-large-v24/holdout-results/area-00.json` bis `area-14.json` gespeichert.

| Kennzahl | Vanilla | V24 | V24/Vanilla |
| --- | ---: | ---: | ---: |
| Luftkontakt-Komponenten | 1.630 | 1.730 | 106,1 % |
| eingeschlossene Erze auf Y=−57 | 6.564 | 906 | 13,8 % |
| eingeschlossene Erze Y=−59..−55 | 32.891 | 5.052 | 15,4 % |
| überlappende Modell-Tunnelkontakte | 52.810 | 7.963 | 15,1 % |

Für die Gruppenquote liegt der Punktwert damit knapp über der Untergrenze des Arbeitskorridors 105–125 %, aber unter dem Wunschwert von ungefähr 115 %. Das ist ein zusammengefasster Holdout-Befund, keine Garantie pro Seed und keine Spielzeitmessung. Die gebietsweise Bootstrap-Auswertung liegt in `experiments/balance-large-v24/holdout-uncertainty.json` (20.000 Wiederholungen, feste Zufallsquelle, vollständige Gebiete als Einheiten): Fundstellen 97,7–114,3 %, Y=−57 13,0–14,7 %, Tunnelkontakte 14,3–15,9 % (2,5–97,5-%-Perzentile).

Die Gruppenverteilung des Kandidaten war 1/2/3/4/5/7 = 219/556/643/265/41/6. Drei- und Vierergruppen stellen 908/1.730 = 52,5 %; Zweiergruppen sind einzeln seltener als diese zusammen, Einer und Fünfer sind selten. Die Gruppen sind flächenweise verbundene Messkomponenten und nicht zwingend vollständige natürliche Adern. V24-Luftkontakte nach Höhenband −64..−48/−47..−32/−31..−16/−15..−1/0..16: 400/1.200/781/658/43. Damit ist eine tiefere Gewichtung sichtbar, aber keine harte obere Fundhöhenbegrenzung bewiesen. Der Zusatzscan Y=17..40 fand im Kandidaten 0 Erze; er deckt nur die untersuchten Gebiete und diese Höhen ab.

Die große Referenz enthielt 1.049 von 105.324 Komponenten an der äußeren Scan-Grenze; V24 401 von 42.126. Luftkontaktgruppen an der äußeren Grenze: 10 Vanilla, 19 V24. Diese Fälle bleiben potenziell abgeschnitten. Die 15 Kandidatengebiete enthielten unter anderem üppige Höhlen, Tropfsteinhöhlen, Deep Dark, Ozean-, Fluss-, Wald-, Dschungel-, Taiga- und Eisbiome. Die gespeicherten Biomeinträge belegen Abdeckung in dieser Stichprobe, aber keine vollständige Biom- oder Erreichbarkeitsgarantie.

### Technische Nachtests

- `python3 -m tools.balance_experiment probe-surfaces --pack experiments/balance-v24/behavior_pack --results experiments/balance-large-v24/verification`: Boden 3/3, Decke 3/3, Wand 3/3 erfolgreich. Kontrollierter Hohlraum, kein Beweis natürlicher Verteilung.
- `python3 -m tools.balance_experiment verify-mining --pack experiments/balance-v24/behavior_pack --results experiments/balance-large-v24/verification --index 0`: simuliertes `setblock air` blieb nach Neustart entfernt; keine weiteren Änderungen in diesem Messgebiet. Kein echter Spielerabbau.
- `python3 -m tools.balance_experiment trace-ores --pack experiments/balance-v24/behavior_pack --results experiments/balance-large-v24/verification --index 0`: in der ausgewählten Probe Vanilla-Wiederholungen identisch, keine zusätzlichen oder entfernten Positionen der geprüften anderen Erztypen. Das ist keine vollständige Blockprüfung.
- Normaler lokaler Add-on-Engine-Test mit Neustart/Fingerprint: Vanilla zeigte eine geänderte Fingerprint-Chunk-ID, der getrennte Add-on-Testlauf keine geänderten Fingerprint-Chunks; die normalen Erzpositionen blieben in diesem Lauf stabil. Ein separater kombinierter Feature-Test und Luftkontakt-/Gegenrichtungs-Test liefen ohne Server- oder JSON-Fehler. Das ist keine direkte V24- oder Realm-Garantie.
- `python3 -m unittest discover -s tests -v`: 84 Tests bestanden. `docker compose config --quiet`: erfolgreich. Diese Prüfungen ersetzen weder echte Spieler- noch Realm-Tests.

### Befund und offene Freigabepunkte

V24 ist nach diesem großen Holdout ein plausibler lokaler Kandidat: Tunnel-/Y=−57-Reduktion liegt nahe 15 %, die Fundstellen liegen knapp im Arbeitskorridor und die gewünschte 3/4-Gruppenmehrheit ist im großen Scan erfüllt. Eine Freigabe erfolgt noch nicht. Offen bleiben reale Spielzeitvergleiche (Tunnel Y=−57 gegen Höhlen), Werkzeug-/Verzauberungs-/Explosionsverhalten, Leistung mit zwei Spielern, Versionsabgleich, Test-Realm sowie PC-/PlayStation-/Switch-Beitritt. Bis dahin kein Produktions-`.mcpack` und kein GitHub-Release.

## V25: Adergrößen und unabhängiger 15-Seed-Holdout (6. November 2026)

V25 ist eine eigene V24-Kopie mit den Gewichten 1/2/35/52/10 für versuchte Größen 1/2/3/4/5. Pack-Hash: `5b4e7b84e8bf5a35b21d3db0544ed0017f83f2e99822c9459694242f0ff21206`. Kleine Kalibrierung: 32/23 Gruppen, 31/118 Y=-57-Erze, 202/1103 Tunnelkontakte, Größen 1/2/3/4/5 = 1/8/16/6/1. Große V24-Kalibrierung: 1729/1630 Gruppen, 906/6564 Y=-57, 7968/52810 Tunnelkontakte, Größen 1/2/3/4/5/7 = 92/453/754/382/42/6; diese Gebiete sind kein unabhängiger Nachweis.

Der vorab festgelegte Plan `reference/balance-holdout-plan-2026-11-06-v25.json` umfasste 15 bisher unbenutzte Seeds mit je 32×32 Chunks. Vanilla wurde zuerst eingefroren, V25 danach in denselben Gebieten gemessen:

| Kennzahl | Vanilla | V25 | Anteil |
| --- | ---: | ---: | ---: |
| Luftkontakt-Fundstellen | 1509 | 1629 | **108,0 %** |
| eingeschlossene Erze Y=-57 | 6683 | 1045 | **15,6 %** |
| eingeschlossene Erze Y=-59..-55 | 33087 | 4977 | **15,0 %** |
| überlappende Tunnelkontakte | 52884 | 8107 | **15,3 %** |

Die Holdout-Gruppen 1/2/3/4/5/6 = 113/394/722/364/34/2; 3er+4er bilden 66,7 %. `experiments/balance-v25/holdout-uncertainty.json` enthält die gebietsweise Bootstrap-Unsicherheit: 99,3–117,0 % Fundstellen, 14,0–17,4 % Y=-57 und 14,5–16,1 % Tunnelkontakte (2,5–97,5 %).

Kontrolltests: `probe-surfaces` Boden/Decke/Wand jeweils 3/3; `verify-mining` nur simuliertes `setblock air` über Neustart; `trace-ores` in der ausgewählten Probe ohne Abweichung bei den geprüften anderen Erztypen. Kein echter Spielerabbau und keine vollständige Weltprüfung. Alle 15 Gebiete liefen ohne Scanner- oder Serverabbruch. V25 bleibt eine lokale Testversion ohne Produktions- oder Realm-Freigabe.

## V26: Vierergruppen für den ersten Spieltest (8. November 2026)

V26 verwendet als eigene V25-Variante die Gewichte 1/1/25/64/10 für versuchte Größen 1/2/3/4/5. Pack-Hash: `ec60528ea113e0f44633a1af020ab83f6ff7dada5e2df1a87dc1105c90bd7cfd`.

Die 15 großen V24-Kalibriergebiete ergaben:

| Kennzahl | Vanilla | V26 | Anteil |
| --- | ---: | ---: | ---: |
| Luftkontakt-Fundstellen | 1630 | 1732 | **106,3 %** |
| eingeschlossene Erze Y=-57 | 6564 | 906 | **13,8 %** |
| eingeschlossene Erze Y=-59..-55 | 32891 | 5053 | **15,4 %** |
| überlappende Tunnelkontakte | 52810 | 7969 | **15,1 %** |

Gruppengrößen 1/2/3/4/5/6/7/8: **90/381/736/461/59/1/3/1**. Dreier- und Vierergruppen bilden 69,1 %; Vierer sind mit 461 gegenüber 381 Zweiergruppen häufiger. Diese Gebiete wurden bereits zur V24-Kalibrierung verwendet und sind kein unabhängiger V26-Holdout.

Kontrolltests: Boden/Decke/Wand jeweils 3/3; simuliertes `setblock air` blieb nach Neustart entfernt. In der ausgewählten Erzpositionsprobe wurden zwei Tiefenschiefer-Goldpositionen gegenüber Vanilla entfernt; andere Erze sind daher nicht als unverändert garantiert. Der 32×32-Scanner verwendet nun 30 Sekunden Ladewartezeit und bricht bei ungeladenen Chunks ab. V26 ist für einen entbehrlichen lokalen Spieltest geeignet, aber weiterhin nicht für Realm, Produktion oder Release freigegeben.
