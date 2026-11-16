# Diamonds for Adventure

Ein **Minecraft-Bedrock-Behavior-Pack**: Diamanten sollen sich vor allem beim Erkunden von Höhlen lohnen, während langes Tunnelgraben auf Y = −57 nur noch selten erfolgreich ist.

## Ziel und aktueller Stand

- Ungefähr 15 % mehr getrennte Höhlenfundstellen als in Vanilla; die Adern sollen dabei nicht größer werden.
- Auf Y = −57 sollen beim Tunnelgraben nur noch selten Diamanten gefunden werden. Die tatsächliche Ausbeute pro Spielzeit ist noch nicht gemessen.
- Normale Diamanterze und Spielmechaniken sollen erhalten bleiben; Tests mit Realms, Konsolen, Verzauberungen und echten Spielern stehen noch aus.

Der ursprüngliche Versuch, vergrabene Erze nach der normalen Weltgenerierung auszudünnen, funktionierte in natürlichen Welten nicht zuverlässig. Der aktuelle Kandidat **V29** ersetzt bestimmte Vanilla-Diamantfeatures und erzeugt normale Diamanterze neu. Er probiert Höhlenboden, Wand und Decke; dies weicht vom ursprünglichen Ansatz ab und erhält originale Adern nicht garantiert.

In zwölf ausgewählten Gebieten hatte V29 349 luftberührte Erzgruppen gegenüber 308 in Vanilla, also 13,3 % mehr. Die Streuung zwischen Gebieten ist groß; Luftkontakt beweist keine Erreichbarkeit. Auf Y=−57 blieben in sechs Gebieten 114 statt 674 eingeschlossene Erzblöcke. Andere Erzarten können sich durch die veränderte Generierung ebenfalls unterscheiden. Details und Grenzen stehen in der [V29-Auswertung](experiments/balance-v29/README.md) und in [AGENTS.md](AGENTS.md).

Die aktuelle feste Paketversion ist [Cave Diamonds v0.1.4](dist/cave-diamonds-v0.1.4.mcpack). Sie wird mit `python3 -m tools.build_v29_dist` unter `dist/` erzeugt. Die Versionsnummer ist keine Bestätigung für Realm- oder Konsolenkompatibilität; vor Einsatz in einer bestehenden Welt ist eine Sicherung nötig.

## Aufbau

| Pfad | Inhalt |
| --- | --- |
| `prototype/behavior_pack/` | Ursprünglicher, in natürlichen Welten fehlgeschlagener Prototyp. |
| `experiments/` | Getrennte Versionen, Messergebnisse und Dokumentation; insbesondere [V29](experiments/balance-v29/README.md). |
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

Der Healthcheck prüft den Serverprozess, nicht das Add-on. Die Compose-Umgebung aktiviert bei einer neuen Testwelt den **ursprünglichen Prototyp**, nicht V8. Der Server nutzt Online-Authentifizierung und eine Allowlist. Port und Version sind in `.env` konfigurierbar; bei späterer Portänderung ist auch `server-port` in der bereits vorhandenen `data/server.properties` zu prüfen. Das Docker-Subnetz ist über `BEDROCK_NETWORK_SUBNET` einstellbar und muss frei von Überschneidungen mit lokalen Netzen, VPNs und anderen Docker-Netzen sein. Ein bestehendes Compose-Netz muss nach einer Subnetzänderung neu erstellt werden; dabei wird der Testserver kurz unterbrochen. `data/` enthält persistente Welten und wird bei Updates nicht automatisch ersetzt. Deploy Cockpit hat die Compose-Konfiguration lokal erkannt; eine Installation darüber wurde noch nicht nachgewiesen.

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
