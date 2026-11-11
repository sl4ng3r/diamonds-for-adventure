"""Build the named 0.1.2 release from the preserved V26 icon package."""
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'experiments/balance-v26-icon'
SOURCE = DIRECTORY / 'cave-diamonds-v26-icon-test.mcpack'
TARGET = DIRECTORY / 'cave-diamonds-v0.1.2.mcpack'


def main():
    with zipfile.ZipFile(SOURCE) as source, zipfile.ZipFile(TARGET, 'x', zipfile.ZIP_DEFLATED) as target:
        for name in source.namelist():
            data = source.read(name)
            if name == 'manifest.json':
                manifest = json.loads(data)
                manifest['header']['name'] = 'Cave Diamonds'
                manifest['header']['description'] = 'Diamanten in Höhlen entdecken und seltener in tiefem Gestein finden.'
                manifest['header']['version'] = [0, 1, 2]
                for module in manifest['modules']:
                    module['version'] = [0, 1, 2]
                data = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
            target.writestr(name, data)
    print(TARGET)


if __name__ == '__main__':
    main()
