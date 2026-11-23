# V61 – Mehr Funde in tiefen Höhlen

V61 baut auf V60 (Paket 0.1.13) auf. Die Ausdünnung behandelt Diamantadern weiter als zusammenhängende Gruppen. Sobald eine Gruppe Luft oder Flüssigkeit berührt, bleibt sie vollständig erhalten. Neu können vollständig eingeschlossene Gruppen über Chunkgrenzen als Ganzes entfernt werden, wenn die angrenzenden Chunks geladen sind und noch ihr Markerpaar tragen. Alte, bearbeitete und unbekannte Bereiche werden geschützt.

Die Erhaltungsquote für prüfbare, vollständig eingeschlossene Adern richtet sich nach der tiefsten Erzposition. Sie beträgt 8 % bis Y=−55, 15 % zwischen Y=−54 und −20 und 22 % oberhalb −20. Die gemessenen Zielwerte beziehen sich auf Erzblöcke ohne direkten Luft- oder Flüssigkeitskontakt im Vergleich zu Vanilla. Der Schutz freiliegender Adern samt den eingeschlossenen Blöcken dahinter und der Schutz ungeklärter Chunkgrenzen erhöhen die gemessene Quote. Die Stellwerte wurden mit den gespeicherten V60-Scans angenähert.

Eine separate Regel ergänzt einzelne luftberührte Erze an tiefen Höhlenflächen. Startpunkte liegen bei Y=−62..−52, die Oberflächensuche reicht vier Blöcke weit. Die übrigen Höhlenregeln einschließlich der oberen Regel bis geplant Y=+30 und der Ozeanregel bis Y=+35 bleiben übernommen.

Feste lokale Paketdatei: `data/package-archive/cave-diamonds-v0.1.14.mcpack`. Erzeugung mit `python3 -m tools.build_v61 --package`. Für einen Spieltest sind neue oder noch unbewertete markierte Chunks relevant. Das Paket kann bereits entfernte Erze nicht wiederherstellen.

In den vier vorherigen V60-Vergleichsgebieten (256 Chunks) blieben 14/107 eingeschlossene Erzblöcke auf Y=−57 und 222/866 oberhalb −20 bis +16 übrig. Alle 39 freiliegenden Adern blieben erhalten. Die Höhlenquote blieb wie in V60 bei 27/26. In den gespeicherten Ausschnitten gab es zwischen Y=−62 und −55 keine trockene Höhlenluft. V62 konzentriert die zusätzliche Suche deshalb auf Y=−54..−52.
