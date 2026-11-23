"""Build the V60 candidate with whole-vein thinning."""

import argparse
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

from tools.build_v57_dist import build_package
from tools.build_v59 import ROOT, build_pack as build_v59, write_feature, write_json


EXPERIMENT = ROOT / 'experiments/balance-v60'
TARGET = EXPERIMENT / 'behavior_pack'
VERSION = (0, 1, 13)
DIST = ROOT / 'data/package-archive/cave-diamonds-v0.1.13.mcpack'


def build_pack(target=TARGET):
    target = build_v59(target)
    rules = target / 'feature_rules'
    features = target / 'features'
    old_rules = ('thin_overworld', 'thin_upper_overworld')
    for name in old_rules:
        (rules / f'{name}.json').unlink()
    for name in ('scan_chunk', 'scan_upper_chunk', 'select_ore', 'select_upper_ore',
                 'thin_diamond', 'thin_deepslate', 'thin_upper_diamond', 'thin_upper_deepslate',
                 'diamond_ore_buried_feature'):
        (features / f'{name}.json').unlink()

    write_feature(target, 'vein_pending_block', 'single_block_feature', {
        'places_block': 'minecraft:barrier',
        'may_replace': ['minecraft:bedrock'],
        'enforce_placement_rules': False,
        'enforce_survivability_rules': False,
    })
    write_feature(target, 'vein_pending_chunk', 'scatter_feature', {
        'places_feature': 'cavediamonds:vein_pending_block',
        'distribution': {
            'iterations': 2,
            'x': {'distribution': 'fixed_grid', 'extent': [0, 1], 'step_size': 1},
            'y': 0,
            'z': 8,
        },
    })
    write_json(rules / 'vein_pending_rule.json', {
        'format_version': '1.21.40',
        'minecraft:feature_rules': {
            'description': {
                'identifier': 'cavediamonds:vein_pending_rule',
                'places_feature': 'cavediamonds:vein_pending_chunk',
            },
            'conditions': {
                'placement_pass': 'final_pass',
                'minecraft:biome_filter': {
                    'any_of': [{'test': 'has_biome_tag', 'value': tag}
                               for tag in ('overworld', 'overworld_generation')],
                },
            },
            'distribution': {'iterations': 1, 'x': 0, 'y': -64, 'z': 0},
        },
    })
    shutil.copytree(EXPERIMENT / 'runtime', target / 'scripts')
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V60 Whole Veins'
    manifest['header']['description'] = 'Testpaket für den Erhalt ganzer Höhlenadern.'
    manifest['modules'].append({
        'type': 'script', 'language': 'javascript', 'entry': 'scripts/main.js',
        'uuid': 'aa45232e-bcad-4307-a63c-b8c89582e6b9', 'version': [0, 1, 0],
    })
    manifest['dependencies'] = [{'module_name': '@minecraft/server', 'version': '2.11.0'}]
    write_json(manifest_path, manifest)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', action='store_true', help=f'Build {DIST.name}')
    if parser.parse_args().package:
        with TemporaryDirectory() as directory:
            print(build_package(DIST, VERSION, source=build_pack(Path(directory) / 'behavior_pack')))
    else:
        print(build_pack())


if __name__ == '__main__':
    main()
