# V26 – Testkandidat für den ersten Spieltest

V26 ist eine eigene Variante auf Basis von V25. Die Adergrößen-Gewichte wurden auf **1/1/25/64/10** für versuchte Größen 1/2/3/4/5 geändert. Damit werden Zweiergruppen weiter reduziert und Vierergruppen stärker bevorzugt. Richtungswahl, Höhenregeln, Fundstellenhäufigkeit und die Reduktion vergrabener Erze bleiben unverändert.

Pack-Hash: `ec60528ea113e0f44633a1af020ab83f6ff7dada5e2df1a87dc1105c90bd7cfd`

## Große Kalibrierung

Auf den 15 bereits für V24 verwendeten großen Gebieten (daher **keine unabhängige Bestätigung**) ergab V26:

| Kennzahl | Vanilla | V26 | V26/Vanilla |
| --- | ---: | ---: | ---: |
| Luftkontakt-Fundstellen | 1.630 | 1.732 | **106,3 %** |
| eingeschlossene Erze Y=-57 | 6.564 | 906 | **13,8 %** |
| eingeschlossene Erze Y=-59..-55 | 32.891 | 5.053 | **15,4 %** |
| überlappende Tunnelkontakte | 52.810 | 7.969 | **15,1 %** |

Die Gruppengrößen 1/2/3/4/5/6/7/8 waren **90/381/736/461/59/1/3/1**. Dreier- und Vierergruppen bilden damit 1.197 von 1.732 Gruppen (**69,1 %**). Vierergruppen sind erstmals häufiger als Zweiergruppen. Die Messung nutzt dieselben Gebiete wie die V24-Kalibrierung und dient nur der Auswahl für einen Spieltest.

Die 20 kleinen Gebiete ergaben 31/23 Fundstellen (134,8 %), 31/118 Y=-57-Erze (26,3 %) und 202/1103 Tunnelkontakte (18,3 %). Die Stichprobe ist für diese Werte zu klein; die große Kalibrierung ist maßgeblich.

## Kontrollen

- Kontrollierter Hohlraum: Boden, Decke und Wand jeweils 3/3 erfolgreich.
- `setblock air`-Probe: entfernte Erzposition blieb nach Neustart entfernt; kein echter Spielerabbau.
- Erzpositionsprobe: Vanilla-Wiederholung identisch; V26 zeigte in der ausgewählten Probe zwei entfernte Tiefenschiefer-Goldpositionen gegenüber Vanilla. Die genaue Engine-Reihenfolge ist ungeklärt; andere Erze sind nicht garantiert unverändert.
- Der große Scanner benötigt für 32×32-Gebiete eine verlängerte Ladewartezeit von 30 Sekunden und bricht bei weiterhin ungeladenen Chunks ab.

## Testpaket und Grenzen

`cave-diamonds-v26-test.mcpack` ist nur ein lokales Testpaket. Vor dem Aktivieren eine entbehrliche Welt und ein Backup verwenden. Der Kandidat wurde noch nicht unabhängig mit neuen Seeds bestätigt und nicht auf einem Realm geprüft. Echte Spielzeitvergleiche, Mehrspielerleistung, Versionsabgleich, PC-/PlayStation-/Switch-Beitritt sowie Werkzeug-, Verzauberungs- und Explosionstests bleiben offen.
