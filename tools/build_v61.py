"""Build the V61 candidate with deeper cave finds and stronger vein thinning."""

import argparse
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

from tools.build_v57_dist import build_package
from tools.build_v59 import ROOT, SURFACES, write_feature, write_json
from tools.build_v60 import build_pack as build_v60


EXPERIMENT = ROOT / 'experiments/balance-v61'
TARGET = EXPERIMENT / 'behavior_pack'
VERSION = (0, 1, 14)
DIST = ROOT / 'dist/cave-diamonds-v0.1.14.mcpack'


def build_pack(target=TARGET, *, deep_start=(-62, -52), deep_attempts=1, deep_chance=42):
    target = build_v60(target)
    path = target / 'feature_rules/cave_rule.json'
    rule = json.loads(path.read_text())
    body = rule['minecraft:feature_rules']
    body['description'] = {
        'identifier': 'cavediamonds:cave_abyss_rule',
        'places_feature': 'cavediamonds:cave_abyss_chance',
    }
    distribution = body['distribution']
    distribution['iterations'] = deep_attempts
    distribution['y']['extent'] = list(deep_start)
    distribution.pop('scatter_chance')
    write_json(path.with_name('cave_abyss_rule.json'), rule)

    write_feature(target, 'cave_abyss_chance', 'scatter_feature', {
        'places_feature': 'cavediamonds:cave_abyss_surface',
        'distribution': {'iterations': 1, 'scatter_chance': deep_chance, 'x': 0, 'y': 0, 'z': 0},
    })
    write_feature(target, 'cave_abyss_surface', 'weighted_random_feature', {
        'features': [[f'cavediamonds:cave_abyss_{surface}', 1] for surface in SURFACES],
    })
    for surface in SURFACES:
        write_feature(target, f'cave_abyss_{surface}', 'snap_to_surface_feature', {
            'feature_to_snap': 'cavediamonds:cave_select',
            'surface': surface,
            'search_range': 4,
            'embed_in_surface': True,
            'allow_air_placement': True,
            'allow_non_air_placement': False,
            'allow_underwater_placement': False,
            'allowed_surface_blocks': ['minecraft:stone', 'minecraft:deepslate'],
        })
    for source in (EXPERIMENT / 'runtime').glob('*.js'):
        shutil.copyfile(source, target / 'scripts' / source.name)
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V61 Balance'
    manifest['header']['description'] = 'Testpaket mit tieferen Höhlenfunden und Adererhalt.'
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
