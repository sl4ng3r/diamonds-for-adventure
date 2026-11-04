# Balance-Test v2 – nicht freigegeben

Diese eigenständige Testvariante baut auf dem Stand von `experiments/balance-v1` auf. Sie erhöht die Versuche für einzelne Höhlenboden-Erze von eins auf zwei pro Chunk und die Versuche für vergrabene Erzvorkommen ebenfalls auf zwei pro Chunk. Der vergrabene Versuchsbereich reicht wieder von Y=−64 bis 16, damit oberhalb von −32 nicht alle vergrabenen Diamantvorkommen entfallen. Das sind experimentelle Parameter; die Verteilung über die Höhe und die Ziele müssen gemessen werden.

Das Pack überschreibt Vanilla-Features und ist ausschließlich für Wegwerfwelten. Keine Freigabe für bestehende Welten oder Realms. EULA, Referenz, Testgrenzen und Betrieb: `experiments/balance-v1/README.md` und `AGENTS.md`.

Nach Docker-Start und EULA-Zustimmung pro Gebiet eine neue Welt erzeugen; vorhandene Ergebnisse werden nicht überschrieben:

```sh
python3 -m tools.balance_experiment scan --pack experiments/balance-v2/behavior_pack --results experiments/balance-v2/results --index 0
python3 -m tools.balance_experiment summarize --results experiments/balance-v2/results
```

Die Indizes 0–19 entsprechen denselben 20 Vanilla-Referenzgebieten wie v1. `area-NN.json` speichert einen Prüfsummen-Fingerabdruck des Packs und der Referenz; unterschiedliche Stände dürfen nicht in einem Ergebnisordner vermischt werden.

## Ergebnis der ersten Messung

20 von 20 Referenzgebieten wurden einmal untersucht, siehe `summary.json` und `results/`. Die Höhlen-Näherung fand 16 statt 23 Vanilla-Luftkontaktgruppen (69,6 %, Ziel ungefähr 115 %). Im Tunnelmodell wurden 125 statt 1.103 Erzblock-Kontakte gezählt (11,3 %); auf Y=−57 waren 21 statt 118 zunächst eingeschlossene Erze vorhanden (17,8 %), im Bereich −59 bis −55 72 statt 727 (9,9 %). Die Messung umfasst kleine Stichproben und überlappende Modellwege, keine echten Spielzeiten. V2 verfehlt das Höhlenziel und ist nicht freigegeben. V3 prüft einen weiteren Höhlenversuch pro Chunk, bei sonst gleicher vergrabener Erzgenerierung.
