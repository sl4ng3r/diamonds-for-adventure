"""Build a V29-derived cave-vein experiment using Bedrock ore features."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v29/behavior_pack'
TARGET = ROOT / 'experiments/balance-v35/behavior_pack'
VEIN_WEIGHTS = ((1, 1), (2, 1), (3, 25), (4, 64), (5, 10))


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V35 Ore Vein Experiment'
    manifest['header']['description'] = (
        'Forschungsvariante: natürliche Aderform an Höhlenflächen; nicht freigegeben'
    )
    write_json(manifest_path, manifest)

    write_json(target / 'features/cave_vein_choice.json', {
        'format_version': '1.21.40',
        'minecraft:weighted_random_feature': {
            'description': {'identifier': 'cavediamonds:cave_vein_choice'},
            'features': [[f'cavediamonds:cave_ore_n{size}', weight]
                         for size,weight in VEIN_WEIGHTS],
        },
    })
    for size,_ in VEIN_WEIGHTS:
        write_json(target / f'features/cave_ore_n{size}.json', {
            'format_version': '1.26.50',
            'minecraft:ore_feature': {
                'description': {'identifier': f'cavediamonds:cave_ore_n{size}'},
                'count': size,
                'replace_rules': [
                    {'places_block': 'minecraft:diamond_ore',
                     'may_replace': ['minecraft:stone']},
                    {'places_block': 'minecraft:deepslate_diamond_ore',
                     'may_replace': ['minecraft:deepslate']},
                ],
            },
        })
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
