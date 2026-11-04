# Adergrößen – Testvariante V9

Nicht für Spielwelten freigegeben. V9 übernimmt die V8-Startpunkte und die Bodensuche, Wandsuche und Deckensuche. Die Auswahl der gewünschten Zahl von Platzierungsversuchen je Fundstelle ist zunächst 1/2/3/4/5 mit Gewichten 5/15/35/35/10. Das sind Arbeitsannahmen, keine gemessenen Fundhäufigkeiten.

Ein zentraler Block und bis zu vier direkt angrenzende Positionen werden versucht. Flächen, Gestein, Reihenfolge und andere Platzierungen können das Ergebnis verändern, einschließlich getrennten oder zusammengewachsenen Gruppen. Die Auswahl enthält feste Richtungen; ein ausnutzbares Muster muss geprüft werden. Die früheren Risiken der Vanilla-Overrides und das offene Balancing gelten weiter.

Fortsetzen: `python3 -m tools.balance_batch run --pack experiments/balance-v9/behavior_pack --results experiments/balance-v9/results --limit 3`. Gruppenverteilung: `python3 -m tools.balance_profiles --results experiments/balance-v9/results`. Ergebnisse einzelner Gebiete sind atomar gespeichert; keinen vorhandenen Teststand überschreiben.

Engine-Stichprobe: alle 20 Referenzgebiete, 42 luftberührte Gruppen. Größen 1/2/3/4/5: 1/17/11/9/4. Drei oder vier kamen insgesamt 20-mal vor, zwei allein 17-mal; damit ist die gewünschte Häufigkeitsverteilung noch nicht überzeugend erreicht. Die Gruppen sind keine garantierten natürlichen Adern. Die 42 V9-Gruppen stehen 23 Vanilla-Gruppen gegenüber; dies verfehlt auch weiterhin das frühere Fundstellenziel. Die ausgewählten Gebiete sind keine unabhängige repräsentative Stichprobe.
