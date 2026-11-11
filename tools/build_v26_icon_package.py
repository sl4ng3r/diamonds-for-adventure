"""Build the icon-only V26 update without modifying the research candidate."""
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v26/behavior_pack'
OUTPUT = ROOT / 'experiments/balance-v26-icon'


def main():
    manifest = json.loads((SOURCE / 'manifest.json').read_text())
    manifest['header']['version'] = [0, 1, 1]
    for module in manifest['modules']:
        module['version'] = [0, 1, 1]
    target = OUTPUT / 'cave-diamonds-v26-icon-test.mcpack'
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(SOURCE.rglob('*')):
            if path.is_file() and path.name != 'manifest.json':
                archive.write(path, path.relative_to(SOURCE).as_posix())
        archive.writestr('manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        archive.write(OUTPUT / 'pack_icon.png', 'pack_icon.png')
    print(target)


if __name__ == '__main__':
    main()
