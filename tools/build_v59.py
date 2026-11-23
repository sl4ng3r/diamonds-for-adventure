"""Add rare ocean cave finds to the V57 generation rules."""

import argparse
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

from tools.build_v57_dist import build_package


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v57/behavior_pack'
TARGET = ROOT / 'experiments/balance-v59/behavior_pack'
VERSION = (0, 1, 12)
DIST = ROOT / 'data/package-archive' / ('cave-diamonds-v' + '.'.join(map(str, VERSION)) + '.mcpack')
SURFACES = ('floor', 'ceiling', 'wall')
SEARCH_RANGE = 4
MAX_ORE_Y = 35


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def write_feature(target, name, feature_type, body):
    write_json(target / 'features' / f'{name}.json', {
        'format_version': '1.26.50',
        f'minecraft:{feature_type}': {
            'description': {'identifier': f'cavediamonds:{name}'},
            **body,
        },
    })


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    write_json(target / 'feature_rules/ocean_cave_rule.json', {
        'format_version': '1.21.40',
        'minecraft:feature_rules': {
            'description': {
                'identifier': 'cavediamonds:ocean_cave_rule',
                'places_feature': 'cavediamonds:ocean_cave_chance',
            },
            'conditions': {
                'placement_pass': 'final_pass',
                'minecraft:biome_filter': {'test': 'has_biome_tag', 'value': 'ocean'},
            },
            'distribution': {
                'iterations': 1,
                'x': {'distribution': 'uniform', 'extent': [0, 15]},
                'y': {'distribution': 'uniform', 'extent': [-40, MAX_ORE_Y - SEARCH_RANGE]},
                'z': {'distribution': 'uniform', 'extent': [0, 15]},
            },
        },
    })
    write_feature(target, 'ocean_cave_chance', 'scatter_feature', {
        'places_feature': 'cavediamonds:ocean_cave_surface',
        'distribution': {'iterations': 1, 'scatter_chance': 35, 'x': 0, 'y': 0, 'z': 0},
    })
    write_feature(target, 'ocean_cave_surface', 'weighted_random_feature', {
        'features': [[f'cavediamonds:ocean_cave_{surface}', 1] for surface in SURFACES],
    })
    for surface in SURFACES:
        write_feature(target, f'ocean_cave_{surface}', 'snap_to_surface_feature', {
            'feature_to_snap': 'cavediamonds:cave_select',
            'surface': surface,
            'search_range': SEARCH_RANGE,
            'embed_in_surface': True,
            'allow_air_placement': False,
            'allow_non_air_placement': False,
            'allow_underwater_placement': True,
            'allowed_surface_blocks': ['minecraft:stone', 'minecraft:deepslate'],
        })
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V59 Ocean Caves'
    manifest['header']['description'] = 'Testpaket mit zusätzlichen Diamanten in Ozeanhöhlen.'
    write_json(manifest_path, manifest)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', action='store_true', help=f'Build {DIST.name}')
    if parser.parse_args().package:
        with TemporaryDirectory() as directory:
            pack = build_pack(Path(directory) / 'behavior_pack')
            print(build_package(DIST, VERSION, source=pack))
    else:
        print(build_pack())


if __name__ == '__main__':
    main()
