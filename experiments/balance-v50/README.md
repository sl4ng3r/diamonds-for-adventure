# V50 – vergrabene Zufallsfunde oberhalb −20

Der Nutzer möchte das Ausdünnen auf Y=−64..−20 begrenzen. Vergrabene Funde oberhalb −20 sollen ungefähr so häufig wie in Vanilla bleiben; die tiefe Tunnelhöhe −57 soll selten bleiben. V44 verfehlte den oberen Teil: In zwölf Gebieten waren zwischen −19 und +16 nur 1.973 statt 10.180 eingeschlossene Erzblöcke und 1.146 statt 4.143 getrennte eingeschlossene Gruppen vorhanden.

V45 hob die Unterdrückung der vergrabenen Vanilla-Quelle auf und beschränkte den späten Filter auf −64..−20. Im ersten V19-Gebiet waren alle 931 oberen Vanilla-Positionen wieder da, auf −57 aber 39/111 = 35,1 % statt ungefähr 15 %. V45 wurde deshalb verworfen. V46 unterdrückt die vergrabene Vanilla-Quelle weiterhin und ergänzt eine eigene obere vergrabene Regel nur mit Startpunkten −19..16. V46 bis V49 kalibrieren deren Adergröße und Häufigkeit; sie ändern die übrigen V44-Höhlenregeln nicht. Die neu erzeugten oberen Adern liegen nicht garantiert an denselben Koordinaten wie die Vanilla-Adern.

Erste V19-16×16-Chunk-Probe für das obere Band −19..16, nur vollständig eingeschlossene Erzblöcke und flächenweise verbundene Gruppen:

| Variante | Blöcke | Gruppen | vergraben auf −57 |
| --- | ---: | ---: | ---: |
| Vanilla | 931 | 353 | 111 |
| V44 | 156 | 89 | 16 |
| V45 | 936 | 355 | 39 |
| V46 | 785 | 462 | 16 |
| V47 | 974 | 506 | 16 |
| V48 | 1.167 | 404 | 16 |
| V49 | 1.005 | 370 | 16 |

V49 über sechs V19-Referenzgebiete/1.536 Chunks: obere vergrabene Blöcke 5.632/4.815 = 117,0 %, Gruppen 2.167/1.984 = 109,2 %. Die sichtbaren Höhlengruppen und eingeschlossenen Erze auf −57 blieben gegenüber V44 in diesen Gebieten bei 188 und 109. V50 senkt nur den oberen `scatter_chance`-Engine-Wert von 55 auf 50; der V24-Referenzlauf mit sechs anderen bereits früher verwendeten Gebieten ist begonnen. `scatter_chance`-Werte werden hier empirisch eingestellt, nicht als nachgewiesene Prozentwahrscheinlichkeiten gelesen.

Alle Referenzen waren früher für andere Varianten verwendet und sind **kein unberührter Holdout**. Die Gruppen sind technisch flächenweise verbundene Blöcke, nicht zwingend komplette natürliche Adern oder erreichbare Funde. Reproduktion und Status:

```sh
python3 -m tools.balance_followup status --plan experiments/balance-v50/calibration-plan.json
python3 -m tools.buried_height_compare --plan experiments/balance-v49/secondary-plan.json
```

V50 ist noch kein festes Paket unter `dist/`; aktuell bleibt v0.1.6 aus V44 die letzte veröffentlichte Paketdatei. Die alten Daten bleiben erhalten.
