# Höhen und Höhlenflächen – Forschungsvariante V8

**Nicht freigegeben.** Diese Variante überschreibt wie V6 Vanilla-Diamantfeatures und erbt die in `AGENTS.md` dokumentierten Probleme; sie eignet sich ausschließlich für Wegwerfwelten. Sie ist noch keine Lösung für das Balancing oder unveränderte andere Erze.

Pro Chunk werden als Startpunkt zwei Versuche gleichverteilt auf Y=−64..−33, ein Versuch auf Y=−32..−1 und mit 10 % Wahrscheinlichkeit ein Versuch auf Y=0..4 gewählt. So nimmt die angestrebte Versuchsdichte pro Höhe nach unten zu. Ein Versuch wählt Boden, Decke oder Wand mit gleichem Gewicht; die Suche nach einer passenden Fläche reicht 12 Blöcke weit. Die tatsächliche Fundhöhe und -häufigkeit hängen von Terrain, Hohlräumen, Suchverhalten und Ersatzregeln ab. Der Suchradius ist keine bewiesene strikte Obergrenze. Die optionale Ergänzung eines Nachbarblocks stammt aus V6 und kann Adern verbinden.

```sh
python3 -m tools.balance_batch status --pack experiments/balance-v8/behavior_pack --results experiments/balance-v8/results
python3 -m tools.balance_batch run --pack experiments/balance-v8/behavior_pack --results experiments/balance-v8/results --limit 3
```

Die Ausgabe zählt Erze mit Luftkontakt an den jeweiligen Seiten; ein Erz kann mehrfach gezählt werden. Ausschließliche Kontakte werden zusätzlich ausgewiesen. Luftkontakt beweist keine Erreichbarkeit und die Messung ordnet einzelne Erze keiner Feature-Regel zu. Neue Scans zählen außerdem alle gefundenen Diamanterze auf Y=17..40; das ist keine Aussage zu größeren Höhen oder zur Herkunft eines Erzes. Alte Scans ohne diese Messung ergeben `null`. Die automatische Auswertung ersetzt weder Kontrolltests noch Realm-Freigabe.

## Ergebnis der 20 Referenzgebiete

42 statt 23 luftberührte Gruppen (182,6 % von Vanilla) verfehlen den angestrebten Richtwert von etwa 115 %. Auf Y=−57 waren 21 statt 118 Erze eingeschlossen (17,8 %); das Tunnelmodell zählte 125 statt 1.103 Kontakte (11,3 %). Test-Erze mit Luftkontakt: 22 an Boden-, 27 an Wand- und 25 an Deckenflächen, mit Überschneidungen; ausschließlich Boden/Wand/Decke: 15/7/11. Höhenbänder −64..−48/−47..−32/−31..−16/−15..−1/0..16: 1/13/21/17/1. Keine Diamanterze wurden auf Y=17..40 beobachtet. Diese gewählten Gebiete sind keine repräsentative Stichprobe, Luftkontakt kein Zugänglichkeitsnachweis und Tunnelkontakte keine Spielzeiten.

Für den isolierten Flächentest wurde ein Hohlraum aus Stein hergestellt. Für jede der drei Flächen platzierten drei von drei direkten Feature-Aufrufen Erz auf der erwarteten Fläche. `verification/surface-probes.json` enthält Rohwerte und die Wegwerf-Testwelt. Wiederholung mit neuem Ergebnisordner: `python3 -m tools.balance_experiment probe-surfaces --pack experiments/balance-v8/behavior_pack --results <neuer-ordner>`.
