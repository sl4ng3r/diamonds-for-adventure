"""Build V40 with shorter cave-surface searches for deep placement rules."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v37/behavior_pack'
TARGET = ROOT / 'experiments/balance-v40/behavior_pack'
DEEP_RULES = ('cave_rule', 'cave_deep_extra', 'cave_deep_extra2')
FACES = ('floor', 'ceiling', 'wall')


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V40 Short Deep Search Experiment'
    manifest['header']['description'] = (
        'Forschungsvariante mit kürzerer Tiefen-Oberflächensuche; nicht freigegeben'
    )
    write_json(manifest_path, manifest)

    for face in FACES:
        source = target / f'features/cave_snap_{face}.json'
        feature = json.loads(source.read_text())
        body = feature['minecraft:snap_to_surface_feature']
        if body['search_range'] != 12:
            raise ValueError(f'unexpected V37 search range: {source}')
        body['description']['identifier'] = f'cavediamonds:cave_snap_{face}_deep'
        body['search_range'] = 6
        write_json(target / f'features/cave_snap_{face}_deep.json', feature)

    choice = json.loads((target / 'features/cave_snap_choice.json').read_text())
    weighted = choice['minecraft:weighted_random_feature']
    weighted['description']['identifier'] = 'cavediamonds:cave_snap_choice_deep'
    weighted['features'] = [[f'cavediamonds:cave_snap_{face}_deep', 1] for face in FACES]
    write_json(target / 'features/cave_snap_choice_deep.json', choice)

    for name in DEEP_RULES:
        path = target / f'feature_rules/{name}.json'
        rule = json.loads(path.read_text())
        description = rule['minecraft:feature_rules']['description']
        if description['places_feature'] != 'cavediamonds:cave_snap_choice':
            raise ValueError(f'unexpected V37 feature in {path}')
        description['places_feature'] = 'cavediamonds:cave_snap_choice_deep'
        write_json(path, rule)
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
