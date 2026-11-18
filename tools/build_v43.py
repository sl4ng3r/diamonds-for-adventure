"""Build V43 with certain replacement of eligible buried diamond ore."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v42/behavior_pack'
TARGET = ROOT / 'experiments/balance-v43/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    for name, host in (('thin_diamond', 'minecraft:stone'),
                       ('thin_deepslate', 'minecraft:deepslate')):
        path = target / f'features/{name}.json'
        feature = json.loads(path.read_text())
        body = feature['minecraft:single_block_feature']
        if not isinstance(body['places_block'], list):
            raise ValueError(f'unexpected V42 placement choices in {path}')
        body['places_block'] = host
        path.write_text(json.dumps(feature, ensure_ascii=False, indent=2) + '\n')
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V43 Certain Late Thinning Experiment'
    manifest['header']['description'] = (
        'Diagnose: Vanilla-Höhlenadern und sichere späte Ausdünnung; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
