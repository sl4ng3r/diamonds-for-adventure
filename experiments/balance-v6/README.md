# Balance-Test v6 – nicht freigegeben

Forschungsvariante auf Basis von v5: drei Höhlen-Platzierungsversuche und zusätzlich ein weiterer Versuch mit 30 % Wahrscheinlichkeit pro Chunk; pro erfolgreicher Platzierung mit 40 % Wahrscheinlichkeit Versuch für höchstens einen angrenzenden Erzblock. Vergrabene Erze wie v2–v5, zwei Versuche je Chunk mit Startpunkten Y=−64 bis 16. Diese Parameter sind Hypothesen, keine erreichten Balancequoten. Chunks mit zusätzlichem Versuch müssen nicht gleichverteilt sein; Feature-Reihenfolge und mögliche Nachbarschaftseffekte sind offen.

Nur für isolierte Wegwerfwelten, nicht freigegeben für Realms. Enthält Vanilla-Feature-Overrides und keine Produktionsskripte. EULA und Testgrenzen stehen in `AGENTS.md`.

```sh
python3 -m tools.balance_experiment scan --pack experiments/balance-v6/behavior_pack --results experiments/balance-v6/results --index 0
python3 -m tools.balance_experiment summarize --results experiments/balance-v6/results
python3 -m tools.balance_profiles --results experiments/balance-v6/results
```

Die Referenzindizes 0–19 sind einzeln fortsetzbar; Pack-/Referenzprüfsummen verhindern, dass verschiedene Varianten versehentlich zusammengezählt werden. Anschließend neues Holdout mit anderen Seeds, Größenverteilung, Neustart, tatsächlich erreichbare Höhlen sowie Realm und Konsolen prüfen. Kein `.mcpack` ausliefern, bevor die vereinbarten Kriterien erfüllt sind.

## Kalibrierung an der bisherigen Referenz

20 von 20 Gebieten gemessen, Daten in `results/` und `summary.json`: 27 luftberührte Gruppen gegenüber 23 Vanilla-Gruppen (117,4 %; gewünschte Größenordnung ca. 115 %). Die einfache Gruppenanalyse ergab 19 Einer-/acht Zweiergruppen gegenüber 15 Einer-/acht Zweiergruppen in Vanilla. Das Tunnelmodell ergab 125 gegenüber 1.103 Kontakten (11,3 %); auf Y=−57 21 gegenüber 118 eingeschlossene Erze (17,8 %), im Band −59 bis −55 72 gegenüber 727 (9,9 %). Diese Werte sind korrelierte Modellwege beziehungsweise kleine Luftkontakt-Stichproben und keine echten, garantiert erreichbaren Höhlenfunde oder Spielzeiten.

Die Parameter wurden anhand dieser Referenz ausgesucht; damit besteht Anpassungsrisiko. Die vorab festgelegten zehn neuen Gebiete in `reference/balance-holdout-plan-2026-11-04.json` müssen separat zunächst in Vanilla und dann mit diesem unveränderten Pack gemessen werden. Gruppengröße, Höhenverteilung, anderer Erzbestand und Neustarts erneut prüfen. Kein Freigabeentscheid vor Holdout, Engine-/Spiel- und Realm-Tests.

## Unabhängiger Vergleich: Ziel verfehlt

Alle zehn vorab festgelegten Vergleichsgebiete wurden mit unverändertem Pack gemessen, siehe `holdout-results/` und `holdout-summary.json`. Gegenüber Vanilla gab es 15 statt 23 luftberührte Gruppen (65,2 %), sieben statt 104 eingeschlossene Erzblöcke auf Y=−57 (6,7 %) und 47 statt 640 Kontakte im Tunnelmodell (7,3 %). Die Vanilla-Gruppen bestanden aus 13 Einzel-, sieben Zweier-, zwei Vierer- und einer Neunergruppe; beim Testpack aus zehn Einzel- und fünf Zweiergruppen. Diese kleine Stichprobe beweist weder allgemeine Quoten noch erreichbare Höhlen. Sie widerlegt aber eine verlässliche Bestätigung der gewünschten Balance und zeigt, dass natürliche größere Gruppen verloren gehen. V6 ist nicht zur Verwendung freigegeben.

Zusätzliche technische Proben: In drei Testgebieten blieb nach einem per Befehl entfernten Erz und Neustart der übrige Diamanterzbestand im untersuchten Gebiet gleich (`verification/mining-*.json`). Ein echter Spielerabbau wurde dabei nicht getestet. Zwei Positionsvergleiche ausgewählter anderer Erze ergaben je ein zusätzliches Lapiserz an einer Stelle mit Diamanterz in Vanilla; die Vanilla-Wiederholungen waren jeweils identisch (`verification/ore-trace-*.json`). Die genaue Ursache ist nicht bewiesen, aber das Ziel unveränderter anderer Erze ist damit nicht erfüllt.
