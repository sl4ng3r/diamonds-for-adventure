"""Build the V30 air-exposure calibration pack from the measured V29 source."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v29/behavior_pack'
TARGET = ROOT / 'experiments/balance-v30/behavior_pack'
REGULAR_RULES = ('cave_rule', 'cave_mid_rule', 'cave_deep_extra', 'cave_deep_extra2')


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V30 Exposure Calibration'
    manifest['header']['description'] = (
        'Forschungsvariante: weniger Höhlenversuche bei gleicher Adergrößenverteilung'
    )
    write_json(manifest_path, manifest)

    for name in REGULAR_RULES:
        path = target / 'feature_rules' / f'{name}.json'
        rule = json.loads(path.read_text())
        rule['minecraft:feature_rules']['description']['places_feature'] = (
            'cavediamonds:cave_regular_chance'
        )
        write_json(path, rule)

    write_json(target / 'features/cave_regular_chance.json', {
        'format_version': '1.21.40',
        'minecraft:scatter_feature': {
            'description': {'identifier': 'cavediamonds:cave_regular_chance'},
            'places_feature': 'cavediamonds:cave_snap_choice',
            'distribution': {
                'iterations': 1,
                'scatter_chance': 45,
                'x': 0, 'y': 0, 'z': 0,
            },
        },
    })
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
