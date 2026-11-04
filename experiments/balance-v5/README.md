# Balance-Test v5 – nicht freigegeben

Wie v3 (drei Höhlen- und zwei vergrabene Versuche pro Chunk), aber pro Höhlenplatzierung wird zusätzlich mit 70 % Wahrscheinlichkeit versucht, **höchstens einen** benachbarten Erzblock in einer zufällig gewählten Richtung zu setzen. Dadurch sollen neben Einzelblöcken auch kleine Zweiergruppen möglich sein. Mehrere Versuche können sich berühren; eine maximale natürliche Adergröße ist damit nicht garantiert. Die Platzierungsregeln und ihre Laufzeitwirkung müssen in der Engine geprüft werden.

Das Pack ist eine Forschungskopie mit Vanilla-Feature-Overrides, nicht für bestehende Welten oder Realms freigegeben. Die `aggregate_feature`-Reihenfolge ist nicht garantiert; mögliche Neustart- und Chunkgrenzeffekte sind offen. Keine Rückschlüsse auf echte Erreichbarkeit, Spielertrag oder Realm-Kompatibilität allein aus Luftkontaktgruppen.

Nach EULA-Zustimmung und Docker-Start die 20 Referenzgebiete (Indizes 0–19) vergleichen:

```sh
python3 -m tools.balance_experiment scan --pack experiments/balance-v5/behavior_pack --results experiments/balance-v5/results --index 0
python3 -m tools.balance_experiment summarize --results experiments/balance-v5/results
python3 -m tools.balance_profiles --results experiments/balance-v5/results
```

Ausgaben sind durch Pack- und Referenzprüfsummen geschützt. Weitere Tests und vorherige Ergebnisse: `AGENTS.md`.

## Erste Auswertung

In 20 Referenzgebieten wurden 24 luftberührte Gruppen gegenüber 23 Vanilla-Gruppen gefunden (104,3 % statt ungefähr 115 %). Von diesen Gruppen hatten 15 zwei und neun einen Block; Vanilla hatte acht Zweier- und 15 Einergruppen. Nach dieser unvollständigen Näherungsmethode sind Testgruppen also im Mittel größer. Das Tunnelmodell ergab 125/1.103 Kontakte (11,3 %); auf Y=−57 21/118 eingeschlossene Erze (17,8 %). Kleine Stichprobe, keine echten Spielzeiten oder vollständig erkannten Adern. V5 ist nicht freigegeben. V6 prüft eine niedrigere Nachbarwahrscheinlichkeit und eine zusätzliche gelegentliche Höhlenplatzierung.
