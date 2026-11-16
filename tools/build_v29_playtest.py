"""Package the measured V29 files for a disposable-world Bedrock playtest."""

import json
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v29/behavior_pack'
ICON = ROOT / 'experiments/balance-v26-icon/pack_icon.png'
TARGET = ROOT / 'experiments/balance-v29/cave-diamonds-v29-playtest.mcpack'
VERSION = [0, 1, 3]


def build_package(target=TARGET):
    target = Path(target)
    manifest = json.loads((SOURCE / 'manifest.json').read_text())
    manifest['header']['name'] = 'Cave Diamonds'
    manifest['header']['description'] = (
        'V29 Test für neue Wegwerfwelten: mehr getrennte Höhlenfunde, '
        'obere Diamanterze bis geplant Y=30. Nicht für Realm oder Spielwelt freigegeben.'
    )
    manifest['header']['version'] = VERSION
    for module in manifest['modules']:
        module['version'] = VERSION

    with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(SOURCE.rglob('*')):
            if path.is_file() and path.name != 'manifest.json':
                archive.write(path, path.relative_to(SOURCE).as_posix())
        archive.writestr('manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        archive.write(ICON, 'pack_icon.png')
    return target


def main():
    print(build_package())


if __name__ == '__main__':
    main()
