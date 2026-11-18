"""Build V38 without the narrow deep cave rule that may cluster finds near Y=-40."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v37/behavior_pack'
TARGET = ROOT / 'experiments/balance-v38/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    (target / 'feature_rules/cave_deep_extra2.json').unlink()
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V38 Spatial Balance Experiment'
    manifest['header']['description'] = (
        'Forschungsvariante ohne die schmale tiefe Zusatzregel; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
