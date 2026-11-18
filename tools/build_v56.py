"""Increase partial thinning of fully buried ore above Y=-20."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v55/behavior_pack'
TARGET = ROOT / 'experiments/balance-v56/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    for name in ('diamond', 'deepslate'):
        path = target / f'features/thin_upper_{name}.json'
        feature = json.loads(path.read_text())
        blocks = feature['minecraft:single_block_feature']['places_block']
        if [block['weight'] for block in blocks] != [1, 2]:
            raise ValueError(f'unexpected V55 upper thinning weights in {name}')
        blocks[0]['weight'] = 2
        blocks[1]['weight'] = 1
        path.write_text(json.dumps(feature, ensure_ascii=False, indent=2) + '\n')
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V56 Upper Buried Balance'
    manifest['header']['description'] = (
        'Forschungsvariante: eingeschlossene Erze oberhalb von Y=-20 ausdünnen; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
