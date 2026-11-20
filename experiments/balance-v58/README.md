# V58 – kleiner oberer mittlerer Höhlenversuch

Nicht freigegebener Kandidat auf Basis von V57. V57 reduziert die sichtbaren Fundstellen im oberen Bereich stark; nach vier von sechs früher verwendeten Referenzgebieten lagen insgesamt nur 133/123 = 108,1 % luftberührte Gruppen vor, unter dem Ziel von 110–115 %.

V58 lässt V57 vollständig bestehen und ergänzt eine getrennte mittlere Regel mit Startpunkten Y=−16..−1 und `scatter_chance: 4`. Dies ist ein empirischer Stellwert; er darf nicht als exakte Prozentwahrscheinlichkeit ausgegeben werden. Die Suche nach Höhlenflächen kann Fundhöhen über das Startband hinaus verschieben. Die eigentliche obere Regel mit geplantem Maximum +30 und die Ausdünnung eingeschlossener Erze bleiben unverändert. Erhofft ist ein kleiner Zuwachs oben, ohne um Y=−40 erneut zu viele Fundstellen zu erzeugen; das ist noch nicht gemessen.

Der eingefrorene Kandidatenplan nutzt ausschließlich gespeicherte Vanilla-Rohscans aus sechs bereits für Varianten verwendeten Gebieten. Er ist kein unabhängiger Holdout:

```sh
python3 -m tools.balance_followup status --plan experiments/balance-v58/secondary-plan.json
python3 -m tools.balance_followup run --plan experiments/balance-v58/secondary-plan.json --limit 1
python3 -m tools.cave_spatial_compare --plan experiments/balance-v58/secondary-plan.json
python3 -m tools.buried_height_compare --plan experiments/balance-v58/secondary-plan.json
```

Vor einer festen Paketversion sind die Höhenprofile, der Erhalt sichtbarer Vanilla-Positionen, die eingeschlossenen Erze und die auffällige Scanleistung erneut zu bewerten.

Ein einziges Gebiet (Index 1) wurde gemessen: insgesamt 35/32 luftberührte Gruppen statt V57s 34/32, bei −15..−1 drei statt zwei Vanilla-Gruppen. Eine der 35 luftberührten Vanilla-Erzpositionen fehlte auch hier. Da der Nutzer rund +10 % Gesamtzuwachs akzeptiert und V57 auf sechs Gebieten 110,4 % erreichte, wird V58 nicht weiter gemessen oder als festes Paket erzeugt. Die eine Gebietsmessung ist keine Gesamtschätzung.
