"""Build V33 with fewer deep and more mid-height cave attempts than V32."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v32/behavior_pack'
TARGET = ROOT / 'experiments/balance-v33/behavior_pack'
DEEP_RULES = ('cave_rule', 'cave_deep_extra', 'cave_deep_extra2')


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V33 Height Redistribution'
    write_json(manifest_path, manifest)

    old_wrapper = target / 'features/cave_regular_chance.json'
    old_wrapper.unlink()
    for name,chance in (('deep',20),('mid',60)):
        write_json(target / f'features/cave_{name}_chance.json', {
            'format_version': '1.21.40',
            'minecraft:scatter_feature': {
                'description': {'identifier': f'cavediamonds:cave_{name}_chance'},
                'places_feature': 'cavediamonds:cave_snap_choice',
                'distribution': {
                    'iterations': 1, 'scatter_chance': chance,
                    'x': 0, 'y': 0, 'z': 0,
                },
            },
        })
    for name in DEEP_RULES + ('cave_mid_rule',):
        path = target / 'feature_rules' / f'{name}.json'
        rule = json.loads(path.read_text())
        layer = 'mid' if name == 'cave_mid_rule' else 'deep'
        rule['minecraft:feature_rules']['description']['places_feature'] = (
            f'cavediamonds:cave_{layer}_chance'
        )
        write_json(path, rule)
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
