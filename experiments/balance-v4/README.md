# Balance-Test v4 – nicht freigegeben

Wie v3, aber vier statt drei Höhlenboden-Platzierungsversuche pro Chunk; vergrabene Vorkommen bleiben bei zwei Versuchen mit Startpunkten von Y=−64 bis 16. Diese Variante ist für Messungen, überschreibt Vanilla-Features und ist nicht für echte Welten oder Realms freigegeben. Einzelne Höhlenplatzierungen erzeugen je einen Erzblock; die resultierende Adergrößenverteilung ist zu prüfen.

Nach EULA-Zustimmung und Docker-Start die 20 Vanilla-Referenzgebiete (Indizes 0–19) messen; vorhandene Ergebnisse werden nicht überschrieben:

```sh
python3 -m tools.balance_experiment scan --pack experiments/balance-v4/behavior_pack --results experiments/balance-v4/results --index 0
python3 -m tools.balance_experiment summarize --results experiments/balance-v4/results
python3 -m tools.balance_profiles --results experiments/balance-v4/results
```

Fortsetzung, Testgrenzen und bisherige Resultate: `AGENTS.md` und die READMEs der vorherigen Varianten.

## Ergebnis

In allen 20 Referenzgebieten ergab die Luftkontakt-Näherung 38 Gruppen gegenüber 23 in Vanilla (165,2 %, statt der angestrebten ungefähr 115 %). Das Tunnelmodell ergab 125/1.103 Kontakte (11,3 %), die übrigen Einschränkungen und Höhenwerte entsprechen weitgehend v3. Die Stichprobe ist klein, aber v4 liegt darin deutlich über dem gewählten Höhlen-Richtwert und ist nicht freigegeben. Details `summary.json` und `results/`.
