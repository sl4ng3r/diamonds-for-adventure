"""Restore a small upper-middle cave attempt while retaining V57's lower band."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v57/behavior_pack'
TARGET = ROOT / 'experiments/balance-v58/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    source_path = target / 'feature_rules/cave_mid_rule.json'
    rule = json.loads(source_path.read_text())
    body = rule['minecraft:feature_rules']
    if body['distribution']['y']['extent'] != [-32, -17] or body['distribution']['scatter_chance'] != 8:
        raise ValueError('unexpected V57 middle cave rule')
    body['description']['identifier'] = 'cavediamonds:cave_mid_upper_rule'
    body['distribution']['y']['extent'] = [-16, -1]
    body['distribution']['scatter_chance'] = 4
    extra = target / 'feature_rules/cave_mid_upper_rule.json'
    extra.write_text(json.dumps(rule, ensure_ascii=False, indent=2) + '\n')
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V58 Upper Cave Balance'
    manifest['header']['description'] = (
        'Forschungsvariante: kleine obere mittlere Höhlenregel; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
