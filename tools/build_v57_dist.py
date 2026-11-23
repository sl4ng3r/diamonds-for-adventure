"""Build a versioned Cave Diamonds V57 package in dist/."""

import argparse
import json
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v57/behavior_pack'
ICON = ROOT / 'experiments/balance-v26-icon/pack_icon.png'
TARGET = ROOT / 'dist/cave-diamonds-v0.1.9.mcpack'
VERSION = [0, 1, 9]


def build_package(target=TARGET, version=VERSION, *, source=SOURCE):
    target = Path(target)
    manifest = json.loads((source / 'manifest.json').read_text())
    manifest['header']['name'] = 'Cave Diamonds'
    manifest['header']['description'] = (
        'Diamanten in Höhlen entdecken und seltener in tiefem Gestein finden.'
    )
    manifest['header']['version'] = list(version)
    for module in manifest['modules']:
        module['version'] = list(version)

    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob('*')):
            if path.is_file() and path.name != 'manifest.json':
                archive.write(path, path.relative_to(source).as_posix())
        archive.writestr('manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        archive.write(ICON, 'pack_icon.png')
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', default='0.1.9', help='Paketversion, z. B. 0.1.10')
    args = parser.parse_args()
    parts = args.version.split('.')
    if len(parts) != 3 or not all(part.isdecimal() for part in parts):
        parser.error('--version muss aus drei nichtnegativen Zahlen bestehen')
    version = [int(part) for part in parts]
    target = ROOT / 'dist' / f'cave-diamonds-v{args.version}.mcpack'
    print(build_package(target, version=version))


if __name__ == '__main__':
    main()
