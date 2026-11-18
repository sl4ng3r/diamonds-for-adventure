"""Reduce the size of added buried diamond deposits above Y=-20."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v53/behavior_pack'
TARGET = ROOT / 'experiments/balance-v54/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    feature_path = target / 'features/sparse_buried.json'
    feature = json.loads(feature_path.read_text())
    body = feature['minecraft:ore_feature']
    if body['count'] != 8:
        raise ValueError('unexpected V53 upper buried vein size')
    body['count'] = 3
    feature_path.write_text(json.dumps(feature, ensure_ascii=False, indent=2) + '\n')
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V54 Upper Buried Reduction'
    manifest['header']['description'] = (
        'Forschungsvariante: kleinere vergrabene Adern oberhalb von Y=-20; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
