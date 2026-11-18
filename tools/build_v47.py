"""Tune buried diamond count above Y=-20 while preserving V46 rules."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v46/behavior_pack'
TARGET = ROOT / 'experiments/balance-v47/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    feature_path = target / 'features/sparse_buried.json'
    feature = json.loads(feature_path.read_text())
    body = feature['minecraft:ore_feature']
    if body['count'] != 4:
        raise ValueError('unexpected V46 upper buried size')
    body['count'] = 5
    feature_path.write_text(json.dumps(feature, ensure_ascii=False, indent=2) + '\n')
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V47 Upper Buried Balance'
    manifest['header']['description'] = (
        'Forschungsvariante: seltene eingeschlossene Erze oberhalb von Y=-20; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
