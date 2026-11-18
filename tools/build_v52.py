"""Reduce upper buried ore toward 30% of Vanilla blocks."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v51/behavior_pack'
TARGET = ROOT / 'experiments/balance-v52/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    rule_path = target / 'feature_rules/upper_buried_rule.json'
    rule = json.loads(rule_path.read_text())
    distribution = rule['minecraft:feature_rules']['distribution']
    if distribution['scatter_chance'] != 45:
        raise ValueError('unexpected V51 upper buried frequency')
    distribution['scatter_chance'] = 6
    rule_path.write_text(json.dumps(rule, ensure_ascii=False, indent=2) + '\n')
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V52 Upper Buried Reduction'
    manifest['header']['description'] = (
        'Forschungsvariante: weniger eingeschlossene Erze oberhalb von Y=-20; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
