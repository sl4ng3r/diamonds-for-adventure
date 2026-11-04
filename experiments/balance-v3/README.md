# Balance-Test v3 – nicht freigegeben

Forschungsvariante gegenüber v2: drei statt zwei einzelne Höhlenboden-Platzierungsversuche je Chunk; vergrabenes Erz bleibt bei zwei Feature-Versuchen mit Startpunkten von Y=−64 bis 16. Das sind Startwerte für Messungen, keine bereits nachgewiesenen Balancequoten. Sie überschreibt Vanilla-Diamantfeatures und verwendet Vanilla-Diamanterz. Keine Freigabe für Welten oder Realms.

Für die 20 Vanilla-Referenzgebiete jeweils eine entbehrliche neue Welt erzeugen, pro Index 0–19:

```sh
python3 -m tools.balance_experiment scan --pack experiments/balance-v3/behavior_pack --results experiments/balance-v3/results --index 0
python3 -m tools.balance_experiment summarize --results experiments/balance-v3/results
```

Vorbedingungen und Einschränkungen: `AGENTS.md` und `experiments/balance-v1/README.md`. Die Untersuchungen berücksichtigen noch keine echte Spielerreichbarkeit, Werkzeuge, Ader-Vollständigkeit, Spielzeit, Mehrspielerleistung oder Realm-Kompatibilität. Ergebnispfade sind durch Prüfsummen gegen vermischte Pack- oder Referenzstände geschützt.

## Erste Auswertung

Alle 20 Referenzgebiete wurden einmal gemessen: 23 luftberührte Erzgruppen gegenüber 23 in Vanilla (100 %, Ziel etwa 115 %). Das Tunnelmodell ergab 125 gegenüber 1.103 Erzblock-Kontakten (11,3 %); eingeschlossene Erze auf Y=−57 21 gegenüber 118 (17,8 %) und im Band −59 bis −55 72 gegenüber 727 (9,9 %). Dies sind begrenzte Stichproben beziehungsweise überlappende Modellwege, keine Spielzeiten.

Alle 23 erkannten Höhlengruppen der Testvariante bestehen aus einem Block; Vanilla hatte 15 Einzel- und acht Zweiergruppen. Die vereinfachte Gruppierung ist kein vollständiger Nachweis natürlicher Adergröße. V3 erfüllt deshalb die gewünschte Erhöhung nicht und kann auch Adern verkleinern. `balance-v4` untersucht einen zusätzlichen Höhlenversuch. Keine Freigabe.
