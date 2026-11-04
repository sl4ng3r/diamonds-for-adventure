# Diamonds for Adventure

Ein Forschungsprojekt für ein **Minecraft-Bedrock-Behavior-Pack**: Diamanten sollen sich vor allem beim Erkunden von Höhlen lohnen, während langes Tunnelgraben auf Y = −57 nur noch selten erfolgreich ist.

**Projektstatus:** Das Add-on befindet sich in Entwicklung; ein Release folgt nach Abschluss der Tests.

## Ziel und aktueller Stand

- Ungefähr 15 % mehr getrennte Höhlenfundstellen als in Vanilla; die Adern sollen dabei nicht größer werden.
- Auf Y = −57 sollen beim Tunnelgraben nur noch selten Diamanten gefunden werden. Die tatsächliche Ausbeute pro Spielzeit ist noch nicht gemessen.
- Normale Diamanterze und Spielmechaniken sollen erhalten bleiben; Tests mit Realms, Konsolen, Verzauberungen und echten Spielern stehen noch aus.

Der ursprüngliche Versuch, vergrabene Erze nach der normalen Weltgenerierung auszudünnen, funktionierte in natürlichen Welten nicht zuverlässig. Die aktuelle Forschungsvariante **V8** ersetzt bestimmte Vanilla-Diamantfeatures und erzeugt normale Diamanterze neu. Sie probiert Höhlenboden, Wand und Decke sowie tiefer gewichtete Startpunkte; dies weicht vom ursprünglichen Ansatz ab und erhält originale Adern nicht garantiert.

In 20 ausgewählten Testgebieten fanden sich 42 luftberührte Erzgruppen gegenüber 23 in Vanilla – deutlich mehr als das angestrebte Plus von ungefähr 15 %. Einzelne Erzblöcke an Wand, Boden und Decke wurden gemessen; ein künstlicher Raum bestätigte die direkte Platzierung auf allen drei Flächen. Die tatsächlichen Höhlenfunde lagen trotz tiefer gewichteter Startpunkte nicht überwiegend ganz unten. Luftkontakt beweist keine Erreichbarkeit. Andere Erzarten können sich durch die veränderte Generierung ebenfalls unterscheiden. Details, frühere Versuche und Grenzen stehen im [Testbericht](TESTREPORT.md) und in [AGENTS.md](AGENTS.md).

## Aufbau

| Pfad | Inhalt |
| --- | --- |
| `prototype/behavior_pack/` | Ursprünglicher, in natürlichen Welten fehlgeschlagener Prototyp. |
| `experiments/` | Getrennte Forschungsvarianten, Messergebnisse und Dokumentation; insbesondere [V8](experiments/balance-v8/README.md). |
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

Der Healthcheck prüft den Serverprozess, nicht das Add-on. Die Compose-Umgebung aktiviert bei einer neuen Testwelt den **ursprünglichen Prototyp**, nicht V8. Der Server nutzt Online-Authentifizierung und eine Allowlist. Port und Version sind in `.env` konfigurierbar; bei späterer Portänderung ist auch `server-port` in der bereits vorhandenen `data/server.properties` zu prüfen. `data/` enthält persistente Welten und wird bei Updates nicht automatisch ersetzt. Deploy Cockpit hat die Compose-Konfiguration lokal erkannt; eine Installation darüber wurde noch nicht nachgewiesen.

## Forschungsvariante messen

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
