# Balance-Test v1 – nicht freigegeben

Dieser eigenständige Forschungsstand untersucht die gewünschten Ziele gegen die gespeicherte Vanilla-Referenz. Das Pack ist **nicht für bestehende Welten oder Realms freigegeben**. Die Ausgangswerte sind Hypothesen, keine nachgewiesenen Prozentzahlen.

- Vanilla-Diamantfeatures werden wie in der bisherigen Forschungsvariante überschrieben. Höhlenversuch: ein zufälliger Platzierungsversuch pro Chunk, direkt an Höhlenböden, kein Start im Wasser; jedes Feature setzt höchstens einen normalen Erzblock. Dadurch sind Adern gegenüber Vanilla möglicherweise kleiner; Anzahlen und Größen sind zu messen.
- Vergrabene Variante: ein Erzfeature-Versuch pro Chunk, Y=−64 bis −32, maximal vier Blöcke pro Versuch und Verwerfen bei Luftkontakt. Die Höhenverteilung ist ein technischer Startpunkt und keine automatisch erreichte 15-%-Quote. Wasser-/Lavakontakt und spätere Weltgenerierung müssen getrennt gemessen werden.
- Pack hat keine Produktionsskripte, nutzt aber bekannte, noch nicht vollständig überprüfte Vanilla-Overrides. Es ist nur für Bedrock Dedicated Server 1.26.61.1 mit der gespeicherten Referenz untersucht.

Nach EULA-Zustimmung und Docker-Start erzeugt jeder Befehl eine **neue Wegwerfwelt** und schreibt ein eigenständiges Ergebnis. Vorhandene Ergebnisse werden nicht überschrieben:

```sh
python3 -m tools.balance_experiment scan --pack experiments/balance-v1/behavior_pack --results experiments/balance-v1/results --index 0
python3 -m tools.balance_experiment summarize --results experiments/balance-v1/results
```

Die Referenz enthält Indizes 0 bis 19. Zunächst einige Gebiete testen und Serverlogs auf Inhaltsfehler sowie Abweichungen prüfen; dann alle Gebiete und bei Bedarf unabhängige Wiederholungen. `area-NN.json` protokolliert den Vanilla- und Add-on-Scan sowie ein grobes Tunnelmodell. Das Modell zählt überlappende alternative Tunnel, keine realen Spielzeiten oder unabhängig gezogenen Stichproben.

Offen bleiben Reproduzierbarkeit, Höhenverteilung, ausreichend viele zugängliche Höhlenfundstellen, Adergrößen, Chunkgrenzen, gespeicherte/nicht gespeicherte Gebiete, Mehrspielerleistung, Realm und Konsolen. Keine alte Welt ersetzen, kein `.mcpack` veröffentlichen und keine Trefferquote behaupten, bevor die Tests das belegen. Stand und Fortsetzung: `AGENTS.md` und `TESTREPORT.md` im Projektverzeichnis.

## Ergebnis der ersten Messung

Alle 20 Referenzgebiete wurden einmal gemessen; Details stehen in `results/area-NN.json` und `summary.json`. Überlappende virtuelle Tunnel ergaben 170 statt 1.103 Erzblock-Kontakte (15,4 % von Vanilla). Auf Y=−57 waren 24 statt 118 zunächst eingeschlossene Erze vorhanden (20,3 %); im Band −59 bis −55 waren es 104 statt 727 (14,3 %). Die Stichproben und Positionen schwanken. Dies sind weder tatsächliche Spielzeiten noch unabhängige Tunnelversuche.

Luftkontakt als unvollständiger Höhlen-Näherungswert ergab 11 statt 23 verbundene Gruppen (47,8 % von Vanilla), also weniger statt der angestrebten 115 %. Das Ziel ist klar verfehlt; 23 Vanilla-Gruppen sind zudem für eine präzise Kalibrierung wenig. V1 wählt die Startpunkte der vergrabenen Erzfeatures nur bis Y=−32; eine Ader kann die Grenze überschreiten, aber der Bereich deutlich darüber wird dadurch nicht gezielt versorgt. Daher bleibt v1 ein verworfener Forschungsstand; `balance-v2` untersucht mehr Höhlenversuche und einen breiteren Höhenbereich. Keine Freigabe.
