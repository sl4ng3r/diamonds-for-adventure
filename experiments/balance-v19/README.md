# V19 – zusätzlicher tiefer Versuch (Kandidat, noch nicht freigegeben)

V19 ist der aktuelle lokal geprüfte Kandidat. Er verwendet acht gleichgewichtete horizontale Richtungsreihenfolgen inklusive Umkehrungen, einen tiefen Durchlauf Y=-64..-33 plus einen zusätzlichen tiefen Durchlauf mit 50-%-Chance, einen mittleren Durchlauf Y=-32..-1 mit 90-%-Chance und **keine** obere Höhlen-Feature-Regel. Die vergrabene Diamanterzregel verwendet drei statt zwei Durchläufe. Alle Änderungen sind neue Feature-Platzierungen und überschreiben die identifizierten Vanilla-Diamantfeatures; Kompatibilitätsrisiken bleiben bestehen.

Kalibrierung (20 Gebiete): 29 gegenüber 23 Vanilla-Luftkontaktgruppen (126,1 %), 31/118 eingeschlossene Erze auf Y=-57 (26,3 %) und 202/1.103 Kontakte im Tunnelmodell (18,3 %). Gruppengrößen 1/2/3/4/5: 3/7/13/5/1.

Unabhängiger Holdout (sechs neue Seeds, 1.536 Chunks, 164 Vanilla-Gruppen): 166 Kandidatengruppen (101,2 %), 112/660 auf Y=-57 (17,0 %) und 803/5.598 Tunnelkontakte (14,3 %). Gruppengrößen 1/2/3/4/5: 25/44/66/27/4; 3er+4er bilden damit die Mehrheit. Die Fundstellenquote liegt leicht unter dem Arbeitskorridor 105–125 %, ist aber im unabhängigen Vergleich nahe am Vanilla-Mittel; zusammen mit der Kalibrierung 195/187 = 104,3 %. Die Werte sind keine Spielerträge pro Stunde.

Technische Gegenproben: Boden, Decke und Wand platzierten in je drei kontrollierten Versuchen erfolgreich Erz; Ost-/West-Vorladen einer negativen 4×4-Region ergab identische 83 Erzpositionen. Zwei simulierte `setblock air`-Abbauproben ließen den entfernten Block nach Neustart entfernt. Ein gezielter Erzvergleich fand eine zusätzliche Tiefenschiefer-Lapisposition; andere Erztypen sind daher nicht vollständig garantiert unverändert. Diese Tests ersetzen keinen echten Spieler-, Performance- oder Realm-Test.

Reproduzierbare Auswertung:

```sh
python3 -m tools.balance_batch status --pack experiments/balance-v19/behavior_pack --results experiments/balance-v19/results
python3 -m tools.balance_batch status --pack experiments/balance-v19/behavior_pack --results experiments/balance-v19/holdout-results --reference reference/balance-holdout-v19-1.26.61.1-2026-11-04.json
python3 -m tools.holdout_uncertainty --results experiments/balance-v19/holdout-results --output experiments/balance-v19/holdout-uncertainty.json
```
