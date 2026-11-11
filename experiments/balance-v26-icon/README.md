# V26-Testpaket mit Icon

`cave-diamonds-v26-icon-test.mcpack` ist eine reine Darstellungsaktualisierung des
V26-Behavior-Packs: dieselbe Pack-UUID und Generierung, Pack-Version 0.1.1
statt 0.1.0 und ein `pack_icon.png` im Pack-Hauptverzeichnis. Es gibt kein
separates Ressourcenpaket. Das ursprüngliche V26-Forschungspaket bleibt erhalten.

Erzeugen mit `python3 -m tools.build_v26_icon_package`. Die Originalmessungen
beziehen sich auf das unveränderte V26-Paket; diese Variante ist weiterhin ein
nicht für Realms freigegebenes Testpaket. Import und Anzeige in Minecraft müssen
auf dem Zielgerät geprüft werden. Vor einer Änderung einer bestehenden Welt
ein Backup erstellen.

Das regulär veröffentlichte Paket `cave-diamonds-v0.1.2.mcpack` hat den
Anzeigenamen „Cave Diamonds“ und eine neue Packversion. Icon und
Weltgenerierungsregeln entsprechen 0.1.1. Erzeugen, sofern das Ziel noch nicht
existiert: `python3 -m tools.build_v26_release`. Spielbalance, Realm- und
Konsolenverhalten sind weiterhin nicht abschließend getestet.
