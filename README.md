# Diamonds for Adventure

Ein **Minecraft-Bedrock-Behavior-Pack**: Diamanten sollen sich vor allem beim Erkunden von Höhlen lohnen, während langes Tunnelgraben auf Y = −57 nur noch selten erfolgreich ist.

## Ziel und aktueller Stand

- Etwa 10–15 % mehr **getrennte Diamanterzgruppen mit direktem Luftkontakt** als in Vanilla. Luftkontakt beweist keine Spieler-Erreichbarkeit.
- Vollständig eingeschlossene Erzblöcke oberhalb Y = −20 sollen auf ungefähr 30 % von Vanilla sinken.
- Auf Y = −57 sollen ungefähr 15 % der eingeschlossenen Erzblöcke übrig bleiben. Die tatsächliche Ausbeute pro Spielzeit ist noch nicht gemessen.
- Normale Diamanterze und Spielmechaniken sollen erhalten bleiben; Tests mit Realms, Konsolen, Verzauberungen und echten Spielern stehen noch aus.

V63 erhält ganze Adern mit Luft- oder Flüssigkeitskontakt und dünnt vollständig eingeschlossene Adern aus. Zusätzliche tiefe Höhlenfunde liegen bei Y=−48 oder tiefer. Die obere Höhlenregel reicht planmäßig bis Y=+30, die Ozeanregel bis Y=+35.

In 384 Bedrock-Testchunks blieben **alle 84 freiliegenden Adern** vollständig erhalten. Gegenüber Vanilla wurden bis Y=+16 **52 statt 44 luftberührte Fundstellen (+18,2 %)** gemessen. In den vier direkt mit V60 vergleichbaren Gebieten waren es **29 statt 26 (+11,5 %)**. Über alle sechs Gebiete blieben auf Y=−57 **21 statt 162 (13,0 %)** eingeschlossene Erzblöcke und oberhalb −20 bis +16 **285 statt 1.175 (24,3 %)**. Details und Grenzen stehen im [Testbericht zu V63](experiments/balance-v63/README.md#ergebnis).

Die aktuelle feste Paketversion ist [Cave Diamonds v0.1.16](dist/cave-diamonds-v0.1.16.mcpack). Erzeugung mit `python3 -m tools.build_v63 --package`. Vor einem Update einer bestehenden Welt eine Sicherung erstellen. Der Test hat die Ausdünnung gezielt ausgelöst. Automatische Ausführung beim Spielen und Realm-Leistung sind noch offen.

## Aufbau

| Pfad | Inhalt |
| --- | --- |
| `prototype/behavior_pack/` | Ursprünglicher, in natürlichen Welten fehlgeschlagener Prototyp. |
| `experiments/` | Getrennte Versionen, Messergebnisse und Dokumentation; insbesondere [V63](experiments/balance-v63/README.md). |
| `dist/` | Aktuelle feste Paketversion und [Ablagehinweise](dist/README.md). |
| `diagnostics/behavior_pack/` | Separates Diagnose-Skript für Testwelten; keine Produktionsabhängigkeit. |
| `reference/` | Zusammengefasste Vanilla-Referenzen und Messpläne. |
| `tools/` und `tests/` | Wiederverwendbare Engine-Vergleiche, Auswertung und automatisierte Prüfungen. |
| `data/` | Lokale Testwelten und Serverdaten; nicht im Repository enthalten. |

## Automatisierte Tests

Python 3 und Node.js werden für die lokalen Tests benötigt:

```sh
python3 -m unittest discover -s tests -v
```

Die Tests prüfen unter anderem Paketstruktur und Testwerkzeuge. Sie ersetzen keine Tests mit der Bedrock-Engine, echten Spielern oder einem Realm.

## Lokaler Bedrock-Testserver

Voraussetzungen sind Docker mit Compose und Unterstützung für `linux/amd64`. Der Server lädt beim Build den offiziellen Bedrock Dedicated Server herunter; die getestete Version ist `1.26.61.1`. Auf ARM-Rechnern wird AMD64-Emulation benötigt.

1. `.env.example` nach `.env` kopieren.
2. Die [Minecraft-EULA](https://www.minecraft.net/eula) lesen und nur bei eigener Zustimmung `EULA=TRUE` in `.env` setzen.
3. Den Testserver starten und seinen Zustand prüfen:

   ```sh
   docker compose up -d --build
   docker compose ps
   docker compose logs -f
   ```

Der Healthcheck prüft den Serverprozess, nicht das Add-on. Die Compose-Umgebung aktiviert bei einer neuen Testwelt den **ursprünglichen Prototyp**, nicht V63. Der Server nutzt Online-Authentifizierung und eine Allowlist. Port und Version sind in `.env` konfigurierbar; bei späterer Portänderung ist auch `server-port` in der bereits vorhandenen `data/server.properties` zu prüfen. Das Docker-Subnetz ist über `BEDROCK_NETWORK_SUBNET` einstellbar und muss frei von Überschneidungen mit lokalen Netzen, VPNs und anderen Docker-Netzen sein. Ein bestehendes Compose-Netz muss nach einer Subnetzänderung neu erstellt werden; dabei wird der Testserver kurz unterbrochen. `data/` enthält persistente Welten und wird bei Updates nicht automatisch ersetzt. Deploy Cockpit hat die Compose-Konfiguration lokal erkannt; eine Installation darüber wurde noch nicht nachgewiesen.

## Ältere V8-Vergleiche

Nach Aufbau des Testservers und Zustimmung zur EULA können neue V8-Vergleiche in isolierten Wegwerfwelten ausgeführt werden:

```sh
python3 -m tools.balance_batch status --pack experiments/balance-v8/behavior_pack --results experiments/balance-v8/results-neu
python3 -m tools.balance_batch run --pack experiments/balance-v8/behavior_pack --results experiments/balance-v8/results-neu --limit 3
python3 -m tools.balance_experiment probe-surfaces --pack experiments/balance-v8/behavior_pack --results experiments/balance-v8/verification-neu
```

Der Sammellauf speichert jedes Gebiet einzeln, kann nach Unterbrechungen fortgesetzt werden und verweigert die Vermischung unterschiedlicher Paket- und Referenzstände. Die dokumentierten alten Ergebnisse sind eingecheckt; ihre zugehörigen **Rohscans und Testwelten unter `data/` fehlen nach einem frischen Clone**. Daher können etwa die Höhen- und Flächenauswertungen alter Ergebnisse ohne Wiederherstellung dieser lokalen Daten nicht vollständig neu berechnet werden. Für neue Vergleiche müssen passende Rohscans und eine dazugehörige Referenz lokal erzeugt werden; bestehende Ergebnisse und Referenzen nicht überschreiben. Weitere Hinweise stehen in [reference/README.md](reference/README.md) und [AGENTS.md](AGENTS.md).

## Grenzen und Sicherheit der Welt

Vor einem späteren Einsatz ist eine Sicherung der Welt erforderlich. Bereits betrachtete, aber von Bedrock nicht dauerhaft gespeicherte Gebiete können beim erneuten Laden mit geänderter Weltgenerierung neu entstehen. Entfernte Erze werden beim Deaktivieren eines Packs nicht automatisch wiederhergestellt. Andere weltgenerierende Add-ons und experimentelle Weltoptionen sind nicht geprüft.

Der lokale Server ist eine Testumgebung; der geplante spätere Betrieb auf einem Realm benötigt keinen eigenen Server.
