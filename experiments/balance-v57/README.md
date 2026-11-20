# V57 – obere Höhlenhäufung nachschärfen

Nicht freigegebener Kandidat auf Basis von V56. Anlass: In sechs bereits verwendeten Referenzgebieten lagen luftberührte Erzgruppen bei Y=−15..−1 mit 31/24 = 129,2 % und bei Y=0..16 mit 12/9 = 133,3 % von Vanilla, während insgesamt 188/164 = 114,6 % gemessen wurden. Diese kleinen Zähler erlauben keine Garantie für einzelne Welten.

V57 ändert nur die mittlere Höhlenregel: Startpunkte Y=−32..−17 statt −32..−1, `scatter_chance` 8 statt 15. Die Reduktion ist ein Einstellversuch, keine bekannte Prozentwirkung der Engine. Wegen des Oberflächensuchradius 12 können Erze weiterhin oberhalb und unterhalb der Startpunkte entstehen. Die tiefe Höhlenregel, die obere Regel mit geplantem Maximum +30, beide Filter für vollständig eingeschlossene Erze und alle übrigen Generierungsdateien bleiben bytegleich zu V56. Ob dadurch die zusätzlichen Gruppen bei Y=−15..−1 sinken **und** die Häufigkeit um Y=−40 erhalten bleibt, muss die Messung zeigen.

Die Messung verwendet nur neue Kandidatenwelten und die bereits gespeicherten Vanilla-Rohscans; kein neuer Vanilla-Scan. Die sechs Gebiete wurden schon mehrfach zur Kalibrierung verwendet und sind kein unabhängiger Holdout:

```sh
python3 -m tools.balance_followup status --plan experiments/balance-v57/secondary-plan.json
python3 -m tools.balance_followup run --plan experiments/balance-v57/secondary-plan.json --limit 1
python3 -m tools.cave_spatial_compare --plan experiments/balance-v57/secondary-plan.json
python3 -m tools.buried_height_compare --plan experiments/balance-v57/secondary-plan.json
```

V56 zeigte in einem anderen großen Gebiet starke Laufzeitprobleme des Scans; deren Ursache ist ungeklärt. V57 ist deshalb keine automatische Freigabe für eine Spielwelt oder einen Realm.

## Gemessener Stand

Sechs Gebiete/1.536 Chunks abgeschlossen: insgesamt **181/164 = 110,4 %** luftberührte Gruppen, im Band −47..−32 **57/52 = 109,6 %**, bei −15..−1 **24/24 = 100 %**, bei 0..16 **10/9 = 111,1 %**. Damit liegt die Gesamtsumme im unteren Teil des Zielkorridors; das auffällige Band −15..−1 hat keinen Zuwachs mehr. Von 181 luftberührten Vanilla-Erzpositionen blieben 180 erhalten; eine Position bei (−68668, −23, 30624) in einer Tropfsteinhöhle fehlte in diesem Lauf. Die Änderung der Weltgenerierung garantiert also keine exakte Positionserhaltung. Vollständig eingeschlossen oberhalb −20: **1.417/4.815 = 29,4 % Erzblöcke**, aber **945/1.984 = 47,6 % Gruppen**. Oberhalb +16 kein Fund in dieser Serie.

Im oberen Bereich Y=−19..16 blieben alle **49 direkt luftberührten Vanilla-Erzpositionen** erhalten; eine zusätzliche Position kam hinzu. Die einzelne verlorene Position liegt tiefer bei Y=−23. Nach der Nutzerentscheidung, dass rund +10 % insgesamt ausreichen, wurde V57 lokal als feste Paketversion `dist/cave-diamonds-v0.1.9.mcpack` abgelegt. Das nächste lokale Release `dist/cave-diamonds-v0.1.10.mcpack` enthält dieselbe Generierung und unterscheidet sich nur durch die Manifest-Version. V58 prüfte nur ein einzelnes Gebiet und wird nicht weiter verfolgt. Die Rohscans wurden gegen gespeicherte Vanilla-Scans derselben sechs Gebiete verglichen, nicht gegen neue unabhängige Welten.
