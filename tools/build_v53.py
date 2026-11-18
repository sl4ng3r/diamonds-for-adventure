"""Tune upper buried diamonds toward 30% of Vanilla."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v52/behavior_pack'
TARGET = ROOT / 'experiments/balance-v53/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    rule_path = target / 'feature_rules/upper_buried_rule.json'
    rule = json.loads(rule_path.read_text())
    distribution = rule['minecraft:feature_rules']['distribution']
    if distribution['scatter_chance'] != 6:
        raise ValueError('unexpected V52 upper buried frequency')
    distribution['scatter_chance'] = 2
    rule_path.write_text(json.dumps(rule, ensure_ascii=False, indent=2) + '\n')
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V53 Upper Buried Reduction'
    manifest['header']['description'] = (
        'Forschungsvariante: etwa 30 Prozent eingeschlossene Erze oberhalb von Y=-20; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
