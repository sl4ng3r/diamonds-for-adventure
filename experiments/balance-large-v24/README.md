# V24 großer Holdout

Dieser Ordner enthält den großen, vorab festgelegten 15-Seed-Vergleich des unveränderten V24-Kandidaten. Er ist ein lokaler Forschungs- und Teststand, kein freigegebenes Add-on.

## Reproduzierbarkeit

- Plan: `reference/balance-large-plan-2026-11-04-v24.json`
- Vanilla-Referenz: `reference/balance-large-v24-1.26.61.1-2026-11-05.json`
- Kandidatenpack: `../balance-v24/behavior_pack`
- Server: Bedrock Dedicated Server 1.26.61.1, `linux/amd64`
- Gebiet: 32×32 Kern-Chunks je Seed, mit gepufferten Ticking-Area-Fenstern
- Ergebnisse: `holdout-results/area-00.json` bis `area-14.json`
- Unsicherheit: `holdout-uncertainty.json`

Status prüfen:

```sh
python3 -m tools.balance_batch status \
  --pack experiments/balance-v24/behavior_pack \
  --results experiments/balance-large-v24/holdout-results \
  --reference reference/balance-large-v24-1.26.61.1-2026-11-05.json
```

Auswertungen:

```sh
python3 -m tools.balance_profiles \
  --results experiments/balance-large-v24/holdout-results \
  --reference reference/balance-large-v24-1.26.61.1-2026-11-05.json

python3 -m tools.balance_experiment summarize \
  --results experiments/balance-large-v24/holdout-results \
  --reference reference/balance-large-v24-1.26.61.1-2026-11-05.json
```

## Ergebnis

Vanilla hatte 1.630, V24 1.730 luftberührte technische Fundstellen (106,1 %). Eingeschlossene Erze auf Y=−57 lagen bei 6.564 zu 906 (13,8 %), das Tunnelmodell bei 52.810 zu 7.963 Kontakten (15,1 %). Die V24-Gruppen 1/2/3/4/5/7 waren 219/556/643/265/41/6. Drei- und Vierergruppen bildeten zusammen 52,5 %.

Die Bootstrap-Perzentile über vollständige Gebiete betragen 97,7–114,3 % für Fundstellen, 13,0–14,7 % für Y=−57 und 14,3–15,9 % für Tunnelkontakte. Luftkontakt ist nur eine Näherung; die technische Gruppierung beweist weder vollständige natürliche Adern noch Spieler-Erreichbarkeit.

## Grenzen

Die Gebiete sind vorab festgelegt, aber nicht weltweit repräsentativ. Randkomponenten werden separat gezählt und können abgeschnitten sein. Der Scan misst keine Diamanten pro Spielstunde. Echte Spieler-, Leistungs- und Realm-/Konsolentests fehlen weiterhin. Die Rohwelten unter `data/research/` bleiben erhalten und werden nicht automatisch gelöscht.
