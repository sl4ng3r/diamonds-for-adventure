"""Partially thin buried ore above Y=-20 while preserving exposed ore."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v54/behavior_pack'
WEIGHTED_SOURCE = ROOT / 'experiments/balance-v42/behavior_pack/features'
TARGET = ROOT / 'experiments/balance-v55/behavior_pack'


def write_json(path, document):
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n')


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    (target / 'feature_rules/upper_buried_rule.json').unlink()
    (target / 'features/sparse_buried.json').unlink()

    rule = json.loads((target / 'feature_rules/thin_overworld.json').read_text())
    body = rule['minecraft:feature_rules']
    body['description'] = {'identifier': 'cavediamonds:thin_upper_overworld',
                           'places_feature': 'cavediamonds:scan_upper_chunk'}
    body['distribution']['y'] = -19
    write_json(target / 'feature_rules/thin_upper_overworld.json', rule)

    scan = json.loads((target / 'features/scan_chunk.json').read_text())
    body = scan['minecraft:scatter_feature']
    body['description']['identifier'] = 'cavediamonds:scan_upper_chunk'
    body['places_feature'] = 'cavediamonds:select_upper_ore'
    body['distribution']['y']['extent'] = [0, 35]
    body['distribution']['iterations'] = 16 * 16 * 36
    write_json(target / 'features/scan_upper_chunk.json', scan)

    choice = json.loads((target / 'features/select_ore.json').read_text())
    body = choice['minecraft:aggregate_feature']
    body['description']['identifier'] = 'cavediamonds:select_upper_ore'
    body['features'] = ['cavediamonds:thin_upper_diamond',
                        'cavediamonds:thin_upper_deepslate']
    write_json(target / 'features/select_upper_ore.json', choice)

    for name, host, ore in (('diamond', 'minecraft:stone', 'minecraft:diamond_ore'),
                            ('deepslate', 'minecraft:deepslate', 'minecraft:deepslate_diamond_ore')):
        feature = json.loads((WEIGHTED_SOURCE / f'thin_{name}.json').read_text())
        body = feature['minecraft:single_block_feature']
        body['description']['identifier'] = f'cavediamonds:thin_upper_{name}'
        body['places_block'] = [{'block': host, 'weight': 1}, {'block': ore, 'weight': 2}]
        write_json(target / f'features/thin_upper_{name}.json', feature)

    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V55 Partial Upper Thinning'
    manifest['header']['description'] = (
        'Forschungsvariante: eingeschlossene obere Erze anteilig ausdünnen; nicht freigegeben'
    )
    write_json(manifest_path, manifest)
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
