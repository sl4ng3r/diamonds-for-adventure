"""Limit middle cave starts to the lower half while preserving other V56 rules."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v56/behavior_pack'
TARGET = ROOT / 'experiments/balance-v57/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    rule_path = target / 'feature_rules/cave_mid_rule.json'
    rule = json.loads(rule_path.read_text())
    distribution = rule['minecraft:feature_rules']['distribution']
    if distribution['y']['extent'] != [-32, -1] or distribution['scatter_chance'] != 15:
        raise ValueError('unexpected V56 middle cave rule')
    distribution['y']['extent'] = [-32, -17]
    distribution['scatter_chance'] = 8
    rule_path.write_text(json.dumps(rule, ensure_ascii=False, indent=2) + '\n')
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V57 Upper Cave Balance'
    manifest['header']['description'] = (
        'Forschungsvariante: weniger obere Höhlenfunde; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
